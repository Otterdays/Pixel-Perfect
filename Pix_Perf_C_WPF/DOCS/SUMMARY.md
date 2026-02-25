# Pixel Perfect C# WPF — Project Summary

## Project Status: 🟡 FOUNDATION BUILT — PARITY IN PROGRESS
**Version**: 0.2.0 (Parity Features)  
**Last Updated**: February 25, 2026  
**Platform**: Windows (.NET 8 / WPF)  

---

## What Is This?

This is the **clean rewrite** of [Pixel Perfect](../README.md) — originally a Python/CustomTkinter desktop pixel art editor that grew to v2.9.0 with 14+ tools, a layer system, animation timeline, 5 themes, and more. That version works great, but the codebase accumulated complexity over 100+ iterations.

This C#/WPF version is a **from-scratch rebuild** using:
- **.NET 8** — Modern, fast, cross-platform capable runtime
- **WPF** — Proven Windows UI framework with hardware-accelerated rendering
- **MVVM Pattern** — Clean architecture from day one using CommunityToolkit.Mvvm
- **WriteableBitmap** — Direct pixel manipulation for high-performance rendering

The goal is to replicate all features of the Python version with cleaner architecture and better performance.

---

## Current State (v0.2.0)

### ✅ Implemented
| Feature | Status | Notes |
|---------|--------|-------|
| Canvas System | ✅ | Presets 8×8–256×256, custom 1–512, `PixelCanvas` with layer management |
| Brush Tool | ✅ | Variable size (1px+), click and drag drawing |
| Eraser Tool | ✅ | Variable size, sets pixels to transparent |
| Fill Tool | ✅ | Scanline-optimized flood fill |
| Eyedropper Tool | ✅ | Pick color from canvas, auto-updates current color |
| Selection Tool | ✅ | Rectangle selection, Copy/Cut/Paste/Delete |
| Move Tool | ✅ | Non-destructive move with background preservation |
| Pan Tool | ✅ | Middle mouse, spacebar, or Pan tool (P) |
| Layer System | ✅ | Add layers, visibility toggle, active layer selection |
| Layer Blending | ✅ | Alpha-composited layer flattening |
| Zoom Control | ✅ | 1x–64x via dropdown, pixel-perfect NearestNeighbor scaling |
| Grid Overlay | ✅ | Toggle with G key, toolbar button |
| Color Picker | ✅ | SNES Classic 16-color palette grid |
| Dark Theme | ✅ | VS Code-inspired dark UI with custom button styles |
| Status Bar | ✅ | Shows cursor coordinates and tool status |
| MVVM Architecture | ✅ | Clean ViewModel with RelayCommands |
| Checkerboard BG | ✅ | Standard transparency indicator behind canvas |
| Undo/Redo | ✅ | Delta-based, groups pixel deltas into transactions |
| Keyboard Shortcuts | ✅ | B, E, F, I, L, R, C, G, P, S, M, Ctrl+C/X/V, Del, Ctrl+S/Z/Y/N |
| Shape Tools | ✅ | Line, Rectangle, Circle (Bresenham/Midpoint) with fluid preview |
| PNG Export | ✅ | Flattened canvas export to native Windows PNG |

### 🔲 Not Yet Implemented (from Python v2.9.0)
| Feature | Priority | Python Version Reference |
|---------|----------|--------------------------|
| Color Picker Full | 🟡 High | Primary, Wheel, Constants, Saved, Recent |
| Save/Load (.pixpf) | 🟡 High | Custom project format |
| Animation Timeline | 🟠 Medium | Frame management, playback, onion skinning |
| Grid Overlay | 🟠 Medium | Toggleable grid lines on canvas |
| Pan Tool | 🟠 Medium | Middle mouse / spacebar pan |
| Theme System | 🟢 Low | Multiple themes with customization |
| Symmetry Tools | 🟢 Low | X/Y/radial mirroring |
| Color Palettes | 🟢 Low | JSON palette loading, 30+ palettes |
| Spray/Dither Tools | 🟢 Low | Specialized drawing tools |
| Tile Preview | 🟢 Low | 3×3 repeating pattern view |
| Reference Panel | 🟢 Low | Load reference images |
| 3D Token Preview | 🟢 Low | Software voxel renderer |
| Godot Export | 🟢 Low | .tres/.tscn game-ready export |

