import cv2
import os
import glob

def downsample_pngs_half_resolution(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    png_files = glob.glob(os.path.join(input_dir, "*.png"))

    for file_path in png_files:
        print(f"Processing {file_path}")
        img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)  # Preserve alpha channel if present
        if img is None:
            print(f"Warning: Could not read {file_path}")
            continue

        height, width = img.shape[:2]
        resized_img = cv2.resize(img, (width // 2, height // 2), interpolation=cv2.INTER_AREA)

        filename = os.path.basename(file_path)
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, resized_img)

# Example usage
input_path = "/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/webpage-sai/rearrange_assets/allwild/blurry"
output_path = os.path.join(input_path, "../blurry_ds")
os.makedirs(output_path, exist_ok=True)
downsample_pngs_half_resolution(input_path, output_path)
