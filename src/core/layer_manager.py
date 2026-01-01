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
    
    def __post_init__(self):
        """Initialize layer properties after dataclass creation"""
        if len(self.pixels.shape) == 3:
            self.height, self.width, _ = self.pixels.shape
        else:
            self.width = 0
            self.height = 0
    
    def set_pixel(self, x: int, y: int, color):
        """Set pixel at given coordinates"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y, x] = color
    
    def get_pixel(self, x: int, y: int):
        """Get pixel color at given coordinates"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return tuple(self.pixels[y, x])
        return (0, 0, 0, 0)
    
    def clear(self):
        """Clear all pixels"""
        self.pixels.fill(0)
    
    @property
    def zoom(self):
        """Dummy zoom property for tool compatibility"""
        return 1.0
    
    def _redraw_surface(self):
        """Dummy method for tool compatibility"""
        pass

class LayerManager:
    """Manages multiple drawing layers"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.layers: List[Layer] = []
        self.active_layer_index = 0
        self.max_layers = 10
        
        # Layer compositor cache for performance optimization
        # Stores the flattened result so we don't recompute unnecessarily
        self._cached_composite: Optional[np.ndarray] = None
        self._cache_valid: bool = False
        self._dirty_regions: List[Tuple[int, int, int, int]] = []  # (x, y, w, h) regions that need update
        
        # Create default layer
        self._create_default_layer()
    
    def invalidate_cache(self, region: Optional[Tuple[int, int, int, int]] = None):
        """
        Mark the compositor cache as invalid.
        
        Args:
            region: Optional (x, y, width, height) tuple to mark specific region dirty.
                    If None, entire cache is invalidated.
        """
        if region is None:
            # Full invalidation
            self._cache_valid = False
            self._dirty_regions.clear()
        else:
            # Track dirty region for potential incremental update
            self._dirty_regions.append(region)
            # For now, just invalidate entire cache (incremental update is future optimization)
            self._cache_valid = False
    
    def _create_default_layer(self):
        """Create the default background layer"""
        pixels = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        layer = Layer("Background", pixels)
        self.layers.append(layer)
        self.invalidate_cache()
    
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
        self.invalidate_cache()
        
        return True
    
    def remove_layer(self, index: int) -> bool:
        """Remove a layer at given index"""
        if len(self.layers) <= 1:  # Keep at least one layer
            return False
        
        if 0 <= index < len(self.layers):
            self.layers.pop(index)
            self.invalidate_cache()
            
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
            self.invalidate_cache()
            
            return True
        
        return False
    
    def clear_layers(self):
        """Clear all layers and add a default background layer"""
        self.layers.clear()
        self.invalidate_cache()
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
            self.invalidate_cache()
            return True
        return False
    
    def set_layer_opacity(self, index: int, opacity: float) -> bool:
        """Set layer opacity (0.0 to 1.0)"""
        if 0 <= index < len(self.layers):
            self.layers[index].opacity = max(0.0, min(1.0, opacity))
            self.invalidate_cache()
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
        """
        Flatten all visible layers into a single image.
        
        NOTE: Caching disabled - many code paths modify layer.pixels directly
        without going through tracked methods. Proper caching requires a 
        comprehensive change tracking system.
        """
        # DISABLED: Caching causes issues with selection tool and undo
        # Return cached composite if valid
        # if self._cache_valid and self._cached_composite is not None:
        #     return self._cached_composite
        
        result = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        
        for layer in self.layers:
            if layer.visible:
                # Vectorized alpha blending using NumPy operations
                layer_alpha = layer.pixels[:, :, 3].astype(np.float32) * layer.opacity
                
                # Create mask for non-transparent pixels
                mask = layer_alpha > 0
                if not np.any(mask):
                    continue
                
                # Calculate blend factor (0-1 range)
                blend_factor = layer_alpha / 255.0
                
                # Expand blend_factor for RGB channels broadcasting
                blend_rgb = blend_factor[:, :, np.newaxis]
                
                # Blend RGB channels where mask is True
                # result_rgb = result_rgb * (1 - blend) + layer_rgb * blend
                result_rgb = result[:, :, :3].astype(np.float32)
                layer_rgb = layer.pixels[:, :, :3].astype(np.float32)
                
                # Apply blending only where mask is True
                blended = result_rgb * (1 - blend_rgb) + layer_rgb * blend_rgb
                
                # Update result where we have visible pixels
                result[:, :, :3] = np.where(
                    mask[:, :, np.newaxis],
                    blended.astype(np.uint8),
                    result[:, :, :3]
                )
                
                # Update alpha channel (max of existing and new)
                result[:, :, 3] = np.maximum(result[:, :, 3], layer_alpha.astype(np.uint8))
        
        # DISABLED: Caching
        # self._cached_composite = result
        # self._cache_valid = True
        # self._dirty_regions.clear()
        
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
            # CRITICAL: Update layer's cached width/height after resizing pixels
            layer.width = new_width
            layer.height = new_height
    
    def get_layer_count(self) -> int:
        """Get number of layers"""
        return len(self.layers)
    
    def get_layer_names(self) -> List[str]:
        """Get list of layer names"""
        return [layer.name for layer in self.layers]
