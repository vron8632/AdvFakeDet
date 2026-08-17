"""
InvisMark (WACV 2025) 基线评估：在 Fawkes 遮蔽图上嵌入+解码，与 WAM/本文方法对比。
- 嵌入: InvisMark encoder (256x256, 100-bit uuid secret)
- 解码: InvisMark decoder, bit accuracy (threshold 0.5)
- 鲁棒: JPEG(80/50)
- 质量: PSNR/SSIM（相对遮蔽图）
用法:
  CUDA_VISIBLE_DEVICES=0 python code/06_eval/eval_invismark.py \
    --input_dir assets/experiments/A_mid/input --out_dir assets/experiments/invismark_mid \
    --n 200 --jpeg 80,50
"""
import argparse
import io
import json
import os
import sys

import numpy as np
import torch
from PIL import Image
import torchvision.transforms as transforms

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INVISMARK = os.path.join(PROJECT_ROOT, "baselines", "invismark")
sys.path.insert(0, INVISMARK)

import train  # noqa: E402
import metrics  # noqa: E402

CKPT = os.path.join(PROJECT_ROOT, "assets", "weights", "invismark", "paper.ckpt")
NBITS = 100


def load_model(device):
    sd = torch.load(CKPT, map_location="cpu", weights_only=False)
    cfg = sd["config"]
    m = train.Watermark(cfg, device=device).to(device)
    m.load_model(CKPT)
    # 注意: Watermark 类重载了 eval()(评估API)，不要调用 nn.Module.eval()
    return m


def to_tensor(img_pil):
    t = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ])
    return t(img_pil).unsqueeze(0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_dir", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--jpeg", default="80,50")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = load_model(device)
    rng = np.random.RandomState(args.seed)

    imgs = sorted(f for f in os.listdir(args.input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png')) and 'invismark' not in f)
    imgs = [f for f in imgs if not f.endswith('_cloaked_invismark.png')][:args.n]
    os.makedirs(args.out_dir, exist_ok=True)
    manifest = []
    results = []

    for i, fname in enumerate(imgs):
        path = os.path.join(args.input_dir, fname)
        img = Image.open(path).convert("RGB")
        orig_size = img.size
        x = to_tensor(img)  # InvisMark _encode 内部自行搬运到 self.device，输入需在 CPU

        secret = rng.randint(0, 2, (1, NBITS)).astype(np.float32)
        secret_t = torch.from_numpy(secret).to(device)

        with torch.no_grad():
            out, _, _ = model._encode(x, secret_t)
            dec = model._decode(out.to(device))  # out 已在 device，显式保证
        # 输出张量搬运到 CPU 计算指标
        dec = dec.cpu()
        dec_bits = (dec[0] > 0.5).float()
        acc = float((dec_bits == secret_t[0].cpu()).float().mean().item())

        # 反归一化保存 (out 在 device 上)
        wm_pil = transforms.ToPILImage()((out[0].cpu() * 0.5 + 0.5).clamp(0, 1))
        out_name = fname.replace(".jpeg", "_invismark.png")
        wm_pil = wm_pil.resize(orig_size, Image.BILINEAR)
        wm_pil.save(os.path.join(args.out_dir, out_name))

        a = np.array(img).astype(float) / 255.0
        b = np.array(wm_pil).astype(float) / 255.0
        mse = np.mean((a - b) ** 2)
        psnr = 10 * np.log10(1.0 / (mse + 1e-12))
        # SSIM 简版（灰度结构相似度，与 WAM 评估一致口径）
        from skimage.metrics import structural_similarity as ssim_fn
        ssim_val = float(ssim_fn(a, b, channel_axis=2, data_range=1.0))

        manifest.append({"image": out_name, "src": fname, "msg": secret.tolist()[0], "psnr": round(psnr, 2), "ssim": round(ssim_val, 4)})
        results.append({"image": out_name, "bit_accuracy": acc, "psnr": psnr, "ssim": ssim_val})

        # JPEG 鲁棒
        for q in [int(v) for v in args.jpeg.split(",")]:
            buf = io.BytesIO()
            wm_pil.save(buf, format="JPEG", quality=q)
            buf.seek(0)
            jpg = Image.open(buf).convert("RGB")
            xj = to_tensor(jpg).to(device)
            with torch.no_grad():
                decj = model._decode(xj)
            decj_bits = (decj[0].cpu() > 0.5).float()
            accj = float((decj_bits == secret_t[0].cpu()).float().mean().item())
            results[-1][f"acc_jpeg{q}"] = accj

        if (i + 1) % 20 == 0:
            print(f"[invismark] {i+1}/{len(imgs)}")

    mean_acc = np.mean([r["bit_accuracy"] for r in results])
    out = {"method": "InvisMark", "nbits": NBITS, "n": len(results), "mean_bit_acc": mean_acc,
           "tpr_ber025_clean": float(np.mean([(r["bit_accuracy"] >= 0.75) for r in results]))}
    for q in [int(v) for v in args.jpeg.split(",")]:
        out[f"mean_acc_jpeg{q}"] = float(np.mean([r[f"acc_jpeg{q}"] for r in results]))
        out[f"tpr_ber025_jpeg{q}"] = float(np.mean([(r[f"acc_jpeg{q}"] >= 0.75) for r in results]))
    out["mean_psnr"] = float(np.mean([r["psnr"] for r in results]))
    out["mean_ssim"] = float(np.mean([r["ssim"] for r in results]))
    out["results"] = results
    with open(os.path.join(args.out_dir, "summary.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"[invismark] n={len(results)} clean_acc={mean_acc*100:.2f}% TPR(BER<=0.25)={out['tpr_ber025_clean']*100:.1f}% PSNR={out['mean_psnr']:.1f} SSIM={out['mean_ssim']:.3f} -> {args.out_dir}")
    for q in [int(v) for v in args.jpeg.split(",")]:
        print(f"[invismark] JPEG{q}: acc={out[f'mean_acc_jpeg{q}']*100:.2f}%  TPR(BER<=0.25)={out[f'tpr_ber025_jpeg{q}']*100:.1f}%")

    # manifest 供 PSR 复用（与 eval_extractor2 的 _cloaked_wm.jpg 命名一致 -> 这里用 _invismark.png）
    with open(os.path.join(args.out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)


if __name__ == "__main__":
    main()
