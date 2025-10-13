# Copy Placement Preview Feature

**Version**: 1.19  
**Added**: October 13, 2025  
**Status**: Production Ready ✅

## Overview
The Copy Placement Preview feature provides real-time visual feedback when placing copied pixel selections. Users can see exactly where their copied pixels will be placed before clicking, with a semi-transparent preview that follows the mouse cursor.

## Visual Design

### Preview Appearance

#### Semi-Transparent Pixels
- **Rendering Method**: Tkinter stipple pattern (`gray50`)
- **Effect**: Checkerboard transparency showing underlying pixels
- **Purpose**: See both original canvas and copied pixels simultaneously
- **Color Accuracy**: Preserves actual pixel colors while showing transparency

#### Boundary Box
- **Color**: Cyan (`#00ffff`)
- **Style**: Dashed line (`dash=(4, 4)`)
- **Width**: 2 pixels
- **Purpose**: Clearly indicates placement area boundaries

#### Grid Snapping
- **Behavior**: Preview snaps to pixel grid automatically
- **Precision**: Exact pixel alignment for clean placement
- **Feedback**: Position updates in real-time with mouse movement

## User Workflow

### Complete Copy-Paste Process

1. **Select Pixels**
   ```
   - Use Selection tool (S)
   - Drag rectangle around desired pixels
   - Selection auto-switches to Move tool
   ```

2. **Copy Selection**
   ```
   - Click "Copy" button
   - Console: "[OK] Selection copied - click on canvas to place"
   - Console: "     Press Escape to cancel placement"
   - Cursor changes to placement mode
   ```

3. **Preview Placement**
   ```
   - Move mouse over canvas
   - Semi-transparent preview follows cursor
   - Preview shows exact placement position
   - Cyan dashed box indicates boundaries
   ```

4. **Place Copy**
   ```
   - Click on canvas to place at current position
   - Pixels are permanently placed
   - Console: "[OK] Copied pixels placed at X, Y"
   - Ready for another placement or action
   ```

5. **Cancel (Optional)**
   ```
   - Press Escape key to cancel
   - Preview disappears
   - No pixels placed
   - Console: "[INFO] Copy placement cancelled"
   ```

### Multiple Placements

You can place the same copied selection multiple times:

1. Copy pixels (once)
2. Move mouse → Click to place (first copy)
3. Move mouse → Click to place (second copy)
4. Move mouse → Click to place (third copy)
5. ...and so on

Each placement creates an independent copy of the original pixels.

## Technical Details

### Preview Rendering

#### Implementation Overview
```python
# Preview is drawn in _draw_selection_on_tkinter() method
if self.is_placing_copy and self.copy_preview_pos:
    # 1. Get copy buffer and dimensions
    # 2. Loop through each pixel
    # 3. Draw with stipple pattern for transparency
    # 4. Draw cyan dashed boundary
```

#### Pixel-by-Pixel Rendering
```python
for py in range(height):
    for px in range(width):
        # Get pixel color from buffer
        pixel_color = copy_buffer[py, px]
        
        # Only draw non-transparent pixels
        if pixel_color[3] > 0:
            # Convert to hex color
            color_hex = f'#{r:02x}{g:02x}{b:02x}'
            
            # Draw with transparency effect
            canvas.create_rectangle(
                x, y, x + zoom, y + zoom,
                fill=color_hex,
                stipple="gray50"  # Semi-transparent
            )
```

#### Boundary Box Rendering
```python
# Calculate screen coordinates
screen_x1 = x_offset + (preview_x * zoom)
screen_y1 = y_offset + (preview_y * zoom)
screen_x2 = screen_x1 + (width * zoom)
screen_y2 = screen_y1 + (height * zoom)

# Draw dashed cyan rectangle
canvas.create_rectangle(
    screen_x1, screen_y1, screen_x2, screen_y2,
    outline="cyan",
    width=2,
    dash=(4, 4)
)
```

### State Management

