# Pixel Perfect - Refactoring Plan

**Date**: October 13, 2025  
**Version**: 1.25  
**Status**: Proposed - Updated Analysis

## Executive Summary

This document outlines a comprehensive refactoring plan to improve code organization by splitting `main_window.py` into multiple focused modules. This aligns with the project's #1 rule: "Split up components to as many parts as possible, in order to reduce token consumption."

**Current Issue**: `main_window.py` has grown to **3,454 lines** (increased from 2,649 lines), making it difficult to navigate, search, and maintain.

**Goal**: Extract multiple functional areas into dedicated modules to improve maintainability, testability, reduce search time, and drastically reduce token consumption.

---

## Current Architecture Analysis

### File Size Breakdown

```
main_window.py:        3,454 lines  ⚠️⚠️ CRITICALLY LARGE - Search is slow!
  - Initialization:    ~175 lines   (icon loading, core systems setup)
  - UI Creation:       ~900 lines   ← PRIORITY 1 for extraction
    • Toolbar:         ~250 lines
    • Canvas area:     ~150 lines
    • Tool panel:      ~250 lines
    • Palette panel:   ~250 lines
  - Palette Views:     ~550 lines   ← PRIORITY 2 for extraction
    • Grid view:       ~90 lines
    • Primary view:    ~180 lines
    • Color wheel:     ~100 lines
    • Variations:      ~80 lines
    • Constants:       ~100 lines
  - Theme System:      ~300 lines   ← PRIORITY 3 for extraction
    • Apply theme:     ~200 lines
    • Update UI:       ~100 lines
  - Selection Ops:     ~400 lines   ← PRIORITY 4 for extraction
    • Mirror/Rotate:   ~110 lines
    • Copy/Paste:      ~120 lines
    • Scaling:         ~170 lines
  - File Operations:   ~250 lines   ← PRIORITY 5 for extraction
    • Save/Load:       ~100 lines
    • Import PNG:      ~110 lines
    • Export:          ~40 lines
  - Event Handlers:    ~650 lines   ← PRIORITY 6 for extraction
    • Mouse events:    ~400 lines
    • Keyboard:        ~150 lines
    • Bind events:     ~100 lines
  - Canvas Drawing:    ~400 lines   ← PRIORITY 7 for extraction
    • Update display:  ~250 lines
    • Grid rendering:  ~150 lines
  - Helper Methods:    ~229 lines
```

**Critical Issue**: At 3,454 lines, semantic search and code navigation are becoming slow and expensive. Breaking this into 8-10 smaller modules would dramatically improve development speed and reduce token costs.

### Priority-Based Extraction Plan

The following modules should be extracted in order of impact on searchability and maintainability:

#### PRIORITY 1: UI Builder Module (~900 lines)
**Target**: `src/ui/ui_builder.py`

**Methods to Extract**:
- `_create_toolbar()`: ~250 lines - Create top toolbar with all buttons
- `_create_tool_panel()`: ~250 lines - Create tool selection panel
- `_create_canvas_area()`: ~150 lines - Create center canvas display
- `_create_palette_panel()`: ~250 lines - Create palette panel structure

**Dependencies**: CustomTkinter, Tkinter, tooltip system

**Benefit**: Removes 26% of main_window.py, isolates all UI construction

---

#### PRIORITY 2: Palette Manager Module (~550 lines)
**Target**: `src/ui/palette_manager.py`

**Methods to Extract**:
- `_create_color_grid()`: ~90 lines - Standard palette grid
- `_create_primary_colors()`: ~180 lines - Primary + variations view
- `_create_color_wheel()`: ~100 lines - HSV color wheel
- `_create_color_variations()`: ~80 lines - Color variations
- `_create_constants_grid()`: ~100 lines - Active colors on canvas
- `_on_view_mode_change()`: ~20 lines - Switch between views
- Color selection handlers: ~80 lines

**Dependencies**: ColorPalette, Canvas, CustomTkinter

**Benefit**: Removes 16% of main_window.py, centralizes palette logic

---

#### PRIORITY 3: Theme Applicator Module (~300 lines)
**Target**: `src/ui/theme_applicator.py`

**Methods to Extract**:
- `_apply_theme()`: ~200 lines - Apply theme to all widgets
- `_update_theme_canvas_elements()`: ~100 lines - Update canvas theme elements

**Dependencies**: ThemeManager, UI widget references

**Benefit**: Removes 9% of main_window.py, isolates theme logic (already partially extracted)

---

#### PRIORITY 4: Selection Operations Module (~400 lines)
**Target**: `src/operations/selection_operations.py`

