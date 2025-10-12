# How to Add New Color Palettes to Pixel Perfect

This guide explains how to add new color palettes to Pixel Perfect.

## Overview

Pixel Perfect supports custom color palettes for different art styles. Currently, palettes are **hardcoded** in the source code, not loaded from JSON files (though JSON files exist for reference/future use).

## Steps to Add a New Palette

### 1. Create the JSON File (Optional - For Reference)

Create a JSON file in `assets/palettes/` with your palette colors:

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

### 2. Add to PaletteType Enum (**REQUIRED**)

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

### 3. Add to get_preset_palettes() (**REQUIRED**)

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

### 4. Add to load_preset() (**REQUIRED**)

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

### 5. Copy to Build Directory (For Distribution)

If building with PyInstaller, copy the JSON file to:
- `BUILDER/dist/assets/palettes/your_palette.json`
- `BUILDER/release/PixelPerfect/assets/palettes/your_palette.json`

This happens automatically when running `build.bat`.

## Example: Old School RuneScape Palette

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

## Testing Your Palette

1. Run the application: `python main.py`
2. Open the **Palette** dropdown in the left panel
3. Select your new palette from the list
4. Verify all 16 colors display correctly

## Future Improvements

**Planned:** Dynamic palette loading from JSON files instead of hardcoding
- Would allow users to add palettes without editing source code
- JSON files would become the primary source of truth
- Current JSON files are already structured for this

## Current Palettes

1. **SNES Classic** - 16-color retro gaming palette
2. **Curse of Aros** - Earthy medieval tones
3. **Heartwood Online** - Forest and nature theme
4. **Definya** - Bright, vibrant colors
5. **Kakele Online** - Warm, golden fantasy palette
6. **Rucoy Online** - Grayscale with earth tones
7. **Old School RuneScape** - Medieval fantasy with OSRS aesthetic

## Troubleshooting

**Palette not appearing in dropdown?**
- Check that you added it to `get_preset_palettes()` dictionary
- Verify the palette name matches exactly (case-sensitive)
- Restart the application after making changes

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

