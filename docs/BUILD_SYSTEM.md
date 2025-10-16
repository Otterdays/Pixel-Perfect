# Build System Documentation

**Version**: 2.0  
**Date**: January 2025  
**Status**: ✅ Complete

## Overview

This document provides comprehensive guidance for building, maintaining, and troubleshooting the Pixel Perfect build system. It includes critical information about adding new modules and features.

---

## Quick Start

### Building the Executable

```batch
cd BUILDER
build.bat
```

**What happens:**
1. ✅ Checks/installs PyInstaller
2. ✅ Cleans previous builds  
3. ✅ Builds optimized executable (~24-25 MB)
4. ✅ Copies assets and documentation
5. ✅ Creates distribution package

**Output locations:**
- `BUILDER/dist/PixelPerfect.exe` - Standalone executable
- `BUILDER/release/PixelPerfect/` - Complete distribution package

---

## ⚠️ CRITICAL: Adding New Modules

### When You Add a New Feature Module

**Every time you create a new Python module** (like `background_control_manager.py` for the light/dark mode toggle), you **MUST** update the build script to include it.

### Step-by-Step Process

1. **Create your new module** (e.g., `src/ui/new_feature_manager.py`)

2. **Add it to the build script** in `BUILDER/build.bat`:
   ```batch
   --hidden-import=src.ui.new_feature_manager
   ```

3. **Place it in the correct location** within the existing `--hidden-import` list (alphabetically)

### Example: Background Mode Toggle Fix

**Problem:** Added `background_control_manager.py` but forgot to update build script.

**Error:** 
```
ModuleNotFoundError: No module named 'ui.background_control_manager'
```

**Solution:** Added to build script:
```batch
--hidden-import=src.ui.grid_control_manager --hidden-import=src.ui.background_control_manager --hidden-import=src.ui.notes_panel
```

### Current Hidden Imports List

The build script includes these modules (keep this list updated):

```batch
--hidden-import=src.core.canvas
--hidden-import=src.core.canvas_renderer  
--hidden-import=src.core.color_palette
--hidden-import=src.core.custom_colors
--hidden-import=src.core.event_dispatcher
--hidden-import=src.core.layer_manager
--hidden-import=src.core.project
--hidden-import=src.core.undo_manager
--hidden-import=src.core.saved_colors
--hidden-import=src.core.window_state_manager
--hidden-import=src.tools.base_tool
--hidden-import=src.tools.brush
--hidden-import=src.tools.eraser
--hidden-import=src.tools.eyedropper
--hidden-import=src.tools.fill
--hidden-import=src.tools.selection
--hidden-import=src.tools.shapes
--hidden-import=src.tools.pan
--hidden-import=src.tools.texture
--hidden-import=src.ui.main_window
--hidden-import=src.ui.dialog_manager
--hidden-import=src.ui.file_operations_manager
--hidden-import=src.ui.selection_manager
--hidden-import=src.ui.tool_size_manager
--hidden-import=src.ui.canvas_zoom_manager
--hidden-import=src.ui.grid_control_manager
--hidden-import=src.ui.background_control_manager  # ← Added for background mode toggle
--hidden-import=src.ui.notes_panel
--hidden-import=src.ui.theme_dialog_manager
--hidden-import=src.ui.ui_builder
--hidden-import=src.ui.layer_panel
--hidden-import=src.ui.timeline_panel
--hidden-import=src.ui.color_wheel
--hidden-import=src.ui.theme_manager
--hidden-import=src.ui.tooltip
--hidden-import=src.ui.import_png_dialog
--hidden-import=src.ui.canvas_operations_manager
--hidden-import=src.ui.layer_animation_manager
--hidden-import=src.ui.color_view_manager
--hidden-import=src.ui.loading_screen
--hidden-import=src.ui.palette_views
--hidden-import=src.ui.palette_views.grid_view
--hidden-import=src.ui.palette_views.primary_view
--hidden-import=src.ui.palette_views.constants_view
--hidden-import=src.ui.palette_views.saved_view
--hidden-import=src.utils.export
--hidden-import=src.utils.import_png
--hidden-import=src.utils.presets
--hidden-import=src.utils.file_association
--hidden-import=src.animation.timeline
```

### Why Hidden Imports Are Needed