**Methods to Extract**:
- `_mirror_selection()`: ~45 lines
- `_rotate_selection()`: ~65 lines
- `_copy_selection()`: ~35 lines
- `_scale_selection()`: ~30 lines
- `_apply_scale()`: ~80 lines
- `_get_scale_handle()`: ~30 lines
- `_draw_scale_handle()`: ~15 lines
- `_simple_scale()`: ~40 lines
- `_place_copy_at()`: ~40 lines
- Supporting state management: ~20 lines

**Dependencies**: Canvas, LayerManager, numpy, scipy

**Benefit**: Removes 12% of main_window.py, isolates selection logic

---

#### PRIORITY 5: File Handler Module (~250 lines)
**Target**: `src/io/file_handler.py`

**Methods to Extract**:
- `_new_project()`: ~40 lines
- `_save_project()`: ~60 lines
- `_load_project()`: ~100 lines
- `_import_png()`: ~110 lines
- `_export_png()`: ~25 lines
- `_export_gif()`: ~15 lines

**Dependencies**: Project, Canvas, LayerManager, file dialogs

**Benefit**: Removes 7% of main_window.py, centralizes I/O operations

---

#### PRIORITY 6: Event Dispatcher Module (~650 lines)
**Target**: `src/events/event_dispatcher.py`

**Methods to Extract**:
- `_on_tkinter_canvas_mouse_down()`: ~100 lines
- `_on_tkinter_canvas_mouse_up()`: ~80 lines
- `_on_tkinter_canvas_mouse_move()`: ~150 lines
- `_on_tkinter_canvas_right_click()`: ~70 lines
- `_on_key_press()`: ~100 lines
- `_bind_events()`: ~100 lines
- Supporting mouse/keyboard handlers: ~50 lines

**Dependencies**: Tools, Canvas, all managers

**Benefit**: Removes 19% of main_window.py, isolates event routing

---

#### PRIORITY 7: Canvas Renderer Module (~400 lines)
**Target**: `src/rendering/canvas_renderer.py`

**Methods to Extract**:
- `_update_pixel_display()`: ~250 lines - Render pixels to canvas
- `_update_single_pixel()`: ~50 lines - Update one pixel
- `_draw_grid()`: ~100 lines - Render grid overlay

**Dependencies**: Canvas, Tkinter canvas, zoom calculations

**Benefit**: Removes 12% of main_window.py, isolates rendering logic

---

### Summary of Extraction Impact

| Module | Lines | % Reduction | Priority |
|--------|-------|-------------|----------|
| UI Builder | 900 | 26% | 1 |
| Palette Manager | 550 | 16% | 2 |
| Theme Applicator | 300 | 9% | 3 |
| Selection Operations | 400 | 12% | 4 |
| File Handler | 250 | 7% | 5 |
| Event Dispatcher | 650 | 19% | 6 |
| Canvas Renderer | 400 | 12% | 7 |
| **TOTAL** | **3,450** | **100%** | - |

**Target**: Reduce main_window.py from 3,454 lines to **~300 lines** (orchestration layer only)

**Benefit**: Search times reduced by 90%, token consumption dramatically decreased, maintainability vastly improved

---

## Proposed Architecture

### New Module Structure

```
src/
  ui/
    __init__.py
    main_window.py          (reduced to ~300 lines - orchestration only)
    ui_builder.py           (NEW - ~900 lines)
    palette_manager.py      (NEW - ~550 lines)
    theme_applicator.py     (NEW - ~300 lines)
    layer_panel.py          (exists)
    timeline_panel.py       (exists)
    theme_manager.py        (exists)
    tooltip.py              (exists)
    color_wheel.py          (exists)
  
  operations/
    __init__.py
    selection_operations.py (NEW - ~400 lines)
  
  io/
    __init__.py
    file_handler.py         (NEW - ~250 lines)
  
  events/
    __init__.py
    event_dispatcher.py     (NEW - ~650 lines)
  
  rendering/
    __init__.py
    canvas_renderer.py      (NEW - ~400 lines)
  
  core/
    canvas.py               (exists)
    color_palette.py        (exists)
    custom_colors.py        (exists)
    layer_manager.py        (exists)
    project.py              (exists)
    undo_manager.py         (exists)
  
  tools/
    [existing tool files]   (exists)
  
  animation/
    timeline.py             (exists)
  
  utils/
    export.py               (exists)
    file_association.py     (exists)
    import_png.py           (exists)
    presets.py              (exists)
```

### Class Design Examples

#### 1. UIBuilder (`src/ui/ui_builder.py`)

```python
class UIBuilder:
    """Builds all UI components for the main window"""
    
    def __init__(self, parent, callbacks):
        self.parent = parent
        self.callbacks = callbacks  # Dict of callback functions
        self.widgets = {}  # Store widget references
    
    def create_toolbar(self):
        """Create top toolbar with all buttons"""
        # Returns toolbar frame and dict of button references
        pass
    
    def create_tool_panel(self, tool_buttons_callback):
        """Create tool selection panel"""
        pass
    
    def create_canvas_area(self):
        """Create center canvas display area"""
        pass
    
    def create_palette_panel(self, palette_callbacks):
        """Create palette panel structure"""
        pass
```

