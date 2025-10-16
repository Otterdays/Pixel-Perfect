"""
Canvas system for Pixel Perfect
Handles pixel data storage and manipulation
"""

import numpy as np
from typing import Tuple, Optional, List
from enum import Enum

class CanvasSize(Enum):
    """Preset canvas sizes"""
    SMALL = (16, 16)      # Item icons
    MEDIUM = (32, 32)     # Character sprites
    WIDE = (16, 32)       # Tall sprites
    LARGE = (32, 64)      # Large characters
    XLARGE = (64, 64)     # Extra large sprites/tiles

class Canvas:
    """Main drawing canvas with pixel-perfect grid"""
    
    def __init__(self, width: int, height: int, zoom: int = 8):
        self.width = width
        self.height = height
        self.zoom = max(0.25, min(32, zoom))  # Clamp zoom between 0.25x and 32x
        
        # Create pixel data array (RGBA)
        self.pixels = np.zeros((height, width, 4), dtype=np.uint8)
        
        # Grid settings
        self.show_grid = True
        self.grid_color = (100, 100, 100, 180)  # More visible gray with higher opacity
        self.grid_mode = "auto"  # "auto", "dark", "light", "paper"
        
        # Paper texture settings
        self.paper_texture_intensity = 0.3  # 0.0 to 1.0
        self.paper_base_color = "#f5f5dc"  # Cream/beige base
        self.paper_grain_color = "#e6e6d4"  # Slightly darker grain
        
        # Background settings
        self.background_color = (255, 255, 255, 255)  # White
        self.checkerboard = True
        self.background_mode = "auto"  # "auto", "dark", "light"
        
        # Mouse tracking
        self.mouse_pos = (0, 0)
        self.last_mouse_pos = (0, 0)
    
    def _create_surface(self):
        """Legacy method - rendering now handled by tkinter"""
        pass
    
    def _redraw_surface(self):
        """Legacy method - rendering now handled by tkinter"""
        pass
    
    def _draw_background(self):
        """Legacy method - rendering now handled by tkinter"""
        pass
    
    def _draw_checkerboard(self):
        """Legacy method - rendering now handled by tkinter"""
        pass
    
    def _draw_pixels(self):
        """Legacy method - rendering now handled by tkinter"""
        pass
    
    def _draw_grid(self):
        """Legacy method - rendering now handled by tkinter"""
        pass
    
    def set_pixel(self, x: int, y: int, color: Tuple[int, int, int, int]):
        """Set pixel at given coordinates"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y, x] = color
            self._redraw_surface()
    
    def get_pixel(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """Get pixel color at given coordinates"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return tuple(self.pixels[y, x])
        return (0, 0, 0, 0)
    
    def clear(self):
        """Clear all pixels"""
        self.pixels.fill(0)
        self._redraw_surface()
    
    def set_zoom(self, zoom: float):
        """Set zoom level and recreate surface"""
        self.zoom = max(0.25, min(32, zoom))
        self._create_surface()
    
    def toggle_grid(self):
        """Toggle grid visibility"""
        self.show_grid = not self.show_grid
        self._redraw_surface()
    
    def toggle_checkerboard(self):
        """Toggle checkerboard background"""
        self.checkerboard = not self.checkerboard
        self._redraw_surface()
    
    def screen_to_canvas(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """Convert screen coordinates to canvas coordinates"""
        canvas_x = int(screen_x / self.zoom)
        canvas_y = int(screen_y / self.zoom)
        return canvas_x, canvas_y
    
    def canvas_to_screen(self, canvas_x: int, canvas_y: int) -> Tuple[int, int]:
        """Convert canvas coordinates to screen coordinates"""
        screen_x = int(canvas_x * self.zoom)
        screen_y = int(canvas_y * self.zoom)
        return screen_x, screen_y
    
    def get_display_size(self) -> Tuple[int, int]:
        """Get display size of canvas"""
        return (int(self.width * self.zoom), int(self.height * self.zoom))
    
    def resize(self, width: int, height: int):
        """Resize canvas"""
        self.width = width
        self.height = height
        
        # Create new pixel array
        new_pixels = np.zeros((height, width, 4), dtype=np.uint8)
        
        # Copy existing pixels (clipped to new size)
        copy_width = min(width, self.pixels.shape[1])
        copy_height = min(height, self.pixels.shape[0])
        new_pixels[:copy_height, :copy_width] = self.pixels[:copy_height, :copy_width]
        
        self.pixels = new_pixels
        self._create_surface()
    
    def set_preset_size(self, size: CanvasSize):
        """Set canvas to preset size"""
        self.resize(size.value[0], size.value[1])
