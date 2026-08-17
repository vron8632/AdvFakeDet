"""
WAM 水印解码评估：输入 水印图目录 + manifest（消息真值），输出位精度/TPR。
也支持鲁棒性变体（JPEG/裁剪/缩放等）。
用法:
  python code/06_eval/eval_wam_decode.py --wm_dir /tmp/b_test_out2 --manifest /tmp/b_test_out2/manifest.json
"""
import argparse
import io
import json
import os
import sys

import numpy as np
import torch
from PIL import Image
from torchvision import transforms as T

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WAM_PROJECT = os.path.join(PROJECT_ROOT, "baselines", "wam")
sys.path.insert(0, WAM_PROJECT)

from notebooks.inference_utils import load_model_from_checkpoint  # noqa

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
        for cand in (os.path.join(WAM_PROJECT, val), os.path.join(base_dir, val)):
            if os.path.exists(cand):
                params[key] = cand
                break
    tmp_path = os.path.join(base_dir, "_params_tmp.json")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(params, f)
    wam = load_model_from_checkpoint(tmp_path, checkpoint)
    os.remove(tmp_path)
    return wam.to(device).eval()


def decode_bits(wam, img_path, device, jpeg_quality=None, mask_aware=True):
    img = Image.open(img_path).convert("RGB")
    if jpeg_quality is not None:
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=jpeg_quality)
        buf.seek(0)
        img = Image.open(buf).convert("RGB")
    img_t = img_transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        preds = wam.detect(img_t)["preds"]  # 1, (1+nbits), 256, 256
    if mask_aware:
        # 用预测 mask 通道（ch0 > 0）定位水印区域，只在区域内多数投票
        mask = (preds[0, 0] > 0)
        if mask.sum() < 100:  # 无检测到区域则退化为全图
            logits = preds[0, 1:]
            decoded = (logits.mean(dim=(1, 2)) > 0).long()
        else:
            logits = preds[0, 1:]
            decoded = (logits[:, mask].mean(dim=1) > 0).long()
    else:
        logits = preds[0, 1:]
        decoded = (logits.mean(dim=(1, 2)) > 0).long()
    return decoded.cpu().numpy()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wm_dir", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--params_json", default=os.path.join(WAM_PROJECT, "checkpoints", "params.json"))
    ap.add_argument("--checkpoint", default=os.path.join(WAM_PROJECT, "checkpoints", "checkpoint.pth"))
    ap.add_argument("--jpeg_quality", type=int, default=None, help="若设置，先做 JPEG 压缩再解码")
    ap.add_argument("--out", default="wam_decode_results.json")
    ap.add_argument("--ber_threshold", type=float, default=None, help="BER 阈值（如 0.2 = 位精度>=80% 视为存在水印）")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    wam = load_wam(args.params_json, args.checkpoint, device)

    with open(args.manifest) as f:
        manifest = json.load(f)

    results = []
    accs = []
    for item in manifest:
        fname = item["image"]
        path = os.path.join(args.wm_dir, fname)
        if not os.path.exists(path):
            continue
        gt = np.array(item["msg"], dtype=np.int64)
        dec = decode_bits(wam, path, device, jpeg_quality=args.jpeg_quality)
        acc = float((dec == gt).mean())
        accs.append(acc)
        results.append({"image": fname, "bit_accuracy": acc, "decoded": dec.tolist()})

    mean_acc = np.mean(accs) if accs else 0.0
    tpr_99 = float(np.mean([a >= 0.99 for a in accs]))  # 位精度≥99% 视为成功
    tpr_95 = float(np.mean([a >= 0.95 for a in accs]))
    extra = ""
    if args.ber_threshold is not None:
        tpr_ber = float(np.mean([a >= (1 - args.ber_threshold) for a in accs]))
        extra = f" TPR@BER{args.ber_threshold}={tpr_ber * 100:.1f}%"
        with open(args.out, "w") as f:
            json.dump({"jpeg_quality": args.jpeg_quality, "mean_bit_acc": mean_acc, "tpr99": tpr_99, "tpr95": tpr_95, "tpr_ber": tpr_ber, "ber_threshold": args.ber_threshold, "results": results}, f, indent=2)
        print(f"[wam decode] n={len(results)} mean_bit_acc={mean_acc * 100:.2f}%{extra}")
        return
    print(f"[wam decode] n={len(results)} mean_bit_acc={mean_acc * 100:.2f}% TPR@99%={tpr_99 * 100:.1f}% TPR@95%={tpr_95 * 100:.1f}%")
    with open(args.out, "w") as f:
        json.dump({"jpeg_quality": args.jpeg_quality, "mean_bit_acc": mean_acc, "tpr99": tpr_99, "tpr95": tpr_95, "results": results}, f, indent=2)
    print(f"saved -> {args.out}")


if __name__ == "__main__":
    main()
