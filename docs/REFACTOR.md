# Pixel Perfect - Refactoring Plan (UPDATED)

**Date**: October 14, 2025  
**Version**: 1.35  
**Status**: Ready for Implementation
**Current main_window.py size**: **4,331 lines** ⚠️ CRITICAL

---

## Executive Summary

**Critical Issue**: `main_window.py` has grown to **4,331 lines** - a monolithic file that's becoming increasingly difficult to navigate, search, and maintain. This directly violates the project's #1 rule: **"Split up components to as many parts as possible, in order to reduce token consumption."**

**Impact**:
- 🐌 Slow semantic search and code navigation
- 💰 High token costs for AI assistance  
- 🔍 Difficult to find specific functionality
- 🐛 Harder to debug and test
- 👥 Difficult for onboarding

**Goal**: Extract **8-10 focused modules** (~300-800 lines each) from main_window.py, reducing it to **~400 lines** of orchestration code only.

**Expected Benefits**:
- ⚡ 90% faster search and navigation
- 💰 90% reduction in token costs
- ✅ Easier to find, modify, and test code
- 🎯 Clear separation of concerns
- 📦 Better code organization

---

## Current Architecture Analysis

### File Size: 4,331 Lines Breakdown

Based on analysis of `src/ui/main_window.py`:

```
main_window.py:        4,331 lines  ⚠️⚠️ CRITICALLY LARGE
  - Initialization:      ~200 lines   (core systems setup, icon loading)
  - UI Creation:       ~1,100 lines   ← PRIORITY 1 for extraction
    • Toolbar:           ~150 lines
    • Tool panel:        ~180 lines
    • Palette panel:     ~800 lines (includes all views)
    • Canvas panel:       ~70 lines
  - Palette Views:       ~850 lines   ← PRIORITY 2 for extraction
    • Grid view:          ~80 lines
    • Primary colors:    ~300 lines
    • Color wheel:       ~150 lines
    • Constants view:    ~100 lines
    • Saved colors:      ~220 lines
  - Theme System:        ~250 lines   ← PRIORITY 3 for extraction
    • Apply theme:       ~170 lines
    • Recursive update:   ~80 lines
  - Selection Ops:       ~500 lines   ← PRIORITY 4 for extraction
    • Mirror/Rotate:     ~120 lines
    • Copy/Paste:        ~100 lines
    • Scaling:           ~280 lines
  - File Operations:     ~300 lines   ← PRIORITY 5 for extraction
    • Save/Load:         ~150 lines
    • Import PNG:        ~120 lines
    • Export (PNG/GIF):   ~80 lines
  - Event Handlers:      ~750 lines   ← PRIORITY 6 for extraction
    • Mouse events:      ~550 lines
    • Keyboard:          ~150 lines
    • Bind events:        ~50 lines
  - Canvas Rendering:    ~380 lines   ← PRIORITY 7 for extraction
    • Update display:    ~280 lines
    • Grid rendering:    ~100 lines
```

**Critical Observation**: At 4,331 lines, this is 25% LARGER than when last analyzed. The problem is accelerating.

---

## Proposed Refactoring Strategy

### Phase-by-Phase Extraction Plan

Extract modules in order of **maximum impact** on searchability and maintainability. Each phase is independent and provides immediate benefits.

---

### ✅ **PRIORITY 1: UI Builder Module** (~1,100 lines extraction)

**Target**: `src/ui/ui_builder.py`

**Why First**: Removes 25% of file size, isolates all UI construction, provides immediate search relief.

**Methods to Extract**:
- `_create_ui()` - Main UI orchestration (~20 lines)
- `_create_toolbar()` - Top toolbar with all controls (~150 lines)
- `_create_undo_redo_buttons()` - Undo/redo button creation (~50 lines)
- `_create_tool_panel()` - Tool selection grid (~180 lines)
- `_create_palette_panel()` - Palette panel structure (~150 lines)
- `_create_canvas_panel()` - Canvas display area (~70 lines)
- Panel collapse/restore UI (~100 lines)
- Collapsible panel logic (~150 lines)
- Panel event handlers (~50 lines)

