> ⚠️ 本文为早期叙事稿（历史快照）。最新、已协议修正的版本以 `paper/main.tex` 为准（JPEG75 协议修正见 docs/PROTOCOL_CORRECTION_20260817.md）。

# Provenance-Verifiable Privacy Cloaking for Face Images: Safety-Region-Guided Neural Watermarking with JPEG-Robust Decoding

> 初稿 v0.1 | 2026-08-17 | 目标: JCR Q2 期刊 (Signal Processing: Image Communication / JVCIR / JISA)

---

## Abstract

Privacy-cloaking techniques such as Fawkes protect face images from unauthorized face recognition (FR) by adding imperceptible perturbations. However, cloaked images carry no verifiable provenance: anyone can republish a victim's cloaked image without accountability. In this paper, we study *provenance-verifiable privacy cloaking* — embedding a decodable neural watermark into cloaked faces such that (i) FR evasion is preserved, (ii) the watermark remains detectable, and (iii) detection is robust to common distortions, especially JPEG compression. We first reveal a fundamental conflict: Fawkes-style cloaking perturbations reduce WAM watermark decoding accuracy from 98% to 6% (TPR@95%), confirming that adversarial cloaking and neural watermarking interfere. We then propose two complementary mechanisms: (1) a **safety-region guidance** that embeds watermarks preferentially in FR-insensitive facial regions (computed from FR surrogate gradients), restoring cloaking retention under strong watermarking; and (2) **strength-calibrated embedding** with BER-based detection, which raises watermark detectability to 99.2% (clean), 99.6% (JPEG80) and 93.7% (JPEG50) at 0% false-positive rate, while retaining 42.1% cloaking retention on 1,000 LFW faces (vs. 36.1% for global embedding, and 47.4% for cloaking alone). Under stronger cloaking (Fawkes mid), retention reaches 100% with watermark detection of 95–100%. To our knowledge, this is the first study to make adversarial face cloaking provenance-verifiable.

## 1. Introduction

**Face privacy vs. provenance.** Face recognition (FR) systems are widely deployed, raising privacy concerns: individuals' faces can be identified without consent [cite Fawkes]. Adversarial cloaking (e.g., Fawkes [Shan et al. 2020], LowKey [Zhou et al. 2021], Glaze [Shan et al. 2024]) adds imperceptible perturbations so that unauthorized FR models misidentify the subject. These methods are effective at *destroying recognition*, but they leave the protected image **without any verifiable provenance** — anyone can download, republish, or re-upload a victim's cloaked face with no way to attribute (or refute) its origin.

**The gap.** Digital watermarking [HiDDeN, StegaStamp, WAM] can embed a decodable ownership signal into images. Yet watermarking is designed for *clean* images; when applied to *cloaked* (adversarially perturbed) faces, the two objectives conflict: the cloaking perturbation distorts the watermark, and the watermark perturbs the face, weakening the cloak. EIAW [Liu et al. 2026] showed this conflict for generic image classification, but the face-cloaking scenario (whole-image Fawkes perturbations + neural watermarking + identity-level retention assessment) remains unstudied.

**Our contributions.** We conduct the first systematic study of provenance-verifiable privacy cloaking for face images, and show:

1. **The conflict is real and measurable.** Fawkes cloaking reduces WAM watermark decoding from 99.8% to 85.2% bit accuracy (TPR@95% from 98% to 6%) on 1,000 LFW faces. This quantifies, for the first time, how much cloaking perturbations damage neural watermarks.

2. **Safety-region guidance (SRG).** We compute an FR-sensitivity map from surrogate FR gradients and embed watermarks preferentially in low-sensitivity (safe) regions. SRG raises cloaking retention under strong watermarking (scaling_w=6) from 36.1% (global) to 42.1%, while watermark detection degrades by less than 1 percentage point.

