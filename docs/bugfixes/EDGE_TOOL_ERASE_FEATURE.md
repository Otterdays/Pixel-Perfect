# Edge Tool Right-Click Erase Feature

**Date**: October 16, 2025  
**Version**: 2.5.1  
**Status**: ✅ Complete  
**Priority**: Medium

## Feature Description

Added right-click erase functionality to the Edge tool, allowing users to remove edge lines by right-clicking near them.

### Functionality
- **Right-click to erase**: Right-click while using the edge tool to erase nearby edge lines
- **Smart detection**: Finds and removes edge lines on the clicked pixel and adjacent pixels
- **Visual feedback**: Console message shows how many edge lines were erased
- **Immediate update**: Canvas redraws immediately after erasing

## Implementation Details

### Files Modified

1. **`src/tools/edge.py`**
   - Added right-click handling in `on_mouse_down()` method (button == 3)
   - Added `_erase_edge_at_position()` method for edge erasure logic
   - Added `_is_edge_near_pixel()` method for smart edge detection
   - Enhanced edge management with removal and redraw functionality

2. **`src/core/event_dispatcher.py`**
   - Added `<Button-3>` event binding for right-click detection
   - Added `on_tkinter_canvas_right_click()` method
   - Integrated float-precision coordinates for edge tool right-click

### Technical Architecture

**Right-Click Detection:**
```python
def on_mouse_down(self, canvas, x: float, y: float, button: int, color: Tuple[int, int, int, int]):
    if button == 1:  # Left mouse button - draw edge
        self.is_drawing = True
        self._draw_edge_at_position(canvas, x, y, color)
    elif button == 3:  # Right mouse button - erase edge
        self._erase_edge_at_position(canvas, x, y)
```

**Smart Edge Detection:**
```python
def _is_edge_near_pixel(self, edge_pixel_x: int, edge_pixel_y: int, edge_type: str, target_x: int, target_y: int) -> bool:
    # Check if edge pixel is the same as target pixel
    if edge_pixel_x == target_x and edge_pixel_y == target_y:
        return True
    
    # Check adjacent pixels based on edge type
    if edge_type == "top":
        return (edge_pixel_x == target_x and edge_pixel_y == target_y - 1)
    elif edge_type == "bottom":
        return (edge_pixel_x == target_x and edge_pixel_y == target_y + 1)
    # ... etc
```

**Event Binding:**
```python
# Canvas mouse events
self.main_window.drawing_canvas.bind("<Button-3>", self.on_tkinter_canvas_right_click)
```

## User Experience

### Workflow
1. **Select Edge tool** from the toolbar
2. **Left-click** to draw edge lines on pixel boundaries
3. **Right-click** to erase edge lines near the clicked position
4. **Console feedback** shows number of erased lines

### Visual Feedback
- **Immediate erasure**: Edge lines disappear instantly when right-clicked
- **Console messages**: "[Edge Tool] Erased X edge line(s)" feedback
- **Smart targeting**: Erases edges on clicked pixel and adjacent pixels

## Benefits

- **Intuitive workflow**: Left-click to draw, right-click to erase
- **Precise control**: Can erase specific edge lines without affecting others
- **Smart detection**: Automatically finds related edge lines on adjacent pixels
- **Consistent UX**: Follows common software patterns for draw/erase tools
- **Non-destructive**: Only affects edge lines, not underlying pixels

## Edge Cases Handled

- **Canvas boundaries**: Prevents erasing outside canvas limits
- **Multiple edges**: Can erase multiple edge lines with one right-click
- **Adjacent detection**: Finds edges on connected pixels based on edge type
- **Empty results**: Gracefully handles clicks with no nearby edges

## Future Enhancements

- **Visual preview**: Show which edges will be erased on hover
- **Undo support**: Integrate with undo system for edge erasure
- **Bulk erasing**: Right-click drag to erase multiple edges
- **Edge selection**: Click to select specific edges before erasing

## Reliability Improvements

- New Project now performs a canvas overlay purge to eliminate any stuck edge lines (rare). The purge:
  - Deletes overlay tags (`edge_preview`, `edge_lines`, etc.)
  - Calls `EdgeTool.clear_all_edges()` to wipe stored lines
- `Ctrl+N` is wired to use FileOps `new_project()` so the purge always runs.

---

**Status**: ✅ Complete and ready for testing  
**Impact**: Medium - adds essential erase functionality to edge tool  
**User Benefit**: High - completes the draw/erase workflow for edge tool
