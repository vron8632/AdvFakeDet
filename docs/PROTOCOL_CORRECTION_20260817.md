# ⚠️ 协议修正记录（CRITICAL: 2026-08-17 下午发现）

> 重要：本修正改变了论文的核心表述，但**不改变任何结论的方向**——反而让结论更强、更诚实。

## 问题：`--jpeg_quality -1` 在 PIL 中等价于 JPEG75

`eval_wam_decode.py` 中 `--jpeg_quality -1` 被用作"无 JPEG（clean）"的哨兵值，但代码逻辑是：
```python
if jpeg_quality is not None:   # -1 不是 None → 进入分支！
    img.save(buf, format="JPEG", quality=jpeg_quality)  # quality=-1 → PIL 默认 75
```
已实测确认：`quality=-1` 与 `quality=75` 输出**逐字节相同**。

**影响范围**：所有用 `--jpeg_quality -1` 跑出的 "clean" 数字，实际是 **JPEG75 重压缩** 后的数字。

## 对论文数字的修正（全部重测）

### 1. 核心动机（原 "cloaking-watermark conflict" 表述有协议错误）
- 原表述：clean 99.8% → cloak 85.2%（98%→6% TPR@95%）
- 问题：clean 用的是 true-clean（jpeg_quality=None），cloak 用的是 JPEG75（q=-1）——**协议不匹配**！
- 正确事实（协议匹配后）：
  | 条件 | bit acc | TPR@95% |
  |---|---|---|
  | clean, true clean | 99.84% | 98.0% |
  | cloak, true clean | **99.89%** | **99.4%** |
  | clean, JPEG75 | 88.25% | 14.0% |
  | cloak, JPEG75 | 85.19% | 6.0% |
- **结论改写**：遮蔽本身在像素级不破坏水印解码（99.84→99.89）；真正的瓶颈是 **JPEG 重压缩**（分享平台的默认格式），遮蔽图对 JPEG 略更脆弱（JPEG75 下 85.2% vs 88.3%）。论文 Sec 4.2 已改写为 "JPEG-Fragility Bottleneck"。

### 2. 主结果表（Table 1, β=6）"WM clean" 列
- 原 99.2/98.6%（其实是 JPEG75）→ 真 clean = **100.0/100.0%**
- JPEG80/50 列不变（本来就是真 JPEG）

### 3. 强度校准表（Table 2）
- 原 "clean TPR@95%" 6.0/57.9% 其实是 JPEG75 → 新增 true-clean 列（99.4/99.7%）
- 结论更清晰：强度不改变 true-clean 解码（都很高），买的是 **JPEG 鲁棒性**

### 4. BER 阈值表（Table 3）与 Fig 6
- 全部改为 **JPEG75 部署条件、正负样本协议匹配**：TPR B 99.2%/C 98.6%/mid 100% @ θ=0.25，FPR 0.2-0.6%
- 原 FPR 0.4-0.8% 是 true-clean 负样本 vs JPEG75 正样本的错配

### 5. mid 表（Table 4）WM clean
- 100/99.5 → **100/100**（true clean）

### 6. InvisMark 对比表（Table 5）WAM 行 WM clean
- 100/99.5 → **100/100**；InvisMark 行不变（其 clean 本身是 true clean）

## 未受影响的部分（验证过）
- PSR / 遮蔽保持（extractor_2 评估）—— 与 JPEG 无关
- SRG 效果（36.1→42.1%）、α 消融、顺序实验、多消息容量
- InvisMark JPEG 失效结论（其失败在 JPEG80/50，独立于 WAM 协议）
- "JPEG50 精确解码难"（TPR@95% ~10%）结论

## 数据与代码
- 完整协议匹配数据：`assets/experiments/honest_core_facts.json`
- 负样本 FPR（JPEG75）：`/tmp/fpr_negatives_{low,mid}_j75.json`
- 正样本 true-clean 重测：`/tmp/{B,C}_{low,mid}_clean.json`、`/tmp/clean100_j{75,80,50}.json`
- 验证脚本：`/tmp/fpr_measure_j75.py`

## 教训
1. 哨兵值（-1）在库函数中有隐含语义，必须显式验证
2. 论文任何 "clean vs 压缩" 对比，正负样本必须同协议
3. 此修正由 2026-08-17 下午补实验（负样本 FPR 测量）触发发现
