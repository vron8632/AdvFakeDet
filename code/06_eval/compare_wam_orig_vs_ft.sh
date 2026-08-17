#!/bin/bash
# 对比评估：原始 WAM vs JPEG-aware 微调 WAM（clean + JPEG 鲁棒性）
set -e
ROOT=/home/jiujiu/Projects/AdvFake
ORIG_CKPT=$ROOT/baselines/wam/checkpoints/checkpoint.pth
FT_CKPT=$ROOT/assets/experiments/wam_cloak_ft/checkpoint_infer.pth
PARAMS=$ROOT/baselines/wam/checkpoints/params.json

# 输入：20 张 Fawkes low cloak 遮蔽图
CLOAK_DIR=/tmp/fawkes20_in
OUT_BASE=/tmp/wam_compare
mkdir -p $OUT_BASE

for TAG in orig ft; do
  CKPT=$ORIG_CKPT; [ $TAG = ft ] && CKPT=$FT_CKPT
  OUT=$OUT_BASE/$TAG
  # 嵌入（全局）
  /home/jiujiu/miniconda3/envs/newpatch/bin/python $ROOT/code/03_wam_watermark/embed_wam.py \
    --input_dir $CLOAK_DIR --out_dir $OUT/wm --mode global \
    --checkpoint $CKPT --params_json $PARAMS 2>/dev/null | tail -1
  # 解码 clean / JPEG80 / JPEG50
  for Q in -1 80 50; do
    /home/jiujiu/miniconda3/envs/newpatch/bin/python $ROOT/code/06_eval/eval_wam_decode.py \
      --wm_dir $OUT/wm --manifest $OUT/wm/manifest.json --jpeg_quality $Q \
      --checkpoint $CKPT --params_json $PARAMS --out $OUT/dec_q${Q}.json 2>/dev/null | grep "wam decode" | sed "s/^/[${TAG} q=${Q}] /"
  done
done
