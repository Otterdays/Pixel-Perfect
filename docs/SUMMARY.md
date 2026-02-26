# Pixel Perfect - Project Summary

## 🔄 C# WPF Rewrite In Progress
**Location**: [`Pix_Perf_C_WPF/`](../Pix_Perf_C_WPF/)  
**Status**: 🟡 Foundation Built (v0.2.2) — Parity In Progress  
**Last Updated**: February 26, 2026  
A clean-slate C# / WPF rebuild targeting parity with Python v2.9.0. **10 tools** (Brush, Eraser, Fill, Eyedropper, Line, Rectangle, Circle, Selection, Move, Pan), canvas size presets, grid overlay, color picker, Copy/Cut/Paste/Delete, layer system, undo/redo, zoom, pan, PNG export, fully skinned dark-mode templates, **14 themes**, MVVM. See `Pix_Perf_C_WPF/DOCS/PARITY.md` for full parity tracker.

---

## Python Version Status: PRODUCTION READY ✅
**Version**: 2.9.0  
**Last Updated**: February 19, 2026 - Canvas Expanded

## Latest Updates (v2.9.0)

### 📐 Bigger Canvas Sizes
- **✅ 128×128 (HUGE)** - Scene tiles, large sprites
- **✅ 256×256 (MASSIVE)** - Full scenes, sprite sheets
- **✅ Auto-Zoom** - Smart zoom adjustment for larger presets

### ⚡ Pillow Image Rendering
- **✅ Performance Overhaul** - Replaced per-pixel rectangles with Pillow compositing
- **✅ Full Coverage** - Main pixels, onion skins, and tile preview all upgraded
- **✅ Crisp Edges** - NEAREST resampling preserves pixel art sharpness

### 🖼️ Reference Image Panel
- **✅ Load Any Image** - PNG, JPG, BMP, GIF, WEBP via file dialog
- **✅ Adjustable Opacity** - 10% to 100% slider
- **✅ Pan & Zoom** - Drag, scroll, double-click to reset
- **✅ Shift+R Toggle** - Quick show/hide keyboard shortcut

### 🔍 Mini Preview Window
- **✅ Aseprite-Style Overlay** - Bottom-right preview showing full canvas
- **✅ Checkerboard Transparency** - Standard alpha background
- **✅ Viewport Indicator** - White rect shows visible area when zoomed in
- **✅ Shift+P Toggle** - Quick show/hide keyboard shortcut

### 🖱️ Right-Click Camera Pan
- **✅ Hold + Drag** - Right-click hold pans the camera (like middle mouse)
- **✅ Click + Release** - Opens context menu as before
- **✅ 5px Threshold** - Smart distinction between pan and click

## Planned Features (v3.x)

### 🤖 AI Features
- See `DOCS/features/AI_FEATURES.md` for full roadmap
- Phase 1: Auto-palette, color reduction, smart outline, shading suggestions (no external deps)
- Phase 2: Auto-shade, smart resize, readability check
- Phase 3: Auto-tiling, animation smoothness, text-to-sprite

### 🪙 3D Token Preview
- **✅ Software Voxel Renderer** - Zero dependencies (Pillow+numpy)
- **✅ Interactive Controls** - Rotate, Zoom, Thickness, Light, Material
- **✅ Export** - PNG render and GIF spin animation
- **✅ Panel** - Collapsible right sidebar (Shift+T)

### 🤖 Godot Engine Export
- **✅ Godot-Ready Sheets** - Zero-spacing sprite sheets
- **✅ .tres Resources** - Auto-generated SpriteFrames
- **✅ .tscn Scenes** - Ready-to-use AnimatedSprite2D nodes
- **✅ Import Guide** - Auto-generated instructions
- **See `DOCS/features/GODOT_EXPORT.md`** for full details

## Previous Updates (v2.7.7)

### 🖱️ Right-Click Context Menu
- **✅ Context-Aware Menu** - Right-click shows relevant actions based on tool/state
- **✅ Selection Operations** - Copy, Cut, Delete, Mirror, Rotate, Scale
- **✅ Paste Support** - Paste when copy buffer exists
- **✅ Tool Switching** - Quick access to common tools
- **✅ Canvas Controls** - Zoom, Grid, Tile Preview toggles

### ⌨️ Copy/Paste Keyboard Shortcuts
- **✅ Ctrl+C/V/X** - Copy, Paste, Cut selection
- **✅ Delete Key** - Delete selection
- **✅ Undo Support** - All operations save undo state

## Previous Updates (v2.7.6)

### 🎨 Theme Customization System
- **✅ Complete Color Control** - Customize all 20+ theme color properties with visual pickers
- **✅ Live Preview** - See changes in real-time as you adjust colors
- **✅ Save Custom Themes** - Save themes with custom names, auto-added to dropdown
- **✅ Export/Import** - Export themes to JSON files, import from other users
- **✅ Persistent Storage** - Custom themes saved to user storage directory

## Previous Updates (v2.7.5)

### 🖼️ Tile Preview Mode
- **✅ 3x3 Repeating Grid** - Canvas repeated around itself for pattern/tile visualization
- **✅ Ghost Tiles** - Surrounding tiles at 50% opacity with stipple transparency effect
- **✅ Performance Optimized** - Only draws visible tiles, uses NumPy for efficient rendering
- **✅ Toolbar Button** - "Tile" button toggles ON/OFF with green highlight

### ⛶ Fullscreen Mode
- **✅ F11 Toggle** - Press F11 to enter/exit true fullscreen mode
- **✅ Escape to Exit** - Press Escape to exit fullscreen
- **✅ Distraction-Free** - Full screen coverage for focused pixel art work

## Previous Updates (v2.7.3)

### 🎨 Claude Theme & UI Polish
- **✅ Claude Theme** - New bright, warm theme (cream backgrounds, coral accents) in theme dropdown
- **✅ Minimalistic Panel Buttons** - Collapse/expand use small ‹/› chevrons; restore buttons minimal, centered
- **✅ Canvas Recenter Fix** - Grid no longer stays off-center when opening panels; redraw runs on expand too

### 🖌️ Tool Previews & Eraser Edge Delete
- **✅ Dither Canvas Preview** - Checkerboard pattern preview at cursor (matches brush size)
- **✅ Spray Preview** - Circular outline at cursor (existing behavior)
- **✅ Eraser Right-Click** - Delete edge lines on canvas; right-click or right-drag to remove edges

## Previous Updates (v2.7.2)

### 🔍 Zoom to Cursor + Fit/100% View
- **✅ Zoom to Cursor** - Ctrl+wheel zooms while keeping cursor position in view
- **✅ Fit / 100% Buttons** - Fit canvas to viewport; 100% zoom reset

