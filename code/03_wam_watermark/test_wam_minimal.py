"""
WAM 最小验证：加载 checkpoint → 嵌入 32-bit 消息 → 检测解码 → 报告位精度与 PSNR。
用法: conda run -n newpatch python code/03_wam_watermark/test_wam_minimal.py
"""
import os
import sys
import json
import argparse
import tempfile

import numpy as np
import torch
from PIL import Image
from skimage.metrics import peak_signal_noise_ratio

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WAM_PROJECT = os.path.join(PROJECT_ROOT, "baselines", "wam")
sys.path.insert(0, WAM_PROJECT)

from torchvision import transforms as T

from notebooks.inference_utils import load_model_from_checkpoint, msg2str
from watermark_anything.data.transforms import unnormalize_img

MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]
img_transform = T.Compose([
    T.Resize((256, 256), interpolation=T.InterpolationMode.BILINEAR),
    T.ToTensor(),
    T.Normalize(MEAN, STD),
])


def load_wam(params_json, checkpoint, device):
    """参照学生 targeted_attack_selected_fixed.py 的 load_wam_model 逻辑"""
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
    ap.add_argument("--params_json", default=os.path.join(WAM_PROJECT, "checkpoints", "params.json"))
    ap.add_argument("--checkpoint", default=os.path.join(WAM_PROJECT, "checkpoints", "checkpoint.pth"))
    ap.add_argument("--image", default=os.path.join(PROJECT_ROOT, "demo", "fawkes_mini_example", "Aaron_Eckhart_0001.jpg"))
    ap.add_argument("--nbits", type=int, default=32)
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[WAM minimal] device={device}")
    wam = load_wam(args.params_json, args.checkpoint, device)

    img = Image.open(args.image).convert("RGB")
    # WAM 训练于 256x256，缩放输入
    img_t = img_transform(img).unsqueeze(0).to(device)  # 1,3,256,256

    msg = torch.randint(0, 2, (1, args.nbits)).to(device)
    print("[WAM minimal] target msg:", msg2str(msg[0].cpu().tolist()))

    with torch.no_grad():
        out = wam.embed(img_t, msgs=msg)
        img_w = out["imgs_w"]
        preds = wam.detect(img_w)["preds"]  # 1, (1+nbits), 256, 256

    # 解码：preds[:, 1:, :, :] > 0 得到每像素位，多数投票
    bits = (preds[0, 1:] > 0).float()          # nbits, H, W
    decoded = (bits.mean(dim=(1, 2)) > 0.5).long()
    acc = (decoded == msg[0]).float().mean().item()
    print(f"[WAM minimal] decoded msg: {msg2str(decoded.cpu().tolist())}")
    print(f"[WAM minimal] bit accuracy: {acc * 100:.2f}%")

    # PSNR
    img_np = unnormalize_img(img_t).clamp(0, 1).squeeze().permute(1, 2, 0).cpu().numpy()
    imgw_np = unnormalize_img(img_w).clamp(0, 1).squeeze().permute(1, 2, 0).cpu().numpy()
    psnr = peak_signal_noise_ratio(img_np, imgw_np, data_range=1.0)
    print(f"[WAM minimal] PSNR: {psnr:.2f} dB")

    outdir = os.path.join(PROJECT_ROOT, "assets", "wam_minimal")
    os.makedirs(outdir, exist_ok=True)
    Image.fromarray((imgw_np * 255).astype(np.uint8)).save(os.path.join(outdir, "watermarked.png"))
    Image.fromarray((img_np * 255).astype(np.uint8)).save(os.path.join(outdir, "original.png"))
    print(f"[WAM minimal] outputs saved to {outdir}")


if __name__ == "__main__":
    main()
