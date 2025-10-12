# Pixel Perfect - Changelog

## Version 1.13 - UI Improvements & Complete Palette System (October 11, 2025) ✅

### New Features
- **Custom Application Icon**: Colorful 4×4 pixel grid logo
  - Displays in EXE file icon, window title bar, and Windows taskbar
  - Proper Windows ICO format with 7 icon sizes (16×16 to 256×256)
  - Fixed runtime icon loading for PyInstaller bundled executables
  - Uses `sys.frozen` detection to locate assets correctly when bundled
- **Resizable Side Panels**: Drag dividers to resize left/right panels horizontally
- **All 6 Palettes Available**: Added 4 missing palette JSON files to distribution

### UI Improvements
1. **Compact 3×3 Tool Grid**: Reorganized tools from vertical stack to grid layout
   - Saves ~130+ pixels of vertical space
   - Fixed button sizes (85px × 28px)
   - Centered Tools section with proper frame wrapping

2. **Reduced Vertical Spacing**: Tightened padding throughout panels
   - Tools panel padding reduced by ~50%
   - Palette panel padding reduced by ~50-65%
   - Total space saved: ~180+ pixels

3. **Resizable Panel System**: Implemented tkinter PanedWindow
   - Left panel: 500px default (min 220px)
   - Right panel: 300px default (min 220px)
   - Canvas: 400px minimum, always expands
   - 8px raised sash handles for easy resizing

### Bug Fixes
- **Project Import Not Working**: Fixed `load_project()` call missing required parameters
  - Now passes canvas, palette, layer_manager, and timeline objects
  - Added UI updates after loading (canvas, layers, timeline, palette)
  - Added better error handling and feedback
- **Missing Palette Files**: Created 4 missing palette JSON files
  - heartwood_online.json (forest theme)
  - definya.json (bright, vibrant colors)
  - kakele_online.json (warm, golden palette)
  - rucoy_online.json (grayscale with earth tones)
- **Tool Button Text**: Changed "Rect" to "Rectangle" for clarity

### Files Modified
- `src/ui/main_window.py` - Resizable panels, compact tool grid
- `assets/palettes/` - Added 4 missing palette JSON files
- `src/core/color_palette.py` - Verified KAKELE enum type
- `BUILDER/build.bat` - Updated with custom_colors module

---

## Version 1.11 - 64x64 Canvas Size Addition (October 11, 2025) ✅

### New Features
- **64x64 Canvas Size**: Added extra-large canvas preset for detailed sprites and tile sets
- **Auto-Zoom Adjustment**: Automatically adjusts zoom to 8x for large canvases (32x64, 64x64) to ensure optimal viewing

### Bug Fixes - Critical
1. **Layer Dimension Caching Bug** ⭐ CRITICAL
   - Fixed Layer class not updating cached width/height after resize
   - Symptom: Could only draw in 32x32 area regardless of canvas size
   - Solution: Update layer.width and layer.height when resizing pixel arrays

2. **Canvas Resize Synchronization**
   - Fixed layer manager and timeline not resizing with canvas
   - Symptom: IndexError when drawing after canvas resize
   - Solution: Call resize_layers() and resize_frames() on canvas size change

3. **Mouse Coordinate Conversion**
   - Fixed incorrect coordinate conversion subtracting widget position twice
   - Symptom: Drawing only worked in upper-left portion of canvas
   - Solution: Removed incorrect winfo_x/y subtraction (event coordinates already widget-relative)

4. **Infinite Redraw Loop**
   - Fixed redraw loop causing console spam and rendering issues
   - Symptom: "Initial draw complete!" repeating endlessly, laggy drawing
   - Solution: Changed _update_canvas_from_layers() to use _update_pixel_display() instead of _initial_draw()

### Technical Changes
- `src/core/canvas.py`: Added CanvasSize.XLARGE = (64, 64)
- `src/core/layer_manager.py`: Added layer dimension update in resize_layers()
- `src/ui/main_window.py`: Enhanced _on_size_change() with layer sync and auto-zoom

### Testing Status
✅ All canvas sizes tested and working:
- 16x16 ✅
- 32x32 ✅
- 16x32 ✅
- 32x64 ✅
- 64x64 ✅

---

## Version 1.10 - Complete Color System Overhaul (Previous)

### Bug Fixes
- Color wheel radio button layout
- Color selection visual feedback
- Color variation highlighting
- Color variation duplicates
- Dynamic color grids

---

## Version 1.09 - UI Improvements (Previous)

### Features
- Primary colors widget duplication fix
- Launch script auto-close enhancement
- Color button hover effects

---

## Version 1.08 - Undo/Redo System (Previous)

### Features
- Complete undo/redo functionality
- Grid centering on window resize
- Keyboard shortcuts (Ctrl+Z, Ctrl+Y)

---

## Version 1.05 - GitHub Release (October 10, 2024)

### Milestone
- Project published to GitHub
- Standalone executable available
- Production ready status

---

## Version 1.0 - Initial Release

### Complete Features
- 9 drawing tools
- 6 color palettes + color wheel
- Layer system with 10 layers
- Animation timeline
- Export system (PNG, GIF, sprite sheets)
- Undo/redo with 50+ state history
- 8 preset templates
- Project save/load system

