# AdvFakeDet 项目续接指南（HANDOFF v3）

> 更新：2026-08-17 18:30 | 用途：重启/新 agent 快速进入状态
> 项目根：`/home/jiujiu/Projects/AdvFake/` | GitHub: `vron8632/AdvFakeDet` (main)

## 1. 项目在做什么（30 秒版）

**论文项目**：给 Fawkes 遮蔽人脸嵌入可溯源神经网络水印（WAM），让人脸识别继续被骗（遮蔽保持）+ 水印可解码（溯源）+ JPEG 鲁棒。
**目标期刊**：Signal Processing: Image Communication (Elsevier, JCR Q2 非 OA, IF≈3.5)
**核心定位**：Provenance-Verifiable Privacy Cloaking — 顺序嵌入 + 安全区域图（SRG）+ 强度校准 + BER 检测。
**投稿系统**：Elsevier Editorial Manager (单盲审稿)

---

## 2. 当前进度总览

### ✅ 已完成（可以投）

| 类别 | 状态 | 说明 |
|---|---|---|
| 全部实验 | ✅ | 9 组实验全部跑完，含 SOTA 对比、消融、统计分析 |
| 论文正文 | ✅ | main.tex 400+ 行，9 表 8 图 18 引，elsarticle 模板 |
| 摘要精简 | ✅ | ~180 词（原 250），故事性增强 |
| 作者信息 | ✅ | Pan Ouyang (一作), Junlin Ouyang (通讯), 湖南科技大学 |
| 统计分析 | ✅ | Bootstrap 95% CI, p 值，SRG 显著性 p=0.03 |
| t-SNE 可视化 | ✅ | fig7_tsne.png，嵌入空间分析 |
| 感知质量对比图 | ✅ | fig8_perceptual_quality.png，PSNR/SSIM 标注 |
| SOTA 基线对比 | ✅ | InvisMark (WACV 2025) 同协议对比 |
| 消融实验 | ✅ | α 消融、BER 阈值、嵌入顺序、多消息容量 |
| Cover Letter | ✅ | `docs/SUBMISSION_PACKAGE.md` 草稿已备 |
| Highlights | ✅ | 5 条，每条 ≤85 字符 |
| 投稿指南 | ✅ | `docs/SUBMISSION_STEP_BY_STEP.md` 逐步操作版 |
| GitHub 推送 | ✅ | dd67854 + 35819fc 已推送 |

### ⏳ 需要你做的（投稿前必须完成）

| 事项 | 优先级 | 说明 |
|---|---|---|
| 生成 fig1 (teaser) + fig2 (框架图) | 🔴 高 | 按 `paper/FIGURE_PROMPTS_中文.md` 用 gpt-image-2 |
| 编译最终 PDF | 🔴 高 | `cd paper && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex` |
| 找推荐审稿人 2-3 人 | 🔴 高 | Google Scholar 搜相关论文，找无合作的不同机构学者 |
| 替换致谢中的基金号 | 🟡 中 | main.tex 第 346 行 `Grant No.~XXXXXXXX` |
| Cover Letter 转 PDF | 🟡 中 | SUBMISSION_PACKAGE.md → 复制到 Word → 导出 PDF |
| 注册 Editorial Manager | 🟢 低 | https://www.editorialmanager.com/spic/ → Register |

---

## 3. 实验结果汇总（9 组实验）

### 3.1 低遮蔽（Fawkes low, 1000 张, β=6）— 压力测试

| 组 | PSR | WM clean/JPEG80/JPEG50 | PSNR/SSIM/LPIPS |
|---|---|---|---|
| A 仅遮蔽 | 47.4% | — | ~40/0.98/0.01 |
| B 全局强水印 | 36.1% | 99.2/99.6/93.7% | 29.0/0.851/0.140 |
| C 安全图水印 | 42.1% | 98.6/99.0/92.7% | 30.1/0.879/0.111 |

- SRG 恢复 PSR: 36.1%→42.1%，bootstrap 95% CI [0.1%, 8.3%], p=0.03
- FPR=0%（500 次随机消息测试）

### 3.2 强遮蔽（Fawkes mid, 200 张, β=6）— 实际部署场景

