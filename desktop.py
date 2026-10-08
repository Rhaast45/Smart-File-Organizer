import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from organizer import OrganizationResult, PlannedMove, organize_directory, plan_organization


class FileOrganizerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Smart File Organizer")
        self.root.geometry("850x650")
        self.root.minsize(680, 500)
        self.root.configure(background="#f4f7f5")

        self.folder_path = tk.StringVar()
        self.status_text = tk.StringVar(value="Choose a folder, then preview or organize its files.")
        self.preview_moves: tuple[PlannedMove, ...] = ()
        self.preview_directory: Path | None = None
        self.folder_path.trace_add("write", self._folder_path_changed)

        self._configure_styles()
        self._build_interface()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background="#f4f7f5")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("TLabel", background="#f4f7f5", foreground="#1c2923", font=("Segoe UI", 10))
        style.configure("Card.TLabel", background="#ffffff", foreground="#1c2923", font=("Segoe UI", 10))
        style.configure("Title.TLabel", background="#f4f7f5", foreground="#17251e", font=("Segoe UI", 28, "bold"))
        style.configure("Subtitle.TLabel", background="#f4f7f5", foreground="#65736b", font=("Segoe UI", 11))
        style.configure("Section.TLabel", background="#ffffff", foreground="#1c2923", font=("Segoe UI", 14, "bold"))
        style.configure("Muted.Card.TLabel", background="#ffffff", foreground="#718078", font=("Segoe UI", 9))
        style.configure("TButton", font=("Segoe UI", 10), padding=(12, 8))
        style.configure("Primary.TButton", background="#248369", foreground="#ffffff", font=("Segoe UI", 10, "bold"))
        style.map("Primary.TButton", background=[("active", "#176c55"), ("disabled", "#a8b9b0")])
        style.configure("Treeview", rowheight=31, font=("Segoe UI", 9), background="#ffffff", fieldbackground="#ffffff")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#f1f5f2")

    def _build_interface(self) -> None:
        outer = ttk.Frame(self.root, padding=(34, 25, 34, 22))
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, 20))
        ttk.Label(header, text="SORTLY", foreground="#248369", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ttk.Label(header, text="A calmer place for all your files.", style="Title.TLabel").pack(anchor="w", pady=(4, 3))
        ttk.Label(
            header,
            text="Pick a folder, review the plan, and let your files find their place.",
            style="Subtitle.TLabel",
        ).pack(anchor="w")

        card = ttk.Frame(outer, style="Card.TFrame", padding=20)
        card.pack(fill="both", expand=True)
        ttk.Label(card, text="Choose a folder", style="Section.TLabel").pack(anchor="w")
        ttk.Label(
            card,
            text="Only files directly inside this folder are organized. Existing files are never overwritten.",
            style="Muted.Card.TLabel",
        ).pack(anchor="w", pady=(4, 15))

        path_row = ttk.Frame(card, style="Card.TFrame")
        path_row.pack(fill="x")
        path_entry = ttk.Entry(path_row, textvariable=self.folder_path, font=("Segoe UI", 10))
        path_entry.pack(side="left", fill="x", expand=True, ipady=7)
        path_entry.bind("<Return>", lambda _event: self.preview())
        ttk.Button(path_row, text="Browse…", command=self.browse).pack(side="left", padx=(9, 0))
        ttk.Button(path_row, text="Preview files", style="Primary.TButton", command=self.preview).pack(
            side="left", padx=(8, 0)
        )

        self.tree = ttk.Treeview(card, columns=("file", "category", "destination"), show="headings", height=3)
        self.tree.heading("file", text="FILE")
        self.tree.heading("category", text="CATEGORY")
        self.tree.heading("destination", text="DESTINATION")
        self.tree.column("file", width=250, minwidth=120)
        self.tree.column("category", width=120, minwidth=90)
        self.tree.column("destination", width=300, minwidth=150)
        self.tree.pack(fill="both", expand=True, pady=(17, 11))

        footer = ttk.Frame(card, style="Card.TFrame")
        footer.pack(fill="x")
        ttk.Label(footer, textvariable=self.status_text, style="Muted.Card.TLabel").pack(side="left", anchor="w")
        self.organize_button = ttk.Button(
            footer,
            text="Organize files",
            style="Primary.TButton",
            command=self.organize,
        )
        self.organize_button.pack(side="right")

        ttk.Label(
            outer,
            text="Private by design · Your files stay on this computer",
            foreground="#77847c",
            font=("Segoe UI", 9),
        ).pack(pady=(13, 0))

    def browse(self) -> None:
        selected = filedialog.askdirectory(title="Choose a folder to organize")
        if selected:
            self.folder_path.set(selected)
            self.preview()

    def _folder_path_changed(self, *_args: str) -> None:
        if self.preview_directory is not None:
            self._clear_preview()

    def preview(self) -> None:
        try:
            directory, moves = plan_organization(self.folder_path.get())
        except (OSError, ValueError) as error:
            self._clear_preview()
            messagebox.showerror("Cannot preview folder", str(error), parent=self.root)
            return

        self.preview_directory = directory
        self.preview_moves = moves
        self._populate_rows(moves)
        self.status_text.set(
            f"{len(moves)} file(s) ready to organize."
            if moves
            else "No files found directly inside this folder. Subfolders are not scanned."
        )

    def organize(self) -> None:
        try:
            directory, moves = plan_organization(self.folder_path.get())
        except (OSError, ValueError) as error:
            self._clear_preview()
            messagebox.showerror("Cannot organize folder", str(error), parent=self.root)
            return

        self.preview_directory = directory
        self.preview_moves = moves
        self._populate_rows(moves)
        if not moves:
            self.status_text.set("No files found directly inside this folder. Subfolders are not scanned.")
            messagebox.showinfo(
                "No files to organize",
                "There are no files directly inside this folder. Choose a folder that contains files; "
                "files inside subfolders are not scanned.",
                parent=self.root,
            )
            return

        count = len(moves)
        confirmed = messagebox.askyesno(
            "Confirm organization",
            f"Move {count} file(s) into category folders in:\n\n{directory}?",
            parent=self.root,
        )
        if not confirmed:
            return

        try:
            result = organize_directory(directory)
        except (OSError, ValueError) as error:
            messagebox.showerror("Organization failed", str(error), parent=self.root)
            self.preview()
            return

        self._show_completed(result)

    def _populate_rows(self, moves: tuple[PlannedMove, ...]) -> None:
        self._clear_rows()
        for move in moves:
            self.tree.insert("", "end", values=(move.source.name, move.category, move.destination.name))

    def _show_completed(self, result: OrganizationResult) -> None:
        self._populate_rows(result.moves)
        self.status_text.set(
            f"Done! Organized {len(result.moves)} file(s). "
            "Select Organize files again to check this folder for new files."
        )
        self.preview_moves = ()
        self.preview_directory = None
        messagebox.showinfo(
            "Organization complete",
            f"Successfully organized {len(result.moves)} file(s).",
            parent=self.root,
        )

    def _clear_rows(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)

    def _clear_preview(self) -> None:
        self._clear_rows()
        self.preview_moves = ()
        self.preview_directory = None
        self.status_text.set("Choose a folder, then preview or organize its files.")


def main() -> None:
    root = tk.Tk()
    FileOrganizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
