"""
Selection Manager for Pixel Perfect
Handles all selection transformation operations (mirror, rotate, scale, copy)

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import numpy as np


class SelectionManager:
    """Manages selection transformation operations"""
    
    def __init__(self, canvas, layer_manager, tools, theme_manager):
        """
        Initialize the SelectionManager.
        
        Args:
            canvas: The canvas object
            layer_manager: The layer manager object
            tools: Dictionary of tool objects
            theme_manager: The theme manager object
        """
        self.canvas = canvas
        self.layer_manager = layer_manager
        self.tools = tools
        self.theme_manager = theme_manager
        
        # State variables for scaling
        self.is_scaling = False
        self.scale_handle = None
        self.scale_original_rect = None
        self.scale_true_original_rect = None
        self.scale_is_dragging = False
        
        # State variables for copy/paste
        self.copy_buffer = None
        self.copy_dimensions = None
        self.is_placing_copy = False
        
        # Callbacks (set by main_window after init)
        self.update_canvas_callback = None
        self.update_display_callback = None
        self.select_tool_callback = None
        self.update_tool_selection_callback = None
        self.get_drawing_layer_callback = None
        
        # Widget references (set after UI creation)
        self.drawing_canvas = None
        self.scale_btn = None
        self.tool_buttons = None
    
    def on_selection_complete(self):
        """Called when selection is complete - auto-switch to move tool"""
        if self.select_tool_callback:
            self.select_tool_callback("move")
    
    def mirror_selection(self):
        """Mirror (flip horizontally) the selected pixels"""
        # Exit scaling mode if active
        if self.is_scaling:
            self.is_scaling = False
            self.scale_handle = None
            self.scale_original_rect = None
            self.scale_true_original_rect = None
            self.scale_is_dragging = False
            self.scale_btn.configure(fg_color=self.theme_manager.get_current_theme().button_normal)
            if self.update_tool_selection_callback:
                self.update_tool_selection_callback()
        
        selection_tool = self.tools.get("selection")
        if not selection_tool or not selection_tool.has_active_selection():
            return
        
        # Get selection data
        if selection_tool.selected_pixels is None:
            return
        
        bounds = selection_tool.get_selection_bounds()
        if not bounds:
            return
        
        left, top, width, height = bounds
        
        # CRITICAL FIX: Finalize move operation to prevent background restoration
        move_tool = self.tools.get("move")
        if move_tool:
            draw_layer = self._get_drawing_layer()
            if draw_layer:
                move_tool.finalize_move(draw_layer)
            print("[MIRROR] Finalized move operation to prevent copy-behind bug")
        
        # Mirror the pixels horizontally (flip left-right)
        mirrored_pixels = np.flip(selection_tool.selected_pixels, axis=1).copy()
        
        # Update the selection with mirrored pixels
        selection_tool.selected_pixels = mirrored_pixels
        
        # Redraw on canvas
        draw_layer = self._get_drawing_layer()
        if draw_layer:
            for py in range(height):
                for px in range(width):
                    if py < mirrored_pixels.shape[0] and px < mirrored_pixels.shape[1]:
                        pixel_color = tuple(mirrored_pixels[py, px])
                        canvas_x = left + px
                        canvas_y = top + py
                        if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                            draw_layer.set_pixel(canvas_x, canvas_y, pixel_color)
            
            # Update canvas display
            if self.update_canvas_callback:
                self.update_canvas_callback()
            if self.update_display_callback:
                self.update_display_callback()
    
    def rotate_selection(self):
        """Rotate the selected pixels 90 degrees clockwise"""
        # Exit scaling mode if active
        if self.is_scaling:
            self.is_scaling = False
            self.scale_handle = None
            self.scale_original_rect = None
            self.scale_true_original_rect = None
            self.scale_is_dragging = False
            self.scale_btn.configure(fg_color=self.theme_manager.get_current_theme().button_normal)
            if self.update_tool_selection_callback:
                self.update_tool_selection_callback()
        
        selection_tool = self.tools.get("selection")
        if not selection_tool or not selection_tool.has_active_selection():
            return
        
        # Get selection data
        if selection_tool.selected_pixels is None:
            return
        
        bounds = selection_tool.get_selection_bounds()
        if not bounds:
            return
        
        left, top, width, height = bounds
        
        # CRITICAL FIX: Finalize move operation to prevent background restoration
        move_tool = self.tools.get("move")
        if move_tool:
            draw_layer = self._get_drawing_layer()
            if draw_layer:
                move_tool.finalize_move(draw_layer)
            print("[ROTATE] Finalized move operation to prevent copy-behind bug")
        
        # Rotate 90 degrees clockwise: transpose then flip horizontally
        rotated_pixels = np.rot90(selection_tool.selected_pixels, k=-1).copy()
        
        # Update the selection with rotated pixels
        selection_tool.selected_pixels = rotated_pixels
        
        # Note: rotation changes dimensions (width becomes height, height becomes width)
        new_width = rotated_pixels.shape[1]
        new_height = rotated_pixels.shape[0]
        
        # Update selection rectangle with new dimensions
        selection_tool.selection_rect = (left, top, new_width, new_height)
        
        # Clear old area
        draw_layer = self._get_drawing_layer()
        if draw_layer:
            # Clear original area
            for py in range(height):
                for px in range(width):
                    canvas_x = left + px
                    canvas_y = top + py
                    if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                        draw_layer.set_pixel(canvas_x, canvas_y, (0, 0, 0, 0))
            
            # Draw rotated pixels
            for py in range(new_height):
                for px in range(new_width):
                    if py < rotated_pixels.shape[0] and px < rotated_pixels.shape[1]:
                        pixel_color = tuple(rotated_pixels[py, px])
                        canvas_x = left + px
                        canvas_y = top + py
                        if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                            if pixel_color[3] > 0:  # Only draw non-transparent pixels
                                draw_layer.set_pixel(canvas_x, canvas_y, pixel_color)
            
            # Update canvas display
            if self.update_canvas_callback:
                self.update_canvas_callback()
            if self.update_display_callback:
                self.update_display_callback()
    
    def copy_selection(self):
        """Enter copy mode - allows placing a copy of the selection"""
        # Exit scaling mode if active
        if self.is_scaling:
            self.is_scaling = False
            self.scale_handle = None
            self.scale_original_rect = None
            self.scale_true_original_rect = None
            self.scale_is_dragging = False
            self.scale_btn.configure(fg_color=self.theme_manager.get_current_theme().button_normal)
            if self.update_tool_selection_callback:
                self.update_tool_selection_callback()
        
        selection_tool = self.tools.get("selection")
        if not selection_tool or not selection_tool.has_active_selection():
            return
        
        # Get selection data
        if selection_tool.selected_pixels is None:
            return
        
        # CRITICAL FIX: Finalize move operation to prevent background restoration
        move_tool = self.tools.get("move")
        if move_tool:
            draw_layer = self._get_drawing_layer()
            if draw_layer:
                move_tool.finalize_move(draw_layer)
            print("[COPY] Finalized move operation to prevent copy-behind bug")
        
        # Store copy data
        self.copy_buffer = selection_tool.selected_pixels.copy()
        bounds = selection_tool.get_selection_bounds()
        if bounds:
            _, _, width, height = bounds
            self.copy_dimensions = (width, height)
            
            # Switch to a placement mode
            self.is_placing_copy = True
    
    def scale_selection(self):
        """Enter scaling mode for the selection"""
        selection_tool = self.tools.get("selection")
        if not selection_tool or not selection_tool.has_active_selection():
            return
        
        bounds = selection_tool.get_selection_bounds()
        if not bounds:
            return
        
        # Enter scaling mode
        self.is_scaling = True
        self.scale_original_rect = bounds  # Reference for calculating deltas
        self.scale_true_original_rect = bounds  # Never changes - for final apply
        
        # Change cursor to arrow for grabbing handles
        if self.drawing_canvas:
            self.drawing_canvas.configure(cursor="arrow")
        
        # Update button states - deselect tool buttons, highlight Scale button
        if self.tool_buttons:
            for tool_id, btn in self.tool_buttons.items():
                btn.configure(fg_color=self.theme_manager.get_current_theme().button_normal)
        if self.scale_btn:
            self.scale_btn.configure(fg_color="blue")
        
        # Update display to show handles
        if self.update_display_callback:
            self.update_display_callback()
    
    def apply_scale(self, new_rect):
        """Apply scaling to the selection"""
        selection_tool = self.tools.get("selection")
        if not selection_tool or selection_tool.selected_pixels is None:
            return
        
        # CRITICAL FIX: Finalize move operation to prevent background restoration
        move_tool = self.tools.get("move")
        if move_tool:
            draw_layer = self._get_drawing_layer()
            if draw_layer:
                move_tool.finalize_move(draw_layer)
            print("[SCALE] Finalized move operation to prevent copy-behind bug")
        
        # Use the TRUE original rect (from when we entered scale mode)
        old_left, old_top, old_width, old_height = self.scale_true_original_rect
        new_left, new_top, new_width, new_height = new_rect
        
        # Ensure minimum size
        if new_width < 1 or new_height < 1:
            return
        
        # Scale the pixels using nearest neighbor
        self._simple_scale(selection_tool, old_width, old_height, new_width, new_height, new_left, new_top)
    
    def place_copy_at(self, canvas_x: int, canvas_y: int):
        """Place the copied pixels at the specified position"""
        if self.copy_buffer is None or self.copy_dimensions is None:
            return
        
        width, height = self.copy_dimensions
        
        # Place pixels
        draw_layer = self._get_drawing_layer()
        if draw_layer:
            for py in range(height):
                for px in range(width):
                    if py < self.copy_buffer.shape[0] and px < self.copy_buffer.shape[1]:
                        pixel_color = tuple(self.copy_buffer[py, px])
                        dest_x = canvas_x + px
                        dest_y = canvas_y + py
                        if 0 <= dest_x < self.canvas.width and 0 <= dest_y < self.canvas.height:
                            # Only draw non-transparent pixels
                            if pixel_color[3] > 0:
                                draw_layer.set_pixel(dest_x, dest_y, pixel_color)
            
            # Update canvas display
            if self.update_canvas_callback:
                self.update_canvas_callback()
            if self.update_display_callback:
                self.update_display_callback()
        
        # Exit placement mode
        self.is_placing_copy = False
    
    def get_scale_handle(self, x: int, y: int, left: int, top: int, width: int, height: int):
        """Detect which scale handle/edge the user clicked near"""
        handle_tolerance = max(3, 8 // self.canvas.zoom)  # Adjust based on zoom
        
        right = left + width
        bottom = top + height
        
        # Check corners first (higher priority)
        if abs(x - left) <= handle_tolerance and abs(y - top) <= handle_tolerance:
            return "tl"  # Top-left
        if abs(x - right) <= handle_tolerance and abs(y - top) <= handle_tolerance:
            return "tr"  # Top-right
        if abs(x - left) <= handle_tolerance and abs(y - bottom) <= handle_tolerance:
            return "bl"  # Bottom-left
        if abs(x - right) <= handle_tolerance and abs(y - bottom) <= handle_tolerance:
            return "br"  # Bottom-right
        
        # Check edges
        if abs(x - left) <= handle_tolerance and top <= y <= bottom:
            return "l"  # Left edge
        if abs(x - right) <= handle_tolerance and top <= y <= bottom:
            return "r"  # Right edge
        if abs(y - top) <= handle_tolerance and left <= x <= right:
            return "t"  # Top edge
        if abs(y - bottom) <= handle_tolerance and left <= x <= right:
            return "b"  # Bottom edge
        
        return None
    
    def draw_scale_handle(self, x: float, y: float, size: int, color: str):
        """Draw a scale handle on the canvas"""
        if not self.drawing_canvas:
            return
        
        half_size = size / 2
        self.drawing_canvas.create_rectangle(
            x - half_size, y - half_size,
            x + half_size, y + half_size,
            fill=color,
            outline="black",
            width=1,
            tags="selection"
        )
    
    def preview_scaled_pixels(self, selection_tool, old_width, old_height, new_width, new_height, new_left, new_top):
        """Show a live preview of scaled pixels during drag (doesn't modify stored data)"""
        # Quick nearest-neighbor scaling for preview
        preview_pixels = np.zeros((new_height, new_width, 4), dtype=np.uint8)
        
        for ny in range(new_height):
            for nx in range(new_width):
                # Map to original coordinates
                ox = int(nx * old_width / new_width)
                oy = int(ny * old_height / new_height)
                if oy < selection_tool.selected_pixels.shape[0] and ox < selection_tool.selected_pixels.shape[1]:
                    preview_pixels[ny, nx] = selection_tool.selected_pixels[oy, ox]
        
        # Temporarily draw the preview on canvas
        draw_layer = self._get_drawing_layer()
        if draw_layer:
            # Clear the TRUE original area (where pixels actually were)
            true_orig_left, true_orig_top, true_orig_width, true_orig_height = self.scale_true_original_rect
            for py in range(true_orig_height):
                for px in range(true_orig_width):
                    canvas_x = true_orig_left + px
                    canvas_y = true_orig_top + py
                    if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                        draw_layer.set_pixel(canvas_x, canvas_y, (0, 0, 0, 0))
            
            # Draw the scaled preview
            for py in range(new_height):
                for px in range(new_width):
                    pixel_color = tuple(preview_pixels[py, px])
                    canvas_x = new_left + px
                    canvas_y = new_top + py
                    if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                        if pixel_color[3] > 0:
                            draw_layer.set_pixel(canvas_x, canvas_y, pixel_color)
            
            if self.update_canvas_callback:
                self.update_canvas_callback()
            if self.update_display_callback:
                self.update_display_callback()
    
    def _simple_scale(self, selection_tool, old_width, old_height, new_width, new_height, new_left, new_top):
        """Simple scaling without scipy"""
        scaled_pixels = np.zeros((new_height, new_width, 4), dtype=np.uint8)
        
        for ny in range(new_height):
            for nx in range(new_width):
                # Map to original coordinates
                ox = int(nx * old_width / new_width)
                oy = int(ny * old_height / new_height)
                if oy < selection_tool.selected_pixels.shape[0] and ox < selection_tool.selected_pixels.shape[1]:
                    scaled_pixels[ny, nx] = selection_tool.selected_pixels[oy, ox]
        
        selection_tool.selected_pixels = scaled_pixels
        selection_tool.selection_rect = (new_left, new_top, new_width, new_height)
        
        # Redraw
        draw_layer = self._get_drawing_layer()
        if draw_layer:
            for py in range(new_height):
                for px in range(new_width):
                    pixel_color = tuple(scaled_pixels[py, px])
                    canvas_x = new_left + px
                    canvas_y = new_top + py
                    if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                        if pixel_color[3] > 0:
                            draw_layer.set_pixel(canvas_x, canvas_y, pixel_color)
            
            if self.update_canvas_callback:
                self.update_canvas_callback()
            if self.update_display_callback:
                self.update_display_callback()
    
    def _get_drawing_layer(self):
        """Get the layer to draw on (via callback or layer manager)"""
        if self.get_drawing_layer_callback:
            return self.get_drawing_layer_callback()
        
        # Fallback: get from layer_manager directly
        active_layer = self.layer_manager.get_active_layer()
        if active_layer is None:
            # No layer selected - find topmost visible layer
            for i in range(len(self.layer_manager.layers) - 1, -1, -1):
                layer = self.layer_manager.layers[i]
                if layer.visible:
                    return layer
        return active_layer
    
    def update_scaling(self, mouse_x: int, mouse_y: int):
        """Update scaling during mouse drag"""
        if not self.is_scaling or not self.scale_handle:
            return
        
        selection_tool = self.tools.get("selection")
        if not selection_tool or not selection_tool.selection_rect:
            return
        
        left, top, width, height = self.scale_original_rect
        
        # Calculate new rectangle based on handle being dragged
        new_left, new_top, new_width, new_height = left, top, width, height
        
        if self.scale_handle == "tl":  # Top-left corner - move top-left
            new_width = width + (left - mouse_x)
            new_height = height + (top - mouse_y)
            new_left = mouse_x
            new_top = mouse_y
        elif self.scale_handle == "tr":  # Top-right corner - move top-right
            new_width = mouse_x - left
            new_height = height + (top - mouse_y)
            new_top = mouse_y
        elif self.scale_handle == "bl":  # Bottom-left corner - move bottom-left
            new_width = width + (left - mouse_x)
            new_height = mouse_y - top
            new_left = mouse_x
        elif self.scale_handle == "br":  # Bottom-right corner - move bottom-right
            new_width = mouse_x - left
            new_height = mouse_y - top
        elif self.scale_handle == "t":  # Top edge - resize from bottom
            new_height = height + (top - mouse_y)
            new_top = mouse_y
        elif self.scale_handle == "b":  # Bottom edge - resize from top
            new_height = mouse_y - top
        elif self.scale_handle == "l":  # Left edge - resize from right
            new_width = width + (left - mouse_x)
            new_left = mouse_x
        elif self.scale_handle == "r":  # Right edge - resize from left
            new_width = mouse_x - left
        
        # Ensure minimum size
        if new_width < 1:
            new_width = 1
        if new_height < 1:
            new_height = 1
        
        # Update the selection rectangle for preview
        selection_tool.selection_rect = (new_left, new_top, new_width, new_height)
        
        # Update display
        if self.update_display_callback:
            self.update_display_callback()

