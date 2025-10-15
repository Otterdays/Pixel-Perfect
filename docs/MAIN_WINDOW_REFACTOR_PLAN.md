# Main Window Refactor Plan

## Current Status (Updated October 2025)
- **main_window.py**: 3,029 lines (down from 3,387), ~95 methods
- **Progress**: Phase 3 Complete ✅ (File Operations Manager extracted)
- **Target**: Reduce main_window.py to ~850 lines (core orchestration only)
- **Actual Reduction So Far**: 358 lines (10.6%)

### Completed Extractions
- ✅ **UIBuilder** (toolbar, tool panel, palette panel, canvas panel)
- ✅ **EventDispatcher** (all mouse/keyboard event handling)
- ✅ **FileOperationsManager** (all file I/O operations)

## 🎯 Key Insights (Read This First!)

### Critical Success Factors
1. **Do ONE phase at a time** - Complete, test, document, then stop for user validation
2. **Test tool consistency obsessively** - Brush/eraser size switching is the #1 failure mode
3. **Use callbacks for managers** - Keeps code decoupled while allowing canvas updates
4. **PowerShell for bulk deletions** - Array slicing beats multiple search_replace calls
5. **Update EventDispatcher carefully** - It has tight coupling with main_window methods

### Most Dangerous Operations
1. ⚠️ **Tool operations** - Must maintain canvas/layer sync or pixels disappear
2. ⚠️ **Color management** - Complex UI widget references, do this LAST
3. ⚠️ **Event dispatcher changes** - Can break mouse/keyboard input if done wrong

### Easiest Extractions (Do These First)
1. ✅ File Operations (DONE) - Self-contained, clean
2. Dialog Management (NEXT) - No dependencies, easy win
3. Selection Manager - Clear boundaries
4. Canvas Renderer - Technical but isolated

### Realistic Timeline
- **Per phase**: 1-2 hours (extraction + testing + documentation)
- **Total remaining**: 5 phases × 1.5 hours = ~7-8 hours
- **Do in sessions**: 1-2 phases per work session

## Problem Analysis

The main_window.py file is too large and contains multiple responsibilities:
1. UI creation (partially moved to UIBuilder)
2. Selection tool operations (mirror, rotate, scale, copy)
3. Color management (views, saved colors, constants, wheel)
4. File operations (import, export, save, load)
5. Dialog creation (custom size, texture panel, warnings)
6. Canvas rendering (grid, pixels, selection preview)
7. Event coordination
8. Tool management
9. Layer/animation coordination

## Refactor Strategy

### Phase 1: Extract Selection Operations (~500 lines)
**New file**: `src/ui/selection_manager.py`

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

**Estimated reduction**: 500+ lines

### Phase 2: Extract Color Management (~600 lines)
**New file**: `src/ui/color_view_manager.py`

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

**Estimated reduction**: 600+ lines

### Phase 3: Extract File Operations (~400 lines)
**New file**: `src/ui/file_operations_manager.py`

**Methods to extract**:
- `_new_project()` - New project (19 lines)
- `_open_project()` - Open file (39 lines)
- `_save_project()` - Save to disk (17 lines)
- `_save_project_as()` - Save as dialog (23 lines)
- `_import_png()` - PNG import (112 lines)
- `_export_png()` - PNG export (25 lines)
- `_export_gif()` - GIF export (26 lines)
- `_export_spritesheet()` - Spritesheet export (26 lines)
- `_show_templates()` - Template dialog (42 lines)
- `_load_template()` - Load template (20 lines)

**Estimated reduction**: 400+ lines

### Phase 4: Extract Dialog Management (~300 lines)
**New file**: `src/ui/dialog_manager.py` (or merge with existing theme_dialog_manager.py)

**Methods to extract**:
- `_open_custom_size_dialog()` - Custom canvas size (131 lines)
- `_show_downsize_warning()` - Downsize warning (108 lines)
- `_open_texture_panel()` - Texture library (46 lines)
- `_create_texture_button()` - Texture button creation (68 lines)
- `_select_texture()` - Texture selection (13 lines)
- `_show_file_menu()` - File menu popup (54 lines)

**Estimated reduction**: 300+ lines

### Phase 5: Extract Canvas Rendering (~400 lines)
**Move to**: `src/core/canvas_renderer.py` (already exists, expand it)

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

**Estimated reduction**: 400+ lines

### Phase 6: Complete UI Builder Extraction (~300 lines)
**Add to**: `src/ui/ui_builder.py`

**Methods to extract**:
- `_create_layer_and_timeline_panels()` - Layer/timeline UI (77 lines)
- Any remaining UI creation methods

**Estimated reduction**: 300+ lines

## Progress Tracking

| Phase | Est. Lines | Actual Lines | Cumulative Size | Status |
|-------|-----------|--------------|-----------------|--------|
| **Starting Point** | - | - | **3,387** | Baseline |
| Phase 3: File Operations | 400 | 358 | **3,029** | ✅ **COMPLETE** |
| Phase 4: Dialog Management | 300 | TBD | ~2,700 | 📋 **Next** |
| Phase 1: Selection Manager | 500 | TBD | ~2,200 | ⏳ Pending |
| Phase 5: Canvas Renderer | 400 | TBD | ~1,800 | ⏳ Pending |
| Phase 2: Color View Manager | 600 | TBD | ~1,200 | ⏳ Pending |
| Phase 6: UI Builder Completion | 300 | TBD | ~900 | ⏳ Pending |

**Target**: ~850-900 lines (73-74% reduction from 3,387)  
**Current**: 3,029 lines (10.6% reduction)  
**Remaining**: ~2,100 lines to extract (5 phases)

### Efficiency Notes
- Estimates are slightly optimistic (~10-15% overhead for documentation/structure)
- Phase 3 achieved 89% of estimate (358 vs 400 expected)
- Expect final size: 850-1,000 lines (realistic with overhead)

## Implementation Order

1. **Selection Manager** (Phase 1) - Self-contained, minimal dependencies
2. **File Operations** (Phase 3) - Self-contained, clear boundaries
3. **Dialog Manager** (Phase 4) - Depends on file operations
4. **Color View Manager** (Phase 2) - Complex, many widget references
5. **Canvas Renderer** (Phase 5) - Core rendering logic
6. **UI Builder** (Phase 6) - Final cleanup

## Architecture After Refactor

```
src/ui/
├── main_window.py (850 lines) - Core orchestration only
├── ui_builder.py - All UI creation
├── selection_manager.py - Selection operations (NEW)
├── color_view_manager.py - Color view management (NEW)
├── file_operations_manager.py - File I/O (NEW)
├── dialog_manager.py - Custom dialogs (NEW)
├── theme_manager.py - Theme system
├── theme_dialog_manager.py - Theme dialogs
├── layer_panel.py - Layer UI
├── timeline_panel.py - Animation UI
├── color_wheel.py - Color wheel widget
└── tooltip.py - Tooltip system

src/core/
├── canvas_renderer.py - All canvas rendering (EXPANDED)
├── canvas.py - Canvas data
├── event_dispatcher.py - Event routing
├── layer_manager.py - Layer system
└── ...
```

## Benefits

1. **Token Efficiency**: Each module can be loaded independently
2. **Maintainability**: Clear separation of concerns
3. **Testability**: Each manager can be tested independently
4. **Readability**: Each file has single responsibility
5. **Collaboration**: Multiple AI agents can work on different files
6. **Debugging**: Easier to locate issues

## Testing Strategy

### Critical Testing Checklist
After each phase, test these areas systematically:

#### Core Functionality
1. **Application Startup**: No errors, all UI elements visible
2. **Tool Selection**: All tools selectable and highlighted properly
3. **Tool Operations**: Brush, eraser, fill, eyedropper work correctly
4. **Tool Sizes**: Multi-size tools (2x2, 3x3) work consistently

#### Tool Consistency (CRITICAL)
5. **Brush Size Switching**: Switch between 1x1, 2x2, 3x3 - previous work stays visible
6. **Eraser Size Switching**: Switch between sizes - canvas doesn't corrupt
7. **Tool Switching**: Switch between different tools - no pixel loss
8. **Layer Integration**: All tools properly update layers AND canvas display

#### UI Components
9. **Palette Views**: Grid, Wheel, Primary, Constants, Saved all functional
10. **Color Selection**: Clicking colors updates primary/secondary properly
11. **Panel Toggles**: Left/right panels collapse and restore correctly
12. **File Menu**: All file operations accessible and functional

#### File Operations
13. **New Project**: Clears canvas, resets layers and timeline
14. **Open Project**: Loads .pixpf files correctly
15. **Save/Save As**: Persists project data
16. **Import PNG**: Loads PNG into canvas with proper dimensions
17. **Export**: PNG, GIF, Spritesheet exports work

#### Documentation
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

## Lessons Learned from Real Refactoring

### ✅ What Worked Well

#### 1. **Callback Pattern for Managers**
```python
# In manager __init__:
self.force_canvas_update_callback = None
self.update_canvas_from_layers_callback = None

# In main_window after manager creation:
self.file_ops.force_canvas_update_callback = self._force_tkinter_canvas_update
self.file_ops.update_canvas_from_layers_callback = self._update_canvas_from_layers
```
**Why**: Keeps managers decoupled while allowing necessary canvas updates

