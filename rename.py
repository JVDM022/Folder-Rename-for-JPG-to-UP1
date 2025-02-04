import os
import shutil
import re

#check - A
#sort files - B
#set variables like for mapping -C
#go through every files-D
#rename and copy files -E

def rename_and_copy_files(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    # A

    pattern = re.compile(r'{prefix}_x(\d+)y(\d+)')
    files = sorted (os.listdir(src_dir))
    # B

    x_dist = 0
    x_counter = {}
    prev_x_val = None
    y_counter = 0
    # C

    for filename in files:
        match = pattern.match(filename)
        if match:
            x_val, y_val = match.groups()
            x_val = int(x_val)
            y_val = int(y_val)

            if x_val not in x_dist:
                x_dist[x_val] =  x_counter
                x_counter += 1 
                # D1
                y_counter = 0
            
            new_x = x_dist[x_val]
            new_y = y_counter
            y_counter += 1

            new_filename = f'{new_x}_x{new_y}y{os.path.splitext(filename)[1]}'
            # D

            src_path = os.path.join(src_dir, filename)
            dest_path = os.path.join(dest_dir, new_filename)

            shutil.copy2(src_path, dest_path)
            # E
            print(f"Copied and renamed {src_path} -> {dest_path}")

        print("Done")

src_dir = input("Enter the source directory: ")
dest_dir = input("Enter the destination directory: ")
prefix = input("Enter the prefix: ")

rename_and_copy_files(src_dir, dest_dir, prefix)

