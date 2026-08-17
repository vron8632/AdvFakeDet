#!/bin/bash
# mid 主实验：A_mid(遮蔽) → B_mid(全局WM sw6) → C_mid(安全图WM sw6) → PSR+水印评估
set -e
ROOT=/home/jiujiu/Projects/AdvFake
cd $ROOT
CLOAK=assets/experiments/A_mid/input
OUT=assets/experiments/full_mid
mkdir -p $OUT

echo "===== [1/4] 安全区域图 ====="
/home/jiujiu/miniconda3/envs/newpatch/bin/python code/04_safety_map/gen_safety_map.py \
  --img_dir $CLOAK --out_dir $OUT/safety_maps --suffix _cloaked.jpeg 2>/dev/null | tail -1

echo "===== [2/4] B_mid 全局 WAM (sw6) ====="
/home/jiujiu/miniconda3/envs/newpatch/bin/python code/03_wam_watermark/embed_wam.py \
  --input_dir $CLOAK --out_dir $OUT/B_sw6 --mode global --scaling_w 6.0 2>/dev/null | tail -1

echo "===== [3/4] C_mid 安全图 WAM (sw6) ====="
/home/jiujiu/miniconda3/envs/newpatch/bin/python code/03_wam_watermark/embed_wam.py \
  --input_dir $CLOAK --out_dir $OUT/C_sw6 --mode safety_map --safety_map_dir $OUT/safety_maps --scaling_w 6.0 2>/dev/null | tail -1

echo "===== [4/4] 评估 ====="
# PSR（extractor_2，遮蔽训练空间）
for TAG in "A $CLOAK _cloaked.jpeg" ; do
  set -- $TAG
  /home/jiujiu/miniconda3/envs/fawkes/bin/python code/06_eval/eval_psr.py \
    --orig_dir $CLOAK --adv_dir $CLOAK --ids assets/dataset/lfw1000/ids.json \
    --adv_suffix $3 --model extractor2 --n 200 --out $OUT/${1}_psr.json 2>/dev/null | grep PSR | sed "s/^/[${1}] /"
done
for TAG in "B_sw6 _cloaked_wm.jpg" "C_sw6 _cloaked_wm.jpg"; do
  set -- $TAG
  /home/jiujiu/miniconda3/envs/fawkes/bin/python code/06_eval/eval_psr.py \
    --orig_dir $CLOAK --adv_dir $OUT/$1 --ids assets/dataset/lfw1000/ids.json \
    --adv_suffix $2 --model extractor2 --n 200 --out $OUT/${1}_psr.json 2>/dev/null | grep PSR | sed "s/^/[${1}] /"
done
# 水印解码（clean/JPEG80/JPEG50, BER）
for TAG in B_sw6 C_sw6; do
  for Q in -1 80 50; do
    /home/jiujiu/miniconda3/envs/newpatch/bin/python code/06_eval/eval_wam_decode.py \
      --wm_dir $OUT/$TAG --manifest $OUT/$TAG/manifest.json --jpeg_quality $Q --ber_threshold 0.25 \
      --out $OUT/${TAG}_q${Q}.json 2>/dev/null | grep "wam decode" | sed "s/^/[${TAG} q=${Q}] /"
  done
done
echo "===== DONE ====="
