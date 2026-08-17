"""
t-SNE embedding space visualization.
Extracts FR embeddings from arcface34 for clean/cloaked/watermarked images,
then plots t-SNE scatter showing how cloaking moves identities apart
and watermarking preserves that separation.

Usage:
    conda run -n fawkes python code/06_eval/eval_tsne.py
"""
import os
import sys
import glob
import numpy as np
from pathlib import Path

# Add baselines to path (only if needed for fawkes alignment)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
# sys.path.insert(0, str(PROJECT_ROOT / "baselines" / "fawkes"))  # Not needed for t-SNE

try:
    import torch
    from torchvision import transforms
    from PIL import Image
except ImportError:
    print("ERROR: torch/torchvision not installed. Run: pip install torch torchvision")
    sys.exit(1)

try:
    from sklearn.manifold import TSNE
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    print("ERROR: scikit-learn/matplotlib not installed. Run: pip install scikit-learn matplotlib")
    sys.exit(1)


def load_arcface():
    """Load arcface34 model (insightface-style via facenet_pytorch or manual)."""
    try:
        from facenet_pytorch import InceptionResnetV1
        model = InceptionResnetV1(pretrained="vggface2").eval()
        print("[INFO] Loaded InceptionResnetV1 (vggface2) as FR surrogate")
        return model, "facenet"
    except ImportError:
        pass

    # Fallback: try insightface
    try:
        import insightface
        from insightface.app import FaceAnalysis
        app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
        app.prepare(ctx_id=0, det_size=(640, 640))
        print("[INFO] Loaded insightface buffalo_l as FR surrogate")
        return app, "insightface"
    except Exception:
        pass

    print("ERROR: No FR model available. Install facenet_pytorch or insightface.")
    sys.exit(1)


def extract_embeddings_facenet(model, img_paths, device="cpu"):
    """Extract embeddings using InceptionResnetV1."""
    transform = transforms.Compose([
        transforms.Resize((160, 160)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])

    embeddings = []
    valid_paths = []
    model = model.to(device).eval()

    with torch.no_grad():
        for p in img_paths:
            try:
                img = Image.open(p).convert("RGB")
                tensor = transform(img).unsqueeze(0).to(device)
                emb = model(tensor).cpu().numpy().flatten()
                embeddings.append(emb)
                valid_paths.append(p)
            except Exception as e:
                print(f"[WARN] Failed {p}: {e}")

    return np.array(embeddings), valid_paths


def extract_embeddings_insightface(app, img_paths):
    """Extract embeddings using insightface."""
    embeddings = []
    valid_paths = []
    for p in img_paths:
        try:
            img = np.array(Image.open(p).convert("RGB"))
            faces = app.get(img)
            if faces:
                emb = faces[0].embedding
                embeddings.append(emb)
                valid_paths.append(p)
        except Exception as e:
            print(f"[WARN] Failed {p}: {e}")
    return np.array(embeddings), valid_paths


def collect_pairs(data_root, n_samples=200):
    """Collect (original, cloaked, watermarked) triplets."""
    original_dir = os.path.join(data_root, "assets", "dataset", "lfw1000", "original")
    low_dir = os.path.join(data_root, "assets", "experiments", "full_low")
    a_low_dir = os.path.join(data_root, "assets", "experiments", "A_low", "input")
    mid_dir = os.path.join(data_root, "assets", "experiments", "full_mid")

    # Get filenames from C_sw6 (watermarked) since those are guaranteed to exist
    c_files = sorted(glob.glob(os.path.join(low_dir, "C_sw6", "*.jpg")))
    if not c_files:
        c_files = sorted(glob.glob(os.path.join(mid_dir, "C_sw6", "*.jpg")))

    # Extract base names
    basenames = []
    for f in c_files[:n_samples]:
        bn = os.path.basename(f).replace("_cloaked_wm.jpg", "")
        basenames.append(bn)

    # Collect paths
    originals, cloaked, watermarked_b, watermarked_c = [], [], [], []
    for bn in basenames:
        orig = os.path.join(original_dir, bn + ".jpg")
        if not os.path.exists(orig):
            continue

        # Cloaked (A group) - check A_low/input first, then A_mid/input
        cloaked_path = os.path.join(a_low_dir, bn + "_cloaked.jpeg")
        if not os.path.exists(cloaked_path):
            cloaked_path = os.path.join(a_low_dir, bn + "_cloaked.jpg")
        if not os.path.exists(cloaked_path):
            cloaked_path = os.path.join(mid_dir, "A_mid", "input", bn + "_cloaked.jpeg")
        if not os.path.exists(cloaked_path):
            continue

        # Watermarked B (global)
        wm_b = os.path.join(low_dir, "B_sw6", bn + "_cloaked_wm.jpg")
        wm_c = os.path.join(low_dir, "C_sw6", bn + "_cloaked_wm.jpg")

        originals.append(orig)
        cloaked.append(cloaked_path)
        if os.path.exists(wm_b):
            watermarked_b.append(wm_b)
        if os.path.exists(wm_c):
            watermarked_c.append(wm_c)

    print(f"[INFO] Collected {len(originals)} triplets")
    return originals, cloaked, watermarked_b, watermarked_c, basenames


def compute_tsne(embeddings_list, labels_list, n_samples=500, perplexity=30):
    """Compute t-SNE on concatenated embeddings."""
    all_embs = np.concatenate(embeddings_list, axis=0)
    all_labels = np.concatenate(labels_list, axis=0)

    if len(all_embs) > n_samples:
        idx = np.random.choice(len(all_embs), n_samples, replace=False)
        all_embs = all_embs[idx]
        all_labels = all_labels[idx]

    tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42, n_iter=1000)
    coords = tsne.fit_transform(all_embs)
    return coords, all_labels


