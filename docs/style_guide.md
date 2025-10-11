# Pixel Perfect - Style Guide

## Overview
This document defines the visual design system and styling patterns used throughout Pixel Perfect. Following this guide ensures consistency, maintainability, and a professional user experience.

## Design Philosophy
- **Retro-Inspired**: SNES-era pixel art aesthetic with modern usability
- **Dark Theme**: Professional dark interface with blue accents
- **Consistency**: Unified styling patterns across all components
- **Accessibility**: Clear visual hierarchy and interactive feedback

---

## Theme Configuration

### Base Theme Settings
```python
# Applied in main_window.py initialization
ctk.set_appearance_mode("dark")          # Dark theme
ctk.set_default_color_theme("blue")      # Blue accent colors
```

### Window Configuration
- **Default Size**: 1200x800 pixels
- **Title**: "Pixel Perfect - Retro Pixel Art Editor"
- **Resizable**: Yes, with automatic grid centering

---

## Layout System

### Main Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│ Toolbar (horizontal, full width)                        │
├─────────────┬─────────────────────────┬─────────────────┤
│ Left Panel  │ Canvas Area             │ Right Panel     │
│ (250px)     │ (expandable)            │ (250px)         │
│ Tools &     │ Drawing Surface         │ Layers &        │
│ Palette     │                         │ Timeline        │
└─────────────┴─────────────────────────┴─────────────────┘
```

### Panel Specifications
- **Left Panel**: 250px width, scrollable
- **Right Panel**: 250px width, scrollable  
- **Canvas Area**: Expandable, fills remaining space
- **Padding**: 10px between panels and main container

### Scrollable Panels
- Use `CTkScrollableFrame` for panels with content overflow
- Consistent 10px padding on all sides
- Smooth scrolling with modern scrollbars

---

## Typography

### Font Hierarchy
```python
# Primary Headers (Panel Titles)
font=ctk.CTkFont(size=16, weight="bold")

# Secondary Headers (Primary Colors, Color Wheel)
font=ctk.CTkFont(size=14, weight="bold")

# Secondary Labels (Toolbar labels, Color Wheel labels)
font=ctk.CTkFont(size=12, weight="bold")

# Button Text (Default)
font=ctk.CTkFont(size=10)  # Default

# Primary Color Button Text
font=ctk.CTkFont(size=10, weight="bold")

