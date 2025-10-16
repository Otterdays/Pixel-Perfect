# Pixel Perfect - Build System

This folder contains the build scripts and tools to create standalone executables for Pixel Perfect.

> **📖 For complete build system documentation, see [docs/BUILD_SYSTEM.md](../docs/BUILD_SYSTEM.md)**

## ⚠️ IMPORTANT: Adding New Modules

**When you create a new Python module** (like `background_control_manager.py`), you **MUST** add it to the build script or the executable will fail to start with `ModuleNotFoundError`.

**Add to `build.bat`:**
```batch
--hidden-import=src.path.to.your.new.module
```

## Quick Start

Simply run:
```batch
build.bat
```

This will:
1. Check and install PyInstaller if needed
2. Clean previous builds
3. Build the executable with all dependencies (~24-25 MB)
4. Copy assets and documentation
5. Create a release package ready for distribution

## Output

After building, you'll find:
- **`dist/PixelPerfect.exe`** - The standalone executable
- **`dist/assets/`** - Required asset files
- **`dist/docs/`** - Documentation files
- **`release/PixelPerfect/`** - Complete distribution package

## Distribution

To share Pixel Perfect with others:
1. Run `build.bat`
2. Zip the entire `BUILDER/release/PixelPerfect/` folder
3. Users just need to extract and run `PixelPerfect.exe`

## Requirements

- Python 3.13+ installed
- All dependencies from `requirements.txt` installed
- PyInstaller (will be auto-installed if missing)

## Build Options

The build script uses these PyInstaller options:
- `--onefile` - Single executable file
- `--windowed` - No console window (GUI only)
- `--add-data` - Includes assets and docs

## Troubleshooting

**Build fails?**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that Python is in your PATH
- Try running as administrator

**Executable won't start?**
- Make sure assets folder is present
- Check Windows Defender isn't blocking it
- Try running from command line to see error messages

## Advanced Usage

Edit `build.bat` to customize:
- Add custom icon with `--icon=path/to/icon.ico`
- Change output directory with `--distpath`
- Add more hidden imports if needed
- Adjust compression settings

## File Structure

```
BUILDER/
├── build.bat           # Main build script
├── README.md           # This file
├── build/              # Temporary build files (auto-generated)
├── dist/               # Built executable (auto-generated)
└── release/            # Distribution package (auto-generated)
```

## Clean Build

To start fresh, the script automatically cleans:
- `build/` folder
- `dist/` folder  
- `*.spec` files

## Version Info

Built executables will include:
- All Python dependencies bundled
- Assets and palettes
- Documentation files
- No external requirements needed

