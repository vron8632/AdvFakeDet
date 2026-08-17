"""
构建 1000 张"干净可识别"LFW 子集（随机公平抽样，避开学生用过的 top2-easy 子集）。
- 输入: newpatch/lfw/（5749 身份, 13233 张）
- 输出: assets/dataset/lfw1000/ 下的 original/ (jpg) + ids.json {basename: identity}
- 每个身份最多取 2 张（保证身份多样性），筛选：无损坏图片
用法: conda run -n newpatch python code/01_data_prep/build_lfw1000.py --n 1000 --seed 42
"""
import argparse
import json
import os
import random
import shutil

from PIL import Image

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LFW_DIR = os.path.join(PROJECT_ROOT, "newpatch", "lfw")


def collect_identities():
    """返回 {identity: [image_path, ...]}"""
    id_map = {}
    for ident in sorted(os.listdir(LFW_DIR)):
        d = os.path.join(LFW_DIR, ident)
        if not os.path.isdir(d):
            continue
        imgs = [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        if imgs:
            id_map[ident] = imgs
    return id_map


def check_valid(path):
    try:
        with Image.open(path) as im:
            im.load()
        return True
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--max_per_id", type=int, default=2)
    ap.add_argument("--out", default=os.path.join(PROJECT_ROOT, "assets", "dataset", "lfw1000"))
    args = ap.parse_args()

    rng = random.Random(args.seed)
    id_map = collect_identities()
    print(f"[data] LFW identities: {len(id_map)}, total images: {sum(len(v) for v in id_map.values())}")

    # 打乱身份顺序，逐个身份抽样直到凑满 n
    selected = []  # (identity, path)
    id_order = list(id_map.keys())
    rng.shuffle(id_order)
    for ident in id_order:
        if len(selected) >= args.n:
            break
        imgs = id_map[ident]
        rng.shuffle(imgs)
        cnt = 0
        for p in imgs:
            if len(selected) >= args.n:
                break
            if cnt >= args.max_per_id:
                break
            if check_valid(p):
                selected.append((ident, p))
                cnt += 1

    print(f"[data] selected: {len(selected)} images from {len(set(i for i, _ in selected))} identities")

    orig_dir = os.path.join(args.out, "original")
    os.makedirs(orig_dir, exist_ok=True)
    ids = {}
    for idx, (ident, p) in enumerate(selected):
        base = os.path.basename(p)
        stem = base.rsplit(".", 1)[0]
        new_name = f"{idx:05d}_{stem}.jpg"
        shutil.copy(p, os.path.join(orig_dir, new_name))
        ids[new_name] = ident

    with open(os.path.join(args.out, "ids.json"), "w") as f:
        json.dump(ids, f, indent=2, ensure_ascii=False)
    print(f"[data] saved to {args.out} ({len(ids)} images, ids.json)")


if __name__ == "__main__":
    main()
