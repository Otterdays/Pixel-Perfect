"""
Texture Tool - Apply repeating texture patterns to canvas
"""
from typing import Tuple, Optional
import numpy as np
from .base_tool import Tool

class TextureTool(Tool):
    """Apply texture patterns with live preview"""
    
    def __init__(self):
        super().__init__("Texture", cursor="crosshair")
        self.current_texture = None  # Currently selected texture pattern
        self.preview_position = None  # Current mouse position for preview
        
    def set_texture(self, texture_data: np.ndarray):
        """Set the current texture pattern"""
        self.current_texture = texture_data
        
    def get_texture_dimensions(self) -> Tuple[int, int]:
        """Get dimensions of current texture"""
        if self.current_texture is not None:
            return self.current_texture.shape[0], self.current_texture.shape[1]
        return 0, 0
    
    def on_mouse_down(self, layer, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Apply texture at clicked position"""
        if button == 1 and self.current_texture is not None:  # Left click
            self._apply_texture(layer, x, y)
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Update preview position for hover effect"""
        self.preview_position = (x, y)
    
    def on_mouse_drag(self, layer, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Apply texture while dragging"""
        if button == 1 and self.current_texture is not None:  # Left click drag
            self._apply_texture(layer, x, y)
            self.preview_position = (x, y)
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Mouse released"""
        pass
    
    def _apply_texture(self, layer, start_x: int, start_y: int):
        """Apply the texture pattern starting at the given position"""
        if self.current_texture is None:
            return
        
        height, width = self.current_texture.shape[0], self.current_texture.shape[1]
        
        # Apply texture pixels
        for py in range(height):
            for px in range(width):
                layer_x = start_x + px
                layer_y = start_y + py
                
                # Check bounds
                if 0 <= layer_x < layer.width and 0 <= layer_y < layer.height:
                    pixel_color = tuple(self.current_texture[py, px])
                    if pixel_color[3] > 0:  # Only apply non-transparent pixels
                        layer.set_pixel(layer_x, layer_y, pixel_color)
    
    def get_preview_rect(self) -> Optional[Tuple[int, int, int, int]]:
        """Get the preview rectangle for rendering"""
        if self.preview_position and self.current_texture is not None:
            x, y = self.preview_position
            height, width = self.current_texture.shape[0], self.current_texture.shape[1]
            return (x, y, width, height)
        return None
    
    def get_preview_texture(self) -> Optional[np.ndarray]:
        """Get the current texture for preview rendering"""
        return self.current_texture


# Hardcoded texture patterns
class TextureLibrary:
    """Library of hardcoded texture patterns"""
    
    @staticmethod
    def get_grass_8x8() -> np.ndarray:
        """
        8x8 grass texture with multiple shades of green
        Format: RGBA values (0-255)
        """
        # Define grass colors (RGBA)
        dark_green = (34, 139, 34, 255)    # Forest green base
        med_green = (50, 205, 50, 255)     # Lime green highlights
        light_green = (124, 252, 0, 255)   # Lawn green accents
        yellow_green = (154, 205, 50, 255) # Yellow-green variation
        
        # Create 8x8 pattern - artistic grass texture
        grass = np.array([
            # Row 0
            [dark_green, dark_green, med_green, dark_green, dark_green, med_green, dark_green, dark_green],
            # Row 1
            [dark_green, med_green, light_green, med_green, dark_green, dark_green, med_green, dark_green],
            # Row 2
            [med_green, dark_green, med_green, dark_green, med_green, dark_green, dark_green, med_green],
            # Row 3
            [dark_green, dark_green, dark_green, yellow_green, dark_green, med_green, dark_green, dark_green],
            # Row 4
            [dark_green, med_green, dark_green, dark_green, dark_green, light_green, med_green, dark_green],
            # Row 5
            [med_green, dark_green, med_green, dark_green, med_green, med_green, dark_green, med_green],
            # Row 6
            [dark_green, dark_green, yellow_green, med_green, dark_green, dark_green, dark_green, dark_green],
            # Row 7
            [dark_green, med_green, dark_green, dark_green, med_green, dark_green, med_green, dark_green],
        ], dtype=np.uint8)
        
        return grass
    
    @staticmethod
    def get_all_textures():
        """Get all available textures as a dictionary"""
        return {
            "Grass 8x8": TextureLibrary.get_grass_8x8(),
        }

