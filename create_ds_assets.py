import os
import shutil
from PIL import Image
import cv2

from pathlib import Path

# Base paths
src_base = Path("/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/webpage-sai/assets")
dst_base = src_base.parent / "ds_assets"

# Subdirectories to downsample
to_downsample = {"historical", "wild", "simulated", "limitations"}
target_size = (640, 360)

def resize_image(src_path, dst_path):
    img = Image.open(src_path)
    img = img.resize(target_size, Image.Resampling.LANCZOS)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst_path)

def resize_video(src_path, dst_path):
    dst_path.parent.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(src_path))
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(str(dst_path), fourcc, cap.get(cv2.CAP_PROP_FPS), target_size)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_resized = cv2.resize(frame, target_size)
        out.write(frame_resized)

    cap.release()
    out.release()

def process():
    for root, dirs, files in os.walk(src_base):
        rel_root = Path(root).relative_to(src_base)
        subdir_name = rel_root.parts[0] if rel_root.parts else ""

        if subdir_name in to_downsample:
            for file in files:
                src_file = Path(root) / file
                dst_file = dst_base / rel_root / file

                if file.lower().endswith(".png"):
                    print(f"Resizing image: {src_file}")
                    resize_image(src_file, dst_file)
                elif file.lower().endswith(".mp4"):
                    print(f"Resizing video: {src_file}")
                    resize_video(src_file, dst_file)
        else:
            # Copy everything else as-is
            src_dir = Path(root)
            dst_dir = dst_base / rel_root
            if not dst_dir.exists():
                shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)

if __name__ == "__main__":
    process()
