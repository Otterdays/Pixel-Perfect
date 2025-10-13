# Pixel Perfect - Changelog

## Version 1.27 - Canvas Resize Pixel Preservation (October 13, 2025) ✅

### Bug Fixes
- **Fixed Canvas Resize Pixel Loss**: Pixels now properly preserved when changing canvas size
  - All layers and timeline frames preserve pixel data in top-left region
  - Auto-adjusts zoom when resizing: 16x for small canvases, 8x for large canvases
  - Prevents "tiny sprite" issue when upsizing canvas
  - Zoom restoration when going back to smaller canvas sizes
  - Console logging shows exact preservation region (e.g., "Top-left 16x32 region preserved")
  - No more accidental pixel loss from size changes!

### Technical Implementation
- Enhanced `_on_size_change()` method with proper pixel preservation flow
- Added automatic zoom adjustment for all canvas sizes (16x16, 32x32, 16x32, 32x64, 64x64)
- Zoom increases to 16x minimum for small canvases to maintain visibility
- Zoom decreases to 8x maximum for large canvases to prevent clipping
- Detailed console logging for resize operations

## Version 1.26 - Panel Width Adjustments (October 13, 2025) ✅

### UI Enhancements
- **Optimized Panel Widths**: Adjusted side panel dimensions for better workspace
  - Left panel: Expanded from 500px to 520px (more room for tools and palette)
  - Right panel: Expanded from 300px to 500px (66% larger for layers/animation)
  - User requested wider panels for improved visibility and workflow
  - All collapse/restore operations updated to use new widths

### Technical Implementation
- Updated 4 instances of left panel width (initial setup, scrollable frame, 2x restore operations)
- Updated 3 instances of right panel width (initial setup, scrollable frame, restore operation)
- Panel widths maintained consistently across all UI states

## Version 1.25 - Grid Overlay, Branding & Constants Palette (October 13, 2025) ✅

### New Features
- **Grid Overlay Button**: Toggle grid lines on top of pixels
  - New "Grid Overlay" button in toolbar (90px width)
  - Shows "Overlay: ON" (blue) when enabled, "Overlay: OFF" (gray) when disabled
  - Grid lines appear through drawn pixels for precise editing
  - Useful for seeing grid alignment in heavily drawn areas
  - Uses canvas tag layering (`tag_raise("grid")`) for efficient rendering

- **Diamond Clad Studios Branding**: Professional brand integration
  - Replaced palette emoji with DCS logo in toolbar
  - 24x24px logo with high-quality LANCZOS resampling
  - Tooltip: "Color Theme - Diamond Clad Studios"
  - Logo stored in `assets/icons/dcs.png` for bundling
  - Error handling with fallback to emoji

- **Constants Palette View**: Dynamic color palette from canvas
  - New "Constants" radio button in palette panel (4th view mode)
  - Shows only colors actively used on the canvas
  - Scans all layers and extracts unique colors automatically
  - 4-column grid layout with clickable color buttons
  - Shows color count: "X colors in use"
  - Empty state: "No colors used yet. Draw on canvas to see colors here."
  - Smart selection: uses palette if color exists, switches to wheel if not
  - Perfect for seeing your actual color usage at a glance

### Technical Implementation
- Added `self.grid_overlay` state flag to main window
- Toggle button calls `_toggle_grid_overlay()` method
- Automatically updates display with `_force_tkinter_canvas_update()`
- Grid raised above pixels when both overlay mode and grid visibility are enabled
- Applied in both main display update and theme update methods
- PIL Image import for logo loading with dynamic path resolution

### Legal
- Added proprietary LICENSE - All Rights Reserved
- Copyright © 2024-2025 Diamond Clad Studios

## Version 1.24 - Collapsible Panels (October 13, 2025) ✅

### Features
- **Collapsible Side Panels**: Hide panels for maximum canvas space
  - Blue rounded arrow buttons (◀ ▶) on each panel edge
  - Click to collapse panel into thin 20px restore button
  - Click restore button to expand panel back to original position
  - Smooth transitions with proper widget management
  - Independent collapse for left and right panels

