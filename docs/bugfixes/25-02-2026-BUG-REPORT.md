🔍 C# WPF Port — Code Review Report
Date: February 25, 2026 | Version: 0.1.3 → **0.2.1 (post-fixes)**

**Status: ✅ 14 of 20 items IMPLEMENTED — Build verified.**

The codebase is solid and well-structured. Below is a thorough analysis organized by category — Bugs, Performance, and Novel UX/Architecture opportunities.

🐛 Bugs & Correctness Issues
1. 

UndoManager
 uses List as a Stack — O(n) operations (Medium severity)
Location: 

Core/UndoManager.cs
 — Lines 82–84, 103–104, 117–118

csharp
// BUG: Insert(0,...) and RemoveAt(0) on a List<T> are O(n) — all items shift.
_undoStack.Insert(0, _currentTransaction); // O(n) every time!
_undoStack.RemoveAt(0);                    // O(n) every time!
_undoStack.Insert(0, tx);                  // O(n) on redo!
The fix: Use LinkedList<T> or a true Stack<T> with a mirror for redo. Since you already use Stack<UndoTransaction> for _redoStack, unifying both to Stack<> would be cleaner and bring these back to 

O(1)
:

csharp
private readonly Stack<UndoTransaction> _undoStack = new();
private readonly Stack<UndoTransaction> _redoStack = new();
// Then: _undoStack.Push(tx), _undoStack.Pop(), trim oldest = harder;
// for limit enforcement, a LinkedList<T> is ideal
2. 

Escape
 command clears selection pixels without undo (Medium severity)
Location: 

ViewModels/MainViewModel.cs
 — Lines 603–620

csharp
private void Escape()
{
    // ...
    var layer = Canvas.ActiveLayer;
    if (layer != null) ClearSelectionPixels(layer); // ← No BeginTransaction + EndTransaction!
    SelectionManager.ClearSelection();
    // ...
}
Pressing Escape will destructively delete the selection's pixels permanently with no undo. The same applies to the 

Delete
 and 

Cut
 commands — only 

Cut
 is missing an undo transaction wrap around 

ClearSelectionPixels
.

Fix: Wrap 

ClearSelectionPixels
 calls in UndoManager.BeginTransaction() / UndoManager.EndTransaction().

3. 

FillTool
 can produce duplicate stack pushes (O(n²) worst-case) (Medium severity)
Location: 

Core/Tools.cs
 — Lines 252–288

The scanline flood fill pushes 

(i, cy-1)
 and 

(i, cy+1)
 for every pixel on the span, not just at boundary transitions. For a solid-color region, this pushes thousands of duplicate coordinates onto the stack (one per pixel, not one per span edge), negating the benefit of a scanline approach.

csharp
// Current: pushes for EVERY pixel — O(width * height) stack entries
if (cy > 0 && layer.GetPixel(i, cy - 1) == target)
    stack.Push((i, cy - 1)); // ← pushed for every i, not just at transitions
Fix: Track when you cross a same-color boundary — only push seeds at the start/end of a contiguous run above/below:

csharp
bool inAbove = false, inBelow = false;
for (int i = left; i <= right; i++)
{
    layer.SetPixel(i, cy, replacement);
    bool above = cy > 0 && layer.GetPixel(i, cy - 1) == target;
    if (above && !inAbove) stack.Push((i, cy - 1));
    inAbove = above;
    bool below = cy < layer.Height - 1 && layer.GetPixel(i, cy + 1) == target;
    if (below && !inBelow) stack.Push((i, cy + 1));
    inBelow = below;
}
4. 

MagicWandTool
 uses a naïve 4-connected BFS without scanline optimization (Low-Medium severity)
Location: 

Core/Tools.cs
 — Lines 826–868

Same issue as FillTool — the stack can hold O(width × height) entries. For a 256×256 canvas, that's up to 65,536 stack entries for a full-canvas flood. Should be a proper scanline collector like FillTool's intended design.

5. 

CircleTool
 allocates a HashSet on every 

DrawCircle
 call (Low severity — perf + correctness)
Location: 

Core/Tools.cs
 — Lines 520, 544–556

csharp
HashSet<(int, int)> points = new(); // ← allocated every mouse move!
During 

OnMouseMove
, this is called every frame while dragging. The HashSet is created and discarded on every pixel move. Extract it to the class level and .Clear() it instead.

Also, the filled circle uses Math.Pow(...) in a double loop which is a floating-point performance hit:

