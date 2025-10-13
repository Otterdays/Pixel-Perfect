"""
Saved Colors Manager for Pixel Perfect
Manages user's personally saved color palettes (local storage, not in git)
"""

import json
import os
from typing import List, Tuple, Optional

class SavedColorsManager:
    """Manages saved colors in local user storage"""
    
    def __init__(self, max_colors: int = 24):
        self.max_colors = max_colors
        self.colors: List[Optional[Tuple[int, int, int, int]]] = [None] * max_colors
        self.storage_path = self._get_storage_path()
        self._load_colors()
    
    def _get_storage_path(self) -> str:
        """Get path to user's local storage file (not in git)"""
        # Use AppData on Windows, home directory on other systems
        if os.name == 'nt':  # Windows
            app_data = os.getenv('APPDATA')
            if app_data:
                pixel_perfect_dir = os.path.join(app_data, 'PixelPerfect')
            else:
                # Fallback to local directory
                pixel_perfect_dir = os.path.join(os.path.expanduser('~'), '.pixelperfect')
        else:  # macOS, Linux
            pixel_perfect_dir = os.path.join(os.path.expanduser('~'), '.pixelperfect')
        
        # Create directory if it doesn't exist
        os.makedirs(pixel_perfect_dir, exist_ok=True)
        
        return os.path.join(pixel_perfect_dir, 'saved_colors.json')
    
    def _load_colors(self):
        """Load saved colors from local storage"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    # Convert lists back to tuples, handle None values
                    self.colors = [
                        tuple(color) if color is not None else None 
                        for color in data.get('colors', [None] * self.max_colors)
                    ]
                    # Ensure we have the right number of slots
                    while len(self.colors) < self.max_colors:
                        self.colors.append(None)
                    self.colors = self.colors[:self.max_colors]
                print(f"[SAVED COLORS] Loaded from: {self.storage_path}")
        except Exception as e:
            print(f"[SAVED COLORS] Error loading: {e}")
            self.colors = [None] * self.max_colors
    
    def _save_colors(self):
        """Save colors to local storage"""
        try:
            data = {
                'colors': self.colors,  # JSON handles tuples as lists automatically
                'max_colors': self.max_colors
            }
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"[SAVED COLORS] Saved to: {self.storage_path}")
        except Exception as e:
            print(f"[SAVED COLORS] Error saving: {e}")
    
    def set_color(self, slot_index: int, color: Tuple[int, int, int, int]):
        """Save a color to a specific slot"""
        if 0 <= slot_index < self.max_colors:
            self.colors[slot_index] = color
            self._save_colors()
    
    def get_color(self, slot_index: int) -> Optional[Tuple[int, int, int, int]]:
        """Get color from a specific slot"""
        if 0 <= slot_index < self.max_colors:
            return self.colors[slot_index]
        return None
    
    def clear_slot(self, slot_index: int):
        """Clear a specific color slot"""
        if 0 <= slot_index < self.max_colors:
            self.colors[slot_index] = None
            self._save_colors()
    
    def clear_all(self):
        """Clear all saved colors"""
        self.colors = [None] * self.max_colors
        self._save_colors()
    
    def export_to_file(self, filepath: str):
        """Export saved colors to a JSON file"""
        try:
            # Filter out None values for export
            export_data = {
                'colors': [color for color in self.colors if color is not None],
                'format': 'PixelPerfect Saved Colors v1.0'
            }
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            print(f"[SAVED COLORS] Exported to: {filepath}")
            return True
        except Exception as e:
            print(f"[SAVED COLORS] Export error: {e}")
            return False
    
    def import_from_file(self, filepath: str) -> bool:
        """Import saved colors from a JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                imported_colors = data.get('colors', [])
                # Import up to max_colors
                for i, color in enumerate(imported_colors[:self.max_colors]):
                    if color is not None:
                        self.colors[i] = tuple(color)
            self._save_colors()
            print(f"[SAVED COLORS] Imported from: {filepath}")
            return True
        except Exception as e:
            print(f"[SAVED COLORS] Import error: {e}")
            return False