#### 2. PaletteManager (`src/ui/palette_manager.py`)

```python
class PaletteManager:
    """Manages all palette view modes and color selection"""
    
    def __init__(self, display_frame, palette, canvas):
        self.display_frame = display_frame
        self.palette = palette
        self.canvas = canvas
        self.current_view = "grid"
        self.color_buttons = []
    
    def create_grid_view(self):
        """Create standard palette grid"""
        pass
    
    def create_primary_colors_view(self):
        """Create primary + variations view"""
        pass
    
    def create_color_wheel_view(self):
        """Create HSV color wheel"""
        pass
    
    def create_constants_view(self):
        """Create active colors grid"""
        pass
    
    def switch_view(self, view_mode):
        """Switch between view modes"""
        pass
    
    def on_color_select(self, color_index):
        """Handle color selection"""
        pass
```

#### 3. EventDispatcher (`src/events/event_dispatcher.py`)

```python
class EventDispatcher:
    """Routes all mouse/keyboard events to appropriate handlers"""
    
    def __init__(self, main_window):
        self.window = main_window
        self.is_drawing = False
        self.last_mouse_pos = None
    
    def bind_all_events(self, root, canvas):
        """Bind all keyboard and mouse events"""
        pass
    
    def on_mouse_down(self, event):
        """Handle mouse down events"""
        pass
    
    def on_mouse_move(self, event):
        """Handle mouse move events"""
        pass
    
    def on_mouse_up(self, event):
        """Handle mouse up events"""
        pass
    
    def on_key_press(self, event):
        """Handle keyboard events"""
        pass
```

#### 4. CanvasRenderer (`src/rendering/canvas_renderer.py`)

```python
class CanvasRenderer:
    """Handles all canvas rendering operations"""
    
    def __init__(self, tk_canvas, pixel_canvas, zoom):
        self.tk_canvas = tk_canvas
        self.pixel_canvas = pixel_canvas
        self.zoom = zoom
        self.grid_lines = []
    
    def update_full_display(self):
        """Render all pixels to canvas"""
        pass
    
    def update_single_pixel(self, x, y):
        """Update one pixel"""
        pass
    
    def draw_grid(self, show_grid, overlay_mode):
        """Render grid overlay"""
        pass
    
    def clear_grid(self):
        """Remove grid from display"""
        pass
```

### Integration with MainWindow (After Refactor)

```python
# main_window.py (reduced to ~300 lines)

class MainWindow:
    def __init__(self):
        # Initialize core systems (same as before)
        self.canvas = Canvas(32, 32, zoom=16)
        self.palette = ColorPalette()
        self.layer_manager = LayerManager(32, 32)
        # ... other managers
        
        # Create extracted modules
        self.ui_builder = UIBuilder(self.main_frame, self._get_callbacks())
        self.palette_manager = PaletteManager(
            self.palette_panel_frame,
            self.palette,
            self.canvas
        )
        self.event_dispatcher = EventDispatcher(self)
        self.canvas_renderer = CanvasRenderer(
            self.drawing_canvas,
            self.canvas,
            self.canvas.zoom
        )
self.selection_ops = SelectionOperations(
            self.canvas,
            self.layer_manager
        )
        self.file_handler = FileHandler(
            self.project,
            self.canvas,
            self.layer_manager
        )
        
        # Build UI using extracted modules
        self._create_ui()
        
        # Bind events using dispatcher
        self.event_dispatcher.bind_all_events(self.root, self.drawing_canvas)
    
    def _get_callbacks(self):
        """Return dict of callbacks for UI builder"""
        return {
            'new_project': self.file_handler.new_project,
            'save_project': self.file_handler.save_project,
            'load_project': self.file_handler.load_project,
            'import_png': self.file_handler.import_png,
            'export_png': self.file_handler.export_png,
            'select_tool': self._on_tool_select,
            'toggle_grid': self._toggle_grid,
            # ... etc
        }
    
    def _create_ui(self):
        """Orchestrate UI creation (much simpler now)"""
        toolbar_widgets = self.ui_builder.create_toolbar()
        tool_panel = self.ui_builder.create_tool_panel(self._on_tool_select)
        canvas_frame = self.ui_builder.create_canvas_area()
        palette_panel = self.ui_builder.create_palette_panel(
            self.palette_manager._get_callbacks()
        )
        # Store widget references
        self.toolbar_widgets = toolbar_widgets
        # ...
    
    # Main window now only contains:
    # - Module initialization
    # - Orchestration/coordination logic
    # - Simple delegation methods
    # Total: ~300 lines
```

