"""
Fill bucket tool for Pixel Perfect
Flood fill tool
"""

from .base_tool import Tool
from typing import Tuple, Set
import pygame

class FillTool(Tool):
    """Flood fill bucket tool"""
    
    def __init__(self):
        super().__init__("Fill", cursor="spraycan")
    
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Perform flood fill"""
        if button == 1:  # Left mouse button
            self._flood_fill(canvas, x, y, color)
        elif button == 3:  # Right mouse button (fill with transparent)
            self._flood_fill(canvas, x, y, (0, 0, 0, 0))
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """No action needed"""
        pass
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """No action needed"""
        pass
    
    def _flood_fill(self, canvas, start_x: int, start_y: int, fill_color: Tuple[int, int, int, int]):
        """Perform flood fill algorithm"""
        if not (0 <= start_x < canvas.width and 0 <= start_y < canvas.height):
            return
        
        # Get the target color (the color we're replacing)
        target_color = canvas.get_pixel(start_x, start_y)
        
        # If target color is the same as fill color, no need to fill
        if target_color == fill_color:
            return
        
        # Use iterative flood fill to avoid stack overflow
        stack = [(start_x, start_y)]
        visited = set()
        
        while stack:
            x, y = stack.pop()
            
            if (x, y) in visited:
                continue
            
            if not (0 <= x < canvas.width and 0 <= y < canvas.height):
                continue
            
            if canvas.get_pixel(x, y) != target_color:
                continue
            
            visited.add((x, y))
            canvas.set_pixel(x, y, fill_color)
            
            # Add neighboring pixels to stack
            stack.append((x + 1, y))
            stack.append((x - 1, y))
            stack.append((x, y + 1))
            stack.append((x, y - 1))
    
    def draw_preview(self, surface: pygame.Surface, x: int, y: int, color: Tuple[int, int, int, int]):
        """Draw fill preview"""
        # Draw a small bucket icon at the cursor position
        pygame.draw.circle(surface, color[:3], (x, y), 2, 1)
