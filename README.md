# EXIFframe_maker

## How to Use

Screenshot:

![img](https://github.com/7ryo/EXIFframe_maker/blob/main/screenshot.png?raw=true)

1. Click "Browse Image" to import images.
2. The images will be shown in the list.
   First image on the list is the preview.
3. If you want to remove images from the list, choose images by clicking on the paths.
   (You can choose multiple images. The background will turn into gray.)
4. You can change logo from the combobox.
5. Browse your output folder, or it will create an "output" folder in the same directory.
6. You can change the suffix of the output images.
7. Run the program.

## Tips
### Customize logos
You can customize logos by adding or removing png images inside the "logo" folder.

## Install
Download this project an unzip it.
Run the exe file.

## Changelog

### Recent Updates
- **Bug Fixes**: Fixed resource leak in EXIF data reading (pyexiv2.Image not properly closed)
- **Bug Fixes**: Added error handling for image processing and EXIF data extraction
- **Bug Fixes**: Fixed path handling for cross-platform compatibility (Windows/Linux)
- **Bug Fixes**: Fixed preview image screen ratio and canvas size (canvas: 600x400)
- **Bug Fixes**: Fixed preview image not displaying (Tk/Tkinter instance conflict resolved)
- **Bug Fixes**: Fixed customtkinter CTkEntry configuration error
- **Bug Fixes**: Fixed output directory path normalization
- **Bug Fixes**: Added automatic output directory creation
- **UI Improvement**: Empty EXIF values now display as blank instead of "N/A"
- **Code Cleanup**: Removed all debug print statements and unused code
- **New Feature**: Added multi-language support (繁體中文, English, 简体中文)
  - Language selector in the UI
  - Easy switching between supported languages
- **Project**: Added requirements.txt for dependency management
- **Build**: Added build.spec and build.bat for compiling new executable

## Build Instructions

To create a new executable after code changes:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the build script:
   - Windows: Double-click `build.bat`
   - Or run: `pyinstaller build.spec`

3. The new executable will be created as `EXIFFrame.exe` in the root directory
