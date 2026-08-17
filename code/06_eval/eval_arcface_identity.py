"""
身份识别评估 v2（学生流程：landmark 仿射对齐 + 无归一化）。
- 画廊: 每身份 1 张原图
- 查询: 遮蔽图/水印图
- 指标: revert(被认回原身份) / drift(其他) / 画廊识别正确率；同/异类 sim 分布
"""
import argparse
import json
import os
import sys
from collections import Counter

import numpy as np
import torch
from PIL import Image
from torchvision import transforms

sys.path.insert(0, 'newpatch/rlpatch')
sys.path.insert(0, 'newpatch/rlpatch/models')
sys.path.insert(0, 'newpatch/rlpatch/mtcnn_pytorch_master')
from models.iresnet import iresnet34, iresnet50  # noqa
from mtcnn_pytorch_master.test import crop_face  # noqa

STMODELS = 'newpatch/rlpatch/stmodels_lfw'
MODELS = {'arcface34': ('arcface34', 'arcface_34.pth', iresnet34), 'arcface50': ('arcface50', 'ms1mv3_arcface_r50_fp16.pth', iresnet50)}
trans = transforms.Compose([transforms.ToTensor()])


def build_model(name, device):
    sub, fn, builder = MODELS[name]
    model = builder(False, dropout=0, fp16=True)
    ckpt = torch.load(os.path.join(STMODELS, sub, fn), map_location=device)
    model.load_state_dict(ckpt)
    model.eval().to(device)
    return model


def embed(model, img_path, device):
    img = Image.open(img_path).convert('RGB')
    try:
        crop = crop_face(img, 112, 112)
    except Exception:
        crop = img.resize((112, 112))
    x = trans(crop).unsqueeze(0).to(device)
    with torch.no_grad():
        return model(x)[0].cpu().numpy()


def cos(a, b):
    return float(np.dot(a / np.linalg.norm(a), b / np.linalg.norm(b)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--orig_dir', required=True)
    ap.add_argument('--adv_dir', required=True)
    ap.add_argument('--ids', required=True)
    ap.add_argument('--adv_suffix', default='_cloaked.jpeg')
    ap.add_argument('--model', default='arcface34')
    ap.add_argument('--n', type=int, default=200)
    ap.add_argument('--out', default='arcface_ident_eval.json')
    args = ap.parse_args()

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = build_model(args.model, device)
    ids = json.load(open(args.ids))
    names = sorted(ids.keys())[:args.n]

    # 画廊（每身份一张）+ 同类/异类分布
    gallery = {name: (embed(model, os.path.join(args.orig_dir, name), device), ids[name]) for name in names}
    gl = list(gallery.items())
    same, cross = [], []
    for i in range(min(20, len(gl))):
        for j in range(i + 1, min(20, len(gl))):
            s = cos(gl[i][1][0], gl[j][1][0])
            (same if gl[i][1][1] == gl[j][1][1] else cross).append(s)
    if same:
        print(f'{args.model} 同身份 sim: mean={np.mean(same):.3f} n={len(same)}')
    if cross:
        print(f'{args.model} 跨身份 sim: mean={np.mean(cross):.3f} n={len(cross)}')

    results = []
    for name in names:
        stem = name.rsplit('.', 1)[0]
        adv_path = os.path.join(args.adv_dir, stem + args.adv_suffix)
        if not os.path.exists(adv_path):
            continue
        eq = embed(model, adv_path, device)
        sims = {g: cos(eq, ge) for g, (ge, _) in gallery.items()}
        best = max(sims, key=sims.get)
        best_ident = gallery[best][1]
        true_ident = ids[name]
        sim_orig = sims[name]
        status = 'revert' if sim_orig >= 0.45 else 'drift'
        results.append({'orig': name, 'adv': stem + args.adv_suffix, 'true_ident': true_ident,
                        'recognized_ident': best_ident, 'sim_orig': sim_orig, 'status': status})

    stats = Counter(r['status'] for r in results)
    n = len(results)
    # 画廊识别（真实查询被正确识别为原身份的比例，验证评估有效性）
    gal_ok = sum(1 for r in results if r['recognized_ident'] == r['true_ident'])
    print(f'[识别] n={n} 画廊识别正确={gal_ok} ({gal_ok / max(n, 1) * 100:.1f}%)')
    print(f'[识别] revert(遮蔽失败)={stats.get("revert", 0)} ({stats.get("revert", 0) / max(n, 1) * 100:.1f}%) drift={stats.get("drift", 0)}')
    print(f'[识别] mean sim_orig={np.mean([r["sim_orig"] for r in results]):.4f}')
    json.dump(results, open(args.out, 'w'), indent=2)
    print(f'saved -> {args.out}')


if __name__ == '__main__':
    main()
