# Custom Colors - Troubleshooting Guide

## Common Issues and Solutions

### Issue: "Custom Colors Not Connected" Message

**Symptom:**
```
[WARN] Custom colors not connected
```

**Cause:** The ColorWheel callbacks were not properly initialized

**Solution:**
This was fixed in v1.12. Ensure you have the latest version where `ColorWheel.__init__()` includes:
```python
self.on_save_custom_color: Optional[Callable] = None
self.on_remove_custom_color: Optional[Callable] = None
```

**Status:** ✅ Fixed in v1.12

---

### Issue: UnicodeEncodeError in Console

**Symptom:**
```
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 0
```

**Cause:** Emoji characters (✅, ⚠️, 🗑️) are not compatible with Windows console encoding

**Solution:**
Replaced emoji with ASCII-safe prefixes:
- ✅ → `[OK]`
- ⚠️ → `[WARN]`
- 🗑️ → `[DELETE]`
- ✅ (selection) → `[SELECT]`

**Status:** ✅ Fixed in v1.12

---

### Issue: "Color Already in Custom Colors" Warning

**Symptom:**
```
[WARN] Color already in custom colors: (255, 0, 0, 255)
```

**Cause:** You're trying to save a color that's already in your custom colors library

**Is This a Bug?** ❌ No, this is working correctly!

**Explanation:**
- The system prevents duplicate colors in your custom colors library
- It **only** checks your custom colors (in `custom_colors.json`)
- It does **NOT** check preset palettes (SNES Classic, Curse of Aros, etc.)
- Palette colors and custom colors are completely separate systems

**Solution:**
This is expected behavior. If you want to save this color:
1. It's already in your custom colors grid - just click it to use it
2. Or delete it first, then save it again
3. Or adjust the color wheel slightly to create a different shade

---

### Issue: Colors Not Showing in Grid

**Symptom:** 
- Console shows `[OK] Saved custom color: (r, g, b, a)`
- But color doesn't appear in Custom Colors grid

**Possible Causes:**
1. Grid didn't update (UI refresh issue)
2. File permission issues
3. Storage path incorrect

**Solutions:**

**1. Force Grid Refresh:**
- Switch to Grid or Primary view mode
- Switch back to Wheel mode
- Grid should update

**2. Check Storage Path:**
```
Windows: C:\Users\[YOUR_USERNAME]\AppData\Local\PixelPerfect\custom_colors.json
Mac/Linux: ~/.pixelperfect/custom_colors.json
```

**3. Verify File Contents:**
Open `custom_colors.json` and check if your color is there:
```json
{
  "colors": [
    [255, 0, 0, 255],
    [0, 255, 0, 255]
  ],
  "version": "1.0",
  "max_colors": 32
}
```

**4. Check Console:**
Look for:
```
Loaded X custom colors from C:\Users\...\custom_colors.json
```

**Status:** If you see `[OK]` message and color is in JSON file, the system is working - try restarting the app.

---

### Issue: Can't Delete Custom Color

**Symptom:**
```
[WARN] No custom color selected. Click a custom color first.
```

**Cause:** You clicked "Delete Color" button without selecting a color from the grid

**Solution:**
1. **Click** a custom color in the Custom Colors grid (it gets a white border)
2. **Then** click the "Delete Color" (red) button
3. You should see: `[DELETE] Removed custom color: (r, g, b, a)`

---

### Issue: Custom Colors Disappeared

**Symptom:** Previously saved colors are gone after reopening app

**Possible Causes:**
1. File was deleted
2. Switched to different user account
3. Storage path changed
4. File got corrupted

**Solutions:**

**1. Check if File Exists:**
Navigate to storage location and verify `custom_colors.json` exists

**2. Check User Account:**
Custom colors are user-specific. If you logged in as a different Windows user, you'll have a different set of custom colors.

**3. Check Console on Startup:**
```
Loaded X custom colors from [PATH]
```
- If X = 0, file is empty or newly created
- If path is wrong, file is in wrong location

**4. Restore from Backup:**
If you backed up `custom_colors.json`, copy it back to the storage location

---

### Issue: "Custom Colors Full (max 32)"

**Symptom:**
```
[WARN] Custom colors full (max 32)
```

**Cause:** You've reached the maximum of 32 custom colors

**Solution:**
1. Delete some colors you don't use:
   - Click the color in grid (white border)
   - Click "Delete Color" (red button)
2. Or clear all and start fresh:
   - Delete `custom_colors.json`
   - Restart app (creates new empty file)

---

### Issue: Palette Colors vs Custom Colors Confusion

**Question:** "Why can't I save preset palette colors to custom colors?"

**Answer:** You can! But there's a difference:

**Preset Palette Colors (Grid/Primary View):**
- Part of SNES Classic, Curse of Aros, etc.
- 16 colors per palette
- Change when you switch palettes
- Good for working within a specific style

**Custom Colors (Wheel View):**
- Your personal color library
- Up to 32 colors
- Persist forever across all palettes
- Good for brand colors, favorite shades

**How to Convert:**
1. Switch to Grid view
2. Note the palette color you want
3. Switch to Wheel view
4. Adjust wheel to match that color
5. Click "Save Custom Color"

Now that color is in both places!

---

## Debugging Tips

### Check Console Output

**On App Startup:**
```
Loaded X custom colors from [PATH]
```
- Confirms storage path
- Shows how many colors loaded

**On Save:**
```
Saved X custom colors
Added custom color (r, g, b, a)
[OK] Saved custom color: (r, g, b, a)
```
- Confirms save operation
- Shows the saved color

**On Delete:**
```
Saved X custom colors
[DELETE] Removed custom color: (r, g, b, a)
```
- Confirms delete operation

### Manual File Inspection

**View Storage Info:**
```python
from src.core.custom_colors import CustomColorManager
cm = CustomColorManager()
print(cm.get_storage_info())
```

**Output:**
```python
{
    'storage_path': 'C:\\Users\\...\\PixelPerfect',
    'colors_file': 'C:\\Users\\...\\custom_colors.json',
    'file_exists': True,
    'color_count': 5,
    'max_colors': 32,
    'is_full': False
}
```

---

## Getting Help

If you're still having issues:

1. **Check Console Messages:** Look for `[OK]`, `[WARN]`, `[DELETE]`, `[SELECT]` messages
2. **Verify File Location:** Ensure `custom_colors.json` exists at correct path
3. **Check File Permissions:** Ensure you can read/write to AppData folder
4. **Try Fresh Start:** Delete `custom_colors.json` and restart app
5. **Check Version:** Ensure you're running v1.12 or later

---

**Last Updated:** October 11, 2025  
**Version:** 1.12  
**Status:** All Known Issues Resolved