# Special Buttons (Undo/Redo arrows)
font=ctk.CTkFont(size=16, weight="bold")
```

### Text Colors
- **Primary Text**: White (default in dark theme)
- **Secondary Text**: Light gray
- **Button Text**: White or black (based on background contrast)
- **Primary Color Buttons**: Dynamic text color based on background brightness

---

## Button System

### Button Categories

#### 1. Standard Action Buttons
```python
ctk.CTkButton(
    parent,
    text="Button Text",
    width=80,            # Standard width (80px for layer controls, 100px for tools)
    height=30,           # Standard height
    command=callback
)
```

#### 2. Tool Buttons
```python
ctk.CTkButton(
    parent,
    text="Tool Name",
    width=100,
    height=30,
    command=lambda: self._select_tool("tool_id")
)
```

#### 3. Icon Buttons
```python
ctk.CTkButton(
    parent,
    text="↶",           # Unicode arrow
    width=40,
    height=30,
    font=ctk.CTkFont(size=16, weight="bold"),
    command=callback
)
```

#### 4. Small Control Buttons
```python
ctk.CTkButton(
    parent,
    text="+",            # Single character
    width=30,
    height=30,
    command=callback
)
```

#### 5. Color Buttons
```python
ctk.CTkButton(
    parent,
    text="",
    width=30,
    height=30,
    fg_color=f"#{r:02x}{g:02x}{b:02x}",
    hover_color=f"#{min(255, r+30):02x}{min(255, g+30):02x}{min(255, b+30):02x}",
    border_width=0,
    command=callback
)
```

#### 6. Primary Color Buttons
```python
ctk.CTkButton(
    parent,
    text="Color Name",
    width=60,
    height=35,
    fg_color=f"#{r:02x}{g:02x}{b:02x}",
    text_color="white" if r+g+b < 400 else "black",
    font=ctk.CTkFont(size=10, weight="bold"),
    command=callback
)
```

#### 7. Back Button
```python
ctk.CTkButton(
    parent,
    text="✕ Back to Primary",
    width=120,
    height=30,
    fg_color="gray",
    command=callback
)
```

### Additional UI Components

#### Radio Buttons
```python
ctk.CTkRadioButton(
    parent,
    text="Option Text",
    variable=var,
    value="value",
    command=callback
)
```

#### Option Menus
```python
ctk.CTkOptionMenu(
    parent,
    variable=var,
    values=["option1", "option2", "option3"],
    command=callback
)
```

#### Entry Fields
```python
ctk.CTkEntry(
    parent,
    textvariable=var,
    width=40
)
```

#### Checkboxes
```python
ctk.CTkCheckBox(
    parent,
    text="",
    width=20,
    variable=var,
    command=callback
)
```

#### Scrollable Frames
```python
ctk.CTkScrollableFrame(
    parent,
    width=250,
    height=100  # Optional height constraint
)
```

### Button States

#### Normal State
- **Default Colors**: Theme defaults (blue/gray)
- **Border**: None (border_width=0)

#### Selected State
- **Primary Selection**: `fg_color="blue"`
- **Secondary Selection**: `fg_color="gray"`
- **Color Selection**: White border, 3px width

#### Hover State
- **Standard Buttons**: Theme hover colors
- **Color Buttons**: Brightened version (+30 RGB values)
- **Hover Effects**: White border (2px) + size increase (30px → 32px)

#### Disabled State
- **Undo/Redo**: `fg_color=("gray75", "gray25")` when unavailable
- **Available**: `fg_color=("blue", "blue")` when actions possible

---

## Color System

### Primary Colors
- **Background**: Dark theme default
- **Accent**: Blue (#1f538d)
- **Text**: White
- **Borders**: White (selection), Gray (secondary)

### Interactive Colors
- **Hover**: Brightened versions of base colors (+30 RGB)
- **Selection**: White borders
- **Active**: Blue backgrounds

### Color Button Specifications
- **Size**: 30x30 pixels (32x32 on hover)
- **Grid**: 4 columns, 2px spacing
- **Selection Border**: 3px white
- **Hover Border**: 2px white
- **Hover Size**: 32x32 pixels

---

## Spacing & Padding

### Standard Spacing
- **Panel Padding**: 10px all sides
- **Button Spacing**: 5px horizontal, 2px vertical
- **Grid Spacing**: 2px between color buttons
- **Section Spacing**: 10px between major sections
- **Toolbar Spacing**: 20px between sections, 5px between elements
- **Undo/Redo Spacing**: 2px between arrow buttons

### Padding Patterns
```python
# Panel containers
.pack(padx=10, pady=10)

# Button spacing
.pack(side="left", padx=5)

# Grid spacing
.grid(row=row, column=col, padx=2, pady=2)

