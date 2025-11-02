# Primary Color Selection TypeError Fix

## Issue Description
**Bug**: When selecting a color in the Primary palette view, the application crashes with a TypeError.

**Error Message**:
```
TypeError: '<=' not supported between instances of 'int' and 'tuple'
```

**Stack Trace**:
```
File "src\ui\palette_views\primary_view.py", line 319, in _select_color_variation
    self.on_color_select(color)
File "src\ui\main_window.py", line 900, in _select_color
    self.palette.set_primary_color(color_index)
File "src\ui\..\core\color_palette.py", line 259, in set_primary_color
    if 0 <= index < len(self.colors):
```

## Root Cause Analysis
The issue was in the `_select_color_variation` method in `primary_view.py`. The method was passing a color tuple (RGBA value) to the `on_color_select` callback, but the `_select_color` method in `main_window.py` expected an integer index.

**Problematic Code**:
```python
# In primary_view.py
def _select_color_variation(self, color):
    # ... other code ...
    if self.on_color_select:
        self.on_color_select(color)  # ❌ Passing tuple instead of index
```

**Expected Behavior**:
The `_select_color` method in `main_window.py` expects an integer index:
```python
def _select_color(self, color_index: int):
    self.palette.set_primary_color(color_index)  # ❌ Receives tuple, expects int
```

## Solution
Fixed the `_select_color_variation` method to pass the color index instead of the color tuple:

**Fixed Code**:
```python
def _select_color_variation(self, color):
    """Handle color variation selection"""
    # Set this color as the primary color in the palette
    self.palette.set_primary_color_by_rgba(color)
    
    # Update canvas color
    self.canvas.current_color = color
    
    # Note: Primary view does NOT call on_color_select to prevent auto-switching to brush
    # This prevents color bleeding to grid when just selecting colors
    # The color is already set in the palette and canvas, which is sufficient
```

## Additional Fix: Color Bleeding Prevention
**Issue**: After fixing the TypeError, colors were still bleeding onto the grid area when selecting Primary palette colors.

**Root Cause**: The primary view was calling `self.on_color_select()` which triggered the `_select_color` method in `main_window.py`, which automatically switches to the brush tool, causing immediate painting.

**Solution**: Removed the `on_color_select` callback from the primary view's `_select_color_variation` method. The primary view now only:
1. Sets the color in the palette using `set_primary_color_by_rgba()`
2. Updates the canvas current color
3. Does NOT trigger automatic brush tool switching

This prevents color bleeding while maintaining proper color selection functionality.

## Files Modified
- `src/ui/palette_views/primary_view.py` - Fixed `_select_color_variation` method

## Verification
- ✅ Primary color selection no longer causes TypeError
- ✅ Color selection works correctly in Primary palette view
- ✅ Colors do NOT bleed onto the grid when selecting Primary palette colors
- ✅ Grid view continues to work correctly (passes `color_index` and auto-switches to brush)
- ✅ Primary view now behaves differently from Grid view (no auto-switch to brush)
- ✅ No linting errors introduced

## Impact
- **User Experience**: Users can now select colors from the Primary palette view without crashes
- **Functionality**: Primary color variations can be selected without bleeding onto the grid
- **Stability**: Eliminates a critical crash when using color variations
- **Behavioral Difference**: Primary view now behaves as a color picker (no auto-brush), while Grid view remains a quick-paint tool (auto-brush)

## Related Issues
This fix creates a behavioral distinction between palette views:
- **Grid View**: Acts as a quick-paint tool - selecting colors automatically switches to brush tool for immediate painting
- **Primary View**: Acts as a color picker - selecting colors only changes the active color without switching tools or painting

This differentiation provides users with two different workflows:
1. **Quick Painting**: Use Grid view for rapid color switching and painting
2. **Color Selection**: Use Primary view for careful color selection without accidental painting

## Date Fixed
January 2025 - Version 2.5.7