PyInstaller analyzes your code to determine which modules to include, but it can't always detect:
- Dynamic imports
- Complex import chains
- Modules imported in conditional blocks
- New modules that aren't referenced in the main analysis

**Solution:** Explicitly tell PyInstaller to include them with `--hidden-import`.

---

## Build Configuration

### Current PyInstaller Command

```batch
python -m PyInstaller ^
  --name="PixelPerfect" ^
  --onefile ^
  --windowed ^
  --optimize=2 ^
  --icon="%ICON_PATH%" ^
  --add-data="%LOGO_PATH%;." ^
  --exclude-module=pygame ^
  --exclude-module=scipy ^
  --exclude-module=tkinter.test ^
  --exclude-module=unittest ^
  --exclude-module=test ^
  --exclude-module=xml.etree ^
  --exclude-module=xml.dom ^
  --exclude-module=doctest ^
  --exclude-module=pdb ^
  --exclude-module=email ^
  --exclude-module=http ^
  --exclude-module=urllib ^
  --exclude-module=xmlrpc ^
  --exclude-module=pydoc ^
  --exclude-module=bz2 ^
  --exclude-module=lzma ^
  --exclude-module=_ssl ^
  --exclude-module=ssl ^
  --exclude-module=charset_normalizer ^
  --exclude-module=pycparser ^
  [HIDDEN IMPORTS LIST HERE] ^
  --distpath="BUILDER\dist" ^
  --workpath="BUILDER\build" ^
  --specpath="BUILDER" ^
  main.py
```

### Key Settings Explained

| Setting | Purpose | Impact |
|---------|---------|--------|
| `--onefile` | Single executable | Easy distribution, ~100ms slower startup |
| `--windowed` | No console window | Clean UX, harder to debug |
| `--optimize=2` | Remove docstrings/assertions | ~2 MB smaller, no debugging info |
| `--exclude-module` | Block unused dependencies | Major size reduction (17+ modules) |
| `--hidden-import` | Force include project modules | Prevents runtime import errors |
| `--add-data` | Bundle external files | Icons, logos, etc. |

---

## Size Optimization

### Current Results

| Version | Size | Reduction | Notes |
|---------|------|-----------|-------|
| **v1.29** | 330 MB | - | Original with pygame/scipy |
| **v1.31** | 29 MB | -91% | Removed heavy dependencies |
| **v1.45** | ~24-25 MB | -93% | **Current optimized build** |

### Optimization Strategy

1. **Remove Heavy Dependencies** ✅
   - pygame (~60 MB) - Replaced with Tkinter rendering
   - scipy (~120 MB) - Custom NumPy scaling implementation

2. **Exclude Unused Modules** ✅
   - 15+ stdlib modules (tkinter.test, unittest, xml.*, etc.)
   - 2 third-party modules (charset_normalizer, pycparser)

3. **Bytecode Optimization** ✅
   - `--optimize=2` removes docstrings and assertions

4. **Smart Hidden Imports** ✅
   - Only include modules actually used by the application

---

## Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError on Startup

**Symptom:**
```
ModuleNotFoundError: No module named 'ui.some_module'
```

**Cause:** New module not added to `--hidden-import` list.

**Solution:**
1. Add `--hidden-import=src.path.to.module` to build script
2. Rebuild executable

#### 2. Build Fails with Import Errors

**Symptom:** PyInstaller crashes during analysis.

**Cause:** Trying to exclude a module that's still imported in code.

**Solution:**
1. Remove the module from `--exclude-module` list, OR
2. Remove all imports of that module from source code

#### 3. EXE Runs but Missing Features

**Symptom:** Application starts but some functionality doesn't work.

**Cause:** Module excluded but still needed.

**Solution:**
1. Check PyInstaller build log for warnings
2. Add missing modules to `--hidden-import` list
3. Rebuild

#### 4. Assets Not Found

**Symptom:** Application runs but palettes/icons missing.

**Cause:** Assets not bundled or copied correctly.

**Solution:**
1. Check `--add-data` flags in build script
2. Verify asset copying in build script steps 4-5

### Debug Mode

To see what PyInstaller is doing:

```batch
python -m PyInstaller --debug=imports --debug=noarchive main.py
```

This shows:
- Which modules are being analyzed
- Which imports are found/missing
- Dependency resolution process

---

## Development Workflow

### When Adding New Features

1. **Develop and test** with Python script first:
   ```batch
   python main.py
   ```

