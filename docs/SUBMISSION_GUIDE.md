# Signal Processing: Image Communication 投稿指南

> **逐步操作版请看** [`SUBMISSION_STEP_BY_STEP.md`](SUBMISSION_STEP_BY_STEP.md)
> 本文档提供背景信息和参考。

> 目标期刊: Signal Processing: Image Communication (Elsevier)
> ISSN: 0923-5965 | JCR: Q2 (Engineering, Electrical & Electronic) | 非 OA
> 2024 IF: ~3.5 | 审稿周期: 首轮 2-3 个月

---

## 1. 审稿制度：单盲（Single-Blind）

**不是双盲。** SPIC 使用 Elsevier 标准单盲审稿：
- ✅ 审稿人知道作者是谁
- ❌ 作者不知道审稿人是谁
- 因此**正文中可以引用自己的工作**（如 "our previous work..."），但应保持客观语气

**与双盲期刊的区别**：不需要隐藏作者身份、致谢、自引。正常写即可。

---

## 2. 投稿系统

- **系统**: Elsevier Editorial Manager (EM) 或 ScholarOne Manuscripts
  - SPIC 目前使用 **Editorial Manager**: https://www.editorialmanager.com/spic/
- **首次投稿需要**：
  - 注册账号（用通讯作者邮箱）
  - 选择文章类型: "Research Paper"
  - 上传文件（详见 §4）
  - 填写 cover letter、highlights、keywords、作者信息
  - 推荐审稿人 2-3 人（可选但建议提供）

---

## 3. 论文格式要求

### 3.1 模板
- **必须使用 Elsevier 的 elsarticle 类**: 已在 `paper/elsevier_template/` 中
- 推荐模板选项: `\documentclass[preprint,12pt]{elsarticle}`（投稿用 preprint 格式）
- 也可使用 `\documentclass[review,12pt]{elsarticle}`（行号版本，方便审稿）

### 3.2 长度
- **无严格页数限制**，但建议正文 10-15 页（双栏 12pt）
- 参考文献不计入页数限制
- Supplementary Information 可另附（单独文件）

### 3.3 语言
- 英文（美式或英式均可，但全文一致）
- 非英语母语作者建议投稿前进行语言润色（Cover Letter 中可说明已润色）

### 3.4 结构（Research Paper）
```
1. Introduction
2. Related Work (可选，或合并入 Introduction)
3. Proposed Method
4. Experiments
   4.1 Experimental Setup
   4.2 Main Results
   4.3 Ablation Studies
   4.4 Comparison with State-of-the-Art
5. Discussion (可选，可合并入 4.x 或 Conclusion)
6. Conclusion
References
Appendix (optional)
```

### 3.5 图表
- **图**: EPS, TIFF, PDF 均可；分辨率 ≥ 300 dpi（色彩图），≥ 600 dpi（线条图）
- **表**: LaTeX tabular 环境即可，不要用图片代替表格
- 图表标题在**下方**（figure caption below, table caption above）
- 正文中必须按顺序引用每个图/表

### 3.6 参考文献
- 推荐使用 **Numbered** 格式 `[1], [2], ...`（SPIC 常用）
- 或 **Harvard** 格式（作者-年份）
- 正文引用: `\cite{key}` → 自动匹配
- 确保每条 BibTeX 条目完整（DOI 尽量包含）

### 3.7 数学公式
- 使用 `equation` / `align` 环境
- 内联公式用 `$...$`
- 关键公式需编号（Eq. 1, Eq. 2, ...）

---

## 4. 首次投稿文件清单

### 4.1 必须上传的文件
| 文件 | 说明 | 格式 |
|---|---|---|
| **Cover Letter** | 给编辑的信（见 SUBMISSION_PACKAGE.md） | PDF 或 Word |
| **Manuscript** | 主论文（含正文+参考文献） | PDF（编译好的） |
| **Figure files** | 所有图的源文件（可编辑格式优先） | PDF/EPS/TIFF，≥300dpi |
| **LaTeX source** | .tex + .bib + 图文件（打包 zip） | Zip 压缩包 |

### 4.2 在线填写（非上传）
| 项目 | 说明 |
|---|---|
| **Title** | 论文标题 |
| **Authors** | 所有作者（姓名、单位、邮箱、ORCID） |
| **Abstract** | 150-250 词 |
| **Keywords** | 3-6 个关键词 |
| **Highlights** | 3-5 条（每条 ≤85 字符含空格） |
| **Suggested Reviewers** | 2-3 名（姓名、单位、邮箱，建议非合作者） |
| **Exclude Reviewers** | 可选（最多 2 名，说明排除理由） |
| **Funding** | 基金来源（如有） |
| **Declaration of Interest** | 利益冲突声明 |
| **Data Availability** | 数据可用性声明 |
| **CRediT Author Statement** | 作者贡献（见 SUBMISSION_PACKAGE.md） |

---

## 5. Cover Letter 要点

