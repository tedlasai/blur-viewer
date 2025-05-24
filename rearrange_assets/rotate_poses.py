import cv2
import os
import re

input_root = "/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/webpage-sai/rearrange_assets/allwild/megasam_poses"
output_root = "/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/webpage-sai/rearrange_assets/allwild/megasam_poses_rotated"

special_scenes = ["0010", "0036", "0041", "0042"]


for dirpath, _, filenames in os.walk(input_root):
    for filename in filenames:
        if filename.endswith(".mp4"):
            #check if the special_scenes are in the filename
            for scene in special_scenes:
                if re.search(rf"{scene}", dirpath):
                    print(f"Skipping {dirpath} as it is a special scene.")
                    break


            input_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(dirpath, input_root)
            output_dir = os.path.join(output_root, relative_path)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, filename)

            cap = cv2.VideoCapture(input_path)
            fourcc = cv2.VideoWriter_fourcc(*'avc1')
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            print(f"Flipping vertically and horizontally: {input_path}")

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                flipped = cv2.flip(frame, -1)  # -1 = both axes
                out.write(flipped)

            cap.release()
            out.release()
