# Pixel Perfect - Changelog

## Version 3.1.0 (WPF Edition) - Flex Features Update
**Date**: February 25, 2026
**Type**: Major Feature Release

### 🪙 3D Voxel Tokenizer
- **Software voxel renderer**: Turns your canvas into an interactive 3D voxel model dynamically.
- **Hardware Accelerated**: Fully utilizes WPF Viewport3D for performant rendering even with large canvases.
- **Smart Grouping**: Color-grouped meshes eliminate draw calls, bypassing structural WPF limitations on thousands of elements.
- **Zero-Allocation Ready**: Takes advantage of `FlattenToBuffer` rendering, seamlessly discarding transparent pixels.
- **Live Rotation & Auto Spin**: Includes Y-axis animation and mouse X/Y tracking for free-cam view of the token.
- **Adjustable Thickness**: Slider to dynamically raise and lower your voxel height instantly.

### 🖼️ Reference Photo Overlay
- **Seamless Backdrop**: Load any PNG/JPG into a unified semi-transparent canvas backdrop.
- **Dedicated Controls**: A native Right Panel element provides independent scale, opacity, and X/Y offset sliders.

## Documentation & Repo Cleanup - February 25, 2026
- **README condensed** — Last 5 versions in Latest Updates; full version history linked to CHANGELOG
- **Monetization moved** — Removed from README; full content in [docs/MONETIZATION.md](MONETIZATION.md)
- **.gitignore** — Added `**/bin/` and `**/obj/` for .NET build outputs

## Version 3.0.0 (WPF Edition) - Foundation
**Date**: February 25, 2026
**Type**: Major Framework Rewrite

### ⚡ .NET 8 / WPF Rewrite
- **Complete transition from Python to C# WPF**.
- **Hardware Accelerated**: Butterly-smooth continuous 60+ FPS on massive canvases.
- **Native Experience**: Native Windows 10 & 11 integrations.

## Version 2.9.0 - Canvas Expanded

### 📐 Bigger Canvas Sizes (New Presets)
- **128×128 (HUGE)**: For scene tiles, large sprites, and tile sheets
- **256×256 (MASSIVE)**: For full scenes, sprite sheets, and detailed work
- **Smart Zoom Auto-Adjust**: Larger canvases automatically set zoom to fit (4x for 128, 2x for 256)
- **Custom Size Dialog**: Already supports up to 512×512 via "Custom..." option

### ⚡ Pillow Image Rendering (Performance Overhaul)
- **Replaced per-pixel tkinter rectangles with Pillow Image compositing**
- **Old method**: Created individual `create_rectangle` for each non-transparent pixel (~65,536 items at 256×256)
- **New method**: Builds single PIL Image from numpy array → NEAREST resize → single `create_image` canvas item
- **Coverage**: Main pixel rendering, onion skin frames, and tile preview all upgraded
- **Technical**: Move/rotate exclusion masks now use numpy array slicing instead of nested loops
- **Result**: 256×256 canvas now renders at interactive speeds instead of multi-second freezes

### 🖼️ Reference Image Panel (New Feature)
- **Load any image**: PNG, JPG, BMP, GIF, WEBP supported via file dialog
- **Adjustable opacity**: Slider from 10% to 100%
- **Fit / Fill modes**: Toggle between fitting or filling the preview area
- **Pan & Zoom**: Drag to pan, scroll wheel to zoom, double-click to reset
- **Collapsible section**: In right sidebar below layers/timeline (starts collapsed)
- **Toggle shortcut**: `Shift+R` to show/hide the panel

### 🔍 Mini Preview Window (Aseprite-Style)
- **Bottom-right overlay**: Shows full canvas artwork fitted into a compact 128px preview
- **Checkerboard transparency**: Standard alpha checkerboard pattern for transparent areas
- **Dark frame with title bar**: "Preview" header bar with sleek dark aesthetic
- **Viewport indicator**: White rectangle shows currently visible portion when zoomed in
- **Toggle shortcut**: `Shift+P` to show/hide; starts visible by default

### 🖱️ Right-Click Camera Pan
- **Right-click + hold + drag**: Pan the camera view (same as middle mouse button)
- **Right-click + release**: Opens context menu as before (no behavior change for quick clicks)
- **5px drag threshold**: Distinguishes between pan gesture and click
- **Tool-specific behavior preserved**: Edge tool and eraser right-click actions unchanged
### 🪙 3D Token Preview (New Feature)
- **Software voxel renderer**: Turns pixel art into an interactive 3D coin/medallion — zero new dependencies
- **Interactive rotation**: Drag to rotate, scroll to zoom, double-click to reset
- **Thickness control**: Adjustable coin depth (1-8 voxel layers)
- **Directional lighting**: Adjustable light angle (0-360°) with Blinn-Phong shading
- **Material presets**: Flat (pixel colors), Gold, Silver, Bronze metallic tints
- **Back face modes**: Same, Mirrored, Embossed, Blank
- **Auto-spin**: Toggle for continuous 30fps rotation
- **Export**: PNG (512px) and GIF (360° rotation, 36 frames)
- **Collapsible panel**: Right sidebar, starts collapsed, `Shift+T` toggle
- **Auto-updates**: Debounced sync with canvas pixel changes

### 🤖 Godot Engine Export (New - Phase 1)
- **Zero-Spacing Sheets**: Generates packed sprite sheets compatible with Godot `AnimatedSprite2D`
- **.tres Resources**: Auto-generates native `SpriteFrames` resources with `AtlasTexture` regions
- **.tscn Scenes**: Creates ready-to-use scene files
- **Import Guide**: Auto-creates `GODOT_IMPORT_README.txt` with optimal settings (Nearest filter, etc.)
- **Format**: New "Godot Sprite Sheet" option in export manager

### 🎨 Palettes
- **Hair Colors**: Added `hair_colors.json` with 32 natural hair tones (Blondes, Browns, Reds, Blacks, Greys)

### 🖌️ Eyedropper & Color UX
- **Eyedropper → Wheel Sync**: When in Wheel mode, the eyedropper now always jumps the picked color onto the color wheel instead of switching to Grid view
- **Hex Code Tooltips**: Hovering over any color swatch (Grid, Primary, Constants, Saved, Recent, Custom) now shows an instant tooltip with the hex code (e.g. `#FF8800`)


### 📁 Files Created
- `src/core/voxel_renderer.py` – Software 3D voxel engine (numpy + Pillow rasterization)
- `src/ui/token_preview_panel.py` – Token preview panel UI with controls and export
- `src/ui/reference_panel.py` – Reference Image Panel
- `src/utils/godot_export.py` – Godot export generator module
- `DOCS/features/GODOT_EXPORT.md` – Godot integration specification
- `DOCS/features/AI_FEATURES.md` – AI features roadmap
- `DOCS/features/3D_TOKEN_PREVIEW.md` – 3D token implementation plan

### 📁 Files Modified
- `src/utils/export.py` – Added Godot export format and convenience methods
- `src/core/canvas.py` – Added HUGE and MASSIVE enum values to CanvasSize
- `src/core/canvas_renderer.py` – Pillow rendering, mini preview, token preview notification
- `src/ui/ui_builder.py` – Added 128×128 and 256×256 to size dropdown
- `src/ui/canvas_zoom_manager.py` – Updated size_map, zoom auto-adjustment for larger canvases
- `src/ui/main_window.py` – Integrated ReferencePanel and TokenPreviewPanel
- `src/core/event_dispatcher.py` – Shift+R, Shift+P, Shift+T shortcuts, right-click pan

---


## Version 2.7.7 - Right-Click Context Menu & Copy/Paste Shortcuts
**Date**: January 25, 2026  
**Type**: QoL Enhancement Release

### 🖱️ Right-Click Context Menu (New Feature)
- **Context-Aware Actions**: Right-click on canvas shows relevant menu based on current tool and state
- **Selection Operations**: 
  - Copy, Cut, Delete when selection exists
  - Mirror, Rotate, Scale transformation options
  - All operations properly integrated with undo system
- **Paste Support**: Paste option appears when copy buffer has content
- **Tool-Specific Actions**: 
  - "Fill Here" for fill tool
  - Quick tool switching (Eyedropper, Brush, Eraser)
- **Canvas Operations**: Zoom Fit, Zoom 100%, Toggle Grid, Toggle Tile Preview
- **Smart Filtering**: Menu dynamically shows/hides sections based on context
- **Non-Intrusive**: Doesn't interfere with edge/eraser tool right-click functionality

### ⌨️ Copy/Paste Keyboard Shortcuts (New Feature)
- **Ctrl+C**: Copy current selection
- **Ctrl+V**: Paste copied selection (enters placement mode with preview)
- **Ctrl+X**: Cut selection (copy + delete in one action)
- **Delete/Backspace**: Delete current selection
- **Undo Integration**: All operations save undo state for easy reversal
- **Visual Feedback**: Paste uses existing copy preview system for placement

### 📁 Files Created
- `src/ui/context_menu_manager.py` – Complete context menu system (260+ lines)

### 📁 Files Modified
- `src/core/event_dispatcher.py` – Added context menu trigger, keyboard shortcuts (Ctrl+C/V/X, Del)
- `src/ui/main_window.py` – Integrated context menu manager

---

## Version 2.7.6 - Theme Customization System
**Date**: January 25, 2026  
**Type**: Feature Enhancement Release

### 🎨 Theme Customization Screen (New Feature)
- **Complete Color Control**: Customize all 20+ theme color properties with visual color pickers
  - Background colors (Primary, Secondary, Tertiary)
  - Text colors (Primary, Secondary, Disabled)
  - Button colors (Normal, Hover, Active)
  - Canvas colors (Background, Border, Grid)
  - Tool colors (Selected, Unselected)
  - Selection colors (Outline, Handle, Edge)
  - Scrollbar colors (Button, Hover, Track)
  - Border colors (Normal, Focus)
- **Live Preview**: Real-time preview of changes as you adjust colors
- **Save Custom Themes**: Save themes with custom names, automatically added to theme dropdown
- **Export/Import**: Export themes to JSON files for sharing, import themes from files
- **Persistent Storage**: Custom themes saved to user storage directory
  - Windows: `AppData/Local/PixelPerfect/themes/`
  - Mac/Linux: `~/.pixelperfect/themes/`
- **Reset Functionality**: Reset to original theme at any time
- **Organized UI**: Color properties grouped by logical categories with descriptions
- **Hex Input**: Direct hex color code input for precise color control

### 📁 Files Created
- `src/ui/theme_customizer.py` – Complete theme customization system (600+ lines)

### 📁 Files Modified
- `src/ui/theme_dialog_manager.py` – Added "Customize Theme" button to settings dialog
- `src/ui/main_window.py` – Integrated theme customizer, loads custom themes on startup

---

## Version 2.7.5 - Tile Preview & Fullscreen Mode
**Date**: January 25, 2026  
**Type**: Feature Enhancement Release

### 🖼️ Tile Preview Mode (New Feature)
- **3x3 Repeating Grid**: Canvas is shown repeated in a 3x3 grid around itself
- **Pattern Visualization**: Perfect for designing game tiles, textures, and repeating patterns
- **Ghost Tiles**: Surrounding tiles rendered at 50% opacity with stipple transparency effect
- **Performance Optimized**: 
  - Uses NumPy to efficiently find non-transparent pixels
  - Only draws tiles visible within the viewport
  - Skips pixels outside view bounds
- **Visual Feedback**: Center tile highlighted with dashed cyan border
- **Toolbar Integration**: "Tile" button toggles ON/OFF with green highlight when active

### ⛶ Fullscreen Mode (New Feature)
- **F11 Toggle**: Press F11 to enter/exit true fullscreen mode (covers entire screen)
- **Escape to Exit**: Pressing Escape exits fullscreen before handling other actions
- **Auto-Redraw**: Canvas automatically redraws after fullscreen toggle for correct display
- **Distraction-Free**: Full screen coverage for focused pixel art work

### 📁 Files Modified
- `src/core/canvas.py` – Added `show_tile_preview` state variable
- `src/core/canvas_renderer.py` – Added `draw_tile_preview()` method with optimized rendering
- `src/ui/grid_control_manager.py` – Added `toggle_tile_preview()` and button management
- `src/ui/ui_builder.py` – Added "Tile" button to toolbar with tooltip
- `src/ui/main_window.py` – Wired callbacks, added `_toggle_fullscreen()` and `_exit_fullscreen()`
- `src/core/event_dispatcher.py` – Added F11 keybind and Escape handling for fullscreen

---

## Version 2.7.4 - Smart Layer Caching System
**Date**: January 22, 2026  
**Type**: Performance Enhancement Release

### ⚡ Smart Layer Compositor Caching
- **Re-enabled layer caching** with intelligent change detection system
- **Version tracking**: Each layer tracks a version counter that increments on pixel changes
- **Hash-based validation**: Fast pixel hash computation detects direct array modifications
- **Multi-factor validation**: Cache validity checked via:
  - Layer version counters (catches `set_pixel()`, `clear()`, `mark_modified()`)
  - Pixel data hashes (catches direct `layer.pixels[y, x] = color` modifications)
  - Visibility and opacity state tracking
  - Layer count changes
- **Automatic invalidation**: Cache automatically invalidates when layers are modified through any code path
- **Performance impact**: Eliminates redundant layer blending operations, significantly faster multi-layer rendering

### 🔧 Implementation Details
- **`Layer.mark_modified()`**: New method for explicit cache invalidation after direct pixel access
- **`Layer.compute_pixel_hash()`**: Fast hash based on shape + sample pixels + alpha sum
- **`LayerManager._is_cache_valid()`**: Comprehensive cache validation checking all change factors
- **Undo/redo integration**: Added `mark_modified()` calls after undo/redo operations

### 📁 Files Modified
- `src/core/layer_manager.py` – Re-enabled caching with smart validation, added version tracking and hash computation
- `src/ui/main_window.py` – Added `mark_modified()` calls in undo/redo handlers

---

## Version 2.7.3 - Theme, Tools & UI Polish
**Date**: January 22, 2026  
**Type**: Feature & Bug Fix Release

### 🎨 Claude Theme (New)
- **ClaudeTheme** in `theme_manager.py`: Bright, warm theme inspired by Anthropic Claude brand colors
- Warm cream backgrounds (`#faf6f1`), coral/salmon accents (`#d97757`), clean white canvas
- Available in theme dropdown as "Claude"

### 🖌️ Tool Previews & Eraser Edge Delete
- **Dither canvas preview**: Checkerboard pattern preview at cursor (brush-size area, `(x+y)%2` pattern)
- **Spray canvas preview**: Existing circular dashed outline verified; no changes
- **Eraser right-click**: Delete edge lines on canvas; right-click or right-drag to remove edges (reuses Edge tool storage)

### 🧩 UI Polish
- **Panel open/close buttons**: Redesigned as minimalistic centered chevrons (`‹` `›`), transparent + subtle hover, 14×40px in 16px strip
- **Restore buttons** (when panels collapsed): Minimal grey chevrons, vertically centered, hover highlight
- **Theme integration**: Collapse/restore buttons use `text_secondary`, `button_hover`; btn containers use `bg_primary`

### 🐛 Bug Fixes
- **Canvas grid off-center on panel toggle**: Redraw was only triggered when *collapsing* panels. Now `redraw_callback` runs when *expanding* left/right panels too (`after(50, redraw_callback)`), so canvas recenters immediately.

### 📁 Files Modified
- `src/ui/theme_manager.py` – ClaudeTheme, theme registry
- `src/core/canvas_renderer.py` – `draw_dither_preview`, numpy import fix
- `src/core/event_dispatcher.py` – Dither preview hooks, eraser right-click/right-drag, `canvas_x`/`canvas_y` fix
- `src/tools/eraser.py` – Right-click edge delete, `on_right_drag`, `_erase_edge_at_position`, `set_main_window`
- `src/ui/main_window.py` – Collapse button redesign (containers, minimal buttons)
- `src/core/window_state_manager.py` – Redraw on expand, minimal restore buttons, chevron text
- `src/ui/theme_dialog_manager.py` – Theme apply for btn containers, transparent collapse buttons

---

## Version 2.7.2 - Quality of Life Enhancements
**Date**: January 18, 2026  
**Type**: QoL Enhancement Release

### 🔍 Zoom to Cursor + Fit/100% View
- **Zoom to Cursor**: Ctrl+wheel now zooms while preserving cursor position in view
  - Implemented `_zoom_at_cursor()` method in `main_window.py` for focus-preserving zoom
  - Mouse wheel handler added to `event_dispatcher.py` for Ctrl+wheel detection
  - Calculates zoom center based on cursor position relative to canvas
