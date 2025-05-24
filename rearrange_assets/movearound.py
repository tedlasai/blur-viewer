import os
import shutil

# Input: mapping of group names to list of indices


limitations = [0, 2, 8]
historical = [36, 39, 43, 42, 41, 27, 29, 30,33]
all_scenes = [44, 12, 10, 3, 24, 40, 16, 21, 35, 28]
# add any numbers between 0 and 46 that are not in limitations or historical to all_scenes
for i in range(45):
    if i not in limitations and i not in historical and i not in all_scenes:
        all_scenes.append(i)

group_dict = {
    "limitations": limitations,
    "historical": historical,
    "wild": all_scenes,
}

# Base directory setup
base_dir = "/Users/saitedla/Dropbox/Documents/School/UofT/MotionBlur/Paper/figures/webpage-sai/rearrange_assets/allwild"
output_root = os.path.join(base_dir, "..")

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

        # Blurry - pastfuture
        src = os.path.join(base_dir, "blurry", f"{old_str}_pastfuture.png")
        dst = os.path.join(group_out, "blurry", f"{new_str}_pastfuture.png")
        shutil.copy(src, dst)

        # Blurry - present
        src = os.path.join(base_dir, "blurry", f"{old_str}_present.png")
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


        
        src_megasam = os.path.join(base_dir, "megasam", old_str)
        dst_megasam = os.path.join(group_out, "megasam", new_str)
        copy_all_subfolders(src_megasam, dst_megasam)

   
print("All groups processed successfully.")
