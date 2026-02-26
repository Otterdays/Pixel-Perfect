# Color Wheel & Constants — Implementation Reference

Reference for porting the Python Pixel Perfect color wheel and constants view to the C# WPF port.

**Source**: Python `src/ui/color_wheel.py`, `src/ui/palette_views/constants_view.py`, `src/ui/color_view_manager.py`  
**Docs**: `docs/features/COLOR_WHEEL_BUTTONS.md`

---

## 1. View Mode Architecture (Python)

The Python app has **6 view modes** in the palette panel, selected via radio buttons:

| Mode       | Description                                      |
|------------|--------------------------------------------------|
| **Grid**   | Palette colors (SNES Classic or selected palette) |
| **Primary**| 8 main colors + 24 variations                     |
| **Wheel**  | HSV color wheel + custom colors                   |
| **Constants** | Colors currently used on the canvas           |
| **Saved**  | User-saved custom colors (24 slots)               |
| **Recent** | Last 16 colors used while drawing                |

WPF currently has **Grid** only. This reference covers **Wheel** and **Constants**.

---

## 2. Color Wheel (HSV Picker)

### Purpose
HSV-based color selection for any RGB color. Lets users pick colors outside the palette.

### UI Components (Python `color_wheel.py`)

1. **Hue wheel** (ring, ~250×250px)
   - Circular gradient: 0°=red, 120°=green, 240°=blue
   - Click/drag on ring to set hue (0–360°)
   - Drawn with PIL: for each pixel in ring, `angle → hue`, `rgb = hsv_to_rgb(hue, 1, 1)`

2. **Saturation/Value square** (180×180px)
   - X-axis: saturation (0% left → 100% right)
   - Y-axis: value/brightness (100% top → 0% bottom)
   - Gradient uses current hue; click/drag to set S and V

3. **Color preview** (100×100 frame, shows current color)

4. **HEX label** (e.g. `#FF0000`)

5. **HSV labels** (H: 0°, S: 100%, V: 100%)

6. **RGB entry fields** (R, G, B 0–255; editable, updates wheel on change)

7. **Brightness slider** (0–100, affects value)

8. **Save Custom Color** (green) — adds current color to custom colors

9. **Delete Color** (red) — removes selected custom color

10. **Custom Colors grid** (4 columns, scrollable) — user-saved colors; click to load into wheel

### HSV ↔ RGB Conversion
- `_hsv_to_rgb(h, s, v)` — standard HSV→RGB
- `_rgb_to_hsv(r, g, b)` — standard RGB→HSV

### Callbacks
- `on_color_changed(rgb)` — fired when color changes; updates `CurrentColor` and canvas preview
- `on_save_custom_color` — add to CustomColorManager
- `on_remove_custom_color` — remove from CustomColorManager

### Methods
- `get_color() -> (r, g, b)`
- `set_color(r, g, b)` — load color into wheel from external source (e.g. eyedropper, constants click)

### WPF Port Notes
- Use `System.Windows.Media` or custom drawing for hue ring and saturation square
- WPF `Color` has `GetHue()`, `GetSaturation()`, `GetBrightness()` (0–1) — can map to HSV
- Or implement HSV↔RGB manually (Python logic is straightforward)
- Consider `UserControl` for the wheel; bind to ViewModel `CurrentColor`

---

## 3. Constants View (Used Colors)

### Purpose
Shows **unique colors currently on the canvas** (all visible layers composited). Lets users quickly reselect colors they’re already using.

### Data Source (Python)
```python
def _get_canvas_colors(self) -> List[Tuple[int,int,int,int]]:
    unique_colors = set()
    for y in range(self.canvas.height):
        for x in range(self.canvas.width):
            pixel_color = self.canvas.get_pixel(x, y)  # composited
            if pixel_color[3] > 0:  # skip transparent
                unique_colors.add(tuple(pixel_color))
    return sorted(list(unique_colors))
```

Python `canvas.get_pixel(x, y)` returns the **composited** pixel (all visible layers blended).

### WPF Equivalent
`PixelCanvas` already has:
```csharp
public PixelColor GetCompositePixel(int x, int y)
```
Returns composited color at (x,y) from all visible layers. Use this to build the unique color set.

### UI (Python)
- Grid of color buttons (4 columns, 50×50px)
- If no colors: "No colors used yet. Draw on canvas to see colors here."
- Count label: "N colors in use"
- Click: if color is in current palette → select palette index; else → switch to Wheel view and `color_wheel.set_color(r,g,b)`

### Refresh
Constants view is **recreated** when the user switches to it (`constants_view.create()`). So it always reflects the current canvas state.

### WPF Port Notes
- Add `GetUsedColors()` or similar on `PixelCanvas` or ViewModel: iterate Width×Height, call `GetCompositePixel`, collect unique non-transparent `PixelColor`s
- Bind to `ObservableCollection<PixelColor>`; refresh when switching to Constants view or when canvas changes (e.g. `PixelChanged`)

---

## 4. View Switching (Python)

- `ColorViewManager.show_view(mode)` hides all view frames, then shows the requested one
- Wheel is **recreated** when switching to it (it lives in `palette_content_frame`, which is cleared when switching views)
- Constants view `create()` is called when switching to "constants" — it scans the canvas and builds the grid

### WPF Approach
- Use a `ContentControl` or similar with `Content` bound to the current view
- Or use `Visibility` on separate panels (Grid, Wheel, Constants)
- View mode: `Grid` | `Wheel` | `Constants` as enum or string; radio buttons or ComboBox to switch

---

## 5. Custom Colors (Wheel Feature)

- **CustomColorManager** stores user colors (max 32)
- Persisted to `AppData\Local\PixelPerfect\custom_colors.json`
- Color wheel has "Save Custom Color" and "Delete Color" buttons
- Custom colors grid is inside the wheel UI; colors can be selected and loaded into the wheel

WPF could implement a simple `CustomColorService` with JSON persistence, similar to `PaletteLoader`.

---

## 6. Integration Summary

| Component      | Python Source              | WPF Status / Need                          |
|----------------|----------------------------|--------------------------------------------|
| View mode UI   | Radio buttons (Grid/Wheel/Constants/…) | Add ComboBox or radio group for view mode |
| Color wheel    | `color_wheel.py`           | New `ColorWheelControl` or UserControl     |
| Constants      | `constants_view.py`       | New logic using `GetCompositePixel`        |
| Get canvas colors | `canvas.get_pixel` (composited) | `PixelCanvas.GetCompositePixel` ✅ exists |
| Custom colors  | CustomColorManager + JSON | New service + persistence                  |

---

## 7. Suggested Implementation Order

1. **Constants view** — simpler: scan canvas via `GetCompositePixel`, display grid, click → set `CurrentColor`. No new controls beyond a color grid.
2. **View mode selector** — add Grid | Wheel | Constants (or TabControl) to the palette panel.
3. **Color wheel** — HSV ring + saturation square + preview + RGB fields. Can start minimal (ring + square + preview) and add Save/Delete/Custom later.
