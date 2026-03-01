@echo off
echo Building EXIFframe Maker...
echo.

:: Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
) else (
    echo PyInstaller is already installed.
)

:: Build the executable
echo.
echo Building executable...
pyinstaller build.spec

:: Move the executable to the root directory
move dist\EXIFFrame.exe .\EXIFFrame.exe >nul 2>&1

echo.
echo Build complete! EXIFframe.exe has been created.
pause
