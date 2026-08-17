# 基线调研与投稿策略

> 生成时间：2026-08 | 服务项目：AdvFake（对抗人脸 + 可溯源水印）
> 注：⭐ 为 2026-08 实测（GitHub API 查询）；Fawkes 官方仓库已迁移至 Shawn-Shan/fawkes。

## 1. 目标定位

- 目标：4 个月内发表 JCR Q2 或 CCF-C 及以上
- 方向：对抗人脸 / 图像伪造取证 / 水印溯源
- 约束：实验室显卡与数据集资源有限（单卡/CPU 可跑为宜）
- 对标对象：EIAW (BDMA 2026, IF 6.1, CAS 1区) —— 已立住"对抗+水印双保护"框架，需差异化

## 2. 顶会高 star 基线清单（带官方代码）

### 2.1 攻击/隐私遮蔽侧（人脸方向，省资源）

| 基线 | 出处 | Star | 特点 | 数据 |
|---|---|---|---|---|
| **Fawkes** (Shawn-Shan/fawkes) | ICLR 2022 | **5585** ✅实测 | 黑盒整图遮蔽，FR 认不出；官方代码完善，单卡/CPU 可跑 | LFW/CelebA/FFHQ（LFW 已有） |
| **Glaze** (clashlabs/Glaze) | ICLR 2024 | ≈3.4k | 不可感知扰动防风格模仿，代码工业级（官方仓库待确认） | 自取图即可 |
| **LowKey** (nightRainy/LowKey) | ICLR 2021 | ≈900 | 同门遮蔽，社交平台场景（官方仓库待确认） | LFW/CelebA |
| **Adv-Makeup** (TencentYoutuResearch/Adv-Makeup) | IJCAI 2021 | **77** ✅实测 | 妆容式人脸攻击，腾讯官方代码 | CelebA/CASIA |
| **newpatch-rl**（本地已有） | TPAMI 2022 | — | 黑盒补丁攻击（位置+扰动联合优化） | LFW（已下载 13,233 张） |

### 2.2 水印侧

| 基线 | 出处 | Star | 特点 |
|---|---|---|---|
| **WAM** (facebookresearch/watermark-anything) | Meta 2024 | **1137** ✅实测 | 编码器-解码器，任意区域任意长度消息；AdvFake 已在用 |
| **Stable Signature** (facebookresearch/stable_signature) | ICLR 2024 | **524** ✅实测 | 生成模型潜空间水印，deepfake 溯源对口 |
| **InvisMark** (microsoft/InvisMark) | WACV 2025 | **57** ✅实测 | AI 生成图溯源水印，微软官方代码，最新 SOTA 水印基线 |
| **LampMark** (wangty1/LampMark) | ACM MM 2024 | **15** ✅实测 | 训练-free 人脸地标感知水印，**人脸水印直接对口** |
| **ROBIN** (Hannah1102/ROBIN) | ICLR 2024 | **45** ✅实测 | 扩散模型鲁棒不可见水印 |
| **StegaStamp** | CVPR 2020 | ≈1.4k | 隐写式水印，抗打印拍照 |

### 2.3 检测侧（与主动水印互补，incubator 已有）

- FIRE（CVPR 2025，扩散图检测）
- Semi-Truths（NeurIPS 2024）
- WildFake（2024）
- ICLR 2025 AI 图检测 sanity check

### 2.4 2025–2026 补充检索结论（OpenAlex/arXiv/GitHub 三路）

- **精确小方向（人脸补丁攻击+水印保持）确认无高 star 2025/2026 顶会基线** —— 机会窗口仍在；
- 最相关的新代码基线：**InvisMark（WACV 2025，微软）** 与 **LampMark（ACM MM 2024，人脸地标水印）**，可作为水印侧 SOTA 对照；
- 其它相关 2024–2025 论文（无官方码）：TOMM'24 *Invisible Adversarial Watermarking*、PoPETs'24 *StyleAdv*（对抗编辑防 FR）、arXiv 2408.01428 *Transferable Adversarial Facial Images for Privacy*、ICASSP'24 不可见人脸遮蔽泛化、CVPR'24 *WateRF*、TMM'25 *DiffW*；
- 注意：arXiv API 与 GitHub 均有反爬限流，批量检索时需限速重试。

