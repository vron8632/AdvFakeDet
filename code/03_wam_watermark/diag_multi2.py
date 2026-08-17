import json, os, sys
import numpy as np, torch
sys.path.insert(0, 'baselines/wam'); sys.path.insert(0, 'baselines/wam/notebooks')
from inference_utils import load_model_from_checkpoint
from watermark_anything.data.transforms import get_transforms_segmentation
from watermark_anything.data.loader import get_dataloader
from watermark_anything.losses.detperceptual import LPIPSWithDiscriminator
import omegaconf

device = 'cuda:0'
params = json.load(open('baselines/wam/checkpoints/params.json'))
base = os.path.dirname('baselines/wam/checkpoints/params.json')
for k in ('embedder_config', 'augmentation_config', 'extractor_config', 'attenuation_config'):
    v = params.get(k)
    if v and not os.path.isabs(v):
        p1 = os.path.join('baselines/wam', v); p2 = os.path.join(base, v)
        params[k] = p1 if os.path.exists(p1) else p2
json.dump(params, open('/tmp/_d.json', 'w'))
wam = load_model_from_checkpoint('/tmp/_d.json', 'baselines/wam/checkpoints/checkpoint.pth').to(device)
wam.train(); wam.roll_probability = 0.2; wam.scaling_w = 2.0
loss_fn = LPIPSWithDiscriminator(balanced=True, total_norm=0.0, disc_weight=0.0, percep_weight=0.0,
    detect_weight=1.0, decode_weight=6.0, disc_start=0, disc_num_layers=2, percep_loss='none').to(device)
train_t, _, _, _ = get_transforms_segmentation(256)
loader = get_dataloader('assets/wam_finetune/train', transform=train_t, batch_size=8, shuffle=True, num_workers=0)
for it, (imgs, masks) in enumerate(loader):
    if it >= 8: break
    imgs = imgs.to(device)
    out = wam(imgs, masks, no_overlap=False, params=omegaconf.OmegaConf.create({'img_size_extractor': 256}))
    out['preds'] /= 1.0
    last_layer = wam.embedder.get_last_layer()
    loss, logs = loss_fn(imgs, out['imgs_w'], out['masks'], out['msgs'], out['preds'], 0, 0, last_layer=last_layer)
    pm = out['preds'][:, 1:].mean().item()
    mf = out['masks'].float().mean().item()
    print(f"batch {it}: decode={logs['decode_loss']:.4f} detect={logs['detect_loss']:.4f} mask_frac={mf:.3f} preds_msg_mean={pm:.4f} aug={out['selected_aug']}")
