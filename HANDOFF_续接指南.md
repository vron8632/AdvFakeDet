# AdvFakeDet 项目续接指南（HANDOFF v2）

> 生成：2026-08-17 09:30 | 用途：重启/新 pi agent 快速进入状态
> 项目根：`/home/jiujiu/Projects/AdvFake/` | GitHub: `vron8632/AdvFakeDet` (main)

## 1. 项目在做什么（30 秒版）

**论文项目**：给 Fawkes 遮蔽人脸嵌入可溯源神经网络水印（WAM），让人脸识别继续被骗（遮蔽保持）+ 水印可解码（溯源）+ JPEG 鲁棒。
**目标期刊**：JCR Q2 非 OA（SPIC / JVCIR / JISA，Elsevier）
**核心定位**：Provenance-Verifiable Privacy Cloaking —— 顺序嵌入 + 安全区域图（SRG）+ 强度校准 + BER 检测。

## 2. 已完成清单

### 2.1 环境（miniconda，全 GPU 就绪）
- `fawkes` 环境：py3.8 + TF 2.4.1 + CUDA 11.2（修复 libcusolver symlink）—— Fawkes 遮蔽
- `newpatch` 环境：py3.8 + torch 2.4.1+cu118 + facenet_pytorch + WAM 依赖（修复 py3.8 注解兼容）
- 代理：Clash Verge @ 127.0.0.1:7897（GitHub/HF 下载、tectonic 编译需走代理）
- Gemini key（AQ. 开头）**不可用于 API**（401 blocked）；DeepSeek API key 可用（bashrc 里 DEEPSEEK_API_KEY）

### 2.2 数据与权重（assets/ 已 gitignore）
- LFW 1000 随机子集（771 身份）: `assets/dataset/lfw1000/`
- WAM checkpoint 289MB: `baselines/wam/checkpoints/checkpoint.pth` + params.json
- Fawkes extractor_0/2: `baselines/fawkes/fawkes/model/`（md5 已校验）
- 微调 checkpoint: `assets/experiments/wam_jpeg_ft*/`、`wam_cloak_ft/`（效果不佳，供参考）

### 2.3 关键实验（全部跑完）
**low 遮蔽 1000 张（β=6）**：
| 组 | PSR | WM clean/JPEG80/JPEG50 | PSNR/SSIM/LPIPS |
|---|---|---|---|
| A cloak | 47.4% | — | ~40/0.98/0.01 |
| B 全局 | 36.1% | 99.2/99.6/93.7% | 29.0/0.851/0.140 |
| C 安全图 | 42.1% | 98.6/99.0/92.7% | 30.1/0.879/0.111 |
FPR=0%（500 次）

**mid 遮蔽 200 张（β=6）**：
| 组 | PSR | WM clean/JPEG80/JPEG50 | sim |
|---|---|---|---|
| A | 95.0% | — | 0.054 |
| B | 94.0% | 100/100/93.5% | 0.114 |
| C | 93.5% | 99.5/100/95.0% | 0.083 |

**E 组（联合优化对比）**：顺序嵌入（C）≈ 联合优化（PSR 85% + 水印 100%），回应 EIAW Table 9。

**遮蔽-水印冲突（核心发现）**：clean 99.8%（TPR@95% 98%）→ cloak 85.2%（6%）。

### 2.4 论文（已完成初稿，编译成功）
- `paper/main.tex` + `main.pdf`（10 页，elsarticle 模板，5 图 4 表）
- 故事线：背景→冲突（遮蔽破水印/水印破遮蔽/ARFP 撞车）→方法（SRG+强度校准+BER）→结果（共存）
- 图：fig3 定性、fig4 主结果、fig5 JPEG 鲁棒（matplotlib 已画）；fig1 teaser + fig2 框架为 16:9 占位
- 中文 prompt：`paper/FIGURE_PROMPTS_中文.md`（用户用 gpt-image-2 生成后覆盖占位图）

### 2.5 GitHub 已提交
- `vron8632/AdvFakeDet` main 分支（46dd58a, 44a67f0 两次提交）
- code/（27 脚本）、paper/、docs/、related_work/、README
- .gitignore 排除权重/数据/学生代码

## 3. 关键文件索引