### UI Enhancements
- **Styled Sash Dividers**: Improved draggable panel dividers
  - 10px wide (was 8px) - easier to grab
  - Flat grey (#505050) - visible but clean
  - No borders - professional look
- **Blue Collapse Buttons**: Match UI theme
  - Rounded corners (8px radius)
  - Bold arrows for clarity
  - Hover effect (#1f538d → #144870)

### Bug Fixes
- **Restore Button Grey Boxes**: Fixed ugly grey squares around restore buttons
  - Root cause: CustomTkinter buttons have container backgrounds
  - Solution: Switched to regular tkinter `tk.Button` with flat relief
  - Clean overlay on canvas without background artifacts
  - Symmetrical positioning (5px from edges)
- **Sash Bar Disappearing**: Fixed dividers disappearing when panels collapsed
  - Removed `sashwidth=0` changes - sash stays visible at 10px
- **Grid Shifting on Panel Collapse**: Fixed grid moving when collapsing panels
  - Canvas resizes when panels collapse but grid wasn't re-centering
  - Added automatic canvas redraw (50ms delay) after all collapse/expand operations
  - Grid now properly re-centers in canvas after panel changes

## Version 1.23 - Panel Resize Optimization (October 13, 2025) ✅

### Performance
- **Smooth Panel Resizing**: Optimized PanedWindow divider dragging
  - Set `opaqueresize=False` to show outline during drag (no content redraw)
  - Added sash drag tracking with `_on_sash_drag_start`/`_on_sash_drag_end`
  - Prevents window resize events from interfering during panel resize
  - Fixed resize timer null reference errors
  - Result: Fast, responsive divider movement without lag

### Technical Notes
- Investigated CustomTkinter scrollbar positioning
- CTkScrollableFrame uses hardcoded grid layout (no left-side option)
- Decision: Keep scrollbar on right to preserve theme system integrity

## Version 1.22 - Theme System (October 13, 2025) ✅

### New Features
- **Theme System**: Centralized color scheme management
  - Separate `ThemeManager` module for clean architecture
  - Theme dropdown in toolbar with palette icon 🎨
  - Two built-in themes:
    - **Basic Grey**: Original dark theme
    - **Angelic**: Light, airy theme with soft blues and whites
  - Real-time theme switching
  - Applies to all UI elements (frames, buttons, canvas background)

### UI Updates
- Added theme selector in toolbar (right side, near Grid toggle)
- Palette emoji icon with tooltip
- Theme dropdown with 120px width
- Smooth theme transitions

### Technical
- Created `src/ui/theme_manager.py` with:
  - `Theme` base class defining all color properties
  - `BasicGreyTheme` and `AngelicTheme` implementations
  - `ThemeManager` for theme switching and application
- Callback system for theme changes
- Integration with CustomTkinter appearance modes
- Theme colors affect: backgrounds, buttons, canvas, grid, selections

### Performance
- **Optimized theme switching** for instant transitions
- Removed full canvas redraw (was taking ~1 second)
- Skipped `ctk.set_appearance_mode()` (causes full UI refresh)
- Created `_update_theme_canvas_elements()` for lightweight updates
- Only redraws grid and borders (theme-dependent elements)
- Uses canvas tags to preserve pixel rendering
- Result: **Instant theme switching** (< 50ms, appears immediate)

### Complete Coverage
- **All UI elements update**: Toolbar, panels, buttons, labels, dropdowns
- **Recursive widget updates**: `_apply_theme_to_children()` walks entire widget tree
- **Scrollbars themed**: Left/right panel scrollbars match theme
- **Dividers themed**: Panel dividers (PanedWindow sash) update
- **Nested frames**: All deeply nested widgets update automatically
- **Canvas elements**: Grid lines, borders, selection handles

## Version 1.21 - Pan Tool (October 13, 2025) ✅

### New Features
- **Pan Tool**: Move the camera view around the canvas
  - Open hand cursor when hovering
  - Grabbing hand cursor (fleur) when actively panning
  - Click and drag to pan the view
  - Useful for navigating large canvases or zoomed-in views
  - Pan button added to tool grid (10th tool)
  
### UI Updates
- Added **Pan** button to tool grid
  - Tooltip: "Move camera view (Hold Space)"
  - Open hand (hand2) cursor by default
  - Changes to grabbing hand (fleur) while dragging
  
### Technical
- Created `PanTool` in `src/tools/pan.py`
- Added `pan_offset_x` and `pan_offset_y` state variables
- Modified `_tkinter_screen_to_canvas_coords` to apply pan offset to coordinate conversion
- Modified `_update_pixel_display` to render pixels with pan offset applied
- Pan offset multiplied by zoom for proper screen-space panning

## Version 1.20 - Incremental Scaling Application (October 13, 2025) ✅

### Fixed
- **Scale Tool Incremental Application**: Pixels now maintain scaled size when releasing mouse button
- Each drag operation permanently applies scaling to pixel data
- Multiple drag operations build upon previous scaling results
- Better visual feedback during multi-drag scaling operations

### Technical
- Introduced `scale_true_original_rect` to track initial selection position (never changes during scaling session)
- `scale_original_rect` now updates after each drag release to enable relative scaling
- `_on_tkinter_canvas_mouse_up` applies scaling to `selected_pixels` on each release
- `_preview_scaled_pixels` uses true original rect for accurate pixel clearing and placement
- Simplified "click away" action - just exits scaling mode since pixels already applied
- Both reference rects update to new dimensions after applying each incremental scale

## Version 1.19 - Interactive Scaling & Copy Preview (October 13, 2025) ✅

### New Features
- **Scale Selection Tool**: Interactive pixel scaling with draggable handles
  - Click Scale button to enter scaling mode
  - Drag corner handles (yellow) to scale proportionally
  - Drag edge handles (orange) to scale in one dimension
  - Click away from selection to apply scale
  - Press Escape to cancel scaling
  - Uses nearest-neighbor scaling for crisp pixel art

- **Copy Placement Preview**: Visual feedback during copy placement
  - Semi-transparent preview shows where pixels will be placed
  - Preview follows mouse cursor in real-time
  - Cyan dashed boundary box indicates placement area
  - Pixels snap to grid for precise placement

### UI Updates
- Added **Scale** button below Selection operations
  - Full-width button (spans 3 columns)
  - Gray styling matching other operation buttons
  - Tooltip: "Scale selection with draggable corners"
- Interactive handles appear in scaling mode:
  - Yellow squares at corners (8x8 pixels)
  - Orange squares at edge midpoints
  - Black outline for visibility
- **Dynamic cursor feedback**:
  - Arrow cursor when entering scale mode
  - Diagonal cursors (⬁ ⬂) when hovering corner handles
  - Directional cursors (↕ ↔) when hovering edge handles
  - Cursor restores to current tool when exiting scaling
- **Button state management**:
  - Scale button highlights blue when active
  - All tool buttons gray out in scaling mode
  - Button states restore when exiting scaling
  - Clear visual feedback that scaling mode is active
- **Flexible exit options**:
  - Press Escape to cancel scaling
  - Click any tool button to exit and switch tools
  - Click Mirror/Rotate/Copy to exit and perform operation
  - Clicking outside selection applies the scale
- **Multiple drag support**:
  - Can drag handles multiple times before applying
  - Each drag starts from current rectangle position
  - Real-time visual feedback during drag operations

### Technical Details
- Uses `scipy.ndimage.zoom()` for high-quality nearest-neighbor scaling
  - Fallback to pure numpy implementation if scipy unavailable
  - `order=0` parameter ensures crisp pixel scaling
- Handle detection with zoom-adaptive tolerance
  - `max(3, 8 // zoom)` adjusts for different zoom levels
- Real-time rectangle updates during drag
  - Minimum size constraint (1x1 pixels)
  - Dynamic preview redraws for smooth interaction
- Copy preview uses stipple pattern for semi-transparency
  - `stipple="gray50"` creates checkerboard effect
  - Cyan dashed outline (`dash=(4,4)`)

### Files Modified
- `src/ui/main_window.py`: Scale tool, copy preview, handle drawing
- `requirements.txt`: Added scipy>=1.11.0 dependency

### User Experience
- **Workflow**: Select → Scale → Apply → Continue editing
- **Smart Upscaling**: Scale 32x32 artwork to 64x64 canvas for detail work
- **Visual Feedback**: Always see exactly where copy will be placed
- **Intuitive Controls**: Drag handles like any design software
- Console messages guide user through each step

### Use Cases
- Upscale small sprites when switching to larger canvas
- Fine-tune selection size interactively
- Create multiple scaled variations quickly
- Preview copy placement before committing

---

## Version 1.18 - Selection Operations: Mirror, Rotate, Copy (October 13, 2025) ✅

### New Features
- **Mirror Selection**: Flip selected pixels horizontally
  - Click Mirror button to flip selection left-right
  - Updates instantly on canvas
  - Works with any selection size

- **Rotate Selection**: Rotate selected pixels 90° clockwise
  - Click Rotate button to rotate selection
  - Handles dimension changes automatically
  - Multiple rotations possible (click 4 times = full circle)

- **Copy Selection**: Duplicate selected pixels
  - Click Copy button to enter placement mode
  - Click anywhere on canvas to place copy
  - Press Escape to cancel placement
  - Can place multiple copies (click Copy again after each placement)

### UI Updates
- Added **Selection** section with 3 buttons below Tools:
  - Mirror button (gray) with tooltip "Flip selection horizontally"
  - Rotate button (gray) with tooltip "Rotate selection 90° clockwise"
  - Copy button (gray) with tooltip "Copy selection for placement"
- Buttons arranged in 3-column grid matching tools layout

### Technical Details
- Uses numpy operations for efficient pixel manipulation:
  - `np.flip(axis=1)` for horizontal mirroring
  - `np.rot90(k=-1)` for 90° clockwise rotation
- Copy buffer stores pixel data independently
- Placement mode overrides normal drawing behavior
- Escape key cancels copy placement mode

### Files Modified
- `src/ui/main_window.py`: Selection operations UI and implementation
- `src/tools/selection.py`: Move tool improvements

### User Experience
- Natural workflow: Select → Transform (Mirror/Rotate) or Copy → Place
- Instant visual feedback for all operations
- Console messages confirm each action
- Escape provides easy exit from copy mode

---

## Version 1.17 - Selection Tool Fix & Auto-Switch (October 13, 2025) ✅

### New Features
- **Auto-Switch to Move Tool**: After completing a selection, automatically switches to Move tool
  - Natural workflow: Select → Move
  - Eliminates manual tool switching
  - Console feedback: "Selection complete - switched to Move tool"

### Bug Fixes
- **Selection Tool Visual Feedback**: Fixed selection rectangle not appearing
  - Selection rectangle now displays while selecting
  - White outline with corner markers for visibility
  - Remains visible after selection completes
  - Properly scaled to canvas zoom level
- **Unicode Encoding Error**: Replaced all Unicode characters with ASCII tags
  - Changed ✓ to [OK]
  - Changed ⚠ to [WARN]
  - Changed ✗ to [ERROR]
  - Fixes console crashes on some Windows systems

### Technical Details
- Added `_draw_selection_on_tkinter()` method to render selection on canvas
- Selection rectangle drawn with corner markers (6px size)
- Callback system: `on_selection_complete` triggers tool switch
- Selection visual feedback integrated into `_update_pixel_display()`
- Removed all Unicode emoji from console output

### Files Modified
- `src/tools/selection.py`: Added callback system and improved visual feedback
- `src/ui/main_window.py`: Selection rendering, auto-switch, Unicode cleanup
- `src/utils/file_association.py`: Unicode cleanup

### User Experience Improvements
- Selection tool now provides clear visual feedback
- Smoother workflow with automatic tool switching
- No more console encoding errors
- Corner markers make selection boundaries more visible

---

## Version 1.16 - Tooltip System (October 13, 2025) ✅

### New Features
- **Tooltip System**: Helpful tooltips appear after 1 second hover
  - Simple, direct descriptions for each tool
  - Shows keyboard shortcut for quick reference
  - Professional light yellow tooltip styling
  - Tooltips disappear on click or mouse leave
  - Examples:
    - Brush: "Draw single pixels (B)"
    - Eraser: "Erase pixels (E)"
    - Fill: "Fill areas with color (F)"
    - Eyedropper: "Sample colors from canvas (I)"
    - Selection: "Select rectangular areas (S)"
    - Move: "Move selected pixels (M)"
    - Line: "Draw straight lines (L)"
    - Square: "Draw rectangles and squares (R)"
    - Circle: "Draw circles (C)"

### Bug Fixes
- **Selection Tool**: Fixed numpy import issue causing NameError
- Ensured all tool dependencies properly imported

### Technical Details
- Created `src/ui/tooltip.py` module with ToolTip class
- Tooltips use Tkinter Toplevel windows for clean appearance
- 1000ms (1 second) delay before showing tooltip
- Light yellow background (#ffffe0) with black text
- Solid border for clear visibility
- Auto-positioning below widget with offset
- Tooltips cancel on click or mouse leave

### Files Modified
- `src/ui/tooltip.py`: New tooltip system (NEW)
- `src/ui/main_window.py`: Added tooltips to all tool buttons
- `src/tools/selection.py`: Verified numpy import

### User Experience Improvements
- New users can quickly learn what each tool does
- Keyboard shortcuts displayed in tooltips for power users
- Non-intrusive 1-second delay prevents tooltip spam
- Professional appearance matching modern UI standards

---

## Version 1.15 - Tool Cursor Feedback (October 13, 2025) ✅

### New Features
- **Visual Tool Cursors**: Each tool now has a unique cursor icon for better user feedback
  - **Brush**: Pencil cursor for drawing
  - **Eraser**: X cursor for erasing pixels
  - **Fill**: Spraycan cursor for fill operations
  - **Eyedropper**: Crosshair cursor for precise color sampling
  - **Selection**: Crosshair cursor for selection areas
  - **Move**: Four-directional arrow cursor for moving objects
  - **Line**: Pencil cursor for drawing lines
  - **Square** (formerly Rectangle): Plus cursor for shape drawing
  - **Circle**: Circle cursor for circular shapes
- Cursor changes automatically when switching tools
- Initial cursor set on application startup (brush/pencil)

### UI Updates
- **Rectangle Tool Renamed**: "Rectangle" button now displays as "Square" for clarity
- More intuitive visual feedback when hovering over canvas
- Professional tool experience matching industry-standard editors

### Technical Details
- Added `cursor` property to base `Tool` class
- Each tool specifies its cursor type during initialization
- Canvas cursor updates in `_select_tool()` method
- Uses standard Tkinter cursor names for cross-platform compatibility
- Fixed missing numpy import in `selection.py`

### Files Modified
- `src/tools/base_tool.py`: Added cursor parameter to Tool.__init__()
- `src/tools/brush.py`: Set cursor to "pencil"
- `src/tools/eraser.py`: Set cursor to "X_cursor"
- `src/tools/fill.py`: Set cursor to "spraycan"
- `src/tools/eyedropper.py`: Set cursor to "tcross"
- `src/tools/selection.py`: Set cursor to "crosshair", added numpy import
- `src/tools/shapes.py`: Set cursors for Line (pencil), Rectangle (plus), Circle (circle)
- `src/ui/main_window.py`: Updated tool selection to change canvas cursor, renamed Rectangle to Square

### Benefits
- Improved user experience with clear visual feedback
- No more confusion about which tool is active
- Professional appearance matching industry standards
- Better accessibility and usability

---

## Version 1.14 - PNG Import with Auto-Downscaling (October 12, 2025) ✅

### New Features
- **PNG Import System**: Load PNGs directly into canvas for immediate editing
  - **Direct Canvas Loading**: No intermediate .pixpf file required
  - **Auto-downscaling**: Detects and handles scaled exports (128x128, 256x256, 512x512)
  - Validates PNG dimensions (16x16, 32x32, 64x64 or scaled versions)
  - Loads exact pixel data as RGBA into "Imported" layer
  - Auto-resizes canvas to match PNG dimensions
  - Clears existing project for fresh start
  - Save manually when ready (File → Save Project)
  - Error handling with clear user feedback
  - Created `src/utils/import_png.py` module with validation logic

### UI Updates
- Added "Import PNG" button to File menu (below "Open Project")
- File dialog filters for .png files only
- Dimension validation with scale detection
- Success message shows original size and downscale info
- Immediate canvas update - ready to edit right away

### Auto-Downscaling Feature
- **Detects scaled exports**: Checks 8x, 4x, 2x, 1x scales (in priority order)
- **Smart scale detection**: Prioritizes 8x (default export scale) first
- **Examples**:
  - 256x256 PNG → Auto-downscales 8x to 32x32 canvas ✅
  - 128x128 PNG → Auto-downscales 8x to 16x16 canvas ✅
  - 512x512 PNG → Auto-downscales 8x to 64x64 canvas ✅
- Uses nearest-neighbor scaling to preserve pixel-perfect art
- Console feedback shows detected scale and downscale action
- Correctly restores original canvas size when re-importing

### Use Cases
- **Re-edit exported PNG sprites** (most common workflow - export, edit externally, re-import)
- Import pixel art from other tools (Aseprite, Photoshop, etc.)
- Convert existing 16x16/32x32/64x64 PNGs to editable projects
- Quick project creation from screenshots or images

### Technical Details
- Uses PIL/Pillow for PNG loading and scaling
- Converts to RGBA numpy array
- Generates valid .pixpf JSON structure
- Includes metadata: import date, source filename, original size
- Default zoom based on canvas size (16x for 16/32, 8x for 64)
- Scale detection algorithm checks all common export scales

### Bug Fixes
- **Canvas Dimension Sync**: Fixed index out of bounds errors during import
  - Properly initialize canvas.pixels array before layer operations
  - Update dimensions before clearing layers
  - Copy layer data to canvas before creating pygame surface
  - Correct order: dimensions → canvas.pixels → layers → update → surface
- **Scale Detection Priority**: Fixed incorrect canvas size on re-import
  - Now checks scales in reverse order (8x, 4x, 2x, 1x)
  - Prioritizes original export scale (8x) over smaller scales
  - Prevents 128x128 from being detected as 64x64 at 2x instead of 16x16 at 8x
  - Correctly restores original canvas dimensions when re-importing exported PNGs

### Files Modified
- **NEW**: `src/utils/import_png.py` - PNG import utility with auto-downscaling (228 lines)
- `src/ui/main_window.py` - Added `_import_png()` method with proper dimension handling (105 lines)
- Menu integration and canvas synchronization logic

---

## Version 1.13 - UI Improvements & Complete Palette System (October 11, 2025) ✅

### New Features
- **Custom Application Icon**: Colorful 4×4 pixel grid logo
  - Displays in EXE file icon, window title bar, and Windows taskbar
  - Proper Windows ICO format with 7 icon sizes (16×16 to 256×256)
  - Fixed runtime icon loading for PyInstaller bundled executables
  - Uses `sys.frozen` detection to locate assets correctly when bundled
- **Resizable Side Panels**: Drag dividers to resize left/right panels horizontally
- **All 6 Palettes Available**: Added 4 missing palette JSON files to distribution

### UI Improvements
1. **Compact 3×3 Tool Grid**: Reorganized tools from vertical stack to grid layout
   - Saves ~130+ pixels of vertical space
   - Fixed button sizes (85px × 28px)
   - Centered Tools section with proper frame wrapping

2. **Reduced Vertical Spacing**: Tightened padding throughout panels
   - Tools panel padding reduced by ~50%
   - Palette panel padding reduced by ~50-65%
   - Total space saved: ~180+ pixels

3. **Resizable Panel System**: Implemented tkinter PanedWindow
   - Left panel: 500px default (min 220px)
   - Right panel: 300px default (min 220px)
   - Canvas: 400px minimum, always expands
   - 8px raised sash handles for easy resizing

### Bug Fixes
- **Project Import Not Working**: Fixed `load_project()` call missing required parameters
  - Now passes canvas, palette, layer_manager, and timeline objects
  - Calls `_update_canvas_from_layers()` to composite loaded layers to canvas
  - Added immediate UI refresh with `root.update()` calls
  - Pixels now display immediately when loading projects
  - Fixed method names: `refresh()` for layer and timeline panels
  - Added better error handling with traceback output
- **Missing Palette Files**: Created 4 missing palette JSON files
  - heartwood_online.json (forest theme)
  - definya.json (bright, vibrant colors)
  - kakele_online.json (warm, golden palette)
  - rucoy_online.json (grayscale with earth tones)
- **Tool Button Text**: Changed "Rect" to "Rectangle" for clarity

### UI Polish & Layout
- **Centered Palette Layout**: View mode buttons and color grid now centered
  - Grid/Primary/Wheel buttons centered under Palette dropdown  
  - Color display grid centered in its container
  - Matches the centered design of Tools section
- **Custom Colors Expansion**: Color buttons expand to fill container width
  - Grid columns configured with equal weights (4 columns)
  - Buttons use `sticky="nsew"` to fill their grid cells
  - Increased button size from 40x40 to 50x50 pixels
  - Eliminates wasted space on the right side

### Custom File Icon System
- **Auto-Register .pixpf Icon**: Purple diamond icon for project files
  - Automatically registers on first program launch
  - Uses Windows registry (HKEY_CURRENT_USER) - no admin needed
  - Created `src/utils/file_association.py` module
  - Checks if already registered to avoid duplicate work
  - Manual fallback: `register_pixpf_icon.bat` included in distribution
  - All `.pixpf` files display custom icon in File Explorer
  - Converted save.png to pixpf_icon.ico (256x256 max size)

### Files Modified
- `src/ui/main_window.py` - Resizable panels, compact tool grid, centered palette
- `src/ui/color_wheel.py` - Expanding custom colors grid
- `src/core/color_palette.py` - OSRS palette + enum
- `assets/palettes/` - Added OSRS + 4 missing palettes
- `BUILDER/build.bat` - Updated with all new modules and icons
- `main.py` - Added file association registration on startup
- **NEW**: `src/utils/file_association.py` - Icon registration utility
- **NEW**: `assets/icons/pixpf_icon.ico` - Custom file type icon
- **NEW**: `register_pixpf_icon.bat` - Manual registration script
- **NEW**: `docs/ADDING_PALETTES.md` - Palette creation guide

---

## Version 1.11 - 64x64 Canvas Size Addition (October 11, 2025) ✅

### New Features
- **64x64 Canvas Size**: Added extra-large canvas preset for detailed sprites and tile sets
- **Auto-Zoom Adjustment**: Automatically adjusts zoom to 8x for large canvases (32x64, 64x64) to ensure optimal viewing

### Bug Fixes - Critical
1. **Layer Dimension Caching Bug** ⭐ CRITICAL
   - Fixed Layer class not updating cached width/height after resize
   - Symptom: Could only draw in 32x32 area regardless of canvas size
   - Solution: Update layer.width and layer.height when resizing pixel arrays

2. **Canvas Resize Synchronization**
   - Fixed layer manager and timeline not resizing with canvas
   - Symptom: IndexError when drawing after canvas resize
   - Solution: Call resize_layers() and resize_frames() on canvas size change

3. **Mouse Coordinate Conversion**
   - Fixed incorrect coordinate conversion subtracting widget position twice
   - Symptom: Drawing only worked in upper-left portion of canvas
   - Solution: Removed incorrect winfo_x/y subtraction (event coordinates already widget-relative)

4. **Infinite Redraw Loop**
   - Fixed redraw loop causing console spam and rendering issues
   - Symptom: "Initial draw complete!" repeating endlessly, laggy drawing
   - Solution: Changed _update_canvas_from_layers() to use _update_pixel_display() instead of _initial_draw()

### Technical Changes
- `src/core/canvas.py`: Added CanvasSize.XLARGE = (64, 64)
- `src/core/layer_manager.py`: Added layer dimension update in resize_layers()
- `src/ui/main_window.py`: Enhanced _on_size_change() with layer sync and auto-zoom

### Testing Status
✅ All canvas sizes tested and working:
- 16x16 ✅
- 32x32 ✅
- 16x32 ✅
- 32x64 ✅
- 64x64 ✅

---

## Version 1.10 - Complete Color System Overhaul (Previous)

### Bug Fixes
- Color wheel radio button layout
- Color selection visual feedback
- Color variation highlighting
- Color variation duplicates
- Dynamic color grids

---

## Version 1.09 - UI Improvements (Previous)

### Features
- Primary colors widget duplication fix
- Launch script auto-close enhancement
- Color button hover effects

---

## Version 1.08 - Undo/Redo System (Previous)

### Features
- Complete undo/redo functionality
- Grid centering on window resize
- Keyboard shortcuts (Ctrl+Z, Ctrl+Y)

---

## Version 1.05 - GitHub Release (October 10, 2024)

### Milestone
- Project published to GitHub
- Standalone executable available
- Production ready status

---

## Version 1.0 - Initial Release

### Complete Features
- 9 drawing tools
- 6 color palettes + color wheel
- Layer system with 10 layers
- Animation timeline
- Export system (PNG, GIF, sprite sheets)
- Undo/redo with 50+ state history
- 8 preset templates
- Project save/load system

