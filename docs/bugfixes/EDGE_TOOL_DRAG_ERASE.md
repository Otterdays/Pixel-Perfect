# Edge Tool Drag Erase (Right-Click Hold) Implementation

Date: January 2025  
Version: 2.5.4  
Status: COMPLETE

## Overview
Adds the ability to hold right-click and drag to continuously erase edge segments using the same nearest-edge detection used for drawing.

## Event Routing
- Canvas binds:
  - `<Button-3>` → start erase at cursor
  - `<B3-Motion>` → continuous erase while dragging
  - `<ButtonRelease-3>` → end erase
- Implemented in `src/core/event_dispatcher.py`:
  - `on_tkinter_canvas_right_click`, `on_tkinter_canvas_right_drag`, `on_tkinter_canvas_right_up`
- Float precision coordinate conversion used for accuracy.

## Tool Logic
- `EdgeTool.on_mouse_down(..., button=3, ...)` triggers `_erase_edge_at_position`
- Drag path calls `on_mouse_move` to update hover, then `on_mouse_down(..., button=3, ...)` repeatedly
- Deferred redraw: sets `pending_redraw` and performs batch redraw on mouse-up for smoothness

## Result
- Users can erase multiple contiguous edge segments quickly by right-dragging
- Behavior mirrors brush/eraser drag semantics but operates on stored edge lines
