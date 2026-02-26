# Pixel Perfect C# WPF — Changelog

All notable changes to the WPF rewrite will be documented here.  
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [0.2.0] — February 2026 — Parity Features

### Added (QoL batch — Feb 2026)
- **Undo/Redo toolbar buttons** — ↶ ↷ next to Save; CanExecute from UndoManager.StackChanged
- **Escape** — Cancel paste mode or clear selection (priority order)
- **Fullscreen (F11)** — KeyBinding toggles WindowState
- **Layer panel** — Delete (−), Duplicate (⊕), Move Up (⤴), Move Down (⤵) buttons
- **PNG export scale** — ComboBox 1×–8× in toolbar; default filename `Canvas WxH.png`
- **Status bar zoom %** — Coord display includes `| 1600%` when zoomed
- **UndoManager.StackChanged** — Event for command CanExecute refresh
- **PixelCanvas.ActiveLayerIndexChanged** — Event for layer command refresh

### Fixed
- **Grid overlay** — Grid no longer appears as a solid grey box at high zoom. Line thickness is now 1/Zoom in canvas space (`InverseZoomConverter`) so lines stay ~1 pixel on screen at any zoom level.
- **Grid button state** — Toolbar Grid control is now a `ToggleButton` with `IsChecked` bound to `ShowGrid` and `ToolToggleButton` style so it stays visually highlighted when grid is on. G key still toggles via command.

### Added
- **Theme System** — 6 themes with runtime switching: Dark (VS Code), Light, Nord, Dracula, Retro (phosphor amber), Catppuccin Mocha
- **ThemeService** — Static service for swapping theme ResourceDictionaries at runtime
- **Theme Selector** — Toolbar ComboBox to switch themes; uses DynamicResource for live updates
- **Canvas Size Presets** — New Canvas dialog with presets (8×8 through 256×256) and custom size (1–512)
- **Grid Overlay** — Toggle with G key and toolbar button; draws pixel boundaries
- **Color Picker Panel** — SNES Classic 16-color palette grid; click to select and switch to Brush
- **Pan Tool (P)** — Middle mouse, spacebar+drag, or Pan tool left-drag to pan the canvas view
- **Selection Tool (S)** — Rectangle selection with white border overlay
- **Move Tool (M)** — Non-destructive move with background preservation
- **Copy/Cut/Paste/Delete** — Ctrl+C, Ctrl+X, Ctrl+V, Delete/Backspace; paste mode with preview
- **SelectionManager** — Core class for selection state, clipboard, and move operations
- **NewCanvasDialog** — Modal dialog for canvas size selection
- **NegateConverter** — XAML converter for pan offset binding
- **Palette** — SNES Classic 16-color palette
- **Palette sections** — Optional `sections` in palette JSON (`title` + `colors` per section); UI shows sleek section titles above each group of swatches. All custom palettes now use sections: **Ores** (Iron & neutrals, Copper, Gold, Bronze, Silver, Coal), **Gems** (Ruby, Sapphire, Emerald, Amethyst, Topaz, Diamond, Jade, Lapis), **Minerals** (Quartz, Limestone, Sandstone, Granite, Obsidian, Slate), **Crystals** (Ice, Pink quartz, Frost, Blue, Cyan, Warm), **Cave** (Stone, Moss, Shadow, Underground, Rock, Moss stone, Deep), **Hair Colors** (Greys/Whites, Blondes, Light brown, Strawberry, Auburn, Dark brown, Blacks, Fantasy), **Skin Tones** (Cool, Neutral, Warm, Olive), **Grass** (Shade, Sun). Flat `colors`-only palettes still display as one "Colors" section.

### Changed
- **MainWindow** — DataContext set in code-behind to wire RequestNewCanvasSize callback
- **CreateCanvas** — Replaces hardcoded 32×32; auto-zoom for larger canvases

---

## [0.1.3] — February 2026 — Zero-Allocation Rendering & PNG Export

### Added
- **FileService** — New central static class to handle file I/O operations.
- **Save to PNG** — Bound the `SaveCommand` to a `SaveFileDialog`, forwarding to FileService to export the Active WPF canvas directly.
- **Save Toolbar & Shortcut** — Connected the toolbar 'Save' button. Added Ctrl+S shortcut wire-up in MainWindow input bindings.

### Optimized
- **Zero-Allocation Rendering Loop** — Eradicated the memory bottleneck on canvas frame rendering. Bypassed `new byte[]` allocations and 2D Array object creation (`PixelColor[,]`) on every `HandleMouseMove`. Built a direct byte-stream pipeline inside `PixelCanvas.FlattenToBuffer()`, slashing ms of GC hitching when scribbling on the canvas.

---

## [0.1.2] — February 2026 — Shape Tools

