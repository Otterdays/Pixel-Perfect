# Pixel Perfect - Development Scratchpad

**Last Updated**: February 19, 2026  
**Current Version**: 2.9.0  
**Status**: Production Ready - Canvas Expanded

---

## Version 2.9.0 - Canvas Expanded (February 19, 2026)
**Status**: ✅ COMPLETE

### 📐 Bigger Canvas Sizes
- **128×128 (HUGE)**: For scene tiles and large sprites
- **256×256 (MASSIVE)**: For full scenes and sprite sheets
- Auto zoom adjustment (4x for 128, 2x for 256) on preset selection
- Custom size dialog already supports up to 512×512

### ⚡ Pillow Image Rendering (Performance Overhaul)
- **Replaced per-pixel tkinter rectangles with Pillow Image compositing**
- Old method: Created ~65,536 canvas items at 256×256 (unusable)
- New method: Builds single PIL Image → NEAREST resize → single canvas item
- **Also upgraded**: Onion skin rendering and tile preview use Pillow images
- Transparent pixels preserved via RGBA mode
- Move/rotate exclusion masks applied via numpy slicing (no loops)

### 🖼️ Reference Image Panel (New Feature!)
- **Load any image** (PNG, JPG, BMP, GIF, WEBP) as reference
- **Adjustable opacity** (10% to 100% slider)
- **Fit / Fill modes** for display scaling
- **Drag to pan**, scroll wheel to zoom, double-click to reset
- **Collapsible section** in right panel (starts collapsed)
- **Keyboard shortcut**: `Shift+R` to toggle visibility
- Located below layers/timeline in right sidebar

### 🖱️ Right-Click Camera Pan
- **Right-click + hold + drag** = pan the camera view (same as middle mouse)
- **Right-click + release** (no drag) = open context menu as before
- 5px drag threshold distinguishes pan from click
- Edge tool / Eraser right-click behavior unchanged
### 🔍 Mini Preview Window (Aseprite-Style)
- **Bottom-right overlay** shows full canvas fitted into 128px preview
- Checkerboard transparency background
- Dark frame with "Preview" title bar
- Viewport rectangle shows currently visible area when zoomed in
- `Shift+P` toggles visibility
- Starts visible by default

### 🪙 3D Token Preview (NEW)
- **Software voxel renderer** — zero new dependencies (Pillow + numpy only)
- Interactive 3D coin/medallion of current pixel art
- **Drag to rotate**, scroll to zoom, double-click to reset
- **Thickness slider** (1-8 layers), **Light angle** (0-360°)
- **Material presets**: Flat, Gold, Silver, Bronze
- **Back face modes**: Same, Mirrored, Embossed, Blank
- **Auto-spin toggle** with 30fps rotation
- **Export**: PNG (512px) and GIF (360° animation, 36 frames)
- `Shift+T` toggles panel visibility
- Collapsible right-sidebar panel (starts collapsed)
- **Auto-updates**: Debounced sync with canvas pixel changes

### 🤖 Godot Engine Export (NEW)
- **Problem**: Godot blurs pixel art by default and needs specific sprite sheet formatting (zero spacing)
- **Solution**: Automated export pipeline that generates Godot-ready assets
- **Features**:
  - `export_godot_sheet()`: Zero-spacing sprite sheet + .tres resource
  - Auto-generated `GODOT_IMPORT_README.txt` with optimal settings
  - .tres files define `AtlasTexture` regions for each frame
  - .tscn files create ready-to-use `AnimatedSprite2D` nodes
  - Uses `NEAREST` filtering for all scaling

### 📁 Files Created
- `src/core/voxel_renderer.py` – Software 3D voxel engine
- `src/ui/token_preview_panel.py` – Token preview panel UI
- `src/ui/reference_panel.py` – Reference Image Panel class
- `src/utils/godot_export.py` – Godot export generator
- `DOCS/features/GODOT_EXPORT.md` – Godot integration spec
- `DOCS/features/AI_FEATURES.md` – AI features roadmap
- `DOCS/features/3D_TOKEN_PREVIEW.md` – 3D token implementation plan