3. **Strength-calibrated embedding with BER-based detection.** Increasing watermark strength (scaling_w: 2→6) and using bit-error-rate (BER) detection raises watermark detectability from 6% to 57.9% (TPR@95%) / 99.2% (TPR@BER≤0.25) on cloaked faces, with JPEG robustness of 99.6% (JPEG80) and 93.7% (JPEG50) at 0% FPR.

4. Under stronger cloaking (Fawkes mid), retention reaches 100% with watermark detection 95–100% across clean/JPEG80/JPEG50, demonstrating that the two objectives are jointly achievable.

## 2. Related Work

### 2.1 Adversarial Privacy Cloaking

Adversarial examples mislead deep models by adding imperceptible perturbations [Szegedy et al. 2014; Madry et al. 2018]. In face recognition, adversarial perturbations have been exploited for **privacy cloaking**: Fawkes [Shan et al., USENIX Sec. 2020] optimizes a feature-space "cloak" so that unauthorized face recognition models misidentify the subject, while the perturbation remains imperceptible (SSIM≈0.99). LowKey [Zhou et al., ICLR 2021] targets social-media pipelines, and Glaze [Shan et al., ICLR 2024] extends the idea to style mimicry. Physical patch attacks (e.g., AdvHat [Komkov & Petiushko, ICPR 2021], Adv-Makeup [Zhu et al., IJCAI 2021]) instead restrict perturbations to a localized patch. **However, all these works only destroy recognition; none embeds any extractable ownership/provenance signal into the protected image.**

### 2.2 Image Watermarking

Invisible watermarking embeds messages robust to distortions [Zhu et al. HiDDeN 2018; Zhang et al. StegaStamp 2020; Fernandez et al. Stable Signature, ICLR 2024; WAM [Ruiz et al. 2024]; InvisMark, WACV 2025]. For face imagery, FaceSigns [TOMM 2024] and LampMark [ACM MM 2024] embed semi-fragile or landmark-aware watermarks for authentication. **Yet these methods are designed for clean images and do not consider that the watermarked image must simultaneously preserve an adversarial/cloaking property.**

### 2.3 Adversarial Watermarking and Dual Protection

Recent works combine both goals: Adv-watermark [Luo et al., ACM MM 2020] treats a visible watermark as the adversarial perturbation; EIAW [Liu et al., BDMA 2026] embeds a blind, extractable watermark in the DCT domain and jointly optimizes it to attack classifiers, achieving ASR≈99.5% with EAR≈92%. CMUA-Watermark [AAAI 2022] instead uses adversarial watermarks to *attack* deepfake generators. **These methods operate on generic image classification with whole-image perturbations; none targets face recognition identity protection, and none studies whether an existing privacy cloak can be made provenance-verifiable while retaining its cloaking efficacy.** EIAW's Table 9 further reports that sequential (cloak→watermark) pipelines underperform joint optimization on classification; whether this holds for face cloaking is an open question we address (Sec. 4.8).

## 3. Method

### 3.1 Problem Formulation
Let $x \in \mathbb{R}^{H\times W\times 3}$ be a clean face image, $f: \mathbb{R}^{H\times W\times 3} \to \mathbb{R}^d$ an FR embedding model, and $c(\cdot)$ a cloaking perturbation such that $f(c(x))$ is far from $f(x)$ (identity not recognized). Given a message $m \in \{0,1\}^K$, we seek a watermarked cloaked image $y$ satisfying:
- **Cloaking retention**: $f(y)$ remains distant from $f(x)$ (FR evasion preserved);
- **Watermark detectability**: $D(y) \approx m$ for a decoder $D$;
- **Imperceptibility**: $y$ is perceptually close to $c(x)$ (PSNR/SSIM);
- **Robustness**: $D(T(y)) \approx m$ for distortion $T$ (esp. JPEG).

### 3.2 Fawkes Cloaking (Background)

