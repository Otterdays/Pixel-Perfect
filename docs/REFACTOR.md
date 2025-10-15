# Pixel Perfect - Refactoring Guide

**Last Updated**: October 15, 2025  
**Version**: 1.62  
**Status**: 🟢 **IN PROGRESS** - Phase 3 Complete!

---

## 🎯 Current Status

**main_window.py**: **2,724 lines** (down from 3,387)  
**Progress**: 19.6% reduction (663 lines removed)  
**Target**: ~850-900 lines (core orchestration only)  
**Remaining**: ~1,870 lines to extract (4 phases)

### Completed Extractions ✅
- ✅ **UIBuilder** (436 lines) - Toolbar, tool panel, palette panel, canvas panel
- ✅ **EventDispatcher** (472 lines) - All mouse/keyboard event handling
- ✅ **FileOperationsManager** (395 lines) - All file I/O operations
- ✅ **DialogManager** (417 lines) - All custom dialogs (size, warning, texture)

### Next Up 📋
**Phase 1: Selection Manager** (~500 lines) - Selection operations (mirror, rotate, scale, copy)

---

## 📊 Progress Tracking

| Phase | Est. Lines | Actual | Cumulative | Status |
|-------|-----------|--------|------------|--------|
| **Starting Point** | - | - | **3,387** | Baseline |
| Phase 3: File Ops | 400 | **358** | **3,029** | ✅ **COMPLETE** |
| Phase 4: Dialogs | 300 | **323** | **2,724** | ✅ **COMPLETE** |
| Phase 1: Selection | 500 | TBD | ~2,200 | 📋 **Next** |
| Phase 5: Renderer | 400 | TBD | ~1,800 | ⏳ Pending |
| Phase 2: Colors | 600 | TBD | ~1,200 | ⏳ Pending |
| Phase 6: UI Builder | 300 | TBD | ~900 | ⏳ Pending |

**Note**: Estimates are ~10-15% optimistic. Phase 3 achieved 89% of estimate (358 vs 400).

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
2. **Dialog Manager** (NEXT) - Self-contained, no tool dependencies  ← **DO THIS NEXT**
3. **Selection Manager** - Moderate complexity, clear boundaries
4. **Canvas Renderer** - Technical but isolated
5. **Color View Manager** - Complex UI references, do LAST

### Realistic Timeline
- **Per phase**: 1-2 hours (extraction + testing + documentation)
- **Total remaining**: 5 phases × 1.5 hours = ~7-8 hours
- **Do in sessions**: 1-2 phases per work session

---

## 📋 Remaining Phases (Detailed)

### Phase 4: Dialog Manager (~300 lines) ← **NEXT**
**File**: `src/ui/dialog_manager.py`

**Methods to extract**:
- `_open_custom_size_dialog()` - Custom canvas size (131 lines)
- `_show_downsize_warning()` - Downsize warning (108 lines)
- `_open_texture_panel()` - Texture library (46 lines)
- `_create_texture_button()` - Texture button creation (68 lines)
- `_select_texture()` - Texture selection (13 lines)

**Note**: Keep `_show_file_menu()` in main_window (needs file_ops reference)

---

### Phase 1: Selection Manager (~500 lines)
**File**: `src/ui/selection_manager.py`

**Methods to extract**:
- `_on_selection_complete()` - Auto-switch to move tool
- `_mirror_selection()` - Horizontal flip (52 lines)
- `_rotate_selection()` - 90° clockwise (69 lines)
- `_copy_selection()` - Enter copy mode (34 lines)
- `_scale_selection()` - Enter scaling mode (30 lines)
- `_apply_scale()` - Apply scaling (17 lines)
- `_simple_scale()` - Scaling algorithm (30 lines)
- `_preview_scaled_pixels()` - Live preview (38 lines)
- `_get_scale_handle()` - Detect handle (29 lines)
- `_place_copy_at()` - Place copied pixels (29 lines)

---

### Phase 5: Canvas Renderer Expansion (~400 lines)
**File**: `src/core/canvas_renderer.py` (expand existing)

**Methods to extract**:
- `_init_drawing_surface()` - Surface initialization (5 lines)
- `_initial_draw()` - Initial render (52 lines)
- `_draw_tkinter_grid()` - Grid lines (25 lines)
- `_draw_all_pixels_on_tkinter()` - Pixel rendering (21 lines)
- `_force_tkinter_canvas_update()` - Force update (10 lines)
- `_update_pixel_display()` - Display update (51 lines)
- `_draw_selection_on_tkinter()` - Selection overlay (128 lines)
- `_update_single_pixel()` - Single pixel update (6 lines)
- `_draw_shape_preview()` - Shape preview (94 lines)
- `_draw_brush_preview()` - Brush preview (50 lines)
- `_draw_eraser_preview()` - Eraser preview (47 lines)
- `_draw_texture_preview()` - Texture preview (58 lines)

---

### Phase 2: Color View Manager (~600 lines) **MOST COMPLEX - DO LAST**
**File**: `src/ui/color_view_manager.py`

**Methods to extract**:
- `_initialize_all_views()` - Pre-render all views (24 lines)
- `_show_view()` - Toggle view visibility (27 lines)
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

---

### Phase 6: UI Builder Completion (~300 lines)
**File**: `src/ui/ui_builder.py` (expand existing)

**Methods to extract**:
- `_create_layer_and_timeline_panels()` - Layer/timeline UI (77 lines)
- Any remaining UI creation methods

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
├── main_window.py (~850 lines) - Core orchestration only
├── ui_builder.py ✅ - UI creation (toolbar, tools, palette, canvas)
├── file_operations_manager.py ✅ - File I/O
├── selection_manager.py (TODO) - Selection operations
├── color_view_manager.py (TODO) - Color view management
├── dialog_manager.py (TODO) - Custom dialogs
├── theme_manager.py - Theme system
├── theme_dialog_manager.py - Theme dialogs
├── layer_panel.py - Layer UI
├── timeline_panel.py - Animation UI
├── color_wheel.py - Color wheel widget
└── tooltip.py - Tooltip system

src/core/
├── event_dispatcher.py ✅ - Event routing
├── canvas_renderer.py (TODO: expand) - All rendering
├── canvas.py - Canvas data
├── layer_manager.py - Layer system
└── ...
```

---

## 🚀 Quick Start: Next Phase

### To Extract Phase 4 (Dialog Manager):

1. **Create new file**: `src/ui/dialog_manager.py`

2. **Extract dialog methods** from main_window.py:
   - `_open_custom_size_dialog()`
   - `_show_downsize_warning()`
   - `_open_texture_panel()`
   - `_create_texture_button()`
   - `_select_texture()`

3. **Use callback pattern**:
   ```python
   self.dialog_mgr = DialogManager(self.root, self.canvas, ...)
   self.dialog_mgr.apply_size_callback = self._apply_custom_canvas_size
   ```

4. **Update main_window** to use manager:
   ```python
   # Old: self._open_custom_size_dialog()
   # New: self.dialog_mgr.open_custom_size_dialog()
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
