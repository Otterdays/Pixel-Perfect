"""
Selection tools for Pixel Perfect
Rectangle selection and move functionality
"""

from .base_tool import Tool
from typing import Tuple, Optional, List
import numpy as np

class SelectionTool(Tool):
    """Rectangle selection tool"""
    
    def __init__(self):
        super().__init__("Selection", cursor="crosshair")
        self.is_selecting = False
        self.selection_start = (0, 0)
        self.selection_end = (0, 0)
        self.selection_rect = None
        self.selected_pixels = None
        self.selected_edge_lines = None  # Store captured edge lines
        self.has_selection = False
        self.on_selection_complete = None  # Callback for when selection is finalized
        self.main_window = None  # Will be set by the main window
    
    def set_main_window(self, main_window):
        """Set reference to main window for accessing other tools"""
        self.main_window = main_window
    
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Start selection"""
        if button == 1:  # Left mouse button
            self.is_selecting = True
            self.selection_start = (x, y)
            self.selection_end = (x, y)
            self.has_selection = False
            # Clear old selection to start fresh
            self.selection_rect = None
            self.selected_pixels = None
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """End selection"""
        if button == 1 and self.is_selecting:
            self.is_selecting = False
            self.selection_end = (x, y)
            self._finalize_selection(canvas)
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Update selection while dragging"""
        if self.is_selecting:
            self.selection_end = (x, y)
            self._update_selection_rect()
    
    def _update_selection_rect(self):
        """Update selection rectangle"""
        x1, y1 = self.selection_start
        x2, y2 = self.selection_end
        
        # Calculate rectangle bounds
        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        self.selection_rect = (left, top, width, height)
    
    def _finalize_selection(self, canvas):
        """Finalize the selection and capture pixels"""
        if not self.selection_rect:
            return
        
        left, top, width, height = self.selection_rect
        
        # Clamp to canvas bounds
        left = max(0, min(left, canvas.width))
        top = max(0, min(top, canvas.height))
        width = min(width, canvas.width - left)
        height = min(height, canvas.height - top)
        
        if width <= 0 or height <= 0:
            self.has_selection = False
            return
        
        # ONLY capture pixels if we don't already have them stored
        # This prevents re-capturing after a move operation
        if self.selected_pixels is None:
            # Capture selected pixels
            self.selected_pixels = np.zeros((height, width, 4), dtype=np.uint8)
            
            for y in range(height):
                for x in range(width):
                    canvas_x = left + x
                    canvas_y = top + y
                    if 0 <= canvas_x < canvas.width and 0 <= canvas_y < canvas.height:
                        self.selected_pixels[y, x] = canvas.get_pixel(canvas_x, canvas_y)
            
            # Also capture edge lines that intersect with selection area
            self.selected_edge_lines = self._capture_edge_lines_in_selection(left, top, width, height)
        
        self.has_selection = True
        self.selection_rect = (left, top, width, height)
        
        # Notify that selection is complete
        if self.on_selection_complete:
            self.on_selection_complete()
    
    def _capture_edge_lines_in_selection(self, left: int, top: int, width: int, height: int):
        """Capture edge lines that intersect with the selection area"""
        if not self.main_window or 'edge' not in self.main_window.tools:
            return []
        
        edge_tool = self.main_window.tools['edge']
        captured_edges = []
        
        # Check each edge line to see if it intersects with the selection area
        for edge_data in edge_tool.edge_lines:
            edge_x = edge_data['pixel_x']
            edge_y = edge_data['pixel_y']
            edge_type = edge_data['edge']
            
            # Calculate the actual line coordinates based on edge type
            line_coords = self._get_edge_line_coordinates(edge_x, edge_y, edge_type)
            
            # Check if line intersects with selection rectangle
            if self._line_intersects_rect(line_coords, left, top, width, height):
                captured_edges.append(edge_data)
        
        return captured_edges
    
    def _get_edge_line_coordinates(self, pixel_x: int, pixel_y: int, edge_type: str):
        """Get the actual line coordinates for an edge"""
        if edge_type == "top":
            # Horizontal line above pixel (x, y) to (x+1, y)
            return (pixel_x, pixel_y, pixel_x + 1, pixel_y)
        elif edge_type == "bottom":
            # Horizontal line below pixel (x, y+1) to (x+1, y+1)
            return (pixel_x, pixel_y + 1, pixel_x + 1, pixel_y + 1)
        elif edge_type == "left":
            # Vertical line to left of pixel (x, y) to (x, y+1)
            return (pixel_x, pixel_y, pixel_x, pixel_y + 1)
        elif edge_type == "right":
            # Vertical line to right of pixel (x+1, y) to (x+1, y+1)
            return (pixel_x + 1, pixel_y, pixel_x + 1, pixel_y + 1)
        else:
            return None
    
    def _line_intersects_rect(self, line_coords, rect_left: int, rect_top: int, rect_width: int, rect_height: int):
        """Check if a line intersects with a rectangle"""
        if not line_coords:
            return False
        
        x1, y1, x2, y2 = line_coords
        rect_right = rect_left + rect_width
        rect_bottom = rect_top + rect_height
        
        # Check if line is completely outside rectangle
        if (max(x1, x2) < rect_left or min(x1, x2) > rect_right or
            max(y1, y2) < rect_top or min(y1, y2) > rect_bottom):
            return False
        
        # For simple horizontal/vertical lines, this is sufficient
        # More complex line-rectangle intersection would need proper line-rect intersection math
        return True
    
    def clear_selection(self):
        """Clear current selection"""
        self.has_selection = False
        self.selection_rect = None
        self.selected_pixels = None
        self.selected_edge_lines = None
        self.is_selecting = False
        # Also clear edge-line move tracking so next selection starts clean
        if hasattr(self, '_last_edge_lines_position'):
            self._last_edge_lines_position = None
    
    def get_selection_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get selection bounds (left, top, width, height)"""
        return self.selection_rect
    
    def has_active_selection(self) -> bool:
        """Check if there's an active selection"""
        return self.has_selection

