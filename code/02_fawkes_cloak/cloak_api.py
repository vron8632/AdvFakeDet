"""
Fawkes 遮蔽 Python API 版（支持自定义强度与提取器组合，绕过 CLI 的 mode 限制）。
用法: conda run -n fawkes python code/02_fawkes_cloak/cloak_api.py --dir X --th 0.012 --max-step 75 --lr 20 --gpu 0
"""
import argparse
import glob
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "baselines", "fawkes"))

import numpy as np
from fawkes.protection import Fawkes, generate_cloak_images, IMG_SIZE, PREPROCESS
from fawkes.differentiator import FawkesMaskGeneration
from fawkes.utils import init_gpu, filter_image_paths, Faces, reverse_process_cloaked, load_extractor


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--gpu", default="0")
    ap.add_argument("--extractors", default="extractor_2", help="逗号分隔提取器名")
    ap.add_argument("--th", type=float, default=0.004, help="DSSIM 阈值（low=0.004, mid=0.012, high=0.017）")
    ap.add_argument("--max-step", type=int, default=40, help="迭代步数（low=40, mid=75, high=150）")
    ap.add_argument("--lr", type=float, default=25)
    ap.add_argument("--sd", type=float, default=1e7)
    ap.add_argument("--format", default="jpg")
    ap.add_argument("--no-align", action="store_true")
    args = ap.parse_args()

    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu
    init_gpu(args.gpu)

    ex_names = [e.strip() for e in args.extractors.split(",") if e.strip()]
    extractors = [load_extractor(name) for name in ex_names]
    print(f"[cloak_api] extractors={ex_names} th={args.th} max_step={args.max_step} lr={args.lr}")

    from fawkes.align_face import aligner
    fk = Fawkes.__new__(Fawkes)
    fk.feature_extractors_ls = extractors
    fk.aligner = aligner()
    fk.th, fk.lr, fk.max_step = args.th, args.lr, args.max_step

    image_paths = sorted(glob.glob(os.path.join(args.dir, "*")))
    image_paths = [p for p in image_paths if "_cloaked" not in os.path.basename(p)]
    image_paths, loaded_images = filter_image_paths(image_paths)
    if not image_paths:
        print("no images")
        return

    faces = Faces(image_paths, loaded_images, fk.aligner, verbose=1, no_align=args.no_align)
    original_images = np.array(faces.cropped_faces)
    if len(original_images) == 0:
        print("no face detected")
        return

    protector = FawkesMaskGeneration(
        extractors, batch_size=1, mimic_img=True, intensity_range=PREPROCESS,
        initial_const=args.sd, learning_rate=args.lr, max_iterations=args.max_step,
        l_threshold=args.th, verbose=False, maximize=True, keep_final=False,
        image_shape=(IMG_SIZE, IMG_SIZE, 3), loss_method="features",
        tanh_process=True, save_last_on_failed=True,
    )
    protected = generate_cloak_images(protector, original_images)
    faces.cloaked_cropped_faces = protected
    final_images, images_without_face = faces.merge_faces(
        reverse_process_cloaked(protected, preprocess=PREPROCESS),
        reverse_process_cloaked(original_images, preprocess=PREPROCESS))

    from PIL import Image
    for i, p in enumerate(image_paths):
        if i in images_without_face:
            continue
        out = os.path.splitext(p)[0] + f"_cloaked.{args.format}"
        Image.fromarray((np.clip(final_images[i], 0, 255)).astype(np.uint8)).save(out, format="JPEG" if args.format == "jpg" else args.format.upper())
    print(f"[cloak_api] done {len(final_images)} images, without_face={len(images_without_face)}")


if __name__ == "__main__":
    main()
