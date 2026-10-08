import tempfile
import unittest
from pathlib import Path

from organizer import organize_directory, plan_organization


class OrganizerTests(unittest.TestCase):
    def test_preview_categorizes_known_and_unknown_files(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            folder = Path(temporary_directory)
            (folder / "photo.PNG").touch()
            (folder / "notes.pdf").touch()
            (folder / "README").touch()

            directory, moves = plan_organization(folder)

            self.assertEqual(directory, folder.resolve())
            self.assertEqual(
                [(move.source.name, move.category) for move in moves],
                [("notes.pdf", "Documents"), ("photo.PNG", "Images"), ("README", "Others")],
            )
            self.assertTrue((folder / "photo.PNG").exists())

    def test_organizing_keeps_existing_destination_files(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            folder = Path(temporary_directory)
            images = folder / "Images"
            images.mkdir()
            (images / "photo.jpg").write_text("existing", encoding="utf-8")
            (folder / "photo.jpg").write_text("incoming", encoding="utf-8")

            result = organize_directory(folder)

            self.assertEqual(len(result.moves), 1)
            self.assertEqual(result.moves[0].destination.name, "photo (1).jpg")
            self.assertEqual((images / "photo.jpg").read_text(encoding="utf-8"), "existing")
            self.assertEqual((images / "photo (1).jpg").read_text(encoding="utf-8"), "incoming")

    def test_organizing_only_moves_top_level_files(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            folder = Path(temporary_directory)
            nested = folder / "nested"
            nested.mkdir()
            (nested / "inside.txt").touch()
            (folder / "top.txt").touch()

            result = organize_directory(folder)

            self.assertEqual([move.source.name for move in result.moves], ["top.txt"])
            self.assertTrue((nested / "inside.txt").exists())
            self.assertTrue((folder / "Documents" / "top.txt").exists())

    def test_invalid_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            file_path = Path(temporary_directory) / "file.txt"
            file_path.touch()

            with self.assertRaisesRegex(ValueError, "Choose a folder path"):
                plan_organization("")
            with self.assertRaisesRegex(ValueError, "does not exist"):
                plan_organization(file_path / "missing")
            with self.assertRaisesRegex(ValueError, "not a directory"):
                plan_organization(file_path)


if __name__ == "__main__":
    unittest.main()
