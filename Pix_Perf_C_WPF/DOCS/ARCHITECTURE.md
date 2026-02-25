# Pixel Perfect C# WPF — Architecture

**Version**: 0.2.3  
**Last Updated**: February 25, 2026  
**Pattern**: MVVM (Model-View-ViewModel)

---

## 1. High-Level Overview

The application is structured into four clean layers:

```
┌─────────────────────────────────────────────────┐
│                   Views (XAML)                   │
│  MainWindow.xaml  │  DarkTheme.xaml              │
│  (UI layout, visual tree, data bindings)         │
├─────────────────────────────────────────────────┤
│              Views Code-Behind                   │
│  MainWindow.xaml.cs                              │
│  (Mouse event handling → ViewModel delegation)   │
├─────────────────────────────────────────────────┤
│                ViewModels                        │
│  MainViewModel.cs                                │
│  (State, commands, bitmap rendering)             │
├─────────────────────────────────────────────────┤
│                Core (Models)                     │
│  PixelColor  │  Layer  │  PixelCanvas  │  Tools  │
│  (Pure data, zero UI dependencies)               │
└─────────────────────────────────────────────────┘
```

### Data Flow

```
User Click → MainWindow.xaml.cs (GetCanvasPosition)
           → MainViewModel.HandleMouseDown(x, y)
           → ITool.OnMouseDown(layer, x, y, color)
           → Layer.SetPixel(x, y, color)
           → MainViewModel.UpdateBitmap()
           → PixelCanvas.FlattenLayers()
           → WriteableBitmap.WritePixels()
           → WPF renders updated Image
```

---

## 2. Core Layer (`PixelPerfect.Core`)

### 2.1 PixelColor (Struct)

```
PixelColor (readonly struct)
├── R, G, B, A : byte
├── Static: Transparent, Black, White
├── IsTransparent : bool
├── ToUInt32() / FromUInt32() — packed ARGB conversion
└── Equality operators (==, !=)
```

**Why a struct?** Pixel colors are created and destroyed millions of times during rendering. A `readonly struct` avoids heap allocation entirely — each pixel is 4 bytes on the stack. This is critical for the `FlattenLayers()` hot path.

### 2.2 Layer

```
Layer
├── Properties:
│   ├── Name : string
│   ├── Width, Height : int (immutable)
│   ├── IsVisible : bool (default true)
│   ├── Opacity : double (0.0–1.0, default 1.0)
│   └── IsLocked : bool (default false)
├── Storage:
│   └── _pixels : PixelColor[Height, Width]  (2D array, row-major)
├── Methods:
│   ├── GetPixel(x, y) → PixelColor
│   ├── SetPixel(x, y, color) — respects IsLocked
│   ├── IsInBounds(x, y) → bool
│   ├── Clear() — fills with Transparent
│   ├── Clone() → Layer (deep copy)
│   └── GetPixelArray() → PixelColor[,] (raw access for rendering)
```

**Key detail**: `SetPixel` checks `IsLocked` before writing. `GetPixel` returns `Transparent` for out-of-bounds access (safe default).

### 2.3 PixelCanvas

```
PixelCanvas
├── Properties:
│   ├── Width, Height : int (immutable)
│   ├── Layers : ObservableCollection<Layer>
│   ├── ActiveLayerIndex : int
│   └── ActiveLayer : Layer? (computed)
├── Layer Management:
│   ├── AddLayer(name) → Layer
│   ├── RemoveLayer(index) — prevents removing last layer
│   ├── MoveLayerUp(index)
│   └── MoveLayerDown(index) — tuple swap
└── Rendering:
    └── FlattenToBuffer(byte[])
        (alpha-blends all visible layers bottom-to-top directly into byte array)
```

**FlattenLayers algorithm**: Iterates layers bottom-to-top. For each visible layer, blends each non-transparent pixel using standard alpha compositing:
- If source alpha ≥ 1.0 or destination is transparent: direct replace
- Otherwise: `result = src * srcAlpha + dst * (1 - srcAlpha)`

