# Edge Tool Flickering Lines Fix

**Date:** January 2025  
**Version:** 2.5.3  
**Status:** RESOLVED

## Problem Description

When drawing with the edge tool using continuous mouse drag, the edge lines were flickering in and out of view. This made it impossible to see what was being drawn in real-time and created a poor user experience.

## Root Cause Analysis

The flickering was caused by the hover preview system interfering with the permanent edge drawing during continuous drawing operations:

1. **Preview System Interference**: During mouse drag, `_update_hover_preview()` was constantly being called
2. **Canvas Clearing**: The preview system calls `_clear_preview()` which deletes "edge_preview" canvas items
3. **Redraw Conflicts**: The preview clearing was interfering with the permanent edge line rendering
4. **Deferred Drawing Issues**: The deferred drawing mechanism was working correctly, but the preview system was causing visual conflicts

## Technical Details

### Affected Methods
- `on_mouse_move()` - Was calling preview updates during active drawing
- `_update_hover_preview()` - Was interfering with permanent lines
- `_draw_preview()` and `_clear_preview()` - Were causing visual conflicts

### The Fix

**1. Disable Preview During Active Drawing**
```python
def on_mouse_move(self, canvas, x: float, y: float, color: Tuple[int, int, int, int]):
    """Handle mouse movement for hover preview and drawing"""
    # Only update hover preview when NOT actively drawing to prevent flickering
    if not self.is_drawing:
        self._update_hover_preview(canvas, x, y, color)
    
    # Continue drawing if mouse is down
    if self.is_drawing:
        self._draw_edge_at_position(canvas, x, y, color)
```

**2. Clear Preview Before Starting to Draw**
```python
def on_mouse_down(self, canvas, x: float, y: float, button: int, color: Tuple[int, int, int, int]):
    if button == 1:  # Left mouse button - draw edge
        self.is_drawing = True
        # Clear any existing preview before starting to draw
        self._clear_preview()
        self._draw_edge_at_position(canvas, x, y, color)
```

**3. Clear Preview After Drawing Completes**
```python
def on_mouse_up(self, canvas, x: float, y: float, button: int, color: Tuple[int, int, int, int]):
    self.is_drawing = False
    
    # Clear any remaining preview after drawing is complete
    self._clear_preview()
    
    # Execute any pending redraw now that drawing is complete
    if self.pending_redraw:
        self.redraw_all_edges()
        self.pending_redraw = False
```

## Solution Benefits

1. **Eliminates Flickering**: Edge lines no longer flicker during continuous drawing
2. **Maintains Preview System**: Hover preview still works when not actively drawing
3. **Clean Drawing Experience**: Users can see their edge lines being drawn in real-time
4. **Preserves Performance**: No impact on the deferred drawing optimization
5. **Backward Compatibility**: All existing edge tool functionality remains intact

## Testing Results

- ✅ Continuous edge drawing without flickering
- ✅ Hover preview still works when not drawing
- ✅ Right-click erase functionality preserved
- ✅ Variable thickness feature still works
- ✅ Drag-and-right-click erase still works
- ✅ Performance remains optimal

## Files Modified

- `src/tools/edge.py` - Updated mouse event handlers to prevent preview interference during drawing

## Related Issues

This fix resolves the flickering issue reported in Version 2.5.2 while maintaining all the advanced edge tool features including:
- Variable thickness support
- Right-click erase functionality  
- Enhanced distance detection
- Drag-and-right-click erase
- Deferred drawing optimization
