# AI Analysis: Next Refactor Opportunities

## Current State: main_window.py = 1,888 lines
**Progress**: 44.3% reduction from baseline (3,387 → 1,888)
**Target**: 850-900 lines
**Remaining**: ~990 lines to extract

---

## 📊 Remaining Method Categories (66 methods total)

### 🎨 **Category 1: Color View Management** (~550 lines) ⭐ **BIGGEST**
**21 methods related to palette views, color wheel, saved colors, constants**

**Color View Switching (5 methods, ~68 lines):**
- `_on_palette_change()` - Handle palette dropdown changes (13 lines)
- `_initialize_all_views()` - Initialize all views at startup (23 lines)
- `_show_view()` - Switch between grid/wheel/saved/constants (28 lines)
- `_on_view_mode_change()` - Radio button handler (4 lines)

**Constants View (3 methods, ~108 lines):**
- `_create_constants_grid()` - Build constants UI (63 lines)
- `_get_canvas_colors()` - Extract used colors from canvas (17 lines)
- `_on_constant_color_click()` - Handle color selection (28 lines)

**Saved Colors View (7 methods, ~282 lines):**
- `_create_saved_colors_view()` - Build saved colors UI (96 lines)
- `_update_saved_color_buttons()` - Update button states (27 lines)
- `_on_saved_slot_click()` - Empty slot handler (19 lines)
- `_on_saved_color_click()` - Filled slot handler (9 lines)
- `_export_saved_colors()` - Export to file (14 lines)
- `_import_saved_colors()` - Import from file (15 lines)
- `_clear_all_saved_colors()` - Clear all with dialog (94 lines)

**Color Wheel (6 methods, ~87 lines):**
- `_create_color_wheel()` - Build wheel UI (18 lines)
- `_on_color_wheel_changed()` - Wheel callback (9 lines)
- `_save_custom_color()` - Add custom color (19 lines)
- `_remove_custom_color()` - Delete custom (7 lines)
- `_update_custom_colors_display()` - Update grid (6 lines, if exists)
- `_set_color_from_eyedropper()` - Complex eyedropper logic (64 lines)

**Grid View (2 methods, ~25 lines):**
- `_select_color()` - Select palette color (12 lines)
- `_update_color_grid_selection()` - Update selection borders (12 lines)

**Total**: ~550 lines

---

### 🔧 **Category 2: Tool Size Management** (~140 lines)
**8 methods for brush/eraser size selection**

**Brush Size (4 methods, ~70 lines):**
- `_show_brush_size_menu()` - Right-click menu (29 lines)
- `_set_brush_size()` - Size setter (9 lines)
- `_update_brush_button_text()` - Update button label (6 lines)
- `_draw_brush_at()` - Draw NxN brush (16 lines)

**Eraser Size (4 methods, ~70 lines):**
- `_show_eraser_size_menu()` - Right-click menu (29 lines)
- `_set_eraser_size()` - Size setter (9 lines)
- `_update_eraser_button_text()` - Update button label (6 lines)
- `_erase_at()` - Erase NxN area (15 lines)

**Total**: ~140 lines

---

### 🖼️ **Category 3: Canvas/Zoom Management** (~180 lines)
**3 methods for canvas sizing and zoom**

- `_on_size_change()` - Canvas size dropdown (97 lines)
- `_apply_custom_canvas_size()` - Custom size handler (63 lines)
- `_on_zoom_change()` - Zoom dropdown (11 lines)

**Total**: ~180 lines

---

### 🎛️ **Category 4: UI State Management** (~120 lines)
**10 methods for UI toggles and layout**

- `_toggle_left_panel()` - Panel collapse (5 lines)
- `_toggle_right_panel()` - Panel collapse (5 lines)
- `_redraw_canvas_after_resize()` - Window resize (4 lines)
- `_toggle_grid()` - Grid toggle (6 lines)
- `_update_grid_button_text()` - Update button (9 lines)
- `_toggle_grid_overlay()` - Overlay toggle (6 lines)
- `_update_grid_overlay_button_text()` - Update button (9 lines)
- `_calculate_optimal_panel_widths()` - Responsive sizing (41 lines)
- `_save_window_state()` - Persist window state (28 lines)
- `_restore_window_state()` - Load window state (42 lines)

**Total**: ~120 lines

---

