import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Video parameters
width, height = 640, 480
text = "         This method doesn't  \n support future/past prediction."
num_frames = 16
output_path = "assets/extra_stuff/method_not_supported.mp4"
fps = 5

# Create a white background image with PIL
img = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(img)

# Load font
try:
    font = ImageFont.truetype("DejaVuSans.ttf", 400)
except IOError:
    font = ImageFont.load_default(32)

# Center text
bbox = draw.textbbox((0, 0), text, font=font)
text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
text_x = (width - text_width) / 2
text_y = (height - text_height) / 2
draw.text((text_x, text_y), text, fill='black', font=font, size=64)

# Convert to NumPy array (OpenCV format is BGR)
frame = np.array(img)
frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

# Initialize VideoWriter with H.264 codec (X264)
fourcc = cv2.VideoWriter_fourcc(*'avc1')  # or use 'X264' if available
video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Write the same frame repeatedly
for _ in range(num_frames):
    video_writer.write(frame)

# Release the video writer
video_writer.release()

print(f"Video written to {output_path}")