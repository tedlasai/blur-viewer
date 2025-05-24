import shutil
from pathlib import Path

# Define source and destination directories
src_dir = Path("/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/webpage-sai")
dst_dir = Path("/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/webpage-supplemental")

# Ensure the destination directory exists
dst_dir.mkdir(parents=True, exist_ok=True)

# List of files and folders to copy
items_to_copy = [
    "assets",
    "js",
    "static",
    "ReadMe.txt",
    "index.html",
]

# Copy each item
for item in items_to_copy:
    src_path = src_dir / item
    dst_path = dst_dir / item

    if src_path.is_dir():
        if dst_path.exists():
            shutil.rmtree(dst_path)  # Remove if already exists to avoid merge conflicts
        shutil.copytree(src_path, dst_path)
        print(f"Copied folder: {item}")
    elif src_path.is_file():
        shutil.copy2(src_path, dst_path)
        print(f"Copied file: {item}")
    else:
        print(f"Missing: {item}")
