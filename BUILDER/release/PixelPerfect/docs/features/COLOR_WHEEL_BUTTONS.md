# Color Wheel Buttons - Technical Reference

## Button Layout (Version 1.11)

The Color Wheel has **2 buttons** for managing custom colors:

```
┌─────────────────────────────┐
│    Save Custom Color        │ (Green)
├─────────────────────────────┤
│    Delete Color             │ (Red)
└─────────────────────────────┘
```

---

## Save Custom Color (Green Button)

### Purpose
Permanently save the current color wheel color to user's Custom Colors library.

### Function
```python
def _save_custom_color(self):
    """Save current color to custom colors"""
    rgb = self._hsv_to_rgb(self.hue, self.saturation, self.value)
    rgba = (rgb[0], rgb[1], rgb[2], 255)
    
    if custom_colors.add_color(rgba):
        print("✅ Saved custom color")
        update_custom_colors_display()
    else:
        print("⚠️ Duplicate or limit reached")
```

### Workflow
1. User adjusts color wheel to desired color
2. User clicks "Save Custom Color"
3. Color is added to `CustomColorManager`
4. Saved to `AppData\Local\PixelPerfect\custom_colors.json`
5. Grid updates to show new color
6. Success/warning message in console

### Feedback Messages
- `[OK] Saved custom color: (r, g, b, a)` - Success
- `[WARN] Color already in custom colors: (r, g, b, a)` - Duplicate
- `[WARN] Custom colors full (max 32)` - Limit reached

---

## Delete Color (Red Button)

### Purpose
Remove a selected custom color from the user's library.

### Function
```python
def _delete_selected_color(self):
    """Delete the currently selected custom color"""
    if self.selected_custom_color:
        self._remove_custom_color(self.selected_custom_color)
    else:
        print("⚠️ No custom color selected")
```

### Workflow
1. User clicks a custom color in the grid (gets white border)
2. User clicks "Delete Color" button
3. Color is removed from `CustomColorManager`
4. Removed from `custom_colors.json`
5. Grid updates to remove the color
6. Deletion message in console

### Selection Indicator
- **Unselected**: No border
- **Selected**: 3px white border
- **Hover**: Brightened color

### Feedback Messages
- `[DELETE] Removed custom color: (r, g, b, a)` - Success
- `[WARN] No custom color selected. Click a custom color first.` - No selection

---

## Custom Colors Grid

### Display
- **Layout**: 4 columns, dynamic rows
- **Button Size**: 40x40 pixels
- **Spacing**: 3px between buttons
- **Container**: Scrollable frame (150px height)

### Interactions
- **Left-Click**: Select color (loads into wheel + marks with white border)
- **Delete Button**: Remove selected color

### Visual States
```
Normal:     No border
Selected:   3px white border
Hover:      Brightened (+30 RGB)
```

---

## Removed Buttons (v1.11 Update)

### Previously Had (Removed)
1. ~~"Add to Palette"~~ - Removed (simplified workflow)
2. ~~"Replace Color"~~ - Replaced with "Delete Color"

### Why Removed?
- **Simplified workflow**: One clear purpose - manage custom colors
- **Less confusion**: Color Wheel = Custom Colors only
- **Clearer separation**: Grid/Primary views for palette, Wheel for custom colors

---

## Integration Points

### main_window.py Connections
```python
# Initialize custom colors manager
self.custom_colors = CustomColorManager()

# Connect color wheel buttons
self.color_wheel._save_custom_color = self._save_custom_color
self.color_wheel._remove_custom_color = self._remove_custom_color

# Update display
self._update_custom_colors_display()
```

### Save Custom Color Flow
```
ColorWheel._save_custom_color()
  ↓
MainWindow._save_custom_color()
  ↓
CustomColorManager.add_color(rgba)
  ↓
Save to custom_colors.json
  ↓
MainWindow._update_custom_colors_display()
  ↓
ColorWheel.update_custom_colors_grid(colors)
```

### Delete Color Flow
```
ColorWheel._delete_selected_color()
  ↓
ColorWheel._remove_custom_color(color)
  ↓
MainWindow._remove_custom_color(color)
  ↓
CustomColorManager.remove_color_by_value(color)
  ↓
Save updated JSON
  ↓
MainWindow._update_custom_colors_display()
  ↓
ColorWheel.update_custom_colors_grid(colors)
```

---

## Style Guide

### Button Styling
```python
# Save Custom Color (Green)
fg_color="green"
height=30
text="Save Custom Color"

# Delete Color (Red)
fg_color="red"
height=30
text="Delete Color"
```

### Consistent with App Theme
- **Height**: 30px (standard button height)
- **Full Width**: `pack(fill="x")`
- **Spacing**: 2px vertical padding
- **Font**: Default (10px)

---

## User Flow Examples

### Saving Colors
```
1. Adjust hue wheel → red
2. Adjust saturation/brightness → perfect red
3. Click "Save Custom Color"
4. Color appears in grid with white border (selected)
5. Create another color...
```

### Deleting Colors
```
1. Click a custom color in grid (white border appears)
2. Click "Delete Color" button
3. Color removed from grid
4. Selection cleared
```

### Reusing Saved Colors
```
1. Click saved custom color in grid
2. Color loads into wheel
3. Modify if needed
4. Use for drawing (palette selection)
```

---

**Version**: 1.11  
**Last Updated**: October 11, 2025  
**Module**: `src/ui/color_wheel.py`

