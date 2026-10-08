from pathlib import Path

from organizer import organize_directory


def main() -> None:
    target = input("Enter the path of the folder you want to organize: ").strip()
    target = target.strip('"').strip("'")

    try:
        result = organize_directory(Path(target))
    except (OSError, ValueError) as error:
        print(f"Error: {error}")
        return

    print(f"\nOrganizing files in: {result.directory}")
    for item in result.moves:
        print(f"Moved: {item.source.name} -> {item.category}/{item.destination.name}")
    print(f"\nOrganization complete! {len(result.moves)} file(s) moved.")


if __name__ == "__main__":
    main()