# Section spacing
.pack(pady=(10, 5))
```

---

## Interactive Elements

### Hover Effects
- **Color Buttons**: Size increase + white border
- **Standard Buttons**: Theme hover colors
- **Smart Borders**: Don't interfere with selection states

### Selection Feedback
- **Primary Selection**: Blue background
- **Color Selection**: White border (3px)
- **Secondary Selection**: Gray background or border (2px)

### Visual Hierarchy
- **Active Elements**: Blue backgrounds
- **Inactive Elements**: Gray backgrounds
- **Important Actions**: Bold text or larger buttons

---

## Component-Specific Styles

### Toolbar
- **Height**: Auto (based on content)
- **Layout**: Horizontal, full width
- **Elements**: File menu, size selector, zoom controls, undo/redo, grid toggle
- **Spacing**: 20px between sections, 5px between elements
- **Button Widths**: File (60px), Grid (60px), Undo/Redo (40px each)
- **Option Menus**: Size selector, Zoom selector (default width)

### Color Palette
- **Grid Layout**: 4 columns
- **Button Size**: 30x30 pixels
- **Selection**: White border (3px primary, 2px secondary)
- **Hover**: Size increase + white border

### Layer Panel
- **Layer Buttons**: Full width, left-aligned text
- **Active Layer**: Blue background
- **Inactive Layers**: Gray background
- **Visibility**: Checkboxes (20px width)
- **Lock Indicator**: 🔒 emoji (20px width)
- **Control Buttons**: 80px width (Duplicate, Delete, Merge Down)
- **Add Layer Button**: 30x30 pixels with "+" text

### Timeline Panel
- **Frame Buttons**: 50x30 pixels, "F1", "F2" format
- **Control Buttons**: 30x30 pixels with Unicode symbols (◀ ▶ ⏹)
- **Playback Controls**: Horizontal layout with 5px spacing
- **Frame Control Buttons**: 80px width (Add Frame, Duplicate, Delete)
- **FPS Entry**: 40px width text input field

### Color Wheel
- **Canvas Size**: 200x200 pixels (hue wheel), 150x150 pixels (saturation)
- **Background**: Black
- **No Highlights**: highlightthickness=0
- **Action Buttons**: Standard height (30px), full width
- **Preview Area**: 80x80 pixels color preview frame
- **Value Labels**: 20px width labels, 40px width value displays

---

## Animation & Transitions

### Hover Animations
- **Color Buttons**: Instant size change (30px → 32px)
- **Border Changes**: Instant white border appearance
- **Color Changes**: Instant background color changes

### State Changes
- **Button States**: Instant color/background changes
- **Selection**: Instant border appearance
- **Grid Updates**: Immediate redraw

---

## Accessibility

### Visual Feedback
- **Clear Selection States**: Distinct colors for active/inactive
- **Hover Indicators**: Visual feedback on all interactive elements
- **Color Contrast**: High contrast for text and borders

### Keyboard Support
- **Tool Shortcuts**: Single letter (b, e, f, i, s, m, l, r, c)
- **Undo/Redo**: Ctrl+Z, Ctrl+Y, Ctrl+Shift+Z
- **Canvas Controls**: G for grid toggle

---

## Implementation Guidelines

### Creating New Components
1. **Use CTk Components**: Stick to CustomTkinter widgets
2. **Follow Spacing**: Use standard padding (10px) and spacing (5px)
3. **Consistent Sizing**: Use standard button sizes (30x30, 100x30)
4. **Color Consistency**: Use theme colors and standard hover effects
5. **State Management**: Implement proper selection and hover states

### Code Organization
```python
# Standard component creation pattern
def _create_component(self):
    # Container frame
    frame = ctk.CTkFrame(parent)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Title
    title = ctk.CTkLabel(frame, text="Title", font=ctk.CTkFont(size=16, weight="bold"))
    title.pack(pady=(10, 5))
    
    # Content
    # ... component-specific content
```

### Event Handling
```python
# Standard hover effect pattern
def _on_hover_enter(self, button):
    button.configure(border_width=2, border_color="white")
    button.configure(width=32, height=32)

def _on_hover_leave(self, button):
    button.configure(border_width=0, border_color="")
    button.configure(width=30, height=30)
```

---

## Future Considerations

### Extensibility
- **New Themes**: Color system designed for easy theme switching
- **New Components**: Standard patterns for consistent integration
- **Custom Widgets**: Follow established sizing and spacing patterns

### Maintenance
- **Centralized Colors**: Consider extracting color constants
- **Component Library**: Build reusable UI components
- **Theme System**: Implement theme switching capability

---

## Version History
- **v1.09**: Initial style guide creation and comprehensive audit
- **v1.08**: Hover effects and selection highlighting system
- **v1.07**: Color wheel integration and mode switching
- **v1.0**: Base dark theme with blue accents

---

*This style guide should be updated whenever new UI patterns are introduced or existing patterns are modified.*
