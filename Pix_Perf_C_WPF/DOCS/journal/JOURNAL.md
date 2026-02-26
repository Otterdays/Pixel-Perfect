# Pixel Perfect C# WPF — Development Journal

Dated log of changes, fixes, and notable work. New entries at top.

---

## 2026-02-25 — Settings panel: grid, checkerboard, undo limit

**What**
- Added Settings dialog (⚙ toolbar button) with configurable grid color, checkerboard colors, and undo history limit.

**Features**
- **Grid color** — Presets: Dark (#404040), Light (#808080), Contrast (#202020). Bound to grid overlay Stroke.
- **Checkerboard** — Presets for both colors. Dark: #404040/#505050. Light: #c0c0c0/#d0d0d0. Contrast: #303030/#606060.
- **Undo limit** — ComboBox: 50, 100, 200, 500. UndoManager.MaxHistoryLimit trims stack on EndTransaction.

**Files**
- MainViewModel.cs (GridColor, CheckerboardColor1/2, UndoHistoryLimit, brushes)
- UndoManager.cs (MaxHistoryLimit, List for undo stack to support trim)
- SettingsDialog.xaml, SettingsDialog.xaml.cs
- MainWindow.xaml (CheckerboardBrush, GridColorBrush bindings; ⚙ button)

---

## 2026-02-25 — QoL batch 2: Recent Colors, Swap, Zoom-to-cursor, Fit, Quick Export

**What**
- Implemented 7 QoL features for faster pixel art workflow.

**Features**
- **Recent Colors** — 8 slots, populated when picking from palette or eyedropper. Click to select.
- **Swap colors (X)** — Primary + secondary color swatches. X key or click secondary to swap. Secondary updated when picking.
- **[ ] brush size** — Bracket keys to adjust brush/eraser size (1–32).
- **Zoom to cursor** — Ctrl+wheel zooms centered on cursor; pan adjusts so point under cursor stays put.
- **Fit / 100%** — Toolbar buttons; Fit uses GetCanvasAreaSize to compute zoom.
- **Status bar** — Shows tool name + hotkey when switching (e.g. "Brush (B)").
- **Quick Export (Ctrl+Shift+E)** — Exports to Desktop with current scale, no dialog.

**Files**
- MainViewModel.cs (RecentColors, SecondaryColor, SwapColors, BrushSizeUp/Down, ZoomAtCursor, FitToView, Zoom100, QuickExport, OnCurrentToolChanged)
- MainWindow.xaml (Recent Colors UI, secondary swatch, Fit/100% buttons, key bindings, PreviewMouseWheel)
- MainWindow.xaml.cs (ZoomAtCursor with cursor position)

---

## 2026-02-25 — Fruit & Veggies palette + assets build verification + website

**What**
- Added Fruit & Veggies palette; verified all palettes are included in C# WPF build and publish; updated website palette list.

**Fruit & Veggies**
- `assets/palettes/fruit_and_veggies.json` — 12 sections (Tomato, Orange, Lemon, Apple, Grape, Carrot, Lettuce, Broccoli, Corn, Eggplant, Pepper, Root), 96 colors.

**Assets in build**
- csproj: `Content Include="..\assets\palettes\*.json"` with `CopyToOutputDirectory=PreserveNewest`. Verified: all 16 palettes copy to bin/Debug, bin/Release, and publish output. PaletteLoader reads from exe dir + `assets/palettes/`.

**Website**
- index.html: Features section lists Hair Colors, Skin Tones, Gems, Minerals, Ores, Crystals, Cave, Grass, Fruit & Veggies. C# WPF card mentions "sectioned palettes (Gems, Minerals, Hair, Skin, etc.)".

**Docs**
- SCRATCHPAD, CHANGELOG, PARITY, SUMMARY, JOURNAL updated.

---

## 2026-02-25 — Section titles for Hair, Skin, Grass

**What**
- Added sections to Hair Colors (Extended), Skin Tones (Extended), and Grass palettes so they show titled groups like Gems and Minerals.

**Sections**
- **Hair Colors**: Greys/Whites, Blondes, Light brown, Strawberry, Auburn, Dark brown, Blacks, Fantasy (8 sections, 90 colors).
- **Skin Tones**: Cool, Neutral, Warm, Olive (4 sections, 88 colors).
- **Grass**: Shade, Sun (2 sections, 16 colors).

**Files**
- `assets/palettes/hair_colors.json`, `skin_tones.json`, `grass.json`.

---

## 2026-02-25 — Section titles for all palettes + docs

**What**
- Applied sectioned structure to every custom palette so the palette area shows titled groups (same behavior as Gems and Ores) for Minerals, Crystals, and Cave. Confirmed docs reflect the change.

**Palette sections**
- **Gems** (already done): Ruby, Sapphire, Emerald, Amethyst, Topaz, Diamond, Jade, Lapis.
- **Minerals**: Quartz, Limestone, Sandstone, Granite, Obsidian, Slate (6×8 colors).
- **Crystals**: Ice, Pink quartz, Frost, Blue, Cyan, Warm (6×8 colors).
- **Cave**: Stone, Moss, Shadow, Underground, Rock, Moss stone, Deep (7×8 colors).
- **Ores**: Already had sections (Iron & neutrals, Copper, Gold, Bronze, Silver, Coal).

**Docs**
- SCRATCHPAD: Note that all custom palettes use sections; section title styling (TextPrimary, 12pt).
- CHANGELOG: Palette sections bullet updated to list all five palettes with their section names.
- PARITY: Doc update line for palette section titles applied to all custom palettes.
- JOURNAL: This entry.

**Files**
- `assets/palettes/minerals.json`, `crystals.json`, `cave.json` (converted from flat `colors` to `sections`).
- DOCS: SCRATCHPAD.md, CHANGELOG.md, PARITY.md, journal/JOURNAL.md.

---

## 2026-02-25 — QoL batch: Undo/Redo, Escape, Layers, Export, Fullscreen

**What**
- Implemented 10+ checklist items from FEATURE_BACKLOG: Undo/Redo toolbar buttons, Escape (cancel paste/deselect), Layer Delete/Duplicate/Reorder, PNG export scale, status zoom %, fullscreen F11, save default filename.

**Changes**
- **Toolbar**: Undo (↶), Redo (↷) with CanExecute; Export scale ComboBox (1×–8×)
- **InputBindings**: Escape → EscapeCommand; F11 → ToggleFullscreenCommand
- **EscapeCommand**: If paste mode → cancel; else if selection → deselect
- **Layers panel**: − (delete), ⊕ (duplicate), ⤴ (up), ⤵ (down) buttons; RemoveLayerCommand, DuplicateLayerCommand, MoveLayerUpCommand, MoveLayerDownCommand with CanExecute
- **Save**: Default FileName = Canvas WxH.png; ExportScale passed to FileService
- **StatusText**: Coord display includes `| {Zoom*100}%`
- **UndoManager**: StackChanged event; PixelCanvas.ActiveLayerIndexChanged event

**Files**
- MainWindow.xaml, MainViewModel.cs, UndoManager.cs, PixelCanvas.cs

---

## 2026-02-25 — New palettes: Minerals, Gems, Ores, Crystals, Cave

**What**
- Added 5 new JSON palettes to `assets/palettes/` for mineral, gem, ore, crystal, and cave pixel art.

**Palettes**
- **Minerals** (48 colors): Stone grays, quartz whites, limestone beige, granite, sandstone, obsidian.
- **Gems** (64 colors): Ruby, sapphire, emerald, amethyst, topaz, diamond, jade, lapis ramps.
- **Ores** (56 colors): Silver/iron grays, copper rust/brown, gold ramps, coal black, bronze.
- **Crystals** (48 colors): Icy, prismatic, translucent tones for frost and crystal effects.
- **Cave** (56 colors): Dark dungeon stone, shadow, moss, underground atmosphere.

**Files**
- `assets/palettes/minerals.json`
- `assets/palettes/gems.json`
- `assets/palettes/ores.json`
- `assets/palettes/crystals.json`
- `assets/palettes/cave.json`

---

## 2026-02-25 — Palette selector (custom palettes)

**What**
- User could not switch to custom palettes; only SNES Classic was shown.

**Cause**
- `PaletteColors` was hardcoded to `Palette.SnesClassic`. `PaletteLoader` existed and loads JSON from `assets/palettes/*.json`, but was never wired to the UI.

**Changes**
- **MainViewModel**: Added `AvailablePalettes` (from `PaletteLoader.LoadAll()`), `SelectedPalette` (PaletteEntry), `PaletteColors` now returns `SelectedPalette?.Colors ?? Palette.SnesClassic`. `[NotifyPropertyChangedFor(nameof(PaletteColors))]` on SelectedPalette so the grid updates when palette changes.
- **MainWindow.xaml**: Added ComboBox above the palette color grid, bound to `AvailablePalettes` / `SelectedPalette`, `DisplayMemberPath="Name"`.
- **PaletteLoader** and `assets/palettes/*.json` were already in place; csproj copies them to output.

**Files**
- `ViewModels/MainViewModel.cs`
- `Views/MainWindow.xaml`
- `DOCS/PARITY.md` (Color Management: Grid view, JSON palettes)

---

## 2026-02-25 — Grid overlay fix & button state

**What**
- Grid overlay was rendering as a solid grey box at zoom (e.g. 16×) instead of visible lines.
- Grid toolbar button did not stay visually “on” when grid was enabled.

**Cause**
- Grid lines use WPF `Line` elements in canvas space; the whole canvas is scaled by `Zoom`. With `StrokeThickness="1"` in canvas units, each line became Zoom pixels wide (e.g. 16px), so lines overlapped and looked like one grey block.
- Grid control was a plain `Button`, so it had no checked state to reflect `ShowGrid`.

**Changes**
- **InverseZoomConverter** added: converts `Zoom` (int) to `1.0 / Zoom` for grid line `StrokeThickness`. Lines stay ~1 pixel on screen at any zoom.
- **Grid button** replaced with `ToggleButton`, style `ToolToggleButton`, `IsChecked="{Binding ShowGrid, Mode=TwoWay}"`. No command on the button (click updates via binding); G key still uses `ToggleGridCommand`.
- **OnShowGridChanged** in MainViewModel calls `RefreshGridOverlay()` so toggling via button or command keeps overlay in sync.

**Files**
- `Converters/InverseZoomConverter.cs` (new)
- `Views/MainWindow.xaml` (converter resource, grid Line StrokeThickness binding, Grid → ToggleButton)
- `ViewModels/MainViewModel.cs` (OnShowGridChanged)

**Docs updated**
- SCRATCHPAD, CHANGELOG, PARITY (see those files for summary).

---