### Added
- **Line Tool (L)** — Complete Bresenham's line algorithm integration with real-time fluid preview.
- **Rectangle Tool (R)** — Outlined bounding box dragging with live zero-overhead preview.
- **Circle Tool (C)** — Midpoint circle algorithm integration with 8-way symmetry tracing and real-time preview tracking.
- **Preview System** — Introduced `SetPixelRaw` in the layer to bypass tracking and immediately apply temporary preview pixels which are auto-cleared on mouse move without polluting the UndoManager logic.

---

## [0.1.1] — February 2026 — Undo/Redo & Shortcuts

### Added
- **UndoManager** — Full delta-based undo/redo system with `PixelDelta` structs and `UndoTransaction` objects.
- **PixelChanged Event** — Layer pixel tracking that avoids recording redundant pixel overlaps within the same stroke.
- **Keyboard Shortcuts** — `B` (Brush), `E` (Eraser), `F` (Fill), `I` (Eyedropper), `Ctrl+Z` (Undo), `Ctrl+Y` (Redo), `Ctrl+N` (New).
- **Color Preview Binding** — Created `PixelColorToBrushConverter` to correctly map `PixelColor` to `SolidColorBrush` in the UI.
- **Active Layer Highlight** — Styled the layer ListBox using `ItemContainerStyle` to properly indicate the active selection.

---

## [0.1.0] — February 2026 — Initial Scaffold

### Added
- **Project Structure** — Clean MVVM folder layout: `Core/`, `ViewModels/`, `Views/`, `Themes/`
- **PixelColor** — `readonly struct` for RGBA color with packed `uint` conversion and equality operators
- **Layer** — Pixel storage class with name, visibility, opacity, lock, clone, and bounds-safe get/set
- **PixelCanvas** — Canvas manager with `ObservableCollection<Layer>`, layer add/remove/reorder, and alpha-composited `FlattenLayers()`
- **ITool interface** — Common `OnMouseDown/Move/Up(Layer, x, y, color)` contract for all tools
- **BrushTool** — Variable-size square brush (1px+), click and drag drawing
- **EraserTool** — Variable-size eraser (sets pixels to transparent)
- **FillTool** — Scanline-optimized flood fill
- **EyedropperTool** — Color picker that fires a `ColorPicked` event
- **ToolType enum** — Defines all current and planned tool slots
- **MainViewModel** — MVVM ViewModel with observable properties, `RelayCommand`-based tool selection, layer management, and `UpdateBitmap()` rendering pipeline
- **MainWindow.xaml** — 3-column layout: Left panel (tools + color), Center (canvas), Right (layers), top toolbar, status bar
- **MainWindow.xaml.cs** — Minimal code-behind for WPF mouse events with canvas coordinate conversion and mouse capture
- **DarkTheme.xaml** — VS Code-inspired dark theme with 8 color tokens and a custom `ToolButton` style
- **App.xaml** — Entry point with merged dark theme resource dictionary
- **PixelPerfect.csproj** — .NET 8 WPF project with `CommunityToolkit.Mvvm 8.2.2`
- **README.md** — Quick start, project structure, architecture summary, feature list, and roadmap
- **DOCS/ folder** — Full documentation suite (SUMMARY, ARCHITECTURE, SCRATCHPAD, SBOM, CHANGELOG, My_Thoughts, REQUIREMENTS)

### Architecture Highlights
- `PixelColor` is a value type (struct) — zero heap allocation in rendering hot path
- `Layer.SetPixel` respects the `IsLocked` flag
- `PixelCanvas.FlattenLayers()` implements standard alpha compositing bottom-to-top
- `WriteableBitmap` renders at canvas resolution, WPF `LayoutTransform` handles zoom scaling
- `NearestNeighbor` bitmap scaling preserves pixel art crispness
- Checkerboard transparency background uses `DrawingBrush` with `TileMode="Tile"` (no texture file needed)

### Known Limitations (v0.1.0)
- No file save/load
- No canvas resize/size presets
- Open/Save toolbar buttons have no commands bound

---

## Roadmap Entries (not yet released)

### [0.2.0] — Planned: Canvas & Color
- Canvas size presets dialog (8×8 → 64×64)
- PNG export scale options (1×–8×)
- Color picker panel (basic grid)
- .pixpf project save/load format

### [0.3.0] — Planned: Selection + Move
- Rectangle selection with marching ants
- Move tool (non-destructive, background preservation)
- Copy/Cut/Paste (Ctrl+C/X/V)

### [0.4.0] — Planned: Color Picker Full
- Color grid view (from loaded palettes)
- HSV color wheel
- Saved colors (32 slots)
- Recent colors (last 16)
- JSON palette loading (port palettes from Python version)

### [0.5.0] — Planned: Grid + Pan
- Grid overlay toggle (G key)
- Pan tool (middle mouse / spacebar hold)
- Zoom to cursor (Ctrl+wheel)

### [1.0.0] — Target: Feature Parity with Python v2.9.0
- See `DOCS/PARITY.md` for full parity tracker
- Selection, Move, Pan, Spray, Dither, Edge, Texture tools
- Animation timeline (basic)
- Theme system (multiple themes)
- Full keyboard shortcut coverage
