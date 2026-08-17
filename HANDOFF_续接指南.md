# AdvFake 项目续接指南（HANDOFF）

> 生成：2026-08-16 | 用途：重启/新 pi agent 快速进入状态
> 项目根：`/media/oyp/数据/Projects/042_image_forensic/AdvFake/`

## 1. 项目在做什么（30 秒版）

学生论文项目：**给"对抗人脸"嵌入可溯源水印**——让人脸识别继续被骗（对抗身份保持），同时水印可解码（溯源/版权），且不可感知。
已核查的学术定位：**"对抗+水印双保护"框架已被 EIAW (BDMA 2026) 等发表**，我们的差异化方向 = **"Fawkes 式整图遮蔽 + 频域约束 + 溯源水印"**（避开学生已做的补丁攻击+空间安全图路线）。

## 2. 已完成工作清单

### 2.1 解压与数据（完成 ✅）
- `newpatch.tar` → `AdvFake/newpatch/`（281,834 文件，4.1G）
- `res_else.zip` → `AdvFake/res/`（2.4G，后台续传完成）
- ⚠️ 少量文件名含 `*` 的图片无法在 Linux 创建（Windows 遗留名，不影响代码）
- ⚠️ 所有脚本硬编码 `/workspace/zsy/...` 路径（原服务器），本机运行需改路径或软链

### 2.2 学生项目剖析（完成 ✅，结论见 EIAW_解读.md 第 4 节）
- 流水线：RL 黑盒补丁攻击（newpatch-rl, TPAMI'22）→ AISM 精修 → 空间安全区域图 S=(1−P)(1−R) → WAM 水印嵌入 → 噪声鲁棒评估
- 主实验数字：facenet 定向攻击 1000 样本 95.6% 成功率；水印后 clean 身份保持 93.8%（exact 77.8%）；水印 TPR clean 100%
- **关键漏洞**：①评估集是"最容易"子集（top2 间隔中位数 0.0098 vs 随机 0.22）；②黑盒但画廊已知；③安全图未用于主实验；④JPEG≤80 击穿水印；⑤无任何 SOTA 对比

### 2.3 文献调研（完成 ✅）
- EIAW 原文已下载解读（见下）；EIAW 期刊 = BDMA（IF 6.1，中科院 1 区，OA 免费，审稿 ~8 周）
- 三路检索（OpenAlex/arXiv/GitHub）确认：**该小方向无高 star 2025/2026 顶会基线**
- 高 star 基线实测：Fawkes 5585★、WAM 1137★、Stable Signature 524★、InvisMark 57★（WACV'25）、LampMark 15★、ROBIN 45★、Adv-Makeup 77★

### 2.4 Fawkes 最小样例（完成 ✅）
- 仓库：`baselines/fawkes/`（Shawn-Shan/fawkes，USENIX Security 2020）
- 环境：conda env `fawkes`（Python 3.8 + TF 2.4.1 + keras 2.4.3 + mtcnn）
- 权重：extractor_2.h5（161MB，自动从 mirror.cs.uchicago.edu 下载到 ~/.keras/models/）
- 运行：`conda activate fawkes && cd baselines/fawkes && python3 -m fawkes.protection -d <图片目录> -m low --format jpg --gpu 0`
- 验证：3 张 LFW 图，~14s/张（CPU），PSNR 38.6–41.8dB，SSIM 0.9987–0.9995
- 样例输出：`demo/fawkes_mini_example/`（原图 + *_cloaked.jpeg）

## 3. 关键文件索引

```
AdvFake/
├── newpatch/                      ← 学生代码+数据（LFW 13233张、模型权重）
├── res/                           ← 学生实验结果（zip 解压）
├── baselines/fawkes/              ← Fawkes 官方代码（已跑通）
├── demo/fawkes_mini_example/      ← Fawkes 最小样例输出
└── related_work/
    ├── EIAW_2026_Image_Copyright_Dual-Protection.pdf   ← EIAW 原文（CC-BY OA）
    ├── EIAW_2026_pdf_text.txt                          ← 全文文本（含9张表格）
    ├── EIAW_2026_ieee_page_fulltext.md                 ← IEEE 全文备份
    ├── EIAW_解读.md                                    ← EIAW 通俗解读+与学生对标
    ├── baseline_and_venue_plan.md                      ← 基线清单+投稿策略（JCR Q2/CCF-C）
    ├── experiment_plan_Fawkes_WAM.md                   ← 最小实验方案（4周闭环）
    └── novelty_report_relatedwork.md                   ← Novelty 报告+Related Work 初稿
```

## 4. 核心结论速查（引用时避免重复劳动）

| 问题 | 结论 |
|---|---|
| 学生论文有 SOTA 对比吗 | ❌ 无，只有内部消融 |
| 创新性真实吗 | 组合型创新，非开创型；安全区域图机制+身份一致性评估是亮点，但主实验没用安全图 |
| EIAW 是威胁吗 | 是，必须引用并区分（频域联合优化 vs 空间补丁+独立水印） |
| 推荐方向 | Fawkes 遮蔽 + 频域约束 + 溯源水印（避开学生已有路线） |
| 目标期刊 | JISA / SPIC / JVCIR（JCR Q2/CCF-C）；扎实可冲 BDMA 与 EIAW 同刊对打 |
| 投稿时间表 | 4 个月：W1 痛点+novelty → W2 环境 → W3-8 实验 → W9-10 写作 → W11-14 投稿 |

## 5. 下一步待办（新 agent 从这开始）

1. **（高优先级）校对 related work 参考文献 DOI**：novelty_report 第 5 节部分 DOI 是按记忆填的，需逐条用 Crossref/OpenAlex 核对
2. 安装 `facenet_pytorch` 到 fawkes 或 torch2.9 环境，验证 Fawkes 遮蔽的 FR 逃避效果（原服务器有，本机无）
3. 从 facebookresearch/watermark-anything 重新下载 WAM checkpoint（**学生压缩包里没有**，只被日志引用）
4. 按 `experiment_plan_Fawkes_WAM.md` 跑 A/B/C/D 四组对照（Fawkes→WAM→安全区/频域）
5. 补 EIAW Table 9 的反驳实验：顺序嵌入（遮蔽+水印）vs 联合优化

## 6. 环境备忘

- 本机 miniconda envs：`fawkes`（TF2.4.1, 已装好）、`torch2.9`、`torch2.4`、`apjf`、`aitalk` 等
- GitHub API / arXiv API 对本机 IP 有反爬限流（429/404），批量检索需限速重试
- browser-act 的 stealth-extract 可绕过 IEEE 等反爬（本机已配置）
- 学生原服务器路径：`/workspace/zsy/`（模型、WAM checkpoint、微调数据都在那，压缩包未含）
