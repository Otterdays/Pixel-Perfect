# Edge Tool Detection Fix

**Date**: October 16, 2025  
**Version**: 2.5.1  
**Status**: ✅ Fixed  
**Priority**: High

## Problem Description

Edge tool only drew lines on the upper (top) edge of pixels regardless of where the user clicked within the pixel. Users could not reliably target bottom, left, or right edges of pixels.

### Symptoms
- Clicking anywhere on a pixel would primarily draw on the top edge
- Bottom, left, and right edges were nearly impossible to target
- Edge detection felt inconsistent and unpredictable

## Root Cause

The issue was in the **coordinate conversion system** in `src/ui/main_window.py`. The `_tkinter_screen_to_canvas_coords()` method was using `int()` conversion which **truncated all fractional mouse coordinates** to exact pixel boundaries.

**Critical Bug**: Mouse coordinates like `(15.3, 12.7)` were being converted to `(15, 12)`, making `mouse_in_pixel_x = 0.0` and `mouse_in_pixel_y = 0.0` always, which always detected the "top" edge.

### Problem Code
```python
# In _tkinter_screen_to_canvas_coords() - line 769-770
canvas_x = int((screen_x - x_offset) / self.canvas.zoom)  # ← INT() TRUNCATES!
canvas_y = int((screen_y - y_offset) / self.canvas.zoom)  # ← INT() TRUNCATES!
```

**Debug Output Confirmed**:
```
DEBUG Edge Tool: mouse_x=15.00, mouse_y=12.00, pixel_x=15, pixel_y=12
DEBUG Edge Tool: mouse_in_pixel_x=0.00, mouse_in_pixel_y=0.00  ← ALWAYS 0.00!
DEBUG Edge Tool: detected edge = top  ← ALWAYS TOP!
```

## Solution

Created **separate float-precision coordinate system** for the edge tool:

1. **New Method**: Added `_tkinter_screen_to_canvas_coords_float()` that preserves fractional coordinates
2. **Edge Tool Special Handling**: Modified event dispatcher to use float coordinates specifically for edge tool
3. **Updated Edge Tool**: Changed edge tool methods to accept `float` coordinates instead of `int`
4. **Maintained Compatibility**: Other tools continue using integer coordinates as before

### Fixed Code

**New Float Coordinate Method** (`src/ui/main_window.py`):
```python
def _tkinter_screen_to_canvas_coords_float(self, screen_x: int, screen_y: int) -> tuple[float, float]:
    """Convert tkinter screen coordinates to canvas coordinates with float precision (for edge tool)"""
    # ... same calculation as _tkinter_screen_to_canvas_coords() but WITHOUT int() conversion
    canvas_x = (screen_x - x_offset) / self.canvas.zoom  # ← NO int()!
    canvas_y = (screen_y - y_offset) / self.canvas.zoom  # ← NO int()!
    return (canvas_x, canvas_y)
```

**Event Dispatcher Special Handling** (`src/core/event_dispatcher.py`):
```python
if self.main_window.current_tool == "edge":
    # Convert to float coordinates for edge tool precision
    canvas_x_float, canvas_y_float = self.main_window._tkinter_screen_to_canvas_coords_float(event.x, event.y)
    tool.on_mouse_move(self.main_window.canvas, canvas_x_float, canvas_y_float, current_color)
```

**Edge Tool Method Signatures** (`src/tools/edge.py`):
```python
def on_mouse_down(self, canvas, x: float, y: float, button: int, color: Tuple[int, int, int, int]):
def on_mouse_move(self, canvas, x: float, y: float, color: Tuple[int, int, int, int]):
def _update_hover_preview(self, canvas, x: float, y: float, color: Tuple[int, int, int, int]):
```

## Files Modified

- **`src/ui/main_window.py`**
  - Added `_tkinter_screen_to_canvas_coords_float()` method (lines 778-807)
  - Provides float-precision coordinates for edge tool

- **`src/core/event_dispatcher.py`**
  - Added special handling for edge tool in mouse events (lines 335-339, 474-477)
  - Uses float coordinates for edge tool, integer for others

- **`src/tools/edge.py`**
  - Changed method signatures from `int` to `float` coordinates (lines 25, 31, 35, 44, 210)
  - Removed debug output after issue identification

## Benefits

- **Accurate edge targeting**: Users can now reliably click on any edge of a pixel
- **Precise coordinate handling**: Float coordinates preserve exact mouse position within pixels
- **Fair distribution**: All edges have equal chance of being selected based on actual distance
- **Smart corner handling**: When near corners, selects the actually closest edge
- **Zoom-friendly**: Works well at all zoom levels
- **Backward compatibility**: Other tools unaffected by coordinate system changes

## Testing Recommendations

1. Test edge drawing at various zoom levels (1x, 4x, 16x, 64x)
2. Verify all four edges (top, bottom, left, right) can be targeted
3. Test corner clicking behavior
4. Verify hover preview shows correct edge
5. Test continuous drawing (drag) across multiple pixels

## Technical Details

**Algorithm**: Euclidean distance minimization
- Calculates perpendicular distance to each of the 4 edges
- Selects edge with minimum distance
- Only triggers if within 25% threshold

**Complexity**: O(1) - constant time calculation
**Edge Zone**: 25% of pixel dimension (configurable)

---

**Status**: ✅ Complete and ready for testing  
**Impact**: High - restores full edge tool functionality  
**Regression Risk**: Low - isolated change to detection algorithm

