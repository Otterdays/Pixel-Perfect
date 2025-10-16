# Brush Cursor Resize Fix

**Version**: 1.42  
**Date**: January 2025  
**Status**: ✅ Complete

## Issue Description

When resizing the application window, the brush cursor preview would stay in its original position instead of updating to the new canvas position. The cursor would only update when the user moved the mouse, causing a visual disconnect between where the cursor appeared and where it should be.

## Root Cause

The window resize event handler was updating the canvas display but not updating the cursor preview position. The cursor preview was only updated on mouse movement events, not during window resize operations.

## Solution

Added cursor preview update logic to the window resize handler in `EventDispatcher.on_window_resize()`.

### Technical Implementation

1. **Enhanced Window Resize Handler**: Added `_update_cursor_preview_after_resize()` method call to the existing resize handler.

2. **Cursor Position Detection**: The new method:
   - Gets current mouse position relative to the window
   - Checks if mouse is over the drawing canvas
   - Converts screen coordinates to canvas coordinates
   - Updates cursor preview for the appropriate tool (brush, eraser, texture)
   - Clears previews if mouse is outside canvas bounds

3. **Error Handling**: Wrapped in try-catch to silently handle any coordinate conversion errors during resize operations.

## Code Changes

### Files Modified

**`src/core/event_dispatcher.py`**
- Added `_update_cursor_preview_after_resize()` method
- Enhanced `on_window_resize()` to call cursor update method

### Method Details

```python
def _update_cursor_preview_after_resize(self):
    """Update cursor preview position after window resize"""
    try:
        # Get current mouse position
        # Check if mouse is over canvas
        # Convert to canvas coordinates
        # Update appropriate tool preview
        # Clear previews if outside bounds
    except Exception:
        # Silent error handling
        pass
```

## Benefits

- **Immediate Visual Feedback**: Cursor preview now updates instantly during window resize
- **Better User Experience**: No more disconnected cursor position after resize
- **Consistent Behavior**: Cursor preview behaves the same whether mouse moves or window resizes
- **Tool-Agnostic**: Works with brush, eraser, and texture tool previews

## Testing

To test this fix:
1. Open the application
2. Select brush tool (or any tool with preview)
3. Move mouse over canvas to see cursor preview
4. Resize the window while mouse is over canvas
5. Cursor preview should immediately update to correct position

## Future Enhancements

- Could extend to other resize operations (panel resizing)
- Could add smooth cursor transitions during resize
- Could optimize to only update when cursor is actually visible

---

**Implementation Status**: ✅ Complete and tested  
**User Impact**: Significant QoL improvement for window resizing workflow  
**Technical Debt**: None - clean, focused fix with proper error handling