2. **Update build script** if you created new modules:
   ```batch
   # Add to BUILDER/build.bat
   --hidden-import=src.path.to.new_module
   ```

3. **Test build** locally:
   ```batch
   cd BUILDER
   build.bat
   ```

4. **Verify executable** works:
   ```batch
   BUILDER\dist\PixelPerfect.exe
   ```

5. **Update documentation** (this file) with new modules

### Testing Checklist

After building, verify:
- [ ] Application starts without errors
- [ ] All tools work (brush, eraser, fill, etc.)
- [ ] Theme switching works
- [ ] Grid/background toggles work
- [ ] Palette loading works
- [ ] Export/import functions work
- [ ] All UI panels are functional

---

## File Structure

```
BUILDER/
├── build.bat              # Main build script (EDIT THIS for new modules)
├── README.md              # Quick start guide
├── build/                 # Temporary build files (auto-generated)
├── dist/                  # Built executable (auto-generated)
│   ├── PixelPerfect.exe   # Main executable
│   ├── assets/            # Copied from ../assets/
│   └── docs/              # Copied from ../docs/
└── release/               # Distribution package (auto-generated)
    └── PixelPerfect/      # Complete package for distribution
```

---

## Distribution

### For End Users

**Recommended approach:**
1. Run `build.bat`
2. Zip `BUILDER/release/PixelPerfect/` folder
3. Users extract and run `PixelPerfect.exe`

**Benefits:**
- ✅ Single EXE file (~24-25 MB)
- ✅ No installation required
- ✅ All dependencies included
- ✅ Good antivirus compatibility

### For Developers

**Alternative approach:**
1. Use `--onedir` instead of `--onefile`
2. Zip the entire `dist/PixelPerfect/` folder
3. Users extract and run `PixelPerfect.exe` from the folder

**Benefits:**
- ✅ Faster startup time
- ✅ Easier to debug
- ⚠️ Multiple files instead of single EXE

---

## Maintenance

### Regular Tasks

1. **After adding new modules:**
   - Update `--hidden-import` list in `build.bat`
   - Update this documentation
   - Test build process

2. **After adding new dependencies:**
   - Check if they should be excluded with `--exclude-module`
   - Update `requirements.txt`
   - Test that build still works

3. **After major feature additions:**
   - Run full testing checklist
   - Check executable size hasn't grown significantly
   - Update version numbers in documentation

### Performance Monitoring

Track these metrics:
- **Build time:** Should stay under 60 seconds
- **Executable size:** Target <30 MB
- **Startup time:** Should be under 3 seconds
- **Feature completeness:** All functionality must work

---

## Version History

### v1.45 - Build System Documentation (January 2025)
- ✅ Added comprehensive build documentation
- ✅ Documented hidden imports process
- ✅ Added troubleshooting guide
- ✅ Included development workflow

### v1.44 - Background Mode Toggle Build Fix (January 2025)
- ✅ Added `--hidden-import=src.ui.background_control_manager`
- ✅ Fixed executable startup failure
- ✅ Updated build script for new module

### v1.31 - Advanced Build Optimization (October 2025)
- ✅ Reduced size to ~24-25 MB (from 330 MB)
- ✅ Added bytecode optimization
- ✅ Excluded 17+ unused modules
- ✅ Optimized build process

---

## Best Practices

### Do's

- ✅ **Always test Python script first** before building
- ✅ **Update hidden imports** when adding new modules
- ✅ **Keep this documentation current** with new modules
- ✅ **Test executable thoroughly** after building
- ✅ **Use version control** for build script changes

### Don'ts

- ❌ **Don't exclude modules** you're not sure about
- ❌ **Don't skip testing** after build changes
- ❌ **Don't forget hidden imports** for new features
- ❌ **Don't ignore build warnings** - they often indicate real issues

---

## Support

### Getting Help

1. **Check this documentation** first
2. **Run debug mode** to see PyInstaller analysis
3. **Test with Python script** to isolate issues
4. **Check build log** for specific error messages

### Common Commands

```batch
# Test Python version
python main.py

# Debug PyInstaller analysis
python -m PyInstaller --debug=imports main.py

# Clean build
cd BUILDER
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

# Full rebuild
build.bat
```

---

**Document Status:** ✅ Complete  
**Last Updated:** January 2025  
**Version:** 2.0 (Comprehensive Build System Guide)
