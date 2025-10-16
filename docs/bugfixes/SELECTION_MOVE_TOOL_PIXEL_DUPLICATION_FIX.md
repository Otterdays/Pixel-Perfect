# Selection Move Tool Pixel Duplication Bug Fix

**Date**: October 16, 2025  
**Version**: 2.2.4  
**Severity**: Critical  
**Status**: ✅ FIXED

---

## Bug Description

### The Problem
After fixing the "pixels deleted underneath" bug in version 2.2.3, a new bug appeared:
- **First move**: Worked correctly - pixels moved from point A to point B
- **Second move**: Pixels would be DUPLICATED at the new location
- **Third move**: More duplication would occur
- This made the move tool unusable for iterative adjustments

### User Impact
- Users couldn't make multiple adjustments to selection placement
- Pixels would appear twice (or more) at the destination location
- Workflow was broken for fine-tuning pixel placement
- Only workaround was to undo and move again in one go

### Visual Example
```
Initial State:           After First Move:        After Second Move:
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   [RED]     │         │             │         │             │
│             │   →     │   [RED]     │   →     │  [RED][RED] │  (DUPLICATED!)
│             │         │             │         │             │
└─────────────┘         └─────────────┘         └─────────────┘
```

---

## Root Cause Analysis

### The Bug Chain

The previous fix (v2.2.3) preserved `original_selection` to prevent pixel deletion, but this exposed a new problem:

1. **Every Move Operation**
   ```python
   on_mouse_up() 
   → Draw pixels at new location ✓ (CORRECT)
   → finalize_move() 
     → Draw pixels at new location AGAIN ✗ (DUPLICATION!)
   ```

2. **Why This Happened**
   - `finalize_move()` was being called automatically after EVERY drop (line 233)
   - `finalize_move()` is designed to:
     1. Clear pixels from ORIGINAL position (already empty after first move)
     2. Draw pixels at CURRENT position (already drawn by `on_mouse_up()`)
   - Result: Pixels drawn twice = duplication

### Code Location
**File**: `src/tools/selection.py`, lines 225-233 (before fix)
```python
if self.original_selection:
    orig_left, orig_top, orig_width, orig_height = self.original_selection
    if left != orig_left or top != orig_top:
        self.has_been_moved = True
        print(f"[MOVE] Pixels drawn (background saved for non-destructive adjustment)")
        
        # Auto-finalize the move operation to clear original position
        self.finalize_move(canvas)  # ⚠️ CALLED EVERY TIME = DUPLICATION
```

### Design Flaw

The automatic `finalize_move()` call was meant to clear the original position after the first move. However:
- After the first move, the original position is already cleared
- Subsequent moves don't need to clear anything
- Calling `finalize_move()` on subsequent moves just duplicates the drawing

---

## The Solution

### Strategy
**Only call `finalize_move()` on the FIRST move**, not on subsequent moves.

### Implementation

#### 1. Added Conditional Finalization
**File**: `src/tools/selection.py`, lines 232-236

```python
# BEFORE (Bug):
if left != orig_left or top != orig_top:
    self.has_been_moved = True
    print(f"[MOVE] Pixels drawn (background saved for non-destructive adjustment)")
    
    # Auto-finalize the move operation to clear original position
    self.finalize_move(canvas)  # ⚠️ Called every time = duplication

# AFTER (Fixed):
if left != orig_left or top != orig_top:
    self.has_been_moved = True
    print(f"[MOVE] Pixels drawn (background saved for non-destructive adjustment)")
    
    # Only finalize on the FIRST move to clear original position
    # Subsequent moves don't need finalization since original is already cleared
    if not self.pixels_cleared:  # Only finalize once
        self.finalize_move(canvas)
        self.pixels_cleared = True  # Mark as finalized
```

#### 2. State Management
**Key Variables:**
- `pixels_cleared`: Tracks whether finalization has occurred
- `reset_state()`: Resets `pixels_cleared = False` for new selections

