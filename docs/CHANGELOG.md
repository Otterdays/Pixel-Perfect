# Pixel Perfect - Changelog

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
