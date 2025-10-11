"""
Eyedropper tool for Pixel Perfect
Color sampling tool
"""

from .base_tool import Tool
from typing import Tuple
import pygame

class EyedropperTool(Tool):
    """Eyedropper tool for sampling colors"""
    
    def __init__(self):
        super().__init__("Eyedropper")
    
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Sample color from canvas - handled by main window"""
        # The main window handles color sampling
        pass
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """No action needed"""
        pass
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """No action needed"""
        pass
    
    def draw_preview(self, surface: pygame.Surface, x: int, y: int, color: Tuple[int, int, int, int]):
        """Draw eyedropper preview"""
        # Draw a small eyedropper icon at the cursor position
        pygame.draw.circle(surface, (0, 0, 0), (x, y), 3, 1)
        pygame.draw.circle(surface, (255, 255, 255), (x, y), 2, 1)
