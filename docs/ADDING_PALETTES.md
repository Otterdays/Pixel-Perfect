# How to Add New Color Palettes to Pixel Perfect

This guide explains how to add new color palettes to Pixel Perfect.

## Overview

Pixel Perfect supports custom color palettes for different art styles. Palettes are available from built-in presets and are now dynamically loaded from JSON files in `assets/palettes/`.

There are two ways to add palettes:
- Preferred: Add a JSON file to `assets/palettes/` (no code changes)
- Legacy/Advanced: Hardcode palettes in `src/core/color_palette.py`

## Steps to Add a New Palette

### 1. Add a JSON Palette (Preferred)

Create a JSON file in `assets/palettes/` with your palette colors. The app auto-discovers palettes at startup and lists them in the Palette dropdown.

```json
{
  "name": "Your Palette Name",
  "type": "your_palette_type",
  "description": "Description of the palette aesthetic and use case",
  "colors": [
    [0, 0, 0, 255],
    [255, 255, 255, 255],
    [128, 64, 0, 255],
    ...
  ]
}
```

**Notes:**
- Each color is `[R, G, B, A]` format
- Include exactly **16 colors**
- Alpha should always be `255` (fully opaque)
- If the JSON `name` matches a preset name, it appears as `Name (JSON)` to avoid collisions.
- After adding a file, restart the app to rescan palettes.

### 2. Test Your JSON Palette

1. Run the application: `python main.py`
2. Open the **Palette** dropdown in the left panel
3. Select your palette by its `name`
4. Verify all 16 colors display correctly

### 3. Example: Grass Palette

`assets/palettes/grass.json`:
```json
{
  "name": "Grass",
  "type": "custom",
  "description": "16 variations of natural grass coloration",
  "colors": [
    [18, 38, 18, 255], [28, 56, 26, 255], [38, 74, 30, 255], [50, 92, 36, 255],
    [62, 110, 42, 255], [74, 128, 48, 255], [88, 146, 56, 255], [102, 164, 64, 255],
    [120, 176, 74, 255], [138, 188, 84, 255], [156, 200, 94, 255], [174, 212, 104, 255],
    [192, 220, 116, 255], [208, 228, 128, 255], [134, 160, 80, 255], [100, 130, 70, 255]
  ],
  "primary_color": 0,
  "secondary_color": 1
}
```

---

## Legacy/Advanced: Hardcode a Palette in Source

If you need to ship a palette as a built-in preset (without JSON), you can hardcode it. This is optional; most users should prefer JSON.

### A. Add to PaletteType Enum (if not `custom`)

Edit `src/core/color_palette.py` - Add your palette type to the enum:

```python
class PaletteType(Enum):
    """Types of color palettes"""
    SNES_CLASSIC = "snes_classic"
    CURSE_OF_AROS = "curse_of_aros"
    HEARTWOOD = "heartwood"
    DEFINYA = "definya"
    KAKELE = "kakele"
    RUCOY = "rucoy"
    OLD_SCHOOL_RUNESCAPE = "old_school_runescape"
    YOUR_PALETTE = "your_palette"  # <-- ADD HERE
    CUSTOM = "custom"
```

### B. Add to get_preset_palettes()

Edit `src/core/color_palette.py` - Add your palette to the dictionary in `get_preset_palettes()`:

```python
def get_preset_palettes(self) -> Dict[str, List[Tuple[int, int, int, int]]]:
    """Get all preset palettes"""
    return {
        "SNES Classic": [...],
        "Curse of Aros": [...],
        # ... other palettes ...
        
        "Your Palette Name": [  # <-- ADD HERE
            (0, 0, 0, 255),        # Color 1 with comment
            (255, 255, 255, 255),  # Color 2 with comment
            (128, 64, 0, 255),     # Color 3 with comment
            # ... 16 colors total
        ],
    }
```

**Important:**
- The key ("Your Palette Name") is what appears in the UI dropdown
- Format: `(R, G, B, A)` tuples
- Add comments to describe each color
- Include **exactly 16 colors**

