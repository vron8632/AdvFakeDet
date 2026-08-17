# W4 补实验记录（2026-08-17 追加）：SOTA 基线 + 消融 + BER 曲线 + 顺序实验

> 日期: 2026-08-17 | 环境: newpatch (torch) + fawkes (TF) | 数据: LFW 子集 | 状态: 全部完成
> 汇总 JSON: `assets/experiments/new_results_20260817.json`

## 1. 为什么做这批实验（回应审计缺口）

`docs/EXPERIMENT_AUDIT.md` 列出未完成证据项：
1. ❌ BER 阈值敏感性（θ TPR/FPR 曲线）→ **本次完成**
2. ❌ α 消融（SRG 嵌入强度）→ **本次完成**
3. ❌ 与其他水印方法对比（Stable Signature / InvisMark）→ **本次完成 InvisMark**（Stable Signature 论证不可直接适用）
4. ✅ 多消息容量 → **本次补上交叉串扰数据**

## 2. 实验 1：BER 阈值敏感性曲线（θ TPR/FPR）

**方法**：正样本 = 水印遮蔽图 per-image 位精度（已有 full_low/full_mid 数据）；负样本 = 无印遮蔽图 × 随机消息 500 次解码（新跑，`/tmp/fpr_negatives_low.json` / `fpr_negatives_mid.json`）。

| θ | TPR B (low) | TPR C (low) | TPR B (mid) | FPR low | FPR mid |
|---|---|---|---|---|---|
| 0.15 | 95.2% | 93.1% | 95.0% | 0.00% | 0.00% |
| 0.20 | 98.7% | 97.4% | 100% | 0.20% | 0.00% |
| 0.25 | 99.2% | 98.6% | 100% | 0.40% | 0.80% |
| 0.30 | 99.4% | 98.9% | 100% | 1.00% | 2.40% |

**关键发现**：负样本 BER 集中在 0.50（mean 0.5003）。**论文原 "FPR=0.00%" 需要修正**：θ=0.25 时 FPR 实为 0.4–0.8%；θ≤0.15 才为 0%（500 trials）。论文 Table 3 已改为完整 θ 表 + Fig 6 曲线，正文诚实报告。

## 3. 实验 2：α 消融（SRG 嵌入强度，mid n=200, β=6）

| α | PSR (gallery-query) | WM clean | WM JPEG50 | PSNR |
|---|---|---|---|---|
| 0.25 | 92.5% | 35.0% | 20.5% | 41.9 |
| 0.50 | 93.0% | 98.0% | 75.0% | 36.1 |
| 0.75 | **93.5%** | 100% | 91.0% | 32.5 |
| **1.00** | **93.5%** | 99.5% | **95.0%** | 30.1 |
| 1.25 | 92.0% | 100% | 96.0% | 28.2 |
| 1.50 | 92.5% | 100% | 97.5% | 26.6 |

**结论**：α∈[0.75,1.0] 是甜点区（PSR 保持 93.5%）；α<0.5 水印太弱（JPEG50 TPR 20.5%），α>1.0 破坏遮蔽。α=1.0 近最优。脚本：`code/05_freq_constraint/run_alpha_ablation.sh`，产物 `assets/experiments/alpha_ablation/`。

## 4. 实验 3：SOTA 基线对比（InvisMark, WACV 2025）

**设置**：官方 checkpoint（100-bit, 256×256）从 HuggingFace 镜像下载（`assets/weights/invismark/paper.ckpt`, 1.23GB）；代码 `baselines/invismark/`；评估脚本 `code/06_eval/eval_invismark.py`。与 WAM 相同协议（JPEG80/50 + BER≤0.25 TPR）。

| 方法 | PSR (mid) | WM clean | JPEG80 | JPEG50 | PSNR/SSIM |
|---|---|---|---|---|---|
| B: WAM global β6 | 94.0% | 100% | 100% | 93.5% | 29.0/0.851 |
| C: WAM SRG β6 | 93.5% | 99.5% | 100% | **95.0%** | 30.1/0.879 |
| InvisMark official | 94.5% | 100% (95.1% acc) | **0.0%** (49.7%) | **0.0%** (50.2%) | 49.6/0.991 |

**关键发现（重要）**：
- InvisMark 在干净人脸也扛不住 JPEG（JPEG80 acc 49.5% ≈ 随机；连 JPEG95 也是 55% 随机）—— 官方 checkpoint 的 JPEG 鲁棒性不足（其 Noiser 中 JPEG 每 batch 只有 ~1/15 概率被选中）。
- 用 InvisMark 自己的 v2.JPEG(quality=50) 路径复测：20 张 acc 51.3% ≈ 随机 → 不是我们协议的问题。
- 结论：WAM + BER 检测的 JPEG 鲁棒是本文 C2 的实打实贡献；InvisMark 作为"能嵌入任意消息"的 SOTA 神经水印基线被公平对比。

**Stable Signature 为什么不跑**：需要 latent diffusion decoder（SD2.1/SDXL）+ per-key extractor 训练，且设计目标是"生成模型 root 固定签名"，无法对任意遮蔽照片直接嵌入消息 → 论文中论证性排除，对比 InvisMark（最接近的适用基线）。

## 5. 实验 4：嵌入顺序（watermark-then-cloak vs cloak-then-WAM）

| 顺序 | n | PSR | WM clean | mean bit acc |
|---|---|---|---|---|
| cloak only (A) | 200 | 95.0% | — | — |
| **cloak → WAM (C)** | 200 | **93.5%** | 99.5% | 94.7% |
| WAM → cloak (β=2) | 50 | 70.0% | 100% | 88.3% |
| WAM → cloak (β=6) | 200 | 81.5% | 100% | 95.6% |

**关键发现**：先嵌水印再遮蔽会消耗感知预算，削弱遮蔽（PSR 95%→70–81.5%）；我们的"先遮蔽再嵌水印"顺序保持 PSR 93.5%。直接回答审稿人可能的"为什么不先嵌再遮"质疑。产物 `/tmp/wm_then_cloak*`。

## 6. 实验 5：多消息容量（交叉串扰）

- 同消息解码：mean bit acc 99.6%
- 用其他图片消息解码（87 次交叉试验）：**FPR = 0.0%**（无串扰）→ 支持每图独立溯源。

## 7. 对论文的修改

- main.tex: 新增 Fig 6（BER 曲线）、Table 3（θ 敏感性）、Table 5（InvisMark 对比）、Table 7（α 消融）、Table 8（顺序实验）、多消息段落；修正 FPR 主张（0% → 0.4–0.8% @ θ=0.25）；结论扩为四点。
- 编译成功：15 页（preprint 12pt）。

## 8. 遗留事项
- Stable Signature 对比未做（论证性排除，见上）
- teaser/框架图仍为占位（用户 gpt-image-2 生成）
- 作者信息 TBD
- 投稿材料（cover letter / highlights / author contributions）下一步

## 9. ⚠️ 重大协议修正（同日发现，见 PROTOCOL_CORRECTION_20260817.md）
- `--jpeg_quality -1` 在 PIL 中等价于 JPEG75，导致论文原 "clean" 列（99.2/98.6 等）实际是 JPEG75
- 核心动机表述修正：遮蔽本身不破坏解码（true-clean 99.84→99.89），瓶颈是 JPEG 重压缩，遮蔽图略更脆弱（JPEG75: 85.2 vs 88.3）
- Table 1/2/3/4/5 的 clean 列已全部改为 true-clean 真值（100%）
- BER 阈值曲线改为 JPEG75 部署条件、正负样本协议匹配
- 数据: assets/experiments/honest_core_facts.json
