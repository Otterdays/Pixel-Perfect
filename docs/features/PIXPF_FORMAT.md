# .pixpf File Format Documentation

## Overview

`.pixpf` (Pixel Perfect Project Format) is a proprietary JSON-based project file format for Pixel Perfect that stores complete project state including canvas settings, layers, animation frames, palette information, and metadata.

## Format Version

**Current Version:** 1.0

## File Structure

The `.pixpf` file is a JSON file with the following structure:

```json
{
  "version": "1.0",
  "created": "2025-10-11T14:30:00.123456",
  "modified": "2025-10-11T15:45:00.654321",
  "canvas": { ... },
  "palette": { ... },
  "layers": [ ... ],
  "animation": { ... },
  "metadata": { ... }
}
```

## Top-Level Fields

### version (string)
- **Type:** String
- **Description:** Format version number
- **Current Value:** `"1.0"`
- **Purpose:** Future compatibility and migration support

### created (string, ISO 8601)
- **Type:** ISO 8601 timestamp
- **Description:** Original project creation time
- **Example:** `"2025-10-11T14:30:00.123456"`

### modified (string, ISO 8601)
- **Type:** ISO 8601 timestamp  
- **Description:** Last modification time
- **Example:** `"2025-10-11T15:45:00.654321"`
- **Updated:** Every time the project is saved

## Canvas Section

Stores canvas dimensions, zoom level, and display settings:

```json
"canvas": {
  "width": 32,
  "height": 32,
  "zoom": 16,
  "show_grid": true,
  "checkerboard": true
}
```

### Canvas Fields

| Field | Type | Description | Valid Values |
|-------|------|-------------|--------------|
| `width` | integer | Canvas width in pixels | 16, 32, 64 |
| `height` | integer | Canvas height in pixels | 16, 32, 64 |
| `zoom` | integer | Zoom level multiplier | 1-32 |
| `show_grid` | boolean | Display pixel grid | true/false |
| `checkerboard` | boolean | Show transparency pattern | true/false |

## Palette Section

Stores color palette information:

```json
"palette": {
  "name": "SNES Classic",
  "type": "snes_classic",
  "colors": [
    [0, 0, 0, 255],
    [255, 255, 255, 255],
    ...
  ],
  "primary_color": 0,
  "secondary_color": 1
}
```

### Palette Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Palette name |
| `type` | string | Palette type (snes_classic, curse_of_aros, heartwood, definya, kakele, rucoy, custom) |
| `colors` | array | Array of RGBA color arrays [R, G, B, A] |
| `primary_color` | integer | Index of primary color (0-based) |
| `secondary_color` | integer | Index of secondary color (0-based) |

### Color Format

Colors are stored as 4-element arrays: `[R, G, B, A]`
- **R** (Red): 0-255
- **G** (Green): 0-255
- **B** (Blue): 0-255
- **A** (Alpha): 0-255 (0 = transparent, 255 = opaque)

## Layers Section

Stores all layer data as an array:

```json
"layers": [
  {
    "index": 0,
    "name": "Background",
    "visible": true,
    "opacity": 1.0,
    "locked": false,
    "pixels": [
      [ [0,0,0,0], [255,0,0,255], ... ],
      [ [0,255,0,255], [0,0,255,255], ... ],
      ...
    ]
  },
  ...
]
```

### Layer Fields

| Field | Type | Description | Valid Range |
|-------|------|-------------|-------------|
| `index` | integer | Layer order (0 = bottom) | 0-9 |
| `name` | string | Layer name | any string |
| `visible` | boolean | Layer visibility | true/false |
| `opacity` | float | Layer opacity | 0.0-1.0 |
| `locked` | boolean | Edit protection | true/false |
| `pixels` | 3D array | Pixel data (height × width × 4) | RGBA values |

### Pixel Data Structure

Pixels are stored as a 3D array:
```
[
  [ [R,G,B,A], [R,G,B,A], ... ],  // Row 0
  [ [R,G,B,A], [R,G,B,A], ... ],  // Row 1
  ...
]
```

**Dimensions:** `height × width × 4`

Example for 32×32 canvas:
- Outer array: 32 rows
- Middle array: 32 pixels per row
- Inner array: 4 values (RGBA) per pixel

## Animation Section

Stores animation timeline and frames:

```json
"animation": {
  "current_frame": 0,
  "fps": 12,
  "loop": true,
  "frames": [
    {
      "index": 0,
      "name": "Frame 1",
      "duration": 100,
      "pixels": [ ... ]
    },
    ...
  ]
}
```

### Animation Fields

| Field | Type | Description | Valid Range |
|-------|------|-------------|-------------|
| `current_frame` | integer | Active frame index | 0-based |
| `fps` | integer | Frames per second | 1-60 |
| `loop` | boolean | Loop animation | true/false |
| `frames` | array | Frame data array | 1-8 frames |

### Frame Fields