def plot_tsne(coords, labels, output_path, title="t-SNE of FR Embeddings"):
    """Plot t-SNE scatter."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))

    colors = {"Clean": "#2196F3", "Cloaked (Fawkes)": "#FF5722",
              "Cloaked + WM (B)": "#4CAF50", "Cloaked + WM (C)": "#9C27B0"}

    for label, color in colors.items():
        mask = labels == label
        if mask.any():
            ax.scatter(coords[mask, 0], coords[mask, 1],
                       c=color, label=label, alpha=0.6, s=15, edgecolors="none")

    ax.set_title(title, fontsize=14)
    ax.legend(fontsize=11, markerscale=2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("t-SNE dim 1", fontsize=12)
    ax.set_ylabel("t-SNE dim 2", fontsize=12)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Saved t-SNE plot to {output_path}")


def main():
    data_root = str(PROJECT_ROOT)
    output_dir = os.path.join(data_root, "paper", "figures")
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print("t-SNE Embedding Space Visualization")
    print("=" * 60)

    # Collect image triplets
    originals, cloaked, wm_b, wm_c, basenames = collect_pairs(data_root, n_samples=200)

    if len(originals) < 10:
        print("[ERROR] Not enough image pairs found")
        sys.exit(1)

    # Load FR model
    fr_model, fr_type = load_arcface()

    # Extract embeddings
    print("[INFO] Extracting embeddings from clean images...")
    emb_orig, paths_orig = (extract_embeddings_facenet(fr_model, originals)
                            if fr_type == "facenet"
                            else extract_embeddings_insightface(fr_model, originals))

    print("[INFO] Extracting embeddings from cloaked images...")
    emb_cloaked, paths_cloaked = (extract_embeddings_facenet(fr_model, cloaked)
                                  if fr_type == "facenet"
                                  else extract_embeddings_insightface(fr_model, cloaked))

    emb_wm_b, paths_wm_b = np.array([]), []
    if wm_b:
        print("[INFO] Extracting embeddings from WM-B images...")
        emb_wm_b, paths_wm_b = (extract_embeddings_facenet(fr_model, wm_b)
                                 if fr_type == "facenet"
                                 else extract_embeddings_insightface(fr_model, wm_b))

    emb_wm_c, paths_wm_c = np.array([]), []
    if wm_c:
        print("[INFO] Extracting embeddings from WM-C images...")
        emb_wm_c, paths_wm_c = (extract_embeddings_facenet(fr_model, wm_c)
                                 if fr_type == "facenet"
                                 else extract_embeddings_insightface(fr_model, wm_c))

    # Build embeddings list
    emb_list = [emb_orig, emb_cloaked]
    label_list = [np.array(["Clean"] * len(emb_orig)),
                  np.array(["Cloaked (Fawkes)"] * len(emb_cloaked))]

    if len(emb_wm_b) > 0:
        emb_list.append(emb_wm_b)
        label_list.append(np.array(["Cloaked + WM (B)"] * len(emb_wm_b)))

    if len(emb_wm_c) > 0:
        emb_list.append(emb_wm_c)
        label_list.append(np.array(["Cloaked + WM (C)"] * len(emb_wm_c)))

    # Compute t-SNE
    print("[INFO] Computing t-SNE...")
    coords, labels = compute_tsne(emb_list, label_list, n_samples=500)

    # Plot
    output_path = os.path.join(output_dir, "fig7_tsne.png")
    plot_tsne(coords, labels, output_path,
              title="t-SNE: FR Embedding Space (Clean vs Cloaked vs Watermarked)")

    # Also save embedding statistics
    stats = {
        "n_clean": len(emb_orig),
        "n_cloaked": len(emb_cloaked),
        "n_wm_b": len(emb_wm_b) if len(emb_wm_b) > 0 else 0,
        "n_wm_c": len(emb_wm_c) if len(emb_wm_c) > 0 else 0,
    }

    # Compute inter-group distances
    from sklearn.metrics.pairwise import cosine_distances
    if len(emb_orig) > 0 and len(emb_cloaked) > 0:
        n = min(len(emb_orig), len(emb_cloaked))
        d_clean_cloaked = cosine_distances(emb_orig[:n], emb_cloaked[:n]).diagonal().mean()
        stats["mean_cosine_dist_clean_vs_cloaked"] = float(d_clean_cloaked)

    if len(emb_cloaked) > 0 and len(emb_wm_c) > 0:
        n = min(len(emb_cloaked), len(emb_wm_c))
        d_cloaked_wmc = cosine_distances(emb_cloaked[:n], emb_wm_c[:n]).diagonal().mean()
        stats["mean_cosine_dist_cloaked_vs_wm_c"] = float(d_cloaked_wmc)

    stats_path = os.path.join(output_dir, "tsne_stats.json")
    import json
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"[INFO] Stats saved to {stats_path}")

    print("\n[DONE] t-SNE visualization complete!")


if __name__ == "__main__":
    main()
