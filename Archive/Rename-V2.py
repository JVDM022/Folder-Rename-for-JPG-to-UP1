import os
import shutil
import re
import tkinter as tk
from tkinter import filedialog

def rename_and_copy_files(src_dir, dest_dir, new_name):
    # create a folder for reuslts
    final_dest_folder = os.path.join(dest_dir, new_name)
    if not os.path.exists(final_dest_folder):
        os.makedirs(final_dest_folder)

    # extract x and y values from filenames
    pattern = re.compile(r'(.+)_x(\d+)y(\d+)')  

    files = sorted(os.listdir(src_dir))

    x_dist = {}  # Map x value
    x_counter = 0
    y_counters = {}  # tie y to x

    for filename in files:
        match = pattern.match(filename)
        if match:
            prefix, x_val, y_val = match.groups()
            x_val, y_val = int(x_val), int(y_val)

            if x_val not in x_dist:
                x_dist[x_val] = x_counter
                x_counter += 1
                y_counters[x_val] = 0  # Reset y counter for new x value

            new_x = x_dist[x_val]
            new_y = y_counters[x_val]
            y_counters[x_val] += 1

            ext = os.path.splitext(filename)[1]  # Preserve original extension
            new_filename = f"{prefix}_x{new_x}y{new_y}{ext}"

            src_path = os.path.join(src_dir, filename)
            dest_path = os.path.join(final_dest_folder, new_filename)

            shutil.copy2(src_path, dest_path)
            print(f"Copied and renamed {src_path} -> {dest_path}")

    print("✅ Done! Files copied to:", final_dest_folder)


def select_folder(title):
    root=tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title=title)
    return folder_selected

src_dir = select_folder("Select the source directory")
dest_dir = select_folder("Select the destination directory")
new_dest_name = input("Enter the new destination folder name: ")

rename_and_copy_files(src_dir, dest_dir, new_dest_name)