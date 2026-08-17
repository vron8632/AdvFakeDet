# 新颖性调研报告 v2（含 ARFP 撞车分析）

> 日期: 2026-08-17 | 方法: OpenAlex + arXiv + 全文精读 | 状态: 需调整论文定位

## 1. 重大发现：ARFP 已发表"遮蔽+可验证信息"

**ARFP**（Asymmetric Reversible Face Protection, arXiv:2605.01217, 2026-05, 四川大学等）
- 目标：遮蔽可逆（授权恢复）+ 抗逆向攻击 + 篡改指示
- 方法：Key-Conditioned Manifold Binding + Adversarial Restoration-Aware Training + Authorized Reversible Restoration
- 附加信息：nonce m 嵌入 + 轻量解码器恢复 + BER 一致性检查
- **JPEG 下 BER 4.5%**（他们的 nonce 鲁棒性）
- 评估：PSR（100% - FR accuracy）、恢复保真、LFW+FaceScrub、8 个 FR 模型
- 全文已下载: related_work/arfp_2605.01217.pdf

## 2. ARFP vs 我们的差异矩阵

| 维度 | ARFP | 我们（原计划） | 差异 |
|---|---|---|---|
| 核心目标 | **可逆恢复**（恢复原图） | **溯源验证**（归属/来源） | 应用语义不同 |
| 附加信息 | nonce（生成条件变量） | WAM 32-bit 消息（VAE 嵌入） | 机制不同 |
| 训练范式 | **联合训练**（恢复感知） | **顺序嵌入**（cloak→WM） | 回应 EIAW Table 9 |
| 空间引导 | 无 | **安全区域图**（FR 梯度） | 我们独有 |
| 强度校准 | 无 | **scaling_w 校准 + BER 检测协议** | 我们独有 |
| 冲突量化 | 无（联合训练回避冲突） | **遮蔽-水印冲突量化**（98%→6%） | 我们独有 |
| 检测协议 | BER 表（单点） | **TPR/FPR 检测协议**（θ 敏感性） | 我们更系统 |

## 3. 论文定位调整（防撞车）

**新定位**：*Sequential Provenance-Verifiable Face Cloaking* —— 不追求"可逆"，专注"溯源/归属验证"，证明**顺序嵌入 + 空间引导 + 强度校准**可以达到与联合优化相当的效果（直接回应 EIAW Table 9 与 ARFP 的联合路线）。

**必须引用的"山"**：
1. EIAW（BDMA 2026）：分类场景联合优化 vs 顺序的争论
2. ARFP（2026）：遮蔽+可验证信息（可逆路线）→ 我们走溯源路线并证明顺序可行
3. WAM（ICLR 2025）：神经水印基础
4. Fawkes/LowKey/Glaze：遮蔽基础

**核心贡献（3 个）**：
1. **冲突量化**：Fawkes 遮蔽破坏 WAM 解码（98%→6% TPR@95%），首个量化报告
2. **机制**：安全区域图（SRG）+ 强度校准 + BER 检测 → 遮蔽保持与溯源共存
3. **实证**：顺序嵌入可行（回应 EIAW/ARFP 的联合路线），JPEG 鲁棒 93-99%

## 4. 剩余风险与对策
| 风险 | 对策 |
|---|---|
| 审稿人说"ARFP 已做" | 强调溯源 vs 恢复语义、顺序 vs 联合、SRG/BER 协议独有 |
| 遮蔽迁移性差（arcface 无效） | 主评估用训练空间 PSR + 诚实局限；或改用更强遮蔽 |
| "遮蔽+水印"组合平庸 | 强化 JPEG 鲁棒性（BER 93-99%）与 0% FPR 的系统协议 |

## 5. 结论
- idea 的新颖性**受 ARFP 严重挑战**，但差异化空间明确（溯源/顺序/SRG/BER）
- 若按新定位执行，JCR Q2 期刊可接受；顶会仍需更硬的贡献
- 必须补的实验：E 组（联合优化实证对比，直接打 ARFP/EIAW 的联合路线）
