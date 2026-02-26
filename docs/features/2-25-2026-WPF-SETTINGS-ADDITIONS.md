# WPF Port — Settings Expansion Plan
**Date**: February 25, 2026  
**Version**: 0.2.3 → Target: 0.3.0  
**Current Settings**: 3 (Grid color, Checkerboard colors, Undo limit)  
**Proposed Total**: 25 (3 existing + 22 new)

---

## 📊 Summary

The current WPF Settings dialog (`SettingsDialog.xaml`) has only **3 controls** in a tiny 360×340 window. The Python version's `MAX_SETTINGS.md` catalogs 127 possible settings, but most don't apply to the WPF port's current feature set.

This document proposes **22 new settings** filtered for:
- ✅ Relevance to WPF port's current tools and features
- ✅ High impact for pixel art workflow
- ✅ Easy-to-Medium complexity (KISS / YAGNI)
- ✅ Maps directly to existing MVVM patterns and codebase

### Settings by Tier

| Tier | Count | Theme |
|------|-------|-------|
| 🔴 Tier 1 — Must-Have | 6 | Core workflow & data safety |
| 🟡 Tier 2 — Should-Have | 6 | Professional polish |
| 🟢 Tier 3 — Nice-to-Have | 5 | Fine-tuning & preference |
| 🔵 Novel — WPF-Specific | 5 | Differentiators from Python version |

---

## 🔴 Tier 1 — Must-Have (High Impact, Easy)

### 1. Default Canvas Size
- **Impact**: ⭐⭐⭐⭐⭐ — Saves clicks on every new project
- **Current**: Always opens `NewCanvasDialog`, defaults to nothing
- **Proposed**: Dropdown — `8×8, 16×16, 32×32, 64×64, 128×128, 256×256, Ask Each Time`
- **Implementation**:
  - Add `[ObservableProperty] private string _defaultCanvasSize = "Ask Each Time";`
  - In `NewCanvas()`, skip dialog if preset selected, call `CreateCanvas(w, h)` directly
  - Add `ComboBox` in Settings dialog under "Canvas" section
  - Persist to `%AppData%/PixelPerfect/settings.json`

### 2. Confirm on Exit (Unsaved Changes Guard)
- **Impact**: ⭐⭐⭐⭐⭐ — Prevents data loss
- **Current**: `IsDirty` flag exists, `ConfirmDiscardUnsaved` callback exists for New Canvas, but **window closing has NO guard**
- **Proposed**: `Window.Closing` event checks `IsDirty` and shows "Save before closing?" dialog
- **Implementation**:
  - Add `Closing` handler in `MainWindow.xaml.cs`
  - Reuse existing `ConfirmDiscardUnsaved` pattern
  - Add `[ObservableProperty] private bool _confirmOnExit = true;` as a toggle
  - Options: "Save", "Don't Save", "Cancel"

### 3. Auto-Save
- **Impact**: ⭐⭐⭐⭐⭐ — Data safety critical for any editor
- **Current**: No auto-save whatsoever
- **Proposed**: Timer-based snapshot every N minutes to `%AppData%/PixelPerfect/autosave/`
- **Implementation**:
  - Add `[ObservableProperty] private int _autoSaveIntervalMinutes = 0;` (0 = off)
  - Options: `Off, 1, 5, 10, 15, 30` minutes
  - Use `DispatcherTimer` in MainViewModel
  - Save as PNG to autosave folder with timestamp filename
  - Show "Auto-saved" in status bar
  - On startup, check for recovery files and offer to restore

### 4. Default Palette
- **Impact**: ⭐⭐⭐⭐ — Start with preferred palette
- **Current**: Always defaults to SNES Classic (first in `AvailablePalettes`)
- **Proposed**: Dropdown of all loaded palettes + "Last Used"
- **Implementation**:
  - Add `[ObservableProperty] private string _defaultPaletteName = "SNES Classic";`
  - In constructor, find matching palette from `AvailablePalettes` and set `SelectedPalette`
  - Add `ComboBox` in Settings with `ItemsSource="{Binding AvailablePalettes}"`
  - Persist to settings file

### 5. Grid Opacity
- **Impact**: ⭐⭐⭐⭐ — Fine-tune grid visibility without disabling
- **Current**: Grid is either 100% visible or hidden (toggle only)
- **Proposed**: Slider from 10% to 100%
- **Implementation**:
  - Add `[ObservableProperty] private double _gridOpacity = 1.0;`
  - In `MainWindow.xaml`, bind grid overlay `ItemsControl.Opacity="{Binding GridOpacity}"`
  - Add `Slider` in Settings under "Grid" section
  - Live preview in settings dialog

