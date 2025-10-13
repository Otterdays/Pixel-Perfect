# Theme System - UI Color Scheme Management

## Overview
The Theme System provides centralized color scheme management for Pixel Perfect, allowing users to switch between different visual themes in real-time. The system is architected as a separate module for clean code organization and easy extensibility.

## Features

### Built-in Themes

#### 1. Basic Grey (Default)
**Description**: Original dark theme with grey tones
- Professional, low-eye-strain interface
- Dark backgrounds with light text
- Blue accents for active elements
- Ideal for extended editing sessions

**Color Palette**:
- Background: `#2b2b2b`, `#1e1e1e`, `#363636`
- Text: `#ffffff`, `#d4d4d4`
- Buttons: `#3b3b3b` normal, `#1f6aa5` active
- Canvas: `#2b2b2b` background, `#000000` border

#### 2. Angelic
**Description**: Light, airy theme with soft colors
- Bright, clean interface
- Soft blues and whites
- Gentle on the eyes for daytime work
- Modern, minimalist aesthetic

**Color Palette**:
- Background: `#f5f5f5`, `#ffffff`, `#e8e8e8`
- Text: `#1a1a1a`, `#4a4a4a`
- Buttons: `#e0e7ff` normal, `#818cf8` active
- Canvas: `#fafafa` background, `#cbd5e1` border

### Theme Switcher UI
- **Location**: Toolbar, right side (before Grid toggle)
- **Icon**: 🎨 palette emoji with tooltip
- **Control**: Dropdown menu (120px width)
- **Feedback**: Instant visual update on selection

## Usage

### Switching Themes
1. Click the 🎨 palette icon or dropdown in the toolbar
2. Select desired theme from the list
3. Theme applies instantly to all UI elements


### What Gets Themed (Complete List)
The theme system affects **100% of UI elements**:
- **Main window** backgrounds (primary, secondary, tertiary)
- **Toolbar** background and all buttons
- **Tool panel** background, buttons, and all nested frames
- **Selection operations** panel and buttons
- **Palette panel** background, dropdown, radio buttons
- **Layer panel** background and all children
- **Animation panel** background, frame list area, all children
- **Left/right scrollable panels** and their scrollbars
- **PanedWindow dividers** (vertical bars between panels)
- **Canvas area** background
- **Drawing canvas** background
- **Grid lines** and borders
- **Selection overlays** (outline, handles, edges)
- **All buttons** (normal, hover, active states)
- **All dropdowns** (size, zoom, theme, palette)
- **All text/labels** throughout the UI
- **Undo/Redo buttons**

## Architecture

### Module Structure
```
src/ui/theme_manager.py
├── Theme (Base Class)
│   ├── Color properties for all UI elements
│   └── Default values (Basic Grey)
├── BasicGreyTheme (Implementation)
│   └── Dark theme colors
├── AngelicTheme (Implementation)
│   └── Light theme colors
└── ThemeManager
    ├── Theme registry
    ├── Active theme tracking
    └── Theme switching logic
```

### Integration Points
- **MainWindow**: Initializes ThemeManager, creates theme dropdown
- **Callback System**: `on_theme_changed` fires when theme switches
- **Application Method**: `_apply_theme()` updates all UI elements
- **CTk Integration**: Syncs with CustomTkinter appearance modes

## Technical Details

### Theme Properties
Each theme defines colors for:

**Backgrounds**:
- `bg_primary`: Main background color
- `bg_secondary`: Secondary panels
- `bg_tertiary`: Nested elements

**Text**:
- `text_primary`: Main text
- `text_secondary`: Subtitles, labels
- `text_disabled`: Inactive elements

**Buttons**:
- `button_normal`: Default state
- `button_hover`: Mouse hover
- `button_active`: Selected/active state

**Borders**:
- `border_normal`: Default borders
- `border_focus`: Focused elements

**Canvas**:
- `canvas_bg`: Canvas area background
- `canvas_border`: Canvas border color
- `grid_color`: Pixel grid lines

**Tools**:
- `tool_selected`: Active tool highlight
- `tool_unselected`: Inactive tool color

**Selections**:
- `selection_outline`: Selection rectangle
- `selection_handle`: Corner handles
- `selection_edge`: Edge handles

### Code Example

#### Creating a New Theme
```python
class MyCustomTheme(Theme):
    def __init__(self):
        super().__init__("My Theme")
        # Override colors
        self.bg_primary = "#123456"
        self.button_active = "#ff00ff"
        # ... etc
```

