#!/bin/bash
# 全量实验编排：A(cloak) → B(全局WM) → C(安全图WM) → 评估
# 用法: bash code/run_full_experiment.sh [mode] [n]
MODE=${1:-low}
N=${2:-1000}
ROOT=assets/experiments/full_${MODE}
DATA=assets/dataset/lfw1000/original
mkdir -p $ROOT

echo "===== [1/3] Fawkes ${MODE} cloaking ====="
bash code/02_fawkes_cloak/run_cloak_batch.sh $DATA $MODE 0
CLOAK_DIR=$ROOT/../A_${MODE}/input
mkdir -p $CLOAK_DIR
cp assets/experiments/A_${MODE}/input/* $CLOAK_DIR/ 2>/dev/null || true

echo "===== [2/3] WAM embedding (B global + C safety-map) ====="
/home/jiujiu/miniconda3/envs/newpatch/bin/python code/03_wam_watermark/embed_wam.py \
  --input_dir $CLOAK_DIR --out_dir $ROOT/B_global --mode global
/home/jiujiu/miniconda3/envs/newpatch/bin/python code/04_safety_map/gen_safety_map.py \
  --img_dir $CLOAK_DIR --out_dir $ROOT/safety_maps --suffix _cloaked.jpeg
/home/jiujiu/miniconda3/envs/newpatch/bin/python code/03_wam_watermark/embed_wam.py \
  --input_dir $CLOAK_DIR --out_dir $ROOT/C_safemap --mode safety_map \
  --safety_map_dir $ROOT/safety_maps

echo "===== [3/3] Evaluation ====="
# extractor_2 遮蔽保持
timeout 3600 conda run -n fawkes python code/06_eval/eval_extractor2.py \
  --orig_dir $CLOAK_DIR --adv_dir $CLOAK_DIR --ids assets/dataset/lfw1000/ids.json \
  --adv_suffix _cloaked.jpeg --out $ROOT/A_ext2.json
# B/C 水印解码
/home/jiujiu/miniconda3/envs/newpatch/bin/python code/06_eval/eval_wam_decode.py \
  --wm_dir $ROOT/B_global --manifest $ROOT/B_global/manifest.json --out $ROOT/B_dec_clean.json
/home/jiujiu/miniconda3/envs/newpatch/bin/python code/06_eval/eval_wam_decode.py \
  --wm_dir $ROOT/C_safemap --manifest $ROOT/C_safemap/manifest.json --out $ROOT/C_dec_clean.json
echo "===== DONE ====="
