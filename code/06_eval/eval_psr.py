"""
PSR 评估（Protection Success Rate = 100% - FR识别准确率）。
画廊-查询最近邻识别协议（Fawkes/ARFP 标准）。
- 画廊: 每身份 1 张原图
- 查询: 遮蔽图/水印图
- FR识别正确 = 查询最近邻身份 == 真实身份 → PSR = 100% - 正确率
模型: extractor_2（Fawkes 训练空间）/ facenet（未知标准模型）
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image


def load_extractor2():
    sys.path.insert(0, os.path.join('baselines', 'fawkes'))
    from fawkes.utils import load_extractor, resize  # noqa
    from fawkes.align_face import align, aligner  # noqa
    ex = load_extractor('extractor_2')
    al = aligner()
    def emb(path):
        img = np.array(Image.open(path).convert('RGB'))
        cropped, _ = align(img, al)
        if not cropped:
            return None
        face = cropped[0]
        ls = max(face.shape[0], face.shape[1]) + 30
        base = np.ones((ls, ls, 3)) * np.mean(face, axis=(0, 1))
        s1 = (ls - face.shape[0]) // 2; s2 = (ls - face.shape[1]) // 2
        base[s1:s1 + face.shape[0], s2:s2 + face.shape[1], :] = face
        base = resize(base, (112, 112))
        return ex.predict(base[None].astype('float32'))[0]
    return emb


def load_facenet():
    import torch
    from facenet_pytorch import MTCNN, InceptionResnetV1
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    mtcnn = MTCNN(keep_all=False, device=device)
    model = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    def emb(path):
        img = Image.open(path).convert('RGB')
        face = mtcnn(img)
        if face is None:
            img = img.resize((160, 160))
            face = torch.tensor(np.array(img)).permute(2, 0, 1).float() / 255.0
        with torch.no_grad():
            return model(face.unsqueeze(0).to(device))[0].cpu().numpy()
    return emb


def cos(a, b):
    return float(np.dot(a / np.linalg.norm(a), b / np.linalg.norm(b)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--orig_dir', required=True)
    ap.add_argument('--adv_dir', required=True)
    ap.add_argument('--ids', required=True)
    ap.add_argument('--adv_suffix', default='_cloaked.jpeg')
    ap.add_argument('--model', default='extractor2', choices=['extractor2', 'facenet'])
    ap.add_argument('--n', type=int, default=200)
    ap.add_argument('--out', default='psr_eval.json')
    args = ap.parse_args()

    emb = load_extractor2() if args.model == 'extractor2' else load_facenet()
    ids = json.load(open(args.ids))
    names = sorted(ids.keys())[:args.n]

    # 画廊
    gallery = {}
    for name in names:
        e = emb(os.path.join(args.orig_dir, name))
        if e is not None:
            gallery[name] = e
    print(f'gallery size: {len(gallery)}')

    # 干净基线（原图查询）
    correct_clean = 0
    for name in names:
        if name not in gallery: continue
        q = emb(os.path.join(args.orig_dir, name))
        if q is None: continue
        best = max(gallery, key=lambda g: cos(q, gallery[g]))
        if best == name: correct_clean += 1
    n_clean = len([n for n in names if n in gallery])
    print(f'clean 基线: FR识别={correct_clean}/{n_clean} ({correct_clean/max(n_clean,1)*100:.1f}%) PSR={100-correct_clean/max(n_clean,1)*100:.1f}%')

    # 查询组
    correct = 0
    sims = []
    for name in names:
        if name not in gallery: continue
        stem = name.rsplit('.', 1)[0]
        ap = os.path.join(args.adv_dir, stem + args.adv_suffix)
        if not os.path.exists(ap): continue
        q = emb(ap)
        if q is None: continue
        sims.append(cos(q, gallery[name]))
        best = max(gallery, key=lambda g: cos(q, gallery[g]))
        if best == name: correct += 1
    n = len(sims)
    print(f'[{args.model}] {args.adv_suffix}: FR识别={correct}/{n} ({correct/max(n,1)*100:.1f}%) **PSR={100-correct/max(n,1)*100:.1f}%** sim_orig mean={np.mean(sims):.4f}')
    json.dump({'model': args.model, 'clean_correct': correct_clean, 'clean_n': n_clean,
               'adv_correct': correct, 'adv_n': n, 'psr': 100 - correct / max(n, 1) * 100,
               'mean_sim': float(np.mean(sims))}, open(args.out, 'w'), indent=2)
    print(f'saved -> {args.out}')


if __name__ == '__main__':
    main()