### 📁 Files Modified
- `src/utils/export.py` – Added Godot export format
- `src/core/canvas.py` – Added HUGE (128×128) and MASSIVE (256×256) to CanvasSize enum
- `src/core/canvas_renderer.py` – Pillow rendering, mini preview, token preview notification
- `src/ui/ui_builder.py` – Added 128×128 and 256×256 to size dropdown
- `src/ui/canvas_zoom_manager.py` – Size map, zoom auto-adjustment for larger canvases
- `src/ui/main_window.py` – Integrated ReferencePanel and TokenPreviewPanel
- `src/core/event_dispatcher.py` – Shift+R, Shift+P, Shift+T shortcuts, right-click pan

---

## Version 2.7.8 - Workflow Enhancements (January 25, 2026)
**Status**: ✅ COMPLETE

### ⚡ QoL Improvements
- **Middle Mouse Pan**: Pan the canvas by holding the middle mouse button (wheel click).
- **Tab Panel Toggle**: Press `Tab` to toggle all panels (Maximize Canvas), `Shift+Tab` to toggle left panel only.
- **Roadmap Expansion**: Added 50+ new features to `polish_next_up.md` to guide future development.

### 📁 Files Modified
- `src/core/event_dispatcher.py` – Added Tab key handler and Middle Mouse event handlers.
- `polish_next_up.md` – Major expansion of feature roadmap.

---

## Version 2.7.7 - Right-Click Context Menu & Copy/Paste Shortcuts (January 25, 2026)
**Status**: ✅ COMPLETE

### 🖱️ Right-Click Context Menu (New Feature!)
- **Context-Aware Menu**: Right-click on canvas shows relevant actions based on current tool and state
- **Selection Operations**: Copy, Cut, Delete, Mirror, Rotate, Scale (when selection exists)
- **Paste Support**: Paste option appears when copy buffer has content
- **Tool-Specific Actions**: Fill Here, Eyedropper, tool switching
- **Canvas Operations**: Zoom Fit, Zoom 100%, Toggle Grid, Toggle Tile Preview
- **Smart Filtering**: Menu only shows relevant options (no empty sections)
- **Edge/Eraser Exclusion**: Context menu doesn't interfere with edge/eraser right-click functionality

### ⌨️ Copy/Paste Keyboard Shortcuts (New Feature!)
- **Ctrl+C**: Copy selection
- **Ctrl+V**: Paste copied selection (enters placement mode)
- **Ctrl+X**: Cut selection (copy + delete)
- **Delete/Backspace**: Delete selection
- **Undo Support**: All operations properly save undo state
- **Visual Feedback**: Paste uses existing copy preview system

### 📁 Files Created
- `src/ui/context_menu_manager.py` – Context menu system (260+ lines)

### 📁 Files Modified
- `src/core/event_dispatcher.py` – Added context menu trigger, keyboard shortcuts (Ctrl+C/V/X, Del)
- `src/ui/main_window.py` – Integrated context menu manager

---

## Version 2.7.6 - Theme Customization System (January 25, 2026)
**Status**: ✅ COMPLETE

### 🎨 Theme Customization Screen (New Feature!)
- **Full Color Customization**: Customize all 20+ theme color properties with visual color pickers
- **Live Preview**: See changes in real-time as you adjust colors
- **Save Custom Themes**: Save your custom themes with custom names
- **Export/Import**: Export themes to JSON files and import from other users
- **Persistent Storage**: Custom themes saved to user storage (AppData/PixelPerfect/themes/)
- **Theme Integration**: Custom themes automatically appear in theme dropdown
- **Reset Functionality**: Reset to original theme at any time
- **Organized UI**: Color properties grouped by category (Background, Text, Buttons, Canvas, etc.)

