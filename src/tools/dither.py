"""
Dither tool for Pixel Perfect
Draws in a checkerboard pattern
"""

from .base_tool import Tool
from typing import Tuple

class DitherTool(Tool):
    """Checkerboard pattern brush tool"""
    
    def __init__(self):
        super().__init__("Dither", cursor="pencil")
        self.is_drawing = False
        self.mode = "draw"
    
    def _should_draw(self, x: int, y: int) -> bool:
        """Check if pixel should be drawn based on checkerboard pattern"""
        # Checkerboard pattern: sum of coords is even
        return (x + y) % 2 == 0

    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Start drawing"""
        if button == 1:  # Left mouse button
            self.mode = "draw"
            self.is_drawing = True
            if self._should_draw(x, y):
                canvas.set_pixel(x, y, color)
        elif button == 3:  # Right mouse button (eraser)
            self.mode = "erase"
            self.is_drawing = True
            # Erase everything under cursor, not just pattern
            canvas.set_pixel(x, y, (0, 0, 0, 0))  # Transparent
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Stop drawing"""
        self.is_drawing = False
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Continue drawing while mouse is down"""
        if self.is_drawing:
            if self.mode == "draw":
                if self._should_draw(x, y):
                    canvas.set_pixel(x, y, color)
            else:
                # Erase mode
                canvas.set_pixel(x, y, (0, 0, 0, 0))
