# Pan Tool - Camera View Navigation

## Overview
The Pan Tool allows you to move the camera view around the canvas, providing an intuitive way to navigate large canvases or zoomed-in views without changing your actual artwork.

## Features

### Visual Cursor Feedback
- **Open Hand Cursor**: When hovering with pan tool selected
- **Grabbing Hand Cursor**: While actively dragging the view

### Interaction
1. Select the Pan tool from the tool panel
2. Click and drag anywhere on the canvas
3. The view moves in the direction you drag
4. Release to stop panning

## Use Cases

### Zoomed-In Editing
When working at high zoom levels (16x, 32x), the pan tool makes it easy to navigate around your artwork without constantly zooming in and out.

### Large Canvas Navigation
For larger canvases (64x64), the pan tool provides quick navigation to different areas of your artwork.

### Precision Work
Move the view to center specific areas of your canvas for detailed pixel work.

## Technical Details

### Coordinate System
- Pan offset is stored in canvas pixel coordinates
- Offset is multiplied by zoom level for screen-space rendering
- All mouse coordinates are adjusted for pan offset

### Implementation
- **File**: `src/tools/pan.py`
- **State Variables**: `pan_offset_x`, `pan_offset_y` in MainWindow
- **Cursor Types**: 
  - Default: `hand2` (open hand)
  - Dragging: `fleur` (grabbing hand with 4-way arrows)

### Event Handling
1. **Mouse Down**: Records starting position, begins panning
2. **Mouse Drag**: Calculates delta, updates offsets, redraws canvas
3. **Mouse Up**: Ends panning, restores open hand cursor

## Integration with Other Tools

### Switching Tools
- Pan tool can be switched to/from like any other tool
- Current pan position is maintained when switching tools
- Drawing tools work normally with panned view

### Coordinate Consistency
- All drawing operations account for pan offset
- Selection rectangles render correctly with panned view
- Copy/paste operations place pixels relative to panned view

## Keyboard Shortcut (Future)
**Planned**: Hold Space bar to temporarily activate pan tool, regardless of current tool selection.

## Tips

1. **Quick Reset**: Switch canvas size or zoom to reset pan position
2. **Combined with Zoom**: Use pan + high zoom for detailed pixel work
3. **Navigation**: Pan around large reference images or complex scenes
4. **Preview**: Pan to see different areas without accidentally drawing

## Known Limitations

### Version 1.21
- No visual indicator of pan amount/direction
- No "center view" button to reset pan
- Space bar shortcut not yet implemented
- Pan bounds not limited (can pan beyond canvas edges)

### Future Enhancements
- Center view button
- Pan amount indicator
- Space bar temporary activation
- Bounded panning (optional)
- Pan animation/smoothing
- Mini-map for navigation

## Code Example

### Using Pan Tool in Code
```python
# Select pan tool
self.current_tool = "pan"
tool = self.tools["pan"]

# Start panning
tool.on_mouse_down(x, y, None, None)

# Update pan during drag
dx, dy = tool.on_mouse_drag(new_x, new_y, None, None)
self.pan_offset_x += dx
self.pan_offset_y += dy

# End panning
tool.on_mouse_up(final_x, final_y, None, None)
```

### Applying Pan Offset
```python
# In coordinate conversion
canvas_coord_x -= self.pan_offset_x
canvas_coord_y -= self.pan_offset_y

# In rendering
x_offset += self.pan_offset_x * self.canvas.zoom
y_offset += self.pan_offset_y * self.canvas.zoom
```

## Version History

### v1.21 (October 13, 2025)
- Initial implementation
- Open hand and grabbing hand cursors
- Real-time view panning
- Integration with coordinate system

