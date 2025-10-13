# Interactive Selection Scaling Feature

**Version**: 1.19  
**Added**: October 13, 2025  
**Status**: Production Ready ✅

## Overview
The Interactive Scaling feature allows users to resize selected pixel regions using draggable corner and edge handles. This powerful tool enables smart upscaling of artwork from smaller canvas sizes (e.g., 32x32) to larger ones (e.g., 64x64) while maintaining pixel-perfect quality.

## User Interface

### Scale Button
- **Location**: Below Selection Operations (Mirror, Rotate, Copy)
- **Appearance**: Full-width gray button
- **Text**: "Scale"
- **Tooltip**: "Scale selection with draggable corners" (appears after 1 second hover)
- **Active State**: Button turns blue when in scaling mode, all tool buttons turn gray
- **Visual Feedback**: Clear indication that scaling mode is active, not a drawing tool

### Visual Indicators

#### Selection Handles
When in scaling mode, the selection rectangle displays interactive handles:

- **Corner Handles** (Yellow, 8x8 pixels)
  - Top-left, top-right, bottom-left, bottom-right
  - Drag to scale proportionally
  - Diagonal resize cursor (⬁) appears on hover
  - Useful for overall size adjustments

- **Edge Handles** (Orange, 8x8 pixels)
  - Top, bottom, left, right (centered on edges)
  - Drag to scale in one dimension only
  - Directional resize cursors (↕ or ↔) appear on hover
  - Useful for width or height adjustments

- **Handle Styling**
  - Filled colored squares with black outline (1px)
  - Highly visible against any background
  - Remains consistent across zoom levels

#### Dynamic Cursors
The cursor changes automatically to indicate available actions:
- **Arrow cursor**: Default in scaling mode (away from handles)
- **Diagonal cursors**: Hover over corner handles (⬁ or ⬂)
- **Vertical cursor**: Hover over top/bottom edges (↕)
- **Horizontal cursor**: Hover over left/right edges (↔)
- **Tool cursor**: Returns to current tool's cursor after exiting scaling

## Workflow

### Basic Scaling Process

1. **Select Pixels**
   - Use Selection tool (S) to select a region
   - Move tool activates automatically

2. **Enter Scaling Mode**
   - Click the "Scale" button
   - Yellow and orange handles appear on selection
   - Console message: "[OK] Scaling mode - drag corners/edges to resize"

3. **Drag Handles**
   - Click and drag any handle to resize
   - Selection rectangle updates in real-time
   - Minimum size: 1x1 pixels

4. **Apply Scale**
   - Click anywhere outside the selection to apply
   - Pixels are scaled using nearest-neighbor algorithm
   - Console message: "[OK] Scaled from WxH to WxH"

5. **Exit Scaling Mode**
   - **Press Escape**: Cancel without applying changes
   - **Click any tool button**: Exit scaling and switch to that tool
   - **Click Mirror/Rotate/Copy**: Exit scaling and perform that operation
   - Selection rectangle dimensions preserved until applied
   - Console message: "[INFO] Exited scaling mode"

6. **Multiple Drag Operations**
   - Can drag handles multiple times before applying
   - Each drag starts from the current rectangle position
   - Rectangle updates in real-time during each drag
   - Click away from selection when satisfied with size

### Advanced Techniques

#### Proportional Scaling
- Drag corner handles to scale width and height together
- Maintains aspect ratio based on drag direction
- Ideal for uniform size changes

#### One-Dimensional Scaling
- Drag edge handles to scale only width OR height
- Other dimension remains unchanged
- Perfect for stretching or compressing in one direction

#### Precise Upscaling
Common use case: Upscaling 32x32 artwork to 64x64 canvas
1. Select your 32x32 sprite
2. Click Scale
3. Drag bottom-right corner to double the size
4. Click away to apply
5. Artwork now has 4x the pixels for detail enhancement

## Technical Details

### Scaling Algorithm

#### Primary Method: SciPy
```python
from scipy import ndimage

scaled_pixels = ndimage.zoom(
    selection_tool.selected_pixels,
    (scale_y, scale_x, 1),
    order=0  # Nearest-neighbor interpolation
)
```

**Characteristics:**
- High-quality nearest-neighbor scaling
- Maintains crisp pixel art edges
- No anti-aliasing or blurring
- Fast performance for real-time preview

#### Fallback Method: Pure NumPy
If scipy is unavailable, a pure numpy implementation is used:
```python
# Map each new pixel to closest original pixel
ox = int(nx * old_width / new_width)
oy = int(ny * old_height / new_height)
scaled_pixels[ny, nx] = original_pixels[oy, ox]
```

**Characteristics:**
- Identical visual results to scipy
- Slightly slower for large selections
- No additional dependencies required

### Handle Detection

**Zoom-Adaptive Tolerance:**
```python
handle_tolerance = max(3, 8 // zoom)
```

This ensures handles are easy to click at any zoom level:
- At 1x zoom: 8 pixel tolerance
- At 2x zoom: 4 pixel tolerance
- At 4x zoom: 3 pixel tolerance (minimum)

**Priority Order:**
1. Corner handles (checked first)
2. Edge handles (checked second)
3. No handle (click outside applies scale)

### Performance Optimization

- **Real-Time Preview**: Rectangle updates during drag without resampling pixels
- **Lazy Scaling**: Actual pixel scaling only occurs when applying (clicking outside)
- **Efficient Redraw**: Only selection area is redrawn during preview
- **Minimum Size Check**: Prevents invalid sizes (< 1x1 pixels)

