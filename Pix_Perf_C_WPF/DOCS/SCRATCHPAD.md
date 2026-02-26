# Pixel Perfect C# WPF — Development Scratchpad

**Last Updated**: February 25, 2026  
**Current Version**: 0.2.0
**Status**: Parity Features Complete (Phase 1)

---

## Doc updates (add at top)

- **2026-02-25 — Fruit & Veggies palette**: Added `assets/palettes/fruit_and_veggies.json` with 12 sections (Tomato, Orange, Lemon, Apple, Grape, Carrot, Lettuce, Broccoli, Corn, Eggplant, Pepper, Root). 96 colors for food pixel art.
- **2026-02-25 — Section titles for Hair, Skin, Grass**: Hair Colors (Greys/Whites, Blondes, Light brown, Strawberry, Auburn, Dark brown, Blacks, Fantasy), Skin Tones (Cool, Neutral, Warm, Olive), Grass (Shade, Sun) now use `sections` in JSON. All extended palettes now show titled tone groups.
- **2026-02-25 — Section titles for all custom palettes**: Gems (Ruby, Sapphire, Emerald, etc.), Minerals (Quartz, Limestone, Sandstone, Granite, Obsidian, Slate), Crystals (Ice, Pink quartz, Frost, Blue, Cyan, Warm), and Cave (Stone, Moss, Shadow, Underground, Rock, Moss stone, Deep) now use `sections` in JSON so the palette UI shows titled groups. Ores already had sections. Section title styling: TextPrimary, 12pt SemiBold, bottom border.
- **2026-02-25 — Palette section titles + styled tooltips**: Section titles use a thin bottom border and spacing. Palette swatches and tool buttons use structured tooltips: title (bold), short description, nitty gritty, in StyledToolTip (theme background, border, shadow). ColorSwatchToolTipConverter + ColorSwatchToolTipContent; tool resources for Brush, Eraser, Fill, etc.
- **2026-02-25 — Website update**: Added C# WPF port section to WEBPAGE with c-wpf-v-0.1.png screenshot. GitHub Actions workflow (`.github/workflows/deploy-pages.yml`) deploys WEBPAGE to GitHub Pages. Sleek background: animated gradient mesh + pixel grid overlay in styles.css.
- **2026-02-25 — Docs & repo cleanup**: README condensed — removed monetization section (moved to docs/MONETIZATION.md), kept last 5 versions in Latest Updates, replaced long version history with link to CHANGELOG. .gitignore updated with **/bin/ and **/obj/ for .NET build outputs. MONETIZATION.md added to docs index.
- **2026-02-25 — QoL batch**: Undo/Redo toolbar buttons (↶ ↷), Escape (cancel paste/deselect), Layer −/⊕/⤴/⤵, PNG export scale 1×–8×, status zoom %, F11 fullscreen, save default filename. FEATURE_BACKLOG 2–8, 10–11, 26 DONE.
- **2026-02-25 — Palette sections**: Palettes area now shows section titles when JSON uses optional `sections` array (`{"title":"Section Name","colors":[[r,g,b,a],...]}`). `PaletteLoader` has `PaletteSection` and `PaletteEntry.Sections`; flat `colors` palettes get one section "Colors". MainViewModel exposes `PaletteSections`; MainWindow uses ScrollViewer + per-section title (sleek 11pt SemiBold) + 8-column swatch grid. Ores palette converted to sections (Iron & neutrals, Copper, Gold, Bronze, Silver, Coal).
- **2026-02-25 — New palettes**: Minerals, Gems, Ores, Crystals, Cave added to `assets/palettes/`. Sequential ramps for stone, jewel tones, metallic ores, icy crystals, and cave/dungeon tones.
- **2026-02-25 — Palette selector**: Added ComboBox to switch between palettes. `PaletteLoader.LoadAll()` provides SNES Classic + all JSON files from `assets/palettes/*.json` (curse_of_aros, definya, hair_colors, heartwood_online, kakele_online, old_school_runescape, rucoy_online, skin_tones, grass, etc.). MainViewModel: `AvailablePalettes`, `SelectedPalette`, `PaletteColors` now returns selected palette's colors.
- **2026-02-25 — Grid overlay & button fix**: Grid was rendering as a solid grey box because line `StrokeThickness="1"` was in canvas space; at 16× zoom each line became 16px wide and overlapped. Fixed by adding `InverseZoomConverter` so grid line thickness is 1/Zoom in canvas space (~1px on screen). Grid toolbar control changed from `Button` to `ToggleButton` with `ToolToggleButton` style and `IsChecked="{Binding ShowGrid, Mode=TwoWay}"` so the button stays lit when grid is on. G key still toggles via `ToggleGridCommand`; `OnShowGridChanged` calls `RefreshGridOverlay()` so both UI and keyboard stay in sync.

