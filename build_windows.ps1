$ErrorActionPreference = "Stop"

$Python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    $Python = "python"
}

& $Python -m pip install -r requirements-build.txt
if ($LASTEXITCODE -ne 0) {
    throw "Could not install the Windows build dependencies."
}

& $Python -m PyInstaller --noconfirm --clean --onefile --windowed --name SmartFileOrganizer desktop.py
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller failed to build the desktop application."
}

$Compiler = Get-Command ISCC.exe -ErrorAction SilentlyContinue
$CompilerPath = $null
if ($Compiler) {
    $CompilerPath = $Compiler.Source
}
else {
    $CompilerPath = @(
        "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe",
        "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
        "$env:ProgramFiles\Inno Setup 6\ISCC.exe"
    ) | Where-Object { Test-Path $_ } | Select-Object -First 1
}

if ($CompilerPath) {
    & $CompilerPath installer.iss
    if ($LASTEXITCODE -ne 0) {
        throw "Inno Setup failed to build the installer."
    }
    Write-Host "Installer created in the installer-output folder."
}
else {
    Write-Host "Standalone app created at dist\SmartFileOrganizer.exe"
    Write-Host "To create a setup installer, install Inno Setup and run this script again."
}
