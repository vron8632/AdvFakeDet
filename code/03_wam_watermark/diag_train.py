"""诊断 WAM 训练 decode_loss 恒定的原因"""
import argparse
import json
import os
import sys

import numpy as np
import torch
from torchvision import transforms

sys.path.insert(0, 'baselines/wam')
from watermark_anything.models import Wam, build_embedder, build_extractor
from watermark_anything.augmentation.augmenter import Augmenter
from watermark_anything.data.transforms import get_transforms_segmentation
from watermark_anything.data.loader import get_dataloader
from watermark_anything.modules.jnd import JND
from watermark_anything.losses.detperceptual import LPIPSWithDiscriminator

sys.path.insert(0, 'baselines/wam/notebooks')
from inference_utils import load_model_from_checkpoint

import omegaconf


def main():
    device = 'cuda:0'
    params = json.load(open('baselines/wam/checkpoints/params.json'))
    base = os.path.dirname('baselines/wam/checkpoints/params.json')
    for k in ('embedder_config', 'augmentation_config', 'extractor_config', 'attenuation_config'):
        v = params.get(k)
        if v and not os.path.isabs(v):
            p1 = os.path.join('baselines/wam', v)
            p2 = os.path.join(base, v)
            params[k] = p1 if os.path.exists(p1) else p2
    json.dump(params, open('/tmp/_diag.json', 'w'))

    wam = load_model_from_checkpoint('/tmp/_diag.json', 'baselines/wam/checkpoints/checkpoint.pth').to(device).eval()
    wam.scaling_w = 2.0

    train_t, _, val_t, _ = get_transforms_segmentation(256)
    loader = get_dataloader('assets/wam_finetune/train', transform=train_t, batch_size=8, shuffle=False, num_workers=0)
    imgs, masks = next(iter(loader))
    imgs = imgs.to(device)
    print('imgs range:', imgs.min().item(), imgs.max().item(), imgs.shape)

    with torch.no_grad():
        out = wam(imgs, masks, no_overlap=False, params=omegaconf.OmegaConf.create({'img_size_extractor': 256}))
    preds = out['preds']
    print('preds shape:', preds.shape, 'mean:', preds.mean().item(), 'std:', preds.std().item())
    # 统计 logits 分布
    for idx in range(preds.shape[1]):
        print(f'channel {idx}: mean={preds[:, idx].mean().item():.3f} std={preds[:, idx].std().item():.3f}')


if __name__ == '__main__':
    main()