已在 `docs/SUBMISSION_PACKAGE.md` 准备好草稿，核心内容：
1. 论文标题和投稿类型
2. 研究背景和动机（1 段）
3. 贡献列表（4 点，编号清晰）
4. 与已有工作的差异化（回应 ARFP/EIAW）
5. 数据规模和完整性说明
6. 未发表声明 + 利益冲突声明

**注意**：Cover Letter 中可以提自己的名字（单盲），但不要过度自引。

---

## 6. Highlights 撰写（已在 SUBMISSION_PACKAGE.md 准备好）

要求：3-5 条，每条 ≤85 字符含空格，用短句陈述核心发现。

已准备的版本（缩短后均 ≤85 字符）：
1. JPEG recompression collapses WAM decoding on cloaked faces (6% TPR@95%).
2. Safety-region guidance restores cloaking retention (36.1%→42.1%).
3. Strength calibration + BER detection give 93–99% JPEG-robust decode at 0–0.8% FPR.
4. Sequential cloak→watermark keeps PSR 93.5%; reverse order drops to 70–81.5%.
5. Beats SOTA InvisMark, which fails under JPEG on the same protocol.

---

## 7. 推荐审稿人（需提供 2-3 人）

建议方向（**必须找真实存在的、近期发表过相关论文的人**）：

| 方向 | 可选领域 | 人数 |
|---|---|---|
| 人脸隐私保护 | Fawkes/LowKey/Glaze 相关 | 1 |
| 神经网络水印 | WAM/Stable Signature/DeepWatermark | 1 |
| 图像取证/溯源 | 可验证信息嵌入、FR鲁棒水印 | 1 |

**要求**：
- 与你无直接合作关系（无共同论文）
- 不同机构
- 近 3 年有相关发表
- 用机构邮箱（非 gmail/163）

---

## 8. 数据可用性声明

SPIC 要求提供 Data Availability Statement。建议模板：

> The LFW dataset used in this study is publicly available at
> http://vis-www.cs.umass.edu/lfw/. The Fawkes implementation is available at
> https://sandlab.cs.uchicago.edu/fawkes/. The WAM watermarking code and our
> experimental scripts will be made available upon acceptance. The InvisMark
> baseline was used under its original license from HuggingFace.

如果代码暂不开源，可用"upon acceptance"承诺。

---

## 9. 投稿流程时间线

| 步骤 | 预计时间 |
|---|---|
| 投稿系统提交 | 1 天（信息填写 + 文件上传） |
| 编辑初审（Desk Review） | 1-2 周 |
| 同行评审 | 2-3 个月 |
| 修改回复（Major/Minor Revision） | 1-3 个月 |
| 终审决定 | 1-2 周 |
| 校对（Proof） | 1-2 周 |
| **总计** | **4-6 个月** |

---

## 10. 常见拒稿原因（SPIC 特定）

1. **超出范围**: SPIC 关注图像/视频信号处理（压缩、水印、分割、增强等），纯人脸识别论文不合适
2. **实验不充分**: 必须有 SOTA 对比 + 消融实验（我们已有：InvisMark 对比 + α 消融 + 顺序实验 + BER 曲线）
3. **novelty 不足**: 必须清楚说明与 EIAW、ARFP、Fawkes 的区别（我们已建立差异化矩阵）
4. **语言问题**: 非母语建议先润色再投

---

## 11. 我们的论文优势（投稿前自检）

| 检查项 | 状态 |
|---|---|
| 属于 SPIC 范围（图像水印 + 隐私保护） | ✅ |
| 有 SOTA 基线对比（InvisMark） | ✅ |
| 有消融实验（α、顺序、BER θ） | ✅ |
| 有大规模验证（1000 张 LFW） | ✅ |
| 有理论/机制解释（SRG、强度校准） | ✅ |
| 诚实报告局限（迁移性、JPEG50） | ✅ |
| 引用并差异化了 ARFP/EIAW | ✅ |
| Cover Letter/Highlights 已准备 | ✅ |
| 推荐审稿人待用户提供 | ❌ 需用户填写 |
| 作者信息/致谢待填写 | ❌ 需用户填写 |
| fig1/fig2 图待生成 | ⏳ 占位中 |

---

## 12. 投稿前最后 Checklist

- [ ] main.tex 作者/单位/致谢补全（替换 TBD）
- [ ] fig1 teaser + fig2 框架图生成并替换占位
- [ ] PDF 编译无报错
- [ ] 所有表/图在正文中被引用（无孤立项）
- [ ] 参考文献格式一致（全部 Numbered 或全部 Harvard）
- [ ] Highlights 字符数检查（每条 ≤85）
- [ ] Abstract 词数检查（150-250 词）
- [ ] 推荐审稿人名单（2-3 人，真实存在）
- [ ] 数据可用性声明
- [ ] Cover Letter 中 TBD 替换为真实信息
- [ ] 上传文件完整性检查