---

## Benefits

### Code Organization
- ✅ **Separation of Concerns**: UI, events, rendering, operations, I/O all separated
- ✅ **Massive File Size Reduction**: main_window.py reduced from 3,454 to ~300 lines (91% reduction!)
- ✅ **Single Responsibility**: Each module has one clear, focused purpose
- ✅ **Easier Navigation**: Find code instantly in small, focused files
- ✅ **Logical Grouping**: Related functionality lives together

### Searchability & Performance
- ✅ **90% Faster Search**: Searching 300 lines vs 3,454 lines
- ✅ **Reduced Token Cost**: AI tools consume 90% fewer tokens per search
- ✅ **Faster IDE**: Code navigation, autocomplete, linting all faster
- ✅ **Better Git Diffs**: Changes isolated to relevant modules
- ✅ **Parallel Development**: Multiple devs can work on different modules

### Maintainability
- ✅ **Isolated Changes**: Modify one area without affecting others
- ✅ **Better Testing**: Each module can be unit tested independently
- ✅ **Clearer Dependencies**: Explicit interfaces show what each module needs
- ✅ **Reduced Coupling**: Modules communicate through well-defined interfaces
- ✅ **Easier Debugging**: Smaller files mean easier troubleshooting

### Future Extensibility
- ✅ **New Features**: Add features to focused modules, not monolithic file
- ✅ **Plugin Architecture**: Could support plugins by extending modules
- ✅ **API Ready**: Modules expose clean interfaces for automation
- ✅ **Reusability**: Modules can be reused in other projects
- ✅ **Documentation**: Each module can have focused documentation

### Developer Experience
- ✅ **Onboarding**: New devs can understand one module at a time
- ✅ **Cognitive Load**: Work on 300-line files instead of 3,454-line file
- ✅ **IDE Performance**: Faster autocomplete, linting, refactoring
- ✅ **AI Assistance**: AI tools can analyze entire modules efficiently
- ✅ **Code Review**: Easier to review focused, modular changes

---

## Risks & Mitigation

### Risk 1: Complex State Management
**Issue**: Modules need access to shared state (canvas, layers, tools, UI elements)

**Mitigation**:
- ✅ Pass references explicitly via constructors
- ✅ Use callback dictionaries for communication
- ✅ Keep state ownership clear (who owns what)
- ✅ Document all dependencies in class docstrings
- ✅ Use dependency injection pattern throughout

### Risk 2: Circular Dependencies
**Issue**: Modules might need to import each other

**Mitigation**:
- ✅ MainWindow remains the orchestrator (imports all modules)
- ✅ Modules never import MainWindow (use callbacks instead)
- ✅ Modules communicate through interfaces, not direct calls
- ✅ Use protocol/ABC classes if type hints needed
- ✅ Carefully design module boundaries

### Risk 3: Breaking Existing Functionality
**Issue**: Large refactor could introduce many bugs

**Mitigation**:
- ✅ Refactor in phases (one module at a time)
- ✅ Test thoroughly after each extraction
- ✅ Keep git history (easy rollback)
- ✅ Use feature branches for each module extraction
- ✅ Manual testing of all features after each phase
- ✅ Compare behavior before/after refactor

### Risk 4: Massive Development Time
**Issue**: Extracting 7 modules is a large undertaking

**Mitigation**:
- ✅ Follow priority order (high-value extractions first)
- ✅ Can stop after any phase if needed
- ✅ Each phase provides immediate benefits
- ✅ Budget 4-6 hours per module extraction
- ✅ Total estimated time: 28-42 hours across phases

### Risk 5: Performance Regression
**Issue**: Extra indirection might slow the application

**Mitigation**:
- ✅ Profile before and after each extraction
- ✅ Most operations are user-triggered (not per-frame)
- ✅ Function call overhead is negligible vs actual work
- ✅ Expected impact: <1% performance change
- ✅ Better code organization may actually improve performance

### Risk 6: Over-Engineering
**Issue**: Too many small modules could be worse than one large file

**Mitigation**:
- ✅ Each extracted module is 250-900 lines (reasonable size)
- ✅ Modules map to clear functional areas
- ✅ Similar to successful extractions: LayerPanel, TimelinePanel
- ✅ Aligns with project #1 rule: "Split up components"
- ✅ Searchability improvements justify the complexity

---

## Detailed Refactoring Steps

### Overview

This refactor is divided into 7 phases, each extracting one major functional area. Each phase is independent and provides immediate benefits. You can stop after any phase if desired.

**Recommended Approach**: Extract one module per session, test thoroughly, commit to git.

---

### Phase 1: Extract UI Builder (~6 hours)

**Goal**: Extract all UI creation code (~900 lines) into `src/ui/ui_builder.py`