#### Copy State Variables
```python
# Copy/paste state
self.is_placing_copy = False      # Currently placing a copy?
self.copy_buffer = None           # Pixel data as numpy array
self.copy_dimensions = None       # (width, height) tuple
self.copy_preview_pos = None      # (x, y) mouse position
```

#### State Transitions
```
IDLE → [Click Copy] → PLACEMENT_MODE
PLACEMENT_MODE → [Click Canvas] → PLACED → PLACEMENT_MODE
PLACEMENT_MODE → [Press Escape] → IDLE
```

### Performance Optimization

#### Efficient Updates
- Preview only redraws when mouse moves
- Uses tagged canvas items for easy cleanup
- Minimal overhead for real-time updates
- Zoom-aware rendering for consistent appearance

#### Memory Management
- Copy buffer stored as numpy array (efficient)
- Only one copy buffer active at a time
- Automatic cleanup when starting new copy
- No memory leaks during multiple placements

## Visual Examples

### Example 1: Copying a Small Sprite
```
[Before Copy]
Canvas: ................
        ....XXXX........
        ....XXXX........
        ................

[During Preview]
Canvas: ................
        ....XXXX........
        ....XXXX........  [stippled preview at cursor]
        ......[XXXX].... <- Cyan dashed box
        ................

[After Placement]
Canvas: ................
        ....XXXX........
        ....XXXX........
        ......XXXX...... <- Placed copy
        ................
```

### Example 2: Multiple Placements
```
[Original Selection]
    ██
    ██

[After 3 Placements]
    ██  ██      ██
    ██  ██      ██
```

## Integration with Other Features

### Works With
- **Selection Tool**: Required for initial selection
- **Move Tool**: Often used after copying
- **Rotate/Mirror**: Can transform before copying
- **Scale**: Can scale selection before copying
- **Layers**: Respects current layer