**New Module Structure**:
```python
# src/ui/ui_builder.py

class UIBuilder:
    """Builds all UI components for the main window"""
    
    def __init__(self, parent, callbacks, theme_manager):
        self.parent = parent
        self.callbacks = callbacks
        self.theme_manager = theme_manager
        self.widgets = {}  # Store references
    
    def create_toolbar(self) -> dict:
        """Create top toolbar"""
        # Returns dict of toolbar widgets
        
    def create_tool_panel(self) -> ctk.CTkFrame:
        """Create tool selection panel"""
        
    def create_palette_panel(self) -> ctk.CTkFrame:
        """Create palette panel structure"""
        
    def create_canvas_area(self) -> tuple:
        """Create center canvas display"""
        # Returns (canvas_frame, drawing_canvas, canvas_label)
    
    def create_collapsible_panels(self):
        """Setup collapsible left/right panels"""
```

**Integration with MainWindow**:
```python
# In MainWindow.__init__()
self.ui_builder = UIBuilder(self.main_frame, self._get_ui_callbacks(), self.theme_manager)
toolbar_widgets = self.ui_builder.create_toolbar()
self.tool_frame = self.ui_builder.create_tool_panel()
# etc.
```

**Estimated Time**: 6-8 hours  
**Benefit**: main_window.py reduced to 3,231 lines (25% reduction)

---

### ✅ **PRIORITY 2: Palette Manager Module** (~850 lines extraction)

**Target**: `src/ui/palette_manager.py`

**Why Second**: Removes 20% more, centralizes all palette view logic, huge search improvement.

**Methods to Extract**:
- `_create_color_grid()` - Standard grid view (~80 lines)
- `_create_primary_colors()` - Primary colors orchestration (~50 lines)
- `_create_primary_colors_grid()` - Primary grid implementation (~160 lines)
- `_create_color_variations_grid()` - Variation display (~90 lines)
- `_create_color_wheel()` - HSV wheel integration (~150 lines)
- `_create_constants_grid()` - Active colors view (~100 lines)
- `_create_saved_colors_view()` - Saved slots view (~220 lines)
- Color hover effects (~80 lines)
- View mode switching (~40 lines)
- Color selection handlers (~80 lines)

**New Module Structure**:
```python
# src/ui/palette_manager.py

class PaletteManager:
    """Manages all palette view modes and color selection"""
    
    def __init__(self, display_frame, palette, canvas, theme_manager):
        self.display_frame = display_frame
        self.palette = palette
        self.canvas = canvas
        self.theme_manager = theme_manager
        self.current_view = "grid"
        self.color_buttons = []
        self.color_wheel = None
    
    def create_grid_view(self):
        """Create standard palette grid"""
        
    def create_primary_colors_view(self):
        """Create primary + variations view"""
        
    def create_color_wheel_view(self):
        """Create HSV color wheel"""
        
    def create_constants_view(self):
        """Create active colors grid"""
        
    def create_saved_colors_view(self):
        """Create saved color slots"""
    
    def switch_view(self, view_mode: str):
        """Switch between view modes"""
        
    def on_color_select(self, color_index: int):
        """Handle color selection"""
```

**Estimated Time**: 5-7 hours  
**Benefit**: main_window.py reduced to 2,381 lines (20% more reduction, 45% total)

---

### ✅ **PRIORITY 3: Theme Applicator Module** (~250 lines extraction)

**Target**: `src/ui/theme_applicator.py`

**Why Third**: Removes complex theme logic, already partially separated with ThemeManager.

**Methods to Extract**:
- `_apply_theme()` - Main theme application (~170 lines)
- `_apply_theme_to_children()` - Recursive widget theming (~80 lines)
- `_update_theme_canvas_elements()` - Canvas theme updates (~50 lines currently in main)

**New Module Structure**:
```python
# src/ui/theme_applicator.py

class ThemeApplicator:
    """Applies themes to all UI elements"""
    
    def __init__(self, theme_manager):
        self.theme_manager = theme_manager
        self.widget_refs = {}  # Store widget references
    
    def register_widgets(self, **widget_groups):
        """Register widgets for theme application"""
        
    def apply_theme(self, theme):
        """Apply theme to all registered widgets"""
        
    def apply_to_children(self, parent_widget, theme):
        """Recursively apply theme to children"""
```

**Estimated Time**: 4-5 hours  
**Benefit**: main_window.py reduced to 2,131 lines (6% more reduction, 51% total)

---

### ✅ **PRIORITY 4: Selection Operations Module** (~500 lines extraction)

**Target**: `src/operations/selection_operations.py`

**Why Fourth**: Complex but isolated functionality, easy to extract.

**Methods to Extract**:
- `_on_selection_complete()` - Selection handler (~10 lines)
- `_mirror_selection()` - Mirror operation (~55 lines)
- `_rotate_selection()` - Rotate operation (~70 lines)
- `_copy_selection()` - Copy operation (~40 lines)
- `_scale_selection()` - Scale initiation (~50 lines)
- `_apply_scale()` - Scale application (~100 lines)
- `_get_scale_handle()` - Handle detection (~40 lines)
- `_draw_scale_handle()` - Handle rendering (~20 lines)
- `_simple_scale()` - Scaling algorithm (~45 lines)
- `_place_copy_at()` - Copy placement (~50 lines)
- Scaling state variables (~20 lines)

**New Module Structure**:
```python
# src/operations/selection_operations.py

class SelectionOperations:
    """Handles all selection manipulation operations"""
    
    def __init__(self, canvas, layer_manager, selection_tool):
        self.canvas = canvas
        self.layer_manager = layer_manager
        self.selection_tool = selection_tool
        # Scaling state
        self.scale_original_rect = None
        self.scale_handle_size = 12
    
    def mirror_selection(self):
        """Mirror selected pixels horizontally"""
        
    def rotate_selection(self):
        """Rotate selected pixels 90° clockwise"""
        
    def copy_selection(self):
        """Copy selected pixels to clipboard"""
        
    def scale_selection(self, mouse_x, mouse_y):
        """Initialize interactive scaling"""
        
    def apply_scale(self, new_rect):
        """Apply scaling to selection"""
```

**Estimated Time**: 5-6 hours  
**Benefit**: main_window.py reduced to 1,631 lines (12% more reduction, 62% total)

---

### ✅ **PRIORITY 5: File Handler Module** (~300 lines extraction)

**Target**: `src/io/file_handler.py`

**Why Fifth**: Clear functional boundary, easy to test independently.

**Methods to Extract**:
- `_show_file_menu()` - File menu display (~50 lines)
- `_new_project()` - New project creation (~60 lines)
- `_save_project()` - Save operation (~20 lines)
- `_save_project_as()` - Save as operation (~25 lines)
- `_load_project()` - Load operation (~50 lines)
- `_import_png()` - PNG import (~115 lines)
- `_export_png()` - PNG export (~30 lines)
- `_export_gif()` - GIF export (~30 lines)
- `_export_spritesheet()` - Spritesheet export (~20 lines)

**New Module Structure**:
```python
# src/io/file_handler.py

class FileHandler:
    """Handles all file I/O operations"""
    
    def __init__(self, project, canvas, layer_manager, timeline, root):
        self.project = project
        self.canvas = canvas
        self.layer_manager = layer_manager
        self.timeline = timeline
        self.root = root
    
    def show_file_menu(self):
        """Display file menu"""
        
    def new_project(self):
        """Create new project"""
        
    def save_project(self, save_as=False):
        """Save current project"""
        
    def load_project(self):
        """Load project from file"""
        
    def import_png(self):
        """Import PNG image"""
        
    def export_png(self):
        """Export to PNG"""
        
    def export_gif(self):
        """Export animation as GIF"""
```

**Estimated Time**: 4-5 hours  
**Benefit**: main_window.py reduced to 1,331 lines (7% more reduction, 69% total)

---

### ✅ **PRIORITY 6: Event Dispatcher Module** (~750 lines extraction)

**Target**: `src/events/event_dispatcher.py`

**Why Sixth**: Large but essential, routes all user interaction.

**Methods to Extract**:
- `_bind_events()` - Event binding setup (~50 lines)
- `_on_focus_in()` - Window focus handler (~10 lines)
- `_on_key_press()` - Keyboard handler (~180 lines)
- `_on_tkinter_canvas_mouse_down()` - Mouse down handler (~120 lines)
- `_on_tkinter_canvas_mouse_up()` - Mouse up handler (~100 lines)
- `_on_tkinter_canvas_mouse_drag()` - Mouse drag handler (~100 lines)
- `_on_tkinter_canvas_mouse_move()` - Mouse move handler (~100 lines)
- `_on_tkinter_canvas_right_click()` - Right click handler (~40 lines)
- Supporting mouse state (~50 lines)

**New Module Structure**:
```python
# src/events/event_dispatcher.py

class EventDispatcher:
    """Routes all mouse/keyboard events to appropriate handlers"""
    
    def __init__(self, main_window):
        self.window = main_window
        self.is_drawing = False
        self.last_mouse_pos = None
        self.is_panning = False
    
    def bind_all_events(self, root, canvas):
        """Bind all keyboard and mouse events"""
        
    def on_mouse_down(self, event):
        """Handle mouse down events"""
        
    def on_mouse_move(self, event):
        """Handle mouse move events"""
        
    def on_mouse_up(self, event):
        """Handle mouse up events"""
        
    def on_key_press(self, event):
        """Handle keyboard events"""
```

**Estimated Time**: 6-7 hours  
**Benefit**: main_window.py reduced to 581 lines (17% more reduction, 87% total)

---

### ✅ **PRIORITY 7: Canvas Renderer Module** (~380 lines extraction)

**Target**: `src/rendering/canvas_renderer.py`

**Why Seventh**: Final major extraction, isolates rendering logic.

**Methods to Extract**:
- `_update_pixel_display()` - Main rendering (~280 lines)
- `_update_single_pixel()` - Single pixel update (~50 lines)
- `_draw_grid()` - Grid overlay rendering (~50 lines)
- Grid state management (~20 lines)

**New Module Structure**:
```python
# src/rendering/canvas_renderer.py

class CanvasRenderer:
    """Handles all canvas rendering operations"""
    
    def __init__(self, tk_canvas, pixel_canvas, zoom):
        self.tk_canvas = tk_canvas
        self.pixel_canvas = pixel_canvas
        self.zoom = zoom
        self.grid_lines = []
        self.grid_visible = False
    
    def update_full_display(self):
        """Render all pixels to canvas"""
        
    def update_single_pixel(self, x, y):
        """Update one pixel"""
        
    def draw_grid(self, show_grid, overlay_mode):
        """Render grid overlay"""
        
    def clear_display(self):
        """Clear canvas"""
```

**Estimated Time**: 5-6 hours  
**Benefit**: main_window.py reduced to **~400 lines** (9% more reduction, **91% total**)

---

## Final Architecture

### New Module Structure

```
src/
  ui/
    __init__.py
    main_window.py          (~400 lines - orchestration only) ✅
    ui_builder.py           (NEW - ~1,100 lines) 🆕
    palette_manager.py      (NEW - ~850 lines) 🆕
    theme_applicator.py     (NEW - ~250 lines) 🆕
    layer_panel.py          (exists - 500 lines)
    timeline_panel.py       (exists - 400 lines)
    theme_manager.py        (exists - 200 lines)
    tooltip.py              (exists - 100 lines)
    color_wheel.py          (exists - 300 lines)
  
  operations/
    __init__.py
    selection_operations.py (NEW - ~500 lines) 🆕
  
  io/
    __init__.py
    file_handler.py         (NEW - ~300 lines) 🆕
  
  events/
    __init__.py
    event_dispatcher.py     (NEW - ~750 lines) 🆕
  
  rendering/
    __init__.py
    canvas_renderer.py      (NEW - ~380 lines) 🆕
  
  core/
    canvas.py               (exists)
    color_palette.py        (exists)
    custom_colors.py        (exists)
    layer_manager.py        (exists)
    project.py              (exists)
    undo_manager.py         (exists)
    saved_colors.py         (exists)
  
  tools/
    [existing tool files]   (exists)
```

---

## Extraction Summary

| Phase | Module | Lines Extracted | Time | Cumulative Reduction |
|-------|--------|----------------|------|----------------------|
| 1 | UI Builder | 1,100 | 6-8h | 25% |
| 2 | Palette Manager | 850 | 5-7h | 45% |
| 3 | Theme Applicator | 250 | 4-5h | 51% |
| 4 | Selection Operations | 500 | 5-6h | 62% |
| 5 | File Handler | 300 | 4-5h | 69% |
| 6 | Event Dispatcher | 750 | 6-7h | 87% |
| 7 | Canvas Renderer | 380 | 5-6h | **91%** |
| **TOTAL** | **7 modules** | **4,130 lines** | **35-44h** | **91% reduction** |

**Final Result**: main_window.py from **4,331 lines → ~400 lines**

---

## Benefits of This Refactor

### Immediate Benefits
- ⚡ **90% faster search** - Find code in 400 lines vs 4,331
- 💰 **90% lower token costs** - AI tools analyze 10x less code
- 🔍 **Instant navigation** - Know exactly where to find things
- 📦 **Better organization** - Each module has clear purpose

### Development Benefits
- ✅ **Easier to modify** - Change one area without affecting others
- 🧪 **Better testing** - Test modules independently
- 🐛 **Easier debugging** - Smaller scope to investigate
- 👥 **Better onboarding** - Understand one module at a time

### Long-term Benefits
- 🚀 **Faster features** - Add to focused modules, not monolith
- 🔧 **Easier maintenance** - Clear boundaries and responsibilities
- 📚 **Better documentation** - Document each module separately
- 🎯 **Professional codebase** - Industry-standard architecture

---

## Risk Mitigation

### Potential Risks

1. **Breaking functionality** during extraction
   - ✅ Mitigate: Test thoroughly after each phase
   - ✅ Use git branches for each phase
   - ✅ Keep backups before starting

2. **Complex state dependencies**
   - ✅ Mitigate: Pass references explicitly via constructors
   - ✅ Document all dependencies
   - ✅ Use callback patterns for communication

3. **Time investment** (35-44 hours total)
   - ✅ Mitigate: Can stop after any phase
   - ✅ Each phase provides immediate value
   - ✅ Spread across multiple weeks if needed

4. **Circular dependencies**
   - ✅ Mitigate: MainWindow remains orchestrator
   - ✅ Modules never import MainWindow
   - ✅ Use callbacks instead of direct calls

---

## Implementation Roadmap

### Phase-by-Phase Schedule

#### Option 1: Aggressive (1-2 Weeks)
- **Week 1**: Phases 1-3 (UI components)
  - Days 1-2: UI Builder
  - Days 3-4: Palette Manager
  - Day 5: Theme Applicator
- **Week 2**: Phases 4-7 (Operations + Events)
  - Day 1: Selection Operations
  - Day 2: File Handler
  - Days 3-4: Event Dispatcher
  - Day 5: Canvas Renderer

#### Option 2: Balanced (3-4 Weeks)
- **Week 1**: Phase 1 (UI Builder)
- **Week 2**: Phases 2-3 (Palette + Theme)
- **Week 3**: Phases 4-5 (Selection + Files)
- **Week 4**: Phases 6-7 (Events + Rendering)

