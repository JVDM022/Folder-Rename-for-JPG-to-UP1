# Project README

## Version Updates

### **V2 (Latest Version)**
- **Status**: The executable (exe) file is functioning properly.
- **Known Bug**:
  - Due to SEM generating an uneven number of y-values, repack files may experience glitches.
  - **Temporary Solution**: Manually remove certain patterns to ensure even x and y values. For example, ensure that all the maximum y-values for each x-value are the same (e.g., `x1y100`, `x2y100`, `x3y100`, etc.).

---

### **V1 (Archived Version)**
- **Status**: The program is functioning properly.
- **Drawback**: Requires manual input for the folder path.
- **Note**: V1 is now archived and no longer actively maintained.

---

### **V3 (Projected Long-term Solution)**
- **Current Work**: Source code has been already released, releasing the exe file soon.
- **Updates/Features**: Sort the file into main and extra folders.

---

## Roadmap

### ✅ **Completed**
- Implemented an executable (V2).
- Added automatic folder selection (GUI).
- Organized files into `main` and `extra` folders.

### 🔄 **In Progress**
- Releasing the executable for **V3**.
- Improving **file organization** to prevent repack software-induced glitches.
- Enhancing **error handling** for unexpected file patterns, including dynamically recognize the file format.

### 🚀 **Planned Features**
-**V3.1**
- **Automated Bug Fixing**: Script will auto-adjust SEM uneven values.
- **Better UI/UX**: User-friendly interface for non-technical users.
- **Multi-threading Optimization**: Faster processing for large datasets.
- **Porogress Bar for Large Folders**: Progress bar for copying/moving thousands of files in a folder.
- **Excel**: Add Excel files for the all jpg files
- **V3.2**
- **Optimization**: Further optmiziation
- **save configuration**: store user preferences.
- **Multithreading optimized**: Parallelize File Operations with Asynchronous Processing
- **Undo/Restore**:  Create a log of files, and allow an undo operation.
- **Independent exe**: Convert into a Fully Functional Windows EXE with GUI
- **V3.3**
- **Memory Optimization**: Use efficient data structures to handle large datasets better
- **Batch Processing**: Allow processing multiple folders in one go.
---

## How to Use

1. Download the **V2 exe** file and run it locally.
2. Follow the steps outlined in the *Temporary Solution* if you encounter any bugs.

---