### Doesn't Interfere With
- **Drawing Tools**: Can't draw while placing
- **Palette Selection**: Maintains selected colors
- **Zoom**: Preview scales correctly at all zoom levels
- **Grid Display**: Preview respects grid visibility

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Escape` | Cancel copy placement |
| `S` | Switch to Selection tool (exits placement) |

**Note**: Most keyboard shortcuts are disabled during copy placement to prevent accidental actions.

## Use Cases

### 1. Pattern Creation
**Scenario**: Creating repeating patterns or textures

**Steps**:
1. Draw one tile (e.g., 8x8)
2. Select the tile
3. Click Copy
4. Place copies in grid pattern
5. Creates seamless repeating texture

**Example**: Grass tiles, brick walls, checkerboard patterns

### 2. Element Duplication
**Scenario**: Multiple identical objects in scene

**Steps**:
1. Draw one object (tree, cloud, star)
2. Select and copy
3. Place copies around scene
4. Modify each copy as needed

**Example**: Forest with multiple trees, starry sky

### 3. Symmetry Creation
**Scenario**: Mirror artwork for symmetrical designs

**Steps**:
1. Draw left half
2. Select left half
3. Click Mirror
4. Click Copy
5. Place on right side

**Example**: Symmetrical characters, logos, UI elements

### 4. Animation Frames
**Scenario**: Creating animation with similar frames

**Steps**:
1. Draw base frame
2. Select and copy
3. Place in next frame position
4. Modify slightly for animation
5. Repeat for all frames

**Example**: Walking cycles, blinking eyes, bouncing balls

## Tips and Best Practices

### For Best Results

1. **Use Preview for Alignment**
   - Watch the preview position carefully
   - Align with existing pixels before clicking
   - Cyan box shows exact boundaries

2. **Plan Multiple Placements**
   - Visualize final layout before placing
   - Place copies in logical order
   - Leave space for variations

3. **Combine with Transformations**
   - Rotate before copying for varied angles
   - Mirror for flipped versions
   - Scale for size variations

4. **Check Transparency**
   - Preview shows which pixels will be placed
   - Transparent areas in preview = transparent in copy
   - Non-transparent pixels overwrite existing pixels

### Common Patterns

#### Grid Pattern
```python
1. Copy small tile
2. Place in row: Click, move right, click, move right...
3. Move to next row
4. Repeat placements
```

#### Scattered Pattern
```python
1. Copy element
2. Place randomly: Click here, click there...
3. Vary positions for natural look
4. Overlap for depth (layers)
```

#### Symmetrical Pattern
```python
1. Copy left side
2. Mirror the copy
3. Place on right side
4. Align carefully with preview
```

## Console Messages

| Message | Meaning |
|---------|---------|
| `[OK] Selection copied - click on canvas to place` | Copy successful, ready to place |
| `     Press Escape to cancel placement` | Instructions for canceling |
| `[OK] Copied pixels placed at X, Y` | Placement successful at coordinates |
| `[INFO] Copy placement cancelled` | User pressed Escape |

## Troubleshooting

### Preview Not Visible
**Problem**: Can't see preview after copying

**Solutions**:
- Move mouse over canvas area
- Check that selection had non-transparent pixels
- Verify "Copy" button was clicked successfully
- Look for console message confirming copy

### Preview Position Wrong
**Problem**: Preview not appearing where expected

**Solutions**:
- Remember preview position is top-left corner
- Account for zoom level (preview scales with zoom)
- Ensure mouse is within canvas bounds
- Check grid alignment if enabled

### Pixels Not Placing
**Problem**: Clicking doesn't place the copy

**Solutions**:
- Ensure you're in placement mode (check console)
- Click within canvas bounds (not outside)
- Verify copy buffer exists (recent copy)
- Try clicking again (single click should work)

### Preview Too Faint
**Problem**: Hard to see semi-transparent preview

**Solutions**:
- This is intentional design (shows both layers)
- Use cyan boundary box to see bounds
- Zoom in for better visibility
- Look for stipple pattern (checkerboard)

### Multiple Unwanted Copies
**Problem**: Accidentally placed too many copies

**Solutions**:
- Use Undo feature (if available)
- Press Escape before placing more
- Select and delete unwanted copies
- More careful clicking in future

## Related Features

- [Copy Selection](CUSTOM_COLORS_FEATURE_SUMMARY.md) - The copy button that activates this feature
- [Selection Tool](../README.md#selection-tool) - Required for copying
- [Move Tool](../README.md#move-tool) - Similar drag-and-drop behavior
- [Interactive Scaling](INTERACTIVE_SCALING.md) - Often used before copying

## Future Enhancements

### Potential Additions (Not Yet Implemented)
- [ ] Adjustable transparency for preview (slider)
- [ ] Toggle preview on/off while maintaining placement mode
- [ ] Snap-to-grid options (align to 8x8, 16x16, etc.)
- [ ] Copy counter showing number of placements
- [ ] Keyboard shortcuts for precise positioning (arrow keys)
- [ ] Right-click to cancel placement
- [ ] Preview rotation during placement (R key)

## Technical Notes

### Tkinter Stipple Patterns
Available patterns for transparency effect:
- `gray12` - Very light (12% fill)
- `gray25` - Light (25% fill)
- `gray50` - Medium (50% fill) ← **Currently used**
- `gray75` - Dark (75% fill)

We use `gray50` for optimal visibility of both layers.

### Canvas Tag System
Preview uses `"copy_preview"` tag for easy cleanup:
```python
# Draw preview with tag
canvas.create_rectangle(..., tags="copy_preview")

# Clear all preview elements
canvas.delete("copy_preview")
```

### Coordinate Systems
Three coordinate systems involved:
1. **Canvas Coordinates**: Pixel positions (0-width, 0-height)
2. **Screen Coordinates**: Tkinter display positions (includes zoom)
3. **Mouse Coordinates**: Raw event positions (converted to canvas)

Preview correctly handles all three systems for accurate display.

---

**Last Updated**: October 13, 2025  
**Feature Version**: 1.19  
**Maintainer**: Pixel Perfect Development Team

