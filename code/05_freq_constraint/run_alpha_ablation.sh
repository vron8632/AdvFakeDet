#!/bin/bash
# α 消融: SRG 嵌入强度 (Eq.3 的 alpha) 对 遮蔽保持(PSR) × 水印解码 × 质量 的影响
# 数据: A_mid 200 张 (Fawkes mid 遮蔽), 安全图已生成
set -e
ROOT=/home/jiujiu/Projects/AdvFake
cd $ROOT
CLOAK=assets/experiments/A_mid/input
MAPS=assets/experiments/full_mid/safety_maps
OUT=assets/experiments/alpha_ablation
IDS=assets/dataset/lfw1000/ids.json
PY=/home/jiujiu/miniconda3/envs/newpatch/bin/python
mkdir -p $OUT

for A in 0.25 0.50 0.75 1.00 1.25 1.50; do
  TAG=alpha${A}
  echo "===== alpha=$A ====="
  $PY code/03_wam_watermark/embed_wam.py \
    --input_dir $CLOAK --out_dir $OUT/$TAG \
    --mode safety_map --safety_map_dir $MAPS --scaling_w 6.0 --alpha $A \
    2>/dev/null | tail -1
  for Q in -1 50; do
    $PY code/06_eval/eval_wam_decode.py \
      --wm_dir $OUT/$TAG --manifest $OUT/$TAG/manifest.json --jpeg_quality $Q \
      --ber_threshold 0.25 --out $OUT/${TAG}_q${Q}.json 2>/dev/null | grep "wam decode" \
      | sed "s/^/[alpha=$A q=$Q] /"
  done
  # PSR (extractor_2, fawkes env) - 注意 embed 输出文件名 cloaked_wm.jpg
  CUDA_VISIBLE_DEVICES=1 conda run -n fawkes python code/06_eval/eval_extractor2.py \
    --orig_dir $CLOAK --adv_dir $OUT/$TAG --ids $IDS --adv_suffix _cloaked_wm.jpg \
    --out $OUT/${TAG}_psr.json 2>/dev/null | grep extractor2 | sed "s/^/[alpha=$A PSR] /"
done
echo "===== ALPHA ABLATION DONE ====="
