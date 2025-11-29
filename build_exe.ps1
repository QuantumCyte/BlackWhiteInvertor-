<#
Build a one-file, windowed Windows executable for inv.py using PyInstaller.

Usage (from project root, in the activated venv):
  .\build_exe.ps1

What it does:
- Installs/ensures PyInstaller is available in the active environment
- Runs PyInstaller with --onefile --windowed to create a single executable

Notes:
- Building on Windows produces a native .exe; cross-compiling to Windows
  from macOS/Linux is not supported by PyInstaller.
#>

$ErrorActionPreference = "Stop"

Write-Host "Installing runtime requirements + build dependency (PyInstaller)..."
# Ensure runtime requirements (including Pillow) are installed so PyInstaller
# can detect package hooks and data files correctly.
pip install -r requirements.txt
pip install --upgrade pyinstaller

Write-Host "Running PyInstaller to build a single-file executable (collecting Pillow assets)..."
# Collect Pillow assets explicitly to ensure thumbnails and resources are bundled.
# --collect-all PIL gathers data files, submodules and binaries for Pillow.
pyinstaller --noconfirm --clean --onefile --windowed --name inverter --collect-all PIL inv.py

Write-Host "Build finished. Find the executable in the 'dist' folder."
