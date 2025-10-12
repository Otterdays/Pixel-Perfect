# Pixel Perfect - Changelog

## Version 1.14 - PNG Import with Auto-Downscaling (October 12, 2025) ✅

### New Features
- **PNG Import System**: Load PNGs directly into canvas for immediate editing
  - **Direct Canvas Loading**: No intermediate .pixpf file required
  - **Auto-downscaling**: Detects and handles scaled exports (128x128, 256x256, 512x512)
  - Validates PNG dimensions (16x16, 32x32, 64x64 or scaled versions)
  - Loads exact pixel data as RGBA into "Imported" layer
  - Auto-resizes canvas to match PNG dimensions
  - Clears existing project for fresh start
  - Save manually when ready (File → Save Project)
  - Error handling with clear user feedback
  - Created `src/utils/import_png.py` module with validation logic

### UI Updates
- Added "Import PNG" button to File menu (below "Open Project")
- File dialog filters for .png files only
- Dimension validation with scale detection
- Success message shows original size and downscale info
- Immediate canvas update - ready to edit right away

### Auto-Downscaling Feature
- **Detects scaled exports**: 8x, 4x, 2x, 1x scales
- **Examples**:
  - 256x256 PNG → Auto-downscales 8x to 32x32 canvas
  - 128x128 PNG → Auto-downscales 8x to 16x16 canvas
  - 512x512 PNG → Auto-downscales 8x to 64x64 canvas
- Uses nearest-neighbor scaling to preserve pixel-perfect art
- Console feedback shows detected scale and downscale action

### Use Cases
- **Re-edit exported PNG sprites** (most common workflow - export, edit externally, re-import)
- Import pixel art from other tools (Aseprite, Photoshop, etc.)
- Convert existing 16x16/32x32/64x64 PNGs to editable projects
- Quick project creation from screenshots or images

### Technical Details
- Uses PIL/Pillow for PNG loading and scaling
- Converts to RGBA numpy array
- Generates valid .pixpf JSON structure
- Includes metadata: import date, source filename, original size
- Default zoom based on canvas size (16x for 16/32, 8x for 64)
- Scale detection algorithm checks all common export scales

### Files Modified
- **NEW**: `src/utils/import_png.py` - PNG import utility with auto-downscaling (228 lines)
- `src/ui/main_window.py` - Added `_import_png()` method and menu item (85 lines)

---

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
  - Calls `_update_canvas_from_layers()` to composite loaded layers to canvas
  - Added immediate UI refresh with `root.update()` calls
  - Pixels now display immediately when loading projects
  - Fixed method names: `refresh()` for layer and timeline panels
  - Added better error handling with traceback output
- **Missing Palette Files**: Created 4 missing palette JSON files
  - heartwood_online.json (forest theme)
  - definya.json (bright, vibrant colors)
  - kakele_online.json (warm, golden palette)
  - rucoy_online.json (grayscale with earth tones)
- **Tool Button Text**: Changed "Rect" to "Rectangle" for clarity

### UI Polish & Layout
- **Centered Palette Layout**: View mode buttons and color grid now centered
  - Grid/Primary/Wheel buttons centered under Palette dropdown  
  - Color display grid centered in its container
  - Matches the centered design of Tools section
- **Custom Colors Expansion**: Color buttons expand to fill container width
  - Grid columns configured with equal weights (4 columns)
  - Buttons use `sticky="nsew"` to fill their grid cells
  - Increased button size from 40x40 to 50x50 pixels
  - Eliminates wasted space on the right side

### Custom File Icon System
- **Auto-Register .pixpf Icon**: Purple diamond icon for project files
  - Automatically registers on first program launch
  - Uses Windows registry (HKEY_CURRENT_USER) - no admin needed
  - Created `src/utils/file_association.py` module
  - Checks if already registered to avoid duplicate work
  - Manual fallback: `register_pixpf_icon.bat` included in distribution
  - All `.pixpf` files display custom icon in File Explorer
  - Converted save.png to pixpf_icon.ico (256x256 max size)

### Files Modified
- `src/ui/main_window.py` - Resizable panels, compact tool grid, centered palette
- `src/ui/color_wheel.py` - Expanding custom colors grid
- `src/core/color_palette.py` - OSRS palette + enum
- `assets/palettes/` - Added OSRS + 4 missing palettes
- `BUILDER/build.bat` - Updated with all new modules and icons
- `main.py` - Added file association registration on startup
- **NEW**: `src/utils/file_association.py` - Icon registration utility
- **NEW**: `assets/icons/pixpf_icon.ico` - Custom file type icon
- **NEW**: `register_pixpf_icon.bat` - Manual registration script
- **NEW**: `docs/ADDING_PALETTES.md` - Palette creation guide

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

