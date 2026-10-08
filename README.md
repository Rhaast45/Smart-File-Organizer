# Smart File Organizer

A native Windows desktop file organizer. Choose a folder, preview the proposed moves, and organize files into `Images`, `Documents`, `Code`, `Archives`, `Videos`, or `Others` — without opening a browser.

## Download here:

-[Click here to download ](https://mega.nz/file/iAVzBIQJ#JVckngmvrXPCcEJhcYlhOdnXSXLdRMM-3EmMBumA6rw)

## Links

- [Facebook](https://www.facebook.com/RTNeru)
- [linkedin](https://www.linkedin.com/in/michael-ortinero-a59b30427/)
- [GitHub](https://github.com/Rhaast45)

## Features

- Browse for a folder and preview the top-level files and their destinations before organizing.
- Only organizes files directly inside the selected folder; subfolders are left alone.
- Keeps existing destination files safe by adding a numbered suffix to duplicate names.
- Runs on your computer; your files are never uploaded.
- Uses Python's standard library for the desktop app; no web server or runtime dependencies are needed.

## Project structure

```text
smart-file-organizer/
├── desktop.py             # Native Tkinter desktop interface
├── build_windows.ps1      # Builds the Windows app and installer
├── installer.iss          # Inno Setup installer recipe
├── requirements-build.txt # Build-only PyInstaller dependency
├── requirements.txt       # No runtime dependencies
├── organizer.py           # Shared categorization and file operations
├── main.py                # Command-line alternative
└── tests/
    └── test_organizer.py  # Organizer behavior tests
```

## Run the desktop app from source

1. Install Python 3.10 or newer with Tcl/Tk support (the standard Windows installer includes it).
2. Enjoy app
   
Choose **Browse…** to select a folder. **Organize files** is always available: it scans the selected folder and asks for confirmation before moving anything. You can also select **Preview files** to review destinations first. After each run, you can click **Organize files** again to sort any new files added to the folder. The app only scans files directly inside the selected folder; files inside subfolders are left untouched.

## Build a Windows application and installer

From PowerShell in the project folder, run:

```powershell
.\build_windows.ps1
```

The script creates a standalone `dist\SmartFileOrganizer.exe`. To also produce a regular Windows setup program (`SmartFileOrganizer-Setup.exe`), install [Inno Setup 6](https://jrsoftware.org/isinfo.php) first and run the script again. The installer is written to `installer-output\SmartFileOrganizer-Setup.exe`; it adds Start Menu and optional desktop shortcuts and supports uninstalling the app.
