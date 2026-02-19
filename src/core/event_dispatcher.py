"""
Event Dispatcher for Pixel Perfect
Handles all keyboard, mouse, and window events

OPTIMIZATION: Uses CanvasEventOptimizer for throttled mouse event handling
"""

from typing import Callable, Dict, Any, Optional, Tuple
import tkinter as tk
from src.core.canvas import Canvas, SymmetryWrapper
from src.core.layer_manager import Layer
from .event_throttle import CanvasEventOptimizer


class EventDispatcher:
    """Centralized event handling for the application"""
    
    def __init__(self, main_window):
        """
        Initialize the event dispatcher
        
        Args:
            main_window: Reference to MainWindow instance for accessing state and methods
        """
        self.main_window = main_window
        
        # Event state tracking
        self.is_dragging = False
        self.last_canvas_x = None
        self.last_canvas_y = None
        
        # Initialize event throttling for smooth mouse handling
        # 8ms = ~120 FPS target for responsive cursor preview updates
        self.canvas_optimizer = CanvasEventOptimizer(throttle_ms=8.0)
        
        # State tracking for middle mouse pan
        self.is_middle_panning = False
        
        # State tracking for right-click: pan-on-hold vs context-menu-on-release
        self.is_right_panning = False
        self._right_click_start_x = 0
        self._right_click_start_y = 0
        self._right_click_did_drag = False  # True once drag exceeds threshold
        self._RIGHT_CLICK_DRAG_THRESHOLD = 5  # pixels before it becomes a pan
        
    def bind_all_events(self):
        """Bind all keyboard, mouse, and window events"""
        root = self.main_window.root
        
        # Keyboard events
        root.bind("<Key>", self.on_key_press)
        try:
            root.focus_set()
        except Exception:
            pass  # Ignore focus errors during initialization
        
        # Window events
        root.bind("<Configure>", self.on_window_resize)
        root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # Panel resize events
        self.main_window.paned_window.bind("<ButtonPress-1>", self.on_sash_drag_start)
        self.main_window.paned_window.bind("<ButtonRelease-1>", self.on_sash_drag_end)
        
        # Focus events
        root.bind("<FocusIn>", self.on_focus_in)
        
        # Canvas mouse events
        if hasattr(self.main_window, 'drawing_canvas') and self.main_window.drawing_canvas:
            self.main_window.drawing_canvas.bind("<Button-1>", self.on_tkinter_canvas_mouse_down)
            self.main_window.drawing_canvas.bind("<ButtonRelease-1>", self.on_tkinter_canvas_mouse_up)
            self.main_window.drawing_canvas.bind("<B1-Motion>", self.on_tkinter_canvas_mouse_drag)
            self.main_window.drawing_canvas.bind("<Button-3>", self.on_tkinter_canvas_right_click)
            self.main_window.drawing_canvas.bind("<B3-Motion>", self.on_tkinter_canvas_right_drag)
            self.main_window.drawing_canvas.bind("<ButtonRelease-3>", self.on_tkinter_canvas_right_up)
            self.main_window.drawing_canvas.bind("<Motion>", self.on_tkinter_canvas_mouse_move)
            # Mouse wheel zoom (Ctrl + wheel)
            self.main_window.drawing_canvas.bind("<MouseWheel>", self.on_mouse_wheel)
            self.main_window.drawing_canvas.bind("<Button-4>", self.on_mouse_wheel)
            self.main_window.drawing_canvas.bind("<Button-5>", self.on_mouse_wheel)
            
            # Middle mouse pan (Button-2 on Windows/Linux)
            self.main_window.drawing_canvas.bind("<Button-2>", self.on_middle_mouse_down)
            self.main_window.drawing_canvas.bind("<B2-Motion>", self.on_middle_mouse_drag)
            self.main_window.drawing_canvas.bind("<ButtonRelease-2>", self.on_middle_mouse_up)
    
    # ==================== Window & Panel Events ====================
    
    def on_sash_drag_start(self, event):
        """Called when user starts dragging panel divider"""
        self.main_window.window_state_manager.is_resizing_panels = True
    
    def on_sash_drag_end(self, event):
        """Called when user stops dragging panel divider"""
        # #region agent log
        try:
            import json, time, os
            p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "debug-00503f.log")
            open(p, "a").write(json.dumps({"sessionId":"00503f","location":"event_dispatcher.py:on_sash_drag_end","message":"Sash drag ended","data":{"has_redraw":False},"timestamp":int(time.time()*1000),"hypothesisId":"B"})+"\n")
        except Exception: pass
        # #endregion
        self.main_window.window_state_manager.is_resizing_panels = False
        self.main_window.window_state_manager.save_state()
    
    def on_window_resize(self, event):
        """Handle window resize events"""
        # Only handle resize events for the root window
        if event.widget == self.main_window.root:
            # #region agent log
            try:
                import json, time, os
                p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "debug-00503f.log")
                open(p, "a").write(json.dumps({"sessionId":"00503f","location":"event_dispatcher.py:on_window_resize","message":"Root Configure","data":{"w":event.width,"h":event.height},"timestamp":int(time.time()*1000),"hypothesisId":"C"})+"\n")
            except Exception: pass
            # #endregion
            # Save window state after resize
            if hasattr(self.main_window, 'window_state_manager'):
                self.main_window.window_state_manager.save_state()
                # Call WindowStateManager's resize handler to trigger redraw
                self.main_window.window_state_manager.on_window_resize(event)
            
            # Still update cursor preview position after resize
            if hasattr(self.main_window, 'canvas_renderer'):
                self._update_cursor_preview_after_resize()
    
    def on_restore_btn_enter(self, button):
        """Handle mouse enter on restore button"""
        button.configure(fg_color="#2fa572")
    
    def on_restore_btn_leave(self, button):
        """Handle mouse leave on restore button"""
        button.configure(fg_color="transparent")
    
    def on_focus_in(self, event):
        """Handle window focus in event"""
        # Refresh layer panel when window gains focus
        if hasattr(self.main_window, 'layer_panel') and self.main_window.layer_panel:
            self.main_window.layer_panel.refresh()
        
        # Refresh timeline panel if it exists
        if hasattr(self.main_window, 'timeline_panel') and self.main_window.timeline_panel:
            self.main_window.timeline_panel.refresh()
    
    def _update_cursor_preview_after_resize(self):
        """Update cursor preview position after window resize"""
        try:
            # Get current mouse position
            mouse_x = self.main_window.root.winfo_pointerx() - self.main_window.root.winfo_rootx()
            mouse_y = self.main_window.root.winfo_pointery() - self.main_window.root.winfo_rooty()
            
            # Check if mouse is over the drawing canvas
            canvas_x = self.main_window.drawing_canvas.winfo_x()
            canvas_y = self.main_window.drawing_canvas.winfo_y()
            canvas_width = self.main_window.drawing_canvas.winfo_width()
            canvas_height = self.main_window.drawing_canvas.winfo_height()
            
            # Check if mouse is within canvas bounds
            if (canvas_x <= mouse_x <= canvas_x + canvas_width and 
                canvas_y <= mouse_y <= canvas_y + canvas_height):
                
                # Convert to canvas coordinates
                canvas_coords = self.main_window._tkinter_screen_to_canvas_coords(
                    mouse_x - canvas_x, mouse_y - canvas_y
                )
                canvas_x_coord, canvas_y_coord = canvas_coords
                
                # Check if we're in bounds
                if (0 <= canvas_x_coord < self.main_window.canvas.width and 
                    0 <= canvas_y_coord < self.main_window.canvas.height):
                    
                    # Update cursor preview based on current tool
                    if self.main_window.current_tool == "brush":
                        self.main_window.canvas_renderer.draw_brush_preview(canvas_x_coord, canvas_y_coord)
                    elif self.main_window.current_tool == "eraser":
                        self.main_window.canvas_renderer.draw_eraser_preview(canvas_x_coord, canvas_y_coord)
                    elif self.main_window.current_tool == "spray":
                        self.main_window.canvas_renderer.draw_spray_preview(canvas_x_coord, canvas_y_coord)
                    elif self.main_window.current_tool == "dither":
                        self.main_window.canvas_renderer.draw_dither_preview(canvas_x_coord, canvas_y_coord)
                    elif self.main_window.current_tool == "texture":
                        texture_tool = self.main_window.tools.get("texture")
                        if texture_tool:
                            self.main_window.canvas_renderer.draw_texture_preview(texture_tool, canvas_x_coord, canvas_y_coord)
                else:
                    # Mouse is outside canvas bounds, clear previews
                    self.main_window.drawing_canvas.delete("brush_preview")
                    self.main_window.drawing_canvas.delete("eraser_preview")
                    self.main_window.drawing_canvas.delete("spray_preview")
                    self.main_window.drawing_canvas.delete("dither_preview")
                    self.main_window.drawing_canvas.delete("texture_preview")
                    self.main_window.drawing_canvas.delete("edge_preview")
            else:
                # Mouse is outside canvas, clear previews
                self.main_window.drawing_canvas.delete("brush_preview")
                self.main_window.drawing_canvas.delete("eraser_preview")
                self.main_window.drawing_canvas.delete("spray_preview")
                self.main_window.drawing_canvas.delete("texture_preview")
                self.main_window.drawing_canvas.delete("edge_preview")
                
        except Exception as e:
            # Silently handle any errors during cursor update
            pass
    
    def on_window_close(self):
        """Handle window close event"""
        # Save window state before closing
        if hasattr(self.main_window, 'window_state_manager'):
            self.main_window.window_state_manager.save_state()
        
        # Destroy the window
        self.main_window.root.destroy()
    
    # ==================== Keyboard Events ====================
    
    def on_key_press(self, event):
        """Handle keyboard events"""
        # F11 for fullscreen toggle
        if event.keysym == 'F11':
            self.main_window._toggle_fullscreen()
            return
        
        # Escape key - exit fullscreen first, then handle other escape actions
        if event.keysym.lower() == 'escape':
            # Exit fullscreen if active
            if hasattr(self.main_window, 'is_fullscreen') and self.main_window.is_fullscreen:
                self.main_window._exit_fullscreen()
                return
            # Otherwise handle rotation cancel
            if hasattr(self.main_window, 'selection_mgr'):
                if self.main_window.selection_mgr.is_rotating:
                    self.main_window.selection_mgr.cancel_rotation()
                    return
        
        # Tab key - toggle panels
        if event.keysym == 'Tab':
            if hasattr(self.main_window, 'window_state_manager'):
                wsm = self.main_window.window_state_manager
                
                # Shift+Tab: Toggle left panel only
                if event.state & 0x1:
                    wsm.toggle_left_panel()
                    return
                
                # Tab: Toggle both panels (Maximize Canvas mode)
                # If either panel is visible, hide both. If both hidden, show both.
                if not wsm.left_panel_collapsed or not wsm.right_panel_collapsed:
                    # Hide both
                    if not wsm.left_panel_collapsed:
                        wsm.toggle_left_panel()
                    if not wsm.right_panel_collapsed:
                        wsm.toggle_right_panel()
                else:
                    # Show both
                    wsm.toggle_left_panel()
                    wsm.toggle_right_panel()
            return
        
        # Ctrl+Z for undo
        if event.state & 0x4 and event.keysym.lower() == 'z':
            if event.state & 0x1:  # Shift is also pressed (Ctrl+Shift+Z)
                self.main_window.redo()
            else:  # Just Ctrl+Z
                self.main_window.undo()
            return
        
        # Ctrl+Y for redo
        if event.state & 0x4 and event.keysym.lower() == 'y':
            self.main_window.redo()
            return
        
        # Ctrl+S for save
        if event.state & 0x4 and event.keysym.lower() == 's':
            self.main_window.save_project()
            return
        
        # Ctrl+O for open
        if event.state & 0x4 and event.keysym.lower() == 'o':
            self.main_window.open_project()
            return
        
        # Ctrl+N for new project
        if event.state & 0x4 and event.keysym.lower() == 'n':
            # Route through FileOperationsManager to ensure full cleanup
            if hasattr(self.main_window, 'file_ops'):
                self.main_window.file_ops.new_project()
            return
        
        # Handle rotation preview mode (Enter key)
        if hasattr(self.main_window, 'selection_mgr'):
            if event.keysym.lower() == 'return':  # Enter key - apply rotation
                if self.main_window.selection_mgr.is_rotating:
                    self.main_window.selection_mgr.apply_rotation()
                    return
        
        # Ctrl+E for export PNG
        if event.state & 0x4 and event.keysym.lower() == 'e':
            if not (event.state & 0x1):  # Not Shift (Ctrl+E, not Ctrl+Shift+E)
                if hasattr(self.main_window, 'file_ops'):
                    self.main_window.file_ops.export_png()
                return
        
        # Ctrl+Shift+E for quick export
        if event.state & 0x4 and event.state & 0x1 and event.keysym.lower() == 'e':
            if hasattr(self.main_window, 'file_ops'):
                self.main_window.file_ops.quick_export()
            return
        
        # Ctrl+C for copy (only if there's a selection)
        if event.state & 0x4 and event.keysym.lower() == 'c':
            selection_tool = self.main_window.tools.get("selection")
            if selection_tool and selection_tool.has_active_selection():
                if hasattr(self.main_window, 'context_menu_mgr'):
                    self.main_window.context_menu_mgr._copy_selection()
            return
        
        # Ctrl+V for paste (only if there's something to paste)
        if event.state & 0x4 and event.keysym.lower() == 'v':
            if (hasattr(self.main_window, 'selection_mgr') and 
                self.main_window.selection_mgr.copy_buffer is not None):
                if hasattr(self.main_window, 'context_menu_mgr'):
                    self.main_window.context_menu_mgr._paste_selection()
            return
        
        # Ctrl+X for cut (only if there's a selection)
        if event.state & 0x4 and event.keysym.lower() == 'x':
            selection_tool = self.main_window.tools.get("selection")
            if selection_tool and selection_tool.has_active_selection():
                if hasattr(self.main_window, 'context_menu_mgr'):
                    self.main_window.context_menu_mgr._cut_selection()
                    return
        
        # Delete key for delete selection
        if event.keysym == 'Delete' or event.keysym == 'BackSpace':
            if hasattr(self.main_window, 'context_menu_mgr'):
                self.main_window.context_menu_mgr._delete_selection()
            return
        
        # Tool shortcuts (B, E, F, D, S, L, Q, C, P, M, R, T, X)
        if not (event.state & 0x4):  # No Ctrl modifier
            key = event.keysym.lower()
            tool_map = {
                'b': 'brush',
                'e': 'eraser',
                'y': 'spray',
                'f': 'fill',
                'd': 'eyedropper',
                's': 'selection',
                'w': 'magic_wand',
                'l': 'line',
                'q': 'square',
                'c': 'circle',
                'p': 'pan',
                'm': 'move',
                'r': 'rotate',
                't': 'texture'
            }
            
            # Shift+R to toggle reference panel (before tool_map so it takes priority)
            if key == 'r' and (event.state & 0x1):
                if hasattr(self.main_window, 'reference_panel'):
                    self.main_window.reference_panel.toggle_visibility()
                return
            
            # Shift+P to toggle mini preview window
            if key == 'p' and (event.state & 0x1):
                self.main_window.canvas_renderer.toggle_mini_preview()
                return
            
            # Shift+T to toggle 3D token preview panel
            if key == 't' and (event.state & 0x1):
                if hasattr(self.main_window, 'token_preview_panel'):
                    self.main_window.token_preview_panel.toggle_visibility()
                return
            
            if key in tool_map:
                self.main_window._select_tool(tool_map[key])
                return
            
            # X for swap colors
            if key == 'x':
                self.main_window.swap_colors()
                return

    def on_mouse_wheel(self, event):
        """Handle mouse wheel zoom with Ctrl modifier"""
        # Require Ctrl for zoom to avoid accidental scroll zoom
        if not (event.state & 0x4):
            return

        direction = 0
        if hasattr(event, 'delta') and event.delta != 0:
            direction = 1 if event.delta > 0 else -1
        elif hasattr(event, 'num'):
            if event.num == 4:
                direction = 1
            elif event.num == 5:
                direction = -1

        if direction == 0:
            return

        if hasattr(self.main_window, '_zoom_at_cursor'):
            self.main_window._zoom_at_cursor(direction, event.x, event.y)
    
    # ==================== Mouse Events (Canvas) ====================
    
    def on_middle_mouse_down(self, event):
        """Handle middle mouse down for panning"""
        if "pan" in self.main_window.tools:
            tool = self.main_window.tools["pan"]
            tool.start_pan(event.x, event.y, self.main_window.pan_offset_x, self.main_window.pan_offset_y)
            self.is_middle_panning = True
            
            # Change cursor to hand
            try:
                self.main_window.drawing_canvas.configure(cursor="fleur")
            except Exception:
                pass

    def on_middle_mouse_drag(self, event):
        """Handle middle mouse drag for panning"""
        if not self.is_middle_panning or "pan" not in self.main_window.tools:
             return
             
        tool = self.main_window.tools["pan"]
        result = tool.update_pan(event.x, event.y, self.main_window.canvas.zoom)
        if result is not None:
             temp_offset_x, temp_offset_y = result
             # Temporarily update display with new pan offset
             old_offset_x = self.main_window.pan_offset_x
             old_offset_y = self.main_window.pan_offset_y
             self.main_window.pan_offset_x = temp_offset_x
             self.main_window.pan_offset_y = temp_offset_y
             self.main_window.canvas_renderer.update_pixel_display()
             # Restore original offset (will be set permanently on mouse up)
             self.main_window.pan_offset_x = old_offset_x
             self.main_window.pan_offset_y = old_offset_y

    def on_middle_mouse_up(self, event):
        """Handle middle mouse up"""
        if not self.is_middle_panning or "pan" not in self.main_window.tools:
             return
             
        tool = self.main_window.tools["pan"]
        result = tool.update_pan(event.x, event.y, self.main_window.canvas.zoom)
        if result is not None:
             self.main_window.pan_offset_x, self.main_window.pan_offset_y = result
        
        tool.end_pan()
        self.main_window.canvas_renderer.update_pixel_display()
        self.is_middle_panning = False
        
        # Restore cursor
        try:
            self.main_window.drawing_canvas.configure(cursor="arrow")
        except Exception:
            pass
    
    def on_tkinter_canvas_mouse_down(self, event):
        """Handle mouse down on tkinter canvas"""
        # Clear any tool previews when starting to draw
        self.main_window.drawing_canvas.delete("brush_preview")
        self.main_window.drawing_canvas.delete("eraser_preview")
        self.main_window.drawing_canvas.delete("spray_preview")
        self.main_window.drawing_canvas.delete("texture_preview")
        self.main_window.drawing_canvas.delete("edge_preview")
        
        # Handle pan tool start (use raw screen coords, not canvas coords!)
        if self.main_window.current_tool == "pan":
            tool = self.main_window.tools["pan"]
            tool.start_pan(event.x, event.y, self.main_window.pan_offset_x, self.main_window.pan_offset_y)
            return
        
        # Convert tkinter screen coordinates to canvas coordinates
        canvas_x, canvas_y = self.main_window._tkinter_screen_to_canvas_coords(event.x, event.y)

        # Handle copy placement mode
        if self.main_window.selection_mgr.is_placing_copy and self.main_window.selection_mgr.copy_buffer is not None:
            if 0 <= canvas_x < self.main_window.canvas.width and 0 <= canvas_y < self.main_window.canvas.height:
                # Save undo state before placing paste
                active_layer = self.main_window.layer_manager.get_active_layer()
                if active_layer:
                    edge_lines = None
                    edge_tool = self.main_window.tools.get("edge")
                    if edge_tool and hasattr(edge_tool, 'edge_lines'):
                        edge_lines = edge_tool.edge_lines
                    
                    self.main_window.undo_manager.save_state(
                        active_layer.pixels.copy(),
                        self.main_window.layer_manager.active_layer_index,
                        edge_lines
                    )
                
                self.main_window.selection_mgr.place_copy_at(canvas_x, canvas_y)
            return
        
        # Handle rotation preview mode - commit rotation on ANY click,
        # then continue handling this click (so user can immediately start a move)
        if self.main_window.selection_mgr.is_rotating:
            self.main_window.selection_mgr.apply_rotation()
            # Do not return; fall through to normal processing
        
        # Handle scaling mode
        if self.main_window.selection_mgr.is_scaling:
            selection_tool = self.main_window.tools.get("selection")
            if selection_tool and selection_tool.selection_rect:
                left, top, width, height = selection_tool.selection_rect
                
                # Check if clicking near a handle or edge
                handle = self.main_window.selection_mgr.get_scale_handle(canvas_x, canvas_y, left, top, width, height)
                
                if handle:
                    # Start scaling from this handle
                    self.main_window.selection_mgr.scale_handle = handle
                    # Reset baseline to the CURRENT rect so each drag uses latest bounds
                    self.main_window.selection_mgr.scale_original_rect = selection_tool.selection_rect
                    self.main_window.selection_mgr.scale_true_original_rect = selection_tool.selection_rect
                    self.main_window.selection_mgr.scale_is_dragging = True
                    return
                else:
                    # Click outside handles - cancel scaling mode
                    self.main_window.selection_mgr.is_scaling = False
                    self.main_window.selection_mgr.scale_handle = None
                    self.main_window.canvas_renderer.update_pixel_display()
                    return
        
        # Check if we're in bounds
        if not (0 <= canvas_x < self.main_window.canvas.width and 0 <= canvas_y < self.main_window.canvas.height):
            return
        
        # Save undo state before any drawing operation
        if self.main_window.current_tool in ["brush", "eraser", "spray", "fill", "texture", "line", "rectangle", "circle", "edge", "dither"]:
            active_layer = self.main_window.layer_manager.get_active_layer()
            if active_layer:
                # ALWAYS save edge lines state so undo preserves them regardless of current tool
                edge_lines = None
                edge_tool = self.main_window.tools.get("edge")
                if edge_tool and hasattr(edge_tool, 'edge_lines'):
                    edge_lines = edge_tool.edge_lines
                
                self.main_window.undo_manager.save_state(active_layer.pixels.copy(), self.main_window.layer_manager.active_layer_index, edge_lines)
        
        # Set dragging state
        self.is_dragging = True
        self.last_canvas_x = canvas_x
        self.last_canvas_y = canvas_y
        
        # Get current tool
        tool = self.main_window.tools.get(self.main_window.current_tool)
        if not tool:
            return
        
        # Handle eyedropper tool specially
        if self.main_window.current_tool == "eyedropper":
            self.main_window._handle_eyedropper_click(canvas_x, canvas_y, 1)  # Left click
            return
        
        # Get current drawing color (from palette or color wheel based on view mode)
        current_color = self.main_window.get_current_color()
        
        # Track color usage for recent colors palette
        if hasattr(self.main_window, 'recent_colors') and self.main_window.recent_colors:
            self.main_window.recent_colors.add_color(current_color)
        
        # Handle all brush sizes consistently
        if self.main_window.current_tool == "brush":
            draw_layer = self.main_window._get_drawing_layer()
            if draw_layer:
                target_layer = SymmetryWrapper(draw_layer, self.main_window.canvas)
                self.main_window.tool_size_mgr.draw_brush_at(target_layer, canvas_x, canvas_y, current_color)
                self.main_window.layer_manager.invalidate_cache()  # Pixels were modified
                self.main_window._update_canvas_from_layers()
                self.main_window.canvas_renderer.update_pixel_display()
            if hasattr(tool, 'is_drawing'):
                tool.is_drawing = True  # Set drawing state
            return
        elif self.main_window.current_tool == "eraser":
            draw_layer = self.main_window._get_drawing_layer()
            if draw_layer:
                target_layer = SymmetryWrapper(draw_layer, self.main_window.canvas)
                self.main_window.tool_size_mgr.erase_at(target_layer, canvas_x, canvas_y)
                self.main_window.layer_manager.invalidate_cache()  # Pixels were modified
                self.main_window._update_canvas_from_layers()
                self.main_window.canvas_renderer.update_pixel_display()
            if hasattr(tool, 'is_erasing'):
                tool.is_erasing = True  # Set erasing state
        elif self.main_window.current_tool == "spray":
            draw_layer = self.main_window._get_drawing_layer()
            if draw_layer:
                target_layer = SymmetryWrapper(draw_layer, self.main_window.canvas)
                self.main_window.tool_size_mgr.spray_at(target_layer, canvas_x, canvas_y, current_color)
                self.main_window.layer_manager.invalidate_cache()  # Pixels were modified
                self.main_window._update_canvas_from_layers()
                self.main_window.canvas_renderer.update_pixel_display()
            if hasattr(tool, 'is_spraying'):
                tool.is_spraying = True
        elif self.main_window.current_tool == "edge":
            # Handle edge tool with float precision coordinates
            canvas_x_float, canvas_y_float = self.main_window._tkinter_screen_to_canvas_coords_float(event.x, event.y)
            tool.on_mouse_down(self.main_window.canvas, canvas_x_float, canvas_y_float, 1, current_color)
            self.main_window.canvas_renderer.update_pixel_display()
        elif self.main_window.current_tool == "magic_wand":
            # Magic wand works with flattened canvas (all layers combined)
            # Use canvas directly since it shows flattened layers
            tool.on_mouse_down(self.main_window.canvas, canvas_x, canvas_y, 1, current_color)
            self.main_window.canvas_renderer.update_pixel_display()
        elif self.main_window.current_tool in ["fill", "texture", "line", "rectangle", "circle", "move", "selection"]:
            # Handle fill, texture, shape, move, and selection tools with layer-based approach
            draw_layer = self.main_window._get_drawing_layer()
            if draw_layer:
                # Apply symmetry wrapper only for drawing tools
                target_layer = draw_layer
                if self.main_window.current_tool in ["line", "rectangle", "circle", "texture"]:
                    target_layer = SymmetryWrapper(draw_layer, self.main_window.canvas)
                
                tool.on_mouse_down(target_layer, canvas_x, canvas_y, 1, current_color)
                if self.main_window.current_tool in ["fill", "texture"]:
                    # Fill and texture tools update immediately
                    self.main_window.layer_manager.invalidate_cache()  # Pixels were modified
                    self.main_window._update_canvas_from_layers()
                    self.main_window.canvas_renderer.update_pixel_display()
                # Shape tools and move/selection tools don't update on mouse down
        else:
            # Call tool's on_mouse_down method (standard interface) for other tools
            tool.on_mouse_down(self.main_window.canvas, canvas_x, canvas_y, 1, current_color)
            self.main_window.canvas_renderer.update_pixel_display()
    
    def on_tkinter_canvas_mouse_up(self, event):
        """Handle mouse up on tkinter canvas"""
        # Handle pan tool end
        if self.main_window.current_tool == "pan":
            tool = self.main_window.tools["pan"]
            # Get the final pan offset and apply it permanently
            result = tool.update_pan(event.x, event.y, self.main_window.canvas.zoom)
            if result is not None:
                self.main_window.pan_offset_x, self.main_window.pan_offset_y = result
            tool.end_pan()
            self.main_window.canvas_renderer.update_pixel_display()
            return
        
        # Handle scaling mode
        if self.main_window.selection_mgr.is_scaling and self.main_window.selection_mgr.scale_handle:
            # Finish scaling - apply the scale
            selection_tool = self.main_window.tools.get("selection")
            if selection_tool and selection_tool.selection_rect:
                self.main_window.selection_mgr.apply_scale(selection_tool.selection_rect)
            self.main_window.selection_mgr.scale_handle = None
            self.main_window.selection_mgr.scale_is_dragging = False
            self.main_window.canvas_renderer.update_pixel_display()
            return
        
        # Convert tkinter screen coordinates to canvas coordinates
        canvas_x, canvas_y = self.main_window._tkinter_screen_to_canvas_coords(event.x, event.y)
        
        # Check if we're in bounds
        if not (0 <= canvas_x < self.main_window.canvas.width and 0 <= canvas_y < self.main_window.canvas.height):
            self.is_dragging = False
            return
        
        # Get current tool
        tool = self.main_window.tools.get(self.main_window.current_tool)
        if not tool:
            self.is_dragging = False
            return
        
        # Get current drawing color (from palette or color wheel based on view mode)
        current_color = self.main_window.get_current_color()
        
        # For shape tools and move tool, we need to pass the layer instead of canvas
        if self.main_window.current_tool in ["line", "rectangle", "circle", "move", "selection"]:
            draw_layer = self.main_window._get_drawing_layer()
            if draw_layer:
                # Apply symmetry wrapper only for drawing tools
                target_layer = draw_layer
                if self.main_window.current_tool in ["line", "rectangle", "circle"]:
                    target_layer = SymmetryWrapper(draw_layer, self.main_window.canvas)
                    
                tool.on_mouse_up(target_layer, canvas_x, canvas_y, 1, current_color)
                self.main_window.layer_manager.invalidate_cache()  # Pixels finalized to layer
                self.main_window._update_canvas_from_layers()
        elif self.main_window.current_tool == "spray":
            # Stop spraying without calling tool.on_mouse_up (parity with brush/eraser)
            if hasattr(tool, 'is_spraying'):
                tool.is_spraying = False
        else:
            # Call tool's on_mouse_up method (standard interface)
            tool.on_mouse_up(self.main_window.canvas, canvas_x, canvas_y, 1, current_color)
        
        self.main_window.canvas_renderer.update_pixel_display()
        
        # Save drawing to current animation frame
        if hasattr(self.main_window, 'layer_anim_mgr'):
            self.main_window.layer_anim_mgr.save_canvas_to_current_frame()
        
        # Clear dragging state
        self.is_dragging = False
        self.last_canvas_x = None
        self.last_canvas_y = None
    
    def on_tkinter_canvas_right_click(self, event):
        """Handle right mouse button down on tkinter canvas.
        
        Defers between context menu (quick click+release) and camera pan
        (hold+drag). Edge tool and eraser have their own right-click 
        behaviour and bypass the pan/menu logic.
        """
        # Edge tool: immediate right-click action (no pan)
        if self.main_window.current_tool == "edge":
            canvas_x_float, canvas_y_float = self.main_window._tkinter_screen_to_canvas_coords_float(event.x, event.y)
            tool = self.main_window.tools.get("edge")
            if tool:
                current_color = self.main_window.get_current_color()
                tool.on_mouse_down(self.main_window.canvas, canvas_x_float, canvas_y_float, 3, current_color)
                self.main_window.canvas_renderer.update_pixel_display()
            return
        
        # Eraser tool: immediate right-click action (no pan)
        if self.main_window.current_tool == "eraser":
            canvas_x, canvas_y = self.main_window._tkinter_screen_to_canvas_coords(event.x, event.y)
            tool = self.main_window.tools.get("eraser")
            if tool:
                current_color = self.main_window.get_current_color()
                tool.on_mouse_down(self.main_window.canvas, canvas_x, canvas_y, 3, current_color)
                self.main_window.canvas_renderer.update_pixel_display()
            return
        
        # For all other tools: record start position; decide pan vs menu on release
        self._right_click_start_x = event.x
        self._right_click_start_y = event.y
        self._right_click_did_drag = False
        self.is_right_panning = False
        self._right_click_event = event  # Save for potential context menu
    
    def on_tkinter_canvas_mouse_drag(self, event):
        """Handle mouse drag on tkinter canvas"""
        # Handle pan tool drag (use raw screen coords!)
        if self.main_window.current_tool == "pan":
            tool = self.main_window.tools["pan"]
            result = tool.update_pan(event.x, event.y, self.main_window.canvas.zoom)
            if result is not None:
                temp_offset_x, temp_offset_y = result
                # Temporarily update display with new pan offset
                old_offset_x = self.main_window.pan_offset_x
                old_offset_y = self.main_window.pan_offset_y
                self.main_window.pan_offset_x = temp_offset_x
                self.main_window.pan_offset_y = temp_offset_y
                self.main_window.canvas_renderer.update_pixel_display()
                # Restore original offset (will be set permanently on mouse up)
                self.main_window.pan_offset_x = old_offset_x
                self.main_window.pan_offset_y = old_offset_y
            return
        
        # Handle scaling mode
        if self.main_window.selection_mgr.is_scaling and self.main_window.selection_mgr.scale_handle:
            canvas_x, canvas_y = self.main_window._tkinter_screen_to_canvas_coords(event.x, event.y)
            self.main_window.selection_mgr.update_scaling(canvas_x, canvas_y)
            return
        
        # Convert tkinter screen coordinates to canvas coordinates
        canvas_x, canvas_y = self.main_window._tkinter_screen_to_canvas_coords(event.x, event.y)
        
        # Check if we're in bounds
        if not (0 <= canvas_x < self.main_window.canvas.width and 0 <= canvas_y < self.main_window.canvas.height):
            return
        
        # Only process if we're dragging
        if not self.is_dragging:
            return
        
        # Get current tool
        tool = self.main_window.tools.get(self.main_window.current_tool)
        if not tool:
            return
        
        # Get current drawing color (from palette or color wheel based on view mode)
        current_color = self.main_window.get_current_color()
        
        # Handle all brush sizes consistently during drag
        if self.main_window.current_tool == "brush":
            draw_layer = self.main_window._get_drawing_layer()
            if draw_layer and hasattr(tool, 'is_drawing') and tool.is_drawing:
                target_layer = SymmetryWrapper(draw_layer, self.main_window.canvas)
                self.main_window.tool_size_mgr.draw_brush_at(target_layer, canvas_x, canvas_y, current_color)
                self.main_window.layer_manager.invalidate_cache()  # Pixels modified during drag
                self.main_window._update_canvas_from_layers()
                self.main_window.canvas_renderer.update_pixel_display()
            self.last_canvas_x = canvas_x
            self.last_canvas_y = canvas_y
            return
        elif self.main_window.current_tool == "eraser":
            # Handle eraser during drag
            draw_layer = self.main_window._get_drawing_layer()
            if draw_layer and hasattr(tool, 'is_erasing') and tool.is_erasing:
                target_layer = SymmetryWrapper(draw_layer, self.main_window.canvas)
                self.main_window.tool_size_mgr.erase_at(target_layer, canvas_x, canvas_y)
                self.main_window.layer_manager.invalidate_cache()  # Pixels modified during drag
                self.main_window._update_canvas_from_layers()
                self.main_window.canvas_renderer.update_pixel_display()
            self.last_canvas_x = canvas_x
            self.last_canvas_y = canvas_y
            return
        elif self.main_window.current_tool == "spray":
            draw_layer = self.main_window._get_drawing_layer()
            if draw_layer and hasattr(tool, 'is_spraying') and tool.is_spraying:
                target_layer = SymmetryWrapper(draw_layer, self.main_window.canvas)
                self.main_window.tool_size_mgr.spray_at(target_layer, canvas_x, canvas_y, current_color)
                self.main_window.layer_manager.invalidate_cache()  # Pixels modified during drag
                self.main_window._update_canvas_from_layers()
                self.main_window.canvas_renderer.update_pixel_display()
            self.last_canvas_x = canvas_x
            self.last_canvas_y = canvas_y
            return
        elif self.main_window.current_tool == "dither":
            draw_layer = self.main_window._get_drawing_layer()
            if draw_layer and hasattr(tool, 'is_drawing') and tool.is_drawing:
                target_layer = SymmetryWrapper(draw_layer, self.main_window.canvas)
                tool.on_mouse_move(target_layer, canvas_x, canvas_y, current_color)
                self.main_window.layer_manager.invalidate_cache()
                self.main_window._update_canvas_from_layers()
                self.main_window.canvas_renderer.update_pixel_display()
            self.last_canvas_x = canvas_x
            self.last_canvas_y = canvas_y
            return
        
        # Call tool's on_mouse_move method for drag
        # Handle edge tool with float precision coordinates
        if self.main_window.current_tool == "edge":
            # Convert to float coordinates for edge tool precision
            canvas_x_float, canvas_y_float = self.main_window._tkinter_screen_to_canvas_coords_float(event.x, event.y)
            tool.on_mouse_move(self.main_window.canvas, canvas_x_float, canvas_y_float, current_color)
        # For move and selection tools, use layer; for others, use canvas
        elif self.main_window.current_tool in ["move", "selection", "line", "rectangle", "circle"]:
            draw_layer = self.main_window._get_drawing_layer()
            if draw_layer:
                tool.on_mouse_move(draw_layer, canvas_x, canvas_y, current_color)
        else:
            tool.on_mouse_move(self.main_window.canvas, canvas_x, canvas_y, current_color)
        self.main_window.canvas_renderer.update_pixel_display()
        
        # Draw shape preview for shape tools during drag
        if self.main_window.current_tool in ["line", "rectangle", "circle"]:
            if hasattr(tool, 'is_drawing') and tool.is_drawing:
                self.main_window.canvas_renderer.draw_shape_preview(tool, canvas_x, canvas_y, current_color)
        
        # Update last position for interpolation
        self.last_canvas_x = canvas_x
        self.last_canvas_y = canvas_y
    
    def on_tkinter_canvas_mouse_move(self, event):
        """Handle mouse move on tkinter canvas (no button pressed)"""
        # Convert tkinter screen coordinates to canvas coordinates
        canvas_x, canvas_y = self.main_window._tkinter_screen_to_canvas_coords(event.x, event.y)
        
        # Check if we're in bounds
        if not (0 <= canvas_x < self.main_window.canvas.width and 0 <= canvas_y < self.main_window.canvas.height):
            # Clear any previews when mouse leaves canvas
            self.main_window.drawing_canvas.delete("brush_preview")
            self.main_window.drawing_canvas.delete("eraser_preview")
            self.main_window.drawing_canvas.delete("texture_preview")
            self.main_window.drawing_canvas.delete("edge_preview")
            # Reset cursor when leaving canvas bounds
            try:
                self.main_window.drawing_canvas.configure(cursor="arrow")
            except Exception:
                pass
            if hasattr(self.main_window, 'selection_mgr'):
                self.main_window.selection_mgr.copy_preview_pos = None  # Clear copy preview position
            # Reset throttler position tracking when leaving bounds
            self.canvas_optimizer.reset_position()
            return
        
        # Early exit using throttled position checking
        # This significantly reduces draw overhead for high-DPI displays or fast mouse movement
        if not self.canvas_optimizer.should_process_move(canvas_x, canvas_y):
            return
        
        # Update status bar cursor position
        if hasattr(self.main_window, '_update_status_bar'):
            self.main_window._update_status_bar(canvas_x, canvas_y)
        
        # Update copy preview position if in placement mode
        if hasattr(self.main_window, 'selection_mgr') and self.main_window.selection_mgr.is_placing_copy:
            self.main_window.selection_mgr.copy_preview_pos = (canvas_x, canvas_y)
            self.main_window.canvas_renderer.update_pixel_display()
            return

        # Cursor feedback for scaling handles on hover
        if hasattr(self.main_window, 'selection_mgr') and self.main_window.selection_mgr.is_scaling:
            selection_tool = self.main_window.tools.get("selection")
            if selection_tool and selection_tool.selection_rect:
                left, top, width, height = selection_tool.selection_rect
                handle = self.main_window.selection_mgr.get_scale_handle(canvas_x, canvas_y, left, top, width, height)
                try:
                    if handle:
                        # Show grab hand when over a grab-able scale handle/edge
                        self.main_window.drawing_canvas.configure(cursor="hand2")
                    else:
                        self.main_window.drawing_canvas.configure(cursor="arrow")
                except Exception:
                    pass
        
        # Show tool preview using canvas_renderer
        if self.main_window.current_tool == "brush":
            self.main_window.canvas_renderer.draw_brush_preview(canvas_x, canvas_y)
        elif self.main_window.current_tool == "eraser":
            self.main_window.canvas_renderer.draw_eraser_preview(canvas_x, canvas_y)
        elif self.main_window.current_tool == "spray":
            self.main_window.canvas_renderer.draw_spray_preview(canvas_x, canvas_y)
        elif self.main_window.current_tool == "dither":
            self.main_window.canvas_renderer.draw_dither_preview(canvas_x, canvas_y)
        elif self.main_window.current_tool == "edge":
            # Edge tool has its own preview system - call its on_mouse_move method
            canvas_x_float, canvas_y_float = self.main_window._tkinter_screen_to_canvas_coords_float(event.x, event.y)
            tool = self.main_window.tools.get("edge")
            if tool:
                current_color = self.main_window.get_current_color()
                tool.on_mouse_move(self.main_window.canvas, canvas_x_float, canvas_y_float, current_color)
        elif self.main_window.current_tool == "texture":
            texture_tool = self.main_window.tools.get("texture")
            if texture_tool:
                self.main_window.canvas_renderer.draw_texture_preview(texture_tool, canvas_x, canvas_y)
        elif self.main_window.current_tool in ["line", "rectangle", "circle"]:
            shape_tool = self.main_window.tools.get(self.main_window.current_tool)
            if shape_tool:
                current_color = self.main_window.get_current_color()
                self.main_window.canvas_renderer.draw_shape_preview(shape_tool, canvas_x, canvas_y, current_color)
        else:
            # Clear previews for other tools
            self.main_window.drawing_canvas.delete("brush_preview")
            self.main_window.drawing_canvas.delete("eraser_preview")
            self.main_window.drawing_canvas.delete("spray_preview")
            self.main_window.drawing_canvas.delete("texture_preview")
            self.main_window.drawing_canvas.delete("edge_preview")
            self.main_window.drawing_canvas.delete("shape_preview")
    
    def on_tkinter_canvas_right_drag(self, event):
        """Handle right-button drag on canvas.
        
        For edge/eraser tools: continuous erase action.
        For all other tools: once drag exceeds threshold, start camera pan.
        """
        # Edge tool: continuous erase on right-drag
        if self.main_window.current_tool == "edge":
            tool = self.main_window.tools.get("edge")
            if not tool:
                return
            canvas_x_float, canvas_y_float = self.main_window._tkinter_screen_to_canvas_coords_float(event.x, event.y)
            current_color = self.main_window.get_current_color()
            tool.on_mouse_move(self.main_window.canvas, canvas_x_float, canvas_y_float, current_color)
            tool.on_mouse_down(self.main_window.canvas, canvas_x_float, canvas_y_float, 3, current_color)
            self.main_window.canvas_renderer.update_pixel_display()
            return
        
        # Eraser tool: continuous erase on right-drag
        if self.main_window.current_tool == "eraser":
            tool = self.main_window.tools.get("eraser")
            if not tool:
                return
            canvas_x, canvas_y = self.main_window._tkinter_screen_to_canvas_coords(event.x, event.y)
            current_color = self.main_window.get_current_color()
            tool.on_right_drag(self.main_window.canvas, canvas_x, canvas_y, current_color)
            self.main_window.canvas_renderer.update_pixel_display()
            return
        
        # --- Right-click pan logic for all other tools ---
        dx = event.x - self._right_click_start_x
        dy = event.y - self._right_click_start_y
        
        # Check if drag exceeds threshold to begin panning
        if not self._right_click_did_drag:
            if abs(dx) > self._RIGHT_CLICK_DRAG_THRESHOLD or abs(dy) > self._RIGHT_CLICK_DRAG_THRESHOLD:
                self._right_click_did_drag = True
                self.is_right_panning = True
                # Initialize pan tool with the starting position
                if "pan" in self.main_window.tools:
                    tool = self.main_window.tools["pan"]
                    tool.start_pan(self._right_click_start_x, self._right_click_start_y,
                                   self.main_window.pan_offset_x, self.main_window.pan_offset_y)
                    try:
                        self.main_window.drawing_canvas.configure(cursor="fleur")
                    except Exception:
                        pass
        
        # If panning, update the pan
        if self.is_right_panning and "pan" in self.main_window.tools:
            tool = self.main_window.tools["pan"]
            result = tool.update_pan(event.x, event.y, self.main_window.canvas.zoom)
            if result is not None:
                old_x = self.main_window.pan_offset_x
                old_y = self.main_window.pan_offset_y
                self.main_window.pan_offset_x, self.main_window.pan_offset_y = result
                self.main_window.canvas_renderer.update_pixel_display()
                self.main_window.pan_offset_x = old_x
                self.main_window.pan_offset_y = old_y

    def on_tkinter_canvas_right_up(self, event):
        """Handle right-button release on canvas.
        
        For edge/eraser tools: finalize erase action.
        For all other tools: if no drag occurred, show context menu.
        If we were panning, finalize the pan.
        """
        # Edge tool: finalize erase
        if self.main_window.current_tool == "edge":
            tool = self.main_window.tools.get("edge")
            if not tool:
                return
            canvas_x, canvas_y = self.main_window._tkinter_screen_to_canvas_coords(event.x, event.y)
            current_color = self.main_window.get_current_color()
            tool.on_mouse_up(self.main_window.canvas, canvas_x, canvas_y, 3, current_color)
            self.main_window.canvas_renderer.update_pixel_display()
            if hasattr(self.main_window, 'layer_anim_mgr'):
                self.main_window.layer_anim_mgr.save_canvas_to_current_frame()
            return
        
        # Eraser tool: finalize erase
        if self.main_window.current_tool == "eraser":
            tool = self.main_window.tools.get("eraser")
            if not tool:
                return
            canvas_x, canvas_y = self.main_window._tkinter_screen_to_canvas_coords(event.x, event.y)
            current_color = self.main_window.get_current_color()
            tool.on_mouse_up(self.main_window.canvas, canvas_x, canvas_y, 3, current_color)
            self.main_window.canvas_renderer.update_pixel_display()
            if hasattr(self.main_window, 'layer_anim_mgr'):
                self.main_window.layer_anim_mgr.save_canvas_to_current_frame()
            return
        
        # --- Right-click pan/menu logic ---
        if self.is_right_panning:
            # Finalize the pan (permanently apply offset)
            if "pan" in self.main_window.tools:
                tool = self.main_window.tools["pan"]
                result = tool.update_pan(event.x, event.y, self.main_window.canvas.zoom)
                if result is not None:
                    self.main_window.pan_offset_x, self.main_window.pan_offset_y = result
                tool.end_pan()
                self.main_window.canvas_renderer.update_pixel_display()
            
            # Restore cursor
            try:
                self.main_window.drawing_canvas.configure(cursor="arrow")
            except Exception:
                pass
            
            self.is_right_panning = False
            self._right_click_did_drag = False
        else:
            # No drag occurred — show context menu
            if hasattr(self.main_window, 'context_menu_mgr'):
                self.main_window.context_menu_mgr.show_canvas_context_menu(event)
            self._right_click_did_drag = False
    
    # ==================== UI Callback Events ====================
    
    def on_selection_complete(self):
        """Called when selection is complete - auto-switch to move tool"""
        # Automatically switch to move tool after selection
        self.main_window._select_tool("move")
    
    def on_size_change(self, size_str: str):
        """Handle canvas size change from dropdown"""
        self.main_window._on_size_change(size_str)
    
    def on_zoom_change(self, zoom_str: str):
        """Handle zoom level change from dropdown"""
        self.main_window._on_zoom_change(zoom_str)
    
    def on_palette_change(self, palette_name: str):
        """Handle palette change from dropdown"""
        self.main_window._on_palette_change(palette_name)
    
    def on_view_mode_change(self):
        """Handle view mode change (Grid/Primary/Wheel/etc)"""
        self.main_window._on_view_mode_change()
    
    def on_color_wheel_changed(self, rgb_color):
        """Handle color change from color wheel"""
        self.main_window._on_color_wheel_changed(rgb_color)
    
    def on_theme_selected(self, theme_name: str):
        """Handle theme selection from dropdown"""
        self.main_window._on_theme_selected(theme_name)
    
    def on_layer_changed(self):
        """Handle layer change event"""
        self.main_window._on_layer_changed()
    
    def on_frame_changed(self):
        """Handle animation frame change event"""
        self.main_window._on_frame_changed()

