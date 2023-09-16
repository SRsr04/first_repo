import sys
from pathlib import Path

CATEGORIES = {"Audio": [".mp3"],
              "Video": [".mp4"],
              "Docs": [".txt", ".docx", ".pdf"]
              }

def get_categories(file:Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"

def move_file(file: Path, category: str, root_dir: Path) -> None:
    target_dir = root_dir.joinpath(category)
    print (target_dir.exists())
    if not target_dir.exists():
        target_dir.mkdir()
    file.rename(target_dir.joinpath(file.name))
    


def sort_folder(path:Path) -> None:
    for item in path.glob("**/*"):
        if item.is_file():
            category = get_categories(item)
            move_file(item, category, path)

    for item in path.glob("**/*"):
        if item.is_file() and item.stat().st_size == 0:
            item.unlink()

def main() -> str:
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
        
    if not path.exists():
        return "Folder does not exists"


    sort_folder(path)

    return "All right"

    
if __name__ == '__main__':
    print(main())