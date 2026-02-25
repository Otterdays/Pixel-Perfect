import json
import os
import glob

palettes_data = {}
for path in glob.glob('assets/palettes/*.json'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            name = data.get('name', os.path.basename(path).replace('.json', ''))
            palettes_data[name] = data
    except Exception as e:
        print(f'Failed to load {path}: {e}')

code = f'''"""
Color palette management for Pixel Perfect
Handles SNES-inspired palettes and custom color management
"""

import json
from typing import List, Tuple, Dict, Optional
from enum import Enum

class PaletteType(Enum):
    """Types of color palettes"""
    SNES_CLASSIC = "snes_classic"
    CUSTOM = "custom"

# Hardcoded JSON data to fix portable executable issue
HARDCODED_PALETTES_DATA = {json.dumps(palettes_data, indent=4)}

class ColorPalette:
    """Color palette management system"""
    
    def __init__(self):
        self.colors: List[Tuple[int, int, int, int]] = []
        self.primary_color = 0  # Index of primary color
        self.secondary_color = 1  # Index of secondary color
        self.palette_name = "Default"
        self.palette_type = PaletteType.CUSTOM
        
        self._hardcoded_palettes = HARDCODED_PALETTES_DATA
        
        # Load default palette
        self._load_default_palette()
    
    def _load_default_palette(self):
        """Load default SNES-inspired palette"""
        self.load_by_name("SNES Classic")

    def get_available_palette_names(self) -> List[str]:
        """Return available hardcoded palette names, sorted alphabetically."""
        return sorted(list(self._hardcoded_palettes.keys()))
    
    def _load_from_dict(self, data: dict):
        """Internal helper to load from a dictionary"""
        self.palette_name = data.get("name", "Custom")
        self.colors = [tuple(color) for color in data.get("colors", [])]
        self.primary_color = data.get("primary_color", 0)
        self.secondary_color = data.get("secondary_color", 1)
        
        # Set palette type
        palette_type_str = data.get("type", "custom")
        try:
            self.palette_type = PaletteType(palette_type_str)
        except ValueError:
            self.palette_type = PaletteType.CUSTOM

    def load_by_name(self, palette_name: str):
        """Load a hardcoded palette by name."""
        if palette_name in self._hardcoded_palettes:
            data = self._hardcoded_palettes[palette_name]
            self._load_from_dict(data)
            # Ensure valid primary/secondary indices
            if self.primary_color >= len(self.colors):
                self.primary_color = 0
            if self.secondary_color >= len(self.colors):
                self.secondary_color = min(1, len(self.colors) - 1)
            return
        print(f"Palette '{{palette_name}}' not found among hardcoded palettes.")
    
    def add_color(self, color: Tuple[int, int, int, int]):
        """Add a new color to the palette"""
        if len(self.colors) < 32:  # Limit to 32 colors
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
        for i, color in enumerate(self.colors):
            if color == rgba_color:
                self.primary_color = i
                return
        self.colors.append(rgba_color)
        self.primary_color = len(self.colors) - 1
    
    def swap_colors(self):
        """Swap primary and secondary colors"""
        self.primary_color, self.secondary_color = self.secondary_color, self.primary_color
    
    def find_color_in_presets(self, rgb_color: Tuple[int, int, int, int]) -> Optional[Tuple[str, int]]:
        """Search for a color across all hardcoded palettes."""
        for palette_name, data in self._hardcoded_palettes.items():
            try:
                colors = [tuple(c) for c in data.get("colors", [])]
                for i, color in enumerate(colors):
                    if tuple(color[:3]) == tuple(rgb_color[:3]):
                        return (palette_name, i)
            except Exception:
                continue
        return None
    
    def save_palette(self, filename: str):
        """Save palette to JSON file"""
        palette_data = {{
            "name": self.palette_name,
            "type": self.palette_type.value,
            "colors": self.colors,
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color
        }}
        with open(filename, 'w') as f:
            json.dump(palette_data, f, indent=2)
    
    def load_palette(self, filename: str):
        """Load palette from JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self._load_from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error loading palette: {{e}}")
            self._load_default_palette()
    
    def get_color_count(self) -> int:
        """Get number of colors in palette"""
        return len(self.colors)
    
    def is_empty(self) -> bool:
        """Check if palette is empty"""
        return len(self.colors) == 0
'''

with open('src/core/color_palette.py', 'w', encoding='utf-8') as f:
    f.write(code)