### 6. Symmetry Drawing Toggles
- **Impact**: ⭐⭐⭐⭐ — THE #1 pixel art workflow feature
- **Current**: `ISymmetricTool` interface exists with `SymmetryX`/`SymmetryY` on Brush, Line, Rectangle, Circle — but **there is ZERO UI to toggle them**. Dead feature.
- **Proposed**: Two toolbar toggle buttons (↔ Horizontal Mirror, ↕ Vertical Mirror) + Settings checkboxes for defaults
- **Implementation**:
  - Add `[ObservableProperty] private bool _symmetryX;` and `_symmetryY;` to MainViewModel
  - In `OnSymmetryXChanged`, propagate to all tool instances: `BrushTool.SymmetryX = value;` etc.
  - Add `ToggleButton` pair in toolbar with icons
  - Add default toggles in Settings under "Tools" section
  - Keyboard shortcuts: `Shift+X` / `Shift+Y`

---

## 🟡 Tier 2 — Should-Have (Medium Impact, Easy-Medium)

### 7. Major Grid Lines
- **Impact**: ⭐⭐⭐⭐ — Essential for sprite sheets and tile boundaries
- **Current**: Uniform 1px grid, every pixel looks the same
- **Proposed**: Every N pixels (8, 16, 32), draw a brighter/thicker line
- **Implementation**:
  - Add `[ObservableProperty] private int _majorGridInterval = 0;` (0 = off)
  - Options: `Off, 4, 8, 16, 32`
  - In `RefreshGridOverlay`, generate major lines with a distinct `Stroke` color/thickness
  - Use `GridLineSegment` with an `IsMajor` flag, or a separate `MajorGridOverlayLines` collection

### 8. Default Export Scale
- **Impact**: ⭐⭐⭐⭐ — Remember preferred scale across sessions
- **Current**: `ExportScale` resets to 1 on every app launch
- **Proposed**: Persist the export scale setting
- **Implementation**:
  - Already exists as `[ObservableProperty] private int _exportScale = 1;`
  - Just needs persistence to settings file
  - Add to Settings dialog under "Export" section

### 9. Shape Fill Default
- **Impact**: ⭐⭐⭐ — Remember filled vs outline preference
- **Current**: `CircleTool.Fill` and `RectangleTool.Fill` default to `false`, reset every launch
- **Proposed**: Persist the fill toggle state
- **Implementation**:
  - Add `[ObservableProperty] private bool _shapeFillDefault = false;`
  - On change, propagate to `CircleTool.Fill` and `RectangleTool.Fill`
  - Add `CheckBox` in Settings under "Tools"
  - Also expose as toolbar toggle button: `☐/■`

### 10. Checkerboard Tile Size
- **Impact**: ⭐⭐⭐ — Larger canvases need larger tiles
- **Current**: Hardcoded 16px in `CreateCheckerboardBrush` Viewport (8px squares)
- **Proposed**: Dropdown: `8, 16, 32, 64` pixel tiles
- **Implementation**:
  - Add `[ObservableProperty] private int _checkerboardTileSize = 16;`
  - Modify `CreateCheckerboardBrush` to use dynamic Viewport size
  - Invalidate `_checkerboardBrushCache` on change
  - Add `ComboBox` in Settings under existing Checkerboard section

### 11. Default Brush Size
- **Impact**: ⭐⭐⭐ — Workflow convenience
- **Current**: Always starts at 1px
- **Proposed**: Persist brush size preference (1-8)
- **Implementation**:
  - Already exists as `[ObservableProperty] private int _brushSize = 1;`
  - Just persist to settings file
  - Add `ComboBox` or `Slider` in Settings under "Tools"

