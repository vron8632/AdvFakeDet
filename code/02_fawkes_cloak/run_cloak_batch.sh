"""
A 组实验：Fawkes 遮蔽基线（批量）
流程: LFW1000 original/ → Fawkes cloak (mode=low/mid/high) → 双模型评估（extractor_2 自检 + facenet 迁移）
用法:
  bash code/02_fawkes_cloak/run_cloak_batch.sh assets/dataset/lfw1000/original low 0
"""
#!/bin/bash
set -e
SRC_DIR=${1:-assets/dataset/lfw1000/original}
MODE=${2:-low}
GPU=${3:-0}
OUT_ROOT="assets/experiments/A_${MODE}"

mkdir -p "$OUT_ROOT"
# 拷贝原图（Fawkes 会原地生成 *_cloaked）
CLOAK_DIR="$OUT_ROOT/input"
rm -rf "$CLOAK_DIR"
mkdir -p "$CLOAK_DIR"
cp "$SRC_DIR"/*.jpg "$CLOAK_DIR/"

echo "[A-${MODE}] cloaking $(ls $CLOAK_DIR | wc -l) images, mode=${MODE} gpu=${GPU}"
/home/jiujiu/miniconda3/envs/fawkes/bin/python -m fawkes.protection \
  -d "$CLOAK_DIR" -m "$MODE" --format jpg --gpu "$GPU" \
  > "$OUT_ROOT/cloak.log" 2>&1

echo "[A-${MODE}] cloaking done, cloaked files: $(ls $CLOAK_DIR/*cloaked* 2>/dev/null | wc -l)"