### 📁 Files Created
- `src/ui/theme_customizer.py` – Complete theme customization system (600+ lines)

### 📁 Files Modified
- `src/ui/theme_dialog_manager.py` – Added "Customize Theme" button to settings dialog
- `src/ui/main_window.py` – Integrated theme customizer, loads custom themes on startup

---

## Version 2.7.5 - Tile Preview & Fullscreen Mode (January 25, 2026)
**Status**: ✅ COMPLETE

### 🖼️ Tile Preview Mode (New Feature!)
- **3x3 Repeating Grid**: Canvas repeated around itself for pattern/tile visualization
- **Ghost tiles**: Surrounding tiles drawn at 50% opacity with stipple effect
- **Performance optimized**: Only draws tiles visible in viewport, uses NumPy for efficient pixel lookup
- **Toolbar button**: "Tile" button toggles ON/OFF with green highlight when active
- **Cyan border**: Center tile (your canvas) highlighted with dashed cyan border
- **Use case**: Perfect for game tiles, textures, repeating patterns, and building pieces

### ⛶ Fullscreen Mode (New Feature!)
- **F11 toggle**: Press F11 to enter/exit true fullscreen mode
- **Escape to exit**: Press Escape to exit fullscreen (before other escape actions)
- **Auto-redraw**: Canvas automatically redraws after fullscreen toggle
- **Distraction-free**: Full screen coverage for focused pixel art work

### 📁 Files Modified
- `src/core/canvas.py` – Added `show_tile_preview` state
- `src/core/canvas_renderer.py` – Added `draw_tile_preview()` method
- `src/ui/grid_control_manager.py` – Added tile preview toggle and button management
- `src/ui/ui_builder.py` – Added "Tile" button to toolbar
- `src/ui/main_window.py` – Wired up tile preview callback and button reference, added fullscreen toggle
- `src/core/event_dispatcher.py` – Added F11 and Escape keybinds for fullscreen

---

## Version 2.7.3 - Theme, Tools & UI Polish (January 22, 2026)
**Status**: ✅ COMPLETE

- **Claude theme**: Bright Anthropic-inspired theme (warm cream, coral accents).
- **Dither preview**: Canvas checkerboard preview at cursor; spray preview unchanged.
- **Eraser right-click**: Delete edge lines (click or drag); uses Edge tool storage.
- **Panel buttons**: Minimalistic ‹/› chevrons, transparent + hover; restore buttons minimal, centered.
- **Canvas recenter fix**: Redraw on panel *expand* (not just collapse) so grid stays centered.

---

## Version 2.7.1 - Tool & Undo System Improvements (January 1, 2026)
**Status**: ✅ COMPLETE - New tool and critical fixes

### 🏁 Dither Tool (New Feature!)
- **New `dither.py`**: Checkerboard pattern brush tool
- **Classic technique**: Essential for retro shading and texturing
- **Dual mode**: Left-click to draw pattern, Right-click to erase
- **Undo/Redo support**: Fully integrated with the undo system

### 🔧 Undo System Fixes
- **Brush Undo Fix**: Resolved issue where undoing a brush stroke didn't restore transparent pixels (merged instead of replaced).
- **Edge Tool Undo Support**: Added state tracking for Edge Tool lines (previously ignored by undo system).
- **Snapshot Logic Update**: `UndoManager.save_state()` now correctly handles transparency for full snapshots.

### 🐛 Bug Fixes
- **Edge Tool State**: Fixed `EdgeTool` integration with `EventDispatcher` to ensure state is saved before drawing.
- **Layer Compositor Caching**: Disabled caching that was too aggressive and caused selection/undo issues.
- **Edge Lines During Move**: Fixed edge lines outside selection disappearing during move operations.

