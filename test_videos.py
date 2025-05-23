import cv2

import numpy as np

def video_to_npy(video_path, resize_to=None, max_frames=None):
    """
    Reads a video file and saves the frames as a NumPy array (.npy).
    
    Args:
        video_path (str): Path to the input video file.
        output_npy_path (str): Path where the .npy array will be saved.
        resize_to (tuple or None): (width, height) to resize each frame. Set to None to keep original size.
        max_frames (int or None): Maximum number of frames to read. Set to None to read entire video.
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or (max_frames is not None and count >= max_frames):
            break
        if resize_to:
            frame = cv2.resize(frame, resize_to)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        frames.append(frame)
        count += 1

    cap.release()
    frames_np = np.array(frames)
    return frames_np


gopro_video = video_to_npy("/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/results/selected/in-the-wild/videos/14810348233_2dda2cb3a7_o_1x_Jin.mp4")


print(gopro_video.shape)
