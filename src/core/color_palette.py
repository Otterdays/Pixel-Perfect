"""
Color palette management for Pixel Perfect
Handles SNES-inspired palettes and custom color management
"""

import json
import os
from typing import List, Tuple, Dict, Optional
from enum import Enum

class PaletteType(Enum):
    """Types of color palettes"""
    SNES_CLASSIC = "snes_classic"
    CURSE_OF_AROS = "curse_of_aros"
    HEARTWOOD = "heartwood"
    DEFINYA = "definya"
    KAKELE = "kakele"
    RUCOY = "rucoy"
    OLD_SCHOOL_RUNESCAPE = "old_school_runescape"
    CUSTOM = "custom"

class ColorPalette:
    """Color palette management system"""
    
    def __init__(self):
        self.colors: List[Tuple[int, int, int, int]] = []
        self.primary_color = 0  # Index of primary color
        self.secondary_color = 1  # Index of secondary color
        self.palette_name = "Default"
        self.palette_type = PaletteType.CUSTOM
        
        # Load default palette
        self._load_default_palette()
    
    def _load_default_palette(self):
        """Load default SNES-inspired palette"""
        self.colors = [
            (0, 0, 0, 255),        # Black
            (255, 255, 255, 255),  # White
            (128, 128, 128, 255),  # Gray
            (255, 0, 0, 255),      # Red
            (0, 255, 0, 255),      # Green
            (0, 0, 255, 255),      # Blue
            (255, 255, 0, 255),    # Yellow
            (255, 0, 255, 255),    # Magenta
            (0, 255, 255, 255),    # Cyan
            (128, 64, 0, 255),     # Brown
            (255, 128, 0, 255),    # Orange
            (128, 0, 128, 255),    # Purple
            (0, 128, 0, 255),      # Dark Green
            (0, 0, 128, 255),      # Dark Blue
            (128, 128, 0, 255),    # Olive
            (192, 192, 192, 255),  # Light Gray
        ]
        self.palette_name = "SNES Classic"
        self.palette_type = PaletteType.SNES_CLASSIC
    
    def get_preset_palettes(self) -> Dict[str, List[Tuple[int, int, int, int]]]:
        """Get all preset palettes"""
        return {
            "SNES Classic": [
                (0, 0, 0, 255),        # Black
                (255, 255, 255, 255),  # White
                (128, 128, 128, 255),  # Gray
                (255, 0, 0, 255),      # Red
                (0, 255, 0, 255),      # Green
                (0, 0, 255, 255),      # Blue
                (255, 255, 0, 255),    # Yellow
                (255, 0, 255, 255),    # Magenta
                (0, 255, 255, 255),    # Cyan
                (128, 64, 0, 255),     # Brown
                (255, 128, 0, 255),    # Orange
                (128, 0, 128, 255),    # Purple
                (0, 128, 0, 255),      # Dark Green
                (0, 0, 128, 255),      # Dark Blue
                (128, 128, 0, 255),    # Olive
                (192, 192, 192, 255),  # Light Gray
            ],
            
            "Curse of Aros": [
                (45, 45, 45, 255),     # Dark Gray
                (89, 89, 89, 255),     # Medium Gray
                (134, 134, 134, 255),  # Light Gray
                (101, 67, 33, 255),    # Brown
                (139, 90, 43, 255),    # Light Brown
                (67, 101, 33, 255),    # Dark Green
                (90, 139, 43, 255),    # Green
                (33, 67, 101, 255),    # Dark Blue
                (43, 90, 139, 255),    # Blue
                (101, 33, 67, 255),    # Dark Red
                (139, 43, 90, 255),    # Red
                (67, 101, 67, 255),    # Olive
                (90, 139, 90, 255),    # Light Olive
                (33, 33, 33, 255),     # Very Dark
                (200, 200, 200, 255),  # Very Light
                (255, 255, 255, 255),  # White
            ],
            
            "Heartwood Online": [
                (34, 51, 34, 255),     # Dark Forest
                (68, 85, 68, 255),     # Forest
                (102, 119, 102, 255),  # Light Forest
                (51, 68, 34, 255),    # Dark Green
                (85, 102, 68, 255),    # Green
                (119, 136, 102, 255),  # Light Green
                (68, 51, 34, 255),     # Brown
                (102, 85, 68, 255),    # Light Brown
                (136, 119, 102, 255),  # Tan
                (51, 51, 34, 255),     # Dark Olive
                (85, 85, 68, 255),     # Olive
                (119, 119, 102, 255),  # Light Olive
                (34, 34, 34, 255),     # Dark
                (68, 68, 68, 255),     # Medium
                (102, 102, 102, 255),  # Light
                (136, 136, 136, 255),  # Very Light
            ],
            
            "Definya": [
                (0, 0, 0, 255),        # Black
                (255, 255, 255, 255),  # White
                (255, 0, 0, 255),      # Bright Red
                (0, 255, 0, 255),      # Bright Green
                (0, 0, 255, 255),      # Bright Blue
                (255, 255, 0, 255),    # Yellow
                (255, 0, 255, 255),    # Magenta
                (0, 255, 255, 255),    # Cyan
                (128, 0, 0, 255),      # Dark Red
                (0, 128, 0, 255),      # Dark Green
                (0, 0, 128, 255),      # Dark Blue
                (128, 128, 0, 255),    # Dark Yellow
                (128, 0, 128, 255),    # Dark Magenta
                (0, 128, 128, 255),    # Dark Cyan
                (64, 64, 64, 255),     # Dark Gray
                (192, 192, 192, 255),  # Light Gray
            ],
            
            "Kakele Online": [
                (255, 255, 0, 255),    # Bright Yellow
                (255, 128, 0, 255),    # Orange
                (255, 0, 0, 255),      # Red
                (255, 0, 128, 255),    # Pink
                (128, 0, 255, 255),    # Purple
                (0, 0, 255, 255),      # Blue
                (0, 128, 255, 255),    # Light Blue
                (0, 255, 255, 255),    # Cyan
                (0, 255, 128, 255),    # Light Green
                (0, 255, 0, 255),      # Green
                (128, 255, 0, 255),    # Lime
                (255, 255, 128, 255),  # Light Yellow
                (128, 128, 128, 255),  # Gray
                (64, 64, 64, 255),     # Dark Gray
                (192, 192, 192, 255),  # Light Gray
                (255, 255, 255, 255),  # White
            ],
            
            "Rucoy Online": [
                (0, 0, 0, 255),        # Black
                (32, 32, 32, 255),     # Very Dark Gray
                (64, 64, 64, 255),     # Dark Gray
                (96, 96, 96, 255),     # Medium Gray
                (128, 128, 128, 255),  # Gray
                (160, 160, 160, 255), # Light Gray
                (192, 192, 192, 255), # Very Light Gray
                (224, 224, 224, 255), # Almost White
                (255, 255, 255, 255), # White
                (64, 32, 0, 255),     # Dark Brown
                (128, 64, 0, 255),    # Brown
                (192, 96, 0, 255),    # Light Brown
                (0, 64, 0, 255),      # Dark Green
                (0, 128, 0, 255),     # Green
                (0, 192, 0, 255),     # Light Green
                (0, 0, 64, 255),      # Dark Blue
            ],
            
            "Old School RuneScape": [
                (0, 0, 0, 255),        # Black
                (255, 255, 255, 255),  # White
                (139, 69, 19, 255),    # Saddle Brown
                (36, 97, 49, 255),     # Dark Green
                (125, 102, 48, 255),   # Earthy Brown
                (255, 215, 0, 255),    # Gold
                (128, 0, 0, 255),      # Maroon
                (1, 111, 189, 255),    # Deep Blue
                (246, 103, 57, 255),   # Vibrant Orange
                (225, 158, 37, 255),   # Goldenrod
                (112, 128, 144, 255),  # Slate Gray
                (101, 67, 33, 255),    # Dark Brown
                (192, 192, 192, 255),  # Silver
                (76, 105, 38, 255),    # Grass Green
                (70, 70, 70, 255),     # Dark Gray
                (160, 82, 45, 255),    # Sienna
            ]
        }
    
    def load_preset(self, palette_name: str):
        """Load a preset palette"""
        presets = self.get_preset_palettes()
        if palette_name in presets:
            self.colors = presets[palette_name].copy()
            self.palette_name = palette_name
            
            # Set appropriate palette type
            if palette_name == "SNES Classic":
                self.palette_type = PaletteType.SNES_CLASSIC
            elif palette_name == "Curse of Aros":
                self.palette_type = PaletteType.CURSE_OF_AROS
            elif palette_name == "Heartwood Online":
                self.palette_type = PaletteType.HEARTWOOD
            elif palette_name == "Definya":
                self.palette_type = PaletteType.DEFINYA
            elif palette_name == "Kakele Online":
                self.palette_type = PaletteType.KAKELE
            elif palette_name == "Rucoy Online":
                self.palette_type = PaletteType.RUCOY
            elif palette_name == "Old School RuneScape":
                self.palette_type = PaletteType.OLD_SCHOOL_RUNESCAPE
            
            # Ensure we have valid primary/secondary colors
            if self.primary_color >= len(self.colors):
                self.primary_color = 0
            if self.secondary_color >= len(self.colors):
                self.secondary_color = min(1, len(self.colors) - 1)
    
    def add_color(self, color: Tuple[int, int, int, int]):
        """Add a new color to the palette"""
        if len(self.colors) < 16:  # Limit to 16 colors
            self.colors.append(color)
    
    def remove_color(self, index: int):
        """Remove color at given index"""
        if 0 <= index < len(self.colors) and len(self.colors) > 1:
            self.colors.pop(index)
            
            # Adjust primary/secondary indices
            if self.primary_color >= len(self.colors):
                self.primary_color = len(self.colors) - 1
            if self.secondary_color >= len(self.colors):
                self.secondary_color = len(self.colors) - 1
    
    def set_color(self, index: int, color: Tuple[int, int, int, int]):
        """Set color at given index"""
        if 0 <= index < len(self.colors):
            self.colors[index] = color
    
    def get_primary_color(self) -> Tuple[int, int, int, int]:
        """Get primary color"""
        if self.colors and 0 <= self.primary_color < len(self.colors):
            return self.colors[self.primary_color]
        return (0, 0, 0, 255)
    
    def get_secondary_color(self) -> Tuple[int, int, int, int]:
        """Get secondary color"""
        if self.colors and 0 <= self.secondary_color < len(self.colors):
            return self.colors[self.secondary_color]
        return (255, 255, 255, 255)
    
    def set_primary_color(self, index: int):
        """Set primary color index"""
        if 0 <= index < len(self.colors):
            self.primary_color = index
    
    def set_secondary_color(self, index: int):
        """Set secondary color index"""
        if 0 <= index < len(self.colors):
            self.secondary_color = index
    
    def set_primary_color_by_rgba(self, rgba_color: Tuple[int, int, int, int]):
        """Set primary color by RGBA value (add to palette if not exists)"""
        # Check if color already exists in palette
        for i, color in enumerate(self.colors):
            if color == rgba_color:
                self.primary_color = i
                return
        
        # Color doesn't exist, add it to palette
        self.colors.append(rgba_color)
        self.primary_color = len(self.colors) - 1
    
    def swap_colors(self):
        """Swap primary and secondary colors"""
        self.primary_color, self.secondary_color = self.secondary_color, self.primary_color
    
    def save_palette(self, filename: str):
        """Save palette to JSON file"""
        palette_data = {
            "name": self.palette_name,
            "type": self.palette_type.value,
            "colors": self.colors,
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color
        }
        
        with open(filename, 'w') as f:
            json.dump(palette_data, f, indent=2)
    
    def load_palette(self, filename: str):
        """Load palette from JSON file"""
        try:
            with open(filename, 'r') as f:
                palette_data = json.load(f)
            
            self.palette_name = palette_data.get("name", "Custom")
            self.colors = [tuple(color) for color in palette_data.get("colors", [])]
            self.primary_color = palette_data.get("primary_color", 0)
            self.secondary_color = palette_data.get("secondary_color", 1)
            
            # Set palette type
            palette_type_str = palette_data.get("type", "custom")
            try:
                self.palette_type = PaletteType(palette_type_str)
            except ValueError:
                self.palette_type = PaletteType.CUSTOM
                
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error loading palette: {e}")
            self._load_default_palette()
    
    def get_color_count(self) -> int:
        """Get number of colors in palette"""
        return len(self.colors)
    
    def is_empty(self) -> bool:
        """Check if palette is empty"""
        return len(self.colors) == 0
