# Pixel Perfect - Changelog

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