### 📦 Export Presets + Quick Export
- **✅ Export Settings Dialogs** - Configurable PNG/GIF/Sprite Sheet options
- **✅ Preset Persistence** - Settings saved between sessions; Quick Export (Ctrl+Shift+E)

### 🎨 Recent Colors Selection
- **✅ Reliable Selection** - Recent colors view correctly sets active brush color when clicked

## Previous Updates (v2.7.1)

### 🏁 Dither Tool
- **✅ Checkerboard Brush** - New tool for classic pixel art shading and texturing.
- **✅ Pattern Logic** - Automatically draws pixels in a `(x+y)%2` checkerboard pattern.
- **✅ Dual Function** - Left-click to draw pattern, Right-click to erase.

### 🔧 Undo System Refinements
- **✅ Transparent Pixel Restoration** - Fixed critical bug where undoing brush strokes didn't clear pixels back to transparency.
- **✅ Edge Tool Support** - Undo/Redo now correctly tracks and restores Edge Tool lines.
- **✅ Snapshot Logic** - Improved `UndoManager` to handle full state snapshots correctly.

## Previous Updates (v2.6.2)

### 🚀 Performance Optimizations
- **✅ Rendering Optimizations** - NumPy vectorization for `draw_all_pixels_on_tkinter()` and `flatten_layers()` (10-50× faster)
- **✅ Selection/Transform Optimizations** - Vectorized scaling, mirroring, and rotation operations
- **✅ Event Handling Optimizations** - Early-exit caching for mouse move events to skip redundant preview draws
- **✅ Code Cleanup** - Removed remaining debug prints from brush.py and selection_manager.py

## Previous Updates (v2.6.1)

### 🧹 Code Cleanup & Refactor
- **✅ Dead Code Removal** - Removed ~100 lines of unused fallback code from main_window.py
- **✅ Debug Print Cleanup** - Removed ~150+ debug print statements from 4 key files
- **✅ Documentation Compaction** - Reduced SCRATCHPAD.md from 6,058 to ~400 lines (per project rules)
- **✅ Unused Import Cleanup** - Removed unused imports (CanvasSize, UndoState, Optional)

## Previous Updates (v2.6.0)

### ✒️ Spray Paint Tool
- **✅ Natural Coverage** - Drag to spray continuous droplets with adjustable radius/density.
- **✅ Full Integration** - Shares Tool Size manager UI, cursor preview, and undo path with existing tools.
- **✅ Artist Shortcuts** - `Y` hotkey plus right-click context menu for quick parameter changes.

### 🧭 Canvas Zoom Scrollbar
- **✅ Visual Zooming** - Canvas renders a themed scrollbar with +/− buttons and draggable handle.
- **✅ Wheel Harmony** - Scroll wheel, dropdown, and scrollbar stay perfectly synchronized.
- **✅ 64× Support** - Zoom range now spans 0.25× through 64× for detail or overview work.

### 🎨 JSON Palette Loader
- **✅ Auto-Discovery** - On launch, all `assets/palettes/*.json` files populate the palette dropdown.
- **✅ Safe Naming** - Duplicate names receive suffixes, keeping the list unique.
- **✅ Grass Palette** - Bundled `grass.json` introduces 16 natural tones as a working example.

## Previous Updates (v2.5.11)

### 🎨 Primary Color Variations Highlighting Fix
- **✅ Fixed Visual Feedback** - Resolved Primary color variations not showing selection highlighting
- **✅ Root Cause Resolution** - Missing visual feedback system for variation button selection
- **✅ Clear Selection Indication** - Added white border highlighting for selected color variations
- **✅ User Experience** - Clear visual indication of which color variation is currently selected

## Previous Updates (v2.5.10)

### 🐛 Saved Colors Auto-Selection Fix
- **✅ Fixed Brush Color Issue** - Resolved saved colors not becoming active brush color after saving
- **✅ Root Cause Resolution** - Saving colors only stored them but didn't select them as current color
- **✅ Seamless Workflow** - Saved colors immediately become active brush color for painting
- **✅ User Experience** - No more fallback to Grid color after saving colors from Primary/Wheel views

## Previous Updates (v2.5.9)

### 🎨 Primary Colors Centering Fix
- **✅ Fixed Grid Centering** - Resolved Primary colors grid being left-aligned instead of centered
- **✅ Root Cause Resolution** - Missing `grid_columnconfigure` to center columns within container
- **✅ Visual Balance** - Primary colors and variations grids now properly centered for better appearance
- **✅ Style Guide Compliance** - Follows established design patterns for grid centering

## Previous Updates (v2.5.8)

### 🐛 Grid and Wheel Color Saving Fix
- **✅ Fixed Color Saving Issue** - Resolved Grid and Wheel colors not saving to Saved Colors palette
- **✅ Root Cause Resolution** - `get_source_color()` method was checking current view mode instead of using `last_active_view` when in saved mode
- **✅ Proper Color Tracking** - System now correctly tracks which view was active before switching to saved mode
- **✅ Complete Color Management** - Users can now save colors from any view (Grid, Primary, or Wheel) to Saved Colors

## Previous Updates (v2.5.7)

### 🐛 Primary Color Selection TypeError Fix
- **✅ Fixed Color Selection Crash** - Resolved TypeError when selecting colors in Primary palette view
- **✅ Root Cause Resolution** - `primary_view.py` was passing color tuples instead of integer indices to callback
- **✅ Consistent Behavior** - Now matches `grid_view.py` behavior for proper color selection
- **✅ User Experience** - Users can select color variations without application crashes

## Previous Updates (v2.5.6)

### 👁️ Layer Visibility Toggle Fix
- **✅ Fixed layer checkbox toggles** - clicking visibility checkboxes now immediately updates canvas
- **✅ Instant visual feedback** - hiding/showing layers updates display immediately
- **✅ Complete layer system** - all layer operations now provide proper visual feedback

## Previous Updates (v2.5.5)

### 🎨 Layer System Drawing Fix
- **✅ Fixed layer selection confusion** - clicking a layer now always selects it
- **✅ Clear visual feedback** - active layer highlighted in blue  
- **✅ Predictable drawing behavior** - drawing always goes to the highlighted layer
- **✅ Removed confusing deselect behavior** that made layers appear broken

## Previous Updates (v2.5.3)

### 🐛 Edge Tool Flickering Lines Fix
- **✅ Flickering Eliminated**: Fixed critical issue where edge lines flickered during continuous drawing
- **✅ Preview System Isolation**: Disabled hover preview during active drawing to prevent interference
- **✅ Clean Drawing Experience**: Edge lines now draw smoothly without visual artifacts
- **✅ Preserved Functionality**: All edge tool features remain intact (thickness, erase, etc.)

