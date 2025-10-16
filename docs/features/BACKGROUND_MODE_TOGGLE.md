# Background Mode Toggle

**Version**: 1.43  
**Date**: January 2025  
**Status**: ✅ Complete

## Feature Description

A background mode toggle button that allows users to control the canvas background color independently of the current theme. This provides better visibility control and theme independence for the drawing canvas.

## Implementation Overview

The background mode toggle follows the same pattern as the grid mode toggle, providing three modes:
- **Auto Mode**: Uses the theme's default background color
- **Dark Mode**: Forces a dark background regardless of theme
- **Light Mode**: Forces a light background regardless of theme

## Technical Implementation

### 1. Canvas Background Mode Property
**File**: `src/core/canvas.py`
```python
self.background_mode = "auto"  # "auto", "dark", "light"
```

### 2. BackgroundControlManager
**File**: `src/ui/background_control_manager.py`

New manager class that handles:
- Background mode cycling logic
- Button icon and tooltip updates
- Theme-aware button styling

**Key Methods**:
- `toggle_background_mode()`: Cycles through auto → dark → light → auto
- `update_background_mode_button()`: Updates icon, tooltip, and button colors

### 3. Canvas Background Logic
**File**: `src/core/canvas_renderer.py`
```python
def get_background_color(self):
    if self.app.canvas.background_mode == "auto":
        return self.app.theme_manager.get_current_theme().canvas_bg
    elif self.app.canvas.background_mode == "dark":
        return "#0d1117"  # Very dark background
    else:  # light mode
        return "#fafafa"  # Light background
```

### 4. UI Integration
**File**: `src/ui/ui_builder.py`
- Added background mode button to toolbar
- Positioned to the left of grid mode button
- Initial icon: 🌗 (auto mode)

**File**: `src/ui/main_window.py`
- Added callback integration
- Initialized BackgroundControlManager
- Set widget references and callbacks

### 5. Theme Integration
**File**: `src/ui/theme_dialog_manager.py`
- Updated `apply_theme()` to use background mode logic
- Added background mode button styling updates

## Button Layout

The toolbar button order (left to right):
1. **Background Mode** (🌗/⚫/⚪) - New feature
2. **Grid Mode** (🌓/🌙/☀️) - Existing feature  
3. **Grid** - Existing feature
4. **Grid Overlay** - Existing feature
5. **Settings** - Existing feature
6. **Notes** - Existing feature
7. **Theme Selector** - Existing feature

## Icon System

| Mode | Icon | Tooltip | Description |
|------|------|---------|-------------|
| Auto | 🌗 | "Background Mode: Auto (Light/Dark theme)" | Uses theme default |
| Dark | ⚫ | "Background Mode: Dark" | Forces dark background |
| Light | ⚪ | "Background Mode: Light" | Forces light background |

## Theme Integration

### Auto Mode Behavior
- **Light Themes** (Angelic, American): Auto shows light background
- **Dark Themes** (Basic Grey, Gemini): Auto shows dark background

### Manual Mode Behavior
- **Dark Mode**: Always shows `#0d1117` (very dark)
- **Light Mode**: Always shows `#fafafa` (light)

## Benefits

1. **Theme Independence**: Manual modes work consistently across all themes
2. **Better Visibility**: Users can force appropriate backgrounds for any theme
3. **Intuitive Interface**: Clear icons and tooltips explain current mode
4. **Consistent UX**: Follows the same pattern as grid mode toggle
5. **Non-Destructive**: Doesn't interfere with existing functionality

## Usage

1. **Toggle Background Mode**: Click the background mode button to cycle through modes
2. **Auto Mode**: Respects current theme's background color
3. **Dark Mode**: Forces dark background for better visibility on light themes
4. **Light Mode**: Forces light background for better visibility on dark themes

## Technical Details

### Background Color Values
- **Auto**: Uses `theme.canvas_bg` (varies by theme)
- **Dark**: `#0d1117` (GitHub-style very dark)
- **Light**: `#fafafa` (near-white light)

### Button Styling
- **Auto Mode**: Uses `theme.button_active` (highlighted)
- **Manual Modes**: Uses `theme.button_normal` (standard)

### Integration Points
- Theme changes update button appearance
- Canvas background updates immediately on mode change
- Button state persists across theme switches

---

**Implementation Status**: ✅ Complete and tested  
**User Impact**: Significant QoL improvement for canvas visibility control  
**Technical Debt**: None - clean, focused implementation following established patterns