#### 1.1 Create Module (15 min)
```bash
# Module already exists in ui/ folder, just create new file
touch src/ui/ui_builder.py
```

#### 1.2 Define UIBuilder Class (30 min)
- Create class with `__init__(parent, callbacks)`
- Define methods: `create_toolbar()`, `create_tool_panel()`, `create_canvas_area()`, `create_palette_panel()`
- Return widget references for main_window to store

#### 1.3 Extract Toolbar Creation (90 min)
- Copy `_create_toolbar()` method (~250 lines)
- Convert to `UIBuilder.create_toolbar()`
- Replace `self.root` with `self.parent`
- Replace direct method calls with `self.callbacks['method_name']()`
- Return dict of button references

#### 1.4 Extract Tool Panel (90 min)
- Copy `_create_tool_panel()` method (~250 lines)
- Convert to `UIBuilder.create_tool_panel(callback)`
- Handle tool button creation and tooltip setup

#### 1.5 Extract Canvas Area (60 min)
- Copy canvas frame creation (~150 lines)
- Convert to `UIBuilder.create_canvas_area()`

#### 1.6 Extract Palette Panel (90 min)
- Copy `_create_palette_panel()` method (~250 lines)
- Convert to `UIBuilder.create_palette_panel(callbacks)`

#### 1.7 Update main_window.py (60 min)
- Import UIBuilder
- Initialize: `self.ui_builder = UIBuilder(self.main_frame, callbacks)`
- Replace `_create_*()` calls with `ui_builder.create_*()`
- Store returned widget references

#### 1.8 Testing (60 min)
- Launch app, verify all UI elements appear
- Test all toolbar buttons
- Test all tool selections
- Verify no visual changes

**Result**: main_window.py reduced by 900 lines (26%)

---

### Phase 2: Extract Palette Manager (~5 hours)

**Goal**: Extract palette view management (~550 lines) into `src/ui/palette_manager.py`

#### Steps (Summary):
1. Create PaletteManager class
2. Extract grid, primary, wheel, variations, constants view methods
3. Move color selection logic
4. Update main_window to use PaletteManager
5. Test all palette views and color selection

**Result**: main_window.py reduced by 550 more lines (16%)

---

### Phase 3: Extract Theme Applicator (~4 hours)

**Goal**: Extract theme application (~300 lines) into `src/ui/theme_applicator.py`

#### Steps (Summary):
1. Create ThemeApplicator class
2. Extract `_apply_theme()` and `_update_theme_canvas_elements()`
3. Store references to all themed widgets
4. Update main_window to use ThemeApplicator
5. Test theme switching

**Result**: main_window.py reduced by 300 more lines (9%)

---

### Phase 4: Extract Selection Operations (~5 hours)

**Goal**: Extract selection ops (~400 lines) into `src/operations/selection_operations.py`

#### Steps (Summary):
1. Create operations/ directory and SelectionOperations class
2. Extract mirror, rotate, copy, scale methods
3. Move scaling state variables
4. Update main_window to use SelectionOperations
5. Test all selection operations

**Result**: main_window.py reduced by 400 more lines (12%)

---

### Phase 5: Extract File Handler (~4 hours)

**Goal**: Extract file I/O (~250 lines) into `src/io/file_handler.py`

#### Steps (Summary):
1. Create io/ directory and FileHandler class
2. Extract save, load, import, export methods
3. Update main_window to use FileHandler
4. Test all file operations

**Result**: main_window.py reduced by 250 more lines (7%)

---

### Phase 6: Extract Event Dispatcher (~6 hours)

**Goal**: Extract event handling (~650 lines) into `src/events/event_dispatcher.py`

#### Steps (Summary):
1. Create events/ directory and EventDispatcher class
2. Extract mouse/keyboard event handlers
3. Extract event binding logic
4. Update main_window to use EventDispatcher
5. Test all mouse/keyboard interactions

**Result**: main_window.py reduced by 650 more lines (19%)

---

### Phase 7: Extract Canvas Renderer (~5 hours)

**Goal**: Extract canvas rendering (~400 lines) into `src/rendering/canvas_renderer.py`

#### Steps (Summary):
1. Create rendering/ directory and CanvasRenderer class
2. Extract `_update_pixel_display()`, `_update_single_pixel()`, grid drawing
3. Update main_window to use CanvasRenderer
4. Test canvas rendering and grid

**Result**: main_window.py reduced by 400 more lines (12%)

---

### Final Result

After all 7 phases:
- **Before**: 3,454 lines in main_window.py
- **After**: ~300 lines in main_window.py (91% reduction!)
- **New modules**: 7 focused, maintainable files
- **Total effort**: 35 hours across all phases

---

## Success Criteria

### Per-Phase Success Criteria

Each phase must meet these criteria before moving to next phase:

