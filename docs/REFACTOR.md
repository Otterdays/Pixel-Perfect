# Pixel Perfect - Refactoring Plan

**Date**: October 13, 2025  
**Version**: 1.19  
**Status**: Proposed

## Executive Summary

This document outlines a refactoring plan to improve code organization by extracting selection operations from `main_window.py` into a dedicated operations module. This aligns with the project's #1 rule: "Split up components to as many parts as possible, in order to reduce token consumption."

**Current Issue**: `main_window.py` has grown to **2,649 lines**, with selection operations (`_mirror_selection`, `_rotate_selection`, `_copy_selection`, `_scale_selection`) embedded within the UI code.

**Goal**: Extract these operations into `src/operations/selection_operations.py` to improve maintainability, testability, and code organization.

---

## Current Architecture Analysis

### File Size Breakdown

```
main_window.py:        2,649 lines  ⚠️ Too large
  - UI setup:          ~400 lines
  - Tool management:   ~200 lines
  - Canvas operations: ~800 lines
  - Selection ops:     ~400 lines   ← Target for extraction
  - Event handlers:    ~600 lines
  - Helper methods:    ~249 lines
```

### Selection Operations (Current Location: main_window.py)

#### Operations to Extract
1. **Mirror Selection** (`_mirror_selection`)
   - Lines: ~45
   - Dependencies: selection_tool, canvas, layers
   - Complexity: Medium (pixel manipulation with numpy)

2. **Rotate Selection** (`_rotate_selection`)
   - Lines: ~65
   - Dependencies: selection_tool, canvas, layers
   - Complexity: Medium (rotation with dimension swap)

3. **Copy Selection** (`_copy_selection`)
   - Lines: ~35
   - Dependencies: selection_tool, copy_buffer state
   - Complexity: Low (data copying)

4. **Scale Selection** (`_scale_selection`)
   - Lines: ~30
   - Dependencies: selection_tool, scaling state variables
   - Complexity: Medium (state management)

5. **Apply Scale** (`_apply_scale`)
   - Lines: ~80
   - Dependencies: selection_tool, canvas, layers, scipy/numpy
   - Complexity: High (pixel scaling with fallback)

6. **Supporting Methods**
   - `_get_scale_handle()`: ~30 lines (handle detection)
   - `_draw_scale_handle()`: ~15 lines (handle rendering)
   - `_simple_scale()`: ~40 lines (fallback scaling)
   - `_place_copy_at()`: ~40 lines (copy placement)

**Total to Extract**: ~380 lines of selection operation code

---

## Proposed Architecture

### New Module Structure

```
src/
  operations/
    __init__.py
    selection_operations.py
    base_operation.py (future)
```

### Class Design: SelectionOperations

```python
# src/operations/selection_operations.py

class SelectionOperations:
    """
    Handles all operations on selected pixel regions.
    Operations: Mirror, Rotate, Copy, Scale
    """
    
    def __init__(self, canvas_manager, layer_manager, undo_manager=None):
        self.canvas_manager = canvas_manager
        self.layer_manager = layer_manager
        self.undo_manager = undo_manager
        
        # State for scaling
        self.is_scaling = False
        self.scale_handle = None
        self.scale_start_pos = None
        self.scale_original_rect = None
        
        # State for copy/paste
        self.copy_buffer = None
        self.copy_dimensions = None
        self.copy_preview_pos = None
        self.is_placing_copy = False
    
    # Core Operations
    def mirror(self, selection_tool):
        """Mirror selected pixels horizontally"""
        pass
    
    def rotate(self, selection_tool):
        """Rotate selected pixels 90° clockwise"""
        pass
    
    def copy(self, selection_tool):
        """Copy selected pixels to buffer"""
        pass
    
    def place_copy_at(self, x: int, y: int):
        """Place copied pixels at position"""
        pass
    
    # Scaling Operations
    def enter_scale_mode(self, selection_tool):
        """Enter interactive scaling mode"""
        pass
    
    def exit_scale_mode(self):
        """Exit scaling mode"""
        pass
    
    def start_scale_drag(self, selection_tool, canvas_x, canvas_y):
        """Start dragging a scale handle"""
        pass
    
    def update_scale_drag(self, selection_tool, canvas_x, canvas_y):
        """Update scale during drag"""
        pass
    
    def end_scale_drag(self, selection_tool):
        """End scale drag operation"""
        pass
    
    def apply_scale(self, selection_tool, new_rect):
        """Apply scaling to pixels"""
        pass
    
    # Helper Methods
    def get_scale_handle(self, x, y, rect, zoom):
        """Detect which scale handle is under cursor"""
        pass
    
    def get_scale_cursor(self, handle):
        """Get cursor name for scale handle"""
        pass
    
    def _scale_pixels_scipy(self, pixels, old_size, new_size):
        """Scale using scipy (preferred)"""
        pass
    
    def _scale_pixels_numpy(self, pixels, old_size, new_size):
        """Scale using numpy (fallback)"""
        pass
```