### 2.4 Tools System

```
ToolType (enum)
├── Brush, Eraser, Fill, Eyedropper
├── Line, Rectangle, Circle
├── Selection, Move, MagicWand
└── Pan, Spray, Dither
    (Edge, Texture, Zoom planned)

ITool (interface)
├── Type : ToolType
├── Name : string
├── OnMouseDown(layer, x, y, color)
├── OnMouseMove(layer, x, y, color)
└── OnMouseUp(layer, x, y, color)

ISymmetricTool (interface)
├── SymmetryX : bool
└── SymmetryY : bool
```

**Implemented Tools** (13 total):

| Tool | Key Behavior |
|------|-------------|
| `BrushTool` | Variable size square brush, tracks `_isDrawing` state, implements `ISymmetricTool` |
| `EraserTool` | Like brush but always writes `Transparent` |
| `FillTool` | Scanline flood fill (stack-based, horizontal span optimization) |
| `EyedropperTool` | Fires `ColorPicked` event with sampled color |
| `LineTool` | Bresenham's algorithm with live preview, ISymmetricTool compatible |
| `RectangleTool` | Outline/fill with live preview, ISymmetricTool compatible |
| `CircleTool` | Midpoint algorithm with 8-way symmetry, ISymmetricTool compatible |
| `SelectionTool` | Rectangle selection, captures to SelectionManager |
| `MoveTool` | Non-destructive move via SelectionManager |
| `PanTool` | No-op; pan handled by View |
| `SprayTool` | Random particle scattering within radius, implements `ISymmetricTool` |
| `DitherTool` | Checkerboard drawing via `(x+y)%2=0`, implements `ISymmetricTool` |
| `MagicWandTool` | Breadth-first contiguous matching for non-rectangular selections via SelectionManager `CaptureMaskedFromLayer` |

**Fill algorithm**: Uses scanline optimization — finds full horizontal spans before pushing adjacent rows. This is significantly faster than naive 4-directional flood fill for large areas.

---

## 3. ViewModel Layer

### 3.1 MainViewModel

```
MainViewModel : ObservableObject
├── Observable Properties:
│   ├── Canvas : PixelCanvas
│   ├── CurrentColor : PixelColor
│   ├── CurrentTool : ITool
│   ├── Zoom : int (1–64)
│   ├── CanvasBitmap : WriteableBitmap?
│   └── StatusText : string
├── Tool Instances:
│   ├── BrushTool, EraserTool, FillTool, EyedropperTool
│   └── ZoomLevels : int[] { 1,2,4,8,16,24,32,48,64 }
├── Commands (RelayCommand):
│   ├── SelectBrush, SelectEraser, SelectFill, SelectEyedropper
│   ├── NewCanvas
│   └── AddLayer
├── Mouse Handlers:
│   ├── HandleMouseDown(x, y)
│   ├── HandleMouseMove(x, y, isPressed)
│   └── HandleMouseUp(x, y)
└── Rendering:
    └── UpdateBitmap()
        (flattens layers → writes BGRA pixel buffer → WriteableBitmap)
```

**Rendering pipeline**: 
1. `FlattenToBuffer(byte[])` sequentially blends layers and directly writes BGRA (`PixelFormats.Bgra32`) into pre-allocated memory.
2. `WritePixels()` writes the buffer to the `WriteableBitmap`
3. WPF data binding automatically displays the updated bitmap

**Note**: The bitmap is created at canvas resolution (e.g., 32×32) and scaled up by WPF's `LayoutTransform` using `NearestNeighbor` scaling. This keeps the bitmap tiny and fast.

---

## 4. View Layer

### 4.1 MainWindow.xaml — Layout

