import sys
from pathlib import Path
import shutil
import zipfile

CATEGORIES = {
    "Audio": [".mp3"],
    "Video": [".mp4"],
    "Docs": [".txt", ".docx", ".pdf"],
    "Images": [".jpg", ".png", ".gif"],
    "Archives": [".zip", ".rar"],
}

def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"

def move_file(file: Path, category: str, root_dir: Path) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
    new_file_path = target_dir.joinpath(file.name)
    if not new_file_path.exists():
        file.rename(new_file_path)
    else:
        # Handle duplicate file names by adding a unique identifier
        count = 1
        while True:
            new_name = f"{file.stem}_{count}{file.suffix}"
            new_file_path = target_dir.joinpath(new_name)
            if not new_file_path.exists():
                file.rename(new_file_path)
                break
            count += 1

def extract_archive(file: Path, extraction_dir: Path):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(extraction_dir)

def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        if item.is_file():
            category = get_categories(item)
            move_file(item, category, path)
        elif item.is_file() and item.stat().st_size == 0:
            item.unlink()

def main() -> str:
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
        
    if not path.exists():
        return "Folder does not exist"

    sort_folder(path)

    return "All done"

if __name__ == '__main__':
    print(main())
