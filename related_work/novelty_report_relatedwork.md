# Novelty 检索报告 + Related Work 初稿

> 生成：2026-08 | 检索范围：OpenAlex / arXiv / Semantic Scholar / GitHub / IEEE Xplore（含 2026 年最新文献）
> 约束：尽量避开学生已在做的（补丁攻击 + WAM + 空间安全区域图 + 身份一致性评估）

## 1. 检索概况

- 检索词：adversarial watermark / watermark adversarial example / adversarial patch + watermark / face recognition + privacy + watermark / robust watermarking / Fawkes cloaking 等 8 组
- 引文追踪：Adv-watermark (ACM MM 2020) 的 25 篇后续引用已全部人工核阅
- 关键发现：**"对抗+水印双保护"框架已发表（EIAW 等），但"人脸遮蔽（cloaking）+ 神经网络水印 + 频域约束"的具体组合未检索到同构工作**

## 2. 已占用的位置（写论文时必须引用的"山"）

| 定位 | 代表文献 | 引用要点 |
|---|---|---|
| 对抗样本 + 水印（框架） | **EIAW**, BDMA 2026, DOI: 10.26599/bdma.2025.9020070 | 频域模运算水印+攻击联合优化；图像分类 |
| 对抗样本 + 水印（框架） | **Adv-watermark**, ACM MM 2020 | 可见水印作扰动；BHE 优化 |
| 对抗样本 + 水印（后续） | **AdvEWM** (JISA 2023)、**BHI** (Inf. Sci. 2023)、**ISWP** (Appl. Intell. 2024)、**EIAW 同系** | 数字水印/改进优化作为扰动 |
| 生成图版权 + 对抗 | **Watermark-embedded Adv. Examples** (CVPR 2024) | 带个人水印对抗样本攻击扩散模型 |
| 人脸隐私遮蔽 | **Fawkes** (USENIX Sec 2020)、**LowKey** (ICLR 2021)、**Glaze** (ICLR 2024) | 整图不可感知扰动让 FR/风格模型失效，**无溯源凭证** |
| 人脸水印 | **FaceSigns** (TOMM 2024)、**SepMark** (ACM MM 2023)、**LampMark** (ACM MM 2024) | 人脸半脆弱水印/地标水印，**无对抗成分** |
| 通用水印模型 | **WAM** (Meta 2024)、**Stable Signature** (ICLR 2024)、**InvisMark** (WACV 2025) | 神经网络水印 SOTA |
| 反向工作（需区分） | **CMUA-Watermark** (AAAI 2022) | 水印作为攻击去破坏 deepfake 生成器 |

## 3. 空白位置（创新窗口，按把握排序）

1. **"遮蔽人脸 + 可解码溯源水印"组合**：Fawkes 系只扰动、无凭证；水印文献只做干净图/生成图 —— 未见两者结合（学生也未做，因其走补丁路线）
2. **频域约束用于遮蔽场景**：EIAW 在整图扰动（PGD）上用频域掩码；Fawkes 也是整图扰动但**完全在像素域** —— 把频域掩码思想嫁接到 Fawkes 遮蔽上，是文献空白
3. **JPEG 鲁棒的对抗水印**：WAM/InvisMark 在 JPEG 下均明显掉点（学生实测 WAM jpeg50 TPR≈0.7%）—— 频域约束正是应对手段
4. **身份一致性作为"水印后对抗保持"的评估协议**：现有工作只报 ASR/EAR，无人报 exact/drift/revert 身份级指标（学生已有此框架，属加分项，不算新点）

## 4. Related Work 初稿（可直接入论文）

### 4.1 对抗样本与隐私遮蔽 (Adversarial Examples and Privacy Cloaking)

Adversarial examples mislead deep models by adding imperceptible perturbations [Szegedy et al. 2014; Madry et al. 2018]. In face recognition, adversarial perturbations have been exploited for **privacy cloaking**: Fawkes [Shan et al., USENIX Sec. 2020] optimizes a feature-space "cloak" so that unauthorized face recognition models misidentify the subject, while the perturbation remains imperceptible (SSIM≈0.99). LowKey [Zhou et al., ICLR 2021] targets social-media pipelines, and Glaze [Shan et al., ICLR 2024] extends the idea to style mimicry. Physical patch attacks (e.g., AdvHat [Komkov & Petiushko, ICPR 2021], Adv-Makeup [Zhu et al., IJCAI 2021]) instead restrict perturbations to a localized patch. **However, all these works only destroy recognition; none embeds any extractable ownership/provenance signal into the protected image.**