```
Window (1200×800, min 900×600)
├── Row 0: Top Toolbar (40px)
│   ├── New, Open, Save buttons
│   ├── Separator
│   └── Zoom: ComboBox
├── Row 1: Main Content (fills)
│   ├── Col 0: Left Panel (200px) — Tools & Color
│   │   ├── Tools Section — Size slider (1–32) + 4-column UniformGrid
│   │   │   └── ✏️ Brush | 🧹 Eraser | 🪣 Fill | 💧 Eyedropper | …
│   │   ├── Color Preview (64×64, hex tooltip)
│   │   ├── Palette (dropdown + grid); Recent Colors (4×4, 16 slots)
│   ├── Col 1: Canvas Area (fills)
│   │   ├── Checkerboard Rectangle (transparency BG)
│   │   └── Image (CanvasBitmap, NearestNeighbor, ScaleTransform)
│   └── Col 2: Right Panel (200px) — Layers
│       ├── "Layers" header + "+" Add Layer button
│       └── ListBox (layer name + visibility checkbox)
└── Row 2: Status Bar (24px)
    └── StatusText (coordinates / messages)
```

### 4.2 MainWindow.xaml.cs — Event Handling

The code-behind is intentionally minimal — only handles WPF mouse events and converts them to canvas coordinates:

```
GetCanvasPosition(MouseEventArgs) → (int x, int y)?
├── Gets position relative to CanvasImage
├── Divides by Zoom to get canvas pixel coordinates
├── Returns null if out of canvas bounds
└── Used by MouseDown, MouseMove, MouseUp handlers
```

Mouse capture is used during drawing to allow strokes that go outside the image bounds without losing the drawing state.

### 4.3 DarkTheme.xaml — Design System

```
Colors (8 tokens):
├── BackgroundPrimary:   #1E1E1E (darkest)
├── BackgroundSecondary: #252526 (panels)
├── BackgroundTertiary:  #2D2D30 (buttons/inputs)
├── Accent:              #007ACC (hover)
├── AccentHover:         #1C97EA (pressed)
├── TextPrimary:         #FFFFFF
├── TextSecondary:       #CCCCCC
└── Border:              #3F3F46

ToolButton Style:
├── Background: Tertiary
├── Border: 1px solid BorderColor
├── CornerRadius: 4px
├── Cursor: Hand
├── Hover: Accent background
└── Pressed: AccentHover background
```

---

## 5. Future Architecture Plans

### Already Implemented (v0.1.x)
```
Core/
├── UndoManager.cs        # Delta-based undo transaction tracking ✅
├── Tools.cs              # 7 tools (Brush, Eraser, Fill, Eyedropper, Line, Rect, Circle) ✅

Services/
└── FileService.cs        # PNG export via SaveCommand ✅

Converters/
└── PixelColorToBrushConverter.cs  # Color preview binding ✅
```

### Phase 1 Additions (Next)
```
Core/
└── SelectionManager.cs   # Rectangle selection + clipboard

ViewModels/
├── MainViewModel.cs      # Extended with selection/move commands
└── ColorPickerViewModel.cs  # Separate VM for color management

Views/
├── ColorPickerPanel.xaml  # UserControl for color selection
└── Dialogs/
    ├── NewCanvasDialog.xaml
    └── ExportDialog.xaml
```

### Phase 2 Additions
```
Core/
├── AnimationTimeline.cs   # Frame management
└── Palette.cs             # JSON palette loading

Views/
├── AnimationPanel.xaml    # Timeline UI
└── PalettePanel.xaml      # Color palette grid
```
*Note: Shape tools (Line, Rect, Circle) already implemented in v0.1.2.*

---

## 6. Design Principles

1. **KISS** — Keep it simple. Don't port Python complexity, redesign for C#
2. **MVVM strict** — Code-behind only for platform-specific events (mouse)
3. **Core is pure** — `Core/` namespace has zero UI dependencies
4. **Value types for hot paths** — `PixelColor` is a struct, not a class
5. **ObservableCollection** — Layer list auto-updates UI via data binding
6. **No premature optimization** — Ship working features first, optimize later
7. **Tool interface** — Adding a new tool = implement `ITool`, register in ViewModel
