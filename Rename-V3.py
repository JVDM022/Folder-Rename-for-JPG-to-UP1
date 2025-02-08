import os
import shutil
import re
import tkinter as tk
from tkinter import filedialog

def rename_and_copy_files(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    pattern = re.compile(r'(.+)_x(\d+)y(\d+)')
    files = sorted(os.listdir(src_dir))

    x_dist = {}
    y_counters = {}

    for filename in files:
        match = pattern.match(filename)
        if match:
            prefix, x_val, y_val = match.groups()
            x_val = int(x_val)
            y_val = int(y_val)

            if x_val not in x_dist:
                x_dist[x_val] = len(x_dist)
                y_counters[x_val] = 0

            new_x = x_dist[x_val]
            new_y = y_counters[x_val]
            y_counters[x_val] += 1

            new_filename = f"{prefix}_x{new_x}y{new_y}{os.path.splitext(filename)[1]}"

            src_path = os.path.join(src_dir, filename)
            dest_path = os.path.join(dest_dir, new_filename)

            shutil.copy2(src_path, dest_path)
            print(f"Copied and renamed {src_path} -> {dest_path}")

    print("✅ Done processing files!")

def organize_files(src_dir, dest_dir):
    # Create the folder
    final_dest_folder = os.path.join(dest_dir, "sorted_files")
    main_folder = os.path.join(final_dest_folder, "main")
    extra_folder = os.path.join(final_dest_folder, "extra")

    if not os.path.exists(final_dest_folder):
        os.makedirs(final_dest_folder)
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
    if not os.path.exists(extra_folder):
        os.makedirs(extra_folder)
    # Sort
    pattern = re.compile(r'(.+)_x(\d+)y(\d+)')
    files = sorted(os.listdir(src_dir))

    x_groups = {}
    for filename in files:
        match = pattern.match(filename)
        if match:
            prefix, x_val, y_val = match.groups()
            x_val, y_val = int(x_val), int(y_val)
            x_groups.setdefault(x_val, []).append((prefix, x_val, y_val, filename))

    min_y_count = min(len(files) for files in x_groups.values())

    for x_val, file_list in x_groups.items():
        file_list.sort(key=lambda x: x[2])
        main_files = file_list[:min_y_count]
        extra_files = file_list[min_y_count:]

        for file_info in main_files:
            src_path = os.path.join(src_dir, file_info[3])
            dest_path = os.path.join(main_folder, file_info[3])
            shutil.copy2(src_path, dest_path)

        for file_info in extra_files:
            src_path = os.path.join(src_dir, file_info[3])
            dest_path = os.path.join(extra_folder, file_info[3])
            shutil.copy2(src_path, dest_path)

    print(f"✅ Files sorted into '{main_folder}' and '{extra_folder}'.")

def select_folder(title):
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title=title)

# Human input
src_dir = select_folder("Select Source Directory")
if not src_dir:
    print("No source directory selected. Exiting...")
    exit()

dest_dir = select_folder("Select Destination Directory")
if not dest_dir:
    print("No destination directory selected. Exiting...")
    exit()

# Call the functions
rename_and_copy_files(src_dir, dest_dir)
organize_files(dest_dir, dest_dir)