### Integration with MainWindow

```python
# In main_window.py __init__

from src.operations.selection_operations import SelectionOperations

# Create operations manager
self.selection_ops = SelectionOperations(
    canvas_manager=self.canvas,
    layer_manager=self.layer_manager,
    undo_manager=None  # Future enhancement
)

# Button callbacks become simple delegations
def _mirror_selection(self):
    self.selection_ops.mirror(self.tools.get("selection"))

def _rotate_selection(self):
    self.selection_ops.rotate(self.tools.get("selection"))

def _copy_selection(self):
    self.selection_ops.copy(self.tools.get("selection"))

def _scale_selection(self):
    self.selection_ops.enter_scale_mode(self.tools.get("selection"))
    self._update_ui_for_scaling()  # UI state management stays in main_window
```

---

## Benefits

### Code Organization
- ✅ **Separation of Concerns**: Operations logic separated from UI logic
- ✅ **Reduced File Size**: main_window.py reduced by ~380 lines (15% reduction)
- ✅ **Single Responsibility**: Each module has clear, focused purpose
- ✅ **Easier Navigation**: Developers can find operation code quickly

### Maintainability
- ✅ **Isolated Changes**: Modify operations without touching UI code
- ✅ **Better Testing**: Operations can be unit tested independently
- ✅ **Clearer Dependencies**: Explicit interfaces show what operations need
- ✅ **Reduced Coupling**: Operations don't directly access UI elements

### Future Extensibility
- ✅ **New Operations**: Easy to add Flip, Skew, Perspective, etc.
- ✅ **Undo/Redo**: Operations interface ready for undo system integration
- ✅ **Batch Operations**: Can apply multiple operations programmatically
- ✅ **API Ready**: Operations exposed for scripting/automation (future)

### Performance
- ✅ **Lazy Loading**: Operations only loaded when needed
- ✅ **Reduced Import Time**: Smaller main_window.py imports faster
- ✅ **Better Caching**: Python can cache smaller modules more efficiently

---

## Risks & Mitigation

### Risk 1: State Management Complexity
**Issue**: Operations need access to UI state (buttons, canvas, layers)

**Mitigation**:
- Pass required state explicitly to operations
- Use context objects to bundle related state
- Keep UI state management in main_window.py
- Operations only handle pixel/data transformations

### Risk 2: Increased Coupling Between Modules
**Issue**: main_window.py and operations module need to communicate

**Mitigation**:
- Define clear interfaces (SelectionOperations class)
- Use dependency injection (pass managers in __init__)
- Document required dependencies in class docstrings
- Keep operations module self-contained

### Risk 3: Breaking Existing Functionality
**Issue**: Refactoring could introduce bugs

**Mitigation**:
- Comprehensive testing before and after refactor
- Keep original code in git history
- Refactor in small, testable increments
- Test each operation individually after extraction

### Risk 4: Regression in Performance
**Issue**: Additional function calls might slow operations

**Mitigation**:
- Profile before and after refactor
- Operations are infrequent (not per-frame)
- Actual pixel manipulation time >> function call overhead
- Expected impact: negligible (<1ms per operation)

---

## Detailed Refactoring Steps

### Phase 1: Preparation (30 minutes)

#### Step 1.1: Create Module Structure
```bash
mkdir src/operations
touch src/operations/__init__.py
touch src/operations/selection_operations.py
```

#### Step 1.2: Define Base Interface
```python
# src/operations/__init__.py
from .selection_operations import SelectionOperations

__all__ = ['SelectionOperations']
```

#### Step 1.3: Create Skeleton Class
```python
# src/operations/selection_operations.py
import numpy as np
from typing import Optional, Tuple

class SelectionOperations:
    """Handles operations on selected pixel regions"""
    
    def __init__(self, canvas_manager, layer_manager):
        self.canvas_manager = canvas_manager
        self.layer_manager = layer_manager
        # State variables...
```

### Phase 2: Extract Methods (60 minutes)

#### Step 2.1: Extract Mirror Operation
1. Copy `_mirror_selection` to `SelectionOperations.mirror()`
2. Update to use `self.canvas_manager` instead of `self.canvas`
3. Update to use `self.layer_manager` instead of `self.layer_manager`
4. Return success status and message for main_window to handle
5. Test mirror operation

