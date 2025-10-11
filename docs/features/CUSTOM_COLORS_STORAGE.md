# Custom Colors Storage - Technical Documentation

## Overview
The Custom Colors system provides **user-specific**, **persistent storage** for colors created in the color wheel. Each user has their own set of custom colors that persist across sessions.

## Storage Location

### Windows
```
C:\Users\[USERNAME]\AppData\Local\PixelPerfect\custom_colors.json
```

### Mac/Linux
```
~/.pixelperfect/custom_colors.json
```

## Key Features

### ✅ User-Specific
- Each user on the system has their own custom colors
- Colors stored in user's profile directory, not app directory
- Survives app updates and reinstalls

### ✅ Not Bundled with Executable
- Empty for fresh installations
- Developer's custom colors are NOT included in distributed EXE
- Users build their own color library

### ✅ Persistent
- Colors saved automatically when added
- Loaded on app startup
- Persists across sessions

### ✅ Limit Protected
- Maximum 32 custom colors per user
- Prevents duplicate colors
- Clear all option for reset

## File Format

```json
{
  "colors": [
    [255, 128, 64, 255],
    [64, 128, 255, 255],
    ...
  ],
  "version": "1.0",
  "max_colors": 32
}
```

## API Usage

### Initialization
```python
from src.core.custom_colors import CustomColorManager

custom_colors = CustomColorManager()
```

### Add Color
```python
# Returns True if added, False if duplicate or full
success = custom_colors.add_color((255, 128, 64, 255))
```

### Remove Color
```python
# By index
custom_colors.remove_color(0)

# By value
custom_colors.remove_color_by_value((255, 128, 64, 255))
```

### Get Colors
```python
colors = custom_colors.get_colors()
count = custom_colors.get_color_count()
is_full = custom_colors.is_full()
```

### Storage Info
```python
info = custom_colors.get_storage_info()
# Returns: {
#   'storage_path': 'C:\\Users\\...\\PixelPerfect',
#   'colors_file': 'C:\\Users\\...\\custom_colors.json',
#   'file_exists': True,
#   'color_count': 12,
#   'max_colors': 32,
#   'is_full': False
# }
```

## Integration with Color Wheel

### "Save Custom Color" Button (Green)
1. Saves current color to **custom_colors.json** (permanent)
2. Available in all future sessions
3. Shows `[OK]` on success or `[WARN]` on duplicate/full

### "Delete Color" Button (Red)
1. Removes selected custom color from **custom_colors.json**
2. Must select a color in grid first (white border)
3. Shows `[DELETE]` on success or `[WARN]` if no selection

## Distribution Notes

### For Developers
- Custom colors file is NOT tracked in git
- Add `custom_colors.json` to `.gitignore`
- Test with fresh user profiles

### For Users
- Custom colors created automatically on first use
- Safe to delete file to reset colors
- Backup file to preserve colors across machines

## Security & Privacy

- Stored locally on user's machine only
- No network transmission
- No data collection
- User has full control (can delete file anytime)

## Testing

### Test Fresh Installation
```python
import os
from pathlib import Path

# Simulate fresh install
storage_path = Path(os.environ['LOCALAPPDATA']) / 'PixelPerfect'
colors_file = storage_path / 'custom_colors.json'

# Delete test file
if colors_file.exists():
    colors_file.unlink()

# Run app - should create empty storage
```

### Test User Isolation
1. Create custom colors as User A
2. Switch to User B account
3. Verify User B has empty custom colors
4. Switch back to User A
5. Verify User A's colors are still there

## Troubleshooting

### Colors Not Saving
1. Check file permissions on storage directory
2. Verify `LOCALAPPDATA` environment variable (Windows)
3. Check console for error messages

### Colors Not Loading
1. Check JSON file format is valid
2. Verify file path is accessible
3. Check file is not corrupted

### Reset Custom Colors
Delete the file:
- Windows: `%LOCALAPPDATA%\PixelPerfect\custom_colors.json`
- Mac/Linux: `~/.pixelperfect/custom_colors.json`

---

**Implementation Date:** October 11, 2025
**Version:** 1.11
**Module:** `src/core/custom_colors.py`

