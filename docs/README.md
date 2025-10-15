# Pixel Perfect - Retro Pixel Art Editor

![Pixel Perfect Logo](assets/icons/logo.png) <!-- Placeholder -->

A **fully functional** desktop pixel art editor designed for creating 2D MMORPG game assets, inspired by classic SNES-era games like Curse of Aros. **Production ready with standalone executable** - no Python installation required!

## ✅ Complete Feature Set

### 🎨 **Drawing Tools** (10 Complete Tools)
- **Pixel Brush**: Precise single-pixel placement with mouse drag (pencil cursor)
- **Eraser**: Clean pixel removal (X cursor)
- **Fill Bucket**: Flood fill with customizable tolerance (spraycan cursor)
- **Eyedropper**: Color sampling from canvas (crosshair cursor)
- **Selection Tool**: Rectangle selection and move (crosshair cursor)
- **Line Tool**: Pixel-perfect line drawing (Bresenham's algorithm, pencil cursor)
- **Square Tool**: Rectangle and square drawing (hollow/filled, plus cursor)
- **Circle Tool**: Circle drawing with midpoint algorithm (circle cursor)
- **Move Tool**: Move selected pixels around canvas (4-way arrow cursor)
- **Pan Tool**: Move camera view around canvas (open hand → grabbing hand cursor)

**Visual Feedback**: Each tool has a unique cursor icon for clear visual indication of the active tool!

### 🖼️ **Canvas System** (Grid Fixed!)
- **Preset Sizes**: 16x16, 32x32, 16x32, 32x64, 64x64 pixels
- **Zoom Levels**: 1x to 32x with **visible pixel grid**
- **Grid Overlay**: Toggleable grid for precise alignment (now working!)
- **Custom Backgrounds**: Checkerboard transparency pattern
- **Mouse Integration**: Click and drag to draw pixels

### 🎨 **Color Management** (6 Complete Palettes)
- **SNES Classic**: 16 colors matching original SNES palette
- **Curse of Aros**: Muted, earthy tones matching the game aesthetic
- **Heartwood Online**: Forest-themed palette
- **Definya**: Bright, vibrant colors
- **Kakele Online**: Warm, golden palette
- **Rucoy Online**: Grayscale palette with earth tones
- **Custom Palettes**: Create and save your own color sets
- **Primary/Secondary**: Quick color switching with visual feedback

### 📚 **Layer System** (Complete UI Integration)
- **Multiple Layers**: Up to 10 layers per project
- **Layer Controls**: Visibility, opacity, reordering with UI buttons
- **Layer Management**: Naming, merging, duplication
- **Layer Effects**: Alpha blending for smooth composition
- **Layer Panel**: Complete UI for layer management

### 🎬 **Animation Timeline** (Complete Implementation)
- **Frame Timeline**: 4-8 frame animation support (SNES style)
- **Playback Controls**: Play, pause, stop with adjustable FPS
- **Frame Management**: Add, duplicate, delete, reorder frames
- **Frame Navigation**: Previous/next frame buttons
- **Timeline UI**: Complete panel with frame thumbnails

### ↩️ **Undo/Redo System** (Complete)
- **50+ State Management**: Comprehensive undo/redo history
- **Layer State Tracking**: Undo/redo per layer
- **Keyboard Shortcuts**: Ctrl+Z (undo), Ctrl+Y (redo)
- **Visual Feedback**: Undo/redo button states

### 📤 **Export Options** (Complete Implementation)
- **PNG Export**: Single frames with transparency support
- **GIF Animation**: Animated sprite export with frame timing
- **Sprite Sheets**: Horizontal, vertical, or grid layouts
- **Multiple Scales**: 1x, 2x, 4x, 8x scaling options
- **JSON Metadata**: Coordinate data for game engines

### 💾 **Project System** (Complete)
- **Custom Format**: `.pixpf` files with full project data
- **Save/Load**: Complete project persistence
- **Recent Files**: Track and access recent projects
- **Metadata**: Project information and settings

### 🎯 **Preset Templates** (8 Ready-to-Use Templates)
- **Character Templates**: 32x32 and 16x32 character sprites
- **Item Templates**: 16x16 and 32x32 item icons
- **Tile Templates**: Grass and stone environment tiles
- **UI Templates**: Buttons and icons for interfaces
- **Template Browser**: Easy access to all presets

## Installation & Setup

### Windows 11 (Primary Platform)

1. **Install Python 3.11+**
   ```bash
   # Download from python.org
   # Make sure "Add to PATH" is checked
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Pixel Perfect**
   ```bash
   python main.py
   ```
   Or double-click `launch.bat` for easy startup

### Building Standalone Executable

Want to create a distributable EXE file?

1. **Navigate to BUILDER folder**
   ```bash
   cd BUILDER
   ```

2. **Run the build script**
   ```bash
   build.bat
   ```

3. **Find your executable**
   - Executable: `BUILDER/dist/PixelPerfect.exe`
   - Distribution package: `BUILDER/release/PixelPerfect/`

The build script automatically:
- Installs PyInstaller if needed
- Bundles all dependencies
- Includes assets and documentation
- Creates a ready-to-distribute package
- Cleans up temporary files

**Pre-built executable available**: Download `BUILDER/release/PixelPerfect/PixelPerfect.exe` for instant use!

See `BUILDER/README.md` for detailed build documentation.

## Quick Start Guide

1. **Launch** Pixel Perfect (`python main.py`)
2. **Select Tool** from the Tools panel (Brush is selected by default)
3. **Choose Color** from the Palette panel (SNES Classic loaded by default)
4. **Start Drawing** - Click and drag on the canvas (grid is now visible!)
5. **Add Layers** using the + button in the Layers panel
6. **Create Animation** using the Timeline panel controls
7. **Export** your work using File menu options

## Complete Keyboard Shortcuts

### Drawing Tools
- `B` - Brush tool (pencil cursor)
- `E` - Eraser tool (X cursor)
- `F` - Fill bucket (spraycan cursor)
- `I` - Eyedropper (crosshair cursor)
- `S` - Selection tool (crosshair cursor)
- `M` - Move tool (4-way arrow cursor)
- `L` - Line tool (pencil cursor)
- `R` - Square tool (plus cursor)
- `C` - Circle tool (circle cursor)

### Canvas Controls
- `Ctrl + Plus` - Zoom in
- `Ctrl + Minus` - Zoom out
- `Ctrl + 0` - Reset zoom
- `G` - Toggle grid (now working!)

### Layer Management
- `Ctrl + Shift + N` - New layer
- `Ctrl + Shift + D` - Duplicate layer
- `Delete` - Delete layer
- `Ctrl + Shift + M` - Merge layers

### Animation Controls
- `Space` - Play/pause animation
- `,` (comma) - Previous frame
- `.` (period) - Next frame
- `Ctrl + Shift + F` - Add frame

### File Operations
- `Ctrl + N` - New project
- `Ctrl + O` - Open project
- `Ctrl + S` - Save project
- `Ctrl + Shift + S` - Save as
- `Ctrl + E` - Export

### Edit Operations
- `Ctrl + Z` - Undo
- `Ctrl + Y` - Redo
- `Ctrl + C` - Copy
- `Ctrl + V` - Paste
- `Ctrl + A` - Select all

## Project Files

Pixel Perfect uses a custom `.pixpf` format that includes:
- Canvas settings (size, zoom, grid state)
- Color palette configuration
- All layer data with visibility and opacity
- Animation frames and timing
- Project metadata (author, description, creation date)

## Export Formats

### PNG Export
- Single frame export with transparency
- Multiple scale options (1x, 2x, 4x, 8x)
- Perfect for static sprites and UI elements

### GIF Animation
- Animated sprite export
- Customizable frame timing and loop settings
- Ideal for character animations and effects

### Sprite Sheets
- Multiple frames in organized layouts
- Horizontal, vertical, or grid arrangements
- JSON metadata for easy game engine integration
- Scale options for different resolutions

## Template System

### Character Templates
- **32x32 Character**: Top-down character sprite template
- **16x32 Character**: Side-view character template

### Item Templates
- **16x16 Item**: Small item icon template
- **32x32 Item**: Detailed item icon template

### Environment Templates
- **16x16 Grass Tile**: Basic terrain tile
- **16x16 Stone Tile**: Structure/path tile

### UI Templates
- **32x16 Button**: Interface button template
- **16x16 Icon**: UI icon template

## System Requirements

- **OS**: Windows 11 (primary), cross-platform compatible
- **Python**: 3.11 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 100MB free space
- **Display**: 1920x1080 recommended for full UI

## Performance

- **60fps rendering** at all zoom levels (1x-32x)
- **Responsive drawing** with mouse integration
- **Efficient memory usage** for large projects
- **Smooth animation playback** up to 60fps

## Troubleshooting

### Grid Not Visible (FIXED)
- **Issue**: Grid overlay not showing on canvas
- **Solution**: Grid rendering algorithm updated - now visible at all zoom levels
- **Verification**: Run application and grid should be clearly visible

### Mouse Drawing Not Working
- **Issue**: Unable to draw on canvas
- **Solution**: Mouse event integration completed - click and drag now works
- **Verification**: Select brush tool and draw on canvas

## Development Status

**Version 1.15 - Tool Cursor Feedback**
- ✅ Visual cursor feedback for all tools
- ✅ Rectangle renamed to Square for clarity
- ✅ Professional tool experience

**Version 0.04 - Complete Implementation**
- ✅ All planned features implemented
- ✅ Grid visibility fixed
- ✅ Mouse drawing working
- ✅ Animation system complete
- ✅ Export functionality working
- ✅ Project save/load operational
- ✅ Preset templates available
- ✅ Comprehensive testing passed (6/6 test suites)

## Future Enhancements

### Planned for Phase 2
- **Onion Skinning**: See previous/next frames while drawing
- **Advanced Animation Tools**: In-betweening and tweening
- **Brush Presets**: Custom brush shapes and sizes
- **Color Picker Enhancements**: HSV color wheel and palettes

### AI Integration (Phase 3)
- **Text-to-Sprite**: Generate sprites from descriptions
- **Style Transfer**: Apply Curse of Aros aesthetic to images
- **Auto-Palette Generation**: Extract palettes from reference images
- **Animation Assistance**: AI-powered in-betweening

## Contributing

The modular architecture makes it easy to add new features. Each tool, export format, and UI component is implemented as a separate module.

## License

*Currently in development - license to be determined for future releases*

## Support & Documentation

Complete documentation available in the `docs/` folder:
- **ARCHITECTURE.md**: Technical architecture and component breakdown
- **SCRATCHPAD.md**: Development notes and version history
- **SBOM.md**: Software Bill of Materials and dependencies
- **SUMMARY.md**: Project status and feature overview
- **AI_PYTHON_KNOWLEDGE.md**: Comprehensive Python guide for AI agents (NEW!)

---

**Pixel Perfect** - Professional pixel art creation tool! 🎮✨

*Ready for creating sprites, tiles, and animations for your 2D MMORPG projects!*
