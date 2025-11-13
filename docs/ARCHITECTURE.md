# Pixel Perfect - Architecture Documentation

## System Overview
Pixel Perfect is a fully functional desktop pixel art editor built with Python, designed for creating 2D MMORPG game assets. The architecture follows a modular design pattern with comprehensive features including animation, layers, custom colors, palette management, and export capabilities.

## Current Status: COMPLETE IMPLEMENTATION
**Version**: 2.6.0  
**Status**: All Core Systems Complete - Production Ready with Spray Tool & Palette Overhaul

### Latest Updates
- **v2.6.0**: Added Spray tool, canvas zoom scrollbar, and JSON palette auto-loader.
- **v2.5.x**: Palette UX hardening (highlighting, saved color behavior, edge tool fixes).
- **v2.0.x**: Build size optimization, panel refactors, background/grid texture modes.

## Core Components

### Canvas System (`src/core/canvas.py`)
- **Purpose**: Main drawing surface with pixel-perfect grid rendering.
- **Key Features**:
  - Zoom levels (0.25× to 64×) with visible grid overlay.
  - Preset canvas sizes (8×8 through 64×64) plus custom sizing.
  - Grid overlay with toggle and overlay mode to render on top of pixels.
  - Paper/background texture modes rendered directly in Tkinter.
  - Mouse position tracking and coordinate conversion helpers.
  - Real-time pixel manipulation backed by numpy arrays.
  - Pan tool for camera movement around canvas.
- **Dependencies**: Native `tkinter` canvas via CustomTkinter plus numpy for efficient pixel operations.

### Color Palette (`src/core/color_palette.py`)
- **Purpose**: Manages palette discovery, loading, and selection.
- **Key Features**:
  - Auto-discovers all JSON palettes in `assets/palettes/` at startup.
  - Default fallback SNES Classic palette when no JSON files exist.
  - Primary/secondary color selection with UI integration.
  - Palette persistence (JSON format) with primary/secondary indexes.
  - Duplicate-name handling ensures unique dropdown entries (`Name (2)`).

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

### Canvas Renderer (`src/core/canvas_renderer.py`)
- **Purpose**: Centralized rendering system for canvas visualization
- **Key Features**:
  - Efficient pixel rendering with zoom support
  - Selection box and move preview visualization
  - Tool cursor feedback and preview rendering
  - Grid overlay and visual effects
  - Coordinate conversion and bounds checking

### Event Dispatcher (`src/core/event_dispatcher.py`)
- **Purpose**: Centralized event handling and routing
- **Key Features**:
  - Window and panel event management
  - Keyboard shortcut handling
  - Mouse event routing to tools
  - Tool preview coordination
  - UI callback delegation

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
Complete modular tool architecture with fully integrated drawing, transformation, and utility tools:

### Tool Interface
```python
class Tool:
    def on_mouse_down(self, canvas, x, y, button, color): pass
    def on_mouse_up(self, canvas, x, y, button, color): pass
    def on_mouse_move(self, canvas, x, y, color): pass
    def draw_preview(self, surface, x, y, color): pass
```

**Enhanced Integration**: All tools now work seamlessly with both Canvas and Layer objects through unified interface compatibility.

