# Smart File Organizer 📂

A simple yet powerful Python automation script that cleans up messy directories (like your Downloads or Desktop) by automatically sorting files into categorized folders (`Images`, `Documents`, `Code`, `Archives`, `Videos`, and `Others`).

## Features
* **Zero Dependencies:** Uses only Python built-in modules (`os`, `shutil`, `pathlib`).
* **Safe Sorting:** Automatically creates destination folders only if they are needed.
* **Catch-All Handling:** Unrecognized file types are safely moved to an `Others` folder.

## How to Run
1. Make sure you have [Python](https://www.python.org/) installed.
2. Clone or download this repository.
3. Run the script from your terminal:
   ```bash
   python main.py