class MoveTool(Tool):
    """Move selection tool"""
    
    def __init__(self):
        super().__init__("Move", cursor="fleur")
        self.is_moving = False
        self.move_offset = (0, 0)
        self.original_selection = None  # (left, top, width, height)
        self.selection_tool = None
        self.cleared_background = None  # Store what was cleared for undo if needed
        self.pixels_cleared = False  # Track if we've cleared original pixels yet
        self.has_been_moved = False  # Track if selection has been moved from original position
        self.last_drawn_position = None  # Track where pixels are currently drawn on canvas
        self.saved_background = None  # Store background pixels before placing selection
    
    def set_selection_tool(self, selection_tool: SelectionTool):
        """Set reference to selection tool"""
        self.selection_tool = selection_tool
    
    def reset_state(self):
        """Reset move tool state (called when selection is cleared or tool is switched)"""
        self.is_moving = False
        self.move_offset = (0, 0)
        self.original_selection = None
        self.cleared_background = None
        self.pixels_cleared = False  # Reset for new selection
        self.has_been_moved = False
        self.last_drawn_position = None
        self.saved_background = None
        # Reset last edge line placement tracking used for cleanup between moves
        if hasattr(self, '_last_edge_lines_position'):
            self._last_edge_lines_position = None
        print("[MOVE] State reset - ready for new selection")
    
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Start moving selection"""
        print(f"[MOVE DEBUG] Mouse down at ({x}, {y}) - selection tool has selection: {self.selection_tool.has_active_selection() if self.selection_tool else False}")
        if (button == 1 and self.selection_tool and 
            self.selection_tool.has_active_selection()):
            
            bounds = self.selection_tool.get_selection_bounds()
            if bounds:
                left, top, width, height = bounds
                # Check if click is within selection
                if left <= x < left + width and top <= y < top + height:
                    # If we just completed a rotation, ensure selected_pixels is current
                    if (hasattr(self.selection_tool.main_window, 'selection_mgr') and 
                        self.selection_tool.main_window.selection_mgr.rotated_pixels_preview is None and
                        self.selection_tool.selected_pixels is not None):
                        # No-op placeholder; selected_pixels already set on apply_rotation
                        pass
                    # Enter moving state
                    self.is_moving = True
                    self.move_offset = (x - left, y - top)
                    
                    # FIRST PICKUP: Refresh selection pixels from layer, then clear originals and edge lines
                    if not self.original_selection:
                        self.original_selection = (left, top, width, height)
                        # Refresh the selected pixel buffer from the ACTIVE LAYER right now.
                        # This ensures we operate on a fresh mask that exactly matches what's on the layer.
                        import numpy as _np
                        fresh_pixels = _np.zeros((height, width, 4), dtype=_np.uint8)
                        for py in range(height):
                            for px in range(width):
                                cx = left + px
                                cy = top + py
                                if 0 <= cx < canvas.width and 0 <= cy < canvas.height:
                                    fresh_pixels[py, px] = canvas.get_pixel(cx, cy)
                        # Replace the cached selection with the fresh snapshot
                        self.selection_tool.selected_pixels = fresh_pixels

                        # Clear ONLY the actual selected pixels from the layer using the fresh snapshot
                        for py in range(height):
                            for px in range(width):
                                if fresh_pixels[py, px][3] > 0:  # non-transparent only
                                    cx = left + px
                                    cy = top + py
                                    if 0 <= cx < canvas.width and 0 <= cy < canvas.height:
                                        canvas.set_pixel(cx, cy, (0, 0, 0, 0))
                        
                        # Clear selected edge lines from original position
                        self._clear_selected_edge_lines_from_original_position(left, top)
                        
                        print("[MOVE] First pickup - cleared selected pixels and edge lines")
                    
                    # SUBSEQUENT PICKUPS: Restore saved background (from last drop)
                    elif self.saved_background and self.last_drawn_position:
                        restore_left, restore_top = self.last_drawn_position
                        for py in range(len(self.saved_background)):
                            for px in range(len(self.saved_background[0])):
                                bg_pixel = self.saved_background[py][px]
                                canvas_x = restore_left + px
                                canvas_y = restore_top + py
                                if 0 <= canvas_x < canvas.width and 0 <= canvas_y < canvas.height:
                                    canvas.set_pixel(canvas_x, canvas_y, bg_pixel)
                        print("[MOVE] Adjustment pickup - restored background from last drop")
                    
                    # Clear saved background for new move
                    self.saved_background = None
                    
                    print("[MOVE] Picked up selection")
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """End moving selection"""
        if button == 1 and self.is_moving:
            self.is_moving = False
            
            # Save background and draw pixels at new position
            if self.selection_tool and self.selection_tool.selected_pixels is not None:
                bounds = self.selection_tool.get_selection_bounds()
                if bounds:
                    left, top, width, height = bounds
                    
                    # Save background pixels BEFORE drawing anything at the new position
                    self.saved_background = []
                    for py in range(height):
                        row = []
                        for px in range(width):
                            canvas_x = left + px
                            canvas_y = top + py
                            if 0 <= canvas_x < canvas.width and 0 <= canvas_y < canvas.height:
                                row.append(canvas.get_pixel(canvas_x, canvas_y))
                            else:
                                row.append((0, 0, 0, 0))
                        self.saved_background.append(row)
                    
                    # Draw ONLY the actual selected pixels at new position
                    for py in range(min(height, self.selection_tool.selected_pixels.shape[0])):
                        for px in range(min(width, self.selection_tool.selected_pixels.shape[1])):
                            pixel_color = tuple(self.selection_tool.selected_pixels[py, px])
                            if pixel_color[3] > 0:  # Only place actual non-transparent pixels
                                canvas_x = left + px
                                canvas_y = top + py
                                if 0 <= canvas_x < canvas.width and 0 <= canvas_y < canvas.height:
                                    canvas.set_pixel(canvas_x, canvas_y, pixel_color)
                    
                    # Now update edge lines at the new position (handles removing previous ones)
                    self._draw_selected_edge_lines_at_position(left, top)
                    
                    # Track this position for next pickup
                    self.last_drawn_position = (left, top)
                    
                    # Track if we've moved from original
                    if self.original_selection:
                        orig_left, orig_top, orig_width, orig_height = self.original_selection
                        if left != orig_left or top != orig_top:
                            self.has_been_moved = True
                            print(f"[MOVE] Pixels drawn (background saved for non-destructive adjustment)")
                            
                            # Only finalize on the FIRST move to clear original position
                            # Subsequent moves don't need finalization since original is already cleared
                            if not self.pixels_cleared:  # Only finalize once
                                # Finalize against the active drawing layer, not the display canvas
                                draw_layer = None
                                if (self.selection_tool and self.selection_tool.main_window 
                                    and hasattr(self.selection_tool.main_window, '_get_drawing_layer')):
                                    draw_layer = self.selection_tool.main_window._get_drawing_layer()
                                if draw_layer is None:
                                    # Fallback to using canvas (legacy behavior)
                                    draw_layer = canvas
                                self.finalize_move(draw_layer)
                                self.pixels_cleared = True
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Update selection position while moving"""
        if self.is_moving and self.selection_tool:
            bounds = self.selection_tool.get_selection_bounds()
            if bounds:
                left, top, width, height = bounds
                new_left = x - self.move_offset[0]
                new_top = y - self.move_offset[1]
                
                # Clamp to canvas bounds
                new_left = max(0, min(new_left, canvas.width - width))
                new_top = max(0, min(new_top, canvas.height - height))
                
                # Update selection position
                self.selection_tool.selection_rect = (new_left, new_top, width, height)
    
    def finalize_move(self, layer):
        """Finalize the move operation - clear original pixels and place at new position on layer"""
        if self.has_been_moved and self.original_selection and self.selection_tool:
            orig_left, orig_top, orig_width, orig_height = self.original_selection
            bounds = self.selection_tool.get_selection_bounds()
            
            if bounds:
                left, top, width, height = bounds
                
                # CRITICAL FIX: Refresh original pixels from layer before clearing
                # This ensures we clear the ACTUAL pixels that were at the original position,
                # not the transformed pixels that might be in selected_pixels
                print("[MOVE] Refreshing original pixels from layer before clearing...")
                import numpy as _np
                original_pixels = _np.zeros((orig_height, orig_width, 4), dtype=_np.uint8)
                for py in range(orig_height):
                    for px in range(orig_width):
                        cx = orig_left + px
                        cy = orig_top + py
                        if 0 <= cx < layer.width and 0 <= cy < layer.height:
                            original_pixels[py, px] = layer.get_pixel(cx, cy)
                
                # Step 1: Clear ONLY the actual pixels that were at the original position
                # This prevents destroying pixels in empty spaces of the selection rectangle
                cleared_count = 0
                for py in range(orig_height):
                    for px in range(orig_width):
                        pixel_color = tuple(original_pixels[py, px])
                        if pixel_color[3] > 0:  # Only clear actual non-transparent pixels
                            canvas_x = orig_left + px
                            canvas_y = orig_top + py
                            if 0 <= canvas_x < layer.width and 0 <= canvas_y < layer.height:
                                layer.set_pixel(canvas_x, canvas_y, (0, 0, 0, 0))
                                cleared_count += 1
                
                print(f"[MOVE] Cleared {cleared_count} original pixels from original position")
                
                # Step 2: Place pixels at new position on layer
                for py in range(min(height, self.selection_tool.selected_pixels.shape[0])):
                    for px in range(min(width, self.selection_tool.selected_pixels.shape[1])):
                        pixel_color = tuple(self.selection_tool.selected_pixels[py, px])
                        if pixel_color[3] > 0:  # Only place actual non-transparent pixels
                            canvas_x = left + px
                            canvas_y = top + py
                            if 0 <= canvas_x < layer.width and 0 <= canvas_y < layer.height:
                                layer.set_pixel(canvas_x, canvas_y, pixel_color)
                
                print(f"[MOVE] Finalized move - cleared {cleared_count} original pixels, placed at new position (LAYER DATA UPDATED)")
                
                # Sync canvas with updated layer data to remove original pixels from display
                if self.selection_tool and self.selection_tool.main_window:
                    self.selection_tool.main_window._update_canvas_from_layers()
                    print("[MOVE] Canvas synchronized with layer data")
                
                # Reset state - but KEEP original_selection so subsequent pickups
                # know this isn't a first-time pickup and won't clear pixels underneath
                self.has_been_moved = False
                # IMPORTANT: Do NOT reset pixels_cleared here; we only finalize once per selection
                # self.pixels_cleared stays True until reset_state() is called for a new selection
                # DON'T reset original_selection here - it prevents the bug where
                # picking up again deletes pixels underneath
                # self.original_selection = None  # ⚠️ REMOVED - this caused the bug
                # Keep saved_background so the very next pickup can restore the last drop
                # (restoration happens in on_mouse_down before clearing)
    
    def _clear_selected_edge_lines_from_original_position(self, left: int, top: int):
        """Clear selected edge lines from their original position"""
        if not self.selection_tool or not self.selection_tool.selected_edge_lines:
            return
        
        # Get reference to edge tool to remove edge lines
        if not self.selection_tool.main_window or 'edge' not in self.selection_tool.main_window.tools:
            return
        
        edge_tool = self.selection_tool.main_window.tools['edge']
        
        # Remove each selected edge line from the edge tool's storage
        for edge_data in self.selection_tool.selected_edge_lines:
            if edge_data in edge_tool.edge_lines:
                edge_tool.edge_lines.remove(edge_data)
        
        # Redraw edge lines to update display
        if hasattr(edge_tool, 'redraw_all_edges'):
            edge_tool.redraw_all_edges(force=True)
        
        print(f"[MOVE] Cleared {len(self.selection_tool.selected_edge_lines)} edge lines from original position")
    
    def _draw_selected_edge_lines_at_position(self, left: int, top: int):
        """Draw selected edge lines at new position"""
        if not self.selection_tool or not self.selection_tool.selected_edge_lines:
            return
        
        # Get reference to edge tool to add edge lines
        if not self.selection_tool.main_window or 'edge' not in self.selection_tool.main_window.tools:
            return
        
        edge_tool = self.selection_tool.main_window.tools['edge']
        orig_left, orig_top = self.original_selection[:2]
        
        # Calculate offset from original position
        offset_x = left - orig_left
        offset_y = top - orig_top
        
        # First, remove any existing edge lines from the previous position
        # (for subsequent moves, we need to clean up the previous position)
        if hasattr(self, '_last_edge_lines_position') and self._last_edge_lines_position:
            last_left, last_top = self._last_edge_lines_position
            last_offset_x = last_left - orig_left
            last_offset_y = last_top - orig_top
            
            # Remove edge lines from previous position
            for edge_data in self.selection_tool.selected_edge_lines:
                prev_edge_data = edge_data.copy()
                prev_edge_data['pixel_x'] = edge_data['pixel_x'] + last_offset_x
                prev_edge_data['pixel_y'] = edge_data['pixel_y'] + last_offset_y
                
                # Remove from edge tool storage if it exists
                if prev_edge_data in edge_tool.edge_lines:
                    edge_tool.edge_lines.remove(prev_edge_data)
        
        # Add each edge line at the new position
        for edge_data in self.selection_tool.selected_edge_lines:
            # Create new edge data with adjusted coordinates
            new_edge_data = edge_data.copy()
            new_edge_data['pixel_x'] = edge_data['pixel_x'] + offset_x
            new_edge_data['pixel_y'] = edge_data['pixel_y'] + offset_y
            
            # Add to edge tool storage
            edge_tool.edge_lines.append(new_edge_data)
        
        # Track this position for next move
        self._last_edge_lines_position = (left, top)
        
        # Redraw edge lines to update display
        if hasattr(edge_tool, 'redraw_all_edges'):
            edge_tool.redraw_all_edges(force=True)
        
        print(f"[MOVE] Drew {len(self.selection_tool.selected_edge_lines)} edge lines at new position")