csharp
// Current (slow):
if (Math.Pow(cx - x0, 2) + Math.Pow(cy - y0, 2) <= r * r)
// Fix (fast):
int dx2 = cx - x0, dy2 = cy - y0;
if (dx2 * dx2 + dy2 * dy2 <= r * r)
6. SelectionManager.UpdateMovePosition allocates a new _backgroundPixels array every drag frame (Low-Medium severity)
Location: 

Core/SelectionManager.cs
 — Line 166

csharp
_backgroundPixels = new PixelColor[h, w]; // ← new allocation every mouse-move frame!
This causes GC pressure during every drag. Since the selection size doesn't change during a move, _backgroundPixels should only be allocated once in 

StartMove
 and reused.

7. GridColorBrush / 

CheckerboardBrush
 create new brush instances on every property read (Low severity)
Location: 

ViewModels/MainViewModel.cs
 — Lines 137–142

csharp
public SolidColorBrush GridColorBrush => new SolidColorBrush(GridColor); // new on every read!
public Brush CheckerboardBrush => CreateCheckerboardBrush(...);           // new on every read!
Every XAML binding cycle creates a new SolidColorBrush / DrawingBrush. These should be cached and only rebuilt when the source color actually changes (using partial void OnGridColorChanged).

8. Layer.Clear() uses a double loop instead of Array.Clear (Minor)
Location: 

Core/Layer.cs
 — Lines 61–66

csharp
// Current:
for (int y = 0; y < Height; y++)
    for (int x = 0; x < Width; x++)
        _pixels[y, x] = PixelColor.Transparent;
// Fix: much faster
Array.Clear(_pixels); // clears all bytes to zero (PixelColor.Transparent == all zeros)
This works because 

PixelColor
 is a struct with all-zero bytes being Transparent (A=0).

9. 

MergeDown
 triggers 

PixelChanged
 for every pixel (undo recording overhead) (Low severity)
Location: 

Core/PixelCanvas.cs
 — Line 112


MergeDown
 calls bottom.SetPixel(cx, cy, blended) which fires 

PixelChanged
 for every non-transparent pixel. Since 

MergeDown
 isn't wrapped in an undo transaction, these pixel change events are all silently dropped by 

RecordPixelChange
 (since _currentTransaction is null). However, the event still fires and does unnecessary work.

10. FileService.ExportToPng creates TransformedBitmap then immediately discards it (Minor code smell)
Location: 

Services/FileService.cs
 — Lines 113–115

csharp
finalSource = new TransformedBitmap(writeableBitmap, scaleTransform); // set...
// ...but then OVERWRITTEN by scaledBitmap below
byte[] scaledBuffer = new byte[...];
// ...manual pixel copy...
finalSource = scaledBitmap; // the TransformedBitmap was pointless!
finalSource is overwritten immediately by the manual scaled bitmap. The TransformedBitmap line is dead code and wastes an allocation. Remove it.

11. 

ZoomAtCursor
 uses linear zoom increments instead of indexed zoom levels (UX issue)
Location: 

ViewModels/MainViewModel.cs
 — Line 466

csharp
int newZoom = Math.Clamp(Zoom + (delta > 0 ? 1 : -1), 1, 64); // +1/-1 pixel
This means scrolling from zoom=1 to zoom=64 requires 63 scroll events. At low zoom levels it feels sluggish; at high zoom levels, each step is huge. It should snap through ZoomLevels = { 1, 2, 4, 8, 16, 24, 32, 48, 64 }, which already exists but isn't used here.

⚡ Performance Enhancements
12. 

FlattenToBuffer
 alpha blending uses double math per-pixel (High impact)
Location: 

Core/PixelCanvas.cs
 — Lines 164–182

csharp
var srcAlpha = src.A * opacity / 255.0;  // double division every pixel
For pixel art at 32×32 with 3 layers, that's ~3,000 double multiplications per frame. Consider using fixed-point integer arithmetic (multiply by 256 instead of dividing by 255.0), which is 5-10× faster:

csharp
// Fixed-point fast path (256 instead of 255 for bit-shift)
int srcA = (int)(src.A * layer.Opacity);         // 0–255 range
int invA = 255 - srcA;
buffer[offset]     = (byte)((src.B * srcA + buffer[offset]     * invA) >> 8);
buffer[offset + 1] = (byte)((src.G * srcA + buffer[offset + 1] * invA) >> 8);
buffer[offset + 2] = (byte)((src.R * srcA + buffer[offset + 2] * invA) >> 8);
buffer[offset + 3] = (byte)Math.Min(255, buffer[offset + 3] + srcA);
13. 

