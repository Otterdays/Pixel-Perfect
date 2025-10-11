# Pixel Perfect - Architecture Documentation

## System Overview
Pixel Perfect is a fully functional desktop pixel art editor built with Python, designed for creating 2D MMORPG game assets. The architecture follows a modular design pattern with comprehensive feature set including animation, layers, custom colors, and export capabilities.

## Current Status: COMPLETE IMPLEMENTATION
**Version**: 1.12
**Status**: All Features Complete - Production Ready with Full System Integration

### Latest Update (v1.12)
- **Custom Colors System**: User-specific persistent color library with local storage

## Core Components

### Canvas System (`src/core/canvas.py`)
- **Purpose**: Main drawing surface with pixel-perfect grid rendering
- **Key Features**:
  - Zoom levels (1x to 32x) with visible grid overlay
  - Preset canvas sizes (16x16, 32x32, 16x32, 32x64, 64x64)
  - Grid overlay with toggle and proper visibility
  - Mouse position tracking and coordinate conversion
  - Real-time pixel manipulation with numpy arrays
- **Dependencies**: Pygame for rendering, numpy for efficient pixel operations

### Color Palette (`src/core/color_palette.py`)
- **Purpose**: Manages color palettes and selection
- **Key Features**:
  - 6 preset SNES-inspired palettes including Curse of Aros style
  - Custom palette creation and management
  - Primary/secondary color selection with UI integration
  - Palette persistence (JSON format)
  - 8-16 color limitation for authentic retro feel

### Custom Colors Manager (`src/core/custom_colors.py`)
- **Purpose**: User-specific persistent color library with local storage
- **Key Features**:
  - User-specific storage path (Windows: `AppData\Local\PixelPerfect`, Mac/Linux: `~/.pixelperfect`)
  - Persistent across all sessions and projects
  - Maximum 32 colors per user
  - Duplicate prevention and limit protection
  - JSON storage format (`custom_colors.json`)
  - Not bundled with executable (empty for fresh installs)
  - OS-independent path resolution

### Layer Manager (`src/core/layer_manager.py`)
- **Purpose**: Handles multiple drawing layers with full UI integration and immediate visual updates
- **Key Features**:
  - Layer visibility and opacity controls with instant canvas refresh
  - Layer reordering and management with proper drawing integration
  - Layer merging and duplication with full UI feedback
  - Layer naming and organization
  - Alpha blending for smooth layer composition
  - "Show all layers" mode for viewing combined layers
  - Drawing layer auto-selection when no layer is specifically selected
  - Canvas interface compatibility for seamless tool integration
  - Complete Canvas interface implementation (set_pixel, get_pixel, width, height, zoom)
  - Real-time canvas updates for all layer operations

### Project System (`src/core/project.py`)
- **Purpose**: Save/load project files with metadata
- **Key Features**:
  - Custom .pixpf format with JSON structure
  - Auto-save functionality and recent files tracking
  - Project metadata storage and version control
  - Cross-platform file handling

## Tool System (`src/tools/`)
Complete modular tool architecture with 9 implemented tools, all fully integrated with layer system:

### Tool Interface
```python
class Tool:
    def on_mouse_down(self, canvas, x, y, button, color): pass
    def on_mouse_up(self, canvas, x, y, button, color): pass
    def on_mouse_move(self, canvas, x, y, color): pass
    def draw_preview(self, surface, x, y, color): pass
```

**Enhanced Integration**: All tools now work seamlessly with both Canvas and Layer objects through unified interface compatibility.