### 🛠️ **Category 5: Core Orchestration** (~90 lines) ⚠️ **KEEP IN MAIN**
**Essential methods that coordinate the app**

- `__init__()` - Constructor (194 lines - some extractable)
- `_create_ui()` - UI creation orchestration (147 lines - some extractable)
- `_create_layer_and_timeline_panels()` - Panel setup (100 lines - some extractable)
- `_get_ui_callbacks()` - Callback dictionary (27 lines)
- `_select_tool()` - Tool switching (48 lines)
- `_update_tool_selection()` - Update button states (9 lines)
- `_on_layer_changed()` - Layer change handler (5 lines)
- `_update_canvas_from_layers()` - Sync canvas (8 lines)
- `_clear_selection_and_reset_tools()` - Reset state (10 lines)
- `_get_drawing_layer()` - Get active layer (21 lines)
- `_handle_eyedropper_click()` - Eyedropper handler (22 lines)
- `_on_theme_selected()` - Theme change (5 lines)
- `_show_file_menu()` - File menu (55 lines)
- `_tkinter_screen_to_canvas_coords()` - Coordinate conversion (28 lines)
- `_on_window_close()` - Window close handler (9 lines)
- `get_current_color()` - Get active color (public method)

---

### 🔄 **Category 6: Undo/Redo** (~60 lines)
- `_update_undo_redo_buttons()` - Update button states (12 lines)
- `_undo()` - Undo action (19 lines)
- `_redo()` - Redo action (19 lines)
- `_add_layer()` - Add layer (8 lines)
- `_sync_canvas_with_layers()` - Sync (11 lines)

---

### 🎬 **Category 7: Animation** (~40 lines)
- `_on_frame_changed()` - Frame change handler (10 lines)
- `_toggle_animation()` - Play/pause (8 lines)
- `_previous_frame()` - Previous frame (6 lines)
- `_next_frame()` - Next frame (6 lines)

---

## 🎯 **NEXT REFACTOR RECOMMENDATION**

### **Phase 2: Color View Manager** (~550 lines)

**Why This Next:**
1. ✅ **Largest impact** - Removes 550 lines (29% reduction)
2. ✅ **Clear boundaries** - All color view related methods
3. ✅ **Already modular** - Uses palette_views classes (GridView, SavedView, etc.)
4. ⚠️ **Most complex** - Heavy UI dependencies, should be done carefully

**Create**: `src/ui/color_view_manager.py`

**Methods to Extract (21 total):**
- All color view switching logic
- All saved colors UI and management
- All constants view logic
- Color wheel creation and callbacks
- Eyedropper color setting
- Custom colors management
- Grid view selection updates

**Estimated Reduction:**
- main_window.py: 1,888 → ~1,338 lines (-550 lines, -29%)
- Total progress: 60.5% reduction from baseline

---

## 💡 **Alternative: Tool Size Manager** (~140 lines)

**Why Consider This:**
1. ✅ **Much easier** - Simple menu/state management
2. ✅ **Lower risk** - Less UI coupling
3. ✅ **Quick win** - Can complete in 30-45 minutes
4. ⚠️ **Smaller impact** - Only 140 lines (~7% reduction)

**Create**: `src/ui/tool_size_manager.py`

**Methods to Extract (8 total):**
- Brush size menu, setter, button update, draw_at
- Eraser size menu, setter, button update, erase_at

**Estimated Reduction:**
- main_window.py: 1,888 → ~1,748 lines (-140 lines, -7%)

---

## 🎲 **Recommendation**

### **Option A: Go Big** 
Extract Color View Manager (550 lines) for maximum impact
- **Pro**: Gets us to 60% total reduction, major cleanup
- **Con**: Most complex refactor, higher risk, 2-3 hours

### **Option B: Quick Win**
Extract Tool Size Manager (140 lines) first, then Color View Manager
- **Pro**: Low risk, quick success, builds confidence
- **Con**: Two separate refactors instead of one

### **My Vote: Option A (Color View Manager)**
We've already completed 4 successful refactors. The team is experienced now. Going for the big win makes sense to get main_window.py closer to the target of 850-900 lines.

**Current**: 1,888 lines  
**After Color View Manager**: ~1,338 lines  
**Remaining to target**: ~438 lines (mostly core orchestration)

This would put us at **60% completion** of the refactoring goal!