RefreshGridOverlay
 creates w + h - 2 POCO objects every time grid toggles (Medium impact at large canvas sizes)
Location: 

ViewModels/MainViewModel.cs
 — Lines 254–264

For a 256×256 canvas, 

RefreshGridOverlay()
 creates 510 

GridLineSegment
 records and adds them to an ObservableCollection, triggering 510 CollectionChanged events. This should either use:

ObservableCollection.AddRange (via SuspendNotifications)
Or replace with a custom DrawingContext approach drawn directly in the View's canvas overlay
14. 

UpdateBitmap()
 called after every 

HandleMouseMove
 when drawing (Medium impact)
Location: 

ViewModels/MainViewModel.cs
 — Lines 741–744

There's no throttle on how often 

UpdateBitmap()
 is called during a mouse drag. On a fast mouse, this can call 

FlattenToBuffer
 200+ times per second. A simple throttle (e.g., limit to 60fps via a DispatcherTimer or timestamp check) would cap CPU usage without visible quality loss.

15. Layer.Clone() uses a double loop instead of Buffer.BlockCopy (Minor)
Location: 

Core/Layer.cs
 — Lines 80–82

csharp
// Current (slow):
for (int y = 0; y < Height; y++)
    for (int x = 0; x < Width; x++)
        clone._pixels[y, x] = _pixels[y, x];
Since 

PixelColor
 is a 4-byte struct stored row-major in a 2D array, you can use Buffer.BlockCopy after getting the underlying flat storage via System.Runtime.InteropServices / unsafe copy, or simply expose a span. A workaround is to use Array.Copy on the flattened equivalent.

💡 Novel UX / Architecture Ideas
16. Dirty-Region Rendering (Novel — High Impact)
Instead of calling 

FlattenToBuffer
 for the entire canvas on every pixel change, maintain a HashSet<int> _dirtyRows (set by 

PixelChanged
). Then 

UpdateBitmap()
 only re-flattens and WritePixels the dirty rows, not the whole canvas. For typical brush strokes (1-3 pixels changed), this would be ~100× faster rendering updates.

csharp
// On PixelChanged: _dirtyRows.Add(y);
// In UpdateBitmap: only re-render dirty rows, use overload WritePixels(sourceRect, ...)
17. INotifyPropertyChanged batching (Novel — UX Smoothness)
Currently, every SetPixel → PixelChanged → RecordPixelChange causes no UI churn during a stroke (which is good). But 

UpdateBitmap()
 is called synchronously on the UI thread. Moving the WriteableBitmap update to an async Dispatcher queue (with coalescing) would keep the UI thread free for input during heavy operations.

18. Tool Cursor Preview Layer (Novel — UX)
Python v2.9 has a rich tool cursor preview system (spray radius ring, dither checkerboard preview, brush size indicator). The WPF port has no cursor preview. A lightweight approach: render a tool preview Adorner that sits on top of the 

CanvasImage
 in screen space. This avoids touching the pixel buffer and is instant (no re-render needed).

19. Palette Name De-duplication is one-way (Minor UX)
Location: 

Services/PaletteLoader.cs
 — Line 93

The seen set prevents duplicate names but silently skips the duplicate file rather than giving it a 

(2)
 suffix like the Python version does (Name (2), Name (3)). For a user who has similarly-named palette files, one will be silently dropped.

20. Missing: 

SelectPaletteColor
 auto-activating brush feels aggressive (UX opinion)
Location: 

ViewModels/MainViewModel.cs
 — Line 419

csharp
CurrentTool = BrushTool; // Force-switches to brush on palette click
Clicking a palette color while the Circle or Line tool is active switches the user away mid-workflow. Consider only auto-switching when 

CurrentTool
 is already 

EyedropperTool
.

📋 Summary Table
#	Issue	File	Severity	Type
1	Undo stack O(n) due to List.Insert(0)	

UndoManager.cs
🔴 Medium	Bug
2	Escape/Delete clears pixels without undo	

MainViewModel.cs
🔴 Medium	Bug
3	FillTool: O(n²) stack duplicates	

Tools.cs
🔴 Medium	Bug+Perf
4	MagicWand: same BFS overflow risk	

Tools.cs
🟡 Low	Bug+Perf
5	CircleTool: HashSet alloc per frame + Math.Pow	

