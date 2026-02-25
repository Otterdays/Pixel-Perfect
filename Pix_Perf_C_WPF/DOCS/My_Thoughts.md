# Pixel Perfect C# WPF — My Thoughts

Internal reasoning, design decisions, and lessons learned for AI continuity.

---

# Initial Project Audit — February 23, 2026

## What I Found

Reviewed the full `Pix_Perf_C_WPF/` project. This is a fresh C# WPF rewrite of the Python Pixel Perfect app (currently at v2.9.0). The scaffold is clean and well-structured:

**Strengths of the existing scaffold:**
1. MVVM is correctly applied — `MainViewModel` inherits `ObservableObject`, uses `[ObservableProperty]` source generators, and `[RelayCommand]` for commands
2. `PixelColor` as a `readonly struct` is the right call — avoids GC pressure in the rendering hot path
3. The `ITool` interface is clean and extensible
4. `FlattenLayers()` implements real alpha blending (not just layer override), which is the correct approach
5. The `FillTool` uses scanline optimization already, which shows good algorithmic thinking
6. `DarkTheme.xaml` uses proper resource key naming with a clear 8-token system
7. `NearestNeighbor` scaling on the canvas Image is essential for pixel art — good that it's already there
8. The checkerboard transparency BG is implemented in pure XAML (no external assets) — clean

**Issues I noted:**
1. Color preview in XAML has a broken `<MultiBinding Converter="{x:Null}">` — this will throw at runtime since null is not a valid converter
2. No keyboard shortcuts wired up at all
3. The layer ListBox has no active-layer highlight — the `SelectedIndex` binding works for selection, but the visual feedback (which item is the active drawing layer) is missing
4. Open/Save buttons are placeholder — fine for v0.1 but worth noting

## Documentation Strategy