- **Brush** (`brush.py`): Multi-size brush strokes via `ToolSizeManager`.
- **Eraser** (`eraser.py`): Multi-size erasing with undo support.
- **Spray** (`spray.py`): Radius/density-controlled spray paint with live preview.
- **Fill** (`fill.py`): Bucket fill with flood algorithm.
- **Eyedropper** (`eyedropper.py`): Smart color sampling with palette/color wheel integration.
- **Selection** (`selection.py`): Rectangle selection and move staging.
- **Move** (`move.py`): Non-destructive move with background restoration.
- **Line** (`line.py`): Pixel-perfect line drawing (Bresenham's algorithm).
- **Rectangle** (`rectangle.py`): Rectangle and square drawing (hollow/filled).
- **Circle** (`circle.py`): Circle drawing with midpoint algorithm.
- **Texture** (`texture.py`): Pattern stamping with configurable libraries.
- **Pan** (`pan.py`): Canvas navigation while maintaining zoom.
- **Edge** (`edge.py`): Sub-pixel edge outlining with thickness controls.

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

### Component Managers (Refactored v1.62-1.69)
- **File Operations Manager** (`file_operations_manager.py`): New, Open, Save, Import, Export operations
- **Dialog Manager** (`dialog_manager.py`): Custom dialogs (size, downsize warning, texture panel)
- **Selection Manager** (`selection_manager.py`): Mirror, rotate, copy, scale transformations
- **Tool Size Manager** (`tool_size_manager.py`): Brush/eraser size management
- **Canvas Zoom Manager** (`canvas_zoom_manager.py`): Canvas resize and zoom controls
- **Canvas Scrollbar** (`canvas_scrollbar.py`): Themed on-canvas zoom scrollbar with drag + button controls
- **Grid Control Manager** (`grid_control_manager.py`): Grid visibility and overlay toggles
- **Theme Dialog Manager** (`theme_dialog_manager.py`): Theme selection and management
- **UI Builder** (`ui_builder.py`): Toolbar and UI component construction

### Main Window (`main_window.py`)
- **Status**: Complete implementation with modular architecture
- Application entry point with event delegation to managers
- Coordinates all UI panels with proper integration
- Mouse event routing through EventDispatcher
- Keyboard shortcuts for all major functions
- **Theme System** (v1.22): Real-time UI color scheme switching with callback architecture
- **Collapsible Panels** (v1.24): Hide/show side panels for maximum canvas space
- **Grid Overlay** (v1.25): Toggle grid lines on top of pixels for precise editing
- **Responsive Panel Sizing** (v1.52): Automatic panel width calculation based on screen resolution with state persistence
- **Modular Refactoring** (v1.62-1.69): Extracted managers for cleaner architecture (File Operations, Dialog, Selection, Tool Size, Canvas/Zoom, Grid Control)

### Toolbar Components
- **File Menu**: New, Open, Save, Export options
- **Size Dropdown**: Canvas size selection (8×8 to 64×64 plus custom)
- **Zoom Dropdown**: Zoom level control (0.25× to 64×) synchronized with on-canvas scrollbar
- **Undo/Redo Buttons**: Arrow buttons (↶ ↷) with visual state feedback
- **Theme Dropdown**: Switch between Basic Grey and Angelic themes
- **Grid Button**: Toggle grid visibility (ON/OFF with color feedback)
- **Grid Overlay Button** (v1.25): Toggle grid lines on top of pixels (Overlay ON/OFF)

### UI Panels (All Implemented)
- **Tool Panel**: Tool selection with visual feedback, 3×3 grid layout
- **Palette Panel**: Color palette display and management (Grid/Primary/Wheel views)
- **Layer Panel** (`layer_panel.py`): Complete layer management UI with visibility toggles
- **Timeline Panel** (`timeline_panel.py`): Animation timeline controls with frame management
- **Notes Panel** (`notes_panel.py`) (v1.71): Persistent note-taking with auto-save and TXT export
- **Collapsible Side Panels** (v1.24): 
  - Left panel: Tools and palette (collapse with ◀ button)
  - Right panel: Layers and animation (collapse with ▶ button)
  - Restore buttons appear when collapsed (blue arrow buttons)
  - Resizable with draggable sash dividers (10px wide)
- **Responsive Panel Sizing** (v1.52):
  - Automatic panel width calculation based on screen resolution
  - Resolution-based sizing: Small (280+260px), Standard (350+320px), Large (400+380px), Ultra-wide (450+420px)
  - Window state persistence saves/restores panel sizes between sessions
  - State saved to `~/.pixelperfect/window_state.json`
  - Automatic recalculation if screen resolution changes

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

1. **User Input** → Main Window → Event Dispatcher → Tool System → Layer
2. **Tool Actions** → Layer → Canvas Renderer → Visual Update
3. **Layer Changes** → Undo Manager → State History
4. **Canvas Changes** → Active Layer → Timeline Frame → Visual Update
5. **Export Request** → File Operations Manager → Export System → File Output
6. **Project Save/Load** → File Operations Manager → Project System → Persistent Storage
7. **UI Events** → Component Managers → Main Window → Canvas Update

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
- **60fps rendering** achieved at 64× zoom
- **Efficient pixel manipulation** using numpy arrays
- **Minimal memory footprint** for undo system (50+ states)
- **Optimized rendering pipeline** with Tkinter + PIL rendering (v1.30+)
- **Smooth mouse interaction** with coordinate conversion
- **Responsive UI** with CustomTkinter integration
- **Real-time layer updates** with immediate visual feedback
- **Efficient canvas refresh** system for seamless user experience
- **Modular architecture** reduces token consumption and improves maintainability (v1.62-1.69)
- **Instant palette view switching** (<10ms, 50-100× faster with pre-rendering)

## Security and Maintenance
- All dependencies tracked in SBOM.md
- Regular update schedule for security patches
- Cross-platform compatibility maintained
- No external API dependencies in core functionality
- Modular architecture enables easier testing and debugging
- Component extraction reduces complexity (main_window.py: 3,387 → 1,582 lines, 53.3% reduction)

## Recent Architectural Improvements (v1.62-1.71)

### Code Refactoring Initiative
**Goal**: Reduce main_window.py from 3,387 lines to ~850 lines by extracting specialized managers

**Completed Extractions**:
1. **Phase 3** (v1.62): File Operations Manager - 10 methods, 395 lines extracted
2. **Phase 4** (v1.64): Dialog Manager - 5 methods, 417 lines extracted  
3. **Phase 5** (v1.65): Selection Manager - 10 methods, 438 lines extracted
4. **Phase 6-7** (v1.68): Tool Size Manager (163 lines) + Canvas/Zoom Manager (226 lines)
5. **Phase 8** (v1.69): Grid Control Manager - 4 methods, 68 lines extracted

**Results**:
- main_window.py reduced from 3,387 → 1,582 lines (53.3% reduction)
- 8 new manager modules created for specialized functionality
- Improved code organization and maintainability
- Easier testing and debugging
- Reduced token consumption for AI-assisted development

### New Components
- **Notes Panel** (v1.71): Persistent note-taking with auto-save to `~/.pixelperfect/notes.json`
- **Palette Views Package**: Modularized color palette views (Grid, Primary, Saved, Constants)
- **Manager Classes**: Specialized managers for file operations, dialogs, selections, tools, canvas, and grid
