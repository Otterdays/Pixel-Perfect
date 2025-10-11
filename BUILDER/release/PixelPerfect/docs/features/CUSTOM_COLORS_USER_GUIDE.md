# Custom Colors - User Guide

## What Are Custom Colors?

Custom Colors let you save your favorite colors from the Color Wheel permanently. Unlike palette colors that change when you switch palettes, **Custom Colors stay with you across all sessions**.

## How It Works

### 🎨 Creating Custom Colors
1. Open the **Color Wheel** view mode
2. Adjust the wheel to create your perfect color
3. Click **"Save Custom Color"** (green button - saves permanently to your library)
4. Your color appears instantly in the Custom Colors grid below

### 🗑️ Deleting Custom Colors
1. Click on a custom color in the grid (it gets a white border)
2. Click **"Delete Color"** (red button)
3. The selected color is removed from your library

### 💾 Where Are They Stored?

**Windows:**
```
C:\Users\[YourUsername]\AppData\Local\PixelPerfect\custom_colors.json
```

**Mac/Linux:**
```
~/.pixelperfect/custom_colors.json
```

### ✅ Key Benefits

#### User-Specific
- Each user on the computer has their own custom colors
- Your colors won't affect other users
- Your saved colors are private to your account

#### Persistent
- Saved custom colors survive:
  - App restarts
  - App updates
  - Palette changes
  - Project changes

#### Not in the App
- Custom colors are stored in **your user folder**, not the app folder
- When someone downloads Pixel Perfect, they start with empty custom colors
- Each user builds their own color library

### 📊 Limits
- **Maximum:** 32 custom colors per user
- **Duplicates:** Can't add the same color twice
- **Reset:** Delete the JSON file to start fresh

## Usage Examples

### Building a Brand Color Library
```
1. Switch to Color Wheel
2. Create your brand's primary color
3. Save as Custom Color
4. Repeat for all brand colors
5. These colors are now available in ALL projects
```

### Creating a Character Palette
```
1. Design character colors in Color Wheel
2. Save skin tone, hair color, eyes, clothing
3. Use Custom Colors grid to quickly access them
4. No need to recreate colors for each new character
```

### Sharing Colors Between Projects
```
1. Find perfect color in Project A
2. Save as Custom Color
3. Switch to Project B
4. Custom Color is there waiting!
```

## Color Wheel Buttons

### Save Custom Color (Green Button)
- **Purpose**: Permanently save current color wheel color
- **Action**: Adds color to Custom Colors grid
- **Storage**: Saves to `custom_colors.json` immediately
- **Feedback**: `[OK]` Success or `[WARN]` Duplicate/Full warning

### Delete Color (Red Button)
- **Purpose**: Remove selected custom color
- **Action**: Deletes color from Custom Colors grid and storage
- **Requirement**: Must click a custom color in grid first
- **Feedback**: `[DELETE]` Deleted or `[WARN]` No color selected

## Comparison

### Palette Colors (Grid/Primary View)
- ✅ Part of current palette (16 colors max)
- ✅ Change when switching palettes
- ✅ Saved in project files
- ❌ Don't persist across palettes

### Custom Colors (Color Wheel View)
- ✅ Persist forever (until manually deleted)
- ✅ Available in all palettes
- ✅ Available in all projects
- ✅ Unique to your user account
- ✅ Up to 32 colors

## Tips & Tricks

### Backup Your Colors
Copy the `custom_colors.json` file to:
- Cloud storage (Dropbox, OneDrive, etc.)
- External drive
- Another computer

### Transfer to Another Machine
1. Export `custom_colors.json` from old machine
2. Copy to same location on new machine
3. Create the PixelPerfect folder if it doesn't exist

### Reset Everything
Delete `custom_colors.json` to start with a clean slate

### Check Your Custom Colors Location
Look in the console when Pixel Perfect starts:
```
Created new custom colors storage at C:\Users\...\custom_colors.json
```

## Privacy & Security

- 🔒 Stored **locally only** on your machine
- 🔒 **No network transmission** - never uploaded anywhere
- 🔒 **No data collection** - just a simple JSON file
- 🔒 **You control it** - delete anytime, no consequences

## Troubleshooting

### Colors Not Saving?
- Check if you have write permissions to AppData folder
- Try running Pixel Perfect as administrator (Windows)
- Check console for error messages

### Colors Disappeared?
- Check if `custom_colors.json` still exists
- File may have been deleted by cleanup software
- Check if you switched user accounts

### Start Fresh
Delete the file and restart Pixel Perfect - it will create a new empty file

---

**Remember:** Custom Colors are YOUR personal color library. They're separate from the app and will follow you across updates and reinstalls (as long as you're using the same user account)!

