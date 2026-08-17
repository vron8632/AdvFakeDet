"""
Perceptual quality comparison figure.
Creates a side-by-side comparison of original/cloaked/watermarked images
with PSNR/SSIM/LPIPS annotations.

Usage:
    python code/06_eval/eval_perceptual.py
"""
import os
import sys
import json
import numpy as np
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    from PIL import Image
except ImportError:
    print("ERROR: matplotlib/PIL not installed")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def compute_psnr(img1, img2):
    """Compute PSNR between two images."""
    arr1 = np.array(img1).astype(float)
    arr2 = np.array(img2).astype(float)
    mse = np.mean((arr1 - arr2) ** 2)
    if mse == 0:
        return float("inf")
    return 20 * np.log10(255.0 / np.sqrt(mse))


def compute_ssim_simple(img1, img2):
    """Simplified SSIM (luminance/contrast/structure)."""
    arr1 = np.array(img1).astype(float)
    arr2 = np.array(img2).astype(float)

    mu1, mu2 = arr1.mean(), arr2.mean()
    sig1, sig2 = arr1.std(), arr2.std()
    sig12 = ((arr1 - mu1) * (arr2 - mu2)).mean()

    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    ssim = ((2 * mu1 * mu2 + c1) * (2 * sig12 + c2)) / \
           ((mu1**2 + mu2**2 + c1) * (sig1**2 + sig2**2 + c2))
    return float(ssim)


def select_representative_images(data_root, n=4):
    """Select diverse representative images for the figure."""
    original_dir = data_root / "assets" / "dataset" / "lfw1000" / "original"
    mid_dir = data_root / "assets" / "experiments" / "full_mid"
    a_mid_dir = data_root / "assets" / "experiments" / "A_mid" / "input"

    # Get first N images from mid cloaking (stronger effect, more visible)
    wm_c_dir = mid_dir / "C_sw6"
    wm_files = sorted(list(wm_c_dir.glob("*.jpg")))[:n * 3]  # Get more, pick diverse

    selected = []
    for wf in wm_files[:n * 3]:
        bn = wf.stem.replace("_cloaked_wm", "")
        orig = original_dir / (bn + ".jpg")
        cloaked_candidates = [
            a_mid_dir / (bn + "_cloaked.jpeg"),
            a_mid_dir / (bn + "_cloaked.jpg"),
        ]
        cloaked = None
        for c in cloaked_candidates:
            if c.exists():
                cloaked = c
                break

        if orig.exists() and cloaked is not None and wf.exists():
            safety_map = mid_dir / "safety_maps" / (bn + "_cloaked_map.npy")
            selected.append({
                "original": str(orig),
                "cloaked": str(cloaked),
                "watermarked": str(wf),
                "safety_map": str(safety_map) if safety_map.exists() else None,
                "name": bn,
            })
            if len(selected) >= n:
                break

    return selected


def create_perceptual_figure(selected, output_path):
    """Create a multi-panel perceptual quality comparison figure."""
    n = len(selected)
    fig = plt.figure(figsize=(16, 4 * n))
    gs = gridspec.GridSpec(n, 5, wspace=0.15, hspace=0.25,
                           width_ratios=[1, 1, 1, 1, 0.3])

    for i, item in enumerate(selected):
        # Load images
        orig = Image.open(item["original"]).convert("RGB")
        cloaked = Image.open(item["cloaked"]).convert("RGB")
        watermarked = Image.open(item["watermarked"]).convert("RGB")

        # Compute metrics
        psnr_cloak = compute_psnr(orig, cloaked)
        ssim_cloak = compute_ssim_simple(orig, cloaked)
        psnr_wm = compute_psnr(orig, watermarked)
        ssim_wm = compute_ssim_simple(orig, watermarked)

        # Safety map
        has_safety = item["safety_map"] is not None

        # Column 0: Original
        ax0 = fig.add_subplot(gs[i, 0])
        ax0.imshow(orig)
        ax0.set_title("Original" if i == 0 else "", fontsize=11)
        ax0.set_ylabel(f"Image {i+1}", fontsize=11, fontweight="bold")
        ax0.set_xticks([])
        ax0.set_yticks([])

        # Column 1: Cloaked
        ax1 = fig.add_subplot(gs[i, 1])
        ax1.imshow(cloaked)
        ax1.set_title("Cloaked (Fawkes)" if i == 0 else "", fontsize=11)
        ax1.text(0.5, -0.08, f"PSNR={psnr_cloak:.1f}dB\nSSIM={ssim_cloak:.3f}",
                 transform=ax1.transAxes, ha="center", fontsize=8, color="#666")
        ax1.set_xticks([])
        ax1.set_yticks([])

        # Column 2: Watermarked
        ax2 = fig.add_subplot(gs[i, 2])
        ax2.imshow(watermarked)
        ax2.set_title("Cloaked + Watermarked" if i == 0 else "", fontsize=11)
        ax2.text(0.5, -0.08, f"PSNR={psnr_wm:.1f}dB\nSSIM={ssim_wm:.3f}",
                 transform=ax2.transAxes, ha="center", fontsize=8, color="#666")
        ax2.set_xticks([])
        ax2.set_yticks([])

        # Column 3: Safety map overlay
        ax3 = fig.add_subplot(gs[i, 3])
        if has_safety:
            safety = np.load(item["safety_map"])
            ax3.imshow(cloaked)
            im = ax3.imshow(safety, cmap="jet", alpha=0.4, vmin=0, vmax=1)
            ax3.set_title("Safety Map Overlay" if i == 0 else "", fontsize=11)
        else:
            ax3.text(0.5, 0.5, "N/A", transform=ax3.transAxes, ha="center")
            ax3.set_title("Safety Map" if i == 0 else "", fontsize=11)
        ax3.set_xticks([])
        ax3.set_yticks([])

        # Column 4: Difference map
        ax4 = fig.add_subplot(gs[i, 4])
        diff = np.abs(np.array(orig).astype(float) - np.array(watermarked).astype(float))
        diff_norm = np.clip(diff / diff.max() * 3, 0, 1) if diff.max() > 0 else diff
        ax4.imshow(diff_norm)
        ax4.set_title("Δ" if i == 0 else "", fontsize=11)
        ax4.set_xticks([])
        ax4.set_yticks([])

    # Add colorbar for safety map
    if any(item["safety_map"] for item in selected):
        cbar_ax = fig.add_axes([0.92, 0.15, 0.01, 0.7])
        sm = plt.cm.ScalarMappable(cmap="jet", norm=plt.Normalize(0, 1))
        sm.set_array([])
        fig.colorbar(sm, cax=cbar_ax, label="FR Sensitivity")

    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"[INFO] Saved perceptual quality figure to {output_path}")


