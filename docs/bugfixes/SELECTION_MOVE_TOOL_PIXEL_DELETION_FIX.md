# Selection Move Tool Pixel Deletion Bug Fix

**Date**: October 16, 2025  
**Version**: 2.2.3  
**Severity**: Critical  
**Status**: ✅ FIXED

---

## Bug Description

### The Problem
When using the Selection tool to select pixels, then the Move tool to move them:
1. **First move**: Works correctly - pixels move from point A to point B
2. **Second move (adjustment)**: Picking up the selection again would **DELETE the pixels underneath** at point B
3. This made it impossible to make fine adjustments to placement without destroying artwork

### User Impact
- Users couldn't reposition moved selections without data loss
- Any attempt to adjust placement would destroy pixels underneath
- Workflow was destructive and frustrating
- Only workaround was to undo and move again in one go (not practical)

### Visual Example
```
Initial State:           After First Move:        After Second Pickup:
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   [RED]     │         │             │         │             │
│             │   →     │   [BLUE]    │   →     │   [BLUE]    │  (BLUE destroyed!)
│   [BLUE]    │         │   [RED]     │         │   [RED]     │
└─────────────┘         └─────────────┘         └─────────────┘
```

---

## Root Cause Analysis

### The Bug Chain

1. **First Move Operation**
   ```python
   on_mouse_down() 
   → if not self.original_selection:  # TRUE (first time)
       → Clear pixels at original location ✓ (CORRECT)
       → Set self.original_selection = (left, top, width, height)
   
   on_mouse_up()
   → Draw pixels at new location
   → finalize_move()
       → self.original_selection = None  # ⚠️ THE BUG!
   ```

2. **Second Move Operation (Bug Triggers)**
   ```python
   on_mouse_down()
   → if not self.original_selection:  # TRUE again! ⚠️
       → Clear pixels at CURRENT location ✗ (WRONG!)
       → Destroys pixels underneath the moved selection
   ```

### Why This Happened

The `finalize_move()` method was resetting `self.original_selection = None` after the first move. This caused the logic to treat every subsequent pickup as a "first pickup", executing the clearing logic that should only run once.

**Key Code Location**: `src/tools/selection.py`, line 274 (before fix)
```python
def finalize_move(self, layer):
    # ... move pixels ...
    
    # Reset state
    self.has_been_moved = False
    self.pixels_cleared = False
    self.original_selection = None  # ⚠️ THIS CAUSED THE BUG
    self.saved_background = None
```

### Design Flaw

The code had a mechanism to save and restore backgrounds (`saved_background`), but it could never be used because `original_selection` was being reset, causing the code to always take the "first pickup" branch instead of the "subsequent pickup" branch.

---

## The Solution

### Strategy
**Preserve the move state** by NOT resetting `original_selection` in `finalize_move()`. Only reset it when truly starting a new selection or switching tools.

### Implementation

#### 1. Fixed `finalize_move()` - Don't Reset Too Early
**File**: `src/tools/selection.py`, lines 271-279

```python
# BEFORE (Bug):
def finalize_move(self, layer):
    # ... move pixels ...
    
    self.has_been_moved = False
    self.pixels_cleared = False
    self.original_selection = None  # ⚠️ Caused the bug
    self.saved_background = None

# AFTER (Fixed):
def finalize_move(self, layer):
    # ... move pixels ...
    
    # Reset state - but KEEP original_selection so subsequent pickups
    # know this isn't a first-time pickup and won't clear pixels underneath
    self.has_been_moved = False
    self.pixels_cleared = False
    # DON'T reset original_selection here - it prevents the bug where
    # picking up again deletes pixels underneath
    # self.original_selection = None  # ⚠️ REMOVED - this caused the bug
    self.saved_background = None
```

#### 2. Added `reset_state()` Method
**File**: `src/tools/selection.py`, lines 131-141

```python
def reset_state(self):
    """Reset move tool state (called when selection is cleared or tool is switched)"""
    self.is_moving = False
    self.move_offset = (0, 0)
    self.original_selection = None  # ✓ Reset HERE instead
    self.cleared_background = None
    self.pixels_cleared = False
    self.has_been_moved = False
    self.last_drawn_position = None
    self.saved_background = None
    print("[MOVE] State reset - ready for new selection")
```

This method is called when:
- Switching to a different tool (not move/selection)
- Explicitly clearing the selection
- Starting a completely new selection

#### 3. Updated Main Window - Call reset_state() Appropriately
**File**: `src/ui/main_window.py`