### 12. Pixel Cursor Highlight
- **Impact**: ⭐⭐⭐⭐ — Shows exact pixel under cursor
- **Current**: No cursor feedback (Bug Report #18 simplified)
- **Proposed**: A single semi-transparent highlight square following the mouse in canvas space
- **Implementation**:
  - Add `[ObservableProperty] private bool _showPixelCursor = true;`
  - In `MainWindow.xaml`, add a `Rectangle` overlay that follows mouse position
  - Position: `Canvas.SetLeft/Top(rect, canvasX * Zoom, canvasY * Zoom)`
  - Style: 1px white border, no fill, `Opacity=0.6`
  - Much simpler than the full Adorner layer from Bug Report #18

---

## 🟢 Tier 3 — Nice-to-Have (Medium Impact, Easy)

### 13. Fill Tolerance
- **Impact**: ⭐⭐⭐ — Allow fuzzy color matching for fill/magic wand
- **Current**: Exact color match only in `FloodFill` and `MagicWandTool`
- **Proposed**: Slider 0-50 (0 = exact, 50 = fuzzy)
- **Implementation**:
  - Add `[ObservableProperty] private int _fillTolerance = 0;`
  - Modify `FloodFill` to use color distance check instead of `==`
  - `int dist = Math.Abs(a.R - b.R) + Math.Abs(a.G - b.G) + Math.Abs(a.B - b.B) + Math.Abs(a.A - b.A);`
  - `if (dist <= tolerance)` instead of `if (a == b)`
  - Pass tolerance into tool methods

### 14. Eraser Mode
- **Impact**: ⭐⭐⭐ — Erase to transparent vs background color
- **Current**: Always erases to `PixelColor.Transparent`
- **Proposed**: Toggle: "To Transparent" (default) or "To Background Color"
- **Implementation**:
  - Add `[ObservableProperty] private bool _eraserToBackground = false;`
  - If true, eraser sets pixel to `SecondaryColor` instead of `Transparent`
  - Add `CheckBox` in Settings or right-click eraser menu

### 15. Pan Sensitivity
- **Impact**: ⭐⭐⭐ — Control pan speed
- **Current**: 1:1 mouse delta mapping
- **Proposed**: Slider 25%-200%
- **Implementation**:
  - Add `[ObservableProperty] private double _panSensitivity = 1.0;`
  - In `AddPanDelta`, multiply: `PanOffsetX += deltaX * PanSensitivity;`
  - Add `Slider` in Settings

### 16. Recent Colors Count
- **Impact**: ⭐⭐ — Customize recent colors capacity
- **Current**: Hardcoded at 8 in `AddToRecentColors`
- **Proposed**: Dropdown: `4, 8, 12, 16, 24`
- **Implementation**:
  - Add `[ObservableProperty] private int _recentColorsMax = 8;`
  - Use in `AddToRecentColors`: `while (RecentColors.Count > RecentColorsMax)`
  - Add `ComboBox` in Settings

### 17. Canvas Border
- **Impact**: ⭐⭐ — Visual separation from dark background
- **Current**: Canvas blends into dark checkerboard, hard to see edges
- **Proposed**: Toggle a 1-2px border around the canvas area
- **Implementation**:
  - Add `[ObservableProperty] private bool _showCanvasBorder = true;`
  - In XAML, add `BorderBrush="{DynamicResource AccentColor}"` and `BorderThickness="1"` on the canvas container, bound to setting

---

## 🔵 Novel — WPF-Specific Additions

### 18. Tablet / Stylus Pressure Sensitivity
- **Impact**: ⭐⭐⭐⭐ — Major differentiator for digital artists
- **Current**: No pressure handling
- **Proposed**: Map pen pressure to brush opacity or size
- **Implementation**:
  - WPF has `StylusDown`/`StylusMove` events with `StylusPointCollection`
  - `float pressure = e.StylusDevice.StylusPoints[0].PressureFactor;` (0.0–1.0)
  - Add `[ObservableProperty] private bool _tabletPressureEnabled = false;`
  - Add `PressureMode` enum: `Off, OpacityControl, SizeControl`
  - Pass pressure to tool's `OnMouseDown/Move` as an optional parameter

### 19. Window Layout Persistence
- **Impact**: ⭐⭐⭐⭐ — Professional feel, eliminates re-setup
- **Current**: Window position/size resets every launch
- **Proposed**: Remember window position, size, and state (maximized/normal)
- **Implementation**:
  - Add `WindowSettings` class with `Left, Top, Width, Height, WindowState`
  - Save to `%AppData%/PixelPerfect/layout.json` on window close
  - Restore on startup in `MainWindow` constructor
  - Add "Reset Layout" button in Settings

### 20. Tile Preview Mode (Default State)
- **Impact**: ⭐⭐⭐ — Python v2.7.5 has full tile preview
- **Current**: No tile preview in WPF port
- **Proposed**: When tile preview is ported, this setting controls whether it starts enabled
- **Implementation**:
  - Add `[ObservableProperty] private bool _tilePreviewDefault = false;`
  - Pre-wires the setting before the feature is built
  - Referenced in future tile preview implementation

### 21. Color Format Display
- **Impact**: ⭐⭐⭐ — Pixel artists share colors by hex code constantly
- **Current**: Status bar shows coordinates only, no color info
- **Proposed**: Show current color as `#RRGGBB` in status bar + tooltips on palette swatches
- **Implementation**:
  - Add `[ObservableProperty] private string _colorDisplayFormat = "Hex";` (Hex, RGB, HSV)
  - Computed property: `public string CurrentColorText => $"#{CurrentColor.R:X2}{CurrentColor.G:X2}{CurrentColor.B:X2}";`
  - Bind in status bar area
  - Add `ToolTip` to palette swatch ItemTemplate

### 22. Startup Behavior
- **Impact**: ⭐⭐⭐ — Control what happens on app launch
- **Current**: Always creates blank 32×32 canvas
- **Proposed**: Dropdown: `New Canvas, Last Opened, Welcome Screen`
- **Implementation**:
  - Add `[ObservableProperty] private string _startupBehavior = "New Canvas";`
  - "Last Opened" saves last file path and opens it
  - "Welcome Screen" could show recent files list (future)
  - Ties into Default Canvas Size setting (#1)

---

## 🏗️ Settings Dialog Redesign

The current dialog needs expansion from 3 groups to organized **tabs**:

```
┌─────────────────────────────────────────────┐
│  Settings                              [X]  │
├─────────────────────────────────────────────┤
│  [Canvas] [Grid] [Tools] [Export] [General] │
├─────────────────────────────────────────────┤
│                                             │
│  ┌ Canvas ─────────────────────────────┐    │
│  │ Default size:    [32×32        ▼]   │    │
│  │ Checkerboard:    [Dark] [Light]     │    │
│  │ Tile size:       [16px         ▼]   │    │
│  │ Canvas border:   [✓]               │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌ Grid ───────────────────────────────┐    │
│  │ Grid color:      [■] presets        │    │
│  │ Grid opacity:    [━━━━━━━●━] 75%    │    │
│  │ Major lines:     [Every 8px    ▼]   │    │
│  └─────────────────────────────────────┘    │
│                                             │
│           [OK]        [Cancel]              │
└─────────────────────────────────────────────┘
```

### Tab Layout:

1. **Canvas** — Default size, checkerboard colors/tile size, canvas border
2. **Grid** — Grid color, opacity, major grid lines
3. **Tools** — Default brush size, symmetry defaults, shape fill, fill tolerance, eraser mode, pixel cursor, pan sensitivity
4. **Export** — Default scale, default palette, recent colors count, color format
5. **General** — Undo limit, confirm on exit, auto-save, startup behavior, window layout, tablet pressure

---

## 📋 Implementation Priority

### Phase 1 (v0.3.0 — Core Safety + Workflow)
1. ☐ Confirm on Exit (#2)
2. ☐ Symmetry Toggles (#6) — unlocks dead code!
3. ☐ Default Canvas Size (#1)
4. ☐ Grid Opacity (#5)
5. ☐ Default Palette (#4)
6. ☐ Settings Persistence (JSON file backbone)

### Phase 2 (v0.3.1 — Polish)
7. ☐ Pixel Cursor Highlight (#12)
8. ☐ Major Grid Lines (#7)
9. ☐ Shape Fill Default (#9)
10. ☐ Default Brush Size (#11)
11. ☐ Default Export Scale (#8)
12. ☐ Checkerboard Tile Size (#10)

### Phase 3 (v0.3.2 — Refinement)
13. ☐ Auto-Save (#3)
14. ☐ Fill Tolerance (#13)
15. ☐ Color Format Display (#21)
16. ☐ Window Layout Persistence (#19)
17. ☐ Canvas Border (#17)
18. ☐ Recent Colors Count (#16)

### Phase 4 (v0.4.0 — Differentiation)
19. ☐ Tablet Pressure Sensitivity (#18)
20. ☐ Eraser Mode (#14)
21. ☐ Pan Sensitivity (#15)
22. ☐ Startup Behavior (#22)

---

## 🔑 Architecture Notes

### Settings Persistence
All settings should be stored in a single JSON file at `%AppData%/PixelPerfect/settings.json`:

```csharp
public class AppSettings
{
    // Canvas
    public string DefaultCanvasSize { get; set; } = "Ask Each Time";
    public int CheckerboardTileSize { get; set; } = 16;
    public bool ShowCanvasBorder { get; set; } = true;
    
    // Grid
    public string GridColorHex { get; set; } = "#404040";
    public double GridOpacity { get; set; } = 1.0;
    public int MajorGridInterval { get; set; } = 0;
    
    // Tools
    public int DefaultBrushSize { get; set; } = 1;
    public bool SymmetryXDefault { get; set; } = false;
    public bool SymmetryYDefault { get; set; } = false;
    public bool ShapeFillDefault { get; set; } = false;
    public int FillTolerance { get; set; } = 0;
    public bool EraserToBackground { get; set; } = false;
    public bool ShowPixelCursor { get; set; } = true;
    public double PanSensitivity { get; set; } = 1.0;
    
    // Export
    public int DefaultExportScale { get; set; } = 1;
    public string DefaultPaletteName { get; set; } = "SNES Classic";
    public int RecentColorsMax { get; set; } = 8;
    public string ColorDisplayFormat { get; set; } = "Hex";
    
    // General
    public int UndoHistoryLimit { get; set; } = 100;
    public bool ConfirmOnExit { get; set; } = true;
    public int AutoSaveIntervalMinutes { get; set; } = 0;
    public string StartupBehavior { get; set; } = "New Canvas";
    public bool TabletPressureEnabled { get; set; } = false;
}
```

Use `System.Text.Json` for serialization. Load on startup, save on dialog OK and on window close. The `SettingsService` static class pattern mirrors the existing `ThemeService`.