#### Option 3: Cautious (7 Weeks)
- One phase per week
- Extensive testing between phases
- Lower risk, slower progress

**Recommended**: Option 2 (Balanced) - Good pace with safety buffer

---

## Success Criteria

### Per-Phase Checklist
After EACH phase, verify:
- [ ] All features work identically
- [ ] No new bugs introduced
- [ ] Application launches cleanly
- [ ] Visual appearance unchanged
- [ ] Module has clear docstrings
- [ ] Git commit with description
- [ ] REFACTOR.md progress updated

### Final Success Criteria
After ALL phases:
- [ ] main_window.py is ~400 lines (91% reduction)
- [ ] 7 new focused modules created
- [ ] All features work identically
- [ ] Search 90% faster
- [ ] No performance regression
- [ ] Documentation updated

---

## Getting Started

### Prerequisites
1. **Backup current state**
   ```bash
   git branch backup-before-refactor
   git tag before-refactor-v1.35
   ```

2. **Create feature branch**
   ```bash
   git checkout -b refactor/phase-1-ui-builder
   ```

3. **Verify all tests pass** (if you have tests)

### Start with Phase 1
1. Read Phase 1 section above
2. Create `src/ui/ui_builder.py`
3. Extract toolbar creation first (smallest, easiest)
4. Test immediately
5. Continue with tool panel, then palette panel
6. Test after each extraction
7. Commit when phase complete

**Estimated Time for Phase 1**: 6-8 hours

---

## Progress Tracking

| Phase | Module | Status | Completed | Notes |
|-------|--------|--------|-----------|-------|
| 1 | UI Builder | ⏸️ Not Started | - | ~1,100 lines |
| 2 | Palette Manager | ⏸️ Not Started | - | ~850 lines |
| 3 | Theme Applicator | ⏸️ Not Started | - | ~250 lines |
| 4 | Selection Operations | ⏸️ Not Started | - | ~500 lines |
| 5 | File Handler | ⏸️ Not Started | - | ~300 lines |
| 6 | Event Dispatcher | ⏸️ Not Started | - | ~750 lines |
| 7 | Canvas Renderer | ⏸️ Not Started | - | ~380 lines |

**Legend**: 
- ⏸️ Not Started
- 🔄 In Progress
- ✅ Complete
- ❌ Failed/Reverted

---

## Next Steps

1. **Review this plan** - Make sure you agree with the approach
2. **Choose schedule** - Aggressive, Balanced, or Cautious?
3. **Create backup** - Branch + tag for safety
4. **Start Phase 1** - Extract UI Builder
5. **Test thoroughly** - After each extraction
6. **Commit + continue** - One phase at a time

**Remember**: You can stop after ANY phase. Each extraction provides immediate value!

---

**Document Version**: 2.0  
**Last Updated**: October 14, 2025  
**Status**: Ready for Implementation  
**Next Action**: Start Phase 1 (UI Builder)

---

## Appendix: Quick Reference

### File Locations
- **Main Window**: `src/ui/main_window.py` (4,331 lines)
- **Architecture**: `docs/ARCHITECTURE.md`
- **Summary**: `docs/SUMMARY.md`
- **Changelog**: `docs/CHANGELOG.md`

### Key Project Rules (from user rules)
1. **#1 RULE**: Split components into as many parts as possible
2. Reduce token consumption
3. Document regularly
4. Keep it simple for future understanding
5. Split game components into many class files

### Successful Past Extractions
- ✅ LayerPanel: 500+ lines
- ✅ TimelinePanel: 400+ lines
- ✅ ColorWheel: 300+ lines
- ✅ ThemeManager: 200+ lines
- ✅ Various tools: 100-200 lines each

**Pattern**: All extractions succeeded without breaking functionality. This refactor follows the same proven pattern.
