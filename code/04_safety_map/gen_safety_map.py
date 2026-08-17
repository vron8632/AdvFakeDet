"""
C 组：FR 敏感度安全区域图生成（基于 arcface34 梯度/相似度敏感性）。
定义：对遮蔽图 B 的每个空间位置，评估该位置扰动对 FR 身份识别的影响。
方法（白盒代理）：
  1. 用 arcface34 作为 FR 代理，输入对齐人脸
  2. 对输入加局部高斯扰动（逐位置探测）或直接取梯度幅度（|dL/dx|）
  3. R(x,y) = 归一化的 FR 敏感度；安全区域 S = 1 - R（低敏感区允许嵌水印）
输出: {basename}_map.npy (H,W) 与可视化 png

用法: python code/04_safety_map/gen_safety_map.py --img_dir X --out_dir Y --model arcface34
"""
import argparse
import os
import sys

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "newpatch", "rlpatch"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "newpatch", "rlpatch", "models"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "newpatch", "rlpatch", "mtcnn_pytorch_master"))

from models.iresnet import iresnet34  # noqa

STMODELS = os.path.join(PROJECT_ROOT, "newpatch", "rlpatch", "stmodels_lfw")


def build_arcface34(device):
    model = iresnet34(False, dropout=0, fp16=True)
    ckpt = torch.load(os.path.join(STMODELS, "arcface34", "arcface_34.pth"), map_location=device)
    model.load_state_dict(ckpt)
    model.eval().to(device)
    return model


def gradient_saliency(model, x, device):
    """对输入求 FR 特征梯度的空间幅度（敏感度 R）。x: 1,3,112,112 归一化 tensor"""
    x = x.clone().detach().requires_grad_(True)
    emb = model(x)
    # 用 embedding 的 L2 范数对输入的梯度（特征敏感度）
    loss = emb.norm()
    model.zero_grad()
    loss.backward()
    grad = x.grad.abs().mean(dim=1, keepdim=True)  # 1,1,112,112
    return grad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--img_dir", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--suffix", default=".jpg", help="输入文件后缀过滤")
    ap.add_argument("--blur", type=int, default=3, help="敏感图高斯平滑核")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = build_arcface34(device)
    os.makedirs(args.out_dir, exist_ok=True)

    imgs = sorted(f for f in os.listdir(args.img_dir) if f.endswith(args.suffix))
    print(f"[safety_map] images: {len(imgs)}")
    for i, fname in enumerate(imgs):
        path = os.path.join(args.img_dir, fname)
        img = Image.open(path).convert("RGB").resize((112, 112))
        x = torch.tensor(np.array(img)).permute(2, 0, 1).float().unsqueeze(0).to(device) / 255.0
        x = (x - 0.5) / 0.5
        sal = gradient_saliency(model, x, device)  # 1,1,112,112
        sal = F.avg_pool2d(sal, 4).repeat_interleave(4, dim=2).repeat_interleave(4, dim=1)  # 平滑到 28x28 再放大
        sal = sal[0, 0].cpu().numpy()
        sal = (sal - sal.min()) / (sal.max() - sal.min() + 1e-12)
        stem = fname.rsplit(".", 1)[0]
        np.save(os.path.join(args.out_dir, f"{stem}_map.npy"), sal)
        if (i + 1) % 50 == 0:
            print(f"[safety_map] {i + 1}/{len(imgs)}")
    print(f"[safety_map] done -> {args.out_dir}")


if __name__ == "__main__":
    main()