### 🟡 Known Minor Issues
- **Move Preview Glitches**: Ghost pixels at original position during drag (see ISSUES.md #4)

---

## Version 2.7.0 - Advanced Features & Memory Optimization (January 1, 2026)
**Status**: ✅ COMPLETE - New features, architectural improvements, and critical bug fixes

### 🧠 Delta-Based Undo System (95% Memory Reduction)
- **Complete refactor of `undo_manager.py`**: Now stores only changed pixels instead of full canvas copies
- **New classes**: `UndoDelta`, `DeltaTracker` for efficient change tracking
- **Memory savings**: From ~16KB per action (64x64 canvas) to ~2KB per action (typical stroke)
- **Increased limit**: Now supports 100 undo states (up from 50) due to smaller memory footprint
- **Backwards compatible**: Legacy `save_state()` still works for existing integrations

### ⚡ Scanline Flood Fill (5-20x Faster)
- **Optimized `fill.py`**: Replaced naive stack-based algorithm with scanline approach
- **Batch operations**: Fills entire horizontal lines at once using NumPy slicing
- **Smart span detection**: Only adds seed points at span boundaries, reducing stack operations
- **Visible improvement**: Large fill areas now complete nearly instantly

### 🎨 Recent Colors Palette (New Feature!)
- **New `recent_colors.py`**: Tracks last 16 colors used while drawing
- **Automatic tracking**: Colors added to recent list when drawing starts
- **Persistent storage**: Saves to user's AppData/PixelPerfect folder between sessions
- **New UI view**: "Recent" radio button in palette panel shows 4x4 color grid
- **Click to select**: Clicking a recent color selects it and switches to brush tool
- **Clear button**: Option to clear recent colors history

### ⚡ Event Throttling System
- **New `event_throttle.py`**: Utility classes for throttling high-frequency events
- **`EventThrottler`**: Limits function calls to specified interval (~120 FPS default)
- **`CanvasEventOptimizer`**: Smart mouse move handling with position deduplication
- **Integration**: EventDispatcher uses throttled position tracking for preview updates
- **Result**: Reduced CPU usage during rapid mouse movements

### 🗄️ Layer Compositor Caching (v2.7.4 - Re-enabled with Smart Detection)
- **`LayerManager` caching**: Stores flattened composite, avoids redundant blending
- **Smart change detection**: Multi-factor validation system:
  - Version counters track explicit modifications (`set_pixel()`, `clear()`, `mark_modified()`)
  - Pixel hashes detect direct array modifications (`layer.pixels[y, x] = color`)
  - Visibility/opacity state tracking
  - Layer count monitoring
- **`invalidate_cache()`**: Called automatically when layers are modified through tracked methods
- **`_is_cache_valid()`**: Comprehensive validation that catches all change paths
- **Automatic invalidation**: Works even when tools modify pixels directly without going through tracked methods
- **Dirty region tracking**: Foundation for future incremental updates (currently full invalidation)

### 📁 New Files Created
- `src/core/recent_colors.py` - RecentColorsManager class
- `src/ui/palette_views/recent_view.py` - UI component for recent colors
- `src/core/event_throttle.py` - Throttling and rate limiting utilities

---

## Version 2.6.2 - Performance Optimizations (January 1, 2026)
**Status**: ✅ COMPLETE - Major rendering and selection speed improvements

### 🚀 Rendering Optimizations
- **`draw_all_pixels_on_tkinter()`**: Now uses NumPy `np.where()` to find non-transparent pixels instead of iterating over all canvas pixels. Dramatically faster for sparse canvases.
- **`flatten_layers()`**: Vectorized alpha blending using NumPy operations instead of nested Python loops. ~10-50x faster for multi-layer compositions.
- **`update_single_pixel()`**: Added note for future incremental update implementation (currently triggers full redraw as safety measure).

### 🎨 Selection/Transform Optimizations
- **`_simple_scale()`**: Uses NumPy fancy indexing for nearest-neighbor scaling instead of nested loops.
- **`preview_scaled_pixels()`**: Vectorized scaling preview with NumPy coordinate grids.
- **`mirror_selection()`**: Now uses `np.where()` to iterate only over non-transparent pixels.
- **`apply_rotation()`**: Vectorized pixel clearing and placement using NumPy masks.

### 🖱️ Event Handling Optimizations
- **`on_tkinter_canvas_mouse_move()`**: Added early-exit caching to skip redundant preview draws when mouse hasn't moved to a new canvas pixel coordinate.

### 🧹 Code Cleanup
- **Removed debug prints**: `brush.py` (2 prints), `selection_manager.py` (1 print)
- **Consolidated update calls**: `loading_screen.py` - reduced redundant `update_idletasks()` calls

### 📊 Expected Improvements
- Brush strokes: Smoother on large canvases
- Selection scaling: Much faster preview during drag
- Mirror/Rotate: Faster transformation application
- Mouse move: Reduced CPU overhead for cursor previews

---

## Version 2.6.1 - Code Cleanup & Refactor (December 3, 2025)
**Status**: ✅ COMPLETE - Removed dead code, cleaned debug prints, compacted documentation

### 🧹 Cleanup Summary
- **Removed dead fallback code** from `main_window.py` (~100 lines)
  - `_initialize_all_views()` fallback after manager delegation
  - `_show_view()` fallback after manager delegation
- **Cleaned debug print statements** (~150+ lines across 4 files)
  - `loading_screen.py`: Removed 75 debug prints
  - `main_window.py`: Removed 41 debug prints
  - `window_state_manager.py`: Removed 23 debug prints
  - `selection.py`: Removed 12 debug prints
- **Compacted SCRATCHPAD.md** per project rules (never delete, only compact)
  - v2.5+ entries kept in full detail
  - v2.0-2.4 entries summarized
  - v1.x entries archived as historical summary

### 📊 Results
- **main_window.py**: 1,493 → ~1,380 lines (cleaner orchestration)
- **loading_screen.py**: 443 → 290 lines (production-ready)
- **window_state_manager.py**: 451 → 285 lines (cleaner state management)
- **SCRATCHPAD.md**: 6,058 → ~400 lines (focused context)

---

## Version 2.6.0 - Spray Tool & Palette Overhaul (November 13, 2025)
**Status**: ✅ COMPLETE - Added spray paint workflow, zoom scrollbar, and JSON palette pipeline

### ✒️ Spray Tool Implementation
- **ToolSizeManager** got `spray_radius` + `spray_density` with right-click menu options (4→24 radius, Low→Ultra density).
- EventDispatcher handles drag loops so droplets stream continuously while button held.
- CanvasRenderer draws spray cursor preview so artists see coverage before committing.

### 🧭 Canvas Zoom Scrollbar
- New `CanvasScrollbar` overlay renders +/− buttons and draggable handle on the canvas edge.
- Scroll wheel events feed through the scrollbar to keep dropdown, wheel, and handle synchronized.
- Theme-aware colors so Basic Grey and Angelic stay consistent.

### 🎨 Palette Loader Refactor
- `ColorPalette` now auto-scans `assets/palettes/*.json`, caches name→path, and loads via `load_by_name`.
- UIBuilder populates palette dropdown directly from discovered JSON names; SNES Classic remains fallback.
- Added `assets/palettes/grass.json` (16 earthy greens) as reference palette.

---

## Version 2.5.15 - Ghost Pixels FINAL FIX (October 18, 2025)
**Status**: ✅ COMPLETE - Fixed the real root cause of ghost pixels after mirror/rotate operations

### 🐛 The Real Issue
**Problem**: The MOVE tool's `finalize_move()` method was using `selected_pixels` to determine which pixels to clear from the original position. After mirroring/rotating, `selected_pixels` contains the **transformed version**, not the **original version**.

### 🔧 The Fix
Modified `finalize_move()` to **refresh the original pixels from the layer** before clearing, ensuring we clear the **actual pixels** that were at the original position.

---

## Version 2.5.14 - Debug System Implementation (October 18, 2025)
**Status**: ✅ COMPLETE - Added comprehensive debug system for mirror/rotate operations

Implemented debug tracking system with 20+ debug statements for pixel operation tracking. Created `DEBUG_LOCATIONS.md` for documentation.

---

## Version 2.5.13 - Mirror & Rotate Ghost Pixels Fix (October 18, 2025)
**Status**: ⚠️ PARTIAL - Initial fix attempted but ghost pixels still occurring

Fixed both `mirror_selection()` and `apply_rotation()` to follow the same two-step pattern as `MoveTool.finalize_move()`: clear original non-transparent pixels first, then place only non-transparent transformed pixels.

---

## Version 2.5.12 - Primary Color Variations Highlighting Fix (January 2025)
**Status**: ✅ COMPLETE - Fixed Primary color variations highlighting with proper visual feedback

Fixed widget reference errors, hover effect conflicts, and improved visual feedback for color variation selection.

---

## Version 2.5.11 - Primary Color Variations Highlighting Fix (January 2025)
**Status**: ✅ COMPLETE - Fixed Primary color variations not showing selection highlighting

Added white border highlighting for selected color variations with proper visual feedback system.

---

## Version 2.5.10 - Saved Colors Auto-Selection Fix (January 2025)
**Status**: ✅ COMPLETE - Fixed saved colors not becoming active brush color after saving

Saving colors now immediately selects them as the current brush color.

---

## Version 2.5.9 - Primary Colors Centering Fix (January 2025)
**Status**: ✅ COMPLETE - Fixed Primary colors grid centering

Added `grid_columnconfigure` to properly center columns within container.

---

## Version 2.5.8 - Grid and Wheel Color Saving Fix (January 2025)
**Status**: ✅ COMPLETE - Fixed Grid and Wheel colors not saving to Saved Colors palette

Fixed `get_source_color()` method to use `last_active_view` when in saved mode.

---

## Version 2.5.7 - Primary Color Selection TypeError Fix (January 2025)
**Status**: ✅ COMPLETE - Fixed TypeError when selecting colors in Primary palette view

Fixed `primary_view.py` to pass color indices instead of color tuples to callback.

---

# Historical Version Summary (v2.0 - v2.4)

## v2.2.x Series (October 2025)
- **v2.2.4**: Fixed pixel duplication when moving selection multiple times
- **v2.2.3**: Fixed pixels being deleted underneath when moving selection
- **v2.2.2**: Loading screen overlay positioning fix
- **v2.2.1**: Loading screen flash fix
- **v2.2.0**: Major modular refactor complete (65.1% reduction in main_window.py)

## v2.1.x Series (December 2024)
- **v2.1.0**: Import PNG Dialog with spinning preview

## v2.0.x Series (December 2024)
- **v2.0.9**: Scroll wheel zoom & draggable scrollbar
- **v2.0.0**: Fixed saved colors blank space UI bug

---

# Historical Version Summary (v1.x)

## Major Milestones

### Architecture & Refactoring (v1.62-1.69)
- Extracted 12 manager classes from main_window.py
- Reduced main_window.py from 3,387 to ~1,180 lines (65% reduction)
- Created modular architecture with dedicated managers for:
  - FileOperationsManager, DialogManager, SelectionManager
  - ToolSizeManager, CanvasZoomManager, GridControlManager
  - CanvasOperationsManager, LayerAnimationManager, ColorViewManager

### UI/UX Improvements (v1.40-1.55)
- Panel loading indicators
- Panel toggle performance optimization (200x faster)
- Responsive panel sizing based on screen resolution
- Theme system with Basic Grey, Angelic, and American themes
- Collapsible panels with restore buttons

### Tools & Features (v1.30-1.42)
- Multi-size brush (1x1, 2x2, 3x3) with right-click menu
- Multi-size eraser (1x1, 2x2, 3x3)
- Texture tool with live preview
- Smart non-destructive move system
- Live shape preview for line/rectangle/circle
- Settings button placeholder (127 settings planned)

### Color System (v1.07-1.33)
- Color wheel with HSV picker
- Saved colors system (24 slots with export/import)
- Custom colors (32 persistent user colors)
- 50-100x faster view switching with pre-rendered views
- Primary colors with 24 variations per color

### Canvas & Export (v1.11-1.30)
- 64x64 canvas size support
- 64x zoom level
- Canvas downsize warning system
- Build size optimization (330MB → 29MB, 91% reduction)
- PNG/GIF/Spritesheet export

### Selection & Layers (v1.16-1.37)
- Selection tool with marching ants
- Move tool with background preservation
- Mirror, rotate, copy, scale operations
- Layer system with visibility/opacity controls

---

# Project Architecture Reference

## Manager Classes (12 Total)
1. **UIBuilder** (485 lines) - Toolbar and UI component construction
2. **EventDispatcher** (682 lines) - All mouse/keyboard event routing
3. **FileOperationsManager** (415 lines) - File I/O operations
4. **DialogManager** (396 lines) - Custom dialog windows
5. **SelectionManager** (626 lines) - Selection transformations
6. **CanvasRenderer** (780 lines) - All rendering operations
7. **ToolSizeManager** (288 lines) - Brush/eraser/spray size management
8. **CanvasZoomManager** (226 lines) - Canvas resizing and zoom
9. **GridControlManager** (115 lines) - Grid visibility controls
10. **CanvasOperationsManager** (144 lines) - Coordinate conversion, panel sizing
11. **LayerAnimationManager** (197 lines) - Layer operations, animation timeline
12. **ColorViewManager** (193 lines) - Color view switching, color wheel

## Key Technical Decisions
- **Callback pattern** for manager communication (keeps code decoupled)
- **Pre-rendered views** for instant palette switching
- **Layer-based drawing** for all tool operations
- **Theme-aware components** with real-time switching
- **Window state persistence** for user preferences

---

# Quick Reference

## File Locations
- **Main Window**: `src/ui/main_window.py`
- **Managers**: `src/ui/*.py` (12 manager files)
- **Core Systems**: `src/core/` (canvas, palette, layers, undo)
- **Tools**: `src/tools/` (13 drawing tools)
- **Documentation**: `docs/` (SUMMARY, ARCHITECTURE, CHANGELOG, etc.)

## Testing Checklist
1. Application startup (no errors, all UI visible)
2. Tool selection and operations
3. Tool size switching (1x1, 2x2, 3x3)
4. Palette view switching (Grid, Primary, Wheel, Constants, Saved)
5. File operations (New, Open, Save, Import, Export)
6. Panel toggles (collapse/expand)
7. Theme switching

## Documentation Files
- **SUMMARY.md** - Project overview and status
- **ARCHITECTURE.md** - System design and components
- **CHANGELOG.md** - Version history
- **SBOM.md** - Dependencies and security
- **REFACTOR.md** - Refactoring guide and lessons learned

---

## Active Tasks
- [x] Build roadmap checklist in `ROADMAP.md`
- [x] Implement zoom-to-cursor + fit/100%
- [x] Implement recent colors selection handling
- [x] Implement export presets + quick export
- [x] Update documentation for new QoL features
- [x] Update docs for v2.7.3 (theme, tools, UI, bugfix)

## Blocked Items
- None

## Recent Context (last 5 actions)
1. 2026-01-22: Claude theme, dither/spray preview, eraser edge delete, panel button redesign
2. 2026-01-22: Canvas grid off-center fix (redraw on panel expand)
3. 2026-01-22: Documentation update (CHANGELOG, SCRATCHPAD, SUMMARY, THEME_SYSTEM, EDGE_TOOL)
4. 2026-01-18: Zoom-to-cursor + fit/100%, export presets, quick export
5. 2026-01-18: Recent colors selection handling

## Compacted History
See entries above for detailed historical context.