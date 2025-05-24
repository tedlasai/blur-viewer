import cv2

# Input and output paths
input_path = "/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/webpage-sai/0045.png"
output_path = input_path  # overwrite, or change path to save elsewhere

# Load image
img = cv2.imread(input_path)
if img is None:
    raise IOError("Cannot load image.")

# Resize to 160x190 (width x height)
resized = cv2.resize(img, (160, 90), interpolation=cv2.INTER_AREA)

# Save resized image
cv2.imwrite(output_path, resized)
