# Pixel Perfect C# WPF — Feature Backlog

**Purpose**: Prioritized list of easy/medium QoL features for the C# WPF port.  
**Last Updated**: February 25, 2026  
**Reference**: Python v2.9.0, PARITY.md

**Completed**: Symmetry UI (Sym X, Sym Y ToggleButtons in MainWindow.xaml) — Feb 2026  
**Completed (Sprint 3 — Feb 2026)**: Items 21–28 — Window title, status tool, save default filename, Clear layer, layer opacity/lock UI, crosshair cursor, hex tooltip  
**Completed (QoL — Feb 2026)**: Recent Colors (17), Copy/Cut/Paste/Delete CanExecute, New Canvas confirm when dirty, Brush/Eraser size slider (1–32)

---

## Quick Reference: 10+ Easy/Medium Features

| # | Feature | Effort | Category | Notes |
|---|---------|--------|----------|-------|
| 1 | Symmetry X/Y Toggle UI | DONE | Tools | Sym X, Sym Y ToggleButtons in MainWindow.xaml (lines 121–157) |
| 2 | Undo/Redo Toolbar Buttons | Easy | UI | Shortcuts exist; add visible buttons next to Save |
| 3 | PNG Export Scale Dropdown | Easy | Export | 1×, 2×, 4×, 8× — FileService already supports scale |
| 4 | Escape to Cancel Paste | Easy | UX | KeyBinding when `_isPasteMode` |
| 5 | Escape to Deselect | Easy | Selection | Clear selection when Escape pressed |
| 6 | Layer Delete Button | Easy | Layers | PixelCanvas.RemoveLayer exists — add "-" button |
| 7 | Layer Duplicate | Easy | Layers | Clone active layer, insert above |
| 8 | Layer Reorder (Up/Down) | Easy | Layers | MoveLayerUp/Down exist — add ↑↓ buttons per layer |
| 9 | Eyedropper Ignore Transparent | Easy | Tools | Don't pick transparent; skip or use underlying |
| 10 | Status Bar Zoom % | Easy | UI | Append " | 1600%" to status when zoomed |
| 11 | Fullscreen (F11) | Easy | UI | Toggle WindowState |
| 12 | Right-Click Context Menu | Medium | UX | Copy/Cut/Paste/Delete, tool switch, zoom fit |
| 13 | Fit/100% Zoom Buttons | Medium | Canvas | Fit canvas to viewport; 100% = 1× zoom |
| 14 | Zoom to Cursor (Ctrl+wheel) | DONE | Canvas | Ctrl+wheel zooms toward cursor (Feb 2026) |
| 15 | Open PNG | DONE | File | Load PNG into canvas; scale to fit |
| 16 | Merge Down | DONE | Layers | ⤓ button, context menu; alpha blend (Feb 2026) |
| 17 | Recent Colors (16 slots) | DONE | Color | 4×4 grid; fills on draw, palette pick, eyedropper (Feb 2026) |
| 18 | JSON Palette Loading | DONE | Color | PaletteLoader + dropdown (Feb 2026) |
| 19 | Quick Export (Ctrl+Shift+E) | Medium | File | Save with last path or prompt |
| 20 | Collapsible Panels | Medium | UI | Toggle left/right panels, Tab key |
| 21 | Layer opacity slider | DONE | Layers | Slider in layer row (Sprint 3 — Feb 2026) |
| 22 | Layer lock checkbox | DONE | Layers | Checkbox in layer row (Sprint 3 — Feb 2026) |
| 23 | Window title shows canvas size | DONE | UI | WindowTitle bound; updates on New/Open (Sprint 3 — Feb 2026) |
| 24 | Current tool in status bar | DONE | UI | StatusDisplayText includes tool name (Sprint 3 — Feb 2026) |
| 25 | Clear layer / Clear canvas | DONE | Canvas | ⌫ button in Layers panel; undoable (Sprint 3 — Feb 2026) |
| 26 | Save default filename | DONE | File | SaveFileDialog.FileName = Canvas WxH.png (Sprint 3 — Feb 2026) |
| 27 | Crosshair cursor on canvas | DONE | UX | CanvasCursor binding when drawing tool active (Sprint 3 — Feb 2026) |
| 28 | Hex color in status or tooltip | DONE | Color | CurrentColorHex tooltip on color swatch (Sprint 3 — Feb 2026) |

---

## Detailed Descriptions

### 1. Symmetry X/Y Toggle UI — **DONE (Feb 2026)**
- **Implemented**: Sym X, Sym Y ToggleButtons in MainWindow.xaml (lines 121–157), bound to `SymmetryX`, `SymmetryY`
- **Files**: MainWindow.xaml

