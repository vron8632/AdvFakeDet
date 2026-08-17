# 研究方法论手册（从 3 个 skills 仓库提炼）

> 来源: ARIS (Auto-claude-code-research-in-sleep), academic-research-skills (ARS), nature-skills
> 用途: 本项目论文生产的操作规范。完整 SKILL.md 在 _skills/ 下，本文是精要版。

## 1. 全流程（ARIS W1→W3 + ARS 10-stage）

```
W1  Idea Discovery: 方向 → 文献 landscape → idea 排序 → novelty 验证 → 实验计划
W1.5 Experiment Bridge: 计划 → 代码实现 → 实验日志
W2  Auto Review Loop: 论文+结果 → 多模型交叉评审 → 改进（迭代）
W3  Paper Writing: 叙事报告 → LaTeX 论文
W4  Rebuttal（审稿后）
```

**本项目当前阶段**: 已跳过 idea-discovery（方向由用户确定），处于 W1.5（实验实现）+ 部分 W2（每次实验后用 nature-reviewer 评审）。

## 2. 实验规范（ARIS run-experiment / experiment-audit）

- 每个实验: 确定性 seed、记录超参、输出 JSON 结果 + 图片样例
- 实验日志: 用 nature-experiment-log 或自建 docs/W*_*.md 记录
- 审计: 报告结果必须可复现（deterministic），禁止"报喜不报忧"
- GPU 预算: pilot ≤2h/GPU

## 3. Novelty 验证（ARIS novelty-check / prior-art-search）

提交前必须回答：
1. 该组合是否已发表？（用 openalex/arxiv 检索）
2. 与最近似工作的差异点是什么？
3. 审稿人最可能的"so what?"攻击是什么？

## 4. 图表规范（nature-figure + ARIS paper-figure）

- **Figure 1 (Teaser)**: 用户用 gpt-image-2 生成，16:9 占位已建（paper/figures/）
- **Figure 2 (Framework)**: 用户用 gpt-image-2 生成（16:9 占位）
- **实验图表**: 用 Python (matplotlib/seaborn)，按 nature-figure 的 figure-contract 流程：
  1. 定义结论 → 2. 证据逻辑 → 3. 数据完整性 → 4. 期刊模板兼容 → 5. 审稿风险
- 导出: 矢量优先（PDF/SVG），期刊用 300dpi TIFF
- 配色: 统一色板，色盲友好

## 5. 写作规范（ARS academic-paper + nature-writing）

- **结构**: 摘要(动机-方法-结果-贡献) → Intro(漏斗式) → Related(定位) → Method(可复现) → Exp(协议-结果-分析) → 结论
- **每个 claim 必须有证据锚点**（引用 DOI 或自己的实验表）
- **写作质量检查**: 避免 AI 腔（过度副词、空洞连接词、模式化短语）
- **引用**: 用 nature-ref-verifier / citation-audit 逐条核对 DOI
- **材料护照 (Material Passport)**: 每个实验结果记录 provenance（代码路径、数据、seed）

## 6. 评审规范（ARS academic-paper-reviewer + nature-reviewer）

论文初稿完成后，用 7 视角评审：
1. Journal-Fit（期刊匹配度）
2. Novelty（新颖性）
3. Method Correctness（方法正确性）
4. Experimental Soundness（实验完备性）
5. Clarity（清晰度）
6. Devil's Advocate（杠精模式：找最致命缺陷）
7. Ethics/Repro（伦理与可复现）

评审输出: 每个视角给出 Evidence-Anchored 判断（必须有证据，不能空泛）。

## 7. 完整性守则（重要）

- 不允许捏造实验结果；每个数字必须来自实际运行
- 引用必须真实存在（DOI 核对）
- 不做"result laundering"（把失败结果包装成成功）
- 诚实报告负面结果（如 JPEG 鲁棒性失败也是发现）

## 8. 工具速查

| 用途 | 工具 |
|---|---|
| 文献检索 | openalex / arxiv / semantic-scholar skills |
| DOI 核对 | nature-ref-verifier / citation-audit |
| 实验日志 | nature-experiment-log / docs/W*.md |
| 图表 | nature-figure (matplotlib) |
| 论文写作 | nature-writing / academic-paper |
| 审稿 | nature-reviewer / academic-paper-reviewer |
| 统计 | nature-statistics |
