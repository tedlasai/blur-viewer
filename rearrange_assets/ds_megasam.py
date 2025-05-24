import cv2
import os

input_root = "/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/webpage-sai/rearrange_assets/allwild/megasam"
output_root = input_root + "_ds"

valid_extensions = ('.mp4', '.mov', '.avi', '.mkv')

for root, _, files in os.walk(input_root):
    for file in files:
        if file.lower().endswith(valid_extensions):
            input_path = os.path.join(root, file)

            # Construct output path
            rel_path = os.path.relpath(root, input_root)
            output_dir = os.path.join(output_root, rel_path)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, file)

            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                print(f"Error opening video: {input_path}")
                continue

            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) // 2
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) // 2
            fps = cap.get(cv2.CAP_PROP_FPS)

            # Try H.264 encoding
            fourcc = cv2.VideoWriter_fourcc(*'avc1')  # Change to 'H264' if needed
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_resized = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
                out.write(frame_resized)

            cap.release()
            out.release()
            print(f"Saved downsampled video: {output_path}")

print("All videos downsampled recursively.")
