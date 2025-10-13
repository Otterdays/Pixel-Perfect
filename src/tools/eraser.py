"""
Eraser tool for Pixel Perfect
Pixel removal tool
"""

from .base_tool import Tool
from typing import Tuple

class EraserTool(Tool):
    """Eraser tool for removing pixels"""
    
    def __init__(self):
        super().__init__("Eraser", cursor="X_cursor")
        self.is_erasing = False
    
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Start erasing"""
        if button == 1:  # Left mouse button
            self.is_erasing = True
            canvas.set_pixel(x, y, (0, 0, 0, 0))  # Transparent
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Stop erasing"""
        self.is_erasing = False
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Continue erasing while mouse is down"""
        if self.is_erasing:
            canvas.set_pixel(x, y, (0, 0, 0, 0))  # Transparent
