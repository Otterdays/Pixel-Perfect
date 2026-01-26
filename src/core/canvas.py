"""
Canvas system for Pixel Perfect
Handles pixel data storage and manipulation
"""

import numpy as np
from typing import Tuple, Optional, List
from enum import Enum

class CanvasSize(Enum):
    """Preset canvas sizes"""
    TINY = (8, 8)         # Micro icons
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
        self.zoom = max(0.25, min(64, zoom))  # Clamp zoom between 0.25x and 64x
        
        # Create pixel data array (RGBA)
        self.pixels = np.zeros((height, width, 4), dtype=np.uint8)
        
        # Grid settings
        self.show_grid = True
        self.grid_color = (100, 100, 100, 180)  # More visible gray with higher opacity
        self.grid_mode = "auto"  # "auto", "dark", "light", "paper"
        
        # Symmetry settings
        self.symmetry_x = False
        self.symmetry_y = False
        self.symmetry_center_x = True 
        
        # Paper texture settings
        self.paper_texture_intensity = 0.3  # 0.0 to 1.0
        self.paper_base_color = "#f5f5dc"  # Cream/beige base
        self.paper_grain_color = "#e6e6d4"  # Slightly darker grain
        
        # Background settings
        self.background_color = (255, 255, 255, 255)  # White
        self.checkerboard = True
        self.background_mode = "auto"  # "auto", "dark", "light", "texture"
        
        # Tile seam preview (for checking repeating edges)
        self.show_tile_seam_preview = False
        
        # Tile preview (shows canvas repeated in 3x3 grid for pattern visualization)
        self.show_tile_preview = False
        
        # Background texture settings
        self.background_texture_intensity = 0.4  # 0.0 to 1.0
        self.background_texture_base_color = "#f5f5dc"  # Same cream base as paper texture
        self.background_texture_grain_color = "#e6e6d4"  # Same grain color as paper texture
        
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
        """Set pixel at given coordinates, handling symmetry"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y, x] = color
            
            # Handle symmetry
            if self.symmetry_x:
                sym_x = self.width - 1 - x
                if 0 <= sym_x < self.width:
                    self.pixels[y, sym_x] = color
            
            if self.symmetry_y:
                sym_y = self.height - 1 - y
                if 0 <= sym_y < self.height:
                    self.pixels[sym_y, x] = color
                    
                    # If both symmetries are active, we need the diagonal mirror too
                    if self.symmetry_x:
                        sym_x = self.width - 1 - x
                        if 0 <= sym_x < self.width:
                            self.pixels[sym_y, sym_x] = color
                            
            self._redraw_surface()
    
    def toggle_symmetry_x(self):
        """Toggle horizontal symmetry"""
        self.symmetry_x = not self.symmetry_x
        self._redraw_surface()
        
    def toggle_symmetry_y(self):
        """Toggle vertical symmetry"""
        self.symmetry_y = not self.symmetry_y
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
        self.zoom = max(0.25, min(64, zoom))
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

class SymmetryWrapper:
    """
    Wraps a Layer or Canvas object to transparently handle symmetry.
    This allows tools to work with symmetry without modification.
    """
    def __init__(self, target, symmetry_provider):
        self.target = target
        self.symmetry_provider = symmetry_provider
        
    def __getattr__(self, name):
        """Delegate attribute access to target"""
        return getattr(self.target, name)
        
    def set_pixel(self, x: int, y: int, color: Tuple[int, int, int, int]):
        """Set pixel with symmetry mirroring"""
        # Set original pixel
        self.target.set_pixel(x, y, color)
        
        # Handle symmetry
        width = self.target.width
        height = self.target.height
        
        if self.symmetry_provider.symmetry_x:
            sym_x = width - 1 - x
            if 0 <= sym_x < width:
                self.target.set_pixel(sym_x, y, color)
        
        if self.symmetry_provider.symmetry_y:
            sym_y = height - 1 - y
            if 0 <= sym_y < height:
                self.target.set_pixel(x, sym_y, color)
                
                # If both symmetries are active, we need the diagonal mirror too
                if self.symmetry_provider.symmetry_x:
                    sym_x = width - 1 - x
                    if 0 <= sym_x < width:
                        self.target.set_pixel(sym_x, sym_y, color)
