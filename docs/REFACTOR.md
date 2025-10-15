# Pixel Perfect - Refactoring Guide

**Last Updated**: December 2024  
**Version**: 1.71  
**Status**: 🟢 **IN PROGRESS** - Phases 1, 3, 4, 5, 6, 7 + Grid Control + Notes Panel Complete!

---

## 🎯 Current Status

**main_window.py**: **1,634 lines** (down from 3,387)  
**Progress**: 51.7% reduction (1,753 lines removed)  
**Target**: ~850-900 lines (core orchestration only)  
**Remaining**: ~734 lines to extract (2 major phases)

### Completed Extractions ✅
- ✅ **UIBuilder** (436 lines) - Toolbar, tool panel, palette panel, canvas panel
- ✅ **EventDispatcher** (472 lines) - All mouse/keyboard event handling
- ✅ **FileOperationsManager** (395 lines) - All file I/O operations
- ✅ **DialogManager** (402 lines) - All custom dialogs (size, warning, texture)
- ✅ **SelectionManager** (438 lines) - All selection operations (mirror, rotate, scale, copy)
- ✅ **CanvasRenderer** (expanded to 494 lines) - All rendering operations (grid, pixels, previews)
- ✅ **ToolSizeManager** (163 lines) - Brush/eraser size selection and drawing
- ✅ **CanvasZoomManager** (226 lines) - Canvas resizing and zoom controls
- ✅ **GridControlManager** (68 lines) - Grid visibility and overlay controls
- ✅ **NotesPanel** (200+ lines) - Persistent notes with auto-save and export

### Next Up 📋
**Phase 2: Color View Manager** (~400 lines) - All color view management (grid, wheel, saved, constants)  
**Phase 8: Layer & Animation Manager** (~200 lines) - Layer operations and animation controls  
**Phase 9: Canvas Operations Manager** (~134 lines) - Canvas coordinate conversion and layer sync

---

## 📊 Progress Tracking

| Phase | Est. Lines | Actual | Cumulative | Status |
|-------|-----------|--------|------------|--------|
| **Starting Point** | - | - | **3,387** | Baseline |
| Phase 3: File Ops | 400 | **358** | **3,029** | ✅ **COMPLETE** |
| Phase 4: Dialogs | 300 | **323** | **2,724** | ✅ **COMPLETE** |
| Phase 1: Selection | 500 | **350** | **2,374** | ✅ **COMPLETE** |
| Phase 5: Renderer | 400 | **486** | **1,888** | ✅ **COMPLETE** |
| Phase 6: Tool Sizes | 140 | **115** | **1,773** | ✅ **COMPLETE** |
| Phase 7: Canvas/Zoom | 180 | **159** | **1,614** | ✅ **COMPLETE** |
| Grid Control | 30 | **32** | **1,582** | ✅ **COMPLETE** |
| Notes Panel | 50 | **52** | **1,634** | ✅ **COMPLETE** |
| Phase 2: Colors | 400 | TBD | ~1,234 | ⏳ Pending |
| Phase 8: Layer/Anim | 200 | TBD | ~1,034 | ⏳ Pending |
| Phase 9: Canvas Ops | 134 | TBD | ~900 | ⏳ Pending |

**Note**: Notes Panel added 52 lines back due to new feature implementation. Still on track for target!

---

## 🎯 Key Insights (Read This First!)

### Critical Success Factors
1. **Do ONE phase at a time** - Complete, test, document, then stop for user validation
2. **Test tool consistency obsessively** - Brush/eraser size switching is the #1 failure mode
3. **Use callbacks for managers** - Keeps code decoupled while allowing canvas updates
4. **PowerShell for bulk deletions** - Array slicing beats multiple search_replace calls
5. **Update EventDispatcher carefully** - It has tight coupling with main_window methods

### Easiest → Hardest Extractions
1. ✅ **File Operations** (DONE) - Self-contained, clean boundaries
2. ✅ **Dialog Manager** (DONE) - Self-contained, no tool dependencies
3. ✅ **Selection Manager** (DONE) - Moderate complexity, clear boundaries
4. ✅ **Canvas Renderer** (DONE) - Technical but isolated
5. ✅ **Tool Size Manager** (DONE) - Clean tool coordination
6. ✅ **Canvas/Zoom Manager** (DONE) - Canvas management
7. ✅ **Grid Control** (DONE) - Simple grid operations
8. ✅ **Notes Panel** (DONE) - Self-contained feature
9. **Canvas Operations Manager** (NEXT) - Utility functions, low complexity ← **DO THIS NEXT**
10. **Layer & Animation Manager** - Medium complexity, clear boundaries
11. **Color View Manager** - Complex UI references, do LAST

### Realistic Timeline
- **Per phase**: 1-2 hours (extraction + testing + documentation)
- **Total remaining**: 3 phases × 1.5 hours = ~4-5 hours
- **Do in sessions**: 1-2 phases per work session

---

## 📋 Remaining Phases (Detailed)

### Phase 2: Color View Manager (~400 lines) ← **NEXT**
**File**: `src/ui/color_view_manager.py`

**Methods to extract**:
- `_initialize_all_views()` - Pre-render all views (24 lines)
- `_show_view()` - Toggle view visibility (40 lines) - **COMPLEX UI LOGIC**
- `_on_view_mode_change()` - Radio button handler (5 lines)
- `_create_constants_grid()` - Constants view UI (64 lines)
- `_get_canvas_colors()` - Extract used colors (17 lines)
- `_on_constant_color_click()` - Color selection (28 lines)
- `_create_saved_colors_view()` - Saved colors UI (96 lines)
- `_update_saved_color_buttons()` - Update UI (26 lines)
- `_on_saved_slot_click()` - Empty slot click (19 lines)
- `_on_saved_color_click()` - Filled slot click (9 lines)
- `_export_saved_colors()` - Export to file (14 lines)
- `_import_saved_colors()` - Import from file (15 lines)
- `_clear_all_saved_colors()` - Clear all slots (94 lines)
- `_create_color_wheel()` - Wheel UI creation (18 lines)
- `_on_color_wheel_changed()` - Wheel callback (9 lines)
- `_save_custom_color()` - Add custom color (19 lines)
- `_remove_custom_color()` - Remove custom (7 lines)
- `_update_custom_colors_display()` - Update UI (6 lines)
- `_set_color_from_eyedropper()` - Eyedropper result (27 lines)

**Complexity**: HIGH - Heavy UI widget management and view switching logic

---

### Phase 8: Layer & Animation Manager (~200 lines)
**File**: `src/ui/layer_animation_manager.py`

**Methods to extract**:
- `_create_layer_and_timeline_panels()` - Layer/timeline UI (77 lines)
- `_on_layer_changed()` - Layer change callback (5 lines)
- `_add_layer()` - Add new layer (7 lines)
- `_sync_canvas_with_layers()` - Layer sync (11 lines)
- `_on_frame_changed()` - Frame change callback (10 lines)
- `_toggle_animation()` - Animation toggle (8 lines)
- `_previous_frame()` - Previous frame (6 lines)
- `_next_frame()` - Next frame (6 lines)
- `_update_canvas_from_layers()` - Canvas update (8 lines)
- `_clear_selection_and_reset_tools()` - Tool reset (10 lines)
- `_get_drawing_layer()` - Get active layer (11 lines)
- `_handle_eyedropper_click()` - Eyedropper handler (22 lines)
- `_set_color_from_eyedropper()` - Color setting (28 lines)

**Complexity**: MEDIUM - Layer and animation coordination

---

### Phase 9: Canvas Operations Manager (~134 lines)
**File**: `src/ui/canvas_operations_manager.py`

**Methods to extract**:
- `_tkinter_screen_to_canvas_coords()` - Coordinate conversion (28 lines)
- `_calculate_optimal_panel_widths()` - Panel sizing (41 lines)
- `_save_window_state()` - Window state save (28 lines)
- `_restore_window_state()` - Window state restore (42 lines)
- `_redraw_canvas_after_resize()` - Canvas redraw (5 lines)

**Complexity**: LOW - Utility functions and window management

---