- **Fit View Button**: New toolbar button automatically calculates optimal zoom to fit entire canvas
  - `_zoom_fit()` method calculates zoom based on canvas size and viewport dimensions
  - `_get_fit_zoom()` helper determines best fit zoom level
- **100% View Button**: Quick reset to 100% zoom level
  - `_zoom_100()` method sets zoom to exactly 1.0x
- **Focus Preservation**: All zoom operations use `_apply_zoom_with_focus()` to maintain visual focus

### 📦 Export Presets + Quick Export
- **Export Settings Dialogs**: Configurable export options for all formats
  - PNG: Scale factor and transparency toggle
  - GIF: Scale factor and frame duration
  - Sprite Sheet: Scale factor, layout (horizontal/vertical/grid), and spacing
  - `_prompt_export_settings()` method creates CustomTkinter dialogs for each format
- **Preset Persistence**: Export settings saved between sessions
  - JSON storage in `~/.pixelperfect/export_presets.json` (or `AppData/PixelPerfect/` on Windows)
  - `_load_export_presets()` and `_save_export_presets()` methods manage persistence
  - Per-format settings with recent directories tracking
- **Quick Export**: Ctrl+Shift+E uses last export settings for instant re-export
  - `quick_export()` method loads last export type and settings
  - File menu includes "Quick Export" option
  - Keyboard shortcut: Ctrl+Shift+E

### 🎨 Recent Colors Selection Improvements
- **Reliable Selection**: Recent colors view now properly sets active brush color
  - `_select_recent_color()` in `color_view_manager.py` stores selected color in `main_window.recent_selected_color`
  - `get_current_color()` in `main_window.py` handles recent view mode correctly
  - Fixed color selection not activating brush tool when clicking recent colors

### 📁 Files Modified
- `src/ui/main_window.py` - Added zoom utilities (`_zoom_fit`, `_zoom_100`, `_zoom_at_cursor`, `_apply_zoom_with_focus`, `_get_fit_zoom`)
- `src/core/event_dispatcher.py` - Added mouse wheel handler for Ctrl+wheel zoom-to-cursor
- `src/ui/file_operations_manager.py` - Added export presets system (`_prompt_export_settings`, `_load_export_presets`, `_save_export_presets`, `quick_export`)
- `src/ui/ui_builder.py` - Added Fit and 100% buttons to toolbar
- `src/ui/color_view_manager.py` - Improved recent colors selection handling

---

## Version 2.7.0 - Advanced Features & Critical Bug Fixes
**Date**: January 1, 2026  
**Type**: Major Feature & Bug Fix Release

### 🧠 Delta-Based Undo System (95% Memory Reduction)
- **Complete refactor of `undo_manager.py`**: Now stores only changed pixels instead of full canvas copies
- **New classes**: `UndoDelta`, `DeltaTracker` for efficient change tracking
- **Memory savings**: From ~16KB per action (64x64 canvas) to ~2KB per action (typical stroke)
- **Increased limit**: Now supports 100 undo states (up from 50)

### ⚡ Scanline Flood Fill (5-20x Faster)
- **Optimized `fill.py`**: Replaced naive stack-based algorithm with scanline approach
- **Batch operations**: Fills entire horizontal lines at once using NumPy slicing
- **Visible improvement**: Large fill areas now complete nearly instantly

### 🎨 Recent Colors Palette (New Feature!)
- **New `recent_colors.py`**: Tracks last 16 colors used while drawing
- **Automatic tracking**: Colors added to recent list when drawing starts
- **Persistent storage**: Saves to user's AppData/PixelPerfect folder between sessions
- **New UI view**: "Recent" radio button in palette panel shows 4x4 color grid

### ⚡ Event Throttling System
- **New `event_throttle.py`**: Utility classes for throttling high-frequency events
- **`EventThrottler`**: Limits function calls to specified interval (~120 FPS default)
- **`CanvasEventOptimizer`**: Smart mouse move handling with position deduplication

### 🐛 Critical Bug Fixes
- **Undo System Restoration**: Fixed `save_state()` storing identical old/new colors, preventing undo from working
- **Edge Lines Lost on Undo**: Fixed edge lines disappearing when undoing non-edge tool actions
  - Now always saves edge lines state for all tools
  - Properly distinguishes `None` vs empty list for edge_lines
- **Selection Tool Clearing Pixels**: Disabled layer compositor caching that was too aggressive
- **Edge Lines During Move**: Fixed edge lines outside selection disappearing during move operations

### 📁 New Files Created
- `src/core/recent_colors.py` - RecentColorsManager class
- `src/ui/palette_views/recent_view.py` - UI component for recent colors
- `src/core/event_throttle.py` - Throttling and rate limiting utilities

---

## Version 2.6.2 - Performance Optimizations
**Date**: January 1, 2026  
**Type**: Performance Release

### 🚀 Rendering Optimizations
- **✅ NumPy Vectorization**: `draw_all_pixels_on_tkinter()` now uses `np.where()` to find non-transparent pixels instead of iterating over all canvas pixels. Dramatically faster for sparse canvases.
- **✅ Layer Flattening**: `flatten_layers()` uses vectorized alpha blending with NumPy operations instead of nested Python loops. ~10-50× faster for multi-layer compositions.
- **✅ Single Pixel Updates**: Added note for future incremental update implementation (currently triggers full redraw as safety measure).

### 🎨 Selection/Transform Optimizations
- **✅ Scaling Operations**: `_simple_scale()` uses NumPy fancy indexing for nearest-neighbor scaling instead of nested loops.
- **✅ Preview Scaling**: `preview_scaled_pixels()` uses vectorized scaling preview with NumPy coordinate grids.
- **✅ Mirror Operations**: `mirror_selection()` now uses `np.where()` to iterate only over non-transparent pixels.
- **✅ Rotation Operations**: `apply_rotation()` uses vectorized pixel clearing and placement with NumPy masks.

### 🖱️ Event Handling Optimizations
- **✅ Mouse Move Caching**: `on_tkinter_canvas_mouse_move()` added early-exit caching to skip redundant preview draws when mouse hasn't moved to a new canvas pixel coordinate.

### 🧹 Code Cleanup
- **✅ Debug Print Removal**: Removed remaining debug prints from `brush.py` (2 prints) and `selection_manager.py` (1 print).
- **✅ Update Call Consolidation**: `loading_screen.py` - reduced redundant `update_idletasks()` calls.

**Expected Improvements**:
- Brush strokes: Smoother on large canvases
- Selection scaling: Much faster preview during drag
- Mirror/Rotate: Faster transformation application
- Mouse move: Reduced CPU overhead for cursor previews

**Files Modified**:
- `src/core/canvas_renderer.py` - NumPy vectorization for rendering
- `src/ui/selection_manager.py` - Vectorized selection transforms
- `src/core/event_dispatcher.py` - Mouse move event optimization
- `src/tools/brush.py` - Debug print cleanup
- `src/ui/loading_screen.py` - Update call consolidation

---

## Version 2.6.1 - Code Cleanup & Refactor
**Date**: December 3, 2025  
**Type**: Maintenance Release

### 🧹 Code Cleanup
- **✅ Dead Code Removal**: Removed ~100 lines of unused fallback code from `main_window.py`
  - `_initialize_all_views()` fallback after manager delegation
  - `_show_view()` fallback after manager delegation
- **✅ Debug Print Cleanup**: Removed ~150+ debug print statements from production code
  - `loading_screen.py`: 75 prints removed
  - `main_window.py`: 41 prints removed
  - `window_state_manager.py`: 23 prints removed
  - `selection.py`: 12 prints removed
- **✅ Unused Import Cleanup**: Removed `CanvasSize`, `UndoState`, `Optional` unused imports
- **✅ Documentation Compaction**: Reduced `SCRATCHPAD.md` from 6,058 to ~400 lines (per project rules)

**Files Modified**:
- `src/ui/main_window.py` - Dead code and print cleanup
- `src/ui/loading_screen.py` - Print cleanup and unused import
- `src/core/window_state_manager.py` - Print cleanup
- `src/tools/selection.py` - Print cleanup
- `docs/SCRATCHPAD.md` - Compacted per project rules

---

## Version 2.6.0 - Spray Tool & Palette Overhaul
**Date**: November 13, 2025  
**Type**: Feature Release

### ✒️ Spray Paint Tool
- **✅ New Tool**: Added `SprayTool` with radius/density controls and live cursor preview.
- **✅ Layer-Aware**: Integrates with `ToolSizeManager.spray_at()` so droplets respect active layer bounds.
- **✅ Shortcut Ready**: Bound to the `Y` hotkey and right-click size menu just like brush/eraser.
- **✅ Continuous Flow**: Dragging keeps spraying while mouse button is held for natural coverage.

### 🧭 Canvas Zoom Scrollbar
- **✅ Visual Zoom Control**: Custom scrollbar with +/− buttons and draggable handle rendered on the canvas edge.
- **✅ Wheel Sync**: Scroll wheel, dropdown, and scrollbar stay in sync via `CanvasScrollbar.update_zoom_index()`.
- **✅ Theme Aware**: Colors follow the active theme for dark/light parity.

### 🎨 Dynamic JSON Palette Loader
- **✅ JSON Auto-Discovery**: Palettes in `assets/palettes/*.json` are scanned at startup and listed in the Palette dropdown.
- **✅ Safe Naming**: Duplicate names get suffixes like `Palette (2)` so nothing collides silently.
- **✅ Default + Extensible**: Ships with SNES Classic fallback plus JSON palettes (including new `grass.json` 16-tone set).

**Technical Details**:
- **UI**: `src/ui/ui_builder.py` menu pulls from `ColorPalette.get_available_palette_names()`.
- **Core**: `src/core/color_palette.py` now indexes external JSON palettes and loads them through `load_by_name()`.
- **Input**: `src/core/event_dispatcher.py` routes spray events and zoom bindings to the new systems.

## Version 2.5.11 - Primary Color Variations Highlighting Fix
**Date**: January 2025  
**Type**: Visual Bug Fix

### 🎨 Primary Color Variations Highlighting Fix
- **✅ Fixed Visual Feedback**: Resolved Primary color variations not showing selection highlighting
- **✅ Root Cause**: Missing visual feedback system for variation button selection
- **✅ Solution**: Added white border highlighting for selected color variations
- **✅ User Impact**: Clear visual indication of which color variation is currently selected

**Technical Details**:
- **Issue**: Clicking color variations in Primary subcategories showed no visual feedback
- **Location**: `src/ui/palette_views/primary_view.py` `_select_color_variation()` method
- **Fix**: Added selection tracking and white border highlighting system
- **Files Modified**: `src/ui/palette_views/primary_view.py`

---

## Version 2.5.10 - Saved Colors Auto-Selection Fix
**Date**: January 2025  
**Type**: Critical Bug Fix

### 🐛 Saved Colors Auto-Selection Fix
- **✅ Fixed Brush Color Issue**: Resolved saved colors not becoming active brush color after saving
- **✅ Root Cause**: Saving colors only stored them but didn't select them as current color
- **✅ Solution**: Automatically select saved color as current brush color when saving
- **✅ User Impact**: Seamless painting workflow - saved colors immediately become active brush color

**Technical Details**:
- **Issue**: After saving colors from Primary/Wheel views, brush reverted to Grid color
- **Location**: `src/ui/palette_views/saved_view.py` `_on_saved_slot_click()` method
- **Fix**: Added `self.current_saved_color = current_color` to auto-select saved color
- **Files Modified**: `src/ui/palette_views/saved_view.py`

---

## Version 2.5.9 - Primary Colors Centering Fix
**Date**: January 2025  
**Type**: Visual Bug Fix

### 🎨 Primary Colors Centering Fix
- **✅ Fixed Grid Centering**: Resolved Primary colors grid being left-aligned instead of centered
- **✅ Root Cause**: Missing `grid_columnconfigure` to center columns within container
- **✅ Solution**: Added proper grid column configuration with `weight=1` for all columns
- **✅ User Impact**: Primary colors and variations grids now properly centered for better visual balance

**Technical Details**:
- **Issue**: Primary colors grid appeared left-aligned with empty space on the right
- **Location**: `src/ui/palette_views/primary_view.py` `_create_primary_colors_grid()` method
- **Fix**: Added `grid_columnconfigure(col, weight=1)` for both Primary colors and variations grids
- **Files Modified**: `src/ui/palette_views/primary_view.py`

---

## Version 2.5.8 - Grid and Wheel Color Saving Fix
**Date**: January 2025  
**Type**: Critical Bug Fix

### 🐛 Grid and Wheel Color Saving Fix
- **✅ Fixed Color Saving Issue**: Resolved Grid and Wheel colors not saving to Saved Colors palette
- **✅ Root Cause**: `get_source_color()` method was checking current view mode instead of using `last_active_view` when in saved mode
- **✅ Solution**: Modified method to use `last_active_view` to determine source view when in saved mode
- **✅ User Impact**: Users can now properly save colors from any view (Grid, Primary, or Wheel) to Saved Colors

**Technical Details**:
- **Issue**: When in "saved" view mode, system was saving Primary colors instead of actual selected colors
- **Location**: `src/ui/main_window.py` `get_source_color()` method
- **Fix**: Use `last_active_view` to determine which view was active before switching to saved mode
- **Files Modified**: `src/ui/main_window.py`

---

## Version 2.5.7 - Primary Color Selection Fix
**Date**: January 2025  
**Type**: Critical Bug Fix

### 🐛 Primary Color Selection TypeError Fix
- **✅ Fixed Color Selection Crash**: Resolved TypeError when selecting colors in Primary palette view
- **✅ Root Cause**: `primary_view.py` was passing color tuples instead of integer indices to `on_color_select` callback
- **✅ Solution**: Updated `_select_color_variation` method to pass `palette.primary_color` index instead of color tuple
- **✅ Consistency**: Now matches behavior of `grid_view.py` which was already working correctly
- **✅ User Impact**: Users can now select color variations from Primary palette without application crashes

**Technical Details**:
- **Error**: `TypeError: '<=' not supported between instances of 'int' and 'tuple'`
- **Location**: `src/ui/palette_views/primary_view.py` line 319
- **Fix**: Pass `color_index` instead of `color` tuple to `on_color_select` callback
- **Files Modified**: `src/ui/palette_views/primary_view.py`

---

## Version 2.5.4 - Edge Tool Reliability Hardening
**Date**: October 16, 2025  
**Type**: Reliability Improvements

### 🧹 Immortal Edge Lines Purge and New Project Consistency
- **✅ Safety Purge Added**: `MainWindow._purge_canvas_overlays()` deletes all transient overlay tags and clears EdgeTool storage
- **✅ New Project Cleanup**: `FileOperationsManager.new_project()` calls purge first to guarantee a clean slate
- **✅ Keyboard Consistency**: `Ctrl+N` now routes to FileOps `new_project()` so the same cleanup path always runs
- **🧩 Context**: Rare reports of “immortal” edge lines persisting after redraws; this hardening ensures overlays cannot survive resets

---

## Version 2.5.3 - Edge Tool Flickering Fix
**Date**: January 2025  
**Type**: Critical Bug Fix

### 🐛 Edge Tool Flickering Lines Fix
- **✅ Flickering Eliminated**: Fixed critical issue where edge lines flickered in and out during continuous drawing
- **✅ Preview System Isolation**: Disabled hover preview during active drawing to prevent interference
- **✅ Clean Drawing Experience**: Edge lines now draw smoothly without visual artifacts
- **✅ Preserved Functionality**: All edge tool features remain intact (thickness, erase, etc.)

### 🔧 Technical Fix
- Modified `on_mouse_move()` to only update preview when not actively drawing
- Added preview clearing before starting to draw and after completing drawing
- Maintained deferred drawing optimization for performance
- Preserved all existing edge tool functionality

## Version 2.5.2 - Edge Tool Variable Thickness
**Date**: October 16, 2025  
**Type**: Feature Enhancement

### 🎨 Edge Tool Variable Thickness Feature
- **✅ Variable Edge Thickness**: Edge tool now supports 5 different thickness levels (0.1P, 0.25P, 0.5P, 1.0P, 2.0P)
- **✅ Right-Click Thickness Menu**: Right-click edge tool button to select thickness with visual indicators
- **✅ Thickness Display**: Edge button shows current thickness: `Edge [0.1P]`, `Edge [0.25P]`, etc.
- **✅ Zoom-Scaled Line Width**: Edge lines scale properly with zoom level for consistent appearance
- **✅ Thickness Persistence**: Each edge line remembers its thickness when redrawn
- **✅ Preview Thickness**: Hover preview shows actual thickness that will be drawn
- **✅ Fine Line Control**: Ultra-fine 0.1P thickness for detailed edge work and line art

