"""
Layer manager for Pixel Perfect
Handles multiple drawing layers with opacity and visibility
"""

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Layer:
    """Represents a single drawing layer"""
    name: str
    pixels: np.ndarray
    visible: bool = True
    opacity: float = 1.0
    locked: bool = False

class LayerManager:
    """Manages multiple drawing layers"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.layers: List[Layer] = []
        self.active_layer_index = 0
        self.max_layers = 10
        
        # Create default layer
        self._create_default_layer()
    
    def _create_default_layer(self):
        """Create the default background layer"""
        pixels = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        layer = Layer("Background", pixels)
        self.layers.append(layer)
    
    def add_layer(self, name: str = None) -> bool:
        """Add a new layer"""
        if len(self.layers) >= self.max_layers:
            return False
        
        if name is None:
            name = f"Layer {len(self.layers) + 1}"
        
        pixels = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        layer = Layer(name, pixels)
        
        # Insert after current active layer
        insert_index = self.active_layer_index + 1
        self.layers.insert(insert_index, layer)
        self.active_layer_index = insert_index
        
        return True
    
    def remove_layer(self, index: int) -> bool:
        """Remove a layer at given index"""
        if len(self.layers) <= 1:  # Keep at least one layer
            return False
        
        if 0 <= index < len(self.layers):
            self.layers.pop(index)
            
            # Adjust active layer index
            if self.active_layer_index >= len(self.layers):
                self.active_layer_index = len(self.layers) - 1
            elif self.active_layer_index > index:
                self.active_layer_index -= 1
            
            return True
        
        return False
    
    def duplicate_layer(self, index: int) -> bool:
        """Duplicate a layer"""
        if len(self.layers) >= self.max_layers:
            return False
        
        if 0 <= index < len(self.layers):
            original_layer = self.layers[index]
            new_pixels = original_layer.pixels.copy()
            new_layer = Layer(
                f"{original_layer.name} Copy",
                new_pixels,
                original_layer.visible,
                original_layer.opacity,
                original_layer.locked
            )
            
            # Insert after original layer
            insert_index = index + 1
            self.layers.insert(insert_index, new_layer)
            self.active_layer_index = insert_index
            
            return True
        
        return False
    
    def clear_layers(self):
        """Clear all layers and add a default background layer"""
        self.layers.clear()
        self.add_layer("Background")
        self.active_layer_index = 0
    
    def move_layer(self, from_index: int, to_index: int) -> bool:
        """Move layer from one position to another"""
        if (0 <= from_index < len(self.layers) and 
            0 <= to_index < len(self.layers) and 
            from_index != to_index):
            
            layer = self.layers.pop(from_index)
            self.layers.insert(to_index, layer)
            
            # Adjust active layer index
            if self.active_layer_index == from_index:
                self.active_layer_index = to_index
            elif from_index < self.active_layer_index <= to_index:
                self.active_layer_index -= 1
            elif to_index <= self.active_layer_index < from_index:
                self.active_layer_index += 1
            
            return True
        
        return False
    
    def set_active_layer(self, index: int) -> bool:
        """Set the active layer"""
        if 0 <= index < len(self.layers):
            self.active_layer_index = index
            return True
        return False
    
    def get_active_layer(self) -> Optional[Layer]:
        """Get the currently active layer"""
        if 0 <= self.active_layer_index < len(self.layers):
            return self.layers[self.active_layer_index]
        return None
    
    def get_layer(self, index: int) -> Optional[Layer]:
        """Get layer at given index"""
        if 0 <= index < len(self.layers):
            return self.layers[index]
        return None
    
    def set_layer_visibility(self, index: int, visible: bool) -> bool:
        """Set layer visibility"""
        if 0 <= index < len(self.layers):
            self.layers[index].visible = visible
            return True
        return False
    
    def set_layer_opacity(self, index: int, opacity: float) -> bool:
        """Set layer opacity (0.0 to 1.0)"""
        if 0 <= index < len(self.layers):
            self.layers[index].opacity = max(0.0, min(1.0, opacity))
            return True
        return False
    
    def set_layer_name(self, index: int, name: str) -> bool:
        """Set layer name"""
        if 0 <= index < len(self.layers):
            self.layers[index].name = name
            return True
        return False
    
    def set_layer_locked(self, index: int, locked: bool) -> bool:
        """Set layer locked state"""
        if 0 <= index < len(self.layers):
            self.layers[index].locked = locked
            return True
        return False
    
    def merge_layers(self, target_index: int, source_index: int) -> bool:
        """Merge source layer into target layer"""
        if (0 <= target_index < len(self.layers) and 
            0 <= source_index < len(self.layers) and 
            target_index != source_index):
            
            target_layer = self.layers[target_index]
            source_layer = self.layers[source_index]
            
            # Blend pixels
            for y in range(self.height):
                for x in range(self.width):
                    target_pixel = target_layer.pixels[y, x]
                    source_pixel = source_layer.pixels[y, x]
                    
                    # Simple alpha blending
                    alpha = source_pixel[3] * source_layer.opacity
                    if alpha > 0:
                        blend_factor = alpha / 255.0
                        target_layer.pixels[y, x] = (
                            int(target_pixel[0] * (1 - blend_factor) + source_pixel[0] * blend_factor),
                            int(target_pixel[1] * (1 - blend_factor) + source_pixel[1] * blend_factor),
                            int(target_pixel[2] * (1 - blend_factor) + source_pixel[2] * blend_factor),
                            max(target_pixel[3], int(alpha))
                        )
            
            # Remove source layer
            self.remove_layer(source_index)
            
            return True
        
        return False
    
    def flatten_layers(self) -> np.ndarray:
        """Flatten all visible layers into a single image"""
        result = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        
        for layer in self.layers:
            if layer.visible:
                for y in range(self.height):
                    for x in range(self.width):
                        layer_pixel = layer.pixels[y, x]
                        alpha = layer_pixel[3] * layer.opacity
                        
                        if alpha > 0:
                            blend_factor = alpha / 255.0
                            result[y, x] = (
                                int(result[y, x][0] * (1 - blend_factor) + layer_pixel[0] * blend_factor),
                                int(result[y, x][1] * (1 - blend_factor) + layer_pixel[1] * blend_factor),
                                int(result[y, x][2] * (1 - blend_factor) + layer_pixel[2] * blend_factor),
                                max(result[y, x][3], int(alpha))
                            )
        
        return result
    
    def resize_layers(self, new_width: int, new_height: int):
        """Resize all layers"""
        self.width = new_width
        self.height = new_height
        
        for layer in self.layers:
            new_pixels = np.zeros((new_height, new_width, 4), dtype=np.uint8)
            
            # Copy existing pixels (clipped to new size)
            copy_width = min(new_width, layer.pixels.shape[1])
            copy_height = min(new_height, layer.pixels.shape[0])
            new_pixels[:copy_height, :copy_width] = layer.pixels[:copy_height, :copy_width]
            
            layer.pixels = new_pixels
    
    def get_layer_count(self) -> int:
        """Get number of layers"""
        return len(self.layers)
    
    def get_layer_names(self) -> List[str]:
        """Get list of layer names"""
        return [layer.name for layer in self.layers]