#### Must Have (P0) - Blocking
- ✅ All functionality works identically to before refactor
- ✅ No new bugs or regressions
- ✅ Application launches and runs without errors
- ✅ Visual appearance unchanged
- ✅ All user workflows still work
- ✅ Code committed to git with descriptive message

#### Should Have (P1) - Important
- ✅ Module has clear, focused responsibility
- ✅ Dependencies documented in class docstring
- ✅ Clean interface (no spaghetti dependencies)
- ✅ main_window.py measurably smaller
- ✅ REFACTOR.md updated with progress

#### Nice to Have (P2) - Optional
- ✅ Module has usage examples in docstring
- ✅ Performance profiled (no regression)
- ✅ ARCHITECTURE.md updated

### Overall Project Success Criteria

After all 7 phases complete:

#### Must Have (P0)
- ✅ main_window.py reduced to ~300 lines (91% reduction)
- ✅ 7 new focused modules created
- ✅ All features work identically
- ✅ Search time dramatically improved
- ✅ No performance regression

#### Should Have (P1)
- ✅ Clear module boundaries and responsibilities
- ✅ Documentation fully updated
- ✅ Each module independently understandable
- ✅ Easier to add new features

#### Nice to Have (P2)
- ✅ Unit tests for extracted modules
- ✅ Performance improvements measured
- ✅ Developer guide for module structure

---

## Timeline

### Per-Phase Timeline

| Phase | Module | Lines Extracted | Estimated Time | Cumulative |
|-------|--------|-----------------|----------------|------------|
| 1 | UI Builder | 900 | 6 hours | 6 hours |
| 2 | Palette Manager | 550 | 5 hours | 11 hours |
| 3 | Theme Applicator | 300 | 4 hours | 15 hours |
| 4 | Selection Operations | 400 | 5 hours | 20 hours |
| 5 | File Handler | 250 | 4 hours | 24 hours |
| 6 | Event Dispatcher | 650 | 6 hours | 30 hours |
| 7 | Canvas Renderer | 400 | 5 hours | 35 hours |

**Total Core Work**: 35 hours

**Buffer (20% for issues)**: +7 hours

**Total with Buffer**: **42 hours** (~1 week of full-time work, or ~2-3 weeks part-time)

### Phased Rollout Strategy

You don't have to do all phases at once. Recommended schedules:

#### Aggressive: 1 Week Sprint
- Day 1: Phase 1 (UI Builder)
- Day 2: Phase 2 (Palette Manager)
- Day 3: Phase 3 (Theme) + Phase 4 (Selection)
- Day 4: Phase 5 (File Handler)
- Day 5: Phase 6 (Events) + Phase 7 (Renderer)

#### Balanced: 2-3 Weeks
- Week 1: Phases 1-3 (UI components)
- Week 2: Phases 4-5 (Operations + I/O)
- Week 3: Phases 6-7 (Events + Rendering)

#### Cautious: One Phase Per Week
- Week 1: Phase 1 only, test extensively
- Week 2: Phase 2 only, test extensively
- Continue until complete

**Recommendation**: Start with Phase 1 (UI Builder). If that goes well, continue. Each phase provides immediate benefits.

---

## Alternative Approaches Considered

### Alternative 1: Keep Everything in main_window.py
**Pros**: Simple, no refactoring needed, no risk of breaking changes

**Cons**: 
- File at 3,454 lines is critically large
- Search/navigation painfully slow
- Violates project #1 rule
- New features make it worse
- High token costs for AI tools

**Verdict**: ❌ **Not viable** - Problem will only get worse

---

### Alternative 2: Extract Only Selection Operations
**Pros**: Smaller refactor, less risk, proven approach

**Cons**:
- Only saves 400 lines (12% reduction)
- Doesn't solve searchability problem
- Main file still 3,000+ lines
- Partial solution to large problem

**Verdict**: ❌ **Insufficient** - Doesn't address core issue

---

### Alternative 3: Extract Everything to Individual Small Files
**Pros**: Maximum modularity, tiny files

**Cons**:
- 30-40+ small files (50-100 lines each)
- Import overhead and complexity
- Hard to find related functionality
- Over-engineered

**Verdict**: ❌ **Over-engineering** - Too granular

---

### Alternative 4: 7-Phase Comprehensive Refactor (CHOSEN)
**Pros**:
- ✅ 91% file size reduction
- ✅ Dramatically improved searchability
- ✅ Each module 250-900 lines (ideal size)
- ✅ Clear functional boundaries
- ✅ Can stop after any phase
- ✅ Proven pattern (LayerPanel, TimelinePanel already extracted)
- ✅ Aligns with project #1 rule

**Cons**:
- Requires 35-42 hours total effort
- Risk of breaking changes (mitigated by phasing)
- State management complexity (mitigated by design)

