# Edge Tool Visual Feedback Fix

**Date**: October 16, 2025  
**Version**: 2.5.1  
**Status**: ✅ Complete  
**Priority**: Medium

## Problem Description

The edge tool was missing visual feedback (hover preview) when moving the mouse over the canvas, unlike the brush and eraser tools which showed proper preview indicators.

### Symptoms
- Edge tool had no visual feedback when hovering over pixels
- No preview showing which edge would be drawn
- Users couldn't see where they were about to draw edge lines
- Inconsistent experience compared to brush/eraser tools

## Root Cause

The edge tool was **not included** in the mouse move event handler in `src/core/event_dispatcher.py`. While brush and eraser tools got their visual feedback through the canvas renderer's preview methods, the edge tool was completely missing from the preview system.

**Missing Code**: The `on_tkinter_canvas_mouse_move()` method had preview logic for brush, eraser, texture, and shape tools, but **no case for the edge tool**.

### Problem Code
```python
# Show tool preview using canvas_renderer
if self.main_window.current_tool == "brush":
    self.main_window.canvas_renderer.draw_brush_preview(canvas_x, canvas_y)
elif self.main_window.current_tool == "eraser":
    self.main_window.canvas_renderer.draw_eraser_preview(canvas_x, canvas_y)
elif self.main_window.current_tool == "texture":
    # ... texture preview logic
# ← MISSING: elif self.main_window.current_tool == "edge":
```

## Solution

Added edge tool support to the mouse move event handler by calling its `on_mouse_move` method, which contains the edge tool's built-in preview system.

### Fixed Code

**Added Edge Tool Preview Logic** (`src/core/event_dispatcher.py`):
```python
elif self.main_window.current_tool == "edge":
    # Edge tool has its own preview system - call its on_mouse_move method
    canvas_x_float, canvas_y_float = self.main_window._tkinter_screen_to_canvas_coords_float(event.x, event.y)
    tool = self.main_window.tools.get("edge")
    if tool:
        current_color = self.main_window.get_current_color()
        tool.on_mouse_move(self.main_window.canvas, canvas_x_float, canvas_y_float, current_color)
```

**Added Edge Preview Cleanup**:
```python
# Clear any previews when mouse leaves canvas
self.main_window.drawing_canvas.delete("brush_preview")
self.main_window.drawing_canvas.delete("eraser_preview")
self.main_window.drawing_canvas.delete("texture_preview")
self.main_window.drawing_canvas.delete("edge_preview")  # ← ADDED

# Clear previews for other tools
self.main_window.drawing_canvas.delete("brush_preview")
self.main_window.drawing_canvas.delete("eraser_preview")
self.main_window.drawing_canvas.delete("texture_preview")
self.main_window.drawing_canvas.delete("edge_preview")  # ← ADDED
```

## Files Modified

- **`src/core/event_dispatcher.py`**
  - Added edge tool case to `on_tkinter_canvas_mouse_move()` method (lines 542-548)
  - Added `edge_preview` cleanup in multiple locations (lines 141, 147, 245, 527, 564)
  - Integrated edge tool's existing preview system with float coordinates

## Technical Details

### Edge Tool Preview System
The edge tool has a sophisticated preview system built into its `on_mouse_move` method:
- **`_update_hover_preview()`**: Detects which edge is being hovered over
- **`_draw_preview()`**: Draws preview lines showing where edge will be placed
- **`_clear_preview()`**: Removes preview lines when moving away

### Coordinate System
- Uses **float precision coordinates** for accurate edge detection
- Calls `_tkinter_screen_to_canvas_coords_float()` for proper coordinate conversion
- Maintains consistency with edge tool's special coordinate handling

## Benefits

- **Visual Consistency**: Edge tool now has visual feedback like other tools
- **Better UX**: Users can see exactly where edge lines will be drawn before clicking
- **Precise Targeting**: Preview shows which edge (top/bottom/left/right) will be affected
- **Professional Feel**: Consistent visual feedback across all drawing tools

## User Experience

### Before Fix
- Edge tool: No visual feedback, users had to guess where edges would be drawn
- Brush tool: ✅ Visual preview showing brush area
- Eraser tool: ✅ Visual preview showing eraser area

### After Fix
- Edge tool: ✅ Visual preview showing edge line placement
- Brush tool: ✅ Visual preview showing brush area  
- Eraser tool: ✅ Visual preview showing eraser area

## Testing Recommendations

1. **Hover Test**: Move mouse over canvas with edge tool selected
2. **Edge Detection**: Verify preview shows correct edge (top/bottom/left/right)
3. **Tool Switching**: Ensure preview clears when switching to other tools
4. **Canvas Boundaries**: Test hover behavior at canvas edges
5. **Zoom Levels**: Verify preview works at different zoom levels

## Related Hardening: Immortal Edge Lines Purge

In rare cases, edge overlays could persist after redraws. We added a safety purge:

- Main window now includes ` _purge_canvas_overlays()` which deletes overlay tags (`edge_preview`, `edge_lines`, `shape_preview`, `selection`, etc.) and asks the Edge tool to clear stored lines.
- `FileOperationsManager.new_project()` calls this purge first to guarantee a clean slate.
- `Ctrl+N` now routes to `FileOperationsManager.new_project()` to ensure the same cleanup path.

This guarantees New Project and session resets cannot inherit “immortal” edge lines.

---

**Status**: ✅ Complete and ready for testing  
**Impact**: Medium - adds essential visual feedback to edge tool  
**User Benefit**: High - provides consistent visual feedback across all tools