#### 2. **PowerShell for Bulk Deletions**
```powershell
(Get-Content 'file.py')[0..2312] + (Get-Content 'file.py')[2661..9999] | Set-Content 'file.py'
```
**Why**: When deleting 300+ lines, this is faster and cleaner than multiple search_replace calls

#### 3. **One Phase at a Time**
- Complete ONE extraction phase
- Test thoroughly
- Update documentation
- Let user test before proceeding
**Why**: Prevents cascading errors and makes debugging easier

#### 4. **Manager Initialization Timing**
- Initialize managers AFTER UI panels are created
- Some managers need references to UI components
- Set callbacks immediately after initialization
**Why**: Prevents AttributeError from missing references

### ⚠️ Critical Warnings

#### 1. **Tool Consistency is FRAGILE**
**Problem**: Mixing canvas-based (1x1) and layer-based (2x2/3x3) drawing causes pixel loss

**Solution**: 
- ALL tool sizes must use same approach (layer-based)
- ALL operations must call `_update_canvas_from_layers()`
- Create helper methods like `_draw_brush_at()` and `_draw_eraser_at()`

**Test**: Switch between tool sizes multiple times - previous work must stay visible

#### 2. **Event Dispatcher Interactions**
**Problem**: EventDispatcher delegates to main_window methods, creating tight coupling

**Be Careful With**:
- Methods that EventDispatcher calls must still exist in main_window
- Multi-pixel tools need special handling in EventDispatcher
- Eyedropper tool needs access to color wheel updates

**Solution**: Keep event-related methods in main_window or update EventDispatcher appropriately

#### 3. **File Reversion Disasters**
**Problem**: Git reverts or bad merges can destroy working code

**Prevention**:
- Commit working code before major changes
- Test after EVERY file operation
- Keep backups of critical files
- Don't commit until user confirms working

#### 4. **UI Widget References**
**Problem**: Extracting UI creation can break widget references elsewhere

**Watch For**:
- `self.tool_buttons` - needed by multiple systems
- `self.drawing_canvas` - needed for cursor changes
- Palette view frames - needed for view switching
- Radio button variables - needed for callbacks

**Solution**: Initialize empty containers BEFORE UIBuilder, populate them during build

### 🔧 Technical Patterns That Work

#### Manager Class Template
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

#### Integration in main_window.py
```python
# After UI creation and panel initialization
self.some_manager = SomeManager(self.root, self.canvas, ...)
self.some_manager.some_callback = self._some_internal_method

# Update menu/buttons to use manager
# Old: command=self._some_method
# New: command=self.some_manager.some_method
```

### 📊 Realistic Expectations

#### Line Count Estimates
Original estimates were optimistic. Real reductions:
- **Phase 3 (File Ops)**: Estimated 400, Actual 358 (89% of estimate)
- **Factor in overhead**: Documentation, imports, class structure add ~10-15%

#### Time Estimates
- Simple extraction: 10-20 minutes
- Complex extraction with dependencies: 30-60 minutes
- Bug fixes after extraction: 15-45 minutes
- **Total per phase**: 1-2 hours including testing

#### Complexity Factors
**Easy extractions**:
- Self-contained methods
- Clear input/output
- No UI widget dependencies
- File operations, templates

**Hard extractions**:
- Methods with UI widget references
- Methods called by EventDispatcher
- Tool operations with canvas/layer sync
- Color management, selection tools

### 🎯 Recommended Order (Updated)

Based on actual experience:

1. ✅ **File Operations** (COMPLETE) - Self-contained, clean boundaries
2. **Dialog Manager** (NEXT) - Self-contained, no tool dependencies
3. **Selection Manager** - Moderate complexity, clear boundaries
4. **Canvas Renderer Expansion** - Technical but well-defined
5. **Color View Manager** - Complex UI references, do LAST
6. **UI Builder Completion** - Final cleanup

**Rationale**: Start with easy wins, build confidence, tackle complex ones last

## Next Steps

### Immediate (Phase 4: Dialog Manager)
1. Extract `_open_custom_size_dialog()` (~131 lines)
2. Extract `_show_downsize_warning()` (~108 lines)
3. Extract `_open_texture_panel()` and related (~127 lines)
4. Keep `_show_file_menu()` in main_window (needs file_ops reference)
5. Test all dialogs thoroughly
6. Update documentation

### Future Phases
1. Selection Manager (Phase 1) - ~500 lines
2. Canvas Renderer (Phase 5) - ~400 lines  
3. Color View Manager (Phase 2) - ~600 lines (most complex)
4. UI Builder cleanup (Phase 6) - ~300 lines