| Field | Type | Description |
|-------|------|-------------|
| `index` | integer | Frame order |
| `name` | string | Frame name |
| `duration` | integer | Frame duration (ms) |
| `pixels` | 3D array | Frame pixel data (same format as layers) |

## Metadata Section

Optional custom metadata:

```json
"metadata": {
  "author": "Artist Name",
  "description": "Project description",
  "tags": ["sprite", "character"],
  "notes": "Additional notes"
}
```

All metadata fields are optional and user-defined.

## File Size

Typical file sizes:
- **16×16 sprite (1 layer, 1 frame):** ~10 KB
- **32×32 sprite (3 layers, 1 frame):** ~40 KB
- **32×32 animation (3 layers, 4 frames):** ~160 KB
- **64×64 complex project (10 layers, 8 frames):** ~2 MB

Size increases with:
- More layers
- More animation frames
- Larger canvas dimensions

## Compatibility

### Forward Compatibility
Newer versions of Pixel Perfect can read older `.pixpf` files by checking the `version` field.

### Backward Compatibility
Older versions may not support new fields added in future versions but can still read basic project data.

### Version Migration
Future versions will automatically migrate old formats:
```python
if project_data["version"] == "1.0":
    # Migrate to newer format
    pass
```

## Reading/Writing

### Save Operation
```python
project.save_project(
    filename="my_sprite.pixpf",
    canvas=canvas,
    palette=palette,
    layer_manager=layer_manager,
    timeline=timeline,
    metadata={"author": "Artist"}
)
```

### Load Operation
```python
success = project.load_project(
    filename="my_sprite.pixpf",
    canvas=canvas,
    palette=palette,
    layer_manager=layer_manager,
    timeline=timeline
)
```

## Error Handling

The system handles these error cases:
- **File not found:** Returns `False`, prints error
- **Invalid JSON:** Returns `False`, prints parse error
- **Missing fields:** Uses defaults, continues loading
- **Corrupted pixel data:** Clears layer, continues loading
- **Version mismatch:** Attempts migration or default values

## Data Validation

When loading, the system validates:
- ✅ Canvas dimensions match valid presets
- ✅ Layer pixel array dimensions match canvas size
- ✅ Color values are in 0-255 range
- ✅ Opacity values are in 0.0-1.0 range
- ✅ Frame indices are sequential
- ✅ All required fields exist

## Best Practices

### For Users
1. **Regular Saves:** Save frequently to avoid data loss
2. **Backup:** Keep backup copies of important projects
3. **Naming:** Use descriptive filenames (`character_walk_cycle.pixpf`)
4. **Version Control:** Safe to commit `.pixpf` files to Git (text-based)

### For Developers
1. **Always validate** loaded data
2. **Use try/except** blocks for file operations
3. **Provide user feedback** on load errors
4. **Log errors** for debugging
5. **Test with corrupted files** to ensure robustness

## Examples

### Minimal Valid Project
```json
{
  "version": "1.0",
  "created": "2025-10-11T12:00:00",
  "modified": "2025-10-11T12:00:00",
  "canvas": {
    "width": 16,
    "height": 16,
    "zoom": 8,
    "show_grid": true,
    "checkerboard": true
  },
  "palette": {
    "name": "Default",
    "type": "custom",
    "colors": [[0,0,0,255], [255,255,255,255]],
    "primary_color": 0,
    "secondary_color": 1
  },
  "layers": [],
  "animation": {
    "current_frame": 0,
    "fps": 12,
    "loop": true,
    "frames": []
  },
  "metadata": {}
}
```

## Future Enhancements

Planned for future versions:
- **Compression:** Optional gzip compression for large files
- **Embedded resources:** Include custom brushes, fonts
- **History:** Store undo history in project file
- **Thumbnails:** Embedded preview image
- **Custom data:** Plugin/extension data support

## Technical Notes

- **Encoding:** UTF-8
- **Line endings:** Platform-independent (JSON)
- **Indentation:** 2 spaces (human-readable)
- **Array storage:** JSON arrays (not binary)
- **Numpy conversion:** `np.array(pixels, dtype=np.uint8)`

## Troubleshooting

### Project Won't Load
1. Check file is valid JSON
2. Verify `version` field exists
3. Check canvas dimensions are valid
4. Look for truncated/corrupted data

### Missing Layers After Load
- Check `layers` array exists
- Verify pixel data dimensions match canvas
- Look for console error messages

### Colors Wrong After Load
- Verify RGBA values are 0-255
- Check palette type is valid
- Ensure color indices are in bounds

## Related Documentation

- **[Custom Colors](CUSTOM_COLORS_STORAGE.md)** - User color storage (separate from projects)
- **[ARCHITECTURE](../ARCHITECTURE.md)** - Technical system design
- **[Export Formats](../README.md#export-formats)** - PNG, GIF, sprite sheet exports

---

**Format Specification Version:** 1.0  
**Last Updated:** October 11, 2025  
**Status:** ✅ Stable