**File**: `src/tools/selection.py`, line 137
```python
def reset_state(self):
    """Reset move tool state (called when selection is cleared or tool is switched)"""
    # ... other resets ...
    self.pixels_cleared = False  # Reset for new selection
```

---

## Fixed Logic Flow

### First Move (Clears Original Position)
```python
on_mouse_down()
→ if not self.original_selection:  # TRUE (first time)
    → Clear pixels at original location ✓
    → Set self.original_selection = (left, top, width, height)

on_mouse_up()
→ Draw pixels at new location ✓
→ finalize_move()  # Called because pixels_cleared = False ✓
    → Clear pixels from original position ✓ (already empty)
    → Draw pixels at new position ✓ (duplicate, but original is cleared)
→ Set pixels_cleared = True ✓
```

### Second Move (No Duplication)
```python
on_mouse_up()
→ Draw pixels at new location ✓
→ if not self.pixels_cleared:  # FALSE ✓
    → Skip finalize_move() ✓
→ No duplication! ✓
```

### Third Move, Fourth Move, etc. (All Work)
Same as second move - no finalization, no duplication.

### Tool Switch or Clear Selection
```python
_select_tool("different_tool")
→ move_tool.reset_state()
    → self.pixels_cleared = False ✓ (Fresh start)
```

---

## Testing & Verification

### Test Case 1: Multiple Repositions
1. ✅ Select red pixels
2. ✅ Switch to move tool
3. ✅ Move to location B - pixels appear once ✓
4. ✅ Pick up and move to location C - pixels appear once ✓ (no duplication)
5. ✅ Pick up and move to location D - pixels appear once ✓ (no duplication)
6. ✅ Repeat multiple times - works every time

### Test Case 2: Tool Switching
1. ✅ Select and move pixels multiple times
2. ✅ Switch to brush tool - move state resets
3. ✅ Make new selection
4. ✅ Move - treats as first move (correct behavior)

### Test Case 3: Clear Selection
1. ✅ Select and move pixels multiple times
2. ✅ Clear selection (Esc or click outside)
3. ✅ Make new selection
4. ✅ Move - treats as first move (correct behavior)

---

## Files Modified

### `src/tools/selection.py`
- **Line 232-236**: Added conditional finalization logic with `pixels_cleared` check
- **Line 137**: Added comment clarifying `pixels_cleared` reset in `reset_state()`
- **Line 234-236**: Added detailed comments explaining the fix

---

## Result

### ✅ Fixed Behaviors
- Users can now move selections **unlimited times** without duplication
- **First move**: Clears original position, draws at new location
- **Subsequent moves**: Only draws at new location (no duplication)
- **Tool switch**: Properly finalizes and resets state for new selections
- **Clean state management**: Each new selection starts fresh

### 📊 Impact
- **User Workflow**: Now fully functional for iterative adjustments
- **Data Integrity**: No more unwanted pixel duplication
- **Productivity**: Users can freely fine-tune positioning
- **Code Quality**: Proper state management with clear boundaries

---

## Lessons Learned

### State Management
- Automatic operations should have clear boundaries and conditions
- Don't repeat operations that should only happen once
- Use flags to track operation state and prevent duplicate execution

### Testing
- After fixing one bug, always test the "do it again" scenario
- Edge cases often appear when fixing related functionality
- User workflows involve multiple iterations - test them thoroughly

### Code Evolution
- Fixes can introduce new bugs if not carefully considered
- Each fix should be tested in isolation AND in combination with existing fixes
- Document the intended behavior clearly to prevent regression

---

## Related Documentation
- `docs/SCRATCHPAD.md` - Version 2.2.4 entry
- `docs/CHANGELOG.md` - Version 2.2.4 entry
- `docs/bugfixes/SELECTION_MOVE_TOOL_PIXEL_DELETION_FIX.md` - Previous related bug fix
- `src/tools/selection.py` - Move tool implementation

## Version History
- **v2.2.3**: Fixed "pixels deleted underneath" bug
- **v2.2.4**: Fixed "pixel duplication" bug (this fix)
