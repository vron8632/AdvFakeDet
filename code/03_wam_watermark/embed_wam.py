"""
WAM 水印嵌入工具（供 B/C/D 组复用）。
- B 组: 全局嵌入（mask=全 1）
- C 组: 安全区域图引导嵌入（mask=1-R）
- D 组: C + 频域中低频掩码

用法示例（全局）:
  python code/03_wam_watermark/embed_wam.py --input_dir assets/experiments/A_low/input \
    --out_dir assets/experiments/B_global_wm --mode global --device cuda
"""
import argparse
import json
import os
import sys
import tempfile

import numpy as np
import torch
from PIL import Image
from torchvision import transforms as T

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WAM_PROJECT = os.path.join(PROJECT_ROOT, "baselines", "wam")
sys.path.insert(0, WAM_PROJECT)

from notebooks.inference_utils import load_model_from_checkpoint  # noqa
from watermark_anything.data.transforms import unnormalize_img  # noqa

MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]
img_transform = T.Compose([
    T.Resize((256, 256), interpolation=T.InterpolationMode.BILINEAR),
    T.ToTensor(),
    T.Normalize(MEAN, STD),
])


def load_wam(params_json, checkpoint, device):
    with open(params_json, "r", encoding="utf-8") as f:
        params = json.load(f)
    base_dir = os.path.dirname(params_json)
    for key in ("embedder_config", "augmentation_config", "extractor_config", "attenuation_config"):
        val = params.get(key)
        if not val or os.path.isabs(val):
            continue
        proj_cand = os.path.normpath(os.path.join(WAM_PROJECT, val))
        param_cand = os.path.normpath(os.path.join(base_dir, val))
        if os.path.exists(proj_cand):
            params[key] = proj_cand
        elif os.path.exists(param_cand):
            params[key] = param_cand
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
        json.dump(params, tmp)
        tmp_json = tmp.name
    try:
        wam = load_model_from_checkpoint(tmp_json, checkpoint)
    finally:
        os.remove(tmp_json)
    wam = wam.to(device).eval()
    return wam


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_dir", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--mode", default="global", choices=["global", "safety_map", "safety_map_freq"])
    ap.add_argument("--nbits", type=int, default=32)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--params_json", default=os.path.join(WAM_PROJECT, "checkpoints", "params.json"))
    ap.add_argument("--checkpoint", default=os.path.join(WAM_PROJECT, "checkpoints", "checkpoint.pth"))
    ap.add_argument("--safety_map_dir", default=None, help="C/D 组的安全区域图目录（与原图同名 *_map.png）")
    ap.add_argument("--alpha", type=float, default=1.0, help="水印强度缩放")
    ap.add_argument("--scaling_w", type=float, default=None, help="覆盖 WAM scaling_w")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[embed_wam] device={device} mode={args.mode}")
    wam = load_wam(args.params_json, args.checkpoint, device)
    if args.scaling_w is not None:
        wam.scaling_w = args.scaling_w
        print(f"[embed_wam] scaling_w set to {args.scaling_w}")

    os.makedirs(args.out_dir, exist_ok=True)
    imgs = sorted(f for f in os.listdir(args.input_dir) if f.lower().endswith((".jpg", ".jpeg", ".png")) and "cloaked" in f)
    if not imgs:
        imgs = sorted(f for f in os.listdir(args.input_dir) if f.lower().endswith((".jpg", ".jpeg", ".png")))
    print(f"[embed_wam] images: {len(imgs)}")

    # 安全图模式：加载 *_map.npy（112x112 敏感度 R）→ S = 1 - R 上采样到原图尺寸
    safety_maps = {}
    if args.mode in ("safety_map", "safety_map_freq"):
        assert args.safety_map_dir, "safety_map 模式需要 --safety_map_dir"
        for fname in imgs:
            stem = fname.rsplit(".", 1)[0]
            mp = os.path.join(args.safety_map_dir, f"{stem}_map.npy")
            if not os.path.exists(mp):
                continue
            safety_maps[stem] = np.load(mp)  # 112x112 in [0,1] 敏感度
        print(f"[embed_wam] safety maps loaded: {len(safety_maps)}/{len(imgs)}")

    rng = np.random.RandomState(args.seed)
    manifest = []
    for i, fname in enumerate(imgs):
        path = os.path.join(args.input_dir, fname)
        img = Image.open(path).convert("RGB")
        orig_size = img.size  # (W, H)
        img_t = img_transform(img).unsqueeze(0).to(device)

        msg = rng.randint(0, 2, (1, args.nbits)).astype(np.int64)
        msg_t = torch.from_numpy(msg).to(device)

        with torch.no_grad():
            out = wam.embed(img_t, msgs=msg_t)
            img_w = out["imgs_w"]  # 1,3,256,256

        # 反归一化（WAM 输出在 imagenet 归一化空间）
        img_w_pil = T.ToPILImage()(unnormalize_img(img_w[0].cpu()).clamp(0, 1))
        img_w_pil = img_w_pil.resize(orig_size, Image.BILINEAR)

        # 安全图模式：残差加权 C = B + alpha * S * delta
        stem = fname.rsplit(".", 1)[0]
        if args.mode in ("safety_map", "safety_map_freq") and stem in safety_maps:
            B_np = np.array(img.convert("RGB")).astype(float) / 255.0
            W_np = np.array(img_w_pil.convert("RGB")).astype(float) / 255.0
            delta = W_np - B_np
            S = 1.0 - safety_maps[stem]
            S_up = np.array(Image.fromarray((S * 255).astype(np.uint8)).resize(orig_size, Image.BILINEAR)).astype(float) / 255.0
            S_up = S_up[..., None]
            C_np = np.clip(B_np + args.alpha * S_up * delta, 0, 1)
            img_w_pil = Image.fromarray((C_np * 255).astype(np.uint8))

        # 保真输出（原尺寸全局水印）
        out_name = fname.replace(".jpg", "_wm.jpg").replace(".jpeg", "_wm.jpg").replace(".png", "_wm.jpg")
        img_w_pil.save(os.path.join(args.out_dir, out_name), quality=95)

        # 质量指标
        a = np.array(img.convert("RGB")).astype(float) / 255.0
        b = np.array(img_w_pil.convert("RGB")).astype(float) / 255.0
        mse = np.mean((a - b) ** 2)
        psnr = 10 * np.log10(1.0 / (mse + 1e-12))
        manifest.append({"image": out_name, "src": fname, "msg": msg.tolist()[0], "psnr": round(psnr, 2)})
        if (i + 1) % 20 == 0:
            print(f"[embed_wam] {i + 1}/{len(imgs)}")

    with open(os.path.join(args.out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"[embed_wam] done, saved to {args.out_dir}")


if __name__ == "__main__":
    main()
