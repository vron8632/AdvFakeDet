"""
E 组实验：联合优化（watermark-aware joint optimization）vs 顺序嵌入（回应 EIAW Table 9 / ARFP）。

科学问题：EIAW/ARFP 声称联合优化优于顺序拼接。
- 顺序嵌入（我们 C 组）: cloak → 独立水印嵌入
- 联合优化（E 组）: 从遮蔽图出发，同时优化 保持遮蔽 + 水印可解码

E 组实现（全 torch）:
  目标 = α·FR 相似度损失（保持遮蔽） + λ·WAM 解码损失（水印可读）
  δ 优化: B → B + δ，其中 WAM 检测器读出目标消息 msg。

对比指标：遮蔽保持（PSR/sim）+ 水印解码（BER）。
用法: python code/05_freq_constraint/e_group_joint.py --input_dir CLOAK --out_dir OUT --n 50
"""
import argparse
import json
import os
import sys

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms as T

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WAM_PROJECT = os.path.join(PROJECT_ROOT, "baselines", "wam")
sys.path.insert(0, WAM_PROJECT)

from notebooks.inference_utils import load_model_from_checkpoint  # noqa
import sys as _s; _s.path.insert(0, os.path.join(PROJECT_ROOT, 'code', '06_eval')); from eval_wam_decode import load_wam, img_transform  # noqa

MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]

# FR 代理：facenet
from facenet_pytorch import MTCNN, InceptionResnetV1  # noqa


def load_fr_proxy(device):
    mtcnn = MTCNN(keep_all=False, device=device)
    model = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    return mtcnn, model


def fr_embed(mtcnn, model, img_pil, device):
    face = mtcnn(img_pil)
    if face is None:
        img = img_pil.resize((160, 160))
        face = torch.tensor(np.array(img)).permute(2, 0, 1).float() / 255.0
    with torch.no_grad():
        return model(face.unsqueeze(0).to(device))[0]


def fr_embed_tensor(mtcnn, model, img_t, device):
    """可微 FR 嵌入：img_t 为 1,3,H,W 归一化 tensor → 直接 resize 到 160 喂 facenet（近似 MTCNN 对齐）"""
    x = F.interpolate(img_t, size=(160, 160), mode='bilinear', align_corners=False)
    return model(x)[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input_dir', required=True, help='遮蔽图目录')
    ap.add_argument('--orig_dir', required=True, help='原图目录')
    ap.add_argument('--out_dir', required=True)
    ap.add_argument('--n', type=int, default=50)
    ap.add_argument('--alpha', type=float, default=0.5, help='FR 相似度损失权重')
    ap.add_argument('--lam', type=float, default=10.0, help='WAM 解码损失权重')
    ap.add_argument('--steps', type=int, default=100)
    ap.add_argument('--lr', type=float, default=0.01)
    ap.add_argument('--seed', type=int, default=42)
    args = ap.parse_args()

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    wam = load_wam(os.path.join(WAM_PROJECT, 'checkpoints', 'params.json'),
                   os.path.join(WAM_PROJECT, 'checkpoints', 'checkpoint.pth'), device)
    mtcnn, fr = load_fr_proxy(device)
    rng = np.random.RandomState(args.seed)

    os.makedirs(args.out_dir, exist_ok=True)
    imgs = sorted(f for f in os.listdir(args.input_dir) if 'cloaked' in f and f.endswith('.jpeg'))[:args.n]

    manifest = []
    for i, fname in enumerate(imgs):
        stem = fname.rsplit('.', 1)[0]
        orig_name = stem.replace('_cloaked', '.jpg')
        orig_path = os.path.join(args.orig_dir, orig_name)
        if not os.path.exists(orig_path):
            continue
        B_pil = Image.open(os.path.join(args.input_dir, fname)).convert('RGB')
        orig_pil = Image.open(orig_path).convert('RGB')
        w, h = B_pil.size

        msg = rng.randint(0, 2, 32).astype(np.int64)
        msg_t = torch.from_numpy(msg).unsqueeze(0).to(device)

        # 参考 embedding（原图）
        e_ref = fr_embed(mtcnn, fr, orig_pil, device)

        # 遮蔽态 embedding（B 本身，不可微基准）
        with torch.no_grad():
            e_B = fr_embed(mtcnn, fr, B_pil, device)

        # 优化 δ（B_t 可微，256 空间）
        B_t = img_transform(B_pil).unsqueeze(0).to(device).clone().requires_grad_(True)
        opt = torch.optim.Adam([B_t], lr=args.lr)
        wam_loss_fn = torch.nn.BCEWithLogitsLoss()
        for step in range(args.steps):
            # FR 损失（可微）：B+δ 的 embedding 保持远离原图 e_ref（遮蔽保持）
            e_cur = fr_embed_tensor(mtcnn, fr, B_t, device)
            sim_ref = F.cosine_similarity(e_cur.unsqueeze(0), e_ref.unsqueeze(0))
            # 保持遮蔽：sim(B+δ, 原图) 不高于 sim(B, 原图) 太多 → 最小化 max(0, sim_ref - sim_B_ref + margin)
            with torch.no_grad():
                e_B_ref = F.cosine_similarity(e_B.unsqueeze(0), e_ref.unsqueeze(0))
            loss_fr = F.relu(sim_ref - e_B_ref + 0.05)
            # WAM 解码损失（可微）
            preds = wam.detect(B_t)['preds']
            logits = preds[:, 1:]
            msg_exp = msg_t.unsqueeze(-1).unsqueeze(-1).expand_as(logits).float()
            loss_wm = wam_loss_fn(logits, msg_exp)
            loss = args.alpha * loss_fr + args.lam * loss_wm
            opt.zero_grad()
            loss.backward()
            opt.step()

        # 输出
        with torch.no_grad():
            B_denorm = B_t.clone()
            for c in range(3):
                B_denorm[:, c] = B_denorm[:, c] * STD[c] + MEAN[c]
            B_denorm = B_denorm.clamp(0, 1)
        out_pil = T.ToPILImage()(B_denorm[0].cpu()).resize((w, h), Image.BILINEAR)
        out_name = orig_name.replace('.jpg', '_joint.jpg')
        out_pil.save(os.path.join(args.out_dir, out_name), quality=95)

        # 解码检查
        dec = (wam.detect(B_t)['preds'][0, 1:].mean(dim=(1, 2)) > 0).long().cpu().numpy()
        ber = float((dec != msg).mean())
        manifest.append({'image': out_name, 'src': fname, 'msg': msg.tolist(), 'ber': ber})
        if (i + 1) % 10 == 0:
            print(f'[E-group] {i+1}/{len(imgs)} mean_BER_so_far={np.mean([m["ber"] for m in manifest]):.4f}')

    mean_ber = np.mean([m['ber'] for m in manifest])
    print(f'[E-group] n={len(manifest)} mean_BER={mean_ber:.4f} BER<=0.25 TPR={np.mean([m["ber"] <= 0.25 for m in manifest]) * 100:.1f}%')
    json.dump(manifest, open(os.path.join(args.out_dir, 'manifest.json'), 'w'), indent=2)
    print(f'[E-group] saved -> {args.out_dir}')


if __name__ == '__main__':
    main()
