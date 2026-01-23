"""
Magic Wand tool for Pixel Perfect
Selects pixels based on color similarity using flood fill algorithm
"""

from .base_tool import Tool
from typing import Tuple, Optional
import numpy as np


class MagicWandTool(Tool):
    """Magic Wand tool - selects pixels by color similarity"""
    
    def __init__(self):
        super().__init__("Magic Wand", cursor="crosshair")
        self.tolerance = 32  # Color similarity threshold (0-255)
        self.contiguous = True  # Only select connected pixels
        self.main_window = None
    
    def set_main_window(self, window):
        """Set reference to main window"""
        self.main_window = window
    
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Select pixels based on color similarity"""
        if button != 1:  # Only left click
            return
        
        if not (0 <= x < canvas.width and 0 <= y < canvas.height):
            return
        
        # Get flattened canvas pixels (all visible layers combined)
        # This ensures magic wand works with the full composite view
        original_pixels = None
        if self.main_window and hasattr(self.main_window, 'layer_manager'):
            flattened_pixels = self.main_window.layer_manager.flatten_layers()
            # Temporarily set canvas pixels to flattened view for selection
            original_pixels = canvas.pixels.copy()
            canvas.pixels = flattened_pixels
        
        try:
            # Get target color at click position
            target_color = tuple(canvas.get_pixel(x, y))
            
            # Skip transparent pixels
            if target_color[3] == 0:
                return
            
            # Perform flood fill to find matching pixels
            # Use flattened canvas pixels for selection
            selected_mask = self._flood_select(canvas, x, y, target_color, self.tolerance, self.contiguous)
            
            if selected_mask is None or not np.any(selected_mask):
                return
            
            # Get bounds of selection
            y_coords, x_coords = np.where(selected_mask)
            if len(x_coords) == 0:
                return
            
            left = int(np.min(x_coords))
            top = int(np.min(y_coords))
            right = int(np.max(x_coords)) + 1
            bottom = int(np.max(y_coords)) + 1
            width = right - left
            height = bottom - top
            
            # Extract selected pixels
            selected_pixels = np.zeros((height, width, 4), dtype=np.uint8)
            for y_idx in range(height):
                for x_idx in range(width):
                    canvas_x = left + x_idx
                    canvas_y = top + y_idx
                    if 0 <= canvas_x < canvas.width and 0 <= canvas_y < canvas.height:
                        if selected_mask[canvas_y, canvas_x]:
                            selected_pixels[y_idx, x_idx] = canvas.get_pixel(canvas_x, canvas_y)
            
            # Check for modifier keys (Shift = add, Alt = subtract)
            # Note: Modifier state would need to be passed from event dispatcher
            # For now, we'll replace selection
            
            # Set selection in selection tool (reuse existing selection system)
            if self.main_window and hasattr(self.main_window, 'tools'):
                selection_tool = self.main_window.tools.get("selection")
                if selection_tool:
                    selection_tool.selection_rect = (left, top, width, height)
                    selection_tool.selected_pixels = selected_pixels
                    selection_tool.has_selection = True
                    selection_tool.selected_edge_lines = None  # Magic wand doesn't capture edge lines
                    
                    # Trigger selection update
                    if hasattr(self.main_window, 'canvas_renderer'):
                        self.main_window.canvas_renderer.update_pixel_display()
                    
                    # Update status bar
                    if hasattr(self.main_window, '_update_status_bar'):
                        self.main_window._update_status_bar()
        finally:
            # Restore original canvas pixels if we swapped them
            if original_pixels is not None:
                canvas.pixels = original_pixels
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """No action needed"""
        pass
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """No action needed"""
        pass
    
    def _flood_select(self, canvas, start_x: int, start_y: int, target_color: Tuple[int, int, int, int], 
                     tolerance: int, contiguous: bool) -> Optional[np.ndarray]:
        """
        Flood fill algorithm to find all pixels matching target color within tolerance
        
        Args:
            canvas: Canvas object (should have flattened pixels set)
            start_x, start_y: Starting position
            target_color: Target RGBA color
            tolerance: Color similarity threshold (0-255)
            contiguous: If True, only select connected pixels. If False, select all matching pixels.
        
        Returns:
            Boolean mask array indicating selected pixels, or None if invalid
        """
        if not (0 <= start_x < canvas.width and 0 <= start_y < canvas.height):
            return None
        
        # Create selection mask
        selected = np.zeros((canvas.height, canvas.width), dtype=bool)
        
        # Convert target color to numpy array
        target_np = np.array(target_color, dtype=np.int16)
        
        # Use canvas pixels directly (should be flattened if magic wand was called correctly)
        canvas_pixels = canvas.pixels
        
        if contiguous:
            # Contiguous selection: flood fill from start point
            visited = np.zeros((canvas.height, canvas.width), dtype=bool)
            stack = [(start_x, start_y)]
            
            while stack:
                x, y = stack.pop()
                
                if visited[y, x]:
                    continue
                
                if not (0 <= x < canvas.width and 0 <= y < canvas.height):
                    continue
                
                # Check color similarity using canvas pixels array directly
                pixel_color = np.array(canvas_pixels[y, x], dtype=np.int16)
                color_diff = np.abs(pixel_color - target_np)
                
                # Skip transparent pixels
                if pixel_color[3] == 0:
                    continue
                
                # Check if color is similar enough (RGB only, not alpha)
                max_diff = np.max(color_diff[:3])
                if max_diff <= tolerance:
                    selected[y, x] = True
                    visited[y, x] = True
                    
                    # Add neighbors to stack
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < canvas.width and 0 <= ny < canvas.height:
                            if not visited[ny, nx]:
                                stack.append((nx, ny))
        else:
            # Global selection: select all matching pixels in canvas
            for y in range(canvas.height):
                for x in range(canvas.width):
                    pixel_color = np.array(canvas_pixels[y, x], dtype=np.int16)
                    
                    # Skip transparent pixels
                    if pixel_color[3] == 0:
                        continue
                    
                    # Check color similarity
                    color_diff = np.abs(pixel_color - target_np)
                    max_diff = np.max(color_diff[:3])
                    
                    if max_diff <= tolerance:
                        selected[y, x] = True
        
        return selected
    
    def set_tolerance(self, tolerance: int):
        """Set color similarity tolerance (0-255)"""
        self.tolerance = max(0, min(255, tolerance))
    
    def set_contiguous(self, contiguous: bool):
        """Set whether to select only contiguous pixels"""
        self.contiguous = contiguous
