import os
import shutil
import cv2
# Input: mapping of group names to list of indices

import subprocess

# Base directory setup
base_dir = "/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/webpage-sai/rearrange_assets/allwild"
output_root = os.path.join(base_dir, "..")



#downsample all videos in the megasam folder to 720p and store in megasam_ds/



#downsample megasam at the beginning
# group_megasam = os.path.join(base_dir, "megasam")
# group_megasam_ds = os.path.join(base_dir,"megasam_ds")

# print(f"Processing directory: {group_megasam}")
# for root, _, files in os.walk(group_megasam):
#     print(f"Processing directory: {root}")
#     for file in files:
#         if file.endswith(".mp4"):
#             rel_path = os.path.relpath(os.path.join(root, file), group_megasam)
#             output_path = os.path.join(group_megasam_ds, rel_path)
#             input_path = os.path.join(root, file)
#             downsample_video_to_720p(input_path, output_path, scale_factor = 0.5)


limitations = [0, 2, 8]
historical = [36, 39, 43, 42, 41, 27, 29, 30,33]
special_scenes = [44, 12, 24, 40, 16, 21, 35, 10, 45]
megasam_scenes = [36, 39, 43, 42, 41, 27, 29, 30, 33, 44, 12, 24, 40, 16, 21, 35]
remove_scene = [15, 28]
all_scenes = special_scenes.copy()
# add any numbers between 0 and 46 that are not in limitations or historical to all_scenes
for i in range(45):
    if i not in limitations and i not in historical and i not in special_scenes and i not in remove_scene:
        all_scenes.append(i)

group_dict = {
    "limitations": limitations,
    "historical": historical,
    "wild": all_scenes,
}


# Helper to copy all subfolders from one index
def copy_all_subfolders(src_root, dst_root):
    if not os.path.exists(src_root):
        print(f"Warning: {src_root} does not exist.")
        return
    for subdir in os.listdir(src_root):
        src_sub = os.path.join(src_root, subdir)
        if os.path.isdir(src_sub):
            dst_sub = os.path.join(dst_root, subdir)
            os.makedirs(dst_sub, exist_ok=True)
            for file in os.listdir(src_sub):
                shutil.copy(os.path.join(src_sub, file), os.path.join(dst_sub, file))

# Process each group
for group_name, indices in group_dict.items():
    group_out = os.path.join(output_root, group_name)

    # Create blurry/icons folders
    os.makedirs(os.path.join(group_out, "blurry"), exist_ok=True)
    os.makedirs(os.path.join(group_out, "icons"), exist_ok=True)

    for new_idx, old_idx in enumerate(indices):
        old_str = f"{old_idx:04d}"
        new_str = f"{new_idx:04d}"

        # Blurry - present (only need present since pastfuture is not used)
        src = os.path.join(base_dir, "blurry_ds", f"{old_str}_present.png")
        dst = os.path.join(group_out, "blurry", f"{new_str}_present.png")
        shutil.copy(src, dst)

        # Icons
        src = os.path.join(base_dir, "icons", f"{old_str}.png")
        dst = os.path.join(group_out, "icons", f"{new_str}.png")
        shutil.copy(src, dst)

        # Tracks
        src_tracks = os.path.join(base_dir, "tracks", old_str)
        dst_tracks = os.path.join(group_out, "tracks", new_str)
        copy_all_subfolders(src_tracks, dst_tracks)

        # Videos
        src_videos = os.path.join(base_dir, "videos", old_str)
        dst_videos = os.path.join(group_out, "videos", new_str)
        copy_all_subfolders(src_videos, dst_videos)

        fallback_mp4 = os.path.join(base_dir, "..", "megasam_not_converged.mp4")


        
        src_megasam = os.path.join(base_dir, "megasam_ds", old_str)
        src_megasam_poses = os.path.join(base_dir, "megasam_poses_rotated", old_str) #use rotated poses
        dst_megasam = os.path.join(group_out, "megasam", new_str)
        dst_megasam_poses = os.path.join(group_out, "megasam_poses", new_str)
        os.makedirs(dst_megasam, exist_ok=True)

        if old_idx in megasam_scenes:
            print(f"Processing directory: {src_megasam}")
            #copy_all_subfolders(os.path.join(src_megasam, "pastfuture"), os.path.join(dst_megasam, "pastfuture"))
            os.makedirs(os.path.join(dst_megasam, "pastfuture"), exist_ok=True)
            os.makedirs(os.path.join(dst_megasam_poses, "pastfuture"), exist_ok=True)
            shutil.copy(os.path.join(src_megasam, "pastfuture", "Ours.mp4"), os.path.join(dst_megasam, "pastfuture", "Ours.mp4"))
            if (os.path.exists(os.path.join(src_megasam_poses, "pastfuture", "Ours.mp4"))):
                shutil.copy(os.path.join(src_megasam_poses, "pastfuture", "Ours.mp4"), os.path.join(dst_megasam_poses, "pastfuture", "Ours.mp4"))
        else:
            os.makedirs(os.path.join(dst_megasam, "pastfuture"), exist_ok=True)
            shutil.copy("/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/webpage-sai/rearrange_assets/nomegasam.mp4", os.path.join(dst_megasam, "pastfuture/Ours.mp4"))
            #shutil.copy("/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/webpage-sai/rearrange_assets/nomegasam.mp4", os.path.join(dst_megasam, "pastfuture/Ours.mp4"))

print("All groups processed successfully.")
