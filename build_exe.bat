@echo off
chcp 65001 >nul
cd /d "%~dp0"
title build hide_icons.exe with PyInstaller

where python >nul 2>&1
if errorlevel 1 (
	echo.
	echo Python was not found in PATH. Install Python 3.8 or newer first.
	echo.
	pause
	exit /b 1
)

python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
	echo.
	echo PyInstaller is missing. Install it with:
	echo   python -m pip install pyinstaller
	echo.
	pause
	exit /b 1
)

echo.
echo ================================================================
echo   building hide_icons.exe
echo ================================================================
python -m PyInstaller --onefile --console --clean --noconfirm --name hide_icons --distpath . --workpath "%~dp0build" --specpath "%~dp0build" hide_icons.py
if errorlevel 1 (
	echo.
	echo build of hide_icons failed.
	echo.
	pause
	exit /b 1
)

echo.
echo ================================================================
echo   done: hide_icons.exe rebuilt next to this script
echo   fix_db.exe in this folder is the engine copy: it must be the
echo   same build as in the PS4_db_rebuilder repository
echo ================================================================
echo.
pause