## Previous Updates (v2.5.2)

### 🎨 Edge Tool Variable Thickness Feature
- **✅ Variable Edge Thickness**: Edge tool now supports 5 thickness levels (0.1P, 0.25P, 0.5P, 1.0P, 2.0P)
- **✅ Right-Click Thickness Menu**: Right-click edge tool button to select thickness with visual indicators
- **✅ Thickness Display**: Edge button shows current thickness: `Edge [0.1P]`, `Edge [0.25P]`, etc.
- **✅ Zoom-Scaled Line Width**: Edge lines scale properly with zoom level for consistent appearance
- **✅ Fine Line Control**: Ultra-fine 0.1P thickness for detailed edge work and line art

## Previous Updates (v2.5.1)

### 🐛 Edge Tool Critical Fix
- **✅ Fixed Edge Detection Bug**: Edge tool now correctly detects all edges (top, bottom, left, right) instead of only drawing on top edges
- **✅ Float Precision Coordinates**: Added separate coordinate system for edge tool with fractional precision
- **✅ Improved Edge Targeting**: Users can now reliably click on any edge of a pixel
- **✅ New Project Edge Clearing**: Edge lines are now properly cleared when creating new projects

## Previous Updates (v2.5.0)

### 🔍 Zoom System Improvements
- **✅ Added 64x Zoom**: New maximum zoom level for extreme detail work on tiny canvases
- **✅ Updated Zoom Controls**: 64x added to dropdown menu and scrollable zoom bar
- **✅ Increased Zoom Limits**: Canvas zoom limits increased from 32x to 64x

### 🎨 Edge Tool Complete Implementation
- **✅ Edge Tool Fully Functional**: Draws thin lines on pixel boundaries with hover preview
- **✅ Edge Line Persistence**: Edge lines survive canvas redraws and tool switching
- **✅ Hover Preview System**: Real-time preview shows where edge line will be drawn
- **✅ Edge Detection Zones**: 0.1 pixel width zones detect top/bottom/left/right edges
- **✅ Canvas Integration**: Edge tool properly integrated with canvas renderer system

## Previous Updates (v2.4.0)

## Previous Updates (v2.3.0)

### 🐛 Critical Import Dialog Fixes
- **✅ Fixed GUI Scale Calculation**: Dialog now uses validated base dimensions for scale calculations instead of raw file dimensions
- **✅ Fixed Import Logic Priority**: Import process now prioritizes scaled export detection over direct size detection
- **✅ Fixed Scale Switching**: No more GUI state corruption when switching between scale options

## Previous Updates (v2.2.9)

### 🐛 Critical Algorithm Fix
- **✅ Fixed PNG Validation Priority**: Algorithm now prioritizes scaled export detection over direct size detection
- **✅ Fixed 8x8 Scaled Export Detection**: 8x8 images exported at 8x scale now correctly detected as 8x8 base size

## Previous Updates (v2.2.8)

### 🐛 Critical Import Dialog Fix
- **✅ Fixed Import PNG Dialog Dimensions**: Dialog now shows detected base dimensions instead of raw file dimensions
- **✅ Fixed Scaled Export Display**: 8x8 images exported at 8x scale now correctly show "Original: 8x8 pixels"

## Previous Updates (v2.2.7)

### 🐛 Critical Import Fix
- **✅ Fixed 8x8 PNG Import Validation**: 8x8 images now correctly import without dimension detection errors
- **✅ Fixed Import Dialog Display**: Import PNG dialog now shows correct dimensions for 8x8 images

## Previous Updates (v2.2.6)

### 🎨 UI Styling Fixes
- **✅ Fixed Double "Layers" Text**: Removed duplicate "Layers" title in the Layers panel
- **✅ Removed Visual Boxes**: Eliminated unwanted rectangular boxes around Layers and Animation panels for cleaner appearance

## Previous Updates (v2.2.5)

### 🎯 Quality of Life Improvements
- **✅ Added 8x8 Canvas Size**: New "Tiny" preset for micro icons and detailed pixel work
- **✅ Fixed File Dialog Layering**: All file dialogs now properly appear on top of the main application window

## Previous Updates (v2.2.4)

### 🐛 Selection Move Tool Pixel Duplication Fix - CRITICAL
**Fixed pixel duplication when moving selection multiple times**
- **New Bug**: After fixing the "pixels deleted underneath" bug, pixels were being duplicated on second move
- **Root Cause**: `finalize_move()` was being called automatically after every drop, causing double drawing
- **Solution**: Only call `finalize_move()` on the FIRST move using `pixels_cleared` flag
- **Files Modified**: `src/tools/selection.py` - Added conditional finalization logic
- **Result**: Multiple moves now work correctly without pixel duplication
- **Status**: ✅ **FIXED** - Selection moves work perfectly for unlimited repositioning

## Previous Updates (v2.2.3)

### 🐛 Selection Move Tool Bug Fix - CRITICAL
**Fixed pixels being deleted underneath when moving selection multiple times**
- **Critical Bug**: Picking up moved selection again would delete pixels underneath at new location
- **User Impact**: Users couldn't make adjustments to placement without destroying pixels
- **Root Cause**: `finalize_move()` was resetting `original_selection = None` after first move
- **Solution**: Preserve `original_selection` during moves, only reset when switching tools
- **New Method**: Added `reset_state()` to properly reset move tool state
- **Files Modified**: `src/tools/selection.py`, `src/ui/main_window.py`
- **Result**: Users can now pick up and reposition selections unlimited times without data loss
- **Documentation**: `docs/bugfixes/SELECTION_MOVE_TOOL_PIXEL_DELETION_FIX.md`
- **Status**: ✅ **FIXED** - Non-destructive selection adjustment now working correctly

## Previous Updates (v2.0.9)

### 🖱️ Scroll Wheel Zoom & Draggable Canvas Scrollbar
**Added mouse wheel zoom and visual scrollbar for intuitive canvas control**
- **Scroll Wheel Zoom**: Mouse wheel over canvas zooms in/out smoothly (Windows/Linux/Mac)
- **Draggable Scrollbar**: Custom widget on right edge with + button (top), handle (middle), - button (bottom)
- **Perfect Synchronization**: Scroll wheel, scrollbar, and dropdown stay perfectly in sync
- **Theme Aware**: Scrollbar colors adapt to Basic Grey and Angelic themes automatically
- **Visual Feedback**: Proportional handle position shows current zoom level
- **Smooth Interaction**: Drag handle for precise zoom control, click buttons for single-level jumps
- **Cross-Platform**: Works on Windows, Linux, and macOS with native event handling
- **Files Created**: `src/ui/canvas_scrollbar.py` (240 lines)
- **Files Modified**: `src/ui/main_window.py`, `src/ui/canvas_zoom_manager.py`, `src/ui/theme_dialog_manager.py`
- **Status**: ✅ **COMPLETE** - Full implementation tested and integrated

