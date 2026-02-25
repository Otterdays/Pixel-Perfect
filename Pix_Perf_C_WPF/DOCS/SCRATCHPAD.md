# Pixel Perfect C# WPF — Development Scratchpad

**Last Updated**: February 25, 2026  
**Current Version**: 0.2.0
**Status**: Parity Features Complete (Phase 1)

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
1. 2026-02-25: Implemented full parity plan — Canvas presets, Grid, Color picker, Pan, Selection, Move, Copy/Paste shortcuts
2. 2026-02-25: Documentation run — created PARITY.md, updated SUMMARY/ARCHITECTURE/README/CHANGELOG/REQUIREMENTS for accurate parity tracking
2. 2026-02-23: Initial documentation audit and creation for WPF project
3. (Project created with scaffold — exact date unknown)

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