---

## Active Tasks

### Completed (v0.2.0)
- [x] Canvas size presets (New Canvas dialog, 8×8–256×256, custom)
- [x] Grid overlay toggle (G key)
- [x] Color picker panel (SNES Classic 16-color palette)
- [x] Pan tool (middle mouse, spacebar, P key)
- [x] Selection tool (rectangle select, Copy/Cut/Paste/Delete)
- [x] Move tool (non-destructive, background preservation)

### Completed (theme system)
- [x] 6 themes: Dark, Light, Nord, Dracula, Retro, Catppuccin
- [x] ThemeService + runtime switching via toolbar ComboBox

### Backlog
- [ ] Color Wheel (HSV picker)
- [ ] Recent Colors
- [ ] Animation timeline

---

## Blocked Items
- None

---

## Recent Context (last 5 actions)
1. 2026-02-25: Palette sections — section titles in palettes area (PaletteSection, PaletteSections binding, ores.json sections)
2. 2026-02-25: Grid overlay fix — InverseZoomConverter for 1px grid lines at any zoom; Grid button → ToggleButton with ShowGrid binding so it stays lit when on
3. 2026-02-25: Implemented full parity plan — Canvas presets, Grid, Color picker, Pan, Selection, Move, Copy/Paste shortcuts
4. 2026-02-25: Documentation run — created PARITY.md, updated SUMMARY/ARCHITECTURE/README/CHANGELOG/REQUIREMENTS for accurate parity tracking
5. 2026-02-23: Initial documentation audit and creation for WPF project

---

## Known Issues
- **~~Color preview~~** ~~binding in XAML uses `<MultiBinding Converter="{x:Null}">` — needs a proper `IValueConverter` to display the current `PixelColor` as a `SolidColorBrush`~~ (Fixed)
- **~~Open/Save buttons~~** ~~in toolbar are not wired up (no commands bound)~~ (Fixed - Save bound to PNG export)
- **Quick Colors** grid is empty (placeholder section)
- **~~No keyboard shortcuts~~** ~~— all tool switching requires clicking buttons~~ (Fixed)
- **~~Layer ListBox~~** ~~doesn't visually indicate the active layer (no highlight styling)~~ (Fixed)

---

## Technical Debt
- ~~`MainWindow.xaml` color preview section needs a `PixelColorToBrushConverter`~~ (Fixed)
- ~~`UpdateBitmap()` rebuilds the entire pixel buffer every frame — could optimize with dirty region tracking later~~ (Fixed - zero-allocation pipeline)
- Tools don't have a way to influence the ViewModel directly (e.g., Eyedropper uses an event, but future tools may need richer communication)

---

## Design Notes
- The Python version's `main_window.py` grew to 3,387 lines before refactoring into 12 manager classes. The C# version should avoid this by keeping the ViewModel focused and extracting services/managers early.
- WPF's data binding eliminates most of the manual UI update code that plagued the Python version
- Consider using `ICommand` implementations for undo/redo rather than a separate manager class

---

## Compacted History
- v0.1.0: Initial scaffold — 4 tools, layer system, dark theme, MVVM architecture, WriteableBitmap rendering
- v0.1.1: Undo/Redo tracking system, keyboard shortcuts, active layer UI styling
- v0.1.2: Shape tools (Line, Rectangle, Circle) with preview rendering via `SetPixelRaw`
- v0.1.3: Zero-allocation rendering (`FlattenToBuffer`), PNG export (`SaveCommand` via `FileService`)