#### Step 2.2: Extract Rotate Operation
1. Copy `_rotate_selection` to `SelectionOperations.rotate()`
2. Update canvas/layer references
3. Test rotation operation

#### Step 2.3: Extract Copy Operation
1. Copy `_copy_selection` to `SelectionOperations.copy()`
2. Move `copy_buffer`, `copy_dimensions` to SelectionOperations
3. Update main_window to reference `self.selection_ops.copy_buffer`
4. Test copy/paste workflow

#### Step 2.4: Extract Scale Operations
1. Copy all scaling methods:
   - `_scale_selection` → `enter_scale_mode()`
   - `_apply_scale` → `apply_scale()`
   - `_get_scale_handle` → `get_scale_handle()`
   - `_draw_scale_handle` → (keep in main_window - UI rendering)
   - `_simple_scale` → `_scale_pixels_numpy()`
2. Move scaling state variables to SelectionOperations
3. Update main_window references
4. Test scaling workflow

### Phase 3: Update main_window.py (30 minutes)

#### Step 3.1: Add Import
```python
from src.operations.selection_operations import SelectionOperations
```

#### Step 3.2: Initialize Operations Manager
```python
def __init__(self, ...):
    # ... existing init code ...
    
    # Create operations manager
    self.selection_ops = SelectionOperations(
        canvas_manager=self.canvas,
        layer_manager=self.layer_manager
    )
```

#### Step 3.3: Update Button Callbacks
```python
def _mirror_selection(self):
    # Exit scaling mode if active
    if self.selection_ops.is_scaling:
        self.selection_ops.exit_scale_mode()
        self.scale_btn.configure(fg_color="gray")
        self._update_tool_selection()
    
    # Perform mirror operation
    success, message = self.selection_ops.mirror(self.tools.get("selection"))
    if message:
        print(message)
    
    if success:
        self._update_canvas_from_layers()
        self._update_pixel_display()
```

#### Step 3.4: Update Scaling Mouse Handlers
```python
def _on_tkinter_canvas_mouse_down(self, event):
    # ... existing code ...
    
    # Handle scaling mode
    if self.selection_ops.is_scaling:
        canvas_x, canvas_y = self._tkinter_screen_to_canvas_coords(event.x, event.y)
        selection_tool = self.tools.get("selection")
        
        result = self.selection_ops.start_scale_drag(
            selection_tool, canvas_x, canvas_y
        )
        
        if result == "apply":
            # Apply scale and exit
            self.selection_ops.exit_scale_mode()
            self.scale_btn.configure(fg_color="gray")
            self._update_tool_selection()
            self._update_pixel_display()
        elif result == "dragging":
            # Started dragging a handle
            pass
        
        return
```

### Phase 4: Testing (30 minutes)

#### Test Plan
1. **Unit Tests** (if test framework exists):
   - Test mirror operation on 4x4 sample
   - Test rotate operation on 4x4 sample
   - Test copy buffer storage
   - Test scale handle detection
   - Test pixel scaling algorithms

2. **Integration Tests**:
   - Open app, make selection
   - Test Mirror: Select pixels → Click Mirror → Verify flip
   - Test Rotate: Select pixels → Click Rotate × 4 → Verify 360°
   - Test Copy: Select → Copy → Click to place → Verify copy
   - Test Scale: Select → Scale → Drag handle → Apply → Verify resize

3. **Edge Cases**:
   - Empty selection
   - 1x1 selection
   - Full canvas selection
   - Selection at canvas edge
   - Multiple operations in sequence

4. **Performance Tests**:
   - Time operations before refactor
   - Time operations after refactor
   - Verify <10% overhead (expected: <1%)

### Phase 5: Documentation (15 minutes)

#### Update Documentation
1. **ARCHITECTURE.md**: Add operations module section
2. **README.md**: Update code organization section
3. **SCRATCHPAD.md**: Add refactor entry
4. **Code Comments**: Add docstrings to new module

---

## Success Criteria

### Must Have (P0)
- ✅ All operations work identically to before refactor
- ✅ No new bugs introduced
- ✅ main_window.py reduced by at least 300 lines
- ✅ All existing tests pass (if any)
- ✅ Application launches and runs without errors

### Should Have (P1)
- ✅ Operations can be called independently (not just from buttons)
- ✅ Clear separation between operation logic and UI state
- ✅ Code is more maintainable (subjective but reviewable)
- ✅ Documentation updated

### Nice to Have (P2)
- ✅ Unit tests for operations module
- ✅ Performance benchmarks showing no regression
- ✅ Example usage in operations module docstring
- ✅ Future roadmap for additional operations

