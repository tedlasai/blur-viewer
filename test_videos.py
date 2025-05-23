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


one_video = video_to_npy("/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/results/selected/in-the-wild/videos/165773_1x_Ours.mp4")
full_video = video_to_npy("/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/results/selected/full/videos/Adobe240-lower_fps_frames-720p_240fps_4-frame_00093_in0085_ie0101_os0077_oe0109_ctr0093_win0016_fps0120_2x.png_Ours.mp4")
gopro_video = video_to_npy("/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/results/selected/gopro/videos/GOPR0384_11_00_Jin.mp4")

print(one_video.shape)
print(full_video.shape)
print(gopro_video.shape)
