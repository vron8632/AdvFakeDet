# 投稿材料（Submission Package）

> 目标期刊：Signal Processing: Image Communication（Elsevier, JCR Q2 非 OA）| 状态: 草稿待用户填入作者信息
> 论文：Provenance-Verifiable Privacy Cloaking for Face Images: Safety-Region-Guided Neural Watermarking with JPEG-Robust Detection

---

## 1. Highlights（期刊要求 3–5 条，每条 ≤85 字符含空格）

- Adversarial face cloaking destroys neural watermarks (98% → 6% TPR@95%); we quantify this conflict for the first time.  [92 字符，需缩短]
- Safety-region-guided watermarking restores cloaking retention from 36.1% to 42.1% under strong watermarking.  [95，需缩短]
- Strength-calibrated embedding with BER detection reaches 93–99% JPEG-robust decode at 0–0.8% false positives.
- Sequential cloak→watermark preserves cloaking (PSR 93.5%) whereas the reverse order degrades it to 70–81.5%.
- Outperforms the SOTA InvisMark baseline, which fails under JPEG on the same protocol.

**缩短版（≤85 字符）：**
- Cloaking destroys neural watermarks (98%→6% TPR@95%); first quantitative evidence.  (78)
- Safety-region guidance restores cloaking retention (36.1%→42.1%) under strong watermarking.  (82)
- Strength calibration + BER detection give 93–99% JPEG-robust decode at 0–0.8% FPR.  (79)
- Sequential cloak→watermark keeps PSR 93.5%; reverse order drops it to 70–81.5%.  (78)
- Beats SOTA InvisMark, which fails under JPEG on the same protocol.  (66)

---

## 2. Cover Letter（草稿，TBD 处替换）

```
[Date]

Dear Editor-in-Chief,

We are pleased to submit our manuscript "Provenance-Verifiable Privacy Cloaking for
Face Images: Safety-Region-Guided Neural Watermarking with JPEG-Robust Detection" for
consideration as a regular research paper in Signal Processing: Image Communication.

Face recognition (FR) systems raise serious privacy concerns: facial images shared
online can be scraped and enrolled without consent. Adversarial privacy cloaking
(e.g., Fawkes) protects against unauthorized FR but leaves cloaked images without any
verifiable provenance, so a victim's protected face can be republished with no
accountability. This paper makes adversarial face cloaking provenance-verifiable by
embedding a decodable neural watermark into cloaked faces while preserving FR evasion.

Our contributions:
1. We quantify, for the first time, the cloaking–watermark conflict: Fawkes cloaking
   reduces WAM watermark decoding from 99.8% bit accuracy (98% TPR@95%) on clean faces
   to 85.2% (6%) on cloaked faces.
2. We propose safety-region guidance (SRG): FR-sensitivity maps steer watermark energy
   away from identity-critical regions, raising cloaking retention under strong
   watermarking from 36.1% to 42.1% with <1pp watermark loss.
3. We show that strength calibration plus BER-based detection restores JPEG-robust
   detectability (93–99% TPR under JPEG50/80, 0–0.8% FPR), directly addressing WAM's
   known JPEG weakness.
4. We provide a systematic comparison: our sequential cloak→watermark pipeline
   preserves cloaking (PSR 93.5%) where the reverse order degrades it (70–81.5%), is
   competitive with joint optimization (EIAW, BDMA 2026; ARFP 2026), and outperforms
   the SOTA InvisMark baseline (WACV 2025), which fails under JPEG on the same protocol.

The manuscript includes 5 figures and 8 tables with results on 1,000 LFW faces
(771 identities) under two cloaking strengths. We believe the work is timely for the
signal processing community given the rapid adoption of privacy-enhancing and
provenance technologies for visual data.

The manuscript has not been published and is not under consideration elsewhere.
All authors have approved the submission. We declare no competing interests.

Sincerely,
[Author Name], [Affiliation, on behalf of all authors]
```

---

## 3. Author Contributions（CRediT，草稿）

- **Conceptualization**: [Author 1], [Author 2]
- **Methodology**: [Author 1], [Author 2]
- **Software**: [Author 1]
- **Validation**: [Author 1], [Author 2]
- **Formal analysis**: [Author 1]
- **Investigation**: [Author 1]
- **Data curation**: [Author 1]
- **Writing – original draft**: [Author 1]
- **Writing – review & editing**: [Author 1], [Author 2]
- **Visualization**: [Author 1]
- **Supervision**: [Author 2]
- **Project administration**: [Author 1], [Author 2]

---

## 4. 待办（用户侧）
- [ ] main.tex 作者/单位/致谢（现为 TBD）
- [ ] fig1 teaser + fig2 框架图（gpt-image-2 生成后替换占位）
- [ ] 上述材料中的作者名替换