```
AdvFake/
├── code/
│   ├── 01_data_prep/build_lfw1000.py    # 1000 子集
│   ├── 02_fawkes_cloak/cloak_api.py     # 自定义强度遮蔽（Python API）
│   ├── 03_wam_watermark/embed_wam.py    # WAM 嵌入（global/safety_map + scaling_w）
│   ├── 04_safety_map/gen_safety_map.py  # FR 敏感度安全图
│   ├── 05_freq_constraint/e_group_joint.py  # E 组联合优化
│   ├── 06_eval/eval_psr.py              # PSR 标准评估（extractor2/facenet）
│   ├── 06_eval/eval_wam_decode.py       # 水印 BER 解码评估
│   └── 06_eval/make_paper_figures.py    # 论文图表
├── paper/main.tex + main.pdf            # 论文（elsarticle）
├── paper/FIGURE_PROMPTS_中文.md          # 配图 prompt
├── docs/
│   ├── MASTER_PLAN.md                   # 主计划
│   ├── EXPERIMENT_AUDIT.md              # 实验核查（重要发现）
│   ├── NOVELTY_AUDIT_v2.md              # 新颖性（ARFP 撞车分析）
│   └── W1/W2/W23_*.md                   # 实施记录
└── related_work/                        # EIAW、ARFP 全文 + 解读
```

## 4. 关键经验教训（避免重复劳动）

1. **遮蔽迁移性**：Fawkes 对所有未知 FR 模型（arcface34/facenet）PSR≈0%，只在训练提取器（extractor_2）有效（mid 95%）。论文已诚实定位（遮蔽有效性入局限）。
2. **评估协议**：必须用 PSR（画廊-查询识别）；arcface 需学生流程（landmark 对齐+无归一化）；sim 阈值（0.4）在 extractor_2 上不可靠（区分度差）。
3. **WAM 微调失败**：JPEG-heavy 微调（8/30 epochs）未改善（权重加载 bug 已修，但微调本身效果差）；sw6 强度校准才是有效方案。
4. **推理时频域滤波无效**（WAM 依赖高频）；BER 检测协议是 JPEG 鲁棒的关键。
5. **ARFP（arXiv:2605.01217）撞车**：已做遮蔽+可验证信息（可逆路线）→ 我们差异化：溯源语义 + 顺序嵌入 + SRG + BER 协议。

## 5. 下一步待办（新 agent 从这开始）

1. **（高优先级）用户生成 teaser/框架图**：按 FIGURE_PROMPTS_中文.md 用 gpt-image-2，替换 fig1/fig2 占位后重编译（fig6 已就绪）
2. **补作者信息**：main.tex 的 author/affiliation/acknowledgment 是 TBD；docs/SUBMISSION_PACKAGE.md 已备好 cover letter/highlights/author contributions 草稿
3. **可选补实验**：Stable Signature 对比（需 SD 解码器+per-key extractor 训练，论文已论证性排除）；遮蔽迁移性多模型报告（现仅 arcface34/facenet）
4. **投稿准备**：填作者后生成最终 PDF + cover letter 定稿
5. 引用 DOI 核对已完成（related_work/doi_verify_report.md 12 条）

## 5.5 2026-08-17 下午新增（W4 补实验，全部完成）
- **⚠️ 重大协议修正**（docs/PROTOCOL_CORRECTION_20260817.md）：`--jpeg_quality -1` 在 PIL 中等价于 JPEG75！原论文所有 "clean" 列（99.2/98.6 等）实际是 JPEG75；核心动机从 "遮蔽破坏水印（98→6%)" 修正为 "遮蔽本身不破坏（true-clean 99.84→99.89），JPEG 重压缩才是瓶颈（JPEG75 下 cloak 6%/clean 14%）"
- **InvisMark SOTA 基线对比**（WACV 2025 官方 ckpt）：遮蔽图 clean 解码 100% TPR，但 JPEG80/50 下 TPR=0%（干净图也一样，连 JPEG95 都失效）→ 论文 Table 5 + Sec. 4.8
- **BER 阈值敏感性曲线**（JPEG75 部署条件、协议匹配）：θ=0.25 时 TPR 99.2/98.6/100%，FPR 0.2–0.6%；θ≤0.15 时 FPR=0% → Fig 6 + Table 3
- **α 消融**（SRG 强度）：甜点区 α∈[0.75,1.0]（PSR 93.5%）；α<0.5 水印失效 → Table 7
- **嵌入顺序实验**：先嵌水印再遮蔽 PSR 掉到 70–81.5%，先遮蔽再嵌水印保持 93.5% → Table 8（回击审稿人顺序质疑）
- **多消息容量**：交叉串扰 FPR=0%（87 trials）
- 论文更新至 16 页（5 图 8 表 + conflict 分解表），编译通过；诚实数据汇总: assets/experiments/honest_core_facts.json；记录 docs/W4_supplementary_20260817.md

## 6. 环境备忘（重启后验证）
- GPU：2×RTX 4090（学生遗留进程 targeted_attack_selected_fixed.py 占 ~2GB/卡，勿杀）
- conda：fawkes（TF）、newpatch（torch）两个环境
- 代理：http://127.0.0.1:7897（git push / tectonic / HF 下载需用）
- 后台任务：无（全部完成）
- 学生数据路径：/home/jiujiu/workspace/zsy/（原始压缩包）
