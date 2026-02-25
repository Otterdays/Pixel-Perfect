# Pixel Perfect C# WPF — Requirements

**Version**: 0.1.3  
**Last Updated**: February 25, 2026  
**Status**: Phase 1 Features In Progress

This document tracks feature requirements for the WPF rewrite, cross-referenced against the Python version's implementation status.

---

## Overview

The C# WPF version's goal is full feature parity with Python v2.9.0 over multiple phases, while improving architecture, performance, and Windows integration. The Python version is the source of truth for UX decisions.

---

## FR1: Canvas System

### FR1.1 Canvas Initialization
- **Status**: ✅ Implemented (32×32 default)
- Default canvas: 32×32 pixels, 1 layer, dark theme
- Support preset sizes: 8×8, 16×16, 32×32, 16×32, 32×64, 64×64, 128×128, 256×256
- Custom size dialog (any size up to 512×512)
- Auto-zoom for large presets (e.g., 128×128 → 4x, 256×256 → 2x)

### FR1.2 Layer System  
- **Status**: ✅ Implemented (basic)
- Add/Remove layers (always keep at least 1)
- Visibility toggle (checkbox per layer)
- Opacity control (0.0–1.0)
- Lock layer (prevent drawing)
- Reorder layers (move up/down)
- Clone/duplicate layer
- Active layer visual indicator (highlight in panel)
- Alpha compositing when flattening

### FR1.3 Zoom  
- **Status**: ✅ Implemented (1x–64x dropdown)
- Zoom levels: 1, 2, 4, 8, 16, 24, 32, 48, 64
- Scroll wheel zoom (zoom to cursor)
- Fit canvas to viewport button
- 100% zoom reset button
- Zoom synced between dropdown, wheel, and scrollbar

### FR1.4 Grid Overlay  
- **Status**: 🔲 Planned
- Toggle grid with G key and toolbar button
- Grid scales with zoom
- Grid line color options (auto/dark/light/paper)
- Grid overlay mode (lines on top of pixels)

### FR1.5 Pan  
- **Status**: 🔲 Planned
- Middle mouse button drag to pan
- Spacebar + drag pan
- Right-click drag pan (with 5px threshold before pan activates)

---

## FR2: Drawing Tools

### FR2.1 Brush Tool  
- **Status**: ✅ Implemented (basic)
- Single pixel (1×1) by default
- Variable size: 1×1, 2×2, 3×3 (and larger)
- Right-click menu for size selection
- Square and circular brush shapes (planned)
- Drawing respects active layer lock

### FR2.2 Eraser Tool  
- **Status**: ✅ Implemented (basic)
- Writes `Transparent` pixels
- Same size system as brush
- Right-click edge line deletion (erases edge lines, from Python v2.7.3)

### FR2.3 Fill Tool  
- **Status**: ✅ Implemented (scanline optimized)
- Scanline flood fill (horizontal span optimization)
- Fills contiguous region of same color
- Respects canvas bounds

### FR2.4 Eyedropper Tool  
- **Status**: ✅ Implemented
- Samples color from active layer on click
- Fires `ColorPicked` event → updates CurrentColor

### FR2.5 Selection Tool  
- **Status**: 🔲 Planned
- Rectangle selection with marching ants visualization
- Copy (Ctrl+C), Cut (Ctrl+X), Paste (Ctrl+V)
- Delete selection (Delete key)
- Mirror horizontal/vertical
- Rotate 90°
- Scale selection

### FR2.6 Move Tool  
- **Status**: 🔲 Planned
- Move selected pixels
- Non-destructive: saves background pixels on first pickup
- Restore background on subsequent adjustments
- Visual preview follows cursor during drag