## Previous Updates (v2.0.8)

### 🎨 Background Texture Mode
**Added paper texture as 4th background mode option**
- **New Feature**: Extended background toggle to 4 modes (Auto → Dark → Light → **Paper** → Auto)
- **Organic Rendering**: Realistic paper texture background with organic grain patterns
- **Consistent Colors**: Uses same cream base (#f5f5dc) and grain (#e6e6d4) as grid paper mode
- **UI Integration**: 📄 icon with "Background Mode: Paper Texture" tooltip
- **Bug Fix**: Fixed background texture overriding grid colors (proper rendering order)
- **Files Modified**: `src/core/canvas.py`, `src/core/canvas_renderer.py`, `src/ui/background_control_manager.py`
- **Status**: ✅ **COMPLETE** - Background texture mode fully integrated and functional

## Previous Updates (v2.0.7)

### 🎨 Paper Texture Grid Mode
**Added organic paper texture as 4th grid mode option**
- **New Feature**: Extended grid toggle to 4 modes (Auto → Dark → Light → **Paper** → Auto)
- **Organic Rendering**: Realistic paper grain patterns with organic, non-straight lines
- **Configurable**: Paper base color (#f5f5dc), grain color (#e6e6d4), intensity (0.3)
- **UI Integration**: 📄 icon with "Grid Mode: Paper Texture" tooltip
- **Files Modified**: `src/core/canvas.py`, `src/core/canvas_renderer.py`, `src/ui/grid_control_manager.py`
- **Status**: ✅ **COMPLETE** - Paper texture mode fully integrated and functional

## Previous Updates (v2.0.6)

### 🔧 Pan Tool Jumping Fix
**Fixed pan tool jumping back to original position after dragging**
- **Problem**: Pan tool would temporarily move canvas during drag, then jump back on release
- **Root Cause**: Pan offset was never permanently applied - only temporarily during drag
- **Solution**: Modified mouse up handler to get final pan offset and apply it permanently
- **Files Modified**: `src/core/event_dispatcher.py`
- **Status**: ✅ **RESOLVED** - Pan tool now properly maintains position after dragging

### 🎯 Canvas Grid Centering Fix
**Fixed canvas grid staying in original screen position during window resize**
- **Problem**: Grid didn't recalculate center position when window was resized
- **Root Cause**: EventDispatcher never called WindowStateManager's resize handler
- **Solution**: Added proper resize handler call and enhanced delayed redraw mechanism
- **Files Modified**: `src/core/event_dispatcher.py`, `src/core/window_state_manager.py`, `src/core/canvas_renderer.py`
- **Status**: ✅ **RESOLVED** - Canvas grid now properly centers during window resize

### 🎨 Brush Cursor Alignment Fix
**Fixed brush cursor appearing outside actual grid area after panning**
- **Problem**: Brush cursor (white dotted square) appeared outside actual grid
- **Root Cause**: Cursor preview methods didn't properly account for pan offset
- **Solution**: Fixed pan offset calculation in all cursor preview methods
- **Files Modified**: `src/core/canvas_renderer.py`
- **Status**: ✅ **RESOLVED** - Brush cursor now properly follows panned grid

---

## Previous Updates (v2.0.5)

### 🔧 Color Wheel Hardcoded Palette Fix
**Fixed hardcoded palette calls breaking color wheel brush color update**
- **Problem**: After fixing grid leak, color wheel brush color update was broken again
- **Root Cause**: Two locations had hardcoded `palette.get_primary_color()` calls instead of using `get_current_color()`
- **Solution**: Changed hardcoded calls to use `get_current_color()` which properly respects color wheel mode
- **Files Modified**: `src/core/canvas_renderer.py`, `src/core/event_dispatcher.py`
- **Status**: ✅ **RESOLVED** - Color wheel brush color update works correctly without leaking to grid

---

## Previous Updates (v2.0.3)

### 🔒 Color Wheel Grid Leak Fix
**Fixed color wheel colors leaking into preset palette grid**
- **Problem**: Using color wheel colors caused them to appear in grid layout, polluting preset palettes
- **Root Cause**: Previous fix introduced leak by calling `palette.set_primary_color_by_rgba()` which auto-adds colors
- **Solution**: Reverted to original behavior - `get_current_color()` already handles wheel colors correctly
- **Files Modified**: `src/ui/color_view_manager.py`
- **Status**: ✅ **RESOLVED** - Color wheel colors no longer leak into grid layout

---

## Previous Updates (v2.0.2)

### 🎨 Color Wheel Brush Color Fix
**Fixed color wheel clicks not updating brush color**
- **Problem**: Clicking colors on color wheel didn't change brush color - brush used old palette color
- **Root Cause**: `ColorViewManager.on_color_wheel_changed()` wasn't calling `palette.set_primary_color_by_rgba()`
- **Solution**: Added palette update call to convert RGB to RGBA and set as primary color
- **Files Modified**: `src/ui/color_view_manager.py`
- **Status**: ✅ **RESOLVED** - Color wheel clicks now properly update brush color

---

## Previous Updates (v2.0.1)

### 🎯 Critical Color Wheel Fix
**Fixed recurring color wheel display issue**
- **Problem**: Selecting "Wheel" radio button showed empty canvas instead of color wheel interface
- **Root Cause**: Logic error in `_show_view()` method - condition `and self.color_wheel` always failed since `self.color_wheel` is intentionally `None` during initialization
- **Solution**: Removed faulty condition from both `main_window.py` and `color_view_manager.py`
- **Files Modified**: `src/ui/main_window.py`, `src/ui/color_view_manager.py`
- **Status**: ✅ **RESOLVED** - Color wheel now displays correctly when selected

---

## Previous Updates (v2.0.0)

### 🐛 Critical UI Bug Fix: Saved Colors Blank Space
**Fixed persistent blank space in saved colors view**
- **Root Cause**: `palette_content_frame` was visible when switching to saved view, creating empty box
- **Solution**: Hide `palette_content_frame` when not needed, show only for views that use it
- **Fixed Views**: Grid, Primary, Wheel, Constants views now pack `palette_content_frame` correctly
- **Architecture Fix**: Proper frame hierarchy with `pack_forget()` and `before` parameter
- **Files Modified**: `src/ui/main_window.py`, `src/ui/ui_builder.py`, `src/ui/palette_views/saved_view.py`
- **Key Lesson**: When debugging UI spacing, trace EXACT frame hierarchy - sometimes entire frames are visible when they shouldn't be

---

## Previous Updates (v1.72)

### 📚 Enhanced AI Knowledge Base
**Comprehensive Python knowledge documentation for AI agents**
- **Modern Python Features**: Added Python 3.9+ features, type hints, dataclasses, async/await
- **Testing Frameworks**: Comprehensive pytest guidance, TDD, mocking, integration testing
- **Performance Optimization**: Profiling, memory management, algorithmic optimization, caching
- **Dependency Management**: Virtual environments, poetry, pip, security considerations
- **Maintainability Standards**: Code organization, documentation, linting, CI/CD practices
- **Enhanced Documentation**: `docs/knowledge/AI_PYTHON_KNOWLEDGE.md` (3,500+ lines)
- **Updated Workflow**: `docs/knowledge/AI_AGENT_README.md` with modern development practices

---

## Previous Updates (v1.71)

### ✨ Notes Panel Feature
**Persistent note-taking integrated into the editor**
- **Notes Button**: Added to top toolbar
- **Auto-Save**: Notes automatically saved as you type
- **Export to TXT**: Export functionality with custom filename
- **Persistent Storage**: Notes saved to ~/.pixelperfect/notes.json
- **Toggle Panel**: Appears on right side of canvas area
- **New Component**: `src/ui/notes_panel.py` (200+ lines)

---

## Previous Updates (v1.70)

### 🔧 Critical Move Tool Fixes
**Major bug fixes and visual improvements**
- **Move Tool Layer Sync**: Fixed move tool to update layer data instead of canvas
- **Visual Feedback**: Added live preview during move operations - pixels now follow cursor
- **Bug Resolution**: Original pixels no longer reappear when switching tools after move
- **Event Dispatcher**: Updated to pass layer objects to move/selection tools
- **Canvas Renderer**: Skip rendering original selection area during move for clean visual
- **Files Modified**: `src/tools/selection.py`, `src/core/event_dispatcher.py`, `src/core/canvas_renderer.py`

### 🎨 User Experience Improvements
- **Professional Move Tool**: Pixels visually move with cursor during drag
- **No Duplicate Pixels**: Clean visual feedback without showing original + preview
- **Seamless Tool Switching**: Move → Brush transitions work perfectly
- **Layer Consistency**: All move operations properly sync with layer system

---

## Previous Updates (v1.69)

### 🎯 Grid Control Manager
**Small refactor complete - Grid controls extracted**
- **New Module**: `src/ui/grid_control_manager.py` (68 lines)
- **4 Methods Extracted**: Grid visibility toggle, overlay toggle, button updates
- **Line Reduction**: main_window.py reduced from 1,614 → 1,582 lines (-32 lines, -2.0%)
- **Cumulative**: Down from 3,387 → 1,582 lines (1,805 lines, 53.3% total reduction)
- **Canvas Renderer Updated**: References grid_control_mgr.grid_overlay
- **Benefits**: Clean separation of grid logic, easier to extend with new grid features

---

## Previous Updates (v1.68)

### 🎨 Tool Size & Canvas/Zoom Managers
**Phases 6 & 7 complete - Tool sizing and canvas management extracted**
- **New Module**: `src/ui/tool_size_manager.py` (163 lines)
- **New Module**: `src/ui/canvas_zoom_manager.py` (226 lines)
- **11 Methods Extracted**: Brush/eraser sizing (8) + canvas resize/zoom (3)
- **Line Reduction**: main_window.py reduced from 1,888 → 1,614 lines (-274 lines, -14.5%)
- **Cumulative**: Down from 3,387 → 1,614 lines (1,773 lines, 52.4% total reduction)
- **EventDispatcher Updated**: Brush/eraser operations use tool_size_mgr
- **Canvas Renderer Updated**: Preview methods reference tool_size_mgr for sizes
- **Benefits**: Isolated tool sizing logic, centralized canvas management, easier to test

---

## Previous Updates (v1.67)

### 🔨 Build System Compatibility (v1.67)
**Build system updated for refactored modular architecture**
- **13 New Hidden Imports**: Added all newly extracted modules to PyInstaller build
- **Import Fix**: Corrected `ui_builder.py` import path
- **Modules Verified**: All refactored components import successfully
- **Build Ready**: Can now compile standalone executable with all recent refactors

### 🐛 Critical Bug Fixes (v1.66)
**Selection & UI issues resolved**
- **Copy-Behind Bug Fixed**: Move + mirror/rotate operations no longer leave duplicate pixels at original location
- **Selection Handles Restored**: Drag handles now visible on all selections (not just scaling mode)
- **Cursor Updates Fixed**: Canvas cursor properly changes when auto-switching from selection to move tool
- **AttributeError Fixes**: All scaling/copy attributes correctly reference SelectionManager
- **Tool Selection Fixed**: Tools now respond to clicks and show proper visual feedback
- **Fill Tool Fixed**: Fill operations now persist when switching to brush tool (layer-based approach)
- **New Project Reset**: New project now properly clears selection box and resets tool to brush
- **Eraser Tool Fixed**: Eraser now properly erases individual pixels instead of clearing entire canvas
- **Copy-Behind Bug Fixed**: Move + mirror/rotate operations no longer leave duplicate pixels (proper finalize_move implementation)
- **Undo/Redo System Fixed**: Undo/redo buttons now work properly with visual feedback and state management
- **Rotate Operation Fixed**: Non-destructive rotation preview prevents duplicate pixels in original location
- **Move Tool Fixed**: Auto-finalization prevents duplicate pixels when moving selections

### 🎨 Selection Manager Extraction (v1.65)

### 🎨 Selection Manager Extraction
**Phase 1 complete - All selection operations extracted to dedicated manager**
- **New Module**: `src/ui/selection_manager.py` (438 lines)
- **10 Methods Extracted**: Mirror, rotate, copy, scale operations + helpers
- **8 State Variables Moved**: Scaling and copy/paste state
- **Line Reduction**: main_window.py reduced from 2,724 → 2,374 lines (-350 lines, -12.9%)
- **Cumulative**: Down from 3,387 → 2,374 lines (1,013 lines, 29.9% total reduction)
- **EventDispatcher Updated**: All scaling/copy references point to selection_mgr
- **Benefits**: Clean transformation logic, numpy operations centralized, easier testing

---

## Previous Updates (v1.64)

### 💬 Dialog Manager Extraction
**Phase 4 complete - Custom dialogs extracted to dedicated manager**
- **New Module**: `src/ui/dialog_manager.py` (417 lines)
- **5 Methods Extracted**: Custom size, downsize warning, texture panel + helpers
- **Line Reduction**: main_window.py reduced from 3,047 → 2,724 lines (-323 lines, -10.6%)
- **Cumulative**: Down from 3,387 → 2,724 lines (663 lines, 19.6% total reduction)
- **Low Risk**: Self-contained dialogs with no tool/canvas coupling
- **Easy Testing**: Each dialog independently testable
- **Benefits**: Cleaner separation, reduced complexity, modular dialog system

---

## Previous Updates (v1.62)

### 📁 File Operations Manager Extraction
**Phase 3 complete - File I/O operations extracted**
- **New Module**: `src/ui/file_operations_manager.py` (395 lines)
- **10 Methods Extracted**: New, Open, Save, Import PNG, Export PNG/GIF/Spritesheet, Templates
- **Line Reduction**: main_window.py reduced from 3,387 → 3,029 lines (-358 lines, -10.6%)
- **Clear Separation**: All file I/O operations now in dedicated manager class
- **Callback Integration**: Seamless integration with canvas and layer systems

---

## Previous Updates (v1.57)

### 📚 AI Python Knowledge Document
**Comprehensive Python reference guide for AI agents working in Cursor**
- **470+ lines** of Python knowledge documentation
- **10 major sections** covering fundamentals to advanced patterns
- **Extensive code examples** showing correct vs incorrect patterns
- **AI agent-specific advice** for Cursor workflow and tool usage
- **Project patterns** from Pixel Perfect refactoring experience
- **Debugging techniques** and best practices
- **Architectural patterns** (MVC, Observer, Strategy, Singleton, Factory)
- **Refactoring strategies** for safe code transformation

**File**: `docs/AI_PYTHON_KNOWLEDGE.md`

**Purpose**: Help future AI agents:
- Understand Python best practices and common pitfalls
- Read and understand codebases effectively
- Apply architectural patterns consistently
- Use Cursor tools effectively (grep, search_replace, codebase_search)
- Debug and refactor code safely
- Follow project-specific conventions

**Meta-Insight**: An AI agent creating documentation FOR future AI agents - a powerful feedback loop capturing lessons learned and best practices for AI-assisted Python development.

---

## Previous Updates (v1.54)

### 🎯 Color Wheel Clickable Area Fix
**Fixed color wheel to only respond to clicks on the rainbow ring**
- **Precise Interaction** - Only the rainbow ring responds to clicks, center and outer areas are non-interactive
- **Simplified Architecture** - Removed complex overlay approach with multiple canvases
- **Smart Click Detection** - Validates click position before starting drag operation
- **Cursor Feedback** - Changes to "crosshair" during drag, "arrow" when released
- **Configurable Thickness** - Added `self.wheel_thickness = 30` as instance variable
- **Clean Code** - Simpler, more maintainable implementation

**Technical Implementation:**
- Single canvas design directly on parent frame
- Click validation: `if radius - self.wheel_thickness <= distance <= radius`
- Cursor state changes provide visual feedback
- No grey background artifacts during theme changes

---

## Previous Updates (v1.52)

### 🖥️ Responsive Panel Sizing Fix
**Fixed resolution-dependent panel layout issues**
- **Screen Resolution Detection** - Automatically detects screen size and calculates optimal panel widths
- **Responsive Panel Sizing** - Panels now adapt to different screen resolutions instead of using fixed pixel widths
- **Window State Persistence** - Saves and restores your preferred panel sizes between sessions
- **Better Proportions** - Panels use appropriate percentage of screen space (35-40% depending on resolution)
- **More Canvas Space** - Larger screens get more canvas area, smaller screens get compact panels
- **User Preference** - Manually resized panels are remembered for future sessions

**Resolution-Based Panel Sizes:**
- **Small screens (≤1366px)**: Compact panels (280px + 260px)
- **Standard desktop (≤1920px)**: Balanced panels (350px + 320px)  
- **Large desktop (≤2560px)**: Spacious panels (400px + 380px)
- **Ultra-wide/4K (>2560px)**: Wide panels (450px + 420px)

---

## Previous Updates (v1.49)
**New patriotic theme with red, white, and blue colors**
- **Patriotic Design** - Red, white, and blue color scheme inspired by American flag
- **Professional Appearance** - Clean, readable interface with high contrast
- **Light Theme** - Bright, clean appearance like Angelic theme
- **Theme Variety** - Third theme option alongside Basic Grey and Angelic
- **Color Harmony** - Balanced patriotic colors with professional usability

---

## Previous Updates (v1.47)

### 🎨 Theme-Compatible Panel Loading Indicator
**Fixed Angelic theme compatibility for panel loading system**
- **Theme-aware colors** - Loading indicators now use theme colors instead of hardcoded values
- **Angelic theme fix** - No more grey boxes, shows proper light theme colors
- **Dynamic theming** - Panel containers and buttons update when theme changes
- **Consistent appearance** - Loading indicators match current theme across all themes
- **Professional design** - Cohesive visual experience in both Basic Grey and Angelic themes

---

## Previous Updates (v1.46)

### 🎯 Panel Loading Indicator
**Professional loading feedback for panel rendering**
- **Panel-internal loading** - Loading indicator appears INSIDE the panels themselves
- **Visual feedback** - "Loading Left Panel..." / "Loading Right Panel..." text centered in target panel
- **UX enhancement** - Masks panel rendering delay on mid-level systems
- **Canvas unobstructed** - Canvas stays completely visible during panel loading
- **Professional feel** - Intentional loading vs frozen UI appearance
- **Technical implementation** - Uses ctk.CTkLabel positioned inside target panels
- **100ms timing** - Optimal delay before removing loading indicator

---

## Previous Updates (v1.44)

### 🚀 Panel Toggle Performance Optimization
**Eliminated panel toggle lag with true visibility control**
- **Problem solved** - Panels now toggle truly instantly (no widget recreation)
- **200x speed improvement** - From ~1000ms to <5ms panel toggle
- **True visibility** - Panels stay in memory, just hidden/shown
- **Production ready** - Optimized for end users in executable
- **Memory efficient** - Zero widget recreation overhead
- **State preservation** - Panel state maintained between toggles

---

## Previous Updates (v1.42)

### ⚙️ Settings Button & Dialog Placeholder
**First step toward comprehensive settings system**
- **⚙️ Gear icon button** - Added to top toolbar (between Grid and Theme)
- **Professional placeholder** - "Coming Soon" dialog with feature preview
- **127 planned settings** - References MAX_SETTINGS.md documentation
- **6 feature categories** - Canvas, Tools, Colors, UI, Shortcuts, and more
- **Modal dialog** - Large 64pt gear icon with blue accent styling
- **Easy access** - Click gear to see what's planned
- **Tooltip** - "Settings (Coming Soon)" on hover
- **Consistent styling** - Matches app's CustomTkinter dark theme

---

## Previous Updates (v1.41)

### 🧹 Multi-Size Eraser Tool (1x1, 2x2, 3x3)
**Eraser tool now matches brush with multiple sizes**
- **3 eraser sizes**: 1×1 (single pixel), 2×2 (small), 3×3 (medium)
- **Right-click menu** - Click eraser button with right mouse to select size
- **Visual size indicator** - Button shows `Eraser [2x2]` like brush
- **Checkmark display** - Selected size marked with ✓ in menu
- **Dark theme menu** - Matches brush styling (#2d2d2d with blue highlight)
- **Auto-select tool** - Selecting size switches to eraser automatically
- **Centered erasing** - NxN squares centered on cursor position
- **Fast cleanup** - Erase large areas quickly with 2×2/3×3 sizes
- Full undo/redo support

---

## Previous Updates (v1.40)

### ⚠️ Styled Canvas Downsize Warning Dialog
**Beautiful custom warning for canvas resize operations**
- ⚠️ **Large warning emoji** with orange title for visibility
- **Clear size comparison** (Current vs. New dimensions)
- **Danger messaging** - Strong language about permanent pixel loss
- **Professional buttons** - Grey "No" (safe), Red "Yes" (destructive)
- **Consistent design** - Matches "Clear All Slots" dialog style
- **500×280px modal** - Centered, properly sized, accessible
- Replaced both system messagebox dialogs with custom CTkToplevel

---

## Previous Updates (v1.39)

### 📋 MAX SETTINGS Documentation
**Comprehensive settings catalog for future development**
- **127 total settings** across 14 categories
- **Impact ratings** (1-5 stars) for each setting
- **Complexity assessments** (Easy/Medium/Hard/Very Hard)
- **Implementation checklists** with status tracking
- **Priority matrix** for smart development planning
- **Complete vision** for settings system
- See `docs/MAX_SETTINGS.md` for full details

---

## Previous Updates (v1.38)

### 🌿 Texture Tool with Live Preview
**Complete texture application system with grass 8x8 pattern**
- **Grass texture**: 4 shades of green in hardcoded 8x8 pattern
- **Texture library panel**: Beautiful modal dialog with 64px previews
- **Live preview**: Real-time semi-transparent preview as you hover
- **Button highlighting**: Texture button turns blue when active
- **Click or drag**: Apply textures instantly to canvas
- **Expandable**: Easy architecture to add more textures

### 🎨 Smart Non-Destructive Move System (v1.37)
**Revolutionary two-phase move with background preservation**
- **First pickup**: Clears original pixels (move, not copy - no duplicates!)
- **Adjustments**: Unlimited repositioning with automatic background restoration
- **Background preservation**: Move pixels over others without destroying underlying content
- **Professional workflow**: Adjust position infinitely, red pixels safe when moving black over them
- **Technical**: Saves background on every drop, restores on pickup for truly non-destructive editing

### 🐛 Additional Bug Fixes (v1.36-1.37)
- **Fixed: Selection box visibility** - Multi-event binding + multiple redraw attempts (50ms, 150ms)
- **Fixed: Pixel cloning** - Original pixels now clear on first pickup (was copying instead of moving)
- **Fixed: Background destruction** - Underlying pixels preserved during all repositioning operations
- **Fixed: Empty space deletion** - Selection gaps no longer erase pixels underneath
- **Fixed: Move preview** - Pixels visible during drag operation

---

## Previous Updates (v1.35)

### 🖌️ Multi-Size Brush System
**Elegant brush size selection with right-click menu**
- 3 brush sizes: 1x1 (single pixel), 2x2 (small), 3x3 (medium)
- Right-click brush button for size selection popup
- Visual indicator on button: `Brush [2x2]`
- Checkmark shows selected size in dark theme menu
- Auto-select brush when changing size
- Centered NxN square drawing with bounds checking
- Perfect for both detail work and broad strokes
- Full undo/redo support

**Workflow Benefits**:
- Paint large areas faster with 2x2/3x3
- Switch to 1x1 for fine details
- Intuitive right-click interface
- Visual feedback at all times

---

## Previous Updates (v1.34)

### Eyedropper Perfection 🔍
- Always updates color wheel (even for palette colors)
- Auto-switches to Brush after sampling
- Ignores transparent pixels (no more broken wheel!)
- Seamless workflow improvements

### Custom Styled Dialogs 🎨
- Beautiful confirmation dialog for "Clear All Slots"
- Large emoji icon, bold typography, prominent buttons
- Red for danger, grey for safe actions
- Professional CustomTkinter styling

## Previous Updates (v1.33)

### Saved Colors System 🎨
- 24-slot personal color palette
- Local persistence (saved to AppData, not git)
- Export/Import for sharing
- Click empty slots to save, filled slots to load

### Performance Revolution ⚡
- **50-100× faster view switching**
- Grid/Wheel/Primary/Saved switches: <10ms (was 500-1000ms)
- Pre-rendered views with visibility toggling
- Instant, buttery smooth experience

### UX Enhancements
- Editable RGB values (type exact numbers)
- Auto-switch to Grid when changing palettes
- Color wheel backgrounds match theme

## Previous Updates (v1.32)

### Color Wheel Background Polish
- Fixed black/grey backgrounds
- Backgrounds now match theme seamlessly
- Perfect visual integration

## Previous Updates (v1.31)

### Color Wheel Performance & UX
- **~100× faster** - Eliminated excessive redrawing
- Crosshair cursor for better feedback
- Fixed saturation square design (no more redundant brightness control)
- Smooth, lag-free dragging

## Previous Updates (v1.30)

### Massive Build Optimization
- **91% smaller** - 330MB → 29MB!
- Removed pygame (~60MB) and scipy (~120MB)
- All features work identically
- 5-second downloads vs 53 seconds

---

## Complete Feature Set

### 🎨 Core Tools (13 Complete)
1. **Multi-Size Brush** (1x1, 2x2, 3x3) - Right-click for size menu
2. **Multi-Size Eraser** (1x1, 2x2, 3x3) - Right-click for size menu
3. **Spray Paint** ✒️ - Adjustable radius/density with live preview
4. **Fill Bucket** - Flood fill with tolerance
5. **Eyedropper** - Color sampling (L/R click for primary/secondary)
6. **Selection Tool** - Rectangle selection
7. **Move Tool** - Non-destructive move with background preservation
8. **Line Tool** - Bresenham's algorithm with live preview
9. **Rectangle Tool** - Hollow/filled with live preview
10. **Circle Tool** - Midpoint algorithm with live preview
11. **Texture Tool** 🌿 - Pattern stamping with texture library
12. **Edge Tool** - Sub-pixel edge outlining with variable thickness
13. **Pan Tool** - Canvas navigation

### 🖼️ Canvas System
- Preset sizes: 16×16, 32×32, 16×32, 32×64, 64×64
- Custom sizes: 1×1 to 512×512 with sleek dialog
- Downsize warning system (prevents accidental pixel loss)
- Pixel preservation on resize
- Auto-zoom adjustment (16x small, 8x large)
- Grid overlay toggle

### 🎨 Color Management
- **7 Game-Inspired Palettes**:
  - SNES Classic (16 colors)
  - Old School RuneScape
  - Curse of Aros
  - Heartwood Online
  - Definya
  - Kakele Online
  - Rucoy Online

- **5 View Modes** (instant switching, <10ms):
  - Grid View (4-column, auto-switches on palette change)
  - Primary Colors (8 mains + 24 variations)
  - Color Wheel (HSV picker with editable RGB values)
  - Constants (shows only used colors, auto-updates)
  - Saved Colors (24-slot personal palette with export/import)

- **32 Custom Colors** (user-specific, persists across sessions)
- **Primary/Secondary** color selection
- **Tooltips** on every control

### 🖼️ Layer System
- Unlimited layers
- Add/delete/reorder
- Toggle visibility
- Adjust opacity
- Alpha blending
- Active layer indication

### 🎬 Animation System
- 4-8 frame timeline (SNES style)
- Playback controls (play/pause/stop)
- Adjustable FPS
- Frame management (add/duplicate/delete/reorder)
- Previous/next navigation
- Frame thumbnails

### ↩️ Undo/Redo
- 50+ state history
- Smart state saving (beginning of operations)
- Visual feedback (blue/grey arrow buttons)
- Keyboard shortcuts (Ctrl+Z, Ctrl+Y, Ctrl+Shift+Z)
- Full layer integration

### 💾 Export & Projects
- **PNG Export** (1×-8× scaling, transparency)
- **PNG Import** (auto-scales to canvas)
- **GIF Export** (animated sprites)
- **Sprite Sheets** (horizontal/vertical/grid + JSON metadata)
- **Custom .pixpf Format** (full project data)
- **File Association** (double-click .pixpf to open)
- **Auto-save functionality**
- **Recent files tracking**

### 🎯 Preset Templates (8)
- 32×32 Character (top-down)
- 16×32 Character (side-view)
- 16×16 Item icon
- 32×32 Item icon (detailed)
- 16×16 Grass tile
- 16×16 Stone tile
- 32×16 Button (UI)
- 16×16 Icon (UI)

### 🎨 UI & UX
- **Lightning Fast** - 50-100× faster view switching with pre-rendered views
- **Theme System** - Basic Grey (dark), Angelic (light) with real-time switching
- **Collapsible Panels** - Hide/show left/right panels
- **Resizable Panels** - Left: 520px, Right: 500px
- **Tooltips** - Hover hints on every control
- **Grid Overlay** - Toggle grid on top of pixels
- **Custom Dialogs** - Styled confirmation dialogs
- **Brand Integration** - Diamond Clad Studios logo
- **Professional Styling** - Blue theme, rounded buttons

### ⌨️ Complete Keyboard Shortcuts
**Drawing Tools**: B (brush), E (eraser), F (fill), I (eyedropper), S (selection), M (move), P (pan), L (line), R (rectangle), C (circle)  
**Canvas**: Ctrl+Scroll (zoom), Space+Drag (pan), G (grid), Ctrl+G (overlay), [ / ] (brush size)  
**Files**: Ctrl+N/O/S/Shift+S/E/I (new/open/save/save as/export/import)  
**Edit**: Ctrl+Z/Y/Shift+Z (undo/redo)  
**Layers**: Ctrl+L/Shift+L (new/delete), Ctrl+Up/Down (move), PgUp/PgDn (select)  
**Animation**: Alt+Left/Right (frames), Space (play/pause)

---

## Technical Stack

- **Python 3.13+** - Core application
- **CustomTkinter 5.2.0** - Modern UI framework
- **Pillow (PIL)** - Image processing
- **NumPy** - Efficient pixel data arrays
- **PyInstaller** - Standalone executable (29MB)

---

## Project Structure

```
Pixel Perfect/
├── main.py                 # Entry point
├── launch.bat              # Windows launcher
├── requirements.txt        # Dependencies
├── dcs.png                 # Brand logo
├── src/
│   ├── core/               # Core systems
│   │   ├── canvas.py       # Pixel data management
│   │   ├── color_palette.py # Palette system
│   │   ├── custom_colors.py # User color library
│   │   ├── layer_manager.py # Layer system
│   │   ├── project.py      # Project file handling
│   │   ├── undo_manager.py # Undo/redo system
│   │   └── saved_colors.py # Saved colors (24 slots)
│   ├── tools/              # Drawing tools
│   │   ├── base_tool.py    # Tool base class
│   │   ├── brush.py        # Multi-size brush tool
│   │   ├── eraser.py       # Eraser tool
│   │   ├── eyedropper.py   # Eyedropper tool
│   │   ├── fill.py         # Fill bucket tool
│   │   ├── pan.py          # Pan tool
│   │   ├── selection.py    # Selection tool
│   │   └── shapes.py       # Line/rectangle/circle tools
│   ├── ui/                 # User interface
│   │   ├── main_window.py  # Main application window
│   │   ├── color_wheel.py  # HSV color picker
│   │   ├── layer_panel.py  # Layer management UI
│   │   ├── theme_manager.py # Theme system
│   │   ├── timeline_panel.py # Animation timeline
│   │   └── tooltip.py      # Tooltip system
│   ├── animation/          # Animation system
│   │   └── timeline.py     # Frame management
│   └── utils/              # Utilities
│       ├── export.py       # PNG/GIF/sprite sheet export
│       ├── import_png.py   # PNG import
│       ├── presets.py      # Template presets
│       └── file_association.py # .pixpf registration
├── assets/
│   ├── palettes/           # 8 JSON color palettes
│   └── icons/              # App icons
├── docs/                   # Documentation
│   ├── SUMMARY.md          # This file
│   ├── CHANGELOG.md        # Version history
│   ├── SCRATCHPAD.md       # Development notes
│   ├── ARCHITECTURE.md     # System design
│   ├── REQUIREMENTS.md     # Specifications
│   ├── SBOM.md             # Dependencies
│   └── features/           # Feature docs
└── BUILDER/                # Build system
    ├── build.bat           # PyInstaller script
    └── release/            # 29MB executable
