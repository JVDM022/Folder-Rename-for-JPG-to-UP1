import os
import shutil
import re
import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal


class FileProcessor(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, src_dir, dest_dir):
        super().__init__()
        self.src_dir = src_dir
        self.dest_dir = dest_dir

    def run(self):
        if not os.path.exists(self.dest_dir):
            os.makedirs(self.dest_dir)

        main_folder = os.path.join(self.dest_dir, "main")
        extra_folder = os.path.join(self.dest_dir, "extra")

        os.makedirs(main_folder, exist_ok=True)
        os.makedirs(extra_folder, exist_ok=True)

        pattern = re.compile(r'(.+)_x(\d+)y(\d+)')
        files = sorted(os.listdir(self.src_dir))

        x_dist = {}
        y_counts = {}

        for filename in files:
            match = pattern.match(filename)
            if match:
                prefix, x_val, y_val = match.groups()
                x_val, y_val = int(x_val), int(y_val)

                if x_val not in x_dist:
                    x_dist[x_val] = len(x_dist)

                if x_val not in y_counts:
                    y_counts[x_val] = []
                y_counts[x_val].append(y_val)

        max_y = max(len(y_vals) for y_vals in y_counts.values())

        excel_data = []

        for filename in files:
            match = pattern.match(filename)
            if match:
                prefix, x_val, y_val = match.groups()
                x_val, y_val = int(x_val), int(y_val)

                new_x = x_dist[x_val]
                new_y = y_counts[x_val].index(y_val)
                new_filename = f"{prefix}_x{new_x}y{new_y}{os.path.splitext(filename)[1]}"

                src_path = os.path.join(self.src_dir, filename)
                if new_y < max_y:
                    dest_path = os.path.join(main_folder, new_filename)
                else:
                    dest_path = os.path.join(extra_folder, new_filename)

                shutil.copy2(src_path, dest_path)
                excel_data.append([prefix, x_val, y_val, new_x, new_y, dest_path])

            self.progress.emit(int((files.index(filename) + 1) / len(files) * 100))

        df = pd.DataFrame(excel_data, columns=["Prefix", "Old X", "Old Y", "New X", "New Y", "New Path"])
        df.to_excel(os.path.join(self.dest_dir, "file_mapping.xlsx"), index=False)

        self.finished.emit()


class FileOrganizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Select Source and Destination Folders", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.btn_select_src = QPushButton("Select Source Folder", self)
        self.btn_select_src.clicked.connect(self.select_source_folder)
        layout.addWidget(self.btn_select_src)

        self.btn_select_dest = QPushButton("Select Destination Folder", self)
        self.btn_select_dest.clicked.connect(self.select_destination_folder)
        layout.addWidget(self.btn_select_dest)

        self.btn_process = QPushButton("Start Processing", self)
        self.btn_process.clicked.connect(self.start_processing)
        layout.addWidget(self.btn_process)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.src_dir = ""
        self.dest_dir = ""

    def select_source_folder(self):
        self.src_dir = QFileDialog.getExistingDirectory(self, "Select Source Folder")

    def select_destination_folder(self):
        self.dest_dir = QFileDialog.getExistingDirectory(self, "Select Destination Folder")

    def start_processing(self):
        if self.src_dir and self.dest_dir:
            self.progress_bar.setValue(0)
            self.processor = FileProcessor(self.src_dir, self.dest_dir)
            self.processor.progress.connect(self.progress_bar.setValue)
            self.processor.finished.connect(self.on_processing_complete)
            self.processor.start()

    def on_processing_complete(self):
        self.label.setText("Processing Completed! Files Organized.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec())
