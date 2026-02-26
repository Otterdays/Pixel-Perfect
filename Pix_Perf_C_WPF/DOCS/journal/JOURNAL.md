# Pixel Perfect C# WPF — Development Journal

Dated log of changes, fixes, and notable work. New entries at top.

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
