# Import PNG Dialog Feature

**Version:** 2.1.0  
**Status:** ✅ Complete  
**Location:** `src/ui/import_png_dialog.py`

## Overview

The Import PNG Dialog provides a user-friendly interface for importing PNG images into Pixel Perfect projects. It features a spinning 3D preview, flexible scaling options, and intelligent auto-detection of exported pixel art.

## Features

### 1. **Spinning Preview**
- Real-time 3D rotation animation of the selected PNG
- Shows the actual image you're about to import
- Smooth, slow rotation for visual clarity
- Automatically sized to fit the preview area

### 2. **Smart Auto-Downscaling**
When you import a PNG that was previously exported at a higher scale (e.g., 128x128 from a 16x16 canvas exported at 8x), the importer:
- Automatically detects the original scale (8x, 4x, 2x, etc.)
- Downscales to the base pixel art dimensions (16x16, 32x32, or 64x64)
- Preserves pixel-perfect quality using nearest-neighbor resampling
- Displays clear console messages about the detection

**Example:**
```
Auto-downscaled from 128x128 to 16x16 (8x scale detected)
```

### 3. **Manual Scale Options**
Choose how to import your image:
- **1x** - Import at original pixel art size (no scaling)
- **2x** - Double the dimensions
- **3x** - Triple the dimensions
- **4x** - Quadruple the dimensions

The result dimensions are displayed in real-time as you select different scales.

### 4. **Automatic Canvas Resizing**
- The canvas automatically resizes to match the imported image dimensions
- Layer manager dimensions are updated accordingly
- All UI elements (size display, zoom, etc.) update to reflect the new canvas size

### 5. **Validation**
- Only accepts valid PNG files
- Validates dimensions (must be 16x16, 32x32, 64x64, or scaled versions)
- Provides clear error messages for invalid files

## Usage

### Basic Import (1x Scale)
1. Click **File → Import PNG**
2. Select a PNG file
3. Watch the spinning preview
4. Click **1x** (default)
5. Click **Import**

### Scaled Import
1. Click **File → Import PNG**
2. Select a PNG file
3. Choose your desired scale (2x, 3x, or 4x)
4. The result dimensions update to show the final size
5. Click **Import**

### Example Scenarios

#### Scenario 1: Import a 16x16 sprite at original size
- PNG: 16x16 pixels
- Scale: 1x
- Result: 16x16 canvas with pixel-perfect sprite

#### Scenario 2: Import a previously exported image
- Original: Created a 16x16 sprite
- Exported: Saved as 128x128 PNG (8x scale)
- Import: Select 128x128 PNG → Auto-downscales to 16x16 → Choose 1x
- Result: Back to original 16x16 canvas

#### Scenario 3: Upscale a small sprite
- PNG: 16x16 pixels
- Scale: 4x
- Result: 64x64 canvas with 4x upscaled sprite

## Technical Implementation

### Files Modified
- `src/ui/import_png_dialog.py` - New dialog class
- `src/ui/main_window.py` - Integration and import handling
- `src/utils/import_png.py` - PNG to .pixpf conversion with scaling support
- `src/core/project.py` - Canvas and layer manager dimension sync
- `src/core/event_dispatcher.py` - Focus handling fixes

### Key Methods

**ImportPNGDialog**
- `show()` - Display the dialog
- `_load_preview()` - Load and display PNG preview
- `_rotate_preview()` - Animate the spinning preview
- `_set_scale()` - Update scale factor and result dimensions
- `_do_import()` - Execute the import callback

**PNGImporter**
- `import_png_to_pixpf(file, output, scale_factor)` - Convert PNG to .pixpf with optional upscaling

### Scale Factor Logic

The importer distinguishes between:
1. **Auto-downscaling** (`detected_scale`) - For exported images that need to be restored to pixel art size
2. **User scaling** (`scale_factor`) - For intentional upscaling during import

This allows you to import a 128x128 exported PNG, have it correctly detected as an 8x export of 16x16, then optionally upscale it to 32x32 (2x), 48x48 (3x), or 64x64 (4x).

## Known Issues

None! All issues have been resolved.

## Future Enhancements

Potential improvements for future versions:
- [ ] Support for non-square images
- [ ] Batch import multiple PNGs
- [ ] Preview grid overlay to show pixel boundaries
- [ ] Custom palette extraction from imported image
- [ ] Drag-and-drop PNG import
- [ ] Import to specific layer instead of replacing entire canvas

## Version History

### v2.1.0 (2025-10-15)
- ✅ Initial implementation
- ✅ Spinning preview animation
- ✅ Scale options (1x, 2x, 3x, 4x)
- ✅ Auto-downscale detection
- ✅ Canvas auto-resize
- ✅ Fixed scale_factor variable conflict bug
- ✅ Fixed layer manager dimension sync
- ✅ Fixed canvas rendering errors
- ✅ Fixed TclError on success dialog (replaced with messagebox)
- ✅ Fixed dialog positioning to stay within screen bounds

---

**See Also:**
- `PIXPF_FORMAT.md` - File format specification
- `ARCHITECTURE.md` - System design
- `CHANGELOG.md` - Version history
