# Pixel Perfect - Retro Pixel Art Editor

![Pixel Perfect Logo](assets/icons/logo.png) <!-- Placeholder -->

A **fully functional** desktop pixel art editor designed for creating 2D MMORPG game assets, inspired by classic SNES-era games like Curse of Aros. **Production ready with standalone executable** - no Python installation required!

## 🚀 Quick Start

### Download & Run (No Installation Required)
1. Download the latest release from `BUILDER/release/PixelPerfect/`
2. Extract the folder
3. Double-click `PixelPerfect.exe` to start creating pixel art!

### Build from Source
```bash
# Clone the repository
git clone https://github.com/AfyKirby1/Pixel-Perfect.git
cd Pixel-Perfect

# Install dependencies
pip install -r requirements.txt

# Run directly
python main.py

# Or build executable
cd BUILDER
build.bat
```

## ✅ Complete Feature Set

### 🎨 **Drawing Tools** (9 Complete Tools)
- **Pixel Brush**: Precise single-pixel placement with mouse drag
- **Eraser**: Clean pixel removal
- **Fill Bucket**: Flood fill with customizable tolerance
- **Eyedropper**: Color sampling from canvas
- **Selection Tool**: Rectangle selection and move
- **Line Tool**: Pixel-perfect line drawing (Bresenham's algorithm)
- **Rectangle Tool**: Rectangle and square drawing (hollow/filled)
- **Circle Tool**: Circle drawing with midpoint algorithm
- **Move Tool**: Move selected pixels around canvas

### 🖼️ **Canvas System**
- **Preset Sizes**: 16x16, 32x32, 16x32, 32x64 pixels
- **Zoom Levels**: 1x to 32x with **visible pixel grid**
- **Grid Overlay**: Toggleable grid for precise alignment
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

### 📚 **Layer System**
- **Multiple Layers**: Up to 10 layers per project
- **Layer Controls**: Visibility, opacity, reordering with UI buttons
- **Layer Management**: Naming, merging, duplication
- **Layer Effects**: Alpha blending for smooth composition
- **Layer Panel**: Complete UI for layer management

### 🎬 **Animation Timeline**
- **Frame Timeline**: 4-8 frame animation support (SNES style)
- **Playback Controls**: Play, pause, stop with adjustable FPS
- **Frame Management**: Add, duplicate, delete, reorder frames
- **Frame Navigation**: Previous/next frame buttons
- **Timeline UI**: Complete panel with frame thumbnails

### 💾 **Export & Project Management**
- **PNG Export**: Single frames with transparency (1x-8x scaling)
- **GIF Export**: Animated sprite export with frame timing
- **Sprite Sheets**: Horizontal, vertical, grid layouts with JSON metadata
- **Project Files**: Custom .pixpf format with full project data
- **Auto-Save**: Automatic save functionality
- **Recent Files**: Track and access recent projects

### 🎯 **Preset Templates** (8 Ready-to-Use)
- 32x32 Character (top-down)
- 16x32 Character (side-view)
- 16x16 Item icon
- 32x32 Item icon (detailed)
- 16x16 Grass tile
- 16x16 Stone tile
- 32x16 Button (UI)
- 16x16 Icon (UI)

### ⌨️ **Complete Keyboard Shortcuts**
- `B` - Brush tool
- `E` - Eraser tool
- `F` - Fill bucket
- `I` - Eyedropper
- `S` - Selection tool
- `M` - Move tool
- `L` - Line tool
- `R` - Rectangle tool
- `C` - Circle tool
- `G` - Toggle grid
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo
- `Ctrl+S` - Save project
- `Ctrl+O` - Open project
- `Ctrl+N` - New project

## 🛠️ Technology Stack

- **Language**: Python 3.13.6 (3.11+ compatible)
- **Graphics**: Pygame 2.6.1 (SDL 2.28.4)
- **UI**: CustomTkinter 5.2.0+ with Tkinter Canvas integration
- **Image Processing**: Pillow 10.0.0+
- **Numerical Computing**: NumPy 1.24.0+
- **Platform**: Windows 11 (Primary), cross-platform compatible

## 📋 System Requirements

- **OS**: Windows 11 (Primary), Windows 10, macOS, Linux
- **Python**: 3.11 or higher (Tested with 3.13.6) - Only needed for source build
- **RAM**: 4GB minimum, 8GB recommended
- **Display**: 1920x1080 recommended for full UI
- **Storage**: 100MB free space

## 🎮 Perfect for Game Development

Designed specifically for creating assets for 2D MMORPG games like:
- **Curse of Aros** style sprites
- **SNES-era** pixel art aesthetics
- **Retro gaming** character sprites
- **Tile-based** game assets
- **UI elements** and icons

## 📁 Project Structure

```
Pixel Perfect/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── launch.bat             # Windows launcher
├── assets/                # Color palettes and icons
├── src/                   # Source code
│   ├── core/              # Core systems (canvas, layers, etc.)
│   ├── tools/             # Drawing tools
│   ├── ui/                # User interface
│   ├── utils/             # Utilities (export, presets)
│   └── animation/         # Animation system
├── docs/                  # Documentation
├── BUILDER/               # Build system
│   ├── build.bat          # Build script
│   ├── dist/              # Built executable
│   └── release/           # Distribution package
└── test_*.py              # Test suites
```

## 🚀 Performance

- **60fps rendering** at all zoom levels (1x-32x)
- **Responsive drawing** with immediate pixel display
- **Efficient memory usage** for large projects
- **Smooth animation playback** up to 60fps
- **No crashes or freezes** - stable operation

## 📖 Documentation

- **[Architecture](docs/ARCHITECTURE.md)** - System design and architecture
- **[Summary](docs/SUMMARY.md)** - Project overview and status
- **[SBOM](docs/SBOM.md)** - Software Bill of Materials
- **[Build Guide](BUILDER/README.md)** - Detailed build instructions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. See LICENSE file for details.

## 🎯 Future Roadmap

### Phase 2: Advanced Features
- Onion skinning overlay for animation
- Advanced animation tools (tweening, in-betweening)
- Custom brush shapes and sizes
- HSV color wheel picker

### Phase 3: AI Integration
- Text-to-sprite generation
- Style transfer matching game aesthetics
- Auto-palette generation
- AI-powered animation assistance

---

**Ready to create pixel art for your 2D MMORPG!** 🎮✨

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/AfyKirby1/Pixel-Perfect/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AfyKirby1/Pixel-Perfect/discussions)
- **Email**: motorcycler14@yahoo.com

---

**Made with ❤️ for the pixel art community**