### 2.5 关键提醒

- 精确小方向（人脸补丁攻击+水印保持）没有高 star 2025/2026 顶会基线 —— 这是机会也是风险：创新点须靠"积木组合 + 安全区域图机制"立住，不能靠"没人做过"；
- Fawkes 官方仓库在 github.com/Shawn-Shan/fawkes（5585★，从 Secure-AI-Systems 迁移）；LowKey/Glaze 官方仓库未在检索中定位（可能已归档），需从论文主页确认；
- WAM checkpoint 与微调后的解码器**不在压缩包里**（只被日志引用，路径 /workspace/zsy/Watermark_anything/checkpoints/checkpoint.pth），实验前需从 facebookresearch/watermark-anything 官方仓库重新获取。

## 3. 创新定位建议（差异化 vs EIAW）

| 维度 | EIAW | 我们的建议定位 |
|---|---|---|
| 任务 | 图像分类 + 整图扰动 | 人脸识别 + 隐私遮蔽（Fawkes 系）/ 补丁攻击 |
| 水印 | 自研频域模运算 | WAM 神经网络水印（任意消息） |
| 核心机制 | 频域掩码（中低频） | **空间安全区域图 S=(1−P)(1−R) + 频域掩码联合约束** |
| 指标 | ASR + EAR | 身份一致性（exact/drift/revert）+ 水印 TPR + 噪声鲁棒 + 不可感知 |

叙事建议：**"隐私遮蔽人脸的可验证溯源"** —— AI 认不出你（事前防护）+ 能验明"这是你发的图"（事后问责）。该叙事在文献中是空白（Fawkes 只有扰动、无凭证；水印文献只做干净图/生成图）。

## 4. 投稿策略

### 4.1 首选期刊（JCR Q2 / CCF-C，4 个月窗口）

| 期刊 | CCF / JCR | 审稿预估 | 备注 |
|---|---|---|---|
| **Signal Processing: Image Communication** | CCF-C / Q2 | 1–3 月 | 用户已锁定，图像处理对口 |
| **J. Visual Communication & Image Representation** | CCF-C / Q2 | 1–3 月 | 图像+安全对口 |
| **J. Information Security & Applications** | CCF-C / Q1–Q2 | 1–2 月 | **AdvEWM 同刊**（对抗+水印直接对口） |
| **The Visual Computer** | CCF-C / Q2 | 2–4 月 | Springer |
| **Pattern Recognition Letters** | CCF-C / Q2 | 1–2 月 | 短文友好 |
| **Multimedia Tools & Applications** | CCF-C / Q2 | 2–4 月 | 快但 APC 高（~$2300） |
| 🎁 **BDMA**（EIAW 同刊） | Q1 / CAS 1区 | ~8 周 | OA 免费，与 EIAW 同刊对打最有说服力（超出 Q2 下限，实验扎实可冲） |

### 4.2 会议备选（CCF-C，赶 deadline）

- ICIP（通常 9–10 月截稿）
- ICPR（CCF-C）
- ACCV（CCF-C）

### 4.3 时间表（14 周）

| 周 | 任务 |
|---|---|
| W1 | 定义痛点（如：WAM 在 JPEG 下 TPR 0.7%；Fawkes 图无溯源凭证），novelty 检索定稿 |
| W2 | 搭环境：Fawkes + WAM + LFW 子集（单卡/CPU 可跑） |
| W3–8 | 改 1–2 个模块，闭环实验（安全区域图 + 频域掩码），跑对照表 |
| W9–10 | 写作（先写 camera-ready 版） |
| W11–14 | 投稿 + 返修窗口 |

## 5. 风险清单

1. 创新被判增量 → 必须用"安全图让顺序方法不输联合优化（EIAW Table 9 的反驳实验）"来对冲
2. 数据集调整被质疑 → 绑定真实场景（社交媒体重压缩、JPEG、跨姿态）
3. WAM checkpoint 缺失 → 第一周就从官方仓库重新下载
4. GitHub 限流 → 克隆仓库时如遇 404/429，稍后重试或换网络
