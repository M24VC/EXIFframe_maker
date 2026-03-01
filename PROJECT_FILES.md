# EXIFframe_maker - Project Files

## Executable
- `EXIFFrame.exe` (28 MB) - Standalone Windows executable

## Source Code
- `mainApp.py` (14 KB) - Main application UI
- `EXIFframe.py` (7.7 KB) - EXIF processing and watermark generation
- `nikon_lens.py` (42 KB) - Nikon lens database
- `lang.py` (1.4 KB) - Multi-language support

## Configuration
- `build.spec` - PyInstaller build configuration
- `build.bat` - Windows build script
- `requirements.txt` - Python dependencies

## Documentation
- `README.md` - User manual and changelog
- `REFACTORING.md` - Code refactoring summary
- `BUILD_REPORT.md` - Build report

## Resources
- `logo/` - Camera brand logos (10 PNG files)
- `Saira_Semi_Condensed/` - Font files for watermark text

## Project Structure
```
EXIFframe_maker/
├── EXIFFrame.exe          # Main executable
├── mainApp.py              # UI code
├── EXIFframe.py           # Core logic
├── nikon_lens.py          # Lens database
├── lang.py                # Language support
├── build.spec             # Build config
├── build.bat              # Build script
├── requirements.txt        # Dependencies
├── README.md              # Documentation
├── REFACTORING.md         # Refactoring notes
├── BUILD_REPORT.md        # Build report
├── logo/                  # Logo images
│   ├── Canon_red.png
│   ├── Nikon_yellow.png
│   ├── FUJIFILM.png
│   ├── SONY.png
│   ├── Leica_black.png
│   ├── Leica_red.png
│   ├── Leica_text.png
│   ├── HASSELBLAD_H.png
│   ├── NXstudio.png
│   └── lumix.png
└── Saira_Semi_Condensed/   # Font family
    ├── SairaSemiCondensed-Regular.ttf
    ├── SairaSemiCondensed-Bold.ttf
    └── Other font weights...
```

## Distribution Package
To distribute, create a ZIP file containing:
1. EXIFFrame.exe
2. README.md
3. logo/ folder
4. Saira_Semi_Condensed/ folder

Users only need these files to run the application.