---

## Architecture Overview

```
Pix_Perf_C_WPF/
├── Core/                        # Pure data models (no UI dependency)
│   ├── PixelColor.cs            # RGBA color struct (value type)
│   ├── Layer.cs                 # Pixel storage + visibility/opacity/lock
│   ├── PixelCanvas.cs           # Canvas state + layer management
│   ├── UndoManager.cs           # Delta-based undo/redo transactions
│   └── Tools.cs                 # ITool interface + 7 tool implementations
├── Services/
│   └── FileService.cs           # PNG export, save/load (planned)
├── Converters/
│   └── PixelColorToBrushConverter.cs  # PixelColor → SolidColorBrush for XAML
├── ViewModels/
│   └── MainViewModel.cs         # MVVM ViewModel (commands, state, rendering)
├── Views/
│   ├── MainWindow.xaml          # UI layout (3-column: tools | canvas | layers)
│   └── MainWindow.xaml.cs       # Mouse event handling (code-behind)
├── Themes/
│   └── DarkTheme.xaml           # Color resources + button styles
├── App.xaml                     # Entry point, theme loading
├── App.xaml.cs                  # Application startup
└── PixelPerfect.csproj          # .NET 8 project file
```

### Key Design Decisions
1. **MVVM from day one** — No giant God-class like the Python version's `main_window.py`
2. **Struct for colors** — `PixelColor` is a `readonly struct` for zero-allocation pixel ops
3. **ITool interface** — All tools implement a common interface for clean extensibility
4. **WriteableBitmap** — Direct pixel buffer writes for maximum rendering performance
5. **Core has no UI deps** — `Core/` namespace is pure logic, testable without WPF

---

## Comparison to Python Version

| Aspect | Python (v2.9.0) | C# WPF (v0.1.3) |
|--------|-----------------|-------------------|
| Lines of Code | ~15,000+ | ~1000 |
| Manager Classes | 12 | 1 (ViewModel) |
| Drawing Tools | 14 | 10 |
| Architecture | Evolved organically | Clean MVVM from start |
| Performance | Pillow compositing | WriteableBitmap (faster) |
| Rendering | PIL → tkinter canvas | Direct bitmap pixel writes |
| Dependencies | 4 (Pillow, numpy, customtkinter, pygame) | 1 (CommunityToolkit.Mvvm) |
| Platform | Windows/Mac/Linux | Windows (WPF) |
| Build Output | PyInstaller exe (29MB) | .NET publish (TBD) |

---

## Quick Start

```bash
# Prerequisites: .NET 8 SDK installed
cd Pix_Perf_C_WPF

dotnet restore   # Restore NuGet packages
dotnet build     # Compile
dotnet run       # Launch
```

---

## Documentation Index

| Document | Purpose |
|----------|---------|
| `DOCS/SUMMARY.md` | This file — project overview and status |
| `DOCS/PARITY.md` | Feature parity tracker vs Python v2.9.0 |
| `DOCS/ARCHITECTURE.md` | System design, class relationships, data flow |
| `DOCS/SCRATCHPAD.md` | Active memory — current tasks and context |
| `DOCS/SBOM.md` | Dependencies, versions, and security |
| `DOCS/CHANGELOG.md` | Version history |
| `DOCS/My_Thoughts.md` | AI reasoning and design decisions |
| `DOCS/REQUIREMENTS.md` | Feature requirements (ported from Python) |
| `README.md` | User-facing project README |
