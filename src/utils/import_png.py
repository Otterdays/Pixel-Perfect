"""
PNG to .pixpf Import Utility
Converts PNG images back into editable Pixel Perfect projects
"""

import os
import json
from datetime import datetime
from typing import Optional, Tuple
import numpy as np
from PIL import Image


class PNGImporter:
    """Handles PNG to .pixpf conversion"""
    
    VALID_SIZES = [8, 16, 32, 64]  # Added 8 for 8x8 canvas support
    SCALE_FACTORS = [1, 2, 4, 8]  # Common export scales
    
    def __init__(self):
        pass
    
    def import_png_to_pixpf(self, png_path: str, pixpf_path: str, 
                           palette_name: str = "SNES Classic",
                           palette_type: str = "snes_classic",
                           scale_factor: int = 1) -> Tuple[bool, str]:
        """
        Convert PNG to basic .pixpf project
        
        Args:
            png_path: Path to input PNG file
            pixpf_path: Path to output .pixpf file
            palette_name: Default palette name
            palette_type: Default palette type
            scale_factor: Scale multiplier (1x, 2x, 3x, 4x) - scales UP the imported image
            
        Returns:
            (success: bool, message: str)
        """
        try:
            # 1. Validate PNG file exists
            if not os.path.exists(png_path):
                return False, f"PNG file not found: {png_path}"
            
            # 2. Load PNG with PIL
            try:
                image = Image.open(png_path)
            except Exception as e:
                return False, f"Failed to open PNG: {e}"
            
            # 3. Get dimensions
            width, height = image.size
            original_width, original_height = width, height
            
            # 4. Check if dimensions need downscaling (from scaled exports)
            needs_downscale = False
            detected_scale = 1
            
            # PRIORITY: Check if it's a scaled export FIRST (before direct sizes)
            # This prevents 64x64 from being treated as direct size when it's actually 8x8 scaled
            for scale in reversed(self.SCALE_FACTORS):
                scaled_width = width // scale
                scaled_height = height // scale
                
                if (scaled_width in self.VALID_SIZES and 
                    scaled_height in self.VALID_SIZES and
                    width % scale == 0 and height % scale == 0):
                    # Found valid downscale!
                    width = scaled_width
                    height = scaled_height
                    detected_scale = scale
                    needs_downscale = True
                    break
            
            # SECONDARY: Check direct sizes only if no scaled export detected
            if not needs_downscale and (width not in self.VALID_SIZES or height not in self.VALID_SIZES):
                return False, (
                    f"Invalid dimensions: {original_width}x{original_height}\n\n"
                    f"Valid sizes: 8x8, 16x16, 32x32, 64x64\n"
                    f"(or scaled versions: 128x128, 256x256, 512x512, etc.)\n\n"
                    f"Your image: {original_width}x{original_height}"
                )
            
            # 5. Convert to RGBA and downscale if needed
            rgba_image = image.convert('RGBA')
            
            if needs_downscale:
                # Downscale using nearest neighbor to preserve pixel art
                new_size = (width, height)
                rgba_image = rgba_image.resize(new_size, Image.NEAREST)
                print(f"Auto-downscaled from {original_width}x{original_height} to {width}x{height} ({detected_scale}x scale detected)")
            
            # 5.5. Apply user-requested scale factor (scale UP)
            if scale_factor > 1:
                scaled_width = width * scale_factor
                scaled_height = height * scale_factor
                rgba_image = rgba_image.resize((scaled_width, scaled_height), Image.NEAREST)
                print(f"Scaling up {scale_factor}x: {width}x{height} → {scaled_width}x{scaled_height}")
                width = scaled_width
                height = scaled_height
            
            pixels = np.array(rgba_image, dtype=np.uint8)
            
            # 6. Get default palette colors
            palette_colors = self._get_default_palette(palette_type)
            
            # 7. Build minimal .pixpf structure
            project_data = {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat(),
                "canvas": {
                    "width": width,
                    "height": height,
                    "zoom": self._get_default_zoom(width),
                    "show_grid": True,
                    "checkerboard": True
                },
                "palette": {
                    "name": palette_name,
                    "type": palette_type,
                    "colors": palette_colors,
                    "primary_color": 0,
                    "secondary_color": 1
                },
                "layers": [{
                    "index": 0,
                    "name": "Imported",
                    "visible": True,
                    "opacity": 1.0,
                    "locked": False,
                    "pixels": pixels.tolist()
                }],
                "animation": {
                    "current_frame": 0,
                    "fps": 12,
                    "loop": True,
                    "frames": []
                },
                "metadata": {
                    "imported_from": os.path.basename(png_path),
                    "import_date": datetime.now().isoformat(),
                    "original_size": f"{width}x{height}"
                }
            }
            
            # 8. Save to .pixpf
            with open(pixpf_path, 'w') as f:
                json.dump(project_data, f, indent=2)
            
            # Build success message
            msg = f"Successfully imported PNG to {width}x{height} canvas"
            if needs_downscale:
                msg += f"\n(Auto-downscaled from {original_width}x{original_height})"
            if scale_factor > 1:
                msg += f"\n(Scaled up {scale_factor}x)"
            
            return True, msg
            
        except Exception as e:
            return False, f"Import error: {e}"
    
    def _get_default_zoom(self, canvas_size: int) -> int:
        """Get appropriate default zoom based on canvas size"""
        zoom_map = {
            16: 16,
            32: 16,
            64: 8
        }
        return zoom_map.get(canvas_size, 16)
    
    def _get_default_palette(self, palette_type: str) -> list:
        """Get default palette colors"""
        # SNES Classic palette (16 colors)
        snes_palette = [
            [0, 0, 0, 255],           # Black
            [255, 255, 255, 255],     # White
            [136, 0, 0, 255],         # Dark Red
            [170, 255, 238, 255],     # Cyan
            [204, 68, 204, 255],      # Purple
            [0, 204, 85, 255],        # Green
            [0, 0, 170, 255],         # Blue
            [238, 238, 119, 255],     # Yellow
            [221, 136, 85, 255],      # Orange
            [102, 68, 0, 255],        # Brown
            [255, 119, 119, 255],     # Light Red
            [51, 51, 51, 255],        # Dark Gray
            [119, 119, 119, 255],     # Gray
            [170, 255, 102, 255],     # Light Green
            [0, 136, 255, 255],       # Light Blue
            [187, 187, 187, 255]      # Light Gray
        ]
        
        # You can add more palettes here if needed
        palette_map = {
            "snes_classic": snes_palette,
            "curse_of_aros": snes_palette,  # Default to SNES for now
            "heartwood": snes_palette,
            "definya": snes_palette,
            "kakele": snes_palette,
            "rucoy": snes_palette,
            "old_school_runescape": snes_palette
        }
        
        return palette_map.get(palette_type, snes_palette)
    
    def validate_png_dimensions(self, png_path: str) -> Tuple[bool, str, int, int]:
        """
        Check if PNG dimensions are valid for import (includes scaled detection)
        
        Returns:
            (is_valid: bool, message: str, width: int, height: int)
        """
        try:
            if not os.path.exists(png_path):
                return False, "File not found", 0, 0
            
            image = Image.open(png_path)
            width, height = image.size
            
            # PRIORITY: Check if it's a scaled export FIRST (before direct sizes)
            # This prevents 64x64 from being treated as direct size when it's actually 8x8 scaled
            for scale in reversed(self.SCALE_FACTORS):
                scaled_width = width // scale
                scaled_height = height // scale
                
                if (scaled_width in self.VALID_SIZES and 
                    scaled_height in self.VALID_SIZES and
                    width % scale == 0 and height % scale == 0):
                    return True, f"Valid scaled export: {width}x{height} (will downscale {scale}x to {scaled_width}x{scaled_height})", scaled_width, scaled_height
            
            # SECONDARY: Check direct sizes only if no scaled export detected
            if width in self.VALID_SIZES and height in self.VALID_SIZES:
                return True, f"Valid dimensions: {width}x{height}", width, height
            
            return False, f"Invalid dimensions: {width}x{height}. Must be 8x8, 16x16, 32x32, 64x64 (or scaled versions)", width, height
                
        except Exception as e:
            return False, f"Error reading PNG: {e}", 0, 0


# Convenience function for direct use
def import_png(png_path: str, pixpf_path: str = None) -> Tuple[bool, str]:
    """
    Quick import function
    
    Args:
        png_path: Path to PNG file
        pixpf_path: Optional output path (defaults to same name with .pixpf)
        
    Returns:
        (success: bool, message: str)
    """
    if pixpf_path is None:
        pixpf_path = os.path.splitext(png_path)[0] + ".pixpf"
    
    importer = PNGImporter()
    return importer.import_png_to_pixpf(png_path, pixpf_path)

