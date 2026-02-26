# Pixel Perfect — Feature Parity Tracker

**Purpose**: Track C# WPF port progress toward full parity with Python v2.9.0.  
**Last Updated**: February 25, 2026  
**WPF Version**: 0.2.0  
**Python Reference**: 2.9.0

---

## Doc updates (add at top)

- **2026-02-25**: Palette section titles applied to all custom palettes (Gems, Minerals, Ores, Crystals, Cave, Hair Colors, Skin Tones, Grass, Fruit & Veggies). Assets/palettes included in build and publish output.
- **2026-02-25**: Grid overlay — Fixed grey-box bug (grid lines use 1/Zoom thickness via `InverseZoomConverter`). Grid toolbar button is a ToggleButton bound to `ShowGrid` and stays lit when on.

---

## Parity Overview

| Category | Python v2.9.0 | WPF v0.2.0 | Parity % |
|----------|---------------|------------|----------|
| Drawing Tools | 14 | 10 | 71% |
| Canvas System | Full | Basic | ~55% |
| Color Management | 5 views + 30+ palettes | Basic grid | ~25% |
| Layer System | Full | Basic | ~70% |
| Export/File | PNG/GIF/Sheet/.pixpf | PNG only | ~25% |
| Undo/Redo | Delta-based | Delta-based | 100% |
| Animation | Timeline + onion | None | 0% |
| UI/UX | Themes, panels, shortcuts | Dark theme, shortcuts | ~50% |

**Overall Parity**: ~55% (Selection, Move, Pan, Color Picker, Canvas presets, Grid implemented)

---

## Drawing Tools

| Tool | Python | WPF | Notes |
|------|--------|-----|------|
| Brush | ✅ | ✅ | WPF: variable size (1px+), click+drag |
| Eraser | ✅ | ✅ | WPF: variable size, sets transparent |
| Fill | ✅ | ✅ | Both: scanline-optimized flood fill |
| Eyedropper | ✅ | ✅ | WPF: ColorPicked event → CurrentColor |
| Line | ✅ | ✅ | Both: Bresenham, live preview |
| Rectangle | ✅ | ✅ | Both: outline/fill, live preview |
| Circle | ✅ | ✅ | Both: midpoint algorithm, live preview |
| Selection | ✅ | 🔲 | Rectangle select, marching ants, clipboard |
| Move | ✅ | 🔲 | Non-destructive, background preservation |
| Pan | ✅ | 🔲 | Middle mouse, spacebar, right-click drag |
| Spray | ✅ | 🔲 | Radius/density, continuous droplets |
| Dither | ✅ | 🔲 | Checkerboard (x+y)%2 pattern |
| Edge | ✅ | 🔲 | Sub-pixel boundaries, variable thickness |
| Texture | ✅ | 🔲 | Pattern stamping, texture library |

---

## Canvas System

| Feature | Python | WPF | Notes |
|---------|--------|-----|------|
| Preset sizes | 8×8→256×256 | ✅ | New Canvas dialog: 8×8 through 256×256 |
| Custom size | 1×512 dialog | ✅ | Custom option in New Canvas dialog |
| Zoom | 0.25×–64× | 1×–64× | WPF: dropdown, NearestNeighbor |
| Zoom to cursor | Ctrl+wheel | ✅ | ZoomAtCursor adjusts pan so point under cursor stays put |
| Fit/100% buttons | ✅ | 🔲 | |
| Grid overlay | ✅ | ✅ | G key, toolbar; vector overlay, zoom-invariant 1px lines; toggle button stays lit when on |
| Tile preview | 3×3 ghost | 🔲 | |
| Checkerboard BG | ✅ | ✅ | WPF: XAML DrawingBrush |
| Pan | Middle+Space+R | ✅ | Middle mouse, spacebar, Pan tool |

---

## Layer System

| Feature | Python | WPF | Notes |
|---------|--------|-----|------|
| Add/Remove | ✅ | ✅ | WPF: + − buttons; always keep ≥1 |
| Visibility toggle | ✅ | ✅ | WPF: checkbox per layer |
| Opacity | ✅ | ✅ | WPF: 0.0–1.0 |
| Lock | ✅ | ✅ | WPF: IsLocked |
| Reorder | ✅ | ✅ | WPF: ⤴ ⤵ buttons; MoveLayerUp/Down |
| Active highlight | ✅ | ✅ | WPF: ItemContainerStyle |
| Alpha compositing | ✅ | ✅ | Both: bottom-to-top blend |
| Clone | ✅ | ✅ | WPF: ⊕ Duplicate layer button |
| Layer naming | ✅ | ✅ | WPF: default "Layer N" |

