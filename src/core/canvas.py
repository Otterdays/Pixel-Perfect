"""
Canvas system for Pixel Perfect
Handles pixel-perfect grid rendering and drawing surface
"""

import pygame
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
        
        # Background settings
        self.background_color = (255, 255, 255, 255)  # White
        self.checkerboard = True
        
        # Mouse tracking
        self.mouse_pos = (0, 0)
        self.last_mouse_pos = (0, 0)
        
        # Surface for rendering
        self.surface = None
        self._create_surface()
    
    def _create_surface(self):
        """Create pygame surface for rendering"""
        # Calculate display size
        display_width = int(self.width * self.zoom)
        display_height = int(self.height * self.zoom)
        
        self.surface = pygame.Surface((display_width, display_height), pygame.SRCALPHA)
        self._redraw_surface()
    
    def _redraw_surface(self):
        """Redraw the entire surface"""
        if not self.surface:
            return
            
        # Clear surface
        self.surface.fill((0, 0, 0, 0))
        
        # Draw background
        self._draw_background()
        
        # Draw pixels
        self._draw_pixels()
        
        # Draw grid
        if self.show_grid:
            self._draw_grid()
    
    def _draw_background(self):
        """Draw background (solid or checkerboard)"""
        if self.checkerboard:
            self._draw_checkerboard()
        else:
            self.surface.fill(self.background_color)
    
    def _draw_checkerboard(self):
        """Draw checkerboard pattern for transparency"""
        checker_size = max(1, int(self.zoom))
        light_color = (240, 240, 240, 255)
        dark_color = (200, 200, 200, 255)
        
        for y in range(0, int(self.height * self.zoom), checker_size):
            for x in range(0, int(self.width * self.zoom), checker_size):
                checker_x = x // checker_size
                checker_y = y // checker_size
                
                if (checker_x + checker_y) % 2 == 0:
                    color = light_color
                else:
                    color = dark_color
                
                pygame.draw.rect(self.surface, color, 
                               (x, y, checker_size, checker_size))
    
    def _draw_pixels(self):
        """Draw all pixels to surface"""
        for y in range(self.height):
            for x in range(self.width):
                pixel_color = self.pixels[y, x]
                
                # Skip transparent pixels
                if pixel_color[3] == 0:
                    continue
                
                # Draw pixel rectangle
                rect = pygame.Rect(
                    int(x * self.zoom),
                    int(y * self.zoom),
                    int(self.zoom),
                    int(self.zoom)
                )
                
                pygame.draw.rect(self.surface, pixel_color[:3], rect)
    
    def _draw_grid(self):
        """Draw pixel grid overlay"""
        # Always draw grid when enabled, regardless of zoom level
        if not self.show_grid:
            return

        # Use a more visible grid color with higher opacity
        grid_color = (100, 100, 100, 180)  # More visible gray

        # Draw thicker grid lines for better visibility
        line_width = max(1, min(2, int(self.zoom / 8)))  # Adaptive line width

        # Draw grid lines with proper spacing
        # Vertical lines
        for x in range(0, self.width + 1):
            screen_x = int(x * self.zoom)
            pygame.draw.line(self.surface, grid_color[:3],
                           (screen_x, 0), (screen_x, int(self.height * self.zoom)), line_width)

        # Horizontal lines
        for y in range(0, self.height + 1):
            screen_y = int(y * self.zoom)
            pygame.draw.line(self.surface, grid_color[:3],
                           (0, screen_y), (int(self.width * self.zoom), screen_y), line_width)
    
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
    
    def get_pixels_as_surface(self) -> pygame.Surface:
        """Get pixels as pygame surface (for export)"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        for y in range(self.height):
            for x in range(self.width):
                pixel_color = self.pixels[y, x]
                surface.set_at((x, y), pixel_color)
        
        return surface