### 2. Undo/Redo Toolbar Buttons — **Easy**
- **Current**: Ctrl+Z, Ctrl+Y work; no visible buttons
- **Work**: Add ↶ Undo and ↷ Redo buttons next to Save; bind to UndoCommand, RedoCommand
- **UX**: Disable when stack empty (CanExecute)

### 3. PNG Export Scale Dropdown — **Easy**
- **Current**: FileService.ExportToPng(canvas, path, 1) — hardcoded 1×
- **Work**: Add ComboBox (1×, 2×, 4×, 8×) in Save dialog or toolbar; pass to FileService
- **Files**: MainViewModel.Save(), MainWindow.xaml or SaveFileDialog extension

### 4. Escape to Cancel Paste — **Easy**
- **Current**: Paste mode has no cancel
- **Work**: Add `KeyBinding Key="Escape"` that calls `CancelPasteCommand` when `_isPasteMode`
- **Files**: MainWindow.xaml InputBindings, MainViewModel

### 5. Escape to Deselect — **Easy**
- **Current**: Selection persists until new selection or Delete
- **Work**: Escape clears selection (SelectionManager.ClearSelection)
- **Files**: MainViewModel, add Escape KeyBinding

### 6. Layer Delete Button — **Easy**
- **Current**: PixelCanvas.RemoveLayer(int) exists; Layers panel has "+" only
- **Work**: Add "-" button; call RemoveLayer(ActiveLayerIndex); keep ≥1 layer
- **Files**: MainWindow.xaml, MainViewModel.AddRemoveLayerCommand

### 7. Layer Duplicate — **Easy**
- **Current**: Layer.Clone() exists
- **Work**: Insert Clone() of active layer above current; name "Layer N (copy)"
- **Files**: MainViewModel.DuplicateLayerCommand, MainWindow.xaml

### 8. Layer Reorder (Up/Down) — **Easy**
- **Current**: PixelCanvas.MoveLayerUp/Down exist
- **Work**: Add ↑ and ↓ buttons per layer row, or in layer header
- **Files**: MainWindow.xaml (ListBox ItemTemplate), MainViewModel

### 9. Eyedropper Ignore Transparent — **Easy**
- **Current**: EyedropperTool picks any pixel including transparent
- **Work**: If picked color is transparent, don't fire ColorPicked (or sample from flattened composite)
- **Files**: Core/Tools.cs EyedropperTool

### 10. Status Bar Zoom % — **Easy**
- **Current**: StatusText shows "(x, y)" only
- **Work**: Append " | 1600%" when Zoom=16, etc.
- **Files**: MainViewModel.HandleMouseMove, UpdateBitmap status updates

### 11. Fullscreen (F11) — **Easy**
- **Current**: No fullscreen
- **Work**: KeyBinding F11 → Toggle Fullscreen; WindowState = Maximized vs Normal
- **Files**: MainWindow.xaml, MainWindow.xaml.cs or ViewModel

### 12. Right-Click Context Menu — **Medium**
- **Current**: Right-click does nothing on canvas
- **Work**: ContextMenu with Copy/Cut/Paste/Delete (when applicable), Zoom Fit, Grid toggle, tool shortcuts
- **Reference**: Python `context_menu_manager.py`
- **Files**: MainWindow.xaml (CanvasImage ContextMenu), MainViewModel

### 13. Fit/100% Zoom Buttons — **Medium**
- **Current**: Zoom dropdown only
- **Work**: "Fit" = compute zoom so canvas fits viewport; "100%" = Zoom=1
- **Challenge**: Need viewport size; use CanvasArea.ActualWidth/Height in code-behind
- **Files**: MainWindow.xaml, MainWindow.xaml.cs, MainViewModel

### 14. Zoom to Cursor (Ctrl+wheel) — **Medium**
- **Current**: Zoom dropdown; no mouse wheel zoom
- **Work**: Add MouseWheel handler; if Ctrl held, zoom toward cursor by adjusting PanOffset
- **Math**: PanOffset += (cursorScreen - center) * (1/newZoom - 1/oldZoom)
- **Files**: MainWindow.xaml.cs, MainViewModel

### 15. Open PNG — **Medium**
- **Current**: Open button not wired
- **Work**: OpenFileDialog → load PNG → create canvas from image; scale down if larger than max
- **Files**: FileService.ImportFromPng(), MainViewModel.OpenCommand

### 16. Merge Down — **Medium**
- **Current**: No merge
- **Work**: Alpha-blend active layer into layer below; remove active; update ActiveLayerIndex
- **Files**: PixelCanvas.MergeDown(int) or MainViewModel

