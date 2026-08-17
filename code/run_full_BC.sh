#!/bin/bash
# 全量 B/C 组：A_low 遮蔽图 → 安全图 → B(全局WM) → C(安全图WM) → 评估
set -e
ROOT=/home/jiujiu/Projects/AdvFake
cd $ROOT
CLOAK_DIR=assets/experiments/A_low/input
OUT=assets/experiments/full_low
mkdir -p $OUT

echo "===== [1/4] 安全区域图 ====="
/home/jiujiu/miniconda3/envs/newpatch/bin/python code/04_safety_map/gen_safety_map.py \
  --img_dir $CLOAK_DIR --out_dir $OUT/safety_maps --suffix _cloaked.jpeg

echo "===== [2/4] B 组全局 WAM ====="
/home/jiujiu/miniconda3/envs/newpatch/bin/python code/03_wam_watermark/embed_wam.py \
  --input_dir $CLOAK_DIR --out_dir $OUT/B_global --mode global

echo "===== [3/4] C 组安全图 WAM ====="
/home/jiujiu/miniconda3/envs/newpatch/bin/python code/03_wam_watermark/embed_wam.py \
  --input_dir $CLOAK_DIR --out_dir $OUT/C_safemap --mode safety_map --safety_map_dir $OUT/safety_maps

echo "===== [4/4] 评估 ====="
# A 组遮蔽保持（extractor_2）
CUDA_VISIBLE_DEVICES=1 conda run -n fawkes python code/06_eval/eval_extractor2.py \
  --orig_dir $CLOAK_DIR --adv_dir $CLOAK_DIR --ids assets/dataset/lfw1000/ids.json \
  --adv_suffix _cloaked.jpeg --out $OUT/A_ext2.json
# B/C 解码（clean + JPEG）
for TAG in B_global C_safemap; do
  for Q in -1 80 50; do
    /home/jiujiu/miniconda3/envs/newpatch/bin/python code/06_eval/eval_wam_decode.py \
      --wm_dir $OUT/$TAG --manifest $OUT/$TAG/manifest.json --jpeg_quality $Q \
      --out $OUT/${TAG}_dec_q${Q}.json 2>/dev/null | grep "wam decode" | sed "s/^/[${TAG} q=${Q}] /"
  done
done
echo "===== DONE ====="
