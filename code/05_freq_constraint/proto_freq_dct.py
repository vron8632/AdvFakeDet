"""
D 组原型：频域中低频约束实验。
思路：对 WAM 全局水印图做 DCT 域处理——保留中低频、抑制高频，
验证 JPEG 压缩下解码率是否改善（WAM 短板的频域应对）。

协议：
1. 对水印图 B_w 与原图 B 求残差 delta = B_w - B
2. 对 delta 做分块 DCT (8x8)，保留 |u|+|v| <= R 的中低频系数（其余置 0）
3. 重建 C = B + delta_filtered
4. 在 JPEG(q) 下解码，对比原始 B_w
"""
import argparse
import json
import os
import sys

import numpy as np
import torch
from PIL import Image
from scipy.fftpack import dct, idct

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WAM_PROJECT = os.path.join(PROJECT_ROOT, "baselines", "wam")
sys.path.insert(0, WAM_PROJECT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "code", "06_eval"))

from eval_wam_decode import load_wam, decode_bits  # noqa
from eval_wam_decode import img_transform  # noqa


def jpeg_quant_table(quality=80):
    """标准 JPEG 亮度量化表（libjpeg 默认），quality<50 时缩放"""
    base = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]], dtype=float)
    if quality < 50:
        scale = 5000.0 / quality
    else:
        scale = 200 - 2 * quality
    return np.clip(np.floor((base * scale + 50) / 100), 1, 255)


def jpeg_projection(delta, quality=80):
    """JPEG 量化投影：对残差做 8x8 DCT → 量化 → 反量化（JPEG 鲁棒残差）"""
    q = jpeg_quant_table(quality)
    h, w, c = delta.shape
    out = np.zeros_like(delta)
    for ch in range(c):
        d = delta[:, :, ch]
        dh, dw = h // 8 * 8, w // 8 * 8
        d = d[:dh, :dw]
        blocks = d.reshape(dh // 8, 8, dw // 8, 8).transpose(0, 2, 1, 3)
        coefs = dct(dct(blocks, axis=2, norm="ortho"), axis=3, norm="ortho")
        quantized = np.round(coefs / q) * q
        rec = idct(idct(quantized, axis=2, norm="ortho"), axis=3, norm="ortho")
        out[:dh, :dw, ch] = rec.transpose(0, 2, 1, 3).reshape(dh, dw)
    return out


def dct8x8_filter(delta, radius):
    """分块 8x8 DCT，保留 |u|+|v|<=radius 的系数。delta: HxWxC float in [-1,1]"""
    h, w, c = delta.shape
    out = np.zeros_like(delta)
    for ch in range(c):
        d = delta[:, :, ch]
        # 分块
        dh, dw = h // 8 * 8, w // 8 * 8
        d = d[:dh, :dw]
        blocks = d.reshape(dh // 8, 8, dw // 8, 8).transpose(0, 2, 1, 3)
        coefs = dct(dct(blocks, axis=2, norm="ortho"), axis=3, norm="ortho")
        # 掩码（8x8 广播到所有块）
        u = np.arange(8)[:, None]
        v = np.arange(8)[None, :]
        mask = (np.abs(u) + np.abs(v)) <= radius
        coefs *= mask.astype(float)
        rec = idct(idct(coefs, axis=2, norm="ortho"), axis=3, norm="ortho")
        out[:dh, :dw, ch] = rec.transpose(0, 2, 1, 3).reshape(dh, dw)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wm_dir", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--orig_dir", required=True, help="原始(遮蔽)图目录")
    ap.add_argument("--radius", type=int, default=4, help="DCT 保留半径")
    ap.add_argument("--method", default="lowpass", choices=["lowpass", "jpeg_proj"], help="频域方法")
    ap.add_argument("--alpha", type=float, default=1.0, help="滤波残差缩放")
    ap.add_argument("--jpeg_quality", type=int, default=80)
    ap.add_argument("--out_dir", default=None)
    args = ap.parse_args()

    # 延迟导入 WAM（放最后避免依赖循环）
    sys.path.insert(0, os.path.join(PROJECT_ROOT, "baselines", "wam"))
    sys.path.insert(0, PROJECT_ROOT)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    wam = load_wam(os.path.join(WAM_PROJECT, "checkpoints", "params.json"),
                   os.path.join(WAM_PROJECT, "checkpoints", "checkpoint.pth"), device)

    with open(args.manifest) as f:
        manifest = json.load(f)

    os.makedirs(args.out_dir, exist_ok=True) if args.out_dir else None
    accs_orig, accs_filt = [], []
    for item in manifest:
        fname = item["image"]
        src = item["src"]
        orig_path = os.path.join(args.orig_dir, src)  # 原遮蔽图
        wm_path = os.path.join(args.wm_dir, fname)
        if not os.path.exists(orig_path):
            continue
        B = np.array(Image.open(orig_path).convert("RGB")).astype(float) / 255.0
        Bw = np.array(Image.open(wm_path).convert("RGB")).astype(float) / 255.0
        delta = Bw - B
        if args.method == "lowpass":
            delta_f = dct8x8_filter(delta, args.radius) * args.alpha
        else:
            delta_f = jpeg_projection(delta, quality=args.jpeg_quality) * args.alpha
        C = np.clip(B + delta_f, 0, 1)
        out_path = os.path.join(args.out_dir, fname) if args.out_dir else "/tmp/freq_filt.jpg"
        Image.fromarray((C * 255).astype(np.uint8)).save(out_path, quality=95)

        gt = np.array(item["msg"], dtype=np.int64)
        a_orig = float((decode_bits(wam, wm_path, device, args.jpeg_quality) == gt).mean())
        a_filt = float((decode_bits(wam, out_path, device, args.jpeg_quality) == gt).mean())
        accs_orig.append(a_orig)
        accs_filt.append(a_filt)
        print(f"{fname}: orig_jpeg{args.jpeg_quality}={a_orig * 100:.1f}%  freq_filt_jpeg{args.jpeg_quality}={a_filt * 100:.1f}%")

    print(f"[D-prototype] radius={args.radius} mean orig={np.mean(accs_orig) * 100:.1f}% mean filt={np.mean(accs_filt) * 100:.1f}%")


if __name__ == "__main__":
    main()
