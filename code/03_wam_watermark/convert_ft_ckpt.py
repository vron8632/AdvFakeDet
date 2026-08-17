"""
将 WAM 训练 checkpoint（含 model/optimizer/scheduler）转为纯 state_dict 推理格式。
用法: python code/03_wam_watermark/convert_ft_ckpt.py --in assets/experiments/wam_jpeg_ft/checkpoint.pth
"""
import argparse
import os

import torch


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    ckpt = torch.load(args.inp, map_location="cpu")
    if isinstance(ckpt, dict) and "model" in ckpt:
        sd = ckpt["model"]
    else:
        sd = ckpt
    # 去掉 DDP module. 前缀
    sd = {k.replace("module.", ""): v for k, v in sd.items()}
    out = args.out or os.path.splitext(args.inp)[0] + "_infer.pth"
    torch.save(sd, out)
    print(f"saved inference state_dict -> {out} ({len(sd)} keys)")


if __name__ == "__main__":
    main()