## ✅ Lessons Learned from Real Refactoring

### What Worked Well

#### 1. Callback Pattern for Managers
```python
# In manager __init__:
self.force_canvas_update_callback = None
self.update_canvas_from_layers_callback = None

# In main_window after manager creation:
self.file_ops.force_canvas_update_callback = self._force_tkinter_canvas_update
self.file_ops.update_canvas_from_layers_callback = self._update_canvas_from_layers
```
**Why**: Keeps managers decoupled while allowing necessary canvas updates

#### 2. PowerShell for Bulk Deletions
```powershell
(Get-Content 'file.py')[0..2312] + (Get-Content 'file.py')[2661..9999] | Set-Content 'file.py'
```
**Why**: When deleting 300+ lines, this is faster and cleaner than multiple search_replace calls

#### 3. One Phase at a Time
- Complete ONE extraction phase
- Test thoroughly
- Update documentation
- Let user test before proceeding

**Why**: Prevents cascading errors and makes debugging easier

#### 4. Manager Initialization Timing
- Initialize managers AFTER UI panels are created
- Some managers need references to UI components
- Set callbacks immediately after initialization

**Why**: Prevents AttributeError from missing references

---

### ⚠️ Critical Warnings

#### 1. Tool Consistency is FRAGILE
**Problem**: Mixing canvas-based (1x1) and layer-based (2x2/3x3) drawing causes pixel loss

**Solution**: 
- ALL tool sizes must use same approach (layer-based)
- ALL operations must call `_update_canvas_from_layers()`
- Create helper methods like `_draw_brush_at()` and `_draw_eraser_at()`

**Test**: Switch between tool sizes multiple times - previous work must stay visible

#### 2. Event Dispatcher Interactions
**Problem**: EventDispatcher delegates to main_window methods, creating tight coupling

**Be Careful With**:
- Methods that EventDispatcher calls must still exist in main_window
- Multi-pixel tools need special handling in EventDispatcher
- Eyedropper tool needs access to color wheel updates

**Solution**: Keep event-related methods in main_window or update EventDispatcher appropriately

#### 3. File Reversion Disasters
**Problem**: Git reverts or bad merges can destroy working code

**Prevention**:
- Commit working code before major changes
- Test after EVERY file operation
- Keep backups of critical files
- Don't commit until user confirms working

#### 4. UI Widget References
**Problem**: Extracting UI creation can break widget references elsewhere

**Watch For**:
- `self.tool_buttons` - needed by multiple systems
- `self.drawing_canvas` - needed for cursor changes
- Palette view frames - needed for view switching
- Radio button variables - needed for callbacks

**Solution**: Initialize empty containers BEFORE UIBuilder, populate them during build

---

## 🔧 Technical Patterns

### Manager Class Template
```python
class SomeManager:
    def __init__(self, root, canvas, ...required_refs):
        self.root = root
        self.canvas = canvas
        # ... store all required references
        
        # Callbacks (set by main_window after init)
        self.some_callback = None
    
    def some_operation(self):
        # Do operation
        # Call callback if needed
        if self.some_callback:
            self.some_callback()
```

### Integration in main_window.py
```python
# After UI creation and panel initialization
self.some_manager = SomeManager(self.root, self.canvas, ...)
self.some_manager.some_callback = self._some_internal_method

# Update menu/buttons to use manager
# Old: command=self._some_method
# New: command=self.some_manager.some_method
```

---

## 🧪 Testing Checklist

After EACH phase, test systematically:

### Core Functionality
1. **Application Startup**: No errors, all UI elements visible
2. **Tool Selection**: All tools selectable and highlighted properly
3. **Tool Operations**: Brush, eraser, fill, eyedropper work correctly
4. **Tool Sizes**: Multi-size tools (2x2, 3x3) work consistently

### Tool Consistency (CRITICAL)
5. **Brush Size Switching**: Switch between 1x1, 2x2, 3x3 - previous work stays visible
6. **Eraser Size Switching**: Switch between sizes - canvas doesn't corrupt
7. **Tool Switching**: Switch between different tools - no pixel loss
8. **Layer Integration**: All tools properly update layers AND canvas display

