# Pixel Perfect - Changelog

## Version 1.36 - Selection & Move Tool Bug Fixes (October 14, 2025) ✅

### 🐛 Critical Bug Fixes

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
