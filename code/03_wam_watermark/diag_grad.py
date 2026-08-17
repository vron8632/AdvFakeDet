"""诊断2：训练一步前后模型权重与 preds 是否变化"""
import json
import os
import sys

import numpy as np
import torch

sys.path.insert(0, 'baselines/wam')
sys.path.insert(0, 'baselines/wam/notebooks')
from inference_utils import load_model_from_checkpoint
from watermark_anything.data.transforms import get_transforms_segmentation
from watermark_anything.data.loader import get_dataloader
from watermark_anything.losses.detperceptual import LPIPSWithDiscriminator
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
    json.dump(params, open('/tmp/_diag2.json', 'w'))

    wam = load_model_from_checkpoint('/tmp/_diag2.json', 'baselines/wam/checkpoints/checkpoint.pth').to(device)
    wam.train()
    wam.scaling_w = 2.0

    loss_fn = LPIPSWithDiscriminator(
        balanced=True, total_norm=0.0, disc_weight=0.0, percep_weight=0.0,
        detect_weight=1.0, decode_weight=6.0, disc_start=0, disc_num_layers=2,
        percep_loss='none'
    ).to(device)

    train_t, _, _, _ = get_transforms_segmentation(256)
    loader = get_dataloader('assets/wam_finetune/train', transform=train_t, batch_size=8, shuffle=False, num_workers=0)
    imgs, masks = next(iter(loader))
    imgs = imgs.to(device)

    # 记录初始权重
    emb0 = {k: v.clone() for k, v in wam.embedder.state_dict().items() if v.dtype == torch.float32}
    ext0 = {k: v.clone() for k, v in wam.detector.state_dict().items() if v.dtype == torch.float32}

    opt = torch.optim.AdamW([{'params': wam.embedder.parameters()}, {'params': wam.detector.parameters()}], lr=1e-4)
    opt.zero_grad()

    out = wam(imgs, masks, no_overlap=False, params=omegaconf.OmegaConf.create({'img_size_extractor': 256}))
    out['preds'] /= 1.0
    last_layer = wam.embedder.get_last_layer()
    loss, logs = loss_fn(imgs, out['imgs_w'], out['masks'], out['msgs'], out['preds'], 0, 0, last_layer=last_layer)
    print('decode_loss:', logs['decode_loss'].item(), 'detect_loss:', logs['detect_loss'].item())
    loss.backward()

    # 梯度范数
    g_emb = sum(p.grad.abs().sum().item() for p in wam.embedder.parameters() if p.grad is not None)
    g_ext = sum(p.grad.abs().sum().item() for p in wam.detector.parameters() if p.grad is not None)
    print('embedder grad L1:', g_emb, 'detector grad L1:', g_ext)
    n_emb = sum(1 for p in wam.embedder.parameters() if p.grad is not None)
    n_ext = sum(1 for p in wam.detector.parameters() if p.grad is not None)
    print('params with grad: embedder', n_emb, 'detector', n_ext)

    opt.step()
    # 权重变化
    d_emb = sum((wam.embedder.state_dict()[k] - v).abs().sum().item() for k, v in emb0.items())
    d_ext = sum((wam.detector.state_dict()[k] - v).abs().sum().item() for k, v in ext0.items())
    print('embedder weight change L1:', d_emb, 'detector weight change L1:', d_ext)


if __name__ == '__main__':
    main()
