# 实验完备性审计 & 补充计划

## 已有实验（9 表 6 图，n=1000/200/200）

| 实验 | 表/图 | 数据量 | 状态 |
|---|---|---|---|
| JPEG 瓶颈分析 | Table 1 | n=1000 | ✅ |
| 主结果（低遮蔽） | Table 2 | n=1000 | ✅ |
| 强度校准 | Table 3 | n=1000 | ✅ |
| BER 阈值敏感性 | Table 4 | n=500×4 | ✅ |
| 强遮蔽 | Table 5 | n=200 | ✅ |
| InvisMark SOTA 对比 | Table 6 | n=200 | ✅ |
| 顺序 vs 联合 | Table 7 | n=20 | ✅ |
| SRG α 消融 | Table 8 | n=200 | ✅ |
| 嵌入顺序 | Table 9 | n=200 | ✅ |
| 多消息容量 | 文字 | n=87 | ✅ |
| 定性图 | fig3 | - | ✅ |
| 主结果图 | fig4 | - | ✅ |
| JPEG 鲁棒图 | fig5 | - | ✅ |
| BER 曲线 | fig6 | - | ✅ |

## 需补充（SCI Q2 必需）

### 🔴 高优先级
1. **t-SNE 嵌入空间可视化** — 从 arcface34 提取 clean/cloaked/watermarked 的 FR 嵌入，画 t-SNE 散点图，展示"遮蔽把身份推远，水印保持分离"。这是论文最有说服力的图。
   - 数据：full_low/ 下有 A/B/C 各 1000 张，full_mid/ 下有 A/B/C 各 200 张
   - 脚本：需新写 `code/06_eval/eval_tsne.py`

2. **统计显著性** — 关键比较加 bootstrap 置信区间
   - B vs C 的 PSR 差异 (36.1% vs 42.1%, n=1000) → bootstrap 95% CI
   - BER 阈值曲线加 error bar
   - 脚本：需新写 `code/06_eval/eval_significance.py`

3. **感知质量对比图** — 4 张并排（原图/遮蔽/遮蔽+水印/安全图），标注 PSNR/SSIM/LPIPS
   - 数据：full_mid/ 下有 C_sw6 的图和 safety_maps
   - 脚本：需新写 `code/06_eval/eval_perceptual.py`

### 🟡 中优先级
4. **更多 SOTA 基线** — 至少加 StegaStamp 或 HiDDeN
   - 需检查 baselines/ 是否有代码
   - 如果没有，至少在 Related Work 中说明为何不直接对比

### 🟢 低优先级
5. **FR 模型消融** — safety map 用不同 FR surrogate 的效果
6. **运行时分析** — embedding/detection 耗时

## 写作改进
1. Abstract 精简（当前~250词→150词）
2. Introduction 改善故事线（背景→冲突→方法→结果）
3. 低遮蔽 PSR 47.4% 的 framing
4. Conclusion 去重复、增强
5. 去 AI 味

## 作者信息
- 一作：Pan Ouyang, 393974615@qq.com, ORCID: 0009-0003-3995-0847
- 通讯：Junlin Ouyang, 18818351620@163.com, ORCID: 0000-0001-7155-2732
- 单位：School of Computer Science and Engineering, Hunan University of Science and Technology
