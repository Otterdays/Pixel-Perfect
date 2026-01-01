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
        
        # State variables for rotation/mirror preview
        self.is_rotating = False
        self.is_mirroring = False
        self.original_pixels_backup = None
        self.original_rect_backup = None
        self.rotated_pixels_preview = None
        
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
        
        # Prepare background so transform replaces the previous drop
        # rather than stacking duplicates. This restores the last drop's
        # background on the layer, then snapshots a fresh background so the
        # next pickup can restore correctly.
        self._restore_and_prepare_move_background(left, top, width, height)
        
        # Mirror the pixels horizontally (flip left-right)
        mirrored_pixels = np.flip(selection_tool.selected_pixels, axis=1).copy()
        
        # Update the selection with mirrored pixels
        selection_tool.selected_pixels = mirrored_pixels
        
        # Update the layer data with mirrored pixels - only non-transparent pixels
        draw_layer = self._get_drawing_layer()
        if draw_layer:
            # Find non-transparent pixels using NumPy
            non_transparent = mirrored_pixels[:, :, 3] > 0
            y_coords, x_coords = np.where(non_transparent)
            
            for i in range(len(y_coords)):
                py, px = y_coords[i], x_coords[i]
                pixel_color = tuple(mirrored_pixels[py, px])
                canvas_x = left + px
                canvas_y = top + py
                if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                    draw_layer.set_pixel(canvas_x, canvas_y, pixel_color)
            
            # Update canvas from layers (this will show the mirrored pixels)
            if self.update_canvas_callback:
                self.update_canvas_callback()
            if self.update_display_callback:
                self.update_display_callback()
    
    def rotate_selection(self):
        """Rotate the selected pixels 90 degrees clockwise (preview mode)"""
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
        
        # Prepare background and state like mirror does so transforms don't stack
        # on top of the last drop and the next pickup restores correctly.
        self._restore_and_prepare_move_background(left, top, width, height)
        
        # Enter rotation preview mode
        self.is_rotating = True
        self.is_mirroring = False  # Exit mirror mode if active
        
        # Backup original pixels and rect
        self.original_pixels_backup = selection_tool.selected_pixels.copy()
        self.original_rect_backup = selection_tool.selection_rect  # Tuple doesn't need .copy()
        
        # Rotate 90 degrees clockwise: transpose then flip horizontally
        rotated_pixels = np.rot90(selection_tool.selected_pixels, k=-1).copy()
        
        # Store rotated pixels separately for preview (don't modify selected_pixels yet)
        self.rotated_pixels_preview = rotated_pixels
        
        # Note: rotation changes dimensions (width becomes height, height becomes width)
        new_width = rotated_pixels.shape[1]
        new_height = rotated_pixels.shape[0]
        
        # Update selection rectangle with new dimensions for preview
        selection_tool.selection_rect = (left, top, new_width, new_height)
        
        # Update display to show preview
        if self.update_display_callback:
            self.update_display_callback()
    
    def apply_rotation(self):
        """Apply the current rotation preview to the layer"""
        if not self.is_rotating:
            return
        
        selection_tool = self.tools.get("selection")
        if not selection_tool or selection_tool.selected_pixels is None:
            return
        
        bounds = selection_tool.get_selection_bounds()
        if not bounds:
            return
        
        left, top, width, height = bounds
        
        # Apply rotation to the layer
        draw_layer = self._get_drawing_layer()
        if draw_layer and self.rotated_pixels_preview is not None:
            # If the user had previously dropped the selection (move tool active),
            # restore that area's background first to avoid stacking duplicates.
            # Otherwise (no prior move), fall back to clearing the original area.
            move_tool = self.tools.get("move")
            had_prior_drop = bool(move_tool and move_tool.last_drawn_position)
            if had_prior_drop:
                self._restore_and_prepare_move_background(left, top, width, height)
            else:
                # No prior drop to restore; clear original area where needed
                orig_left, orig_top, orig_width, orig_height = self.original_rect_backup
                # Find non-transparent pixels in original backup
                non_transparent_orig = self.original_pixels_backup[:, :, 3] > 0
                y_coords, x_coords = np.where(non_transparent_orig)
                
                for i in range(len(y_coords)):
                    py, px = y_coords[i], x_coords[i]
                    canvas_x = orig_left + px
                    canvas_y = orig_top + py
                    if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                        draw_layer.set_pixel(canvas_x, canvas_y, (0, 0, 0, 0))
            
            # Draw rotated pixels from preview - only non-transparent
            rotated_pixels = self.rotated_pixels_preview
            new_width = rotated_pixels.shape[1]
            new_height = rotated_pixels.shape[0]
            
            non_transparent = rotated_pixels[:, :, 3] > 0
            y_coords, x_coords = np.where(non_transparent)
            
            for i in range(len(y_coords)):
                py, px = y_coords[i], x_coords[i]
                pixel_color = tuple(rotated_pixels[py, px])
                canvas_x = left + px
                canvas_y = top + py
                if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                    draw_layer.set_pixel(canvas_x, canvas_y, pixel_color)
            
            # Now update the selection with the rotated pixels
            selection_tool.selected_pixels = rotated_pixels
            # Ensure selection_rect keeps new dimensions
            selection_tool.selection_rect = (left, top, rotated_pixels.shape[1], rotated_pixels.shape[0])
            # Reset move tool state flags so first pickup after rotation acts as adjustment
            move_tool = self.tools.get("move")
            if move_tool:
                # Do not reset original_selection; keep it from initial selection
                move_tool.pixels_cleared = True  # original area has been cleared already by rotation
                move_tool.last_drawn_position = (left, top)
            
            # Update canvas display
            if self.update_canvas_callback:
                self.update_canvas_callback()
            if self.update_display_callback:
                self.update_display_callback()
        
        # Exit rotation mode
        self.is_rotating = False
        self.original_pixels_backup = None
        self.original_rect_backup = None
        self.rotated_pixels_preview = None
        
        # Clear rotation preview from canvas
        if hasattr(self, 'drawing_canvas') and self.drawing_canvas:
            self.drawing_canvas.delete("rotate_preview")
    
    def cancel_rotation(self):
        """Cancel rotation and restore original pixels"""
        if not self.is_rotating:
            return
        
        selection_tool = self.tools.get("selection")
        if selection_tool and self.original_pixels_backup is not None and self.original_rect_backup is not None:
            # Restore original pixels and rect
            selection_tool.selected_pixels = self.original_pixels_backup.copy()
            selection_tool.selection_rect = self.original_rect_backup  # Tuple doesn't need .copy()
        
        # Exit rotation mode
        self.is_rotating = False
        self.original_pixels_backup = None
        self.original_rect_backup = None
        self.rotated_pixels_preview = None
        
        # Clear rotation preview from canvas
        if hasattr(self, 'drawing_canvas') and self.drawing_canvas:
            self.drawing_canvas.delete("rotate_preview")
        
        # Update display
        if self.update_display_callback:
            self.update_display_callback()

    def _restore_and_prepare_move_background(self, left: int, top: int, width: int, height: int):
        """Restore the last drop's background on the active layer (removing the
        currently placed selection) and snapshot a new background under the
        current bounds so the next pickup can restore it correctly.

        This keeps move/transform workflows non-destructive and prevents
        duplicate stacking when the user mirrors/rotates then moves again.
        """
        move_tool = self.tools.get("move")
        draw_layer = self._get_drawing_layer()
        if not move_tool or not draw_layer:
            return
        # 1) Restore previous background if we have it
        if move_tool.saved_background is not None and move_tool.last_drawn_position is not None:
            restore_left, restore_top = move_tool.last_drawn_position
            for py in range(len(move_tool.saved_background)):
                for px in range(len(move_tool.saved_background[0])):
                    bg_pixel = move_tool.saved_background[py][px]
                    canvas_x = restore_left + px
                    canvas_y = restore_top + py
                    if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                        draw_layer.set_pixel(canvas_x, canvas_y, bg_pixel)
            print("[TRANSFORM] Restored background at previous drop")
        # 2) Snapshot fresh background under current bounds for the next pickup
        new_saved_background = []
        for py in range(height):
            row = []
            for px in range(width):
                cx = left + px
                cy = top + py
                if 0 <= cx < self.canvas.width and 0 <= cy < self.canvas.height:
                    row.append(draw_layer.get_pixel(cx, cy))
                else:
                    row.append((0, 0, 0, 0))
            new_saved_background.append(row)
        move_tool.saved_background = new_saved_background
        move_tool.last_drawn_position = (left, top)
        print("[TRANSFORM] Snapshotted new background for transformed selection")
    
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
        
        # Clear move tool's background restoration state to prevent copy-behind bug
        move_tool = self.tools.get("move")
        if move_tool:
            move_tool.saved_background = None
            move_tool.last_drawn_position = None
            print("[COPY] Cleared move tool state to prevent copy-behind bug")
        
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
        
        # Finalize move operation to prevent background restoration
        move_tool = self.tools.get("move")
        if move_tool:
            draw_layer = self._get_drawing_layer()
            if draw_layer:
                move_tool.finalize_move(draw_layer)
        
        # Determine current source dimensions from selected_pixels to avoid stale baselines
        new_left, new_top, new_width, new_height = new_rect
        old_height, old_width = selection_tool.selected_pixels.shape[0], selection_tool.selected_pixels.shape[1]
        
        # Ensure minimum size
        if new_width < 1 or new_height < 1:
            return
        
        # Scale the pixels using nearest neighbor, mapping from current content size
        self._simple_scale(selection_tool, old_width, old_height, new_width, new_height, new_left, new_top)

        # Update baseline rects for subsequent drags within scaling mode
        self.scale_original_rect = (new_left, new_top, new_width, new_height)
        self.scale_true_original_rect = (new_left, new_top, new_width, new_height)
    
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
        # Quick nearest-neighbor scaling for preview using NumPy vectorization
        # Create coordinate grids for the new size
        ny_coords = np.arange(new_height)
        nx_coords = np.arange(new_width)
        
        # Map to original coordinates
        oy_coords = (ny_coords * old_height // new_height).clip(0, selection_tool.selected_pixels.shape[0] - 1)
        ox_coords = (nx_coords * old_width // new_width).clip(0, selection_tool.selected_pixels.shape[1] - 1)
        
        # Use NumPy fancy indexing for fast scaling
        preview_pixels = selection_tool.selected_pixels[oy_coords[:, np.newaxis], ox_coords]
        
        # Temporarily draw the preview on canvas
        draw_layer = self._get_drawing_layer()
        if draw_layer:
            # Clear the TRUE original area using NumPy slicing where possible
            true_orig_left, true_orig_top, true_orig_width, true_orig_height = self.scale_true_original_rect
            
            # Bounds-safe clearing
            clear_y_start = max(0, true_orig_top)
            clear_y_end = min(self.canvas.height, true_orig_top + true_orig_height)
            clear_x_start = max(0, true_orig_left)
            clear_x_end = min(self.canvas.width, true_orig_left + true_orig_width)
            
            for py in range(clear_y_start, clear_y_end):
                for px in range(clear_x_start, clear_x_end):
                    draw_layer.set_pixel(px, py, (0, 0, 0, 0))
            
            # Draw the scaled preview - only non-transparent pixels
            non_transparent = preview_pixels[:, :, 3] > 0
            y_coords, x_coords = np.where(non_transparent)
            
            for i in range(len(y_coords)):
                py, px = y_coords[i], x_coords[i]
                pixel_color = tuple(preview_pixels[py, px])
                canvas_x = new_left + px
                canvas_y = new_top + py
                if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                    draw_layer.set_pixel(canvas_x, canvas_y, pixel_color)
            
            if self.update_canvas_callback:
                self.update_canvas_callback()
            if self.update_display_callback:
                self.update_display_callback()
    
    def _simple_scale(self, selection_tool, old_width, old_height, new_width, new_height, new_left, new_top):
        """Simple scaling without scipy - uses NumPy for efficiency"""
        # Use NumPy vectorization for fast nearest-neighbor scaling
        ny_coords = np.arange(new_height)
        nx_coords = np.arange(new_width)
        
        # Map to original coordinates
        oy_coords = (ny_coords * old_height // new_height).clip(0, selection_tool.selected_pixels.shape[0] - 1)
        ox_coords = (nx_coords * old_width // new_width).clip(0, selection_tool.selected_pixels.shape[1] - 1)
        
        # Use NumPy fancy indexing for fast scaling
        scaled_pixels = selection_tool.selected_pixels[oy_coords[:, np.newaxis], ox_coords]
        
        selection_tool.selected_pixels = scaled_pixels
        selection_tool.selection_rect = (new_left, new_top, new_width, new_height)
        
        # Redraw - only non-transparent pixels
        draw_layer = self._get_drawing_layer()
        if draw_layer:
            non_transparent = scaled_pixels[:, :, 3] > 0
            y_coords, x_coords = np.where(non_transparent)
            
            for i in range(len(y_coords)):
                py, px = y_coords[i], x_coords[i]
                pixel_color = tuple(scaled_pixels[py, px])
                canvas_x = new_left + px
                canvas_y = new_top + py
                if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
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