---

## Timeline

| Phase | Task | Estimated Time | Total |
|-------|------|----------------|-------|
| 1 | Preparation | 30 min | 30 min |
| 2 | Extract Methods | 60 min | 90 min |
| 3 | Update main_window | 30 min | 120 min |
| 4 | Testing | 30 min | 150 min |
| 5 | Documentation | 15 min | 165 min |

**Total Estimated Time**: 2.75 hours

**Buffer for Issues**: +45 minutes

**Total with Buffer**: **3.5 hours**

---

## Alternative Approaches Considered

### Alternative 1: Keep Everything in main_window.py
**Pros**: Simple, no refactoring needed
**Cons**: File continues to grow, harder to maintain
**Verdict**: ❌ Not recommended - violates #1 rule

### Alternative 2: Create Individual Files per Operation
**Pros**: Maximum modularity
**Cons**: Too many small files, overhead of imports
**Verdict**: ❌ Over-engineered for current needs

### Alternative 3: Create Operations Namespace within main_window.py
**Pros**: No new files, some organization
**Cons**: File still large, not truly separated
**Verdict**: ❌ Doesn't solve core problem

### Alternative 4: Extract to SelectionOperations Class (CHOSEN)
**Pros**: Balanced, clear ownership, testable, future-ready
**Cons**: Requires careful state management
**Verdict**: ✅ **RECOMMENDED**

---

## Future Enhancements

### Phase 2 Refactoring (Future)
Once selection operations are extracted, consider:

1. **Extract Tool Management** (`src/tools/tool_manager.py`)
   - Move tool registration and switching logic
   - ~150 lines extracted

2. **Extract Canvas Operations** (`src/canvas/canvas_manager.py`)
   - Move pixel manipulation helpers
   - ~200 lines extracted

3. **Extract Event Handlers** (`src/events/event_dispatcher.py`)
   - Move mouse/keyboard event routing
   - ~300 lines extracted

4. **Extract UI State** (`src/ui/ui_state.py`)
   - Move button state, mode flags
   - ~100 lines extracted

**Result**: main_window.py becomes thin orchestration layer (~800 lines)

### New Operations to Add
Once operations module exists:
- **Flip Vertical**: Mirror on Y axis
- **Outline**: Add outline to selection
- **Shadow**: Add drop shadow effect
- **Crop to Selection**: Resize canvas to selection bounds
- **Expand Selection**: Grow/shrink selection by N pixels
- **Color Replace**: Replace one color with another in selection
- **Hue Shift**: Adjust hue of selected pixels

---

## Rollback Plan

If refactoring introduces critical bugs:

1. **Immediate Rollback**:
   ```bash
   git checkout HEAD~1 src/
   ```

2. **Partial Rollback** (keep some changes):
   - Cherry-pick working operations
   - Revert problematic operations
   - Fix and re-apply

3. **Testing Before Deploy**:
   - Always test refactored code locally
   - Don't push to main until fully tested
   - Use feature branch: `refactor/selection-operations`

---

## References

### Related Documents
- [ARCHITECTURE.md](ARCHITECTURE.md) - Current architecture overview
- [SUMMARY.md](SUMMARY.md) - Project status
- [SCRATCHPAD.md](SCRATCHPAD.md) - Development notes

### Code Patterns
- **Tool Pattern**: See `src/tools/base_tool.py`
- **Manager Pattern**: See `src/core/layer_manager.py`
- **State Pattern**: See `src/animation/timeline.py`

### Similar Refactorings
- **Custom Colors**: Extracted to `src/core/custom_colors.py` (Success)
- **File Association**: Extracted to `src/utils/file_association.py` (Success)
- **Export**: Extracted to `src/utils/export.py` (Success)

---

## Approval & Sign-off

**Prepared By**: AI Development Team  
**Date**: October 13, 2025  
**Status**: Awaiting approval  

**Approved By**: _______________  
**Date**: _______________  

**Implementation Start**: _______________  
**Implementation Complete**: _______________  

---

## Post-Refactor Checklist

- [ ] All operations work identically
- [ ] No new bugs in testing
- [ ] main_window.py reduced by 300+ lines
- [ ] Operations module has clear docstrings
- [ ] ARCHITECTURE.md updated
- [ ] SCRATCHPAD.md updated with refactor notes
- [ ] Git commit with clear message
- [ ] Performance verified (no regression)
- [ ] User testing completed
- [ ] Documentation review completed

---

**Last Updated**: October 13, 2025  
**Version**: 1.0  
**Next Review**: After implementation

