"""
Fawkes extractor_2 遮蔽有效性评估（Fawkes 训练提取器空间）。
用途: 在遮蔽有效的模型上比较 A（cloak）vs B（cloak+wm）的遮蔽保持率。
用法: conda run -n fawkes python code/06_eval/eval_extractor2.py --orig_dir X --adv_dir Y --ids json --adv_suffix _cloaked.jpeg
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "baselines", "fawkes"))
from fawkes.utils import load_extractor, resize  # noqa
from fawkes.align_face import align, aligner  # noqa

STATUS_REVERT = "reverted_to_orig"
STATUS_DRIFT = "drift_other_nonorig"


def get_face_emb(img, ex, al):
    cropped_arr, _ = align(img, al)
    if not cropped_arr:
        return None
    face = cropped_arr[0]
    long_size = max(face.shape[0], face.shape[1]) + 30
    base = np.ones((long_size, long_size, 3)) * np.mean(face, axis=(0, 1))
    s1 = (long_size - face.shape[0]) // 2
    s2 = (long_size - face.shape[1]) // 2
    base[s1:s1 + face.shape[0], s2:s2 + face.shape[1], :] = face
    base = resize(base, (112, 112))
    return ex.predict(base[None].astype("float32"))[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--orig_dir", required=True)
    ap.add_argument("--adv_dir", required=True)
    ap.add_argument("--ids", required=True)
    ap.add_argument("--adv_suffix", default="_cloaked.jpeg")
    ap.add_argument("--threshold", type=float, default=0.4)
    ap.add_argument("--out", default="extractor2_eval.json")
    args = ap.parse_args()

    ex = load_extractor("extractor_2")
    al = aligner()
    with open(args.ids) as f:
        id_map = json.load(f)

    results = []
    for orig_name, ident in id_map.items():
        stem = orig_name.rsplit(".", 1)[0]
        adv_path = os.path.join(args.adv_dir, stem + args.adv_suffix)
        if not os.path.exists(adv_path):
            continue
        orig = np.array(Image.open(os.path.join(args.orig_dir, orig_name)).convert("RGB"))
        adv = np.array(Image.open(adv_path).convert("RGB"))
        if orig.shape != adv.shape:
            adv = np.array(Image.open(adv_path).convert("RGB").resize((orig.shape[1], orig.shape[0])))
        e1 = get_face_emb(orig, ex, al)
        e2 = get_face_emb(adv, ex, al)
        if e1 is None or e2 is None:
            continue
        sim = float(np.dot(e1 / np.linalg.norm(e1), e2 / np.linalg.norm(e2)))
        status = STATUS_REVERT if sim >= args.threshold else STATUS_DRIFT
        results.append({"orig": orig_name, "adv": stem + args.adv_suffix, "id": ident, "status": status, "sim": sim})

    from collections import Counter
    stats = Counter(r["status"] for r in results)
    n = len(results)
    keep_rate = stats.get(STATUS_DRIFT, 0) / max(n, 1)
    print(f"[extractor2] n={n} keep_rate(遮蔽保持)={keep_rate * 100:.1f}% revert={stats.get(STATUS_REVERT, 0)} ({stats.get(STATUS_REVERT, 0) / max(n, 1) * 100:.1f}%)")
    print(f"[extractor2] mean sim={np.mean([r['sim'] for r in results]):.4f}")
    with open(args.out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"saved -> {args.out}")


if __name__ == "__main__":
    main()