---

## Color Management

| Feature | Python | WPF | Notes |
|---------|--------|-----|------|
| Current color preview | ✅ | ✅ | WPF: PixelColorToBrushConverter |
| Grid view | 4-col palette | ✅ | ComboBox to switch palettes; SNES Classic + assets/palettes/*.json |
| Primary + variations | 8 mains + 24 var | 🔲 | |
| Color Wheel | HSV picker | 🔲 | |
| Constants | Used colors only | 🔲 | |
| Saved Colors | 24 slots | 🔲 | |
| Recent Colors | Last 16 | ✅ | 8 slots; from palette + eyedropper |
| JSON palettes | 30+ palettes | ✅ | 16 palettes: SNES, Gems, Minerals, Ores, Crystals, Cave, Hair, Skin, Grass, Fruit & Veggies, game palettes; sectioned UI; assets copied to build output |
| Custom colors | 32 user | 🔲 | |

---

## Export & File Operations

| Feature | Python | WPF | Notes |
|---------|--------|-----|------|
| PNG export | 1×–8× scale | ✅ | Export scale dropdown (1×–8×); default filename Canvas WxH.png |
| GIF export | Animated | 🔲 | |
| Sprite sheet | H/V/Grid + JSON | 🔲 | |
| Godot export | .tres/.tscn | 🔲 | |
| Save (.pixpf) | Custom format | 🔲 | |
| Load (.pixpf) | Full project | 🔲 | |
| Import PNG | Auto-scale | 🔲 | |
| Quick export | Ctrl+Shift+E | ✅ | Exports to Desktop with current scale |

---

## Undo/Redo

| Feature | Python | WPF | Notes |
|---------|--------|-----|------|
| Delta-based | ✅ | ✅ | Both: pixel-level tracking |
| Transaction grouping | ✅ | ✅ | WPF: BeginTransaction/EndTransaction |
| Ctrl+Z / Ctrl+Y | ✅ | ✅ | WPF: InputBindings |
| History limit | 50+ | 100 | WPF: configurable |

---

## Animation

| Feature | Python | WPF | Notes |
|---------|--------|-----|------|
| Timeline | 4–8 frames | 🔲 | |
| Playback | Play/Pause/Stop | 🔲 | |
| FPS control | 1–60 | 🔲 | |
| Frame thumbnails | ✅ | 🔲 | |
| Onion skinning | Prev/next ghost | 🔲 | |
| Add/duplicate/delete | ✅ | 🔲 | |

---

## UI & UX

| Feature | Python | WPF | Notes |
|---------|--------|-----|------|
| Dark theme | ✅ | ✅ | WPF: VS Code-inspired |
| Light theme | ✅ | ✅ | Clean professional light |
| Theme customization | ✅ | 🔲 | |
| Multiple themes | 5 | 6 | WPF: Dark, Light, Nord, Gruvbox, Catppuccin, Retro |
| Grid overlay toggle | G | 🔲 | |
| Status bar | ✅ | ✅ | WPF: coords + messages |
| Keyboard shortcuts | Full | Partial | WPF: B/E/F/I/L/R/C, Ctrl+Z/Y/S/N |
| Collapsible panels | ✅ | 🔲 | |
| Mini preview | Shift+P | 🔲 | |
| Reference panel | Shift+R | 🔲 | |
| 3D token preview | Shift+T | 🔲 | |
| Fullscreen | F11 | ✅ | KeyBinding F11 → ToggleFullscreenCommand |
| Right-click context | ✅ | 🔲 | |
| Copy/Paste shortcuts | Ctrl+C/V/X | ✅ | Copy, Cut, Paste, Delete, Escape (cancel/deselect) |

---

## Recommended Next Steps (Priority Order)

1. **Save/Load .pixpf** — Project persistence
2. **Animation Timeline** — Frame management, playback
3. **Spray Tool** — Radius/density, continuous droplets
4. **Dither Tool** — Checkerboard pattern
5. **Color Wheel** — HSV picker
6. ~~**JSON Palette Loading**~~ — DONE: 16 palettes (SNES, Gems, Minerals, Ores, Crystals, Cave, Hair, Skin, Grass, Fruit & Veggies, game palettes) from assets/palettes

---

## Document Maintenance

- Update this doc when implementing features or when Python version changes
- Add dated notes when parity status changes
- Keep "Recommended Next Steps" aligned with SCRATCHPAD active tasks
