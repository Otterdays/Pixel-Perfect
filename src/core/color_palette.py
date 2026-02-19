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
    CUSTOM = "custom"

class ColorPalette:
    """Color palette management system"""
    
    def __init__(self):
        self.colors: List[Tuple[int, int, int, int]] = []
        self.primary_color = 0  # Index of primary color
        self.secondary_color = 1  # Index of secondary color
        self.palette_name = "Default"
        self.palette_type = PaletteType.CUSTOM
        # External JSON palettes discovered at runtime: name -> file path
        self._external_palettes: Dict[str, str] = {}
        
        # Load default palette
        self._load_default_palette()
        # Discover external JSON palettes (non-blocking, safe)
        self._scan_external_palettes()
    
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
    
    # Removed hardcoded presets. Palettes are now provided exclusively via JSON files.

    def _get_palettes_dir(self) -> str:
        """Return absolute path to the assets/palettes directory."""
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        return os.path.join(base_dir, "assets", "palettes")

    def _scan_external_palettes(self):
        """Scan assets/palettes for JSON files and index them by name.

        Safely reads the "name" field from each JSON. If missing, uses the stem.
        Ensures names are unique across all discovered JSON files by suffixing " (2)", " (3)", etc.
        """
        try:
            palettes_dir = self._get_palettes_dir()
            if not os.path.isdir(palettes_dir):
                return
            seen_names: set = set()
            for fname in os.listdir(palettes_dir):
                if not fname.lower().endswith(".json"):
                    continue
                fpath = os.path.join(palettes_dir, fname)
                name = os.path.splitext(fname)[0]
                try:
                    with open(fpath, "r") as f:
                        data = json.load(f)
                        file_name = str(data.get("name", name))
                        name = file_name.strip() or name
                except Exception:
                    # Skip malformed files silently to avoid breaking startup
                    continue
                # Ensure unique name across already-seen externals
                final_name = name
                if final_name in seen_names:
                    i = 2
                    while f"{name} ({i})" in seen_names:
                        i += 1
                    final_name = f"{name} ({i})"
                self._external_palettes[final_name] = fpath
                seen_names.add(final_name)
        except Exception:
            # Do not crash app if filesystem scanning fails
            self._external_palettes = {}

    def get_available_palette_names(self) -> List[str]:
        """Return discovered external JSON palette names only, sorted alphabetically."""
        return sorted(self._external_palettes.keys())
    
    # Removed load_preset – palettes are loaded from JSON by name.

    def load_by_name(self, palette_name: str):
        """Load a palette by name from external JSON files."""
        json_path = self._external_palettes.get(palette_name)
        if json_path:
            self.load_palette(json_path)
            # Ensure valid primary/secondary indices
            if self.primary_color >= len(self.colors):
                self.primary_color = 0
            if self.secondary_color >= len(self.colors):
                self.secondary_color = min(1, len(self.colors) - 1)
            return
        # Unknown name; keep current palette but print debug
        print(f"Palette '{palette_name}' not found among JSON palettes.")
    
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
    
    def find_color_in_presets(self, rgb_color: Tuple[int, int, int, int]) -> Optional[Tuple[str, int]]:
        """Search for a color across all discovered JSON palettes.

        Returns:
            Tuple of (palette_name, color_index) if found, None otherwise.
        """
        for palette_name, json_path in self._external_palettes.items():
            try:
                with open(json_path, "r") as f:
                    data = json.load(f)
                colors = [tuple(c) for c in data.get("colors", [])]
                for i, color in enumerate(colors):
                    if tuple(color[:3]) == tuple(rgb_color[:3]):
                        return (palette_name, i)
            except Exception:
                # Skip malformed palettes during search
                continue
        return None
    
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