### Available Tools (All Implemented)
- **Brush** (`brush.py`): Single pixel placement with mouse drag support
- **Eraser** (`eraser.py`): Pixel removal tool
- **Fill** (`fill.py`): Bucket fill with flood algorithm
- **Eyedropper** (`eyedropper.py`): Smart color sampling with palette/color wheel integration
- **Selection** (`selection.py`): Rectangle selection and move tool
- **Move** (`move.py`): Move selected pixels
- **Line** (`line.py`): Pixel-perfect line drawing (Bresenham's algorithm)
- **Rectangle** (`rectangle.py`): Rectangle and square drawing (hollow/filled)
- **Circle** (`circle.py`): Circle drawing with midpoint algorithm

## Animation System (`src/animation/`)

### Timeline (`timeline.py`)
- **Status**: Fully implemented with UI integration
- Frame management (4-8 frame limit as per SNES style)
- Onion skinning overlay (planned for future)
- Playback controls with adjustable FPS
- Frame reordering and duplication
- Animation loop control

### Frame Manager (Integrated in timeline.py)
- Individual frame storage with pixel data
- Frame duration control
- Animation export preparation

## UI System (`src/ui/`)

### Main Window (`main_window.py`)
- **Status**: Complete implementation with full functionality
- Application entry point with comprehensive event handling
- Coordinates all UI panels with proper integration
- Mouse event routing to canvas tools
- Keyboard shortcuts for all major functions

### UI Panels (All Implemented)
- **Tool Panel**: Tool selection with visual feedback
- **Palette Panel** (`palette_panel.py`): Color palette display and management
- **Layer Panel** (`layer_panel.py`): Complete layer management UI
- **Timeline Panel** (`timeline_panel.py`): Animation timeline controls

## Utility Systems (`src/utils/`)

### Export (`export.py`)
- **Status**: Complete implementation with multiple formats
- PNG export with transparency support
- GIF animation export with frame timing
- Sprite sheet generation (horizontal/vertical/grid layouts)
- Multiple scale factors (1x, 2x, 4x, 8x)
- JSON metadata for sprite sheets

### Presets (`presets.py`)
- **Status**: Complete with 8 ready-to-use templates
- Template management across 5 categories
- Character sprite templates (32x32, 16x32)
- Item icon templates (16x16, 32x32)
- Environment tile templates (grass, stone)
- UI element templates (buttons, icons)
- Custom template creation from canvas

## Data Flow (Complete Implementation)

1. **User Input** → Main Window → Tool System → Canvas
2. **Tool Actions** → Canvas → Layer Manager → Undo/Redo System
3. **Canvas Changes** → Active Layer → Timeline Frame → Visual Update
4. **Export Request** → Export System → File Output
5. **Project Save/Load** → Project System → Persistent Storage

## Extension Points for Future AI Integration

### Planned AI Module (`src/ai/`)
- Text-to-sprite generation using Stable Diffusion + ControlNet
- Style transfer matching Curse of Aros aesthetic
- Auto-palette generation from reference images
- Animation in-betweening assistance
- Tile pattern generation from descriptions

### Integration Strategy
- Keep AI features in separate module for easy addition
- Use plugin architecture for AI tools
- Maintain full compatibility with manual tools
- No refactoring needed for core systems

## File Format Specification

### Project File (.pixpf) - Fully Implemented
```json
{
  "version": "1.0",
  "created": "2024-10-08T12:00:00",
  "modified": "2024-10-08T14:30:00",
  "canvas": {
    "width": 32,
    "height": 32,
    "zoom": 8,
    "show_grid": true,
    "checkerboard": true
  },
  "palette": {
    "name": "Curse of Aros",
    "type": "curse_of_aros",
    "colors": [[45,45,45,255], ...],
    "primary_color": 0,
    "secondary_color": 1
  },
  "layers": [
    {
      "index": 0,
      "name": "Background",
      "visible": true,
      "opacity": 1.0,
      "locked": false,
      "pixels": [[...], [...]]
    }
  ],
  "animation": {
    "current_frame": 0,
    "fps": 12,
    "loop": true,
    "frames": [
      {
        "index": 0,
        "name": "Frame 1",
        "duration": 100,
        "pixels": [[...], [...]]
      }
    ]
  },
  "metadata": {
    "author": "User",
    "description": "Character sprite"
  }
}
```

### Export Formats
- **PNG**: Individual frames with transparency
- **GIF**: Animated sprite export with timing
- **Sprite Sheet**: Multiple frames in grid layout with JSON metadata

## Recent System Integration Improvements (v1.12)

### Complete Layer System Integration
- **Canvas Interface Compatibility**: Layer objects now implement complete Canvas interface (set_pixel, get_pixel, width, height, zoom)
- **Real-time Visual Updates**: All layer operations (visibility, drawing, selection) update canvas display immediately
- **Smart Drawing Layer Selection**: Automatic selection of appropriate layer for drawing when no layer is specifically selected
- **Unified Tool Integration**: All 9 tools work seamlessly with both Canvas and Layer objects

### Enhanced Eyedropper Tool
- **Smart Color Detection**: Automatically detects if sampled color exists in current palette
- **Palette Integration**: Sets primary/secondary color and updates UI highlights when color found in palette
- **Color Wheel Fallback**: Automatically switches to color wheel mode for non-palette colors
- **Left/Right Click Support**: Left click sets primary color, right click sets secondary color

### UI/UX Improvements
- **Button Optimization**: Fixed button truncation issues with optimized sizing and spacing
- **Consistent Styling**: Uniform button heights (28px) and fonts (12px) across all panels
- **Professional Appearance**: Clean, modern interface with no visual artifacts

## Performance Achievements
- **60fps rendering** achieved at 32x zoom
- **Efficient pixel manipulation** using numpy arrays
- **Minimal memory footprint** for undo system (50+ states)
- **Optimized rendering pipeline** with Pygame surface management
- **Smooth mouse interaction** with coordinate conversion
- **Responsive UI** with CustomTkinter integration
- **Real-time layer updates** with immediate visual feedback
- **Efficient canvas refresh** system for seamless user experience

## Security and Maintenance
- All dependencies tracked in SBOM.md
- Regular update schedule for security patches
- Cross-platform compatibility maintained
- No external API dependencies in core functionality
