import os
import shutil
import re

def rename_and_copy_files(src_dir, dest_dir, prefix, new_dest_name):
    # Create renamed destination folder inside dest_dir
    final_dest_folder = os.path.join(dest_dir, new_dest_name)
    if not os.path.exists(final_dest_folder):
        os.makedirs(final_dest_folder)

    # Compile regex pattern dynamically based on the prefix
    pattern = re.compile(rf'{re.escape(prefix)}_x(\d+)y(\d+)')

    files = sorted(os.listdir(src_dir))

    x_dist = {}  # Dictionary to map old x values to new ones
    x_counter = 0
    y_counters = {}  # Separate y counter for each x value

    for filename in files:
        match = pattern.match(filename)
        if match:
            x_val, y_val = map(int, match.groups())

            if x_val not in x_dist:
                x_dist[x_val] = x_counter
                x_counter += 1
                y_counters[x_val] = 0  # Reset y counter for new x value

            new_x = x_dist[x_val]
            new_y = y_counters[x_val]
            y_counters[x_val] += 1

            ext = os.path.splitext(filename)[1]  # Preserve original extension
            new_filename = f"{new_x}_x{new_y}{ext}"

            src_path = os.path.join(src_dir, filename)
            dest_path = os.path.join(final_dest_folder, new_filename)

            shutil.copy2(src_path, dest_path)
            print(f"Copied and renamed {src_path} -> {dest_path}")

    print("✅ Done! Files copied to:", final_dest_folder)

# User input
src_dir = input("Enter the source directory: ")
dest_dir = input("Enter the destination directory: ")
new_dest_name = input("Enter the new destination folder name: ")

rename_and_copy_files(src_dir, dest_dir, prefix, new_dest_name)