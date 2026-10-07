import os
import shutil
from pathlib import Path

# Define the folder categories and their corresponding extensions
DIRECTORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Code": [".py", ".html", ".css", ".js", ".json", ".cpp", ".java"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"]
}

def organize_folder(target_dir):
    path = Path(target_dir)
    
    if not path.exists():
        print(f"Error: The directory '{target_dir}' does not exist.")
        return

    print(f"\nOrganizing files in: {path.absolute()}")
    
    # Iterate through all items in the target directory
    for item in path.iterdir():
        if item.is_file():
            file_extension = item.suffix.lower()
            moved = False
            
            # Check which category the file extension belongs to
            for folder_name, extensions in DIRECTORIES.items():
                if file_extension in extensions:
                    dest_folder = path / folder_name
                    dest_folder.mkdir(exist_ok=True)
                    shutil.move(str(item), str(dest_folder / item.name))
                    print(f"Moved: {item.name} -> {folder_name}/")
                    moved = True
                    break
            
            # If extension doesn't match any category, move to 'Others'
            if not moved:
                other_folder = path / "Others"
                other_folder.mkdir(exist_ok=True)
                shutil.move(str(item), str(other_folder / item.name))
                print(f"Moved: {item.name} -> Others/")

    print("\n✨ Organization complete!")

if __name__ == "__main__":
    target = input("Enter the path of the folder you want to organize: ").strip()
    # Remove quotes if the user dragged and dropped the folder into the terminal
    target = target.strip('"').strip("'")
    organize_folder(target)