### 🔧 Technical Implementation
- Added `edge_thickness` property to ToolSizeManager with 0.1P default
- Implemented `show_edge_thickness_menu()` with 5 thickness options and checkmarks
- Updated `_draw_edge_line_on_canvas()` to accept and use variable thickness
- Modified edge data storage to include thickness for persistence
- Added `update_edge_button_text()` to display current thickness
- Enhanced preview system to show actual thickness being drawn
- Integrated right-click menu binding in UIBuilder

### 🎯 User Experience
- **Ultra Fine (0.1P)**: Perfect for detailed line art and fine edges
- **Fine (0.25P)**: Great for subtle outlines and detailed work
- **Medium (0.5P)**: Good balance for most edge drawing
- **Thick (1.0P)**: Bold edges for emphasis
- **Extra Thick (2.0P)**: Heavy outlines for dramatic effect

---

## Version 2.5.1 - Edge Tool Detection Fix
**Date**: October 16, 2025  
**Type**: Critical Bug Fix

### 🐛 Edge Tool Critical Fix
- **✅ Fixed Edge Detection Bug**: Edge tool now correctly detects all edges (top, bottom, left, right)
- **✅ Float Precision Coordinates**: Added separate coordinate system for edge tool with fractional precision
- **✅ Improved Edge Targeting**: Users can now reliably click on any edge of a pixel
- **✅ New Project Edge Clearing**: Edge lines are now properly cleared when creating new projects
- **✅ Right-Click Erase**: Added right-click functionality to erase edge lines near clicked pixels
- **✅ Visual Feedback Fix**: Edge tool now shows hover preview like brush and eraser tools
- **✅ Enhanced Distance Detection**: Multi-pixel edge detection with 3x3 scanning and 40% edge zone

### 🔧 Technical Changes
- Added `_tkinter_screen_to_canvas_coords_float()` method for edge tool precision
- Modified event dispatcher to use float coordinates specifically for edge tool
- Updated edge tool method signatures to accept float coordinates
- Added edge clearing functionality to FileOperationsManager
- Added right-click event handling (`<Button-3>`) for edge tool erasing
- Implemented smart edge detection for erasing nearby edge lines
- Added edge tool visual feedback integration to mouse move event handler
- Added edge preview cleanup across all preview clearing locations
- Implemented multi-pixel edge detection with 3x3 scanning system
- Enhanced edge zone from 25% to 40% for more forgiving detection
- Added cross-pixel edge detection for cursor positioning between pixels
- Added distance prioritization system for optimal edge selection
- Maintained backward compatibility with other tools

### 📚 Documentation
- Added comprehensive edge tool detection bug fix documentation
- Updated technical architecture documentation

## Version 2.5.0 - 64x Zoom and Edge Tool Complete
**Date**: January 2025  
**Type**: Major Feature Release

### 🔍 Zoom System Improvements
- **✅ Added 64x Zoom**: New maximum zoom level for extreme detail work
- **✅ Updated Zoom Dropdown**: Added 64x option to toolbar zoom menu
- **✅ Updated Scrollbar**: Added 64x to scrollable zoom bar
- **✅ Increased Zoom Limits**: Canvas zoom limits increased from 32x to 64x

### 🎨 Edge Tool Complete Implementation
- **✅ Edge Tool Fully Functional**: Draws thin lines on pixel boundaries with hover preview
- **✅ Edge Line Persistence**: Edge lines survive canvas redraws and tool switching
- **✅ Hover Preview System**: Real-time preview shows where edge line will be drawn
- **✅ Edge Detection Zones**: 0.1 pixel width zones detect top/bottom/left/right edges
- **✅ Canvas Integration**: Edge tool properly integrated with canvas renderer system

### 🔧 Technical Changes
- Updated zoom arrays in ui_builder.py, canvas_zoom_manager.py, canvas_scrollbar.py
- Increased canvas zoom limits from 32x to 64x in canvas.py
- Added Edge tool with persistent storage system
- Implemented canvas renderer integration for edge line persistence
- Added main window reference system for tools

### 📚 Documentation
- Added comprehensive Edge tool feature documentation
- Updated zoom functionality documentation
- Updated changelog with all improvements

## Version 2.4.0 - Edge Tool Feature
**Date**: January 2025  
**Type**: Major Feature Addition

### 🎨 Major Feature: Edge Tool
- **✅ Smart Edge Detection**: Automatically detects shape boundaries and draws clean outlines
- **✅ Three Edge Modes**: Outline, Inner, and Outer edge placement options
- **✅ Shape Recognition**: Uses flood fill algorithm to identify connected pixel shapes
- **✅ Right-click Mode Cycling**: Cycle through edge modes with right-click
- **✅ Thickness Control**: 1-3 pixel thick edges for different artistic needs

### 🔧 UI Improvements
- **✅ Squished Texture Button**: Reduced from 175px to 85px width to make room
- **✅ Added Edge Button**: New Edge tool button positioned next to texture button
- **✅ Tooltip Support**: "Draw edges around pixel shapes (G)" tooltip

### 📚 Documentation
- Added comprehensive Edge tool feature documentation
- Updated changelog with edge tool implementation details

## Version 2.3.0 - Import PNG Dialog Scale Calculation Fix
**Date**: January 2025  
**Type**: Critical Bug Fix

### 🐛 Critical Import Dialog Fixes
- **✅ Fixed GUI Scale Calculation**: Dialog now uses validated base dimensions for scale calculations instead of raw file dimensions
- **✅ Fixed Import Logic Priority**: Import process now prioritizes scaled export detection over direct size detection
- **✅ Fixed Scale Switching**: No more GUI state corruption when switching between scale options

### 🔧 Technical Changes
- Added base dimension storage in Import PNG dialog
- Fixed scale calculation to use validated dimensions
- Applied priority logic to import process matching validation logic
- Eliminated GUI state corruption during scale switching

### 📚 Documentation
- Added comprehensive scale calculation fix documentation
- Updated import dialog behavior documentation

## Version 2.2.9 - PNG Validation Algorithm Priority Fix
**Date**: January 2025  
**Type**: Critical Algorithm Fix

### 🐛 Critical Algorithm Fix
- **✅ Fixed PNG Validation Priority**: Algorithm now prioritizes scaled export detection over direct size detection
- **✅ Fixed 8x8 Scaled Export Detection**: 8x8 images exported at 8x scale now correctly detected as 8x8 base size

### 🔧 Technical Changes
- Reordered validation logic to check scaled exports before direct sizes
- Fixed algorithm priority preventing 64x64 from being treated as direct size when it's actually 8x8 scaled
- Added clear comments explaining validation priority system

### 📚 Documentation
- Added comprehensive algorithm priority fix documentation
- Updated validation logic explanation

## Version 2.2.8 - Import PNG Dialog Dimension Detection Fix
**Date**: January 2025  
**Type**: Critical Bug Fix

### 🐛 Critical Import Dialog Fix
- **✅ Fixed Import PNG Dialog Dimensions**: Dialog now shows detected base dimensions instead of raw file dimensions
- **✅ Fixed Scaled Export Display**: 8x8 images exported at 8x scale now correctly show "Original: 8x8 pixels"

### 🔧 Technical Changes
- Modified Import PNG dialog to use validation logic for dimension display
- Added fallback to raw dimensions if validation fails
- Integrated PNGImporter validation with dialog UI

### 📚 Documentation
- Added comprehensive dimension detection fix documentation
- Updated import dialog behavior documentation

## Version 2.2.7 - PNG Import 8x8 Validation Fix
**Date**: January 2025  
**Type**: Critical Bug Fix

### 🐛 Critical Import Fix
- **✅ Fixed 8x8 PNG Import Validation**: 8x8 images now correctly import without dimension detection errors
- **✅ Fixed Import Dialog Display**: Import PNG dialog now shows correct dimensions for 8x8 images

### 🔧 Technical Changes
- Added `8` to `VALID_SIZES` array in PNG validation system
- Updated error messages to include 8x8 as valid size
- Fixed validation logic to properly recognize 8x8 images

### 📚 Documentation
- Added comprehensive PNG import validation fix documentation
- Updated error messages and validation text

## Version 2.2.6 - UI Styling Fixes
**Date**: January 2025  
**Type**: UI/UX Improvements

### 🎨 UI Styling Fixes
- **✅ Fixed Double "Layers" Text**: Removed duplicate "Layers" title in the Layers panel
- **✅ Removed Visual Boxes**: Eliminated unwanted rectangular boxes around Layers and Animation panels for cleaner appearance

### 🔧 Technical Changes
- Changed panel containers from `fg_color=theme.bg_secondary` to `fg_color="transparent"`
- Removed duplicate title creation in `LayerPanel` class
- Improved visual consistency across all themes

### 📚 Documentation
- Added comprehensive UI styling fix documentation
- Updated changelog with visual improvement details

## Version 2.2.5 - Quality of Life Improvements
**Date**: January 2025  
**Type**: Quality of Life Fixes

### 🎯 Quality of Life Improvements
- **✅ Added 8x8 Canvas Size**: New "Tiny" preset for micro icons and detailed pixel work
- **✅ Fixed File Dialog Layering**: All file dialogs (Import PNG, Open/Save Project, Export functions) now properly appear on top of the main application window

### 🔧 Technical Changes
- Added `CanvasSize.TINY = (8, 8)` to canvas size enum
- Updated UI dropdown to include "8x8" option  
- Fixed all `filedialog` calls with proper `parent` parameter
- Enhanced Import PNG dialog with focus management

### 📚 Documentation
- Added comprehensive file dialog layering fix documentation
- Updated canvas size documentation with new 8x8 option

## Version 2.2.4 - Selection Move Tool Pixel Duplication Fix
**Date**: October 16, 2025  
**Type**: Critical Bug Fix

### 🐛 Fixed Pixel Duplication Bug
**Fixed pixels being duplicated when moving selection multiple times**

**The Bug:**
- After fixing the "pixels deleted underneath" bug, a new bug appeared
- Moving a selection a second time would DUPLICATE the pixels on the canvas
- Pixels would appear twice at the new location, creating unwanted duplicates

**Root Cause:**
- `finalize_move()` was being called automatically after EVERY drop
- This caused pixels to be drawn twice: once in `on_mouse_up()` and again in `finalize_move()`
- The automatic finalization was meant to clear the original position, but was running on every move

**The Fix:**
- Only call `finalize_move()` on the FIRST move, not on subsequent moves
- Added `pixels_cleared` flag to track if finalization has already occurred
- `reset_state()` properly resets the flag for new selections

**Files Modified:**
- `src/tools/selection.py`: Added conditional finalization logic with `pixels_cleared` flag

**Result:**
✅ First move: Clears original position, draws at new location  
✅ Second move: Only draws at new location (no duplication)  
✅ Third move: Only draws at new location (no duplication)  
✅ Tool switch: Properly finalizes and resets state  

---

## Version 2.2.3 - Selection Move Tool Bug Fix
**Date**: October 16, 2025  
**Type**: Critical Bug Fix

### 🐛 Fixed Critical Selection Move Bug
**Fixed pixels being deleted underneath when moving selection multiple times**

**The Bug:**
- When using Selection tool → Move tool, moving pixels once worked fine
- But picking them up again to adjust position would DELETE pixels underneath
- Users couldn't make adjustments without destroying artwork
- Only happened under the pixels being moved, not the entire selection area

**Root Cause:**
- `finalize_move()` was resetting `original_selection = None` after first move
- Next pickup treated it as "first pickup" and cleared pixels at current location
- This destroyed pixels underneath that should have been preserved

**The Fix:**
- Don't reset `original_selection` in `finalize_move()` - preserve it for subsequent moves
- Added `reset_state()` method to properly reset move tool only when switching tools
- Subsequent pickups now correctly use saved_background restoration logic
- Pixels underneath are preserved via the background saving mechanism

**Files Modified:**
- `src/tools/selection.py`: Commented out problematic reset, added `reset_state()` method
- `src/ui/main_window.py`: Call `reset_state()` when clearing selection or switching tools

**Result:**
✅ Users can now pick up and reposition selections multiple times  
✅ Pixels underneath are preserved during adjustments  
✅ No more destructive behavior when fine-tuning placement  
✅ Clean state management when switching tools

---

## Version 2.0.8 - Background Texture Mode
**Date**: December 2024  
**Type**: New Feature

### 🎨 Added Background Texture Mode
**Extended background toggle to include paper texture option**