| 组 | PSR | WM clean/JPEG80/JPEG50 | sim |
|---|---|---|---|
| A 仅遮蔽 | 95.0% | — | 0.054 |
| B 全局强水印 | 94.0% | 100/100/93.5% | 0.114 |
| C 安全图水印 | 93.5% | 99.5/100/95.0% | 0.083 |

- **关键发现**：强遮蔽下水印与遮蔽共存无损（PSR 93.5-95%）

### 3.3 其他实验

| 实验 | 结果 | 论文位置 |
|---|---|---|
| BER 阈值敏感性 | θ=0.25 TPR 93-100%, FPR 0.2-0.6%; θ≤0.15 FPR=0% | Table 3, Fig 6 |
| α 消融 | 甜点区 α∈[0.75,1.0]，α<0.5 水印失效 | Table 7 |
| 嵌入顺序 | cloak→watermark PSR 93.5% vs watermark→cloak 70-81.5% | Table 8 |
| 多消息容量 | 交叉串扰 FPR=0%（87 trials） | Sec 4.7 |
| InvisMark 对比 | JPEG80/50 下 TPR=0%（我们的方法 93-100%） | Table 5 |
| t-SNE 可视化 | clean→cloaked 距离 0.055，cloaked→watermarked 0.001 | Fig 7 |
| 感知质量 | 遮蔽 PSNR=37.5dB/SSIM=0.998，水印 PSNR=31.3dB/SSIM=0.994 | Fig 8 |
| 统计显著性 | SRG p=0.03，嵌入顺序 p=0.0005，FPR@θ≤0.15=0% | Sec 4.2 |

---

## 4. 关键文件索引

```
AdvFake/
├── paper/
│   ├── main.tex                    # 论文主文件（elsarticle, 403 行）
│   ├── main.pdf                    # 编译后的 PDF（需重新编译）
│   ├── FIGURE_PROMPTS_中文.md       # fig1/fig2 的 gpt-image-2 prompt
│   ├── FIGURE_GENERATION_GUIDE.md  # 配图生成指南
│   └── figures/
│       ├── fig1_teaser.png         # 占位，需生成
│       ├── fig2_framework.png      # 占位，需生成
│       ├── fig3_qualitative.png    # ✅ 定性对比
│       ├── fig4_main_results.png   # ✅ 主结果
│       ├── fig5_jpeg_robustness.png# ✅ JPEG 鲁棒
│       ├── fig6_ber_curve.png      # ✅ BER 曲线
│       ├── fig7_tsne.png           # ✅ t-SNE 可视化（新）
│       └── fig8_perceptual_quality.png # ✅ 感知质量（新）
├── code/
│   ├── 01_data_prep/build_lfw1000.py
│   ├── 02_fawkes_cloak/cloak_api.py
│   ├── 03_wam_watermark/embed_wam.py
│   ├── 04_safety_map/gen_safety_map.py
│   ├── 05_freq_constraint/e_group_joint.py
│   ├── 06_eval/
│   │   ├── eval_psr.py             # PSR 评估
│   │   ├── eval_wam_decode.py      # 水印解码评估
│   │   ├── eval_extractor2.py      # FR 提取器评估
│   │   ├── eval_tsne.py            # ✅ t-SNE（新）
│   │   ├── eval_perceptual.py      # ✅ 感知质量（新）
│   │   ├── eval_significance.py    # ✅ 统计显著性（新）
│   │   └── make_paper_figures.py   # 论文图表
├── docs/
│   ├── SUBMISSION_STEP_BY_STEP.md  # ✅ 投稿逐步操作指南（新）
│   ├── SUBMISSION_GUIDE.md         # 投稿背景信息
│   ├── SUBMISSION_PACKAGE.md       # Cover Letter/Highlights 草稿
│   ├── EXPERIMENT_COMPLETENESS_AUDIT.md # ✅ 实验完整性审计（新）
│   ├── EXPERIMENT_AUDIT.md         # 实验核查
│   ├── PROTOCOL_CORRECTION_20260817.md # 协议修正记录
│   ├── MASTER_PLAN.md              # 主计划
│   └── W4_supplementary_20260817.md # W4 补充实验记录
├── assets/
│   └── experiments/
│       ├── new_results_20260817.json  # 全部实验结果
│       ├── significance_analysis.json # ✅ 统计分析结果（新）
│       ├── perceptual_quality_stats.json # ✅ 感知质量数据（新）
│       └── tsne_stats.json           # ✅ t-SNE 统计（新）
├── baselines/
│   ├── fawkes/                     # Fawkes 代码+权重
│   ├── wam/                        # WAM 代码+权重
│   └── invismark/                  # InvisMark 基线
├── HANDOFF_续接指南.md              # 本文件
└── README.md
```

