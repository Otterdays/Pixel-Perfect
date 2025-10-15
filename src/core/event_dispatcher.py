"""
Event Dispatcher for Pixel Perfect
Handles all keyboard, mouse, and window events
"""

from typing import Callable, Dict, Any, Optional, Tuple
import tkinter as tk


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
            self.main_window.drawing_canvas.bind("<Motion>", self.on_tkinter_canvas_mouse_move)
    
    # ==================== Window & Panel Events ====================
    
    def on_sash_drag_start(self, event):
        """Called when user starts dragging panel divider"""
        self.main_window.window_state_manager.is_resizing_panels = True
    
    def on_sash_drag_end(self, event):
        """Called when user stops dragging panel divider"""
        self.main_window.window_state_manager.is_resizing_panels = False
        self.main_window.window_state_manager.save_state()
    
    def on_window_resize(self, event):
        """Handle window resize events"""
        # Only handle resize events for the root window
        if event.widget == self.main_window.root:
            # Save window state after resize
            if hasattr(self.main_window, 'window_state_manager'):
                self.main_window.window_state_manager.save_state()
            
            # Update grid centering if canvas exists
            if hasattr(self.main_window, 'canvas') and self.main_window.canvas:
                # Trigger a redraw to recenter the grid
                if hasattr(self.main_window, 'canvas_renderer'):
                    self.main_window.canvas_renderer.update_pixel_display()
    
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
            self.main_window.new_project()
            return
        
        # Handle rotation preview mode
        if hasattr(self.main_window, 'selection_mgr'):
            if event.keysym.lower() == 'return':  # Enter key - apply rotation
                if self.main_window.selection_mgr.is_rotating:
                    self.main_window.selection_mgr.apply_rotation()
                    return
            elif event.keysym.lower() == 'escape':  # Escape key - cancel rotation
                if self.main_window.selection_mgr.is_rotating:
                    self.main_window.selection_mgr.cancel_rotation()
                    return
        
        # Ctrl+E for export
        if event.state & 0x4 and event.keysym.lower() == 'e':
            self.main_window.export_png()
            return
        
        # Tool shortcuts (B, E, F, D, S, L, Q, C, P, M, R, T, X)
        if not (event.state & 0x4):  # No Ctrl modifier
            key = event.keysym.lower()
            tool_map = {
                'b': 'brush',
                'e': 'eraser',
                'f': 'fill',
                'd': 'eyedropper',
                's': 'selection',
                'l': 'line',
                'q': 'square',
                'c': 'circle',
                'p': 'pan',
                'm': 'move',
                'r': 'rotate',
                't': 'texture'
            }
            
            if key in tool_map:
                self.main_window._select_tool(tool_map[key])
                return
            
            # X for swap colors
            if key == 'x':
                self.main_window.swap_colors()
                return
    
    # ==================== Mouse Events (Canvas) ====================
    
    def on_tkinter_canvas_mouse_down(self, event):
        """Handle mouse down on tkinter canvas"""
        # Clear any tool previews when starting to draw
        self.main_window.drawing_canvas.delete("brush_preview")
        self.main_window.drawing_canvas.delete("eraser_preview")
        self.main_window.drawing_canvas.delete("texture_preview")
        
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
                self.main_window.selection_mgr.place_copy_at(canvas_x, canvas_y)
            return
        
        # Handle rotation preview mode - commit if clicking outside selection
        if self.main_window.selection_mgr.is_rotating:
            selection_tool = self.main_window.tools.get("selection")
            if selection_tool and selection_tool.selection_rect:
                left, top, width, height = selection_tool.selection_rect
                # Check if click is outside selection bounds
                if not (left <= canvas_x < left + width and top <= canvas_y < top + height):
                    # Click outside selection - commit the rotation
                    self.main_window.selection_mgr.apply_rotation()
                    return
        
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
        if self.main_window.current_tool in ["brush", "eraser", "fill", "texture", "line", "rectangle", "circle"]:
            active_layer = self.main_window.layer_manager.get_active_layer()
            if active_layer:
                self.main_window.undo_manager.save_state(active_layer.pixels.copy(), self.main_window.layer_manager.active_layer_index)
        
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
        
        # Handle all brush sizes consistently
        if self.main_window.current_tool == "brush":
            draw_layer = self.main_window._get_drawing_layer()
            if draw_layer:
                self.main_window.tool_size_mgr.draw_brush_at(draw_layer, canvas_x, canvas_y, current_color)
                self.main_window._update_canvas_from_layers()
                self.main_window.canvas_renderer.update_pixel_display()
            if hasattr(tool, 'is_drawing'):
                tool.is_drawing = True  # Set drawing state
            return
        elif self.main_window.current_tool == "eraser":
            draw_layer = self.main_window._get_drawing_layer()
            if draw_layer:
                self.main_window.tool_size_mgr.erase_at(draw_layer, canvas_x, canvas_y)
                self.main_window._update_canvas_from_layers()
                self.main_window.canvas_renderer.update_pixel_display()
            if hasattr(tool, 'is_erasing'):
                tool.is_erasing = True  # Set erasing state
        elif self.main_window.current_tool in ["fill", "texture", "line", "rectangle", "circle", "move", "selection"]:
            # Handle fill, texture, shape, move, and selection tools with layer-based approach
            draw_layer = self.main_window._get_drawing_layer()
            if draw_layer:
                tool.on_mouse_down(draw_layer, canvas_x, canvas_y, 1, current_color)
                if self.main_window.current_tool in ["fill", "texture"]:
                    # Fill and texture tools update immediately
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
                tool.on_mouse_up(draw_layer, canvas_x, canvas_y, 1, current_color)
                self.main_window._update_canvas_from_layers()
        else:
            # Call tool's on_mouse_up method (standard interface)
            tool.on_mouse_up(self.main_window.canvas, canvas_x, canvas_y, 1, current_color)
        
        self.main_window.canvas_renderer.update_pixel_display()
        
        # Clear dragging state
        self.is_dragging = False
        self.last_canvas_x = None
        self.last_canvas_y = None
    
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
                self.main_window.tool_size_mgr.draw_brush_at(draw_layer, canvas_x, canvas_y, current_color)
                self.main_window._update_canvas_from_layers()
                self.main_window.canvas_renderer.update_pixel_display()
            self.last_canvas_x = canvas_x
            self.last_canvas_y = canvas_y
            return
        elif self.main_window.current_tool == "eraser":
            # Handle eraser during drag
            draw_layer = self.main_window._get_drawing_layer()
            if draw_layer and hasattr(tool, 'is_erasing') and tool.is_erasing:
                self.main_window.tool_size_mgr.erase_at(draw_layer, canvas_x, canvas_y)
                self.main_window._update_canvas_from_layers()
                self.main_window.canvas_renderer.update_pixel_display()
            self.last_canvas_x = canvas_x
            self.last_canvas_y = canvas_y
            return
        
        # Call tool's on_mouse_move method for drag
        # For move and selection tools, use layer; for others, use canvas
        if self.main_window.current_tool in ["move", "selection", "line", "rectangle", "circle"]:
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
            if hasattr(self.main_window, 'selection_mgr'):
                self.main_window.selection_mgr.copy_preview_pos = None  # Clear copy preview position
            return
        
        # Update copy preview position if in placement mode
        if hasattr(self.main_window, 'selection_mgr') and self.main_window.selection_mgr.is_placing_copy:
            self.main_window.selection_mgr.copy_preview_pos = (canvas_x, canvas_y)
            self.main_window.canvas_renderer.update_pixel_display()
            return
        
        # Show tool preview using canvas_renderer
        if self.main_window.current_tool == "brush":
            self.main_window.canvas_renderer.draw_brush_preview(canvas_x, canvas_y)
        elif self.main_window.current_tool == "eraser":
            self.main_window.canvas_renderer.draw_eraser_preview(canvas_x, canvas_y)
        elif self.main_window.current_tool == "texture":
            texture_tool = self.main_window.tools.get("texture")
            if texture_tool:
                self.main_window.canvas_renderer.draw_texture_preview(texture_tool, canvas_x, canvas_y)
        elif self.main_window.current_tool in ["line", "rectangle", "circle"]:
            shape_tool = self.main_window.tools.get(self.main_window.current_tool)
            if shape_tool:
                current_color = self.main_window.palette.get_primary_color()
                self.main_window.canvas_renderer.draw_shape_preview(shape_tool, canvas_x, canvas_y, current_color)
        else:
            # Clear previews for other tools
            self.main_window.drawing_canvas.delete("brush_preview")
            self.main_window.drawing_canvas.delete("eraser_preview")
            self.main_window.drawing_canvas.delete("texture_preview")
            self.main_window.drawing_canvas.delete("shape_preview")
    
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

