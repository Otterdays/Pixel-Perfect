"""
Brush tool for Pixel Perfect
Single pixel placement tool
"""

from .base_tool import Tool
from typing import Tuple
import pygame

class BrushTool(Tool):
    """Single pixel brush tool"""
    
    def __init__(self):
        super().__init__("Brush", cursor="pencil")
        self.is_drawing = False
    
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Start drawing"""
        if button == 1:  # Left mouse button
            self.is_drawing = True
            canvas.set_pixel(x, y, color)
        elif button == 3:  # Right mouse button (eraser)
            self.is_drawing = True
            canvas.set_pixel(x, y, (0, 0, 0, 0))  # Transparent
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Stop drawing"""
        self.is_drawing = False
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Continue drawing while mouse is down"""
        if self.is_drawing:
            canvas.set_pixel(x, y, color)
    
    def draw_preview(self, surface: pygame.Surface, x: int, y: int, color: Tuple[int, int, int, int]):
        """Draw brush preview"""
        # Draw a small crosshair at the cursor position
        pygame.draw.line(surface, color[:3], (x-2, y), (x+2, y), 1)
        pygame.draw.line(surface, color[:3], (x, y-2), (x, y+2), 1)
