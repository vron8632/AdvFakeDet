# AdvFakeDet: Provenance-Verifiable Privacy Cloaking for Face Images

Safety-region-guided neural watermarking with JPEG-robust detection for adversarial face cloaking.

## Overview

This repository implements **provenance-verifiable privacy cloaking**: embedding a decodable neural watermark (WAM) into Fawkes-cloaked face images so that face recognition evasion is preserved while the watermark remains detectable and JPEG-robust.

Key scientific findings:
- **The JPEG-fragility bottleneck**: cloaking alone doesn't degrade WAM at pixel level (99.89% vs 99.84% bit accuracy), but JPEG recompression — standard on sharing platforms — collapses decoding on cloaked faces (6% TPR@95% at JPEG75; 85.2% vs 88.3% vs clean), making JPEG robustness the deployment bottleneck.
- **Safety-region guidance (SRG)**: FR-sensitivity maps guide watermark embedding away from FR-critical regions, restoring cloaking retention (36.1% → 42.1%) with <1pp watermark loss.
- **Strength calibration + BER detection**: scaling_w=6 and BER≤0.25 detection reach 99.2%/99.6%/93.7% (clean/JPEG80/JPEG50) at 0.4–0.8% FPR (0% at θ≤0.15).
- **Sequential ≈ joint, and order matters**: sequential embedding (cloak → SRG-guided WAM) is competitive with joint optimization (PSR 85% vs 85%) and preserves cloaking (93.5%) whereas watermark-then-cloak degrades it to 70–81.5%.
- **SOTA baseline**: InvisMark (WACV 2025) official checkpoint fails under JPEG on the same protocol (TPR 0% at JPEG80/50, even on clean faces), while our method stays 93–100%.

## Repository Structure

```
├── code/
│   ├── 01_data_prep/       # LFW 1000 subset construction
│   ├── 02_fawkes_cloak/    # Fawkes cloaking (low/mid/high, batch)
│   ├── 03_wam_watermark/   # WAM embedding, JPEG-aware finetune, checkpoint tools
│   ├── 04_safety_map/      # FR-sensitivity safety maps (arcface gradients)
│   ├── 05_freq_constraint/ # Frequency-domain experiments + E-group joint optimization
│   ├── 06_eval/            # PSR, watermark decode (BER), FR identity, figures
│   └── common/             # DOI verification etc.
├── paper/
│   ├── main.tex            # Elsevier elsarticle LaTeX manuscript
│   ├── main.pdf            # Compiled PDF
│   ├── figures/            # All figures (teaser/framework placeholders included)
│   └── FIGURE_PROMPTS_中文.md  # Chinese prompts for gpt-image-2
├── docs/                   # Plans, experiment audits, novelty reports
├── related_work/           # Literature (EIAW, ARFP) and analyses
├── baselines/              # Fawkes, WAM official code
└── assets/                 # Weights, datasets, experiment outputs (gitignored)
```

## Quick Start

```bash
# 1. Environment (conda)
conda create -n fawkes python=3.8        # TF 2.4.1 + CUDA 11.2 (Fawkes)
conda create -n newpatch python=3.8      # torch 2.4.1 (WAM, evaluation)

# 2. Download assets
# WAM checkpoint: hf-mirror.com/facebook/watermark-anything -> baselines/wam/checkpoints/
# Fawkes extractors: mirror.cs.uchicago.edu/fawkes/files/ -> baselines/fawkes/fawkes/model/

# 3. Full experiment
bash code/run_mid_experiment.sh          # mid cloaking + B/C watermark + PSR + BER eval
```

## Key Results (1000 LFW, low cloaking, β=6)

| Group | PSR (retention) | WM clean | WM JPEG80 | WM JPEG50 | PSNR/SSIM/LPIPS |
|---|---|---|---|---|---|
| A: cloak only | 47.4% | — | — | — | ~40/0.98/0.01 |
| B: +WAM global | 36.1% | 99.2% | 99.6% | 93.7% | 29.0/0.851/0.140 |
| C: +WAM safety-region | **42.1%** | 98.6% | 99.0% | 92.7% | **30.1/0.879/0.111** |

FPR = 0.2–0.6% at θ=0.25 under matched JPEG75 (0% at θ≤0.15, 500 trials). Under mid cloaking: PSR 93.5% + watermark 95–100% coexist. See `docs/W4_supplementary_20260817.md` (SOTA baseline, α ablation, BER curve, embedding order) and `docs/PROTOCOL_CORRECTION_20260817.md` (JPEG75 protocol fix).

## Related Work

- EIAW (BDMA 2026): joint optimization of attack + DCT watermark (classification)
- ARFP (arXiv:2605.01217): reversible face protection with keyed recovery (joint-training)
- WAM (ICLR 2025): neural watermarking backbone

## License

Research use only. Third-party code (Fawkes, WAM) retains their licenses.
