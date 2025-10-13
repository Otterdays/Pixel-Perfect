"""
Base tool interface for Pixel Perfect
All drawing tools inherit from this base class
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional
import pygame

class Tool(ABC):
    """Base class for all drawing tools"""
    
    def __init__(self, name: str, cursor: str = "arrow"):
        self.name = name
        self.cursor = cursor  # Tkinter cursor type
        self.is_active = False
        self.preview_surface = None
    
    @abstractmethod
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Handle mouse button press"""
        pass
    
    @abstractmethod
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Handle mouse button release"""
        pass
    
    @abstractmethod
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Handle mouse movement"""
        pass
    
    def draw_preview(self, surface: pygame.Surface, x: int, y: int, color: Tuple[int, int, int, int]):
        """Draw tool preview (optional)"""
        pass
    
    def activate(self):
        """Called when tool is selected"""
        self.is_active = True
    
    def deactivate(self):
        """Called when tool is deselected"""
        self.is_active = False