### 4.2 数字水印与溯源 (Digital Watermarking and Provenance)

Invisible watermarking embeds messages robust to distortions [Zhu et al. HiDDeN 2018; Zhang et al. StegaStamp 2020; Fernandez et al. Stable Signature, ICLR 2024; WAM, 2024; InvisMark, WACV 2025]. For face imagery, FaceSigns [TOMM 2024] and LampMark [ACM MM 2024] embed semi-fragile or landmark-aware watermarks for authentication. **Yet these methods are designed for clean images and do not consider that the watermarked image must simultaneously preserve an adversarial/cloaking property.**

### 4.3 对抗水印与双重保护 (Adversarial Watermarking and Dual Protection)

Recent works combine both goals: Adv-watermark [Luo et al., ACM MM 2020] treats a visible watermark as the adversarial perturbation; EIAW [Liu et al., BDMA 2026] embeds a blind, extractable watermark in the DCT domain and jointly optimizes it to attack classifiers, achieving ASR≈99.5% with EAR≈92%. CMUA-Watermark [AAAI 2022] instead uses adversarial watermarks to *attack* deepfake generators. **These methods operate on generic image classification with whole-image perturbations; none targets face recognition identity protection, and none studies whether an existing privacy cloak can be made provenance-verifiable while retaining its cloaking efficacy.**

### 4.4 定位声明 (Positioning)

To the best of our knowledge, we are the first to study **provenance-verifiable privacy cloaking for face images**: embedding a decodable neural watermark into Fawkes-style cloaked faces such that (i) face recognition evasion is preserved (identity-consistency preserved), (ii) the watermark remains detectable/decodable, and (iii) robustness to common distortions (esp. JPEG) is achieved via frequency-domain constraints.

## 5. 参考文献清单（带 DOI/arXiv）

1. Liu et al., "Image Copyright Dual-Protection Based on Extractable and Imperceptible Adversarial Watermark", Big Data Mining and Analytics 9(3):719–734, 2026. doi:10.26599/bdma.2025.9020070 ✅
2. Luo et al., Adv-watermark, ACM MM 2020. doi:10.1145/3394171.3413976
3. Jiang et al., AdvEWM, J. Inf. Security & Applications, 2023. doi:10.1016/j.jisa.2023.103662
4. Wang et al., BHI, Information Sciences, 2023. doi:10.1016/j.ins.2023.119037
5. Zhu et al., "Watermark-embedded Adversarial Examples for Copyright Protection against Diffusion Models", CVPR 2024. doi:10.1109/cvpr52733.2024.02305 ✅
6. Shan et al., Fawkes, USENIX Security 2020 (arXiv:2002.08927)
7. Zhou et al., LowKey, ICLR 2021 (arXiv:2109.11598)
8. Shan et al., Glaze, ICLR 2024 (arXiv:2302.04222)
9. Zhu et al., Adv-Makeup, IJCAI 2021. doi:10.24963/ijcai.2021/173
10. Komkov & Petiushko, AdvHat, ICPR 2021. doi:10.1109/icpr48806.2021.9412236
11. Ruiz et al., WAM (Watermark Anything), arXiv:2410.20820, 2024. Code: facebookresearch/watermark-anything
12. Fernandez et al., Stable Signature, ICLR 2024. Code: facebookresearch/stable_signature
13. Chen et al., InvisMark, WACV 2025. Code: microsoft/InvisMark
14. Wang et al., LampMark, ACM MM 2024. doi:10.1145/3664647.3680869
15. Jia et al., FaceSigns, ACM TOMM 2024. doi:10.1145/3640466
16. Zhu et al., CMUA-Watermark, AAAI 2022. doi:10.1609/aaai.v36i1.19982
17. Zhang et al., SepMark, ACM MM 2023. doi:10.1145/3581783.3612471

## 6. 给写作的落地建议

- Related Work 4.1–4.3 三节各留 2–3 句"批判性缺口句"（已写好），正文直接在此基础上扩展
- 定位声明（4.4）就是 Introduction 里 novelty claim 的骨架，投 JISA/SPIC 时按模板扩成一段
- 所有基线表（Fawkes/WAM/InvisMark/Adv-Makeup 等）的代码位置见 `baseline_and_venue_plan.md`
