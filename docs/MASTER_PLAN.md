# AdvFake 期刊论文项目 · 主计划 (MASTER PLAN)

> 版本: v1.0 | 日期: 2026-08-16 | 目标: JCR Q2 非OA SCI 期刊论文
> 项目根: /home/jiujiu/Projects/AdvFake/

---

## 0. 目标与约束

- **论文目标**: 一篇 JCR Q2 非OA SCI 期刊论文（候选：Signal Processing: Image Communication / JVCIR / JISA / Neurocomputing 按工作量选）
- **时间**: 4 个月闭环（W1 启动 → W3-10 实验 → W11-13 写作 → W14 投稿）
- **硬约束**:
  - 不和学生现有工作重合（学生=补丁攻击 newpatch-rl + AISM 精修 + 空间安全图 + WAM，评估=身份一致性）
  - 我们 = **Fawkes 式整图遮蔽 + 频域约束 + 溯源水印**，且主实验必须用安全区域图（学生没用）
  - 代码放 `code/`，论文放 `paper/`，图表占位放 `paper/figures/`（16:9 占位由用户用 gpt-image-2 生成）
  - 环境用 miniconda，权重/数据/baseline 下载到本地
  - 每步记录实施文档到 `docs/`

## 1. 研究定位（一句话）

**Provenance-Verifiable Privacy Cloaking**: 给 Fawkes 式遮蔽人脸嵌入可解码溯源水印，让 FR 继续被骗（身份保持）+ 水印可解码（溯源）+ JPEG 鲁棒（频域约束）。

### 与已有工作差异（写作卖点）
| 维度 | 学生论文 | EIAW (BDMA 2026) | **我们** |
|---|---|---|---|
| 攻击形式 | 空间补丁（局部） | 整图 PGD 扰动 | **整图遮蔽（Fawkes 式）** |
| 水印 | WAM 独立嵌入 | 频域模运算 + 联合优化 | **WAM + 安全区域图 + 频域掩码** |
| 评估 | 身份一致性 | ASR/EAR | **身份一致性 + 水印 TPR + 质量 + 鲁棒** |
| 关键卖点 | 补丁+安全图 | 分类器联合优化 | **遮蔽可溯源 + JPEG 鲁棒 + 顺序嵌入不输联合优化** |

### 创新点（3 个，写成 2 个 main + 1 个评估贡献）
1. **C1 (机制)**: 安全区域图引导的 WAM 嵌入 —— 只在水印对 FR 影响最小的区域嵌入，遮蔽性保持率显著高于全局嵌入
2. **C2 (鲁棒)**: 频域中低频掩码约束 —— 针对 WAM 在 JPEG 下失效的已知短板，把水印能量压到 JPEG 保留的中低频，JPEG80/50 TPR 大幅提升
3. **C3 (评估)**: 身份级保持协议（exact/drift/revert/not_detected）用于水印后对抗保持评估（学生框架的复用+扩展，加分项）

## 2. 实验矩阵（四组对照 + 消融）

| 组 | 处理 | 回答的问题 |
|---|---|---|
| A | Fawkes 遮蔽（无印） | 基线：遮蔽有效性与质量上界 |
| B | Fawkes + WAM 全局嵌入 | 朴素方案：水印破坏遮蔽性 |
| C | Fawkes + WAM 安全区域图嵌入 | C1：安全图机制保住遮蔽性 |
| D | C + 频域中低频掩码 | C2：JPEG 鲁棒 |
| E | EIAW 风格联合优化（复现简化版） | 顺序 vs 联合（回应 EIAW Table 9） |

### 评估协议（每张遮蔽水印图）
1. **遮蔽保持**: FR 代理（arcface34/50）识别遮蔽图 → exact_adv_consistent / drift / revert / not_detected；核心指标 = revert 率↓、exact+drift 保持率
2. **水印**: TPR@像素级阈值、32-bit 位精度、负样本 FPR
3. **质量**: PSNR / SSIM / LPIPS (C vs A 或原图 vs C)
4. **鲁棒**: JPEG(50/80/95)、裁剪、缩放、亮度、旋转、高斯模糊（几何+值度量 14 种，复用学生噪声协议）

### 数据
- LFW 13233 张 / 5749 身份（已在 newpatch/lfw/），取干净可识别 1000 样本（避开学生用过的 top2 easy 子集，随机公平抽样）
- 补充数据集（可选）: CelebA-HQ 或 FFHQ 小批（若需跨域泛化表）

## 3. 技术管线

