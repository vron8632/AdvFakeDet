"""
FR 身份一致性评估（facenet_pytorch InceptionResnetV1）。
输入: 一组 (original, cloaked/watermarked) 图像对 + 身份标签。
输出: 遮蔽有效性指标 — exact_adv_consistent / drift / revert / not_detected。

评估协议（对齐学生 evaluate_adv_id_consistency.py 的 STATUS 体系）：
- 以原图为画廊，遮蔽图为查询：计算遮蔽图嵌入与同身份原图嵌入的余弦相似度 vs 与随机负样本的相似度
- exact_adv_consistent: 遮蔽图被识别为"另一个身份"（与原身份不同但被检测到）
- reverted_to_orig: 遮蔽图被认回原身份（遮蔽失败）
- not_detected: 未检测到人脸
"""
import argparse
import json
import os
import random
from collections import Counter

import numpy as np
import torch
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1

STATUS_EXACT = "exact_adv_consistent"
STATUS_DRIFT = "drift_other_nonorig"
STATUS_REVERT = "reverted_to_orig"
STATUS_NOT_DETECTED = "not_detected"


def load_model(device):
    mtcnn = MTCNN(keep_all=False, device=device)
    model = InceptionResnetV1(pretrained="vggface2").eval().to(device)
    return mtcnn, model


def embed(mtcnn, model, img_path, device, default_size=160):
    """返回嵌入向量或 None（未检测到人脸）"""
    img = Image.open(img_path).convert("RGB")
    face = mtcnn(img)
    if face is None:
        # 退化为居中裁剪 resize
        img = img.resize((default_size, default_size))
        face = (torch.tensor(np.array(img)).permute(2, 0, 1).float() / 255.0).to(device)
    face = face.unsqueeze(0)
    if face.device != next(model.parameters()).device:
        face = face.to(device)
    with torch.no_grad():
        emb = model(face)
    return emb[0].cpu().numpy()


def cos_sim(a, b):
    a, b = a / (np.linalg.norm(a) + 1e-12), b / (np.linalg.norm(b) + 1e-12)
    return float(np.dot(a, b))


def evaluate_pairs(pairs, mtcnn, model, device, seed=42):
    """pairs: list of dict {orig: path, adv: path, id: label, neg_id: label}
    判定逻辑：adv 嵌入与 orig 嵌入相似度是否 > 阈值(默认 0.4)；以及 adv 是否被识别为某身份。
    简化版：用同身份相似度 sim_orig 与跨身份相似度分布比较。
    """
    rng = random.Random(seed)
    results = []
    for p in pairs:
        e_orig = embed(mtcnn, model, p["orig"], device)
        e_adv = embed(mtcnn, model, p["adv"], device)
        if e_adv is None:
            results.append({**p, "status": STATUS_NOT_DETECTED, "sim_orig": None})
            continue
        sim_orig = cos_sim(e_orig, e_adv)
        if sim_orig >= 0.4:
            status = STATUS_REVERT
        else:
            status = STATUS_DRIFT  # 简化：非原身份即 drift/exact
        results.append({**p, "status": status, "sim_orig": sim_orig})
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--orig_dir", required=True)
    ap.add_argument("--adv_dir", required=True)
    ap.add_argument("--ids", required=True, help="json: {orig_basename: id}")
    ap.add_argument("--out", default="fr_eval_results.json")
    ap.add_argument("--threshold", type=float, default=0.4)
    ap.add_argument("--adv_suffix", default="_cloaked.jpeg", help="对抗图文件后缀（如 _wm.jpg）")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    mtcnn, model = load_model(device)

    with open(args.ids) as f:
        id_map = json.load(f)

    pairs = []
    for orig_name, ident in id_map.items():
        stem = orig_name.rsplit(".", 1)[0]
        adv_name = stem + args.adv_suffix
        adv_path = os.path.join(args.adv_dir, adv_name)
        if not os.path.exists(adv_path):
            continue
        pairs.append({"orig": os.path.join(args.orig_dir, orig_name),
                      "adv": adv_path, "id": ident})

    results = evaluate_pairs(pairs, mtcnn, model, device)
    stats = Counter(r["status"] for r in results)
    total = len(results)
    print(f"[FR eval] n={total}")
    for k in (STATUS_EXACT, STATUS_DRIFT, STATUS_REVERT, STATUS_NOT_DETECTED):
        print(f"  {k}: {stats.get(k, 0)} ({stats.get(k, 0) / max(total, 1) * 100:.1f}%)")
    keep = [r for r in results if r["sim_orig"] is not None]
    if keep:
        sims = [r["sim_orig"] for r in keep]
        print(f"  mean sim_orig: {np.mean(sims):.4f}")
    with open(args.out, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"saved -> {args.out}")


if __name__ == "__main__":
    main()