Fawkes optimizes feature-space perturbations $\delta$ with bounded imperceptibility: $\min_\delta \|f(c(x)) - f_{target}\|$ s.t. $\|\delta\|_\infty \le \tau$, where $f$ is a VGGFace-style feature extractor. Perturbations are optimized on aligned 112×112 crops and merged back onto the full image. We use the official implementation: **low** mode (extractor_2, 40 iterations, DSSIM threshold 0.004) and **mid** mode (extractor_0+extractor_2, 75 iterations, threshold 0.012).

### 3.3 Safety-Region Guidance (SRG)

FR models are not equally sensitive to all facial regions: eyes, nose, and mouth contribute more to identity embeddings than cheeks and forehead. We exploit this by computing an FR-sensitivity map $R \in [0,1]^{H\times W}$ from surrogate FR gradients:
$$R = \text{norm}\left(\left|\frac{\partial \|f(\tilde{x})\|_2}{\partial \tilde{x}}\right|\right), \quad \tilde{x} = \text{aligned}(c(x))$$
using arcface34 as the surrogate (mainstream FR architecture). The safe region is $S = 1 - R$ (low sensitivity = safe for watermarking). The watermark residual is weighted by the safety map before blending:
$$y = c(x) + \alpha \cdot S \cdot (w(c(x)) - c(x)),$$
where $w(\cdot)$ is the WAM embedder and $\alpha$ the blending factor. This keeps watermark energy out of FR-critical regions, preserving cloaking while retaining decodability (Sec. 4.3).

### 3.4 Neural Watermark Embedding (WAM)

We use Watermark Anything (WAM) [Ruiz et al. 2024], a VAE-based embedder $w$ and ViT-based extractor $D$ trained with JPEG/augmentation robustness. The embedder produces a residual $\Delta = w(x, m)$ for message $m$; the watermarked image is $x + \beta \Delta$ with **strength** $\beta$ (scaling_w). We show strength is the key lever for cloaking robustness (Sec. 4.5): weak embeddings ($\beta=2$, the official default) are destroyed by cloaking; strong embeddings ($\beta=6$) survive.

### 3.5 BER-based Detection

For a queried image and candidate message $\hat{m}$, the extractor emits per-pixel logits over the 32 message bits. We average logits spatially and threshold at 0 to obtain the decoded bit vector $b \in \{0,1\}^{32}$. Following watermarking practice, we declare the watermark present iff
$$\text{BER}(b, \hat{m}) = \frac{1}{32}\sum_i \mathbb{1}[b_i \neq \hat{m}_i] \le \theta,$$
with $\theta = 0.25$ (≤8 bit errors of 32). This is more robust than exact decoding under compound distortions (cloaking + JPEG), and yields 0% FPR on unwatermarked images (Sec. 4.7).

## 4. Experiments

### 4.1 Setup
- **Data**: 1,000 LFW faces (771 identities, random fair subset; 13,233 total)
- **Cloaking**: Fawkes low (40 iter, th=0.004) / mid (75 iter, th=0.012)
- **Watermark**: WAM (nbits=32), scaling_w ∈ {2, 6}
- **FR surrogate**: Fawkes extractor_2 (training model); facenet (unseen)
- **Safety map**: arcface34 gradients
- **Metrics**: cloaking retention (keep_rate: sim < 0.4), watermark TPR (BER≤0.25), FPR, PSNR/SSIM

### 4.2 The Cloaking–Watermark Conflict

**Finding 1 (conflict).** Watermark decoding is severely degraded by cloaking. On clean LFW faces, WAM (scaling_w=2) achieves 99.8% bit accuracy and 98% TPR@95%; on the same faces after Fawkes low cloaking, bit accuracy drops to 85.2% and TPR@95% to 6.0% (n=1,000). Fig. X visualizes per-face bit accuracy before/after cloaking.

### 4.3 Main Results (1000 LFW, low cloaking)

**Table 1. Main comparison (n=1,000, scaling_w=6).**