def main():
    print("=" * 60)
    print("Perceptual Quality Comparison Figure")
    print("=" * 60)

    selected = select_representative_images(PROJECT_ROOT, n=4)
    print(f"[INFO] Selected {len(selected)} representative images")

    if not selected:
        print("[ERROR] No images found")
        sys.exit(1)

    output_path = PROJECT_ROOT / "paper" / "figures" / "fig8_perceptual_quality.png"
    create_perceptual_figure(selected, output_path)

    # Also compute and save aggregate stats
    all_psnr_cloak, all_psnr_wm = [], []
    all_ssim_cloak, all_ssim_wm = [], []

    original_dir = PROJECT_ROOT / "assets" / "dataset" / "lfw1000" / "original"
    mid_dir = PROJECT_ROOT / "assets" / "experiments" / "full_mid"

    import glob
    wm_c_files = sorted(glob.glob(str(mid_dir / "C_sw6" / "*.jpg")))[:50]

    for wf in wm_c_files:
        bn = os.path.basename(wf).replace("_cloaked_wm.jpg", "")
        orig_path = original_dir / (bn + ".jpg")
        if not orig_path.exists():
            continue
        orig = Image.open(orig_path).convert("RGB")
        wm = Image.open(wf).convert("RGB")
        psnr = compute_psnr(orig, wm)
        ssim = compute_ssim_simple(orig, wm)
        all_psnr_wm.append(psnr)
        all_ssim_wm.append(ssim)

    # Cloaked images
    wm_cloaked_files = sorted(glob.glob(str(PROJECT_ROOT / "assets" / "experiments" / "A_mid" / "input" / "*_cloaked.*")))[:50]
    for cf in wm_cloaked_files:
        bn = os.path.basename(cf).replace("_cloaked.jpeg", "").replace("_cloaked.jpg", "")
        orig_path = original_dir / (bn + ".jpg")
        if not orig_path.exists():
            continue
        orig = Image.open(orig_path).convert("RGB")
        cloak = Image.open(cf).convert("RGB")
        psnr = compute_psnr(orig, cloak)
        ssim = compute_ssim_simple(orig, cloak)
        all_psnr_cloak.append(psnr)
        all_ssim_cloak.append(ssim)

    stats = {
        "cloaked_vs_original": {
            "mean_psnr": float(np.mean(all_psnr_cloak)) if all_psnr_cloak else 0,
            "std_psnr": float(np.std(all_psnr_cloak)) if all_psnr_cloak else 0,
            "mean_ssim": float(np.mean(all_ssim_cloak)) if all_ssim_cloak else 0,
            "n": len(all_psnr_cloak),
        },
        "watermarked_vs_original": {
            "mean_psnr": float(np.mean(all_psnr_wm)) if all_psnr_wm else 0,
            "std_psnr": float(np.std(all_psnr_wm)) if all_psnr_wm else 0,
            "mean_ssim": float(np.mean(all_ssim_wm)) if all_ssim_wm else 0,
            "n": len(all_psnr_wm),
        },
    }

    stats_path = PROJECT_ROOT / "assets" / "experiments" / "perceptual_quality_stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"[INFO] Aggregate stats saved to {stats_path}")

    print(f"\nCloaked vs Original: PSNR={stats['cloaked_vs_original']['mean_psnr']:.1f}±"
          f"{stats['cloaked_vs_original']['std_psnr']:.1f} dB, "
          f"SSIM={stats['cloaked_vs_original']['mean_ssim']:.3f}")
    print(f"Watermarked vs Original: PSNR={stats['watermarked_vs_original']['mean_psnr']:.1f}±"
          f"{stats['watermarked_vs_original']['std_psnr']:.1f} dB, "
          f"SSIM={stats['watermarked_vs_original']['mean_ssim']:.3f}")

    print("\n[DONE] Perceptual quality analysis complete!")


if __name__ == "__main__":
    main()
