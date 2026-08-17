#!/bin/bash
# WAM JPEG-aware 微调（C2 加强版）：在 LFW 上微调，JPEG-heavy 增强
set -e
ROOT=/home/jiujiu/Projects/AdvFake
WAM=$ROOT/baselines/wam
OUT=$ROOT/assets/experiments/wam_jpeg_ft
mkdir -p $OUT

cd $WAM
/home/jiujiu/miniconda3/envs/newpatch/bin/python train.py \
  --train_dir $ROOT/assets/wam_finetune/train \
  --train_annotation_file /dev/null \
  --val_dir $ROOT/assets/wam_finetune/val \
  --val_annotation_file /dev/null \
  --output_dir $OUT \
  --augmentation_config configs/all_augs_multi_wm.yaml \
  --embedder_model vae_small --extractor_model sam_base \
  --img_size 256 --img_size_extractor 256 \
  --batch_size 8 --batch_size_eval 16 --workers 4 \
  --epochs 30 \
  --attenuation jnd_1_3_blue \
  --optimizer "AdamW,lr=3e-5" \
  --scheduler "None" \
  --seed 42 \
  --perceptual_loss none --lambda_i 0.0 --lambda_d 0.0 \
  --lambda_w 1.0 --lambda_w2 6.0 \
  --nbits 32 --scaling_i 1.0 --scaling_w 2.0 \
  --resume_from $WAM/checkpoints/checkpoint_wrapped.pth \
  --eval_freq 1 --saveimg_freq 2 --saveckpt_freq 4 \
  --nb_images_eval 50 \
  --debug_slurm \
  --local_rank -1 --master_port -1 \
  > $OUT/finetune.log 2>&1
echo "finetune done, see $OUT/finetune.log"