Created a full `DOCS/` folder inside the WPF project (separate from the parent Python project's `DOCS/`). This keeps the two codebases self-contained. Each doc covers:
- `SUMMARY.md` — Status at a glance, comparison tables, docs index
- `ARCHITECTURE.md` — Deep dive into class design, data flow, rendering pipeline
- `SCRATCHPAD.md` — Active tasks, known issues, recent context
- `SBOM.md` — Single NuGet dep, runtime requirements, security
- `CHANGELOG.md` — v0.1.0 record + version roadmap
- `REQUIREMENTS.md` — Full feature port plan from Python version
- `My_Thoughts.md` — This file

## Key Design Decisions Going Forward

### Don't over-engineer undo from the start
The Python version's delta-based undo is great, but for a C# rewrite, consider using a `Stack<Action>` / `Stack<Action>` (do/undo) pattern first. If memory becomes an issue, swap to delta snapshots. Don't prematurely optimize.

### PixelColor converter is the first real task
The XAML currently has `Converter="{x:Null}"` for the color preview. This needs a `PixelColorToBrushConverter : IValueConverter` that converts a `PixelColor` to a `SolidColorBrush`. This is a quick win and makes the color display work properly.

### Consider a UserControl for the color picker
The Python version had the color picker as a right panel component managed by `ColorViewManager`. In WPF, this should be a proper `UserControl` with its own XAML and ViewModel, bound to the main ViewModel's `CurrentColor`. This keeps `MainWindow.xaml` clean.

### Layer active state feedback
The layer `ListBox` needs an `ItemContainerStyle` that highlights the selected item in the accent color. This is a WPF style trigger, not code. Example:
```xml
<ListBox.ItemContainerStyle>
    <Style TargetType="ListBoxItem">
        <Setter Property="Background" Value="Transparent"/>
        <Style.Triggers>
            <Trigger Property="IsSelected" Value="True">
                <Setter Property="Background" Value="{StaticResource Accent}"/>
            </Trigger>
        </Style.Triggers>
    </Style>
</ListBox.ItemContainerStyle>
```

### Keyboard shortcuts via InputBindings
WPF has a clean `InputBindings` mechanism. Tool shortcuts should be added to the Window's `InputBindings` collection in XAML, bound to the ViewModel commands. No need for a separate EventDispatcher class like the Python version.

### Don't replicate the 12-manager architecture
The Python version needed 12 manager classes because it started monolithic and had to refactor. The WPF version should use dedicated UserControls and Services from day one. Suggested structure going forward:
- `Services/UndoService.cs` — IUndoable command stack
- `Services/FileService.cs` — Save/load/export
- `ViewModels/ColorPickerViewModel.cs` — Separate VM for color panel
- `Controls/CanvasControl.xaml` — Extract canvas rendering as a UserControl
- `Controls/LayerPanel.xaml` — Layer management control
- `Controls/ColorPickerPanel.xaml` — Color selection control

This way `MainViewModel` stays as an orchestrator with < 200 lines, not a 3,000-line god class.

## Lessons from Python Version (Apply Here)

1. **Bitmap rendering** — Python switched from per-pixel rectangles to Pillow images at v2.9 for performance. WPF's `WriteableBitmap` is the right equivalent — stick with it, don't switch to `DrawingContext.DrawRectangle()` per pixel.

2. **Layer visibility** — Python had a bug where visibility toggles didn't refresh the canvas. In WPF, make sure `Layer.IsVisible` is `[ObservableProperty]` OR that the ViewModel calls `UpdateBitmap()` when the checkbox changes.

3. **Undo scope** — Save undo state BEFORE the operation, not after. The Python version learned this the hard way.

4. **Tools don't know about undo** — Tools just modify the layer. The ViewModel captures state before/after. Clean separation.

5. **Eyedropper event** — The existing `EyedropperTool.ColorPicked` event is already wired to `CurrentColor = color` in the ViewModel constructor. This is the right pattern — events from Core, subscriptions in ViewModel.

## What's Next

Priority order for next session:
1. ~~Fix the `Converter="{x:Null}"` color preview binding~~ (Complete)
2. ~~Add `ItemContainerStyle` to layer ListBox for active layer highlight~~ (Complete)  
3. ~~Add `InputBindings` for keyboard shortcuts (B/E/F/I, Ctrl+Z)~~ (Complete)
4. ~~Implement basic delta `UndoService` (action stack)~~ (Complete)
5. Wire up Save (PNG export)
6. Add canvas size presets (New Canvas dialog)

## February 25, 2026 — Undo System Success
Just wrapped up the Undo/Redo tracking system. Instead of full snapshots, I went straight to delta tracking because it's so much more scalable.
- **Layer.SetPixel**: Now triggers a `PixelChanged` event carrying the `OldColor` and `NewColor`.
- **UndoTransaction**: A struct that stores a dictionary of `(Layer, X, Y) -> PixelDelta`. This ignores intermediate overwrites across the same stroke! If you draw a squiggly line over the same pixel five times in one drag, it only tracks the *first* original color.
- **OnMouseDown / OnMouseUp**: In `MainViewModel`, they trigger `BeginTransaction()` and `EndTransaction()`.

It feels blazing fast and totally stable. The keyboard shortcuts `Ctrl+Z` and `Ctrl+Y` hook right in via `InputBindings`. Ready to conquer the actual File I/O (Export PNG / Save Project) next!

## February 25, 2026 — Advanced Tools & Architecture Fortification

### The Scaling Bug (LayoutTransform vs Zoom Matrix)
I fixed a fascinating core coordinate bug today. The mouse was clamping everything to a top-left `2x2` pixel zone while zoomed. The logic was manually dividing `point.X / ViewModel.Zoom`, but because the image uses WPF's `LayoutTransform`, WPF *already* mathematically inverts and maps `e.GetPosition` down to the unscaled local canvas coordinates! Manually applying the zoom a second time basically mapped a `32x32` canvas down to `2x2`. Removing that division cleanly solved both the cursor locking and the weird color artifacts. 

### Symmetry as an Interface (`ISymmetricTool`)
Instead of tangling each tool with `bool SymX, SymY` and messy conditional checking, I extracted it into a specialized `ISymmetricTool` interface with a `SymmetryExtensions` class extending `Layer`. 

It gracefully handles raw pixels alongside `SaveSymmetricPixelState` (used for live shape previews). The `MainViewModel` merely checks `if (CurrentTool is ISymmetricTool symTool)` before interacting with it, preserving total decoupling. `UndoManager` swallows the symmetric strokes magically since it just looks like multiple pixels updating concurrently!

### Float Transforms
Added `Rotate90`, `MirrorHorizontal`, and `MirrorVertical` directly to `SelectionManager`. They mathematically transpose/mirror the floating array in memory over the `SelectedPixels` buffer while wiping and redrawing `_backgroundPixels` without committing pixel deltas straight into the backing layer until the user drops it. Perfectly non-destructive.
