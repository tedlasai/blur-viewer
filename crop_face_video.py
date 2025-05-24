import cv2

# Input and output paths
input_path = "/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/webpage-sai/assets/pose/blurr_face_tracking.mp4"
output_path = "/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/webpage-sai/assets/pose/blurr_face_tracking_crop.mp4"

# Open the input video
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    raise IOError("Cannot open video")

# Get video properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H.264 codec

# Define thirds
third = width // 3
left_part = (0, third)
right_part = (2 * third, width)

# New width after removing center 1/3
new_width = width - third

# Create output video writer
out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Extract left and right thirds
    left = frame[:, left_part[0]:left_part[1]]
    right = frame[:, right_part[0]:right_part[1]]

    # Concatenate horizontally
    combined = cv2.hconcat([left, right])
    out.write(combined)

# Release resources
cap.release()
out.release()
