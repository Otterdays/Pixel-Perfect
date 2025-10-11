"""
Custom colors manager for Pixel Perfect
User-specific color storage with local persistence
"""

import json
import os
from typing import List, Tuple
from pathlib import Path


class CustomColorManager:
    """Manages user-specific custom colors with local storage"""
    
    def __init__(self):
        self.custom_colors: List[Tuple[int, int, int, int]] = []
        self.max_colors = 32  # Allow up to 32 custom colors
        
        # Set up user-specific storage path
        self.storage_path = self._get_user_storage_path()
        self.colors_file = self.storage_path / "custom_colors.json"
        
        # Ensure storage directory exists
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Load existing colors or create empty storage
        self._load_colors()
    
    def _get_user_storage_path(self) -> Path:
        """Get user-specific storage path (OS-independent)"""
        if os.name == 'nt':  # Windows
            # Use AppData/Local/PixelPerfect
            base_path = Path(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')))
            return base_path / 'PixelPerfect'
        else:  # Mac/Linux
            # Use ~/.pixelperfect
            return Path.home() / '.pixelperfect'
    
    def _load_colors(self):
        """Load custom colors from user's storage"""
        try:
            if self.colors_file.exists():
                with open(self.colors_file, 'r') as f:
                    data = json.load(f)
                    # Convert lists back to tuples
                    self.custom_colors = [tuple(color) for color in data.get('colors', [])]
                print(f"Loaded {len(self.custom_colors)} custom colors from {self.colors_file}")
            else:
                # First time - create empty storage
                self.custom_colors = []
                self._save_colors()
                print(f"Created new custom colors storage at {self.colors_file}")
        except Exception as e:
            print(f"Error loading custom colors: {e}")
            self.custom_colors = []
    
    def _save_colors(self):
        """Save custom colors to user's storage"""
        try:
            data = {
                'colors': self.custom_colors,
                'version': '1.0',
                'max_colors': self.max_colors
            }
            with open(self.colors_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Saved {len(self.custom_colors)} custom colors")
        except Exception as e:
            print(f"Error saving custom colors: {e}")
    
    def add_color(self, color: Tuple[int, int, int, int]) -> bool:
        """Add a new custom color"""
        # Check if color already exists
        if color in self.custom_colors:
            print(f"Color {color} already in custom colors")
            return False
        
        # Check color limit
        if len(self.custom_colors) >= self.max_colors:
            print(f"Custom colors limit reached ({self.max_colors})")
            return False
        
        # Add color
        self.custom_colors.append(color)
        self._save_colors()
        print(f"Added custom color {color}")
        return True
    
    def remove_color(self, index: int) -> bool:
        """Remove custom color at index"""
        if 0 <= index < len(self.custom_colors):
            removed = self.custom_colors.pop(index)
            self._save_colors()
            print(f"Removed custom color {removed}")
            return True
        return False
    
    def remove_color_by_value(self, color: Tuple[int, int, int, int]) -> bool:
        """Remove custom color by value"""
        if color in self.custom_colors:
            self.custom_colors.remove(color)
            self._save_colors()
            print(f"Removed custom color {color}")
            return True
        return False
    
    def clear_all(self):
        """Clear all custom colors"""
        self.custom_colors = []
        self._save_colors()
        print("Cleared all custom colors")
    
    def get_colors(self) -> List[Tuple[int, int, int, int]]:
        """Get all custom colors"""
        return self.custom_colors.copy()
    
    def get_color_count(self) -> int:
        """Get number of custom colors"""
        return len(self.custom_colors)
    
    def is_full(self) -> bool:
        """Check if custom colors storage is full"""
        return len(self.custom_colors) >= self.max_colors
    
    def has_color(self, color: Tuple[int, int, int, int]) -> bool:
        """Check if color exists in custom colors"""
        return color in self.custom_colors
    
    def get_storage_info(self) -> dict:
        """Get storage location info for debugging"""
        return {
            'storage_path': str(self.storage_path),
            'colors_file': str(self.colors_file),
            'file_exists': self.colors_file.exists(),
            'color_count': len(self.custom_colors),
            'max_colors': self.max_colors,
            'is_full': self.is_full()
        }