### UI Components
9. **Palette Views**: Grid, Wheel, Primary, Constants, Saved all functional
10. **Color Selection**: Clicking colors updates primary/secondary properly
11. **Panel Toggles**: Left/right panels collapse and restore correctly
12. **File Menu**: All file operations accessible and functional

### File Operations
13. **New Project**: Clears canvas, resets layers and timeline
14. **Open Project**: Loads .pixpf files correctly
15. **Save/Save As**: Persists project data
16. **Import PNG**: Loads PNG into canvas with proper dimensions
17. **Export**: PNG, GIF, Spritesheet exports work

### Documentation
18. Update SCRATCHPAD.md with version entry
19. Update SUMMARY.md with latest changes
20. Update My_Thoughts.md with lessons learned
21. Mark todos complete in todo list

### When Issues Arise
- **DO NOT commit** until fully tested
- Document the issue in SCRATCHPAD.md
- Test with multiple canvas sizes
- Test tool consistency thoroughly
- Verify layer/canvas synchronization

---

## 🏗️ Final Architecture

```
src/ui/
├── main_window.py (~900 lines) - Core orchestration only
├── ui_builder.py ✅ - UI creation (toolbar, tools, palette, canvas)
├── file_operations_manager.py ✅ - File I/O
├── selection_manager.py ✅ - Selection operations
├── color_view_manager.py (TODO) - Color view management
├── dialog_manager.py ✅ - Custom dialogs
├── layer_animation_manager.py (TODO) - Layer & animation coordination
├── canvas_operations_manager.py (TODO) - Canvas utilities & window state
├── tool_size_manager.py ✅ - Tool sizing
├── canvas_zoom_manager.py ✅ - Canvas management
├── grid_control_manager.py ✅ - Grid controls
├── notes_panel.py ✅ - Notes feature
├── theme_manager.py - Theme system
├── theme_dialog_manager.py - Theme dialogs
├── layer_panel.py - Layer UI
├── timeline_panel.py - Animation UI
├── color_wheel.py - Color wheel widget
└── tooltip.py - Tooltip system

src/core/
├── event_dispatcher.py ✅ - Event routing
├── canvas_renderer.py ✅ - All rendering
├── canvas.py - Canvas data
├── layer_manager.py - Layer system
└── ...
```

---

## 🚀 Quick Start: Next Phase

### To Extract Phase 9 (Canvas Operations Manager):

1. **Create new file**: `src/ui/canvas_operations_manager.py`

2. **Extract utility methods** from main_window.py:
   - `_tkinter_screen_to_canvas_coords()`
   - `_calculate_optimal_panel_widths()`
   - `_save_window_state()`
   - `_restore_window_state()`
   - `_redraw_canvas_after_resize()`

3. **Use callback pattern**:
   ```python
   self.canvas_ops = CanvasOperationsManager(self.root, self.canvas, ...)
   self.canvas_ops.window_state_callback = self.window_state_mgr.save_state
   ```

4. **Update main_window** to use manager:
   ```python
   # Old: self._tkinter_screen_to_canvas_coords(x, y)
   # New: self.canvas_ops.tkinter_screen_to_canvas_coords(x, y)
   ```

5. **Delete old methods** (PowerShell):
   ```powershell
   (Get-Content 'src/ui/main_window.py')[0..BEFORE] + 
   (Get-Content 'src/ui/main_window.py')[AFTER..9999] | 
   Set-Content 'src/ui/main_window.py'
   ```

6. **Test thoroughly** using the checklist above

7. **Update docs**:
   - SCRATCHPAD.md (version entry)
   - SUMMARY.md (latest changes)
   - My_Thoughts.md (lessons learned)
   - This file (mark phase complete)

---

## 📚 References

- **Progress Log**: [SCRATCHPAD.md](SCRATCHPAD.md)
- **Lessons Learned**: [My_Thoughts.md](My_Thoughts.md)
- **Summary**: [SUMMARY.md](SUMMARY.md)

---

**Remember**: The goal isn't perfection - it's **progressive improvement**. Each phase makes the codebase better!
