# Mirror & Rotate Ghost Pixels Fix

**Date**: October 18, 2025  
**Status**: ✅ **FIXED**  
**Priority**: High  

## Problem Description
Selected pixels that were Mirrored or Rotated caused ghost pixels to remain on the canvas after being moved to another spot. The original pixels would not be properly cleared, leaving duplicate copies behind.

## Root Cause

### Mirror Selection Issue
The `mirror_selection()` method was writing **ALL pixels (including transparent ones)** directly to the layer without:
1. First clearing the original non-transparent pixels
2. Checking if pixels were transparent before writing

```python
# OLD CODE - BROKEN
for py in range(height):
    for px in range(width):
        pixel_color = tuple(mirrored_pixels[py, px])  # Gets ALL pixels
        draw_layer.set_pixel(canvas_x, canvas_y, pixel_color)  # Writes transparent pixels too!
```

**Problem**: Transparent pixels in the selection rectangle would overwrite the canvas background, and original pixels were never cleared.

### Rotate Selection Issue
The `apply_rotation()` method had a similar issue - it cleared pixels based on the backup, but didn't properly handle the two-step process:
1. Clear original non-transparent pixels
2. Place ONLY non-transparent transformed pixels

## Solution
Both methods now follow the **same pattern as MoveTool.finalize_move()** which works correctly:

### Step 1: Clear Original Non-Transparent Pixels
```python
# Clear ONLY non-transparent pixels from original position
for py in range(min(height, selection_tool.selected_pixels.shape[0])):
    for px in range(min(width, selection_tool.selected_pixels.shape[1])):
        pixel_color = tuple(selection_tool.selected_pixels[py, px])
        if pixel_color[3] > 0:  # Only clear non-transparent pixels
            canvas_x = left + px
            canvas_y = top + py
            if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                draw_layer.set_pixel(canvas_x, canvas_y, (0, 0, 0, 0))
```

### Step 2: Place Only Non-Transparent Transformed Pixels
```python
# Place ONLY non-transparent mirrored/rotated pixels
for py in range(min(height, transformed_pixels.shape[0])):
    for px in range(min(width, transformed_pixels.shape[1])):
        pixel_color = tuple(transformed_pixels[py, px])
        if pixel_color[3] > 0:  # Only place non-transparent pixels
            canvas_x = left + px
            canvas_y = top + py
            if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                draw_layer.set_pixel(canvas_x, canvas_y, pixel_color)
```

## Key Insight
**Transparent pixels in a selection are just empty space in the selection rectangle** - they should NEVER be written to the layer as they would overwrite background pixels underneath.

## Files Modified
- `src/ui/selection_manager.py`:
  - Fixed `mirror_selection()` method (lines 66-133)
  - Fixed `apply_rotation()` method (lines 194-254)

## Testing
Test the fix by:
1. Select some pixels with empty space in the selection
2. Mirror them - verify no ghost pixels remain
3. Move the mirrored selection elsewhere - verify original area is clean
4. Repeat test with Rotate operation
5. Verify transparency is preserved in both operations

## Benefits
✅ No more ghost pixels after mirror/rotate operations  
✅ Consistent behavior with move tool  
✅ Proper transparency handling  
✅ Clean pixel clearing before transformations  
✅ Selection transformations work correctly when moved  

---

**Technical Note**: This fix ensures that mirror and rotate operations handle pixels the exact same way as the move tool - only non-transparent pixels are cleared from original positions and only non-transparent pixels are placed at new positions. Transparent pixels (empty space in selection rectangles) are never written to the layer.


