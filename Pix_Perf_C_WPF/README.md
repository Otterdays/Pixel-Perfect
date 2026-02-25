# 🎨 Pixel Perfect — C# WPF Edition

> A professional pixel art editor rebuilt from the ground up in C# with WPF.  
> Clean architecture. High performance. Windows-native.

---

## About This Version

This is the **C# / WPF rewrite** of [Pixel Perfect](../README.md) — a desktop pixel art editor originally built in Python/CustomTkinter. The Python version grew to v2.9.0 with 14+ tools, layers, animation, and 5 themes, but accumulated complexity over 100+ iterations.

This rewrite starts clean with:
- **MVVM architecture** from day one (no god-class refactors later)
- **WriteableBitmap** for direct, high-performance pixel manipulation
- **CommunityToolkit.Mvvm** for type-safe, source-generated bindings
- **.NET 8** — fast, modern, and ready for future features

---

## Current State (v0.2.0)

✅ Working:
- Brush, Eraser, Fill (scanline), and Eyedropper tools
- Shape Tools (Line, Rectangle, Circle) with fluid preview
- Selection Tool (S) — rectangle select, Copy/Cut/Paste/Delete
- Move Tool (M) — non-destructive move with background preservation
- Pan Tool (P) — middle mouse, spacebar, or Pan tool
- Undo/Redo system (delta-based)
- Multi-layer system with visibility toggle and alpha compositing
- Canvas size presets (8×8–256×256) and custom size via New Canvas dialog
- Grid overlay toggle (G key)
- Color picker panel (SNES Classic 16-color palette)
- Zoom control (1x–64x) with pixel-perfect NearestNeighbor rendering
- Zero-allocation rendering pipeline
- PNG export (Save to PNG)
- Keyboard shortcuts (B, E, F, I, L, R, C, G, P, S, M, Ctrl+C/X/V, Del, Ctrl+S/Z/Y/N)
- Checkerboard transparency background
- Dark theme (VS Code-inspired)
- Status bar with cursor coordinates

🔲 Coming next:
- Save/Load .pixpf project format
- Animation timeline
- Spray and Dither tools

---

## Prerequisites

- [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)
- Windows 10 or 11
- Visual Studio 2022 **or** VS Code with C# Dev Kit extension

---

## Building & Running

```powershell
# From the Pix_Perf_C_WPF directory:
dotnet restore    # Restore NuGet packages
dotnet build      # Compile
dotnet run        # Launch the application
```

---

## Project Structure

```
Pix_Perf_C_WPF/
├── Core/                     # Pure data models (no UI dependency)
│   ├── PixelColor.cs         # RGBA color (readonly struct)
│   ├── Layer.cs              # Pixel layer with visibility/opacity/lock
│   ├── PixelCanvas.cs        # Canvas + layer management + alpha blending
│   ├── UndoManager.cs        # Delta-based undo/redo
│   └── Tools.cs              # ITool + Brush/Eraser/Fill/Eyedropper/Line/Rect/Circle
├── Services/
│   └── FileService.cs        # PNG export
├── Converters/
│   └── PixelColorToBrushConverter.cs
├── ViewModels/
│   └── MainViewModel.cs      # MVVM ViewModel — commands, state, rendering
├── Views/
│   ├── MainWindow.xaml       # 3-column UI layout
│   └── MainWindow.xaml.cs    # Mouse event handling only
├── Themes/
│   └── DarkTheme.xaml        # Color tokens + ToolButton style
├── DOCS/                     # Project documentation
│   ├── SUMMARY.md            # Status and feature checklist
│   ├── PARITY.md             # Feature parity vs Python v2.9.0
│   ├── ARCHITECTURE.md       # Class design and data flow
│   ├── SCRATCHPAD.md         # Active tasks and notes
│   ├── SBOM.md               # Dependencies and security
│   ├── CHANGELOG.md          # Version history
│   ├── REQUIREMENTS.md       # Feature requirements
│   └── My_Thoughts.md        # Design reasoning (AI context)
├── App.xaml                  # Application entry point
└── PixelPerfect.csproj       # .NET 8 project file
```

---

## Architecture

| Layer | Technology | Responsibility |
|-------|-----------|----------------|
| **Model** | `Core/*.cs` | Pixel data, layer state, tool logic |
| **ViewModel** | `MainViewModel` | App state, commands, bitmap rendering |
| **View** | `MainWindow.xaml` | Data binding, layout |
| **Code-behind** | `MainWindow.xaml.cs` | Mouse events → ViewModel calls |
| **Theme** | `DarkTheme.xaml` | Color tokens, button styles |

**Key design choices:**
- `PixelColor` is a `readonly struct` — zero heap allocation in render hot paths
- `Core/` has **no WPF/UI dependencies** — fully testable in isolation
- All zoom scaling is done via WPF `LayoutTransform` on the `Image` element — the bitmap stays at canvas resolution (32×32), WPF handles display scaling
- Tools expose a simple `ITool` interface — adding a new tool only requires implementing 3 methods
- See `DOCS/PARITY.md` for feature parity tracking vs Python v2.9.0

---

## Roadmap

### Phase 1 — Core Features
- [x] Undo/Redo (delta-based, 100 states)
- [ ] Canvas size presets (8×8 → 256×256)
- [ ] Selection tool + Move tool
- [ ] Color picker panel
- [x] PNG export

### Phase 2 — Advanced Features  
- [x] Shape tools (Line, Rectangle, Circle)
- [x] Keyboard shortcuts
- [ ] Grid overlay
- [ ] Animation timeline
- [ ] GIF/Sprite Sheet export

### Phase 3 — Polish & Parity
- [ ] JSON palette system (30+ palettes from Python version)
- [ ] Color Wheel (HSV)
- [ ] Tile preview mode
- [ ] Reference image panel
- [ ] Theme customization
- [ ] Multi-language support

---

## License

Copyright © 2024–2026 Diamond Clad Studios — All Rights Reserved