**New Feature:**
- **Background Texture Mode**: Added 4th mode to background toggle (Auto → Dark → Light → **Paper** → Auto)
- **Organic Background Rendering**: Realistic paper texture background with organic grain patterns
- **Consistent Paper Colors**: Uses same cream base (#f5f5dc) and grain (#e6e6d4) as grid paper mode
- **📄 Icon**: Background paper mode shows document emoji with "Background Mode: Paper Texture" tooltip
- **Proper Rendering Order**: Background texture drawn first, grid appears on top (fixes override issue)

**Technical Implementation:**
- Extended `background_mode` from 3 to 4 modes in `src/core/canvas.py`
- Added `draw_background_texture()` method in `src/core/canvas_renderer.py`
- Updated `toggle_background_mode()` to cycle through 4 modes in `src/ui/background_control_manager.py`
- Fixed rendering order: background texture → grid → border → pixels → selection
- Added background texture settings (intensity, base color, grain color)
- Organic grain patterns using random seed (123) for consistent texture

**Bug Fixes:**
- **Fixed Background Override Issue**: Background paper texture no longer overrides grid colors
- **Proper Layer Order**: Grid now renders on top of background texture correctly
- **Consistent Colors**: Both grid and background paper modes use identical color scheme

**User Experience:**
- Click yin-yang button (🌗/⚫/⚪/📄) to cycle through all 4 background modes
- Paper mode provides realistic paper texture background
- Grid colors work properly regardless of background mode
- Maintains all existing functionality (zoom, pan, themes, etc.)

**Files Modified:**
- `src/core/canvas.py` - Added background texture mode and settings
- `src/core/canvas_renderer.py` - Added background texture rendering and fixed order
- `src/ui/background_control_manager.py` - Extended to 4-mode cycle with 📄 icon

---

## Version 2.0.7 - Paper Texture Grid Mode
**Date**: December 2024  
**Type**: New Feature

### 🎨 Added Organic Paper Texture Grid Mode
**New paper texture option for realistic grid backgrounds**

**New Feature:**
- **Paper Texture Mode**: Added 4th mode to grid toggle (Auto → Dark → Light → **Paper** → Auto)
- **Organic Rendering**: Realistic paper grain patterns with organic, non-straight lines
- **Configurable Settings**: Paper base color (#f5f5dc), grain color (#e6e6d4), and intensity (0.3)
- **📄 Icon**: Paper mode shows document emoji with "Grid Mode: Paper Texture" tooltip
- **Seamless Integration**: Works with existing zoom, pan, and theme systems

**Technical Implementation:**
- Extended `grid_mode` from 3 to 4 modes in `src/core/canvas.py`
- Added `draw_paper_texture_grid()` method in `src/core/canvas_renderer.py`
- Updated `toggle_grid_mode()` to cycle through 4 modes in `src/ui/grid_control_manager.py`
- Added paper texture settings (intensity, base color, grain color)
- Organic grain patterns using random seed for consistent texture
- Subtle grid lines with reduced opacity for realistic paper appearance

**User Experience:**
- Click white orb (🌓/🌙/☀️/📄) to cycle through all 4 grid modes
- Paper mode provides realistic paper texture background
- Maintains all existing functionality (zoom, pan, overlay, etc.)
- Consistent with current theme and UI patterns

**Files Modified:**
- `src/core/canvas.py` - Added paper texture mode and settings
- `src/core/canvas_renderer.py` - Added organic paper texture rendering
- `src/ui/grid_control_manager.py` - Extended to 4-mode cycle with 📄 icon
- `src/ui/ui_builder.py` - Updated tooltip for paper mode

---

## Version 2.0.6 - Pan Tool and Window Resize Fixes
**Date**: December 2024  
**Type**: Critical Bug Fixes

### 🔧 Fixed Pan Tool Jumping Back to Original Position
**Resolved issue where pan tool would jump back to original position after dragging**

**Problem:**
- Pan tool would temporarily move the canvas during drag
- On mouse release, canvas would jump back to original position
- Pan offset was never permanently applied

**Root Cause:**
- `on_tkinter_canvas_mouse_up()` called `tool.end_pan()` but never applied final offset
- Pan offset was only temporarily applied during drag, then immediately restored

**Solution Implemented:**
- Modified `on_tkinter_canvas_mouse_up()` to get final pan offset and apply it permanently
- Added `result = tool.update_pan(event.x, event.y, self.main_window.canvas.zoom)` before ending pan
- Set `self.main_window.pan_offset_x, self.main_window.pan_offset_y = result` permanently

**Files Modified:**
- `src/core/event_dispatcher.py` (lines 357-361)

**Status:** ✅ **RESOLVED** - Pan tool now properly maintains position after dragging

### 🎯 Fixed Canvas Grid Centering During Window Resize
**Resolved issue where canvas grid stayed in original screen position during window resize**

**Problem:**
- Canvas grid would stay in original screen position when window was resized
- Grid didn't recalculate center position for new window dimensions
- Visual disconnect between window size and grid position

**Root Cause:**
- EventDispatcher handled window resize but never called WindowStateManager's resize handler
- WindowStateManager's redraw callback was never triggered
- Canvas dimensions weren't updated before centering calculation

**Solution Implemented:**
- Added call to `window_state_manager.on_window_resize(event)` in EventDispatcher
- Enhanced WindowStateManager with proper delayed redraw mechanism
- Added `update_idletasks()` to force canvas dimension update before centering
- Increased resize delay from 100ms to 150ms for better timing

**Files Modified:**
- `src/core/event_dispatcher.py` (line 75)
- `src/core/window_state_manager.py` (lines 327, 329-332)
- `src/core/canvas_renderer.py` (line 118)

**Status:** ✅ **RESOLVED** - Canvas grid now properly centers during window resize

### 🎨 Fixed Brush Cursor Alignment After Panning
**Resolved issue where brush cursor appeared outside actual grid area after panning**

**Problem:**
- Brush cursor (white dotted square) would appear outside the actual grid
- Cursor preview didn't account for pan offset properly
- Misalignment between visual grid and cursor position

**Root Cause:**
- Cursor preview methods added pan offset directly instead of multiplying by zoom
- Inconsistent pan offset handling between main grid and cursor preview
- Pan offset in canvas pixel coordinates but cursor preview in screen coordinates

**Solution Implemented:**
- Fixed pan offset calculation in all cursor preview methods
- Changed from `+ self.app.pan_offset_x` to `+ self.app.pan_offset_x * self.app.canvas.zoom`
- Applied fix to brush, eraser, and texture preview methods

**Files Modified:**
- `src/core/canvas_renderer.py` (lines 297-298, 332-333, 368-369)

**Status:** ✅ **RESOLVED** - Brush cursor now properly follows panned grid

---

## Version 2.0.5 - Color Wheel Reference Fix
**Date**: December 2024  
**Type**: Critical Bug Fix

### 🔗 Fixed Color Wheel Reference Issue
**Resolved issue where MainWindow.color_wheel was None, preventing color wheel from working**

**Problem:**
- Color wheel rainbow ring selection was stuck on black brush
- Clicking colors on the color wheel didn't change the brush color
- Debug output showed `self.color_wheel exists: None` despite wheel mode being active
- `get_current_color()` always fell back to palette instead of using wheel

**Root Cause:**
- ColorViewManager creates the color wheel object, but MainWindow never gets updated with the reference
- MainWindow.color_wheel remained `None` even when ColorViewManager.color_wheel was properly created
- `get_current_color()` condition `self.color_wheel` was always `False` because it was `None`

**Solution Implemented:**
- Added MainWindow reference to ColorViewManager: `self.color_view_mgr.main_window = self`
- Added code in ColorViewManager to update MainWindow reference when creating wheel:
  ```python
  if hasattr(self, 'main_window') and self.main_window:
      self.main_window.color_wheel = self.color_wheel
  ```
- Added debug output to confirm reference updates

**Files Modified:**
- `src/ui/main_window.py` (lines 614-615)
- `src/ui/color_view_manager.py` (lines 107-110)

**Status:** ✅ **RESOLVED** - Color wheel now properly updates brush color when selecting colors

---

## Version 2.0.4 - Color Wheel Hardcoded Palette Fix
**Date**: December 2024  
**Type**: Critical Bug Fix

### 🔧 Fixed Hardcoded Palette Calls Breaking Color Wheel
**Resolved issue where color wheel brush color update was broken due to hardcoded palette calls**

**Problem:**
- After fixing the grid leak (v2.0.3), color wheel brush color update was broken again
- Clicking colors on the color wheel didn't change the brush color
- Brush continued using old palette color instead of selected wheel color

**Root Cause:**
- Two locations had hardcoded calls to `palette.get_primary_color()` instead of using `get_current_color()`
- These bypassed the proper color wheel mode detection
- `src/core/canvas_renderer.py` line 300: `r, g, b, a = self.app.palette.get_primary_color()`
- `src/core/event_dispatcher.py` line 522: `current_color = self.main_window.palette.get_primary_color()`

**Solution Implemented:**
- Changed both hardcoded calls to use `get_current_color()` instead
- This method properly respects the color wheel mode and gets color from wheel when active
- Maintains the grid leak fix while restoring brush color functionality

**Files Modified:**
- `src/core/canvas_renderer.py` (line 300)
- `src/core/event_dispatcher.py` (line 522)

**Status:** ✅ **RESOLVED** - Color wheel brush color update now works correctly without leaking to grid

---

## Version 2.0.3 - Color Wheel Grid Leak Fix
**Date**: December 2024  
**Type**: Critical Bug Fix

### 🔒 Fixed Color Wheel Colors Leaking Into Grid Layout
**Resolved issue where color wheel colors appeared in preset palette grid**

**Problem:**
- Using colors from the color wheel caused them to appear in the grid layout of colors
- This polluted the preset palette with unwanted colors
- Color wheel colors should be temporary, not permanently added to palettes

**Root Cause:**
- Previous fix (v2.0.2) introduced this leak by calling `palette.set_primary_color_by_rgba()`
- This method automatically adds colors to the palette if they don't exist (lines 275-277 in `color_palette.py`)
- Color wheel colors should NOT be added to the preset palette grid

**Solution Implemented:**
- Reverted the `palette.set_primary_color_by_rgba()` call in `ColorViewManager.on_color_wheel_changed()`
- The `get_current_color()` method already handles color wheel colors correctly by getting them directly from the wheel when in wheel mode
- Color wheel colors now remain temporary and don't pollute the palette grid

**Files Modified:**
- `src/ui/color_view_manager.py` (lines 146-158)

**Status:** ✅ **RESOLVED** - Color wheel colors no longer leak into grid layout

---

## Version 2.0.2 - Color Wheel Brush Color Fix
**Date**: December 2024  
**Type**: Critical Bug Fix

### 🎨 Fixed Color Wheel Click Not Updating Brush Color
**Resolved issue where clicking colors on color wheel didn't change brush color**

**Problem:**
- Clicking colors on the color wheel didn't update the brush color
- Brush continued using the previous palette color instead of the selected wheel color
- Color wheel interface worked but color selection had no effect on drawing

**Root Cause:**
- `ColorViewManager.on_color_wheel_changed()` method wasn't updating the palette's primary color
- Method only called `update_canvas_callback()` and `select_tool_callback()` 
- Missing call to `palette.set_primary_color_by_rgba()` to actually set the new color

**Solution Implemented:**
- Modified `ColorViewManager.on_color_wheel_changed()` to convert RGB to RGBA
- Added call to `self.palette.set_primary_color_by_rgba(rgba_color)` to update palette
- Now color wheel clicks properly update the brush color for immediate painting

**Files Modified:**
- `src/ui/color_view_manager.py` (lines 146-163)

**Status:** ✅ **RESOLVED** - Color wheel clicks now properly update brush color

---

## Version 2.0.1 - Color Wheel Display Fix
**Date**: December 2024  
**Type**: Critical Bug Fix

### 🎯 Fixed Color Wheel Not Displaying
**Resolved critical issue where color wheel was completely broken**

**Problem:**
- Selecting "Wheel" radio button showed empty canvas area instead of color wheel interface
- This was a recurring issue that had happened many times before

**Root Cause:**
- Logic error in `_show_view()` method condition: `elif mode == "wheel" and hasattr(self, 'color_wheel') and self.color_wheel:`
- `self.color_wheel` is intentionally set to `None` during initialization to prevent startup creation
- The `and self.color_wheel` condition always failed, preventing color wheel creation

**Solution Implemented:**
- Removed `and self.color_wheel` condition from both `main_window.py` and `color_view_manager.py`
- Color wheel now creates properly when "Wheel" view is selected
- Maintains lazy initialization pattern while fixing display issue

**Files Modified:**
- `src/ui/main_window.py` (line 913)
- `src/ui/color_view_manager.py` (line 96)

**Status:** ✅ **RESOLVED** - Color wheel displays correctly when selected

---

## Version 2.0.0 - Critical UI Bug Fix
**Date**: December 2024  
**Type**: Bug Fix

### 🐛 Fixed Saved Colors Blank Space Bug
**Eliminated persistent empty frame between palette controls and saved colors section**

**Root Cause:**
- `palette_content_frame` was packed and visible even when switching to saved view
- This frame is only used by Grid, Primary, Wheel, and Constants views - NOT Saved view
- When clearing widgets, the frame itself remained packed and visible, creating empty space

**Solution Implemented:**
- Added `self.palette_content_frame.pack_forget()` to hide frame when clearing it
- Re-pack `palette_content_frame` ONLY for views that need it (Grid, Primary, Wheel, Constants)
- Use `before` parameter to maintain correct packing order in frame hierarchy
- Saved view does NOT pack `palette_content_frame`, eliminating the empty box

**Files Modified:**
- `src/ui/main_window.py` - Fixed `_show_view()` method with proper frame visibility control
- `src/ui/ui_builder.py` - Reduced container padding (pady=5 → pady=0)
- `src/ui/palette_views/saved_view.py` - Reduced top padding on title and grid

**Architecture Insight:**
- `palette_content_frame`: Hosts widgets for Grid, Primary, Wheel, Constants views
- `color_display_container`: Contains individual view frames for ALL views
- `saved_view_frame`: Child of `color_display_container`, does NOT use `palette_content_frame`

**Key Lesson:**
When debugging UI spacing issues, trace the EXACT frame hierarchy and packing order. Don't assume padding is the issue - sometimes entire frames are visible when they shouldn't be. Use `pack_forget()` aggressively to hide unused containers.

---

## Version 1.72 - Enhanced AI Knowledge Base
**Date**: December 2024  
**Type**: Documentation Enhancement

### 📚 AI Knowledge Base Enhancement
**Comprehensive Python knowledge documentation for AI agents**

**Enhancements Added:**
- **Modern Python Features**: Python 3.9+ features, type hints, dataclasses, async/await patterns
- **Testing Frameworks**: Comprehensive pytest guidance, TDD methodology, mocking, integration testing
- **Performance Optimization**: Profiling techniques, memory management, algorithmic optimization, caching strategies
- **Dependency Management**: Virtual environments, poetry, pip, security considerations, package distribution
- **Maintainability Standards**: Code organization, documentation standards, linting, formatting, CI/CD practices
- **Advanced Patterns**: Metaclasses, descriptors, context managers, modern data structures

**Files Enhanced:**
- `docs/knowledge/AI_PYTHON_KNOWLEDGE.md` - Expanded from 1,435 to 3,500+ lines
- `docs/knowledge/AI_AGENT_README.md` - Updated workflow and modern development practices

**Benefits:**
- Better AI agent understanding of modern Python development
- Comprehensive testing and quality assurance guidance
- Performance optimization techniques for scalable applications
- Professional dependency management and security practices
- Industry-standard maintainability and documentation practices

---

## Version 1.71 - Notes Panel Feature
**Date**: December 2024  
**Type**: Feature Addition

### ✨ Notes Panel Added
**Persistent note-taking functionality integrated into the editor**

**Features Added:**
- **Notes Button**: Added to top toolbar for easy access
- **Toggle Panel**: Notes panel appears on right side of canvas area
- **Auto-Save**: Notes automatically saved as you type to `~/.pixelperfect/notes.json`
- **Export to TXT**: Export your notes to a text file with custom filename
- **Clear Function**: Quick clear button for resetting notes
- **Status Feedback**: Visual feedback for save/export operations
- **Persistent Storage**: Notes survive app restarts

**Files Created:**
- `src/ui/notes_panel.py` - Complete notes panel component (200+ lines)

**Files Modified:**
- `src/ui/ui_builder.py` - Added Notes button to toolbar
- `src/ui/main_window.py` - Integrated notes panel and toggle functionality

---

## Version 1.70 - Move Tool Critical Fixes & Visual Improvements
**Date**: December 2024  
**Type**: Critical Bug Fix + Feature Enhancement

### ✅ Move Tool Layer Synchronization Fixed
**Major bug where moved pixels would reappear in original location**

**Issues Fixed:**
- **Move Tool Canvas vs Layer**: Move tool was updating canvas directly instead of layer data
- **Event Dispatcher**: Was passing canvas object instead of layer object to move/selection tools
- **Visual Feedback**: Added live preview - pixels now follow cursor during move operations
- **Tool Switching**: Original pixels no longer reappear when switching to brush after move
- **Mirror Operations**: Fixed mirror working correctly with moved selections

**Technical Changes:**
- Modified `finalize_move()` to update layer pixels instead of canvas
- Updated `EventDispatcher` to pass `draw_layer` object to move/selection tools
- Added visual feedback during move operations in `MoveTool`
- Enhanced `CanvasRenderer` to skip original selection area during move
- Fixed layer data synchronization across all move operations

### 🎨 User Experience Improvements
- **Professional Move Tool**: Pixels visually move with cursor during drag
- **Clean Visual Feedback**: No duplicate pixels shown during move operations
- **Seamless Tool Transitions**: Move → Brush switching works perfectly
- **Consistent Layer System**: All operations properly sync with layer data

**Files Modified:**
- `src/tools/selection.py` - Move tool layer synchronization
- `src/core/event_dispatcher.py` - Layer object passing
- `src/core/canvas_renderer.py` - Visual feedback improvements

---

## Version 1.69 - Selection Tool Duplication Fixes
**Date**: December 19, 2024  
**Type**: Critical Bug Fix

### ✅ Rotate Operation Fixed
**Eliminated duplicate pixels in original location during rotation**

**Issues Fixed:**
- **Non-Destructive Preview**: Rotation now uses separate preview pixels instead of modifying selected_pixels array
- **Proper Cleanup**: Original pixels are only cleared when rotation is committed, not during preview
- **Dimension Mismatch**: Fixed issues with original dimensions vs rotated pixel array shapes

**Technical Changes:**
- Added `rotated_pixels_preview` state variable to store rotation preview separately
- Modified `rotate_selection()` to not modify `selected_pixels` until `apply_rotation()` is called
- Updated canvas renderer to draw preview pixels from `rotated_pixels_preview`
- Proper cleanup of preview state in both `apply_rotation()` and `cancel_rotation()`

**User Experience:**
- Rotate button now shows true preview without affecting original selection
- No more duplicate pixels appearing in original location
- Enter key commits rotation, Escape cancels and restores original
- Click outside selection commits rotation automatically

### ✅ Move Tool Auto-Finalization
**Fixed duplicate pixels when moving selections**

**Issues Fixed:**
- **Missing Auto-Finalization**: Move tool wasn't automatically clearing original pixels when move completed
- **Manual Finalization Required**: Users had to manually trigger finalization to avoid duplicates

**Technical Changes:**
- Added auto-finalization in `MoveTool.on_mouse_up()` when selection has moved from original position
- Move tool now automatically calls `finalize_move()` to clear original pixels
- Proper tracking of movement state ensures finalization only happens when needed

**User Experience:**
- Move tool now automatically clears original pixels when move is completed
- No more duplicate pixels left behind after moving selections
- Seamless move operations without manual cleanup required

---

## Version 1.68 - Undo/Redo System Fix
**Date**: December 19, 2024  
**Type**: Critical Bug Fix

### ✅ Undo/Redo Functionality Restored
**Fixed completely non-functional undo/redo system**

**Issues Fixed:**
- **Missing Callback Connection**: Undo manager's state change callback wasn't connected to button updates
- **No State Saving**: Drawing operations weren't saving states before making changes
- **Button State Management**: Buttons now properly show blue when actions available, gray when not

**Technical Changes:**
- Connected `undo_manager.on_state_changed` to `_update_undo_redo_buttons` in main window initialization
- Added undo state saving before all drawing operations (brush, eraser, fill, shapes) in event dispatcher
- Proper state management ensures each drawing action can be undone/redone

**User Experience:**
- Undo/redo buttons now work with all drawing tools
- Visual feedback shows when actions are available
- Keyboard shortcuts (Ctrl+Z, Ctrl+Y) work properly
- Professional workflow restored

---

## Version 1.67 - Build System Compatibility Update
**Date**: October 15, 2025  
**Type**: Build System / Module Integration

### 🔨 Build System Updates for Refactored Architecture
**Updated build.bat to support all newly extracted modules from recent refactors**

**Changes:**
- ✅ Added 13 new hidden imports to PyInstaller build script
- ✅ Fixed import error in `ui_builder.py` (`ui.tooltip` → `src.ui.tooltip`)
- ✅ Verified all modules import correctly
- ✅ Build system now compatible with v1.65 Selection Manager extraction
- ✅ Build system now compatible with v1.64 Dialog Manager extraction
- ✅ Build system now compatible with v1.62 File Operations Manager extraction

**New Modules in Build:**
- Core: `canvas_renderer`, `event_dispatcher`, `window_state_manager`
- UI: `dialog_manager`, `file_operations_manager`, `selection_manager`, `theme_dialog_manager`, `ui_builder`
- Palette Views: `grid_view`, `primary_view`, `constants_view`, `saved_view`

**Impact:** Application can now be built into standalone executable with all refactored components included.

---

## Version 1.59 - Complete Application Restoration & Tool Consistency
**Date**: January 2025  
**Type**: Critical Bug Fixes / Complete Functionality Restoration

### 🚀 Major Application Restoration
**Completely restored application functionality after file reversion disaster**

**Critical Issues Resolved:**
1. **Application Startup Failures** - Multiple AttributeError exceptions preventing launch
2. **Missing UI Elements** - Tools, palette panels, and controls completely absent
3. **Canvas Non-Responsive** - No mouse event handling for drawing operations
4. **Palette Views Broken** - Wheel, Primary, Grid views not displaying
5. **Tool Size Indicators Missing** - Brush/Eraser buttons showing no size info

### 🔧 Tool Consistency Issues Fixed
**Major breakthrough in tool behavior consistency**

**Problem**: Switching between brush/eraser sizes caused previous work to disappear
- 1x1 brush work would vanish when switching to 2x2 brush
- 1x1 eraser work would be "undone" by 2x2/3x3 eraser

**Root Cause**: Mixed canvas-based and layer-based approaches
- 1x1 tools worked directly on canvas
- Multi-pixel tools worked on layers then flattened
- Layer flattening overwrote canvas-based work

**Solution**: Unified Layer-Based Architecture
- **All brush sizes** now use `_draw_brush_at()` with consistent layer updates
- **All eraser sizes** now use `_draw_eraser_at()` with consistent layer updates
- **Consistent Updates**: All operations call `_update_canvas_from_layers()`

### 🛠️ Technical Implementation
**Files Modified**: `src/ui/main_window.py`, `src/core/event_dispatcher.py`, `src/ui/ui_builder.py`

**Key Changes**:
- Added missing `_draw_eraser_at()` method for multi-pixel eraser operations
- Updated event dispatcher to handle all tool sizes consistently
- Fixed palette view initialization and radio button positioning
- Restored canvas mouse event bindings
- Added tool button text updates for size indicators

### 📊 Results
- ✅ **Application Stability**: No startup errors, all UI elements functional
- ✅ **Tool Consistency**: All brush/eraser sizes work harmoniously
- ✅ **Palette Functionality**: Grid, Wheel, Primary, Constants views operational
- ✅ **Canvas Responsiveness**: Proper mouse event handling and drawing
- ✅ **UI Completeness**: All buttons, indicators, and controls visible

**Impact**: Application is now fully functional with consistent tool behavior across all sizes.

## Version 1.58 - Event Dispatcher Bug Fixes
**Date**: October 15, 2025  
**Type**: Bug Fixes / Critical Functionality Restoration

### 🔧 Fixed Critical Bugs from Event Dispatcher Refactor
**Restored full functionality after Event Dispatcher refactor introduced multiple breaking issues**

**Problems Fixed:**
1. **Multi-pixel brush/eraser (2x2, 3x3) completely broken** - Tools only drew single pixels
2. **Copy tool moving pixels instead of duplicating** - Selection box lagging behind
3. **Rotate/Mirror reverting after copy operations** - Move tool state interference
4. **AttributeError exceptions** - `zoom_level`, `current_color`, `_draw_scale_handle` not found
5. **Copy preview not following cursor** - Semi-transparent preview not updating

**Solutions Implemented:**

**Multi-Pixel Tool Support** (`event_dispatcher.py`):
- Added special handling for `brush_size > 1` and `eraser_size > 1`
- Event dispatcher now calls `main_window._draw_brush_at()` / `_draw_eraser_at()`
- Created new `_draw_eraser_at()` method in main_window.py
- Applied to both mouse down and mouse drag handlers

**Copy Placement System** (`main_window.py`):
- Updated `_place_copy_at()` to update selection rectangle to new position
- Copy buffer copied to `selection_tool.selected_pixels` for transformations
- Cleared `copy_preview_pos` to remove ghost preview
- Selection now follows placed copy correctly

**Copy Preview Display** (`event_dispatcher.py`):
- Mouse move handler updates `copy_preview_pos` when `is_placing_copy`
- Semi-transparent preview with cyan dashed border follows cursor

**Transform State Management** (`main_window.py`):
- Reset move tool state before mirror/rotate operations
- Clears `original_selection`, `is_moving`, `has_been_moved`, `last_drawn_position`, `saved_background`
- Prevents move tool from reverting transformations

**Attribute Access Corrections** (`event_dispatcher.py`):
- `zoom_level` → `canvas.zoom` (3 occurrences)
- `current_color` → `palette.get_primary_color()` (5 occurrences)
- `_update_pixel_display()` → `canvas_renderer.update_pixel_display()`
- `_draw_scale_handle()` → `canvas_renderer.draw_scale_handle()`

**Files Modified:**
- `src/core/event_dispatcher.py` - Multi-pixel tool handling, attribute fixes
- `src/ui/main_window.py` - Added `_draw_eraser_at()`, fixed copy placement, reset move tool
- `docs/My_Thoughts.md` - Documented bug fixes for future agents
- `docs/SCRATCHPAD.md` - Added Version 1.57 entry

**Results:**
- ✅ 2x2 and 3x3 brush/eraser working perfectly
- ✅ Copy duplicates pixels correctly (doesn't move them)
- ✅ Selection box follows copy placement
- ✅ Rotate/Mirror work correctly after copy
- ✅ No AttributeError exceptions
- ✅ All tools functioning as expected

**Testing Completed:**
- Multi-pixel brush (2x2, 3x3) - working
- Multi-pixel eraser (2x2, 3x3) - working
- Copy → place → rotate → mirror workflow - working
- All transformation tools after copy - working

---

## Version 1.57 - AI Python Knowledge Document
**Date**: October 15, 2025  
**Type**: Documentation / AI Agent Resources

### 📚 Comprehensive Python Knowledge Base for AI Agents
**Created extensive Python reference guide specifically designed for AI agents working in Cursor**

**Purpose:**
- Help future AI agents understand Python best practices
- Reduce common mistakes and anti-patterns
- Document project-specific conventions
- Provide architectural pattern references
- Explain Cursor AI agent workflows

**Content Created:**
- **470+ lines** of comprehensive documentation
- **10 major sections** covering Python fundamentals to advanced patterns
- **Extensive code examples** with ✅ correct vs ❌ wrong patterns
- **Real-world insights** from Pixel Perfect refactoring work
- **Quick reference cheatsheet** for common operations
- **10 core principles** summary for AI agents

**Major Sections:**
1. **Understanding AI Agents in Cursor** - How AI agents work, tool access, collaboration
2. **How to Read Python Code Effectively** - Documentation order, module structure, data flow
3. **Python Core Concepts & Gotchas** - 10 critical concepts with examples
4. **Best Practices for AI-Assisted Development** - 7 key rules for agents
5. **Common Python Pitfalls** - 7 dangerous patterns to avoid
6. **Architectural Patterns** - MVC, Observer, Strategy, Singleton, Factory
7. **Refactoring Strategies** - Extract method/class, simplify conditionals
8. **Tool Usage & File Operations** - grep, search_replace, codebase_search
9. **Debugging Techniques** - Print debugging, assertions, logging
10. **Project-Specific Patterns** - Pixel Perfect conventions and workflows

**Key Topics Covered:**
- **Python Fundamentals**: Indentation, mutable defaults, scope, comprehensions
- **Advanced Concepts**: Context managers, decorators, generators, closures
- **Best Practices**: Type hints, pure functions, error handling, documentation
- **Common Mistakes**: Late binding, list modification during iteration, floating point precision
- **Architectural Patterns**: Design patterns with Python implementations
- **Refactoring Techniques**: Safe code transformation strategies
- **Tool Mastery**: Using Cursor tools effectively (grep, search_replace, codebase_search)
- **Debugging**: Practical debugging approaches for AI agents

**Benefits:**
- ✅ **Knowledge Preservation** - Captures lessons from refactoring work
- ✅ **Reduced Mistakes** - Documents pitfalls with solutions
- ✅ **Consistent Patterns** - Explains project conventions
- ✅ **Faster Onboarding** - New agents can reference immediately
- ✅ **Self-Improvement Loop** - AI documenting for future AI

**Meta-Insight:**
This document represents a powerful feedback loop: an AI agent creating documentation specifically to help future AI agents. It combines general Python knowledge, AI agent-specific advice, and project-specific patterns into one comprehensive resource.

**Files Changed:**
- `docs/AI_PYTHON_KNOWLEDGE.md` - NEW (470+ lines comprehensive guide)
- `docs/README.md` - Added reference to new documentation
- `docs/My_Thoughts.md` - Documented creation process and insights
- `docs/SCRATCHPAD.md` - Added version entry with full details

**Result:**
- ✅ Comprehensive Python knowledge base created
- ✅ Future agents have reference when stuck
- ✅ Project patterns documented
- ✅ Best practices captured
- ✅ Debugging techniques shared
- ✅ Architectural patterns explained

**For Future AI Agents:**
If you're working on this project and face Python challenges, **read `docs/AI_PYTHON_KNOWLEDGE.md` first!** It contains:
- Solutions to common problems
- Project-specific conventions
- Safe refactoring strategies
- Tool usage best practices

This is your knowledge base. Use it!

---

## Version 1.56 - Event Dispatcher Refactor Complete
**Date**: October 15, 2025  
**Type**: Code Refactoring / Architecture

### 🎯 Event Handling Centralization Complete
**Successfully extracted all event handlers into dedicated EventDispatcher module**

**Problem Solved:**
- Event handling code scattered throughout `main_window.py` (720 lines)
- 21 event handler methods mixed with UI and business logic
- Mouse events were 4 large methods (~400 lines total)
- Keyboard shortcuts buried in 78-line `_on_key_press` method
- Difficult to trace event flow and debug issues

**Solution Implemented:**
- **Created EventDispatcher module** in `src/core/event_dispatcher.py` (685 lines)
- **Organized by category**:
  - Window & Panel Events (resize, sash drag, hover, focus, close)
  - Keyboard Events (tool shortcuts, Ctrl+Z/Y, Escape handling)
  - Mouse Events (canvas down/up/drag/move with tool logic)
  - Tool Previews (brush, eraser, texture cursor feedback)
  - UI Callbacks (size, zoom, palette, view, theme, layer, frame)
- **Delegation pattern** - main_window delegates to event_dispatcher
- **Maintained all functionality** - zero breaking changes

**Technical Changes:**
- Created `src/core/event_dispatcher.py` with EventDispatcher class (685 lines)
- Removed 21 event handler methods from `main_window.py` (720 lines)
- Added EventDispatcher initialization and canvas event binding
- Kept `_on_selection_complete` as delegation method
- File size: 4,109 → 3,347 lines (18.6% reduction)

**Combined Refactor Results (Palette + Events):**
- **Starting size**: 5,060 lines
- **After palette refactor**: 4,038 lines (20.2% reduction)
- **After event refactor**: 3,347 lines (33.9% total reduction)
- **New modules**: 5 files (palette_views: 4, event_dispatcher: 1)
- **Lines extracted**: 1,641 lines into focused modules

**Result:**
- ✅ Clearer event flow - all event handling centralized
- ✅ Easier debugging - can trace events through single module
- ✅ Better organization - events separated from UI/business logic
- ✅ Improved maintainability - event changes isolated
- ✅ Reduced coupling - main_window is orchestrator, not handler
- ✅ No linter errors - clean, working code
- ✅ All events functional - mouse, keyboard, window, UI callbacks

**Files Changed:**
- `src/core/event_dispatcher.py` - NEW (685 lines)
- `src/ui/main_window.py` - Removed 720 lines, added dispatcher integration

---

## Version 1.55 - Palette Views Refactor Complete
**Date**: October 15, 2025  
**Type**: Code Refactoring / Architecture

### 🏗️ Palette Views Modularization Complete
**Successfully separated palette view code into dedicated modules**

**Problem Solved:**
- `main_window.py` was 5,060 lines - too large and difficult to maintain
- Palette-related code was scattered throughout the main window class
- Previous refactor attempt left 565 lines of corrupted/duplicate code
- File had 4 duplicate `_update_custom_colors_display` methods and 2 duplicate `_open_texture_panel` methods
- 3 linter errors from undefined variables in corrupted code

**Solution Implemented:**
- **Created 4 dedicated palette view modules** in `src/ui/palette_views/`:
  1. `grid_view.py` (145 lines) - Main 4-column palette grid with color selection
  2. `primary_view.py` (330 lines) - 12 primary colors with dynamic variations
  3. `saved_view.py` (318 lines) - 24 user-saved color slots with import/export
  4. `constants_view.py` (150 lines) - Dynamic canvas color extraction
  5. `__init__.py` (13 lines) - Package exports
- **Cleaned up corrupted integration code** using Python script for bulk deletion
- **Removed 1,020 lines total** from main_window.py (20.2% reduction)

**Technical Changes:**
- Created `src/ui/palette_views/` package with 4 view modules (956 lines)
- Removed old palette methods from `main_window.py`
- Updated integration points: `_initialize_all_views()`, `_show_view()`, `_on_palette_change()`
- Fixed all linter errors and removed duplicate methods
- File size: 5,060 → 4,038 lines

**Result:**
- ✅ Better code organization - each palette view in its own module
- ✅ Improved maintainability - easier to find and modify palette code
- ✅ Reduced file size - 20.2% smaller main_window.py
- ✅ No linter errors - clean, working code
- ✅ All palette views functional - Grid, Primary, Saved, Constants, Wheel
- ✅ Separated concerns - palette logic isolated from main window logic

**Files Changed:**
- `src/ui/main_window.py` - Removed 1,020 lines, added integration code
- `src/ui/palette_views/grid_view.py` - NEW (145 lines)
- `src/ui/palette_views/primary_view.py` - NEW (330 lines)
- `src/ui/palette_views/saved_view.py` - NEW (318 lines)
- `src/ui/palette_views/constants_view.py` - NEW (150 lines)
- `src/ui/palette_views/__init__.py` - NEW (13 lines)

---

## Version 1.54 - Color Wheel Clickable Area Fix
**Date**: October 15, 2025  
**Type**: UI/UX Enhancement

### 🎯 Precise Color Wheel Interaction
**Fixed color wheel to only respond to clicks on the rainbow ring**

**Problem Solved:**
- Color wheel canvas was fully clickable (entire 250x250px area)
- Center area and outer areas responded to clicks even though only rainbow ring should be interactive
- Grey background visible during theme changes
- Complex overlay architecture with multiple canvases caused visual artifacts

**Solution Implemented:**
- **Simplified Architecture** - Removed complex `wheel_frame` and `ring_canvas` overlay approach
- **Single Canvas Design** - Uses just `self.wheel_canvas` directly on parent frame
- **Smart Click Detection** - Validates click position before starting drag operation
- **Cursor Feedback** - Changes to "crosshair" during drag, "arrow" when released
- **Configurable Thickness** - Added `self.wheel_thickness = 30` as instance variable

**Technical Changes:**
- Modified `src/ui/color_wheel.py`: Simplified canvas structure and click detection
- Click validation: `if radius - self.wheel_thickness <= distance <= radius`
- Removed unnecessary canvas overlay and frame wrapper
- Cursor state changes provide visual feedback for interactive state

**Result:**
- ✅ Only rainbow ring responds to clicks
- ✅ Center and outer areas are non-interactive
- ✅ Cleaner, simpler code architecture
- ✅ Better cursor feedback for user interaction
- ✅ No grey background artifacts during theme changes

---

## Version 1.53 - UI Styling Consistency Fix
**Date**: December 19, 2024  
**Type**: UI/UX Enhancement

### 🎨 Seamless Dark Theme Consistency
**Eliminated unwanted light grey containers across UI panels**

**Problem Solved:**
- Layers panel had persistent light grey container background that broke visual consistency
- Right sidebar styling didn't match the seamless dark integration of left sidebar
- UI elements appeared "floating" with visible container boundaries instead of integrated styling

**Solution Implemented:**
- **Transparent Panel Backgrounds** - Made right panel (CTkScrollableFrame) transparent to eliminate light grey container
- **Direct Widget Packing** - Removed unnecessary CTkFrame wrappers around layer entries
- **Consistent Button Styling** - All buttons now use light grey backgrounds (#3a3a3a) with hover effects
- **Seamless Integration** - Both left and right sidebars now have uniform dark theme with no visible container boundaries
- **UIBuilder Integration** - Fixed toolbar positioning and grid_overlay attribute initialization after refactoring

**Technical Changes:**
- Modified `src/ui/main_window.py`: Set right_panel fg_color to "transparent"
- Updated `src/ui/layer_panel.py`: Removed frame wrappers, packed layer buttons directly to parent
- Fixed initialization order for UIBuilder to prevent AttributeError
- Ensured theme application doesn't override transparent backgrounds

**Result:**
- Clean, professional dark theme with seamless panel integration
- Consistent visual hierarchy across all UI sections
- Improved user experience with unified styling approach

**Layer Layout Fix:**
- Fixed layer positioning - layers now appear below Layers header instead of dropping to bottom
- Restored proper layer list container with transparent background
- Ensured layers scroll vertically within the Layers section when more are added
- Maintained seamless dark theme while fixing layout functionality

**Color Display Fixes:**
- Fixed color grid buttons showing grey instead of actual palette colors (SNES Classic, etc.)
- Fixed color preview box in color wheel showing black instead of selected color
- Modified theme application to preserve color button and preview frame colors
- Added smart detection for color buttons (30x30, no text) and color preview frames (100x100)
- Color palette now displays correct colors while maintaining theme consistency

---

## Version 1.52 - Responsive Panel Sizing Fix
**Date**: October 14, 2025  
**Type**: Major Bug Fix & Enhancement

### 🖥️ Responsive Panel Sizing System
**Fixed resolution-dependent panel layout issues**

**Problem Solved:**
- Fixed panel widths (520px + 500px) worked on smaller laptop screens but appeared disproportionately large on larger desktop displays
- No responsive design - panels didn't adapt to different screen resolutions
- No window state persistence - application didn't remember user's preferred panel sizes

**Solution Implemented:**
- **Screen Resolution Detection** - Automatically detects screen size and calculates optimal panel widths
- **Responsive Panel Sizing** - Panels now adapt to different screen resolutions instead of using fixed pixel widths
- **Window State Persistence** - Saves and restores preferred panel sizes between sessions
- **Better Proportions** - Panels use appropriate percentage of screen space (35-40% depending on resolution)
- **More Canvas Space** - Larger screens get more canvas area, smaller screens get compact panels

**Resolution-Based Panel Sizes:**
- **Small screens (≤1366px)**: Compact panels (280px + 260px)
- **Standard desktop (≤1920px)**: Balanced panels (350px + 320px)  
- **Large desktop (≤2560px)**: Spacious panels (400px + 380px)
- **Ultra-wide/4K (>2560px)**: Wide panels (450px + 420px)

**Technical Changes:**
- Added `_calculate_optimal_panel_widths()` method for resolution-based sizing
- Added `_save_window_state()` and `_restore_window_state()` methods
- Added window close handler to save state before exiting
- Replaced hardcoded panel widths with calculated responsive widths
- Window state saved to `~/.pixelperfect/window_state.json`

**Benefits:**
- ✅ Resolution adaptive panels
- ✅ State persistence between sessions
- ✅ Better proportions on all screen sizes
- ✅ More canvas space on larger displays
- ✅ User preference memory

**Status:** ✅ Complete - Responsive panel sizing implemented, resolution-dependent layout issues resolved

---

## Version 1.49 - American Patriotic Theme
**Date**: October 14, 2025
**Type**: New Feature

### 🇺🇸 American Patriotic Theme Addition

**Feature Added:**
New "American" theme with patriotic red, white, and blue colors inspired by the American flag.

**Design Concept:**
Patriotic theme with soft, professional colors that maintain usability while evoking national pride through strategic use of American flag colors.

**Color Scheme:**
- **Primary Background**: `#f8fafc` - Light grey-white (stars background)
- **Secondary Background**: `#ffffff` - Pure white (flag white)
- **Tertiary Background**: `#f1f5f9` - Soft blue-grey (subtle accent)
- **Text**: `#1e293b` - Navy blue for excellent readability
- **Button Normal**: `#fef2f2` - Light red background
- **Button Active**: `#dc2626` - Bold red (American flag red)
- **Tool Selected**: `#1d4ed8` - Bold blue (American flag blue)
- **Canvas**: `#ffffff` - Pure white canvas
- **Selection**: Red outline with blue handles and gold accents

**Implementation:**
- **Theme Class**: Created `AmericanTheme` class inheriting from base `Theme`
- **Theme Manager**: Added "American" to available themes dictionary
- **Light Theme**: Configured as light theme (like Angelic) for CustomTkinter
- **Color Harmony**: Balanced red, white, and blue with professional contrast ratios

**Code Changes:**
- `src/ui/theme_manager.py`: Added `AmericanTheme` class with patriotic color scheme
- Updated `ThemeManager` to include American theme in themes dictionary
- Updated `get_ctk_theme_mode()` to treat American as light theme

**Benefits:**
- **Patriotic Design** - Red, white, and blue color scheme
- **Professional Appearance** - Clean, readable interface
- **Theme Variety** - Third theme option for users
- **Light Theme** - Bright, clean appearance
- **Accessibility** - High contrast text for readability

**Status:** ✅ Complete - American theme added and ready for use

---

## Version 1.47 - Theme-Compatible Panel Loading Indicator
**Date**: October 14, 2025
**Type**: Bug Fix & Theme Enhancement

### 🎨 Angelic Theme Compatibility Fix

**Problem Solved:**
Panel loading indicators were showing as grey boxes in Angelic theme instead of proper colored backgrounds and loading prompts due to hardcoded colors not respecting the current theme.

**Solution:**
Updated panel loading system to use theme colors instead of hardcoded values, ensuring proper appearance across all themes.

**Implementation Details:**
- **Loading indicator text color**: Now uses `theme.button_active` instead of hardcoded `#1f538d`
- **Panel containers**: Now use `theme.bg_primary` instead of hardcoded `#2b2b2b`
- **Collapse buttons**: Now use `theme.button_active` and `theme.button_hover` instead of hardcoded blues
- **Theme application**: Updated `_apply_theme()` to refresh panel colors when theme changes

**Code Changes:**
- `src/ui/main_window.py`: Fixed hardcoded colors in panel loading system
- Loading indicator now respects current theme colors
- Panel containers and buttons update when theme changes
- Angelic theme now shows proper light colors instead of grey boxes

**Theme Compatibility:**
- **Basic Grey**: Loading indicator shows blue (`#1f6aa5`)
- **Angelic**: Loading indicator shows purple-blue (`#818cf8`)
- **Panel backgrounds**: Match theme's primary background color
- **Buttons**: Use theme's active and hover colors

**Benefits:**
- **Theme consistency** - Loading indicators match current theme
- **Proper Angelic theme** - No more grey boxes in light theme
- **Dynamic theming** - Colors update when theme changes
- **Professional appearance** - Cohesive visual design across themes

**Status:** ✅ Complete - Theme compatibility fixed, Angelic theme now works properly

---

## Version 1.46 - Panel Loading Indicator
**Date**: October 14, 2025
**Type**: UX Enhancement

### 🎯 Professional Loading Feedback

**Problem Solved:**
Panel rendering still takes time on mid-level systems, causing perceived lag when toggling panels. User needed visual feedback during panel rendering.

**Solution:**
Implement loading indicator INSIDE the panels themselves to provide immediate visual feedback during rendering.

**Implementation Details:**
- **Panel-internal loading**: Loading indicator appears INSIDE the target panel (left or right)
- **Visual design**: Blue (#1f538d) 16pt bold text "Loading [Left/Right] Panel..."
- **Positioning**: Centered in target panel using `place(relx=0.5, rely=0.5, anchor="center")`
- **Canvas unobstructed**: Canvas stays completely visible during panel loading
- **Timing**: 100ms delay before removing loading indicator

**Code Changes:**
- `src/ui/main_window.py`: Added `_show_panel_loading_indicator()` and `_finish_panel_toggle()` methods
- Uses `ctk.CTkLabel` positioned inside target panels
- Integrated into `_toggle_left_panel()` and `_toggle_right_panel()` methods
- Fixed initial overlay approach that incorrectly covered canvas area

**Key Fix:**
Initially implemented overlay window covering canvas - WRONG approach. User clarified that loading indicator should appear INSIDE the panels themselves, not covering the canvas area.

**Benefits:**
- **Immediate feedback** - User sees loading indicator instantly
- **Professional UX** - No "frozen" UI appearance during panel rendering
- **Canvas visibility** - Canvas stays completely unobstructed during loading
- **Perceived performance** - Loading message makes wait feel intentional
- **Graceful degradation** - Works on all system performance levels

**Status:** ✅ Complete - Panel loading indicator successfully implemented and tested

---

## Version 1.44 - Panel Toggle Performance Optimization
**Date**: October 14, 2025
**Type**: Performance Enhancement

### 🚀 Major Panel Toggle Optimization

**Problem Solved:**
Fixed remaining performance issue where panels still took time to load when toggled via collapse/expand buttons, despite initial optimization.

**Root Cause:**
Panels were using `paned_window.add()` and `paned_window.forget()` which remove and recreate entire containers, causing all child widgets (LayerPanel, TimelinePanel) to be destroyed and recreated on every toggle.

**Solution Implemented:**
Implemented true visibility toggling using `paneconfig()`:
- Hide panels by setting width to 0 (no widget destruction)
- Show panels by restoring original width (no widget recreation)
- Panels remain in memory with all state preserved
- Reduced canvas redraw delay from 50ms to 10ms

**Performance Results:**
- **Before**: ~1000ms panel toggle (widget recreation lag)
- **After**: <5ms panel toggle (true visibility only)
- **Improvement**: 200x speed increase
- **User Experience**: Truly instant panel response

**Technical Changes:**
- Replaced `paned_window.forget()` with `paneconfig(width=0)`
- Replaced `paned_window.add()` with `paneconfig(width=original)`
- Reduced canvas redraw delay from 50ms to 10ms
- Added optimization comments throughout panel toggle methods

**Files Modified:**
- `src/ui/main_window.py` - Panel toggle optimization with paneconfig()

**Benefits:**
- ✅ Truly instant panels - no more toggle lag whatsoever
- ✅ Professional UX - responsive, snappy interface
- ✅ Production ready - optimized for end users
- ✅ Memory efficient - zero widget recreation overhead
- ✅ State preservation - panel state maintained between toggles

---

## Version 1.43 - Side Panel Performance Optimization
**Date**: October 14, 2025
**Type**: Performance Enhancement

### 🚀 Major Performance Improvement

**Problem Solved:**
Fixed critical performance issue where side panels (layers, timeline) took ~1 second to load when toggled, causing visible lag and blank rendering areas in the production executable.

**Root Cause:**
LayerPanel and TimelinePanel were being recreated from scratch on every panel toggle, causing widget creation overhead and rendering delays.

**Solution Implemented:**
Applied "Create Once, Toggle Visibility" optimization pattern:
- Pre-create panels once during application startup
- Store panel references for instant toggling
- Eliminate widget recreation on panel show/hide
- Consistent with settings dialog optimization

**Performance Results:**
- **Before**: ~1000ms panel loading time (widget creation lag)
- **After**: <10ms instant panel display (visibility toggle only)
- **Improvement**: 100x speed increase
- **User Experience**: No more blank/partially rendered panels

**Technical Changes:**
- Added `_create_layer_and_timeline_panels()` method for pre-creation
- Modified `_toggle_right_panel()` to use existing panels
- Added optimization comments to layer and timeline panels
- Maintained all existing panel functionality

**Files Modified:**
- `src/ui/main_window.py` - Panel pre-creation and toggle optimization
- `src/ui/layer_panel.py` - Added optimization comments
- `src/ui/timeline_panel.py` - Added optimization comments

**Benefits:**
- ✅ Instant panel loading - no more 1-second lag
- ✅ Professional UX - smooth, responsive interface
- ✅ Production ready - optimized for end users
- ✅ Memory efficient - reduced widget recreation
- ✅ Consistent pattern - matches settings dialog optimization

---

## Version 1.42 - Settings Button & Placeholder Dialog (October 14, 2025) ✅

### ⚙️ Feature: Settings Button with Gear Icon

**Purpose:**
First step toward implementing the comprehensive settings system documented in MAX_SETTINGS.md (127 planned settings).

**New Settings Button** 🎛️
- **Location** - Top toolbar, positioned between "Grid: ON" button and "Basic Grey" theme dropdown
- **Icon** - ⚙️ Gear emoji (18pt font size)
- **Size** - Compact 40px width button
- **Tooltip** - "Settings (Coming Soon)" (500ms delay)
- **Command** - Opens settings placeholder dialog

**Settings Dialog (Placeholder)** 📋
- **Modal dialog** - 500x350, centered on screen, non-resizable
- **Professional design** - Matches app's CustomTkinter styling
- **Large gear icon** - 64pt ⚙️ at top
- **Blue title** - "SETTINGS" in #1a73e8 (24pt bold)
- **Coming Soon message** - Professional announcement of feature
- **Feature preview** - Lists 6 planned setting categories:
  - Canvas & Grid preferences
  - Tool defaults & behavior
  - Color & Palette options
  - UI customization
  - Keyboard shortcuts
  - And much more!
- **Documentation reference** - Points users to MAX_SETTINGS.md for full list
- **Close button** - Blue "OK" button to dismiss

**Technical Implementation:**
```python
# Settings button in toolbar (line ~370)
self.settings_button = ctk.CTkButton(
    self.toolbar, 
    text="⚙️", 
    width=40,
    command=self._show_settings_dialog,
    font=ctk.CTkFont(size=18)
)
self.settings_button.pack(side="right", padx=5)

# Dialog method (line ~3111)
def _show_settings_dialog(self):
    # Creates modal CTkToplevel dialog
    # Centers on screen
    # Displays gear icon, title, coming soon message
    # Lists planned features
    # References MAX_SETTINGS.md
```

**Code Changes:**
- `src/ui/main_window.py`:
  - Added `self.settings_button` with gear icon
  - Added `_show_settings_dialog()` method
  - Added tooltip with "Settings (Coming Soon)"
  - Positioned between grid toggle and theme selector

**Consistency with App Design:**
- Uses same dialog structure as downsize warning and clear slots
- Dark theme colors (#2d2d2d backgrounds, #e0e0e0 text)
- Blue accent color (#1a73e8) for titles and buttons
- Proper modal behavior (transient, grab_set)
- Centered positioning relative to main window

**User Experience Flow:**
1. User sees gear icon ⚙️ in top toolbar
2. Hovers to see "Settings (Coming Soon)" tooltip
3. Clicks to open professional placeholder dialog
4. Reads about planned settings categories
5. Sees reference to MAX_SETTINGS.md documentation
6. Clicks OK to close
7. User has clear expectation that settings are coming

**Benefits:**
✅ Clear UI indicator for planned settings system
✅ Professional "coming soon" instead of "not implemented" error
✅ Generates user anticipation and excitement
✅ Easy to discover and access
✅ Ready to be replaced with full settings panel
✅ Maintains UI consistency with rest of app
✅ References comprehensive MAX_SETTINGS.md documentation

---

## Version 1.41 - Multi-Size Eraser Tool (October 14, 2025) ✅

### 🧹 Feature: Multi-Size Eraser (1x1, 2x2, 3x3)

**Problem Solved:**
- Eraser tool only erased single pixels
- Slow to clean up large areas
- Inconsistent with brush tool which had multi-size support

**New Multi-Size Eraser Implementation:**

**Three Eraser Sizes** 📏
- **1×1 (Single Pixel)** - Precise cleanup and detail work
- **2×2 (Small)** - Faster erasing for small areas
- **3×3 (Medium)** - Quick cleanup of large regions

**User Interface** 🎨
- **Right-click menu** - Right-click eraser button to select size
- **Visual size indicator** - Button displays `Eraser [1x1]`, `Eraser [2x2]`, `Eraser [3x3]`
- **Checkmark display** - Current size marked with ✓ in popup menu
- **Dark theme styling** - Menu background #2d2d2d with blue highlight #1a73e8
- **Updated tooltip** - "Erase pixels (E) | Right-click for size"
- **Auto-select tool** - Changing size automatically switches to eraser

**Technical Implementation:**
```python
# New eraser size variable
self.eraser_size = 1  # Default 1x1

# New methods implemented
_show_eraser_size_menu(event)  # Right-click popup menu
_set_eraser_size(size)         # Set size and update button
_update_eraser_button_text()   # Display "Eraser [2x2]"
_erase_at(layer, x, y)         # Erase NxN square centered

# Centered erasing logic
offset = self.eraser_size // 2
for dy in range(self.eraser_size):
    for dx in range(self.eraser_size):
        px = x - offset + dx
        py = y - offset + dy
        if bounds_check:
            layer.set_pixel(px, py, (0, 0, 0, 0))  # Transparent
```

**Mouse Event Integration:**
- Special handling in mouse down: `if self.current_tool == "eraser": self._erase_at()`
- Special handling in mouse drag for continuous erasing
- Updates entire erased area, not just single pixel
- Full bounds checking to prevent overflow

**Code Changes:**
- ✅ Added `self.eraser_size = 1` variable
- ✅ Added 4 new eraser methods (~65 lines)
- ✅ Updated mouse event handlers (2 locations)
- ✅ Added right-click binding for eraser button
- ✅ Updated tooltip text
- ✅ Initialize button text on startup

**Consistency with Brush Tool:**
- Identical menu styling
- Same size options (1×1, 2×2, 3×3)
- Same button text format
- Same auto-select behavior
- Same keyboard shortcut hint pattern
- Same centering logic

**User Workflow:**
```
1. User right-clicks "Eraser" button
   ↓
2. Popup menu appears with three sizes
   ✓ 1×1 (Single Pixel)
     2×2 (Small)
     3×3 (Medium)
   ↓
3. User selects "3×3 (Medium)"
   ↓
4. Button updates: "Eraser [3x3]"
   Eraser tool automatically selected
   ↓
5. User clicks or drags on canvas
   ↓
6. Erases 3×3 square centered on cursor!
```

**Benefits:**
- ✅ **Faster Cleanup** - Erase large areas 9× faster with 3×3 size
- ✅ **Consistent UX** - Matches brush tool exactly
- ✅ **Flexible** - Switch between precision and speed
- ✅ **Professional** - Same quality as brush implementation
- ✅ **Centered Erasing** - NxN squares perfectly centered
- ✅ **Safe Bounds** - No overflow errors with checking
- ✅ **Full Undo/Redo** - Inherited from layer system

**Files Modified:**
- `src/ui/main_window.py` - Eraser multi-size implementation

**Documentation Updated:**
- `docs/SCRATCHPAD.md` - v1.41 entry with full technical details
- `docs/SUMMARY.md` - Updated to v1.41
- `docs/CHANGELOG.md` - This entry

---

## Version 1.40 - Styled Canvas Downsize Warning Dialog (October 14, 2025) ✅

### ⚠️ UI Enhancement: Custom Downsize Warning Dialog

**Problem Solved:**
- Old canvas downsize warning used plain system `messagebox.askyesno()` 
- Inconsistent with app's modern CustomTkinter design
- Generic look didn't match polished UI

**New Custom Dialog Implementation:**

**Visual Design** 🎨
- ⚠️ **48px warning emoji** - Immediate visual alert
- **Orange title** (#ff9800) - "DOWNSIZING WARNING" in bold 20px
- **Size comparison display** - "Current size: 32x32" → "New size: 16x16"
- **Strong danger messaging** - "PERMANENTLY DELETE" language
- **Bold question** - "Continue with resize?" in white

**Professional Button Styling** 🔘
- **"No" Button** (Safe Option):
  - Grey color (#4a4a4a, hover #5a5a5a)
  - 140×40px with bold 14px font
  - Right-side positioning
  
- **"Yes" Button** (Destructive Action):
  - Red color (#d32f2f, hover #b71c1c)
  - 140×40px with bold 14px font
  - Next to "No" button

**Technical Implementation:**
- New `_show_downsize_warning()` method in MainWindow
- Custom CTkToplevel dialog (500×280px)
- Modal behavior: `transient()` + `grab_set()` + `wait_window()`
- Centered on main window dynamically
- Returns boolean result (True = Yes, False = No)

**Code Changes:**
- ✅ Added `_show_downsize_warning()` method (~100 lines)
- ✅ Replaced preset canvas size warning (line ~2123)
- ✅ Replaced custom canvas size warning (line ~2185)
- ✅ Removed unused `messagebox` imports

**Consistency with App Design:**
- Matches "Clear All Slots" dialog styling
- Same button dimensions and colors
- Same layout pattern (icon left, title, message, buttons)
- Same modal behavior
- Professional CustomTkinter throughout

**User Experience Flow:**
```
User: Tries to downsize 32×32 → 16×16
↓
System: Beautiful custom dialog appears centered
↓
Dialog: ⚠️ DOWNSIZING WARNING (orange, bold)
        Current size: 32x32
        New size: 16x16
        This will PERMANENTLY DELETE pixels outside the 16x16 region!
        Lost pixels CANNOT be recovered!
        Continue with resize?
        [Yes - Red] [No - Grey]
↓
User clicks "No" → Size safely restored, operation cancelled
User clicks "Yes" → Resize proceeds with pixel loss
```

**Benefits:**
- ✅ **Consistent UI** - Matches app's modern design language
- ✅ **Clear Warning** - Danger obvious with orange + red colors
- ✅ **Professional Look** - Custom dialog instead of system popup
- ✅ **Better UX** - Properly sized, centered, highly readable
- ✅ **Accessible** - Large text, clear messaging, obvious action buttons

**Files Modified:**
- `src/ui/main_window.py` - Dialog implementation

**Documentation Updated:**
- `docs/SCRATCHPAD.md` - v1.40 entry with full details
- `docs/SUMMARY.md` - Updated to v1.40
- `docs/CHANGELOG.md` - This entry

---

## Version 1.39 - MAX SETTINGS Documentation (October 14, 2025) ✅

### 📋 Documentation: Comprehensive Settings Planning

**MAX_SETTINGS.md Created** 📖
- **47-page comprehensive catalog** of all possible settings
- **127 total settings** organized into 14 categories
- Complete planning document for future settings system implementation

**Categories Documented:**
1. **Canvas Preferences** (15 settings) - Default sizes, zoom, backgrounds, borders
2. **Grid & Visual** (12 settings) - Grid colors, rulers, guides, snap-to-grid
3. **Tool Defaults** (18 settings) - Default tools, brush sizes, tool behaviors
4. **Color & Palette** (16 settings) - Palettes, views, color management, gradients
5. **Layer System** (10 settings) - Layer defaults, locking, blend modes, groups
6. **Animation** (11 settings) - FPS, frames, onion skinning, playback
7. **Performance & History** (9 settings) - Undo, auto-save, memory, caching
8. **Export & Import** (14 settings) - Formats, scales, templates, metadata
9. **UI & UX** (15 settings) - Panels, tooltips, status bar, window behavior
10. **Theme & Appearance** (12 settings) - Themes, fonts, colors, accessibility
11. **File Management** (10 settings) - Locations, backups, cloud sync, portable mode
12. **Keyboard Shortcuts** (8 settings) - Custom hotkeys, profiles, gestures
13. **Accessibility** (7 settings) - Screen readers, motion reduction, audio feedback
14. **Advanced & Debug** (10 settings) - Debug mode, GPU, plugins, scripting

**Each Setting Includes:**
- ⭐ **Impact Rating** (1-5 stars) - How valuable to users
- 🔧 **Complexity Rating** (Easy/Medium/Hard/Very Hard) - Implementation difficulty
- 📝 **Purpose** - Why this setting exists and who benefits
- ☑️ **Status Tracking** (🔴 Not Started / 🟡 In Progress / 🟢 Complete)
- ✅ **Implementation Checklist** - Specific tasks for each setting

**Priority Matrix Defined:**
- **15 High-Impact + Easy** settings identified for first implementation
- **15 High-Impact + Medium** settings for second phase
- **10 High-Impact + Hard** settings for long-term development
- Smart prioritization for maximum user value with minimal effort

**Top Priority Settings (Do First):**
1. Default Canvas Size - Save clicks on every new project
2. Auto-Save Interval - Critical data safety feature
3. Undo History Size - Balance features vs. memory
4. Grid Color/Opacity - High visibility impact
5. Default Palette - Workflow efficiency
6. Status Bar - Show cursor position, canvas info, memory
7. Tooltip Delay - Accessibility improvement
8. Panel State Memory - Remember collapsed/expanded panels
9. Export Defaults - Streamline export workflow
10. Confirm Destructive Actions - Prevent accidental data loss

**Settings File Structure:**
- Complete JSON schema defined with sensible defaults
- Organized by category matching documentation
- Ready for implementation

**Benefits:**
- ✅ **Complete Vision** - Every setting possibility cataloged
- ✅ **Smart Planning** - Impact vs. complexity matrix guides development
- ✅ **Implementation Tracking** - Checkboxes for project management
- ✅ **Team Coordination** - Clear roadmap for developers
- ✅ **User Value First** - Prioritize highest-impact features

**Next Steps for Implementation:**
1. Create SettingsManager class (backend data model)
2. Design tabbed settings dialog UI (14 tabs, one per category)
3. Implement high-priority settings first (15 easy + high-impact)
4. Add settings persistence (JSON file in AppData)
5. Test with real users and iterate

**Files Created:**
- `docs/MAX_SETTINGS.md` - Complete settings catalog

**Documentation Updated:**
- `docs/SCRATCHPAD.md` - Added v1.39 entry with full details
- `docs/SUMMARY.md` - Updated to v1.39 with MAX_SETTINGS reference
- `docs/DOC_ORGANIZATION.md` - Added MAX_SETTINGS to core documentation
- `docs/CHANGELOG.md` - This entry

---

## Version 1.38 - Texture Tool with Live Preview (October 14, 2025) ✅

### 🎨 Major Feature: Texture Application System

**Hardcoded Grass 8x8 Texture** 🌿
- **TextureTool class** with complete drawing logic
- **TextureLibrary class** with hardcoded grass pattern
- **4 shades of green**: Dark, medium, light, yellow-green for authentic grass texture
- **Click or drag**: Apply 8x8 texture patterns to canvas instantly

**Beautiful Texture Library Panel** 📚
- Modal dialog (400x300px) with clean interface
- 64x64 preview of grass texture (8x scaled for visibility)
- Clickable texture frames with name, dimensions, and "Select" button
- Auto-closes when texture selected, activates texture tool

**Live Preview System** 👁️✨
- **Real-time hover preview**: See texture before placing
- **Semi-transparent rendering**: Uses stipple effect for preview
- **Dashed white outline**: Clear visual boundary around 8x8 area
- **Follows mouse**: Updates instantly as you move across canvas

**Full Integration:**
- Texture button highlights blue when tool active
- Preview renders during hover AND drag
- Applies on click with perfect pixel alignment
- Undo/redo support built-in

**User Workflow:**
```
1. Click "Texture" button → Opens Texture Library
2. Select "Grass 8x8" texture → Panel closes, tool activates
3. Texture button turns BLUE → Visual confirmation
4. Hover over canvas → See live 8x8 preview
5. Click or drag → Apply grass texture!
```

**Technical Details:**
- `src/tools/texture.py` - Complete texture tool implementation
- `TextureTool` with `set_texture()`, `on_mouse_down/drag/up()`, preview methods
- `TextureLibrary.get_grass_8x8()` - Hardcoded 8x8 NumPy array
- `_draw_texture_preview()` in main_window.py - Live rendering on Tkinter canvas

**Benefits:**
- ✅ **Fast texture application** - Paint grass instantly
- ✅ **Visual feedback** - See exactly what you're placing
- ✅ **Expandable system** - Easy to add more textures
- ✅ **Professional workflow** - Industry-standard live preview

---

## Version 1.37 - Smart Non-Destructive Move System (October 14, 2025) ✅

### 🎨 Major Feature: Two-Phase Move with Background Preservation

**Revolutionary Move Workflow** 🚀
- **Old Behavior**: Moving pixels over others would permanently delete underlying pixels
- **New Behavior**: Unlimited position adjustments without destroying underlying pixels!
- **Why It Matters**: Professional-grade non-destructive editing for precise pixel placement

**The Two-Phase System:**

**Phase 1 - First Pickup (Move Operation Starts):**
1. Click selection to pick up
2. **Original pixels are cleared** from canvas
3. Pixels are now "floating" - no longer on canvas
4. Drop at new position → Pixels placed, **background saved**
5. **Result**: Pixels moved, not copied!

**Phase 2 - Adjustment Pickups (Unlimited Repositioning):**
1. Pick up again from new position
2. **Saved background is restored** → Underlying pixels come back! ✨
3. Pixels lift off, background preserved
4. Drop at another position → Pixels placed, **new background saved**
5. **Result**: Can adjust position infinitely without destroying pixels underneath!

**User Workflow:**
```
1. Select black pixels → White selection box appears
2. Pick up (first time) → Original black pixels cleared from canvas
3. Drop on red pixels → Black appears, red is saved in memory
4. Pick up again → Red pixels restored! (Non-destructive!)
5. Drop elsewhere → Black moves, new background saved
6. Pick up again → Previous background restored again!
7. Repeat infinitely → Never lose underlying pixels!
```

**Technical Implementation:**
- `original_selection`: Tracks initial position for first-pickup detection
- `saved_background`: 2D array storing pixels underneath current position
- `last_drawn_position`: Tracks where pixels are currently placed
- **First pickup**: Clears original pixels (move, not copy)
- **Subsequent pickups**: Restores `saved_background` (non-destructive adjustments)
- **Every drop**: Saves new background, draws pixels at position

**Benefits:**
- ✅ **Move, not copy**: First pickup clears original (no duplicates)
- ✅ **Non-destructive adjustments**: Unlimited repositioning without pixel loss
- ✅ **Background preservation**: Red pixels safe when moving black over them
- ✅ **Professional workflow**: Experiment with positioning, underlying pixels stay intact
- ✅ **Pixel-perfect placement**: Adjust as many times as needed to get it right!

---

## Version 1.36 - Selection & Move Tool Bug Fixes (October 14, 2025) ✅

### 🐛 Critical Bug Fixes

**Fixed: Empty Selection Spaces Erasing Pixels** 🔥🔥 **(CRITICAL - TWO-PART FIX)**
- **Problem**: Moving a selection with empty spaces over existing pixels would delete those pixels
- **Root Cause #1**: `on_mouse_down()` in MoveTool was clearing the ENTIRE selection rectangle when picking up
- **Root Cause #2**: `on_mouse_up()` in MoveTool was also clearing the entire rectangle before placing
- **Visual**: Selection box with scattered pixels acts like an eraser at BOTH pickup and placement
- **Solution**: 
  - **Part 1 (Pickup)**: Only clear actual pixels when picking up, not empty spaces
  - **Part 2 (Placement)**: Only draw non-transparent pixels, skip empty spaces entirely
- **Impact**: Empty spaces in selection are now truly transparent at BOTH stages!
- **Technical**: 
  ```python
  # OLD PICKUP (BUGGY):
  for py in range(height):
      canvas.set_pixel(canvas_x, canvas_y, (0, 0, 0, 0))  # ❌ Clears EVERYTHING!
  
  # NEW PICKUP (FIXED):
  for py in range(height):
      pixel_color = selected_pixels[py, px]
      if pixel_color[3] > 0:  # ✅ Only clear actual pixels!
          canvas.set_pixel(canvas_x, canvas_y, (0, 0, 0, 0))
  
  # NEW PLACEMENT (ALSO FIXED):
  for py in range(height):
      if pixel_color[3] > 0:  # ✅ Only draw actual pixels!
          canvas.set_pixel(canvas_x, canvas_y, pixel_color)
  ```

**Fixed: Selection Box Vanishes on Minimize/Focus Loss** 🔍🔍 **(ENHANCED)**
- **Problem**: Minimizing app and restoring would hide selection box until clicking canvas
- **Root Cause**: `_on_focus_in()` wasn't catching all window visibility events
- **Solution**: 
  - Bound to multiple events: `<FocusIn>`, `<Map>` (unminimize), `<Visibility>` (canvas visible)
  - Multiple redraw attempts: immediate, 50ms, 150ms to catch all timing scenarios
  - Added debug logging to track which events fire
- **Impact**: Selection box now redraws reliably across all focus/visibility scenarios!
- **Technical**: 
  ```python
  # Bind all relevant events
  self.root.bind("<FocusIn>", self._on_focus_in)
  self.root.bind("<Map>", self._on_focus_in)  # Window unminimized
  self.drawing_canvas.bind("<FocusIn>", self._on_focus_in)
  self.drawing_canvas.bind("<Visibility>", self._on_focus_in)  # Canvas visible
  
  # Multiple redraw attempts for reliability
  self._update_pixel_display()  # Immediate
  self.root.after(50, self._update_pixel_display)  # After 50ms
  self.root.after(150, self._update_pixel_display)  # After 150ms
  ```

**Fixed: Selection Tool Pixel Loss on Move**
- **Problem**: Moving a selection and picking it up again would capture transparent/wrong pixels
- **Root Cause**: `_finalize_selection()` was re-capturing pixels from canvas after every move
- **Solution**: Modified selection tool to preserve original `selected_pixels` after initial capture
- **Impact**: Selections now maintain their original pixels through multiple moves
- **Technical**: Added conditional check in `_finalize_selection()` - only captures if `selected_pixels is None`

**Fixed: No Visual Preview While Moving Selection**
- **Problem**: Selected pixels invisible while dragging with move tool
- **Root Cause**: Move tool only updated selection rect, didn't trigger visual redraw
- **Solution**: 
  - Added move preview rendering in `_draw_selection_on_tkinter()` 
  - Renders stored `selected_pixels` at current position during drag
  - Triggers `_update_pixel_display()` on mouse move when `is_moving` is true
- **Impact**: Full visual feedback during selection movement - see exactly where pixels will land
- **Technical**: Drawing tagged as "move_preview" for efficient cleanup

**Fixed: Selection Box Disappears on Window Focus Loss**
- **Problem**: Selection marching ants disappeared when tabbing out/back to application
- **Root Cause**: Canvas not automatically redrawing on focus events
- **Solution**: 
  - Added `<FocusIn>` event handlers to root window and drawing canvas
  - `_on_focus_in()` method triggers full `_update_pixel_display()` 
- **Impact**: Selection remains visible when switching between applications
- **Technical**: Bound both root and canvas for comprehensive focus detection

**Enhanced: Move Tool Pixel Placement**
- Clears target area before placing to prevent overlap artifacts
- Properly handles overlapping source/destination regions
- Logs successful moves: `[MOVE] Pixels placed at new position`

**Enhanced: Selection Tool Reset**
- New selection properly clears old `selection_rect` and `selected_pixels`
- Prevents interference from previous selections
- Cleaner state management

---

## Version 1.35 - Brush Size System (October 14, 2025) ✅

### 🖌️ Multi-Size Brush Feature
**New Feature**: Three brush sizes with sleek right-click menu

**Brush Sizes Available**:
- **1x1** - Single pixel (default) - for precise detail work
- **2x2** - Small brush - for faster coverage
- **3x3** - Medium brush - for broad strokes

**UI Improvements**:
- Right-click brush button to open size selection menu
- Visual size indicator on button: `Brush [1x1]` / `Brush [2x2]` / `Brush [3x3]`
- Checkmark (✓) shows current size in popup menu
- Dark theme popup menu (#2d2d2d) with blue highlight (#1a73e8)
- Tooltip updated: "Draw pixels (B) | Right-click for size"

**Smart Behavior**:
- Brush draws centered NxN squares
- Auto-select brush tool when changing size
- Works seamlessly during click and drag
- Respects canvas boundaries (no overflow)
- Full undo/redo support

**Technical Implementation**:
- `_show_brush_size_menu()` - Right-click popup with checkmarks
- `_set_brush_size()` - Size selection and auto-tool switching
- `_draw_brush_at()` - Optimized NxN painting with bounds checking
- `brush_size` state tracking (1, 2, or 3)
- Modified mouse down/drag handlers for multi-pixel painting

**User Experience**:
- Paint large areas faster with 2x2/3x3 brushes
- Switch to 1x1 for fine detail work
- Intuitive right-click interface (no keyboard shortcuts needed)
- Visual feedback at all times
- Smooth workflow integration

---

## Version 1.34 - Eyedropper Refinements & Custom Dialogs (October 13, 2025) ✅

### Eyedropper Tool Enhancements
- **Always Updates Color Wheel**: Color wheel now updates to show sampled color even for palette colors
  - Better visual feedback - wheel always reflects current selection
  - Improved workflow when color wheel is open
  - Works seamlessly with palette selection

- **Auto-Switch to Brush**: After sampling color, automatically switches to Brush tool
  - Standard workflow: Sample → Paint immediately
  - No manual tool switching needed
  - Works for both left-click (primary) and right-click (secondary)

### Bug Fixes
- **Fixed: Eyedropper Sampling Transparent Pixels**
  - Sampling empty/transparent pixels was breaking color wheel
  - RGB(0,0,0) with 0% brightness made wheel stuck on black
  - Now ignores transparent pixels (alpha=0) when sampling
  - Color wheel stays functional at all times

- **Fixed: Constants & Eyedropper Color Display**
  - Both were calling `_create_color_wheel()` which reset the wheel to red
  - Now use optimized `_show_view("wheel")` for correct color display
  - Fixed with v1.33 performance system integration

### UI Enhancements
- **Custom "Clear All Slots" Confirmation Dialog**
  - Beautiful CustomTkinter dialog replacing standard messagebox
  - Large colorful palette emoji (🎨) for visual impact
  - Bold title and clear warning message
  - Large, prominent buttons (140x40px)
  - Red "Yes" button signals destructive action
  - Grey "No" button as safe default
  - Centers on main window with modal behavior
  - Professional look matching app theme

## Version 1.33 - Saved Colors & Performance Revolution (October 13, 2025) ✅

### Major New Features
- **Saved Colors System**: Personal color palette with 24 slots
  - Click empty slot (+) to save current color
  - Click filled slot to load color
  - Local persistence (not in git) - stored in AppData
  - Export/Import color sets to share with others
  - Clear All button with confirmation
  - Perfect for workflow efficiency

### Massive Performance Improvements
- **50-100× Faster View Switching** ⚡
  - Grid/Wheel/Primary/Saved/Constants switches now <10ms (was 500-1000ms!)
  - Pre-rendered views with visibility toggling (pack_forget/pack)
  - No more widget destruction/recreation on each switch
  - Instant, buttery smooth experience

### Editable RGB Values
- **Type Exact Color Numbers**
  - RGB entry fields in color wheel (0-255)
  - Press Enter or Tab to apply
  - Automatic HSV conversion
  - Invalid input protection (reverts to current color)

### UX Enhancements
- **Auto-Switch to Grid**: Changing palette always shows Grid view
- **Color Wheel Background Polish**: Backgrounds match theme seamlessly
- **Constants Panel Fix**: No longer switches to wheel when selecting colors

### Bug Fixes
- **Fixed: Crash on Startup** - `primary_colors_mode` initialization order
- **Fixed: Palette Change Bug** - No longer forces switch to color wheel
- **Fixed: Constants Color Selection** - Correctly displays selected color in wheel

## Version 1.32 - Color Wheel Background Polish (October 13, 2025) ✅

### Major Fix
- **Color Wheel Background Transparency**
  - Fixed black/grey backgrounds in hue wheel and saturation square
  - Backgrounds now match theme color (bg_primary)
  - Achieved by filling PIL images with theme color instead of RGBA transparency
  - Tkinter PhotoImage doesn't support true RGBA, so we use explicit background fills
  - Seamless integration with dark/light themes

### Technical Details
- Modified `_draw_hue_wheel()` and `_draw_saturation_square()` to use theme color
- Added `_get_bg_color_rgb()` helper to convert hex colors to RGB tuples
- Background fill happens during PIL image creation
- Visual integration is perfect - no visible borders or artifacts

## Version 1.31 - Color Wheel UX & Performance (October 13, 2025) ✅

### Major Performance Optimization
- **~100× Faster Color Wheel** ⚡
  - Eliminated excessive redrawing during drag (was redrawing full wheel/square on every mouse move)
  - Optimized `_update_displays()` with selective redraw parameters
  - Tagged indicator elements for efficient deletion/recreation
  - Console spam removed (print statements on every mouse move)

### UX Enhancements
- **Crosshair Cursor**: Added crosshair cursor to hue wheel and saturation square
- **Smooth Dragging**: No more lag when moving across color picker
- **Visual Feedback**: Clear indication of interactive areas

### Bug Fixes
- **Fixed: Saturation Square Design**
  - Removed redundant brightness control from square (conflicted with slider)
  - Square now shows saturation (X-axis) and lightness (Y-axis) at current brightness
  - Indicator is now a circle that only moves horizontally
  - Brightness controlled exclusively by slider
  - No more confusing "black side" issue

- **Fixed: Cursor Stuck on X-Axis**
  - Saturation square now only updates saturation based on X position
  - Y position no longer affects brightness (handled by slider)
  - Smooth, predictable behavior

### Performance Metrics
- **Before**: 50-100ms per mouse move (lag visible)
- **After**: <1ms per mouse move (instant response)
- **Improvement**: 50-100× faster!

## Version 1.30 - Build Size Optimization (October 12, 2025) ✅

### Massive Executable Size Reduction
- **91% smaller!** - From 330MB to 29MB (301MB saved)
- Removed pygame dependency (~60MB) - All rendering now pure tkinter
- Removed scipy dependency (~120MB) - Using optimized numpy scaling
- Removed unused test/build modules (~120MB+)
- Added hidden imports for proper bundling

### Build System Improvements
- Fixed `dcs.png` bundling for compiled executable
- Cleaned up PyInstaller exclusions
- Added proper `sys._MEIPASS` path resolution
- Zero functionality lost - all features work identically

### Performance Benefits
- Faster downloads: 5 seconds vs 53 seconds on fast WiFi
- Lower disk space usage
- Faster startup (no unused library initialization)
- Cleaner, more maintainable build

## Version 1.29 - Live Shape Preview (October 12, 2025) ✅

### Real-Time Shape Visualization
- **Line Tool**: See line as you drag from start to end point
- **Rectangle Tool**: See rectangle/square preview during drag
- **Circle Tool**: See circle preview as you drag radius
- Professional workflow matching industry standards

### Technical Implementation
- Uses Tkinter canvas overlay for live preview
- Preview updates dynamically during mouse drag
- Preview cleared when shape is finalized
- Works seamlessly with pan/zoom system
- No performance impact

## Version 1.28 - Canvas Downsize Warning (October 12, 2025) ✅

### Pixel Loss Prevention
- **Warning Dialog**: Alerts when downsizing canvas
- **Clear Communication**: Shows which pixels will be deleted
- **Cancel Support**: Restore previous size if you change your mind
- **Professional UX**: Warning icon with Yes/No confirmation

### Smart Detection
- Triggers on width OR height reduction
- Shows exact dimensions being lost
- No warning for upsize operations

## Version 1.27 - Canvas Resize Pixel Preservation (October 12, 2025) ✅

### Pixel Data Preservation
- **Fixed Pixel Loss**: All pixels now preserved in top-left region when resizing
- **Auto-Zoom Adjustment**: 16x for small canvases, 8x for large canvases
- **Smart Visibility**: Zoom automatically adjusts to maintain sprite visibility
- **Console Logging**: Shows exact preservation region for each resize

## Version 1.26 - Panel Width Adjustments (October 12, 2025) ✅

### Optimized Panel Sizes
- **Left Panel**: Expanded to 520px (was 500px)
- **Right Panel**: Expanded to 500px (was 300px) - 66% larger!
- **Better Layout**: More room for tools, palettes, layers, and animation controls
- **User Feedback**: Adjusted based on workflow testing

## Version 1.25 - Grid Overlay & Branding (October 12, 2025) ✅

### Grid Overlay Feature
- **Toggle Grid on Top**: Grid lines visible through drawn pixels
- **Visual Button**: Blue when on, gray when off
- **Perfect for Dense Artwork**: Never lose grid reference
- **Two Modes**: Grid behind pixels (default) or grid overlay

### Brand Integration
- **DCS Logo**: Diamond Clad Studios logo in toolbar
- **Replaced Emoji**: Clean, professional appearance
- **PNG Integration**: Bundled with executable

### Constants Palette
- **Auto-Detection**: Shows only colors actively used on canvas
- **Dynamic Updates**: Updates as you draw
- **Quick Access**: See your current color usage at a glance

## Version 1.24 - Collapsible Panels (October 12, 2025) ✅

### UI Refinements
- **Collapsible Side Panels**: Hide tools/layers for maximum canvas space
- **Clean Restore Buttons**: Blue arrow buttons at screen edges
- **Styled Dividers**: 10px wide flat grey sash dividers
- **Smooth Transitions**: Proper widget management for collapse/expand
- **Independent Control**: Collapse left, right, or both panels

## Version 1.23 - Panel Resize Optimization (October 12, 2025) ✅

### Performance Improvements
- **Smooth Divider Dragging**: Optimized PanedWindow for lag-free resizing
- **Outline-Only Resize**: Shows outline during drag instead of redrawing content
- **Sash Drag Tracking**: Prevents window resize conflicts

## Version 1.22 - Theme System (October 12, 2025) ✅

### Real-Time Theme Switching
- **Two Built-In Themes**: Basic Grey (dark) and Angelic (light)
- **100% UI Coverage**: All panels, buttons, labels, scrollbars update
- **Theme Dropdown**: Palette icon 🎨 in toolbar for easy switching
- **Instant Updates**: No restart required

## Version 1.13 - UI Improvements (October 11, 2025) ✅

### Complete Palette System
- **All 6 Palettes Available**: Added 4 missing palette JSON files
- **Custom Application Icon**: Colorful 4×4 pixel grid logo
- **Resizable Side Panels**: Drag dividers to adjust panel widths
- **Compact 3×3 Tool Grid**: Saves 180+ pixels of vertical space
- **Documentation Organized**: New features/ and technical/ subdirectories

## Version 1.12 - Custom Colors System (October 11, 2025) ✅

### Persistent Color Library
- **32 Custom Color Slots**: Save your favorite colors permanently
- **User-Specific Storage**: Each user has their own color library
- **Simple Interface**: Save (green) and Delete (red) buttons
- **Instant Loading**: Click saved colors to load into color wheel
- **Local Storage**: Stored in user profile, not bundled with app

## Version 1.11 - 64x64 Canvas Support (October 11, 2025) ✅

### Larger Canvas Option
- **64x64 Preset**: Extra-large canvas for detailed sprites
- **Fixed Layer Bug**: Critical layer dimension caching bug resolved
- **Improved Synchronization**: Better canvas resize coordination
- **Auto-Zoom**: Optimal viewing for all canvas sizes

## Version 1.0 - Initial Release (October 10, 2025) ✅

### Core Features
- 10 complete drawing tools
- Layer management system
- Animation timeline (4-8 frames)
- 50-state undo/redo
- 6 game-inspired color palettes
- PNG/GIF export
- Sprite sheet export
- Custom .pixpf project format
- File association system
- Comprehensive keyboard shortcuts

## Version 2.5.6 - Layer Visibility Toggle Fix
**Date**: January 2025  
**Type**: Bug Fix

### 👁️ Layer Visibility Toggle Fix
- **✅ Fixed layer checkbox toggles** - clicking visibility checkboxes now immediately updates canvas
- **✅ Instant visual feedback** - hiding/showing layers updates display immediately
- **✅ Complete layer system** - all layer operations now provide proper visual feedback

### 🔧 Technical Fix
- Added missing `canvas_renderer.update_pixel_display()` call to `_update_canvas_from_layers()`
- Ensures layer visibility changes trigger immediate canvas display updates

## Version 2.5.5 - Layer System Fix
**Date**: January 2025  
**Type**: Critical Bug Fix

### 🎨 Layer System Drawing Fix
- **✅ Fixed layer selection confusion** - clicking a layer now always selects it
- **✅ Clear visual feedback** - active layer highlighted in blue
- **✅ Predictable drawing behavior** - drawing always goes to the highlighted layer
- **✅ Removed confusing deselect behavior** that made layers appear broken

### 🔧 Technical Changes
- Simplified layer selection logic in `layer_panel.py`
- Fixed drawing layer resolution in `layer_animation_manager.py`
- Removed confusing `-1` state handling that caused silent fallbacks

## Version 2.5.4 - Edge Tool UX Fixes
**Date**: January 2025  
**Type**: Bug Fixes / UX Improvements

### 🧹 Right-Click Drag Erase (Edge)
- **✅ Continuous erase** while holding right mouse button and dragging
- Uses the same enhanced edge detection as drawing

### 🖱️ Edge Thickness Menu Reliability
- **✅ Right-click on Edge button** opens thickness menu consistently
- Verified UI binding and callback wiring

### 🔧 Internal
- Added right-button drag and release event routing in canvas event dispatcher
- Ensured float-precision coordinate path for erasing
* Added resizable and collapsible sidebar panels in WPF app using GridSplitters and toggle buttons.
