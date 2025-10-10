"""
Export system for Pixel Perfect
Handles PNG, GIF, and sprite sheet export
"""

import os
from typing import List, Tuple, Optional
import pygame
from PIL import Image, ImageSequence
import numpy as np

class ExportManager:
    """Manages export functionality"""
    
    def __init__(self):
        self.export_formats = ["PNG", "GIF", "Sprite Sheet"]
        self.scale_factors = [1, 2, 4, 8]
    
    def export_png(self, pixels: np.ndarray, filename: str, scale: int = 1, transparent: bool = True) -> bool:
        """Export pixels as PNG image"""
        try:
            height, width = pixels.shape[:2]
            
            # Create PIL Image from numpy array
            if transparent:
                # RGBA mode
                image = Image.fromarray(pixels, 'RGBA')
            else:
                # RGB mode (remove alpha)
                rgb_pixels = pixels[:, :, :3]
                image = Image.fromarray(rgb_pixels, 'RGB')
            
            # Scale image if needed
            if scale > 1:
                new_size = (width * scale, height * scale)
                image = image.resize(new_size, Image.NEAREST)  # Nearest neighbor for pixel art
            
            # Save image
            image.save(filename, 'PNG')
            return True
            
        except Exception as e:
            print(f"Error exporting PNG: {e}")
            return False
    
    def export_gif(self, frames: List[np.ndarray], filename: str, duration: int = 100, scale: int = 1) -> bool:
        """Export frames as animated GIF"""
        try:
            if not frames:
                return False
            
            pil_frames = []
            
            for frame_pixels in frames:
                # Convert numpy array to PIL Image
                frame_image = Image.fromarray(frame_pixels, 'RGBA')
                
                # Scale if needed
                if scale > 1:
                    height, width = frame_pixels.shape[:2]
                    new_size = (width * scale, height * scale)
                    frame_image = frame_image.resize(new_size, Image.NEAREST)
                
                pil_frames.append(frame_image)
            
            # Save as GIF
            if len(pil_frames) == 1:
                pil_frames[0].save(filename, 'GIF')
            else:
                pil_frames[0].save(
                    filename,
                    'GIF',
                    save_all=True,
                    append_images=pil_frames[1:],
                    duration=duration,
                    loop=0  # Infinite loop
                )
            
            return True
            
        except Exception as e:
            print(f"Error exporting GIF: {e}")
            return False
    
    def export_sprite_sheet(self, frames: List[np.ndarray], filename: str, layout: str = "horizontal", 
                           scale: int = 1, spacing: int = 1) -> bool:
        """Export frames as sprite sheet"""
        try:
            if not frames:
                return False
            
            frame_height, frame_width = frames[0].shape[:2]
            frame_count = len(frames)
            
            # Calculate sprite sheet dimensions
            if layout == "horizontal":
                sheet_width = (frame_width * frame_count) + (spacing * (frame_count - 1))
                sheet_height = frame_height
                cols = frame_count
                rows = 1
            elif layout == "vertical":
                sheet_width = frame_width
                sheet_height = (frame_height * frame_count) + (spacing * (frame_count - 1))
                cols = 1
                rows = frame_count
            elif layout == "grid":
                # Try to make a square-ish grid
                cols = int(np.ceil(np.sqrt(frame_count)))
                rows = int(np.ceil(frame_count / cols))
                sheet_width = (frame_width * cols) + (spacing * (cols - 1))
                sheet_height = (frame_height * rows) + (spacing * (rows - 1))
            else:
                return False
            
            # Scale dimensions if needed
            if scale > 1:
                frame_width *= scale
                frame_height *= scale
                sheet_width *= scale
                sheet_height *= scale
                spacing *= scale
            
            # Create sprite sheet image
            sheet_image = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))
            
            # Place frames on sprite sheet
            for i, frame_pixels in enumerate(frames):
                # Convert to PIL Image
                frame_image = Image.fromarray(frame_pixels, 'RGBA')
                
                # Scale if needed
                if scale > 1:
                    frame_image = frame_image.resize((frame_width, frame_height), Image.NEAREST)
                
                # Calculate position
                if layout == "horizontal":
                    x = i * (frame_width + spacing)
                    y = 0
                elif layout == "vertical":
                    x = 0
                    y = i * (frame_height + spacing)
                else:  # grid
                    col = i % cols
                    row = i // cols
                    x = col * (frame_width + spacing)
                    y = row * (frame_height + spacing)
                
                # Paste frame onto sprite sheet
                sheet_image.paste(frame_image, (x, y), frame_image)
            
            # Save sprite sheet
            sheet_image.save(filename, 'PNG')
            
            # Create metadata file (JSON)
            metadata_filename = filename.replace('.png', '_metadata.json')
            self._create_sprite_sheet_metadata(
                metadata_filename, frame_count, frame_width, frame_height,
                cols, rows, layout, scale
            )
            
            return True
            
        except Exception as e:
            print(f"Error exporting sprite sheet: {e}")
            return False
    
    def _create_sprite_sheet_metadata(self, filename: str, frame_count: int, frame_width: int, 
                                    frame_height: int, cols: int, rows: int, layout: str, scale: int):
        """Create metadata file for sprite sheet"""
        import json
        
        metadata = {
            "frame_count": frame_count,
            "frame_width": frame_width,
            "frame_height": frame_height,
            "cols": cols,
            "rows": rows,
            "layout": layout,
            "scale": scale,
            "frames": []
        }
        
        # Calculate frame positions
        for i in range(frame_count):
            if layout == "horizontal":
                x = i * frame_width
                y = 0
            elif layout == "vertical":
                x = 0
                y = i * frame_height
            else:  # grid
                col = i % cols
                row = i // cols
                x = col * frame_width
                y = row * frame_height
            
            metadata["frames"].append({
                "index": i,
                "x": x,
                "y": y,
                "width": frame_width,
                "height": frame_height
            })
        
        try:
            with open(filename, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            print(f"Error creating metadata file: {e}")
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported export formats"""
        return self.export_formats.copy()
    
    def get_scale_factors(self) -> List[int]:
        """Get list of supported scale factors"""
        return self.scale_factors.copy()