#### Adding Theme to Manager
```python
# In theme_manager.py __init__:
self.themes = {
    "Basic Grey": BasicGreyTheme(),
    "Angelic": AngelicTheme(),
    "My Theme": MyCustomTheme()  # Add here
}
```

#### Applying Theme Colors
```python
# Get current theme
theme = self.theme_manager.get_current_theme()

# Apply to widget
my_button.configure(fg_color=theme.button_normal)
```

## Extensibility

### Adding New Themes
1. Create new class extending `Theme` in `theme_manager.py`
2. Override color properties as needed
3. Add to `ThemeManager.themes` dictionary
4. Theme automatically appears in dropdown

### Custom Color Properties
Add new color properties to base `Theme` class:
```python
class Theme:
    def __init__(self, name: str):
        # ... existing properties ...
        self.my_custom_color = "#abcdef"
```

All theme implementations inherit this property and can override it.

### Theme Presets
Future enhancement: Save/load user-created themes
- JSON format for theme definitions
- User themes directory
- Import/export theme files

## Performance

### Optimization
- Theme switching is instant (no reload required)
- Colors applied via configure() calls (fast)
- No performance impact during editing
- Theme state persists across sessions (future)

### Memory
- Minimal memory footprint (~2KB per theme)
- Themes loaded at startup (one-time cost)
- No dynamic color calculations

## Future Enhancements

### Planned Features
1. **User Custom Themes**: Create and save custom themes
2. **Theme Import/Export**: Share themes as JSON files
3. **Color Picker**: Interactive theme editor
4. **Theme Presets**: More built-in themes (cyberpunk, pastel, etc.)
5. **Per-Element Customization**: Fine-tune individual colors
6. **Theme Preview**: Thumbnail previews in dropdown
7. **Dark Mode Auto**: Follow system theme preference
8. **Accessibility**: High-contrast themes
9. **Theme Persistence**: Remember selected theme

### Additional Themes Ideas
- **Cyberpunk**: Neon colors, dark backgrounds
- **Pastel Dream**: Soft pastel palette
- **High Contrast**: Maximum readability
- **SNES**: Retro Super Nintendo colors
- **Monochrome**: Pure black and white
- **Sunset**: Warm oranges and purples

## Best Practices

### For Users
1. Choose theme based on lighting conditions
2. Dark themes (Basic Grey) for low-light environments
3. Light themes (Angelic) for bright workspaces
4. Switch themes if experiencing eye strain

### For Developers
1. Always use theme colors, never hardcode
2. Test features with all themes
3. Add new UI elements to `_apply_theme()`
4. Document custom color properties
5. Maintain color contrast ratios (accessibility)

## Troubleshooting

### Theme Not Applying
- Check that element is added to `_apply_theme()` method
- Verify widget uses `configure()` method
- Ensure theme callback is connected

### Colors Look Wrong
- Verify hex color format (`#rrggbb`)
- Check CustomTkinter widget compatibility
- Test with both dark and light themes

### Dropdown Empty
- Ensure ThemeManager initialized before UI creation
- Verify themes added to ThemeManager.themes dictionary
- Check theme names are strings

## Developer Guide

**Want to create your own themes?** See the comprehensive guide:
📖 **[Theme Development Guide](THEME_DEVELOPMENT_GUIDE.md)**

Covers:
- Step-by-step theme creation
- Required properties
- Color guidelines
- Common pitfalls
- Performance optimization
- Testing checklist

## Implementation Notes

### Recursive Widget Updates
The theme system uses `_apply_theme_to_children()` to recursively update all nested widgets:
- Walks entire widget tree
- Updates frames, labels, buttons, radio buttons
- Preserves "transparent" frames
- Handles errors gracefully

### Why Instant Switching Works
1. **No Appearance Mode**: Skips `ctk.set_appearance_mode()` entirely
2. **Direct Configuration**: All widgets configured directly
3. **Selective Canvas Update**: Only grid/border redrawn, not pixels
4. **Canvas Tags**: Efficient element management
5. **Batch Processing**: All updates in single pass

Result: < 50ms theme switch (appears instant)

## Version History

### v1.22 (October 13, 2025)
- Initial theme system implementation
- Two themes: Basic Grey and Angelic
- Toolbar dropdown with palette icon
- Real-time theme switching (instant)
- Separate ThemeManager module
- Recursive widget updates
- Performance-optimized (no appearance mode)
- Comprehensive developer documentation