### FR2.7 Shape Tools  
- **Status**: ✅ Implemented
- Line tool (Bresenham's algorithm)
- Rectangle tool (outlined/filled)
- Circle tool (midpoint algorithm)
- Features zero-overhead preview during drag via `SetPixelRaw`

### FR2.8 Dither Tool  
- **Status**: 🔲 Planned (Python v2.7.1)
- Checkerboard `(x+y)%2` pattern
- Left-click to draw, right-click to erase

### FR2.9 Spray Tool  
- **Status**: 🔲 Planned (Python v2.6.0)
- Continuous droplet spray while button held
- Configurable radius and density

### FR2.10 Edge Tool  
- **Status**: 🔲 Planned (Python v2.5.0)
- Draw lines on pixel boundaries (not inside pixels)
- Variable thickness
- Survives canvas redraws

---

## FR3: Color Management

### FR3.1 Color Preview  
- **Status**: ✅ Implemented
- Large color swatch showing current color
- Updates immediately on color change (via `PixelColorToBrushConverter`)

### FR3.2 Palette Grid View  
- **Status**: 🔲 Planned
- JSON palette loading from `assets/palettes/*.json`
- Auto-discover all palette files on startup
- Support 8–32 color palettes

### FR3.3 Color Wheel  
- **Status**: 🔲 Planned
- HSV rainbow wheel for color selection
- Clicking ring sets hue; center saturation/value (or slider)
- Sync back to brush color

### FR3.4 Saved Colors  
- **Status**: 🔲 Planned
- 24–32 persistent color slots
- Save current color to slot
- Persist to `AppData\Local\PixelPerfect\`

### FR3.5 Recent Colors  
- **Status**: 🔲 Planned (Python v2.7.0)
- Automatically tracks last 16 colors used while drawing
- Persistent across sessions

### FR3.6 Custom Colors  
- **Status**: 🔲 Planned
- 32 user-defined persistent colors
- Hex input, RGB sliders, or color dialog

---

## FR4: Export / File Operations

### FR4.1 PNG Export  
- **Status**: ✅ Implemented
- Export current frame as PNG via SaveCommand → FileService.ExportToPng()
- Scale: 1× complete (UI for 2×–8× planned)
- Transparency support (RGBA PNG)

### FR4.2 GIF Export  
- **Status**: 🔲 Planned
- Animated GIF from all frames
- Configurable FPS, loop count, scale

### FR4.3 Sprite Sheet Export  
- **Status**: 🔲 Planned
- Horizontal, vertical, or grid layout
- JSON metadata with frame info
- Godot-ready export (zero spacing, .tres/.tscn files)

### FR4.4 Save/Load Project  
- **Status**: 🔲 Planned
- Custom `.pixpf` file format (JSON or binary)
- Stores: canvas size, all layers, all frames, color history, theme preference

### FR4.5 Quick Export  
- **Status**: 🔲 Planned
- Ctrl+Shift+E re-exports with last-used settings

---

## FR5: Animation System

### FR5.1 Timeline  
- **Status**: 🔲 Planned
- Frame-based animation (add/duplicate/delete/reorder frames)
- Thumbnails per frame
- Navigation: previous/next frame

### FR5.2 Playback  
- **Status**: 🔲 Planned
- Play/Pause/Stop controls
- Configurable FPS (1–60)
- Loop mode

### FR5.3 Onion Skinning  
- **Status**: 🔲 Planned
- Show ghost of previous/next frames
- Configurable opacity

---

## FR6: Undo/Redo

### FR6.1 Undo Manager  
- **Status**: ✅ Implemented
- Delta-based: store only changed pixels per transaction stroke
- Tracks `OldColor` and `NewColor` automatically via `PixelChanged` layer event
- Ctrl+Z / Ctrl+Y shortcuts wired via `InputBindings`

---

## FR7: User Interface

### FR7.1 Keyboard Shortcuts  
- **Status**: ✅ Implemented (partial)
- B — Brush, E — Eraser, F — Fill, I — Eyedropper, L — Line, R — Rectangle, C — Circle, Ctrl+N — New
- Ctrl+Z — Undo, Ctrl+Y — Redo, Ctrl+S — Save
- Planned: G — Toggle grid, F11 — Fullscreen

### FR7.2 Theme System  
- **Status**: ✅ Implemented (dark only)
- Dark theme (VS Code-style) — implemented
- Light theme — planned
- Theme customization (custom colors) — planned far future

### FR7.3 Status Bar  
- **Status**: ✅ Implemented
- Shows current cursor coordinates (x, y)
- Shows tool messages (e.g. "New canvas created")

### FR7.4 Mini Preview  
- **Status**: 🔲 Planned (Python v2.9.0)
- Bottom-right overlay showing full canvas
- Viewport indicator shows visible area when zoomed in
- Toggle with Shift+P

### FR7.5 Reference Image Panel  
- **Status**: 🔲 Planned (Python v2.9.0)
- Load any image as reference
- Opacity slider
- Pan/zoom within panel
- Toggle with Shift+R

### FR7.6 Tile Preview  
- **Status**: 🔲 Planned (Python v2.7.5)
- 3×3 repeating canvas for pattern/texture preview
- Ghost tiles at 50% opacity

---

## Non-Functional Requirements

### NFR1: Performance
- < 16ms render update per draw operation (60fps target)
- No UI freezes during fill operations on 256×256 canvas
- Startup < 2 seconds

### NFR2: Compatibility
- **Primary**: Windows 10 / Windows 11
- **Runtime**: .NET 8.0 (self-contained publish option)
- **Display**: 1280×720 minimum, 1920×1080 recommended

### NFR3: Architecture
- MVVM pattern throughout
- `Core/` has zero UI dependencies
- Each major feature area gets a UserControl, not inline XAML in MainWindow
- ViewModel files < 400 lines (extract to services when needed)

### NFR4: Code Quality
- Nullable reference types enabled
- XML doc comments on all public API in `Core/`
- No empty catch blocks
- `using` declarations over `using` blocks where it reduces nesting