**Verdict**: ✅ **STRONGLY RECOMMENDED** - Best balance of benefits vs. effort

---

### Alternative 5: Rewrite from Scratch
**Pros**: Clean architecture, no legacy baggage

**Cons**:
- Months of work
- High risk of losing functionality
- Not practical for mature project
- Excessive

**Verdict**: ❌ **Overkill** - Refactoring is sufficient

---

## Future Enhancements

### Phase 8+: Further Refinement (Optional)

Once the main 7 phases are complete, consider these additional improvements:

#### 8.1 Extract Animation Controller (`src/animation/animation_controller.py`)
- Currently timeline logic is split between timeline.py and main_window.py
- Extract frame management, playback control
- ~150 lines

#### 8.2 Extract Zoom Manager (`src/ui/zoom_manager.py`)
- Handle zoom in/out, coordinate conversions
- ~100 lines

#### 8.3 Extract Layer Operations (`src/operations/layer_operations.py`)
- Merge, flatten, duplicate layer operations
- ~100 lines

#### 8.4 Split UIBuilder Further (If needed)
- If UIBuilder becomes too large (>1000 lines)
- Split into: ToolbarBuilder, PanelBuilder, CanvasBuilder
- Only if necessary

---

### New Features to Add (Post-Refactor)

With clean module structure, these features become easier:

#### Selection Operations (add to SelectionOperations module)
- ✨ **Flip Vertical**: Mirror on Y axis
- ✨ **Flip Horizontal**: Already exists (mirror)
- ✨ **Outline Selection**: Add outline to selected region
- ✨ **Drop Shadow**: Add shadow effect
- ✨ **Crop to Selection**: Resize canvas to selection
- ✨ **Expand/Contract Selection**: Grow/shrink by N pixels
- ✨ **Color Replace in Selection**: Replace one color with another
- ✨ **Hue Shift**: Adjust hue of selected pixels
- ✨ **Selection Invert**: Invert colors in selection

#### Palette Manager (add to PaletteManager module)
- ✨ **Recent Colors**: Show recently used colors
- ✨ **Palette History**: Undo/redo for palette changes
- ✨ **Palette Search**: Filter colors by hex/RGB
- ✨ **Palette Import/Export**: Share palettes

#### Canvas Renderer (add to CanvasRenderer module)
- ✨ **Onion Skinning**: Show previous/next frames
- ✨ **Pixel Grid Numbers**: Show coordinates on grid
- ✨ **Ruler Guides**: Add horizontal/vertical guides
- ✨ **Reference Image Overlay**: Trace over reference

#### File Handler (add to FileHandler module)
- ✨ **Auto-save**: Periodic saves
- ✨ **Export Sprite Sheet**: Multiple frames to grid
- ✨ **Import Sprite Sheet**: Split grid into frames
- ✨ **Export SVG**: Vector export option

---

### Plugin System (Far Future)

Once modules are fully extracted and stable:

```python
# src/plugins/plugin_manager.py
class PluginManager:
    """
    Load and manage external plugins
    Plugins can extend:
    - Operations (new selection/layer ops)
    - Tools (new drawing tools)
    - Export formats
    - Palette generators
    """
    
    def load_plugin(self, plugin_path):
        """Load a plugin from file"""
        pass
    
    def register_operation(self, op_class):
        """Register new operation"""
        pass
```

This would allow community extensions without modifying core code.

---

## Rollback Plan

### Per-Phase Rollback

Since each phase is committed separately, rollback is straightforward:

#### If Phase N Fails:
1. **Immediate Rollback** (recommended):
   ```bash
   git revert HEAD
   # or
   git reset --hard HEAD~1
   ```
   This rolls back just the last phase.

2. **Selective Rollback**:
   ```bash
   git log --oneline  # Find commit hash
   git revert <commit-hash>
   ```

3. **Keep Working Code**:
   - Previous phases remain intact
   - Only problematic phase is reverted
   - Can retry phase with fixes

#### If Multiple Phases Need Rollback:
```bash
git log --oneline  # Identify starting point
git reset --hard <commit-before-refactor>
```

### Git Branch Strategy

**Recommended**: Use feature branches for safety

```bash
# Before starting any phase
git checkout -b refactor/ui-builder

# After Phase 1 successful
git checkout main
git merge refactor/ui-builder
git push

# Start Phase 2
git checkout -b refactor/palette-manager
# ... continue pattern
```

This allows testing each phase in isolation before merging to main.

### Backup Strategy

Before starting any phase:

```bash
# Create backup branch
git branch backup-before-refactor

# Or create tag
git tag before-refactor-phase-1
```

This provides a known-good state to return to.

---

## References

### Project Documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture and component details
- [SUMMARY.md](SUMMARY.md) - Project status and overview
- [SCRATCHPAD.md](SCRATCHPAD.md) - Development notes and history
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [REQUIREMENTS.md](REQUIREMENTS.md) - Functional requirements

