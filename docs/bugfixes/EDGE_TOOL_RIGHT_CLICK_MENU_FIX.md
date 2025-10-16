# Edge Tool Right-Click Thickness Menu Fix

Date: January 2025  
Version: 2.5.4  
Status: RESOLVED

## Symptom
Right-clicking the Edge tool button did not show the thickness selection menu.

## Root Cause
The Edge button is created later as a separate CTk button (not inside the initial loop where brush/eraser were bound). The right-click binding existed for loop-created buttons, but the separately created `edge_btn` did not have the `<Button-3>` binding.

## Fix
- Added explicit binding for the standalone Edge button in `src/ui/ui_builder.py`:
  - `edge_btn.bind("<Button-3>", callbacks['show_edge_thickness_menu'])`
- Verified `_get_ui_callbacks()` exposes `show_edge_thickness_menu`
- Ensured `ToolSizeManager.update_edge_button_text()` runs after tool buttons are assigned

## Result
- Right-clicking the Edge button reliably opens the thickness popup, matching brush/eraser behavior.