## Use Cases

### 1. Smart Upscaling
**Scenario**: Created 32x32 sprite, now need 64x64 version with more detail

**Steps**:
1. Select entire 32x32 canvas
2. Switch to 64x64 canvas (File → New → 64x64)
3. Click Scale
4. Drag corner handle to 64x64
5. Click to apply
6. Add detail to the larger version

### 2. Element Resizing
**Scenario**: Character sprite too large for scene

**Steps**:
1. Select character pixels
2. Click Scale
3. Drag corner handle to desired size
4. Click to apply
5. Character now fits composition

### 3. Stretching UI Elements
**Scenario**: Button needs to be wider but same height

**Steps**:
1. Select button pixels
2. Click Scale
3. Drag right edge handle to increase width
4. Click to apply
5. Button stretched horizontally

### 4. Creating Size Variations
**Scenario**: Need 16x16, 32x32, and 64x64 versions of logo

**Steps**:
1. Create 16x16 original
2. Copy → Paste → Scale to 32x32
3. Copy → Paste → Scale to 64x64
4. Export all three versions

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Escape` | Cancel scaling mode |
| `S` | Switch to Selection tool |
| `M` | Switch to Move tool |

## Tips and Best Practices

### For Best Results

1. **Start Small, Scale Up**
   - Create base artwork at smallest intended size
   - Scale up to add detail at larger sizes
   - Maintains consistency across size variations

2. **Use Nearest-Neighbor Only**
   - Never use smooth/bilinear scaling for pixel art
   - Pixel Perfect uses nearest-neighbor exclusively
   - Preserves crisp pixel boundaries

3. **Scale Before Detail Work**
   - Upscale first, then add fine details
   - More efficient than redrawing at larger size
   - Maintains base structure while adding complexity

4. **Test Multiple Sizes**
   - Create copies at different scales
   - Test readability at each size
   - Ensure recognizability at all scales

### Common Pitfalls

1. **Scaling Too Much**
   - ❌ Scaling 8x8 to 256x256 creates blocky results
   - ✅ Scale incrementally: 8→16→32→64→128

2. **Forgetting to Apply**
   - ❌ Switching tools without clicking outside
   - ✅ Always click away from selection to apply

3. **Wrong Handle Type**
   - ❌ Using corner handle for width-only change
   - ✅ Use edge handles for single-dimension scaling

## Console Messages

| Message | Meaning |
|---------|---------|
| `[OK] Scaling mode - drag corners/edges to resize` | Scaling mode activated successfully |
| `[INFO] Release drag - click away from selection to apply scale` | Handle drag completed, ready to apply |
| `[OK] Scaled from 16x16 to 32x32` | Scaling applied successfully |
| `[INFO] Scaling cancelled` | User pressed Escape, no changes applied |
| `[WARN] scipy not available, using simple scaling` | Fallback algorithm in use (still works perfectly) |

## Technical Architecture

### State Management
```python
# Scaling state variables
self.is_scaling = False           # Currently in scaling mode?
self.scale_handle = None          # Which handle being dragged?
self.scale_start_pos = None       # Mouse position at drag start
self.scale_original_rect = None   # Selection bounds before scaling
```

### Mouse Event Flow
1. **Mouse Down**: Detect handle click or apply scale
2. **Mouse Move**: Update rectangle during drag
3. **Mouse Up**: Release handle, ready for next drag or apply

### Integration Points
- **Selection Tool**: Provides selected pixel data
- **Canvas**: Target for scaled pixels
- **Layer Manager**: Updates active layer with scaled pixels
- **Undo Manager**: Records scale operation (future enhancement)

## Future Enhancements

### Potential Additions (Not Yet Implemented)
- [ ] Lock aspect ratio checkbox for corner handles
- [ ] Numerical input for exact dimensions
- [ ] Scale percentage display during drag
- [ ] Undo/redo support for scale operations
- [ ] Multiple scaling algorithms (2xSaI, HQx, etc.)
- [ ] Preview overlay showing final result before applying

## Related Features
- [Selection Tool](../README.md#selection-tool) - Prerequisite for scaling
- [Copy Feature](CUSTOM_COLORS_FEATURE_SUMMARY.md) - Often used together for size variations
- [Move Tool](../README.md#move-tool) - Activates after selection
- [Canvas Sizes](../README.md#canvas-sizes) - Different canvas sizes for scaling between

## Troubleshooting

### Handle Not Responding
**Problem**: Clicking handle doesn't start drag

**Solutions**:
- Ensure you're in scaling mode (click Scale button first)
- Click directly on the colored handle squares
- Try zooming in for larger click targets

### Scale Not Applying
**Problem**: Dragging handle but pixels don't scale

**Solutions**:
- Remember to click outside selection after dragging
- Don't switch tools before applying
- Check console for error messages

### Blocky Results
**Problem**: Scaled pixels look too blocky

**Solutions**:
- This is expected for large scale factors
- Consider scaling incrementally (2x, then 2x again)
- Add detail manually after scaling
- Remember: pixel art is intentionally blocky!

### Performance Issues
**Problem**: Lag during scaling

**Solutions**:
- Close other applications to free RAM
- Reduce canvas size if extremely large
- Use edge handles for single-dimension scaling (faster)
- Install scipy for better performance

---

**Last Updated**: October 13, 2025  
**Feature Version**: 1.19  
**Maintainer**: Pixel Perfect Development Team