Tools.cs
🟡 Low	Perf
6	SelectionManager: background array reallocated per drag frame	

SelectionManager.cs
🟡 Medium	Perf
7	GridColorBrush creates new brush on every property read	

MainViewModel.cs
🟡 Low	Perf
8	Layer.Clear() slow double loop	

Layer.cs
🟢 Minor	Perf
9	MergeDown fires PixelChanged unnecessarily	

PixelCanvas.cs
🟢 Minor	Perf
10	Dead TransformedBitmap allocation in export	

FileService.cs
🟢 Minor	Bug
11	ZoomAtCursor ignores ZoomLevels array	

MainViewModel.cs
🟡 Medium	UX
12	FlattenToBuffer: slow double-precision alpha blend	

PixelCanvas.cs
🔴 High	Perf
13	RefreshGridOverlay: 500+ ObservableCollection events	

MainViewModel.cs
🟡 Medium	Perf
14	No render throttle on mouse drag	

MainViewModel.cs
🟡 Medium	Perf
15	Layer.Clone slow double loop	

Layer.cs
🟢 Minor	Perf
16	Dirty-region rendering	

PixelCanvas
+VM	🟢 Novel	Novel
17	Async bitmap write with batching	

MainViewModel.cs
🟢 Novel	Novel
18	Tool cursor preview Adorner layer	View layer	🟢 Novel	Novel UX
19	Palette de-duplication skips silently	

PaletteLoader.cs
🟢 Minor	Bug
20	Palette click always forces Brush tool	

MainViewModel.cs
🟢 Minor	UX
---

## ✅ Implementation Status (February 25, 2026 — Audited)

**Status: ✅ 17 of 20 items IMPLEMENTED — Audit verified.**

| # | Status | Notes |
|---|--------|-------|
| 1 | ✅ Fixed | `LinkedList<T>` replaces `List<T>` |
| 2 | ✅ Fixed | Escape/Delete/Cut wrapped in undo transactions (**Cut fix confirmed in audit — was previously missed**) |
| 3 | ✅ Fixed | Boundary-seeding scanline fill |
| 4 | ✅ Fixed | MagicWand upgraded to scanline flood |
| 5 | ✅ Fixed | Class-level HashSet + integer multiply |
| 6 | ✅ Fixed | Array reused during drag |
| 7 | ✅ Fixed | Brushes cached with null-coalescing |
| 8 | ✅ Fixed | `Array.Clear` native memset |
| 9 | ✅ Fixed | `SetPixelRaw` in MergeDown |
| 10 | ✅ Fixed | Dead code removed |
| 11 | ✅ Fixed | ZoomLevels array snapping |
| 12 | ✅ Fixed | Integer-only bit-shift alpha blend |
| 13 | ✅ Fixed | Grid overlay: collection-swap batching (1 notification vs 510) |
| 14 | ✅ Fixed | Render throttle: 60fps timestamp gate in HandleMouseMove |
| 15 | ✅ Fixed | `Array.Copy` native memcpy |
| 16 | 🔲 Future | Dirty-region rendering (Novel — major architectural change) |
| 17 | 🔲 Future | Async bitmap batching (Novel — requires dispatcher refactor) |
| 18 | 🔲 Future | Tool cursor Adorner (Novel UX — requires new View-layer code) |
| 19 | ✅ Fixed | Palette dedup with `(2)` suffix |
| 20 | ✅ Fixed | Palette click only switches from Eyedropper |

**Audit Notes (February 25, 2026):**
- **Bug #2 (Cut)**: Original fix session marked Cut as fixed, but the `UndoManager.BeginTransaction/EndTransaction` wrap was missing from `Cut()`. Fixed in audit.
- **#13 (Grid batching)**: `RefreshGridOverlay` now builds lines into a new `ObservableCollection` and assigns it in a single `PropertyChanged` notification. For a 256×256 canvas this reduces 510 individual `CollectionChanged` events to 1.
- **#14 (Render throttle)**: `HandleMouseMove` now uses `Environment.TickCount64` to cap `UpdateBitmap()` calls to ~60fps during mouse drag. `HandleMouseUp` always renders the final frame.
- **#16–18 remain Future**: These are novel architectural and UX features requiring significant new code (dirty-region tracking, async dispatcher queue, Adorner layer). They don't fix bugs — they're enhancement opportunities.

**Build:** `dotnet build` — ✅ Succeeded (0 errors, 0 warnings)
**Version bumped to:** 0.2.3