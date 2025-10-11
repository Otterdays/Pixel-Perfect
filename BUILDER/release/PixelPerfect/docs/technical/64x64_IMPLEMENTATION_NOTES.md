# 64x64 Canvas Implementation - Technical Notes

## Overview
Implementation of 64x64 canvas size for Pixel Perfect, including critical bug fixes for large canvas support.

**Status**: ✅ Complete and Tested  
**Version**: 1.11  
**Date**: October 11, 2025

---

## Implementation Summary

### Added Canvas Size
- **New Preset**: `CanvasSize.XLARGE = (64, 64)` in `src/core/canvas.py`
- **UI Integration**: Added "64x64" option to size dropdown in toolbar
- **Auto-Zoom**: Automatically adjusts to 8x zoom for optimal viewing on 64x64 and 32x64 canvases

### Files Modified
1. `src/core/canvas.py` - Added XLARGE enum value
2. `src/core/layer_manager.py` - Fixed critical dimension caching bug
3. `src/ui/main_window.py` - Added UI dropdown, resize sync, auto-zoom logic
4. `docs/README.md` - Updated canvas size documentation
5. `docs/ARCHITECTURE.md` - Updated technical specifications
6. `docs/SCRATCHPAD.md` - Comprehensive bug fix documentation

---

## Critical Bugs Discovered & Fixed

### 1. Layer Dimension Caching Bug ⭐ MOST CRITICAL

**Problem:**
The `Layer` class in `layer_manager.py` cached `width` and `height` in `__post_init__()`:

```python
def __post_init__(self):
    if len(self.pixels.shape) == 3:
        self.height, self.width, _ = self.pixels.shape  # Cached once at creation
```

When `resize_layers()` updated the pixel array, it never updated these cached dimensions:

```python
# Before fix:
def resize_layers(self, new_width: int, new_height: int):
    for layer in self.layers:
        layer.pixels = new_pixels  # Array resized to 64x64
        # BUT layer.width still = 32!
```

This caused `set_pixel()` bounds checks to fail:

```python
def set_pixel(self, x: int, y: int, color):
    if 0 <= x < self.width and 0 <= y < self.height:  # Rejected x >= 32
        self.pixels[y, x] = color
```

**Solution:**
Update cached dimensions after resizing:

```python
def resize_layers(self, new_width: int, new_height: int):
    for layer in self.layers:
        layer.pixels = new_pixels
        layer.width = new_width   # ✅ Update cached width
        layer.height = new_height # ✅ Update cached height
```

**Impact**: Drawing beyond 32x32 boundary now works correctly.

---

### 2. Canvas Resize Synchronization

**Problem:**
When changing canvas size, only `canvas.set_preset_size()` was called. The `layer_manager` and `timeline` systems retained old dimensions (32x32), causing:
- IndexError: index 40 out of bounds for axis 0 with size 32
- Drawing attempts beyond y=32 crashed

**Solution:**
Synchronize all three systems:

```python
self.canvas.set_preset_size(size_map[size_str])
self.layer_manager.resize_layers(self.canvas.width, self.canvas.height)
self.timeline.resize_frames(self.canvas.width, self.canvas.height)
self._update_canvas_from_layers()  # Sync pixel data
```

**Impact**: All systems stay synchronized during canvas resize.

---

### 3. Mouse Coordinate Conversion

**Problem:**
`_tkinter_screen_to_canvas_coords()` incorrectly subtracted widget position:

```python
# Wrong - event.x/y already widget-relative
canvas_x = self.drawing_canvas.winfo_x()
relative_x = screen_x - canvas_x - x_offset  # Double subtraction!
```

**Solution:**
Remove unnecessary widget position subtraction:

```python
# Correct - event coordinates already relative to widget
relative_x = screen_x - x_offset  # Only subtract centering offset
```

**Impact**: Mouse clicks now map correctly to canvas pixels.

---

### 4. Infinite Redraw Loop

**Problem:**
`_update_canvas_from_layers()` called `_initial_draw()` which:
- Printed "Initial draw complete!" to console
- Triggered full canvas rebuild
- Was called on every mouse movement during drawing

This created a redraw loop causing:
- Console spam
- Laggy drawing performance
- Pixels not appearing until mouse released

**Solution:**
Use proper update method instead:

```python
# Before: Called initialization function
self._initial_draw()

# After: Call proper update function
self._update_pixel_display()
```

**Impact**: Smooth drawing performance, no console spam.

---

## Auto-Zoom Feature

Large canvases at high zoom create negative offsets (viewport smaller than canvas). The auto-zoom feature prevents this:

```python
if size_str in ["32x64", "64x64"]:
    if size_str == "64x64" and self.canvas.zoom > 8:
        self.canvas.set_zoom(8)
        self.zoom_var.set("8x")
```

**Why 8x?**
- 64 × 8 = 512 pixels fits comfortably in 864px viewport width
- Provides good visibility without negative offsets
- User can manually adjust zoom afterward if needed

---

## Grid System

The grid automatically scales with canvas size:
- **Vertical lines**: `width + 1` lines (65 lines for 64x64)
- **Horizontal lines**: `height + 1` lines (65 lines for 64x64)
- **Line spacing**: 1 line per pixel edge
- **Line width**: Adaptive 1-2px based on zoom level

Grid rendering works identically for all canvas sizes since it uses `self.canvas.width` and `self.canvas.height` dynamically.

---

## Testing Performed

### All Canvas Sizes Verified
- ✅ 16x16: Full coverage, grid visible
- ✅ 32x32: Full coverage, grid visible  
- ✅ 16x32: Full coverage, grid visible
- ✅ 32x64: Full coverage with auto-zoom
- ✅ 64x64: Full coverage with auto-zoom

### Drawing Tests
- ✅ All four corners accessible
- ✅ Drawing along all edges
- ✅ Fill tool works across entire canvas
- ✅ Line tool spans full canvas
- ✅ All tools functional at all sizes

### Performance Tests
- ✅ No console spam
- ✅ Smooth drawing response
- ✅ Instant pixel appearance
- ✅ No redraw loops
- ✅ Zoom changes work correctly

---

## Lessons Learned

1. **Cached Properties**: When caching computed values, always update them when underlying data changes
2. **System Synchronization**: Multiple systems managing same data need explicit sync points
3. **Coordinate Spaces**: Understanding coordinate space transformations is critical (widget-relative vs absolute)
4. **Update vs Initialize**: Distinguish between initialization and update operations
5. **Testing Edge Cases**: Large canvas sizes exposed bugs that worked fine at smaller sizes

---

## Future Considerations

### Potential Enhancements
1. **Dynamic Zoom Calculation**: Calculate optimal zoom based on actual viewport size
2. **Canvas Scrolling**: For very large canvases, add scrollbars instead of limiting zoom
3. **Viewport Indicators**: Show which portion of large canvas is visible
4. **Custom Canvas Sizes**: Allow user to input arbitrary dimensions

### Performance Optimization
- Current implementation redraws entire canvas on changes
- For very large canvases (>64x64), consider:
  - Dirty rectangle tracking
  - Tile-based rendering
  - Canvas viewport culling

---

## Related Documentation
- See `docs/SCRATCHPAD.md` for detailed bug fix history
- See `docs/CHANGELOG.md` for version history
- See `docs/ARCHITECTURE.md` for system architecture

---

*Implementation completed and tested: October 11, 2025*