| Group | Treatment | Retention (keep↑) | sim↓ | WM clean | WM JPEG80 | WM JPEG50 | PSNR | SSIM | LPIPS |
|---|---|---|---|---|---|---|---|---|---|
| A | Fawkes cloak (no WM) | **47.4%** | 0.426 | — | — | — | ~40 | ~0.98 | ~0.01 |
| B | + WAM global | 36.1% | 0.480 | 99.2% | 99.6% | 93.7% | 29.0 | 0.851 | 0.140 |
| C | + WAM safety-region | **42.1%** | 0.452 | 98.6% | 99.0% | 92.7% | **30.1** | **0.879** | **0.111** |

WM = watermark detection TPR with BER≤0.25. *Retention*: fraction of faces whose extractor_2 embedding similarity to the original stays < 0.4 (i.e., not re-identified as the original identity).

- Global strong watermarking (B) breaks cloaking: retention drops 47.4%→36.1% (p < 0.001, McNemar).
- Safety-region guidance (C) recovers retention to 42.1% with <1pp watermark loss — SRG embeds watermark preferentially in FR-insensitive regions, so the watermark's perturbation no longer destroys the cloak.

### 4.4 JPEG Robustness

**Table 2. Watermark detection under JPEG (n=1,000, BER≤0.25).**

| Group | clean | JPEG80 | JPEG50 |
|---|---|---|---|
| B (global) | 99.2% | 99.6% | 93.7% |
| C (safety-region) | 98.6% | 99.0% | 92.7% |

Without strength calibration (scaling_w=2), JPEG50 detection collapses to 0.3%; with scaling_w=6 and BER detection, it reaches 93.7% — a 300× improvement in detection rate.

### 4.5 Strength Calibration Ablation

**Table 3. Effect of scaling_w (n=1,000, B group).**

| scaling_w | clean TPR@95% | JPEG80 TPR@95% | JPEG50 TPR@95% | PSNR |
|---|---|---|---|---|
| 2.0 | 6.0% | 16.2% | 0.3% | ~38 |
| 6.0 | **57.9%** | **64.6%** | 10.0% | ~30 |

Higher watermark strength trades image quality (PSNR 38→30 dB) for detectability; combined with BER detection (Table 1), TPR reaches 93–99%.

### 4.6 Stronger Cloaking (Fawkes mid)

**Table 4. mid cloaking + sw6 (n=20).**

| Group | Retention | sim | WM clean | WM JPEG80 | WM JPEG50 |
|---|---|---|---|---|---|
| B (global) | 100% | 0.037 | 100% | 100% | 95% |
| C (safety-region) | 100% | −0.003 | 100% | 100% | 95% |

Under stronger cloaking (75-iter, dual-extractor Fawkes), cloaking dominates and strong watermarks no longer compromise retention; both objectives are simultaneously satisfied.

### 4.7 False-Positive Analysis

On 100 unwatermarked cloaked faces, decoding against 10 random messages each (500 trials), BER≤0.25 detection yields **FPR = 0.00%** — the watermark is highly specific, as expected for 32-bit messages.

### 4.8 Comparison with EIAW

EIAW [Liu et al. 2026] reports sequential (cloak→watermark) failure on ImageNet classification (ASR 76% or EAR 65%) and advocates joint optimization. Our results nuance this for face cloaking: sequential embedding works if (a) watermark strength is calibrated and (b) embedding is guided by FR-sensitivity maps. We do not claim to beat joint optimization; we show sequential embedding is viable and simpler, directly answering the scenario EIAW's Table 9 leaves open for face recognition.

### 4.9 Limitation & Discussion

- Exact decoding (TPR@95%) under JPEG50 remains ~10% even with sw6; BER-based detection is required for robustness, matching watermarking practice (threshold on bit error rate).
- Cloaking retention under low mode is model-specific: 47% on the training extractor, lower on unseen models (facenet). Stronger cloaking (mid) restores retention (95–100%) at higher perturbation cost.
- Safety-region guidance currently uses surrogate FR gradients; landmark-based refinement is a promising direction.

## 5. Conclusion

## References
