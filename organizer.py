import shutil
from dataclasses import dataclass
from pathlib import Path


DIRECTORIES: dict[str, tuple[str, ...]] = {
    "Images": (".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"),
    "Documents": (".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"),
    "Code": (".py", ".html", ".css", ".js", ".json", ".cpp", ".java"),
    "Archives": (".zip", ".rar", ".tar", ".gz"),
    "Videos": (".mp4", ".mkv", ".avi", ".mov"),
}


@dataclass(frozen=True)
class PlannedMove:
    source: Path
    destination: Path
    category: str


@dataclass(frozen=True)
class OrganizationResult:
    directory: Path
    moves: tuple[PlannedMove, ...]


def _category_for(file_path: Path) -> str:
    extension = file_path.suffix.lower()
    for category, extensions in DIRECTORIES.items():
        if extension in extensions:
            return category
    return "Others"


def _available_destination(folder: Path, filename: str) -> Path:
    destination = folder / filename
    if not destination.exists():
        return destination

    source = Path(filename)
    stem, suffix = source.stem, source.suffix
    counter = 1
    while True:
        destination = folder / f"{stem} ({counter}){suffix}"
        if not destination.exists():
            return destination
        counter += 1


def plan_organization(target_dir: str | Path) -> tuple[Path, tuple[PlannedMove, ...]]:
    if not str(target_dir).strip():
        raise ValueError("Choose a folder path.")

    directory = Path(target_dir).expanduser()
    if not directory.exists():
        raise ValueError(f"The directory '{directory}' does not exist.")
    if not directory.is_dir():
        raise ValueError(f"'{directory}' is not a directory.")

    moves = []
    for item in sorted(directory.iterdir(), key=lambda path: path.name.casefold()):
        if item.is_file():
            category = _category_for(item)
            destination_folder = directory / category
            destination = _available_destination(destination_folder, item.name)
            moves.append(PlannedMove(item, destination, category))

    return directory.resolve(), tuple(moves)


def organize_directory(target_dir: str | Path) -> OrganizationResult:
    directory, moves = plan_organization(target_dir)
    for move in moves:
        move.destination.parent.mkdir(exist_ok=True)
        shutil.move(str(move.source), str(move.destination))
    return OrganizationResult(directory, moves)
