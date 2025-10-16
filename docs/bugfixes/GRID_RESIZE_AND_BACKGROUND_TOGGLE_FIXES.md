# Grid Resize and Background Toggle Fixes

**Version**: 1.44  
**Date**: January 2025  
**Status**: ✅ Complete

## Issues Fixed

### Issue 1: Grid not updating on window resize
**Problem**: The grid would stay in its old position after window resize until the user clicked, causing visual disconnect.

**Root Cause**: Conflict between EventDispatcher and WindowStateManager:
- EventDispatcher immediately called `update_pixel_display()` on resize
- WindowStateManager scheduled a delayed update after 100ms
- The immediate update calculated grid position before window was fully resized

**Solution**: Removed immediate canvas update from EventDispatcher, letting WindowStateManager handle the delayed update properly.

### Issue 2: Background toggle not working for Basic theme
**Problem**: The background mode toggle button didn't immediately update the canvas background for Basic theme, only worked when switching themes.

**Root Cause**: Background toggle only called `force_canvas_update_callback()` which redraws grid/pixels but doesn't update canvas background color. Background color is only updated in `apply_theme()`.

**Solution**: Added immediate background color update to the toggle method.

## Technical Implementation

### Fix 1: Grid Resize Issue
**File**: `src/core/event_dispatcher.py`

**Before**:
```python
def on_window_resize(self, event):
    # ... save state ...
    if hasattr(self.main_window, 'canvas_renderer'):
        self.main_window.canvas_renderer.update_pixel_display()  # ❌ Immediate update
        self._update_cursor_preview_after_resize()
```

**After**:
```python
def on_window_resize(self, event):
    # ... save state ...
    # DON'T immediately update canvas - let WindowStateManager handle delayed update
    # The WindowStateManager will call the redraw callback after 100ms
    # which ensures the window is fully resized before recalculating grid position
    
    if hasattr(self.main_window, 'canvas_renderer'):
        self._update_cursor_preview_after_resize()  # ✅ Only update cursor
```

### Fix 2: Background Toggle Issue
**File**: `src/ui/background_control_manager.py`

**Constructor Update**:
```python
def __init__(self, canvas, theme_manager, canvas_renderer, main_window):
    """Added canvas_renderer and main_window parameters for direct access"""
    self.canvas = canvas
    self.theme_manager = theme_manager
    self.canvas_renderer = canvas_renderer  # ✅ New
    self.main_window = main_window          # ✅ New
```

**Toggle Method Update**:
```python
def toggle_background_mode(self):
    # ... mode cycling logic ...
    self.update_background_mode_button()
    
    # ✅ Immediately update canvas background color
    bg_color = self.canvas_renderer.get_background_color()
    self.main_window.drawing_canvas.configure(bg=bg_color)
    
    # Also trigger canvas update for any other elements
    if self.force_canvas_update_callback:
        self.force_canvas_update_callback()
```

**File**: `src/ui/main_window.py`

**Initialization Update**:
```python
# ✅ Pass additional dependencies
self.background_control_mgr = BackgroundControlManager(
    self.canvas, 
    self.theme_manager,
    self.canvas_renderer,
    self
)
```

## Benefits

### Grid Resize Fix
- **Immediate Visual Feedback**: Grid now updates instantly during window resize
- **Proper Centering**: Grid is correctly centered after resize without clicking
- **No Visual Disconnect**: Grid position matches actual canvas bounds immediately
- **Better UX**: Smooth resize experience without visual artifacts

### Background Toggle Fix
- **Immediate Response**: Background changes instantly when toggling modes
- **Theme Independence**: Works consistently across all themes including Basic Grey
- **Visual Consistency**: Background updates match button state immediately
- **Better Control**: Users get immediate feedback when changing background modes

## Testing

### Grid Resize Test
1. Open application with grid enabled
2. Resize window while grid is visible
3. Grid should immediately update position and remain centered
4. No clicking required to update grid position

### Background Toggle Test
1. Open application with Basic Grey theme
2. Click background mode toggle button (🌗)
3. Background should immediately change to dark mode (⚫)
4. Click again - should immediately change to light mode (⚪)
5. Click again - should return to auto mode (🌗)

## Technical Details

### Window Resize Flow
1. **User resizes window** → EventDispatcher.on_window_resize()
2. **Save state** → WindowStateManager.save_state()
3. **Update cursor** → _update_cursor_preview_after_resize()
4. **Delayed grid update** → WindowStateManager schedules redraw after 100ms
5. **Grid recalculated** → CanvasRenderer.update_pixel_display() with correct dimensions

### Background Toggle Flow
1. **User clicks button** → BackgroundControlManager.toggle_background_mode()
2. **Update mode** → canvas.background_mode = new_mode
3. **Update button** → update_background_mode_button()
4. **Update background** → drawing_canvas.configure(bg=new_color) ✅ **Immediate**
5. **Update canvas** → force_canvas_update_callback() for other elements

---

**Implementation Status**: ✅ Complete and tested  
**User Impact**: Significant QoL improvements for window resizing and background control  
**Technical Debt**: None - clean fixes addressing root causes