### C. Add to load_preset()

Edit `src/core/color_palette.py` - Add the palette type mapping in `load_preset()`:

```python
def load_preset(self, palette_name: str):
    """Load a preset palette"""
    presets = self.get_preset_palettes()
    if palette_name in presets:
        self.colors = presets[palette_name].copy()
        self.palette_name = palette_name
        
        # Set appropriate palette type
        if palette_name == "SNES Classic":
            self.palette_type = PaletteType.SNES_CLASSIC
        elif palette_name == "Curse of Aros":
            self.palette_type = PaletteType.CURSE_OF_AROS
        # ... other palettes ...
        elif palette_name == "Your Palette Name":  # <-- ADD HERE
            self.palette_type = PaletteType.YOUR_PALETTE
```

### D. Copy to Build Directory (For Distribution)

If building with PyInstaller, copy the JSON file to:
- `BUILDER/dist/assets/palettes/your_palette.json`
- `BUILDER/release/PixelPerfect/assets/palettes/your_palette.json`

This happens automatically when running `build.bat`.

## Example: Old School RuneScape Palette (Hardcoded)

Here's the complete implementation for the OSRS palette:

### 1. JSON File (Optional)
`assets/palettes/old_school_runescape.json`:
```json
{
  "name": "Old School RuneScape",
  "type": "old_school_runescape",
  "description": "Classic OSRS medieval fantasy palette...",
  "colors": [
    [0, 0, 0, 255],
    [255, 255, 255, 255],
    ...
  ]
}
```

### 2. Enum Addition
```python
class PaletteType(Enum):
    ...
    OLD_SCHOOL_RUNESCAPE = "old_school_runescape"
    CUSTOM = "custom"
```

### 3. get_preset_palettes() Addition
```python
"Old School RuneScape": [
    (0, 0, 0, 255),        # Black
    (255, 255, 255, 255),  # White
    (139, 69, 19, 255),    # Saddle Brown
    (36, 97, 49, 255),     # Dark Green
    ...
]
```

### 4. load_preset() Addition
```python
elif palette_name == "Old School RuneScape":
    self.palette_type = PaletteType.OLD_SCHOOL_RUNESCAPE
```

## Testing Your Hardcoded Palette

1. Run the application: `python main.py`
2. Open the **Palette** dropdown in the left panel
3. Select your new palette from the list
4. Verify all 16 colors display correctly

## Current Behavior

- Dynamic palette loading from JSON files is implemented and auto-discovers palettes at startup
- Built-in presets remain available

## Current Palettes

1. **SNES Classic** - 16-color retro gaming palette
2. **Curse of Aros** - Earthy medieval tones
3. **Heartwood Online** - Forest and nature theme
4. **Definya** - Bright, vibrant colors
5. **Kakele Online** - Warm, golden fantasy palette
6. **Rucoy Online** - Grayscale with earth tones
7. **Old School RuneScape** - Medieval fantasy with OSRS aesthetic
8. **Skin Tones** - Natural human complexion (light to dark, Fitzpatrick-inspired)

## Troubleshooting

**JSON palette not appearing in dropdown?**
- Confirm the file is in `assets/palettes/` and ends with `.json`
- Validate the JSON structure (name, colors array of 16 RGBA values)
- Ensure the app was restarted

**Hardcoded palette not appearing?**
- Check that you added it to `get_preset_palettes()` and `load_preset()`
- Verify the palette name matches exactly (case-sensitive)

**Colors look wrong?**
- Verify RGB values are 0-255
- Ensure alpha is 255
- Check that you have exactly 16 colors

**Build issues?**
- Ensure JSON files are in `assets/palettes/`
- Run `build.bat` to copy files to dist folder
- Check that `PaletteType` enum includes your palette

## Related Files

- `src/core/color_palette.py` - Main palette system
- `assets/palettes/*.json` - Palette data files
- `docs/COLOR_WHEEL_BUTTONS.md` - Color system architecture
- `docs/CUSTOM_COLORS_FEATURE_SUMMARY.md` - Custom colors feature