---

## 5. 环境备忘

- **conda 环境**：
  - `fawkes`: py3.8 + TF 2.4.1 + CUDA 11.2（Fawkes 遮蔽用）
  - `newpatch`: py3.8 + torch 2.4.1+cu118 + facenet_pytorch（WAM 嵌入+评估用）
- **GPU**: 2×RTX 4090
- **代理**: http://127.0.0.1:7897（git push / HF 下载需用）
- **TeX**: 当前 pdflatex 格式文件损坏（mktexlsr.pl 缺失），需修复或用其他机器编译
- **实验结果**: `assets/experiments/new_results_20260817.json`（全量 JSON）
- **后台任务**: 无

---

## 6. 下一步操作（按顺序）

### 6.1 投稿前（必须）

```
1. 修复 TeX 环境或在其他机器编译 PDF
   - 方案 A: conda install -c conda-forge texlive-core（可能需要重装）
   - 方案 B: 用其他有 TeX 的机器编译
   - 方案 C: 用 Overleaf 在线编译

2. 生成 fig1 + fig2
   - 打开 paper/FIGURE_PROMPTS_中文.md
   - 用 gpt-image-2 或手动绘制
   - 保存到 paper/figures/ 覆盖占位图

3. 重新编译 PDF
   cd paper && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex

4. 找推荐审稿人 2-3 人
   - Google Scholar 搜: "face privacy cloaking" "adversarial face protection" "neural watermarking JPEG"
   - 找近 3 年发过相关论文、不同机构、无合作的学者
   - 记下姓名、单位、机构邮箱

5. 替换致谢基金号
   - 编辑 paper/main.tex 第 346 行
```

### 6.2 投稿（1 天）

```
1. 打开 https://www.editorialmanager.com/spic/
2. Register（通讯作者邮箱注册）
3. Submit New Manuscript → Research Paper
4. 上传文件：main.pdf + Cover Letter + 图文件 + LaTeX zip
5. 填写信息：标题/摘要/关键词/Highlights/作者/审稿人/声明
6. Build PDF → 检查 → Submit
7. 详见 docs/SUBMISSION_STEP_BY_STEP.md
```

### 6.3 投稿后（2-6 个月）

```
- 等待编辑初审（1-2 周）
- 等待同行评审（2-3 个月）
- 收到修改意见后按逐条回复（Response Letter）
- 终审 → 校对 → 发表
```

---

## 7. 关键经验教训

1. **遮蔽迁移性**：Fawkes 对未知 FR 模型（arcface34/facenet）PSR≈0%，只在训练提取器（extractor_2）有效（mid 95%）。论文已诚实定位为局限。
2. **评估协议**：必须用 PSR（画廊-查询识别）；`--jpeg_quality -1` 在 PIL 中等价于 JPEG75（重大修正）。
3. **核心动机修正**：遮蔽本身不破坏水印（true-clean 99.84%→99.89% bit acc），JPEG 重压缩才是瓶颈（JPEG75 下 cloak 6%/clean 14% TPR）。
4. **WAM 微调失败**：JPEG-heavy 微调效果差；sw6 强度校准才是有效方案。
5. **ARFP 撞车处理**：已做差异化（溯源语义 vs 可逆嵌入，顺序 vs 联合，SRG + BER 协议）。
6. **SPIC 是单盲**：不是双盲，正文中可以引用自己的工作。

---

## 8. 论文统计数据

- **正文**: 403 行 main.tex
- **表格**: 9 个（JPEG 瓶颈、主结果、BER 阈值、强遮蔽、InvisMark 对比、联合优化、α 消融、嵌入顺序、冲突分解）
- **图形**: 8 个（teaser+占位、框架+占位、定性、主结果、JPEG 鲁棒、BER 曲线、t-SNE、感知质量）
- **参考文献**: 18 条
- **页数**: 约 16 页（elsarticle 12pt）
- **GitHub 提交**: dd67854 + 35819fc