### 17. Recent Colors (16 slots) — **Medium**
- **Current**: Palette only
- **Work**: On draw start, add CurrentColor to RecentColors list (max 16); show 4×4 grid
- **Persistence**: Optional — save to AppData
- **Files**: Core/RecentColorsManager, MainViewModel, MainWindow.xaml

### 18. JSON Palette Loading — **Medium**
- **Current**: Palette.SnesClassic hardcoded
- **Work**: Scan `assets/palettes/*.json` at startup; parse `{"colors": [[r,g,b,a], ...]}`; dropdown to switch
- **Reference**: Python `color_palette.py`, `assets/palettes/grass.json`
- **Files**: Core/Palette.cs or PaletteLoader, MainViewModel

### 19. Quick Export (Ctrl+Shift+E) — **Medium**
- **Current**: Save opens dialog every time
- **Work**: Remember last path; Ctrl+Shift+E saves there without dialog; if none, prompt
- **Files**: MainViewModel, store _lastExportPath

### 20. Collapsible Panels — **Medium**
- **Current**: Fixed 200px panels
- **Work**: Toggle visibility of left/right columns; Tab = collapse both; Shift+Tab = left only
- **Reference**: Python panel toggle
- **Files**: MainWindow.xaml (ColumnDefinition Width), MainViewModel

### 21. Layer opacity slider — **Easy**
- **Current**: Layer.Opacity property exists; no UI
- **Work**: Add a small slider (0–100%) or numeric in each layer row (or in a popup when layer selected)
- **Files**: MainWindow.xaml (ListBox ItemTemplate or layer detail), MainViewModel

### 22. Layer lock checkbox — **Easy**
- **Current**: Layer.IsLocked exists; no UI
- **Work**: Add a lock checkbox per layer row (e.g. next to visibility)
- **Files**: MainWindow.xaml (ListBox ItemTemplate), Layer binding

### 23. Window title shows canvas size — **Easy**
- **Current**: Title is static "Pixel Perfect"
- **Work**: Bind or update to "Pixel Perfect — 32×32" (and optionally " — Unsaved" when dirty)
- **Files**: MainWindow.xaml or code-behind, MainViewModel (optional Dirty flag)

### 24. Current tool in status bar — **Easy**
- **Current**: Status shows coords and zoom %
- **Work**: Append tool name, e.g. "(12, 8) | 1600% | Brush"
- **Files**: MainViewModel (StatusText or ZoomSuffix; include CurrentTool.Name)

### 25. Clear layer / Clear canvas — **Easy**
- **Current**: No one-shot clear
- **Work**: Button in toolbar or Layers panel, or shortcut (e.g. Ctrl+Shift+N or dedicated key); fill active layer with transparent; wrap in undo
- **Files**: MainViewModel.ClearLayerCommand, MainWindow.xaml

### 26. Save default filename — **Easy**
- **Current**: SaveFileDialog opens with no default filename
- **Work**: Set saveFileDialog.FileName = $"Canvas {Canvas.Width}x{Canvas.Height}.png" or "Untitled.png"
- **Files**: MainViewModel.Save()

### 27. Crosshair cursor on canvas — **Easy** (new idea)
- **Current**: Default arrow over canvas
- **Work**: When CurrentTool is a drawing tool (Brush, Eraser, Line, etc.), set Cursor = Cursors.Cross on CanvasImage; restore when Pan/Selection or when leaving canvas
- **Files**: MainWindow.xaml (CanvasImage Cursor binding or trigger) or code-behind

### 28. Hex color in status or tooltip — **Easy** (new idea)
- **Current**: Color swatch has no hex display
- **Work**: Show CurrentColor as #RRGGBB in status bar (e.g. when idle) or as ToolTip on the color preview Border
- **Files**: MainViewModel (StatusText or property for tooltip), MainWindow.xaml (ToolTip on color Border)

---

## Implementation Order (Suggested)

**Sprint 1 (Quick wins, ~2–4 hours)**  
2, 3, 4, 5, 6, 7, 8, 9, 10, 11 (item 1 done)

**Sprint 2 (Medium, ~4–8 hours)**  
12, 13, 14, 15, 16, 17, 18, 19, 20

**Sprint 3 (Low difficulty, ~2–3 hours)**  
21, 22, 23, 24, 25, 26, 27, 28

---

## Document Maintenance

- Update when features are implemented (move to CHANGELOG)
- Add new items from PARITY.md gaps
- Re-prioritize based on user feedback