```
LFW 干净人脸 A
  → [02_fawkes_cloak] Fawkes 遮蔽（TF 特征提取器，或 torch 复刻）→ 遮蔽图 B
  → [04_safety_map] 安全区域图 R（arcface34 代理梯度定位 FR 敏感区；S=1−R）
  → [03_wam_watermark] WAM 嵌入：C = B + α·S·(wm(B) − B)
  → [05_freq_constraint] D 组：再叠加频域中低频掩码 M
  → [06_eval] 身份保持 + 水印解码 + 质量 + 鲁棒
```

## 4. 环境与依赖（miniconda）

| 环境 | 用途 | 状态 |
|---|---|---|
| `newpatch` | 主实验（torch 2.4.1+cu118, facenet-pytorch 2.5.2, lpips）| ✅ 已有，补 WAM 依赖 |
| `fawkes` | Fawkes 官方代码（TF 2.4.1, keras 2.4.3, mtcnn）| ❌ 需创建 |
| `paper`（可选）| 图表绘制（matplotlib/seaborn 等）| 复用 newpatch 即可 |

### 需下载的资产
| 资产 | 来源 | 落位 |
|---|---|---|
| WAM checkpoint + params.json | facebookresearch/watermark-anything (HuggingFace) | `assets/weights/wam/` |
| Fawkes extractor_2.h5 | 已在 baselines/fawkes/fawkes/model/ ✅ | — |
| arcface34/50, cosface50 权重 | 已在 newpatch/rlpatch/stmodels_* ✅ | — |
| facenet InceptionResnetV1 | 运行时自动下载 | ~/.cache/torch/ |
| 对比 baseline 论文 PDF | related_work/ + 补充下载 | related_work/ |

## 5. 里程碑（含实施文档）

| 周 | 里程碑 | 实施文档 |
|---|---|---|
| W1 | skills 加载 + 环境就绪 + WAM/Fawkes 跑通 + 数据子集构建 | docs/W1_*.md |
| W2 | A/B 两组：拿到"朴素嵌入破坏遮蔽性"基线数字 | docs/W2_*.md |
| W3 | C 组安全区域图 + 1000 样本 | docs/W3_*.md |
| W4 | D 组频域掩码 + JPEG/噪声鲁棒 | docs/W4_*.md |
| W5 | E 组 EIAW 风格联合优化简化复现 + 消融(α, 掩码比例) | docs/W5_*.md |
| W6-8 | 补实验（跨域、失败case、统计显著性）+ 结果整理 | docs/W6-8_*.md |
| W9-11 | 写作（intro/related/method/exp）+ 图表 | paper/ |
| W12-13 | 校对、润色、格式（期刊模板）、DOI 核对 | docs/W12-13_*.md |
| W14 | 投稿（cover letter + rebuttal 预演）| docs/W14_*.md |

## 6. 风险与兜底
- **WAM JPEG 救不回来** → JPEG-aware 微调训练（JPEG 作增强），C2 升级版
- **Fawkes TF 环境装不上（py3.8+TF2.4 冲突）** → torch 复刻 Fawkes 遮蔽（extractor 权重转 torch 或用 arcface34 代理）
- **Fawkes 遮蔽率低** → 调强度参数（low/medium/high）或换 LowKey
- **1000 样本太慢** → 先 200 样本跑通，再扩量
- **审稿质疑 novelty** → 强化 E 组对比 + 跨数据集泛化表

## 7. 目录约定
```
AdvFake/
├── code/          # 全部实验代码（分模块 01-06 + common）
├── paper/         # 论文 tex + figures/
├── assets/        # 权重、数据子集、中间产物
├── docs/          # 计划与实施文档（本文件 + W*_*.md）
├── _skills/       # 克隆的 skills 仓库（方法论参考）
├── related_work/  # 文献与解读
├── baselines/     # 官方 baseline 代码
├── newpatch/ res/ # 学生数据（只读参考，不修改）
```

## 8. 待办队列（本文档维护）
- [x] 克隆 skills 仓库（3 个，zip 下载中）
- [x] 建立目录骨架 + 本计划
- [ ] newpatch 环境补装 WAM 依赖（timm/einops/omegaconf/pycocotools）
- [ ] 创建 fawkes conda 环境（TF 2.4.1）
- [ ] 下载 WAM checkpoint（HuggingFace）
- [ ] 跑通 Fawkes 遮蔽最小样例（本机 GPU）
- [ ] 跑通 WAM 嵌入+解码最小样例
- [ ] 构建 1000 干净样本子集（随机公平，避开学生 top2-easy）
- [ ] A/B/C/D/E 实验
- [ ] 图表生成（占位 16:9 已建，其余用 skills）
- [ ] 论文写作