**Location 1**: Tool switching (lines 799-807)
```python
selection_tool = self.tools.get("selection")
move_tool = self.tools.get("move")
if selection_tool and selection_tool.has_selection:
    selection_tool.clear_selection()
    # Reset move tool state when clearing selection
    if move_tool:
        move_tool.reset_state()  # ✓ Added
    self.canvas_renderer.update_pixel_display()
```

**Location 2**: Clear selection and reset tools (lines 1148-1160)
```python
def _clear_selection_and_reset_tools(self):
    """Clear any active selection and reset tools to brush"""
    selection_tool = self.tools.get("selection")
    move_tool = self.tools.get("move")
    if selection_tool and selection_tool.has_selection:
        selection_tool.clear_selection()
        # Reset move tool state when clearing selection
        if move_tool:
            move_tool.reset_state()  # ✓ Added
    
    self._select_tool("brush")
```

---

## Fixed Logic Flow

### First Move (Works Same as Before)
```python
on_mouse_down()
→ if not self.original_selection:  # TRUE (first time)
    → Clear pixels at original location ✓
    → Set self.original_selection = (left, top, width, height)

on_mouse_up()
→ Save background pixels at new location
→ Draw pixels at new location
→ finalize_move()
    → self.original_selection PRESERVED ✓ (NOT reset)
```

### Second Move (Now Works Correctly!)
```python
on_mouse_down()
→ if not self.original_selection:  # FALSE ✓
→ elif self.saved_background and self.last_drawn_position:  # TRUE ✓
    → Restore saved background from last drop ✓
    → NO pixel destruction! ✓

on_mouse_up()
→ Save NEW background pixels
→ Draw pixels at NEW location
→ finalize_move()
    → self.original_selection PRESERVED ✓
```

### Third Move, Fourth Move, etc. (All Work!)
Same as second move - the `saved_background` mechanism now works properly because `original_selection` is preserved.

### Tool Switch or Clear Selection
```python
_select_tool("different_tool")
→ move_tool.reset_state()
    → self.original_selection = None ✓ (Fresh start)
```

---

## Testing & Verification

### Test Case 1: Multiple Repositions
1. ✅ Select red pixels
2. ✅ Switch to move tool
3. ✅ Move to location with blue pixels underneath
4. ✅ Pick up again - blue pixels are PRESERVED (not deleted)
5. ✅ Move to another location
6. ✅ Pick up again - pixels underneath are PRESERVED
7. ✅ Repeat - works every time

### Test Case 2: Tool Switching
1. ✅ Select and move pixels
2. ✅ Switch to brush tool - move state resets
3. ✅ Make new selection
4. ✅ Move - treats as first move (correct behavior)

### Test Case 3: Clear Selection
1. ✅ Select and move pixels
2. ✅ Clear selection (Esc or click outside)
3. ✅ Make new selection
4. ✅ Move - treats as first move (correct behavior)

---

## Files Modified

### 1. `src/tools/selection.py`
- **Line 131-141**: Added `reset_state()` method
- **Line 275-277**: Commented out `original_selection = None` in `finalize_move()`
- **Line 271-279**: Added detailed comments explaining the bug and fix

### 2. `src/ui/main_window.py`
- **Line 800, 805**: Added move_tool reference and `reset_state()` call in `_select_tool()`
- **Line 1152, 1157**: Added move_tool reference and `reset_state()` call in `_clear_selection_and_reset_tools()`

---

## Result

### ✅ Fixed Behaviors
- Users can now pick up and reposition selections **unlimited times**
- Pixels underneath are **preserved** during all adjustments
- No more **destructive behavior** when fine-tuning placement
- **Clean state management** when switching tools or starting new selections
- The `saved_background` restoration mechanism now works as originally intended

### 📊 Impact
- **User Workflow**: Now non-destructive and intuitive
- **Data Safety**: No more accidental pixel loss
- **Productivity**: Users can freely adjust positioning without fear
- **Code Quality**: Proper separation of concerns (reset only when needed)

---

## Lessons Learned

### State Management
- State should only be reset at logical boundaries (tool switch, selection clear)
- Don't reset state too aggressively in the middle of operations
- Preserve state needed for iterative operations

### Testing
- Need to test "do it again" scenarios, not just "do it once"
- Edge cases often appear in repeated operations
- User workflows involve adjustments and iterations

### Code Comments
- Complex state logic needs clear comments explaining when/why state is reset
- Document the purpose of state variables and their lifecycle
- Add warnings about side effects of resetting state

---

## Related Documentation
- `docs/SCRATCHPAD.md` - Version 2.2.3 entry
- `docs/CHANGELOG.md` - Version 2.2.3 entry
- `src/tools/selection.py` - Move tool implementation
- `src/ui/main_window.py` - Tool switching and selection management