### Code Patterns in Project

#### Panel Pattern (Successful Extractions)
- **LayerPanel**: `src/ui/layer_panel.py` - 500+ lines extracted
- **TimelinePanel**: `src/ui/timeline_panel.py` - 400+ lines extracted
- **ColorWheel**: `src/ui/color_wheel.py` - 300+ lines extracted

These successful extractions prove the pattern works.

#### Manager Pattern
- **LayerManager**: `src/core/layer_manager.py` - Manages layer state
- **UndoManager**: `src/core/undo_manager.py` - Manages undo/redo
- **ThemeManager**: `src/ui/theme_manager.py` - Manages themes
- **ColorPalette**: `src/core/color_palette.py` - Manages colors

#### Tool Pattern
- **BaseTool**: `src/tools/base_tool.py` - Base class for all tools
- Individual tools: brush.py, eraser.py, fill.py, selection.py, etc.
- All ~100-200 lines each (ideal size)

### Previous Successful Refactorings
1. **Custom Colors** (v1.15): Extracted to `src/core/custom_colors.py` ✅
2. **File Association** (v1.16): Extracted to `src/utils/file_association.py` ✅
3. **Export System** (v1.17): Extracted to `src/utils/export.py` ✅
4. **Theme System** (v1.20): Extracted to `src/ui/theme_manager.py` ✅
5. **Tooltip System** (v1.22): Extracted to `src/ui/tooltip.py` ✅
6. **Pan Tool** (v1.23): Extracted to `src/tools/pan.py` ✅

**Pattern**: All extractions improved code organization without breaking functionality.

### External Resources
- [Python Module Design Best Practices](https://realpython.com/python-modules-packages/)
- [Refactoring: Improving the Design of Existing Code](https://martinfowler.com/books/refactoring.html)
- [Separation of Concerns](https://en.wikipedia.org/wiki/Separation_of_concerns)

---

## Approval & Sign-off

**Prepared By**: AI Development Team  
**Date**: October 13, 2025  
**Version**: 1.25  
**Status**: Awaiting approval  

### Decision Points

#### Proceed with Full Refactor (7 Phases)?
- [ ] **Yes** - Begin Phase 1, commit to full refactor
- [ ] **Partial** - Start with Phase 1-3 only, evaluate
- [ ] **No** - Keep current architecture, revisit later

#### Estimated Commitment
- **Full Refactor**: 35-42 hours (~1-2 weeks)
- **Partial (Phases 1-3)**: 15 hours (~2-3 days)
- **Phase 1 Only**: 6 hours (~1 day)

---

**Approved By**: _______________  
**Date**: _______________  

**Implementation Start**: _______________  
**Phase 1 Complete**: _______________  
**Phase 7 Complete**: _______________  

---

## Post-Refactor Checklist

### Per-Phase Checklist (Complete after EACH phase)

- [ ] Phase completed and tested locally
- [ ] All features work identically to before
- [ ] No new bugs introduced
- [ ] Visual appearance unchanged
- [ ] main_window.py measurably smaller
- [ ] Module has clear docstrings
- [ ] Git commit with descriptive message
- [ ] REFACTOR.md updated with progress
- [ ] Ready to proceed to next phase

### Final Checklist (Complete after ALL 7 phases)

- [ ] main_window.py reduced to ~300 lines (91% reduction verified)
- [ ] All 7 new modules created and working
- [ ] All features work identically
- [ ] No performance regression
- [ ] Search time dramatically improved
- [ ] ARCHITECTURE.md updated
- [ ] SUMMARY.md updated
- [ ] SCRATCHPAD.md updated
- [ ] CHANGELOG.md updated with refactor entry
- [ ] Documentation review completed
- [ ] User testing completed
- [ ] Production deployment successful

---

## Progress Tracking

Update this section as phases are completed:

| Phase | Module | Status | Completed | Notes |
|-------|--------|--------|-----------|-------|
| 1 | UI Builder | ⏸️ Not Started | - | - |
| 2 | Palette Manager | ⏸️ Not Started | - | - |
| 3 | Theme Applicator | ⏸️ Not Started | - | - |
| 4 | Selection Operations | ⏸️ Not Started | - | - |
| 5 | File Handler | ⏸️ Not Started | - | - |
| 6 | Event Dispatcher | ⏸️ Not Started | - | - |
| 7 | Canvas Renderer | ⏸️ Not Started | - | - |

**Legend**: 
- ⏸️ Not Started
- 🔄 In Progress
- ✅ Complete
- ❌ Failed/Reverted

---

**Last Updated**: October 13, 2025  
**Document Version**: 1.25  
**Next Review**: After Phase 1 completion  
**Status**: Ready for approval

