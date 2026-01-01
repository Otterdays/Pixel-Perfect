"""
Recent Colors Manager for Pixel Perfect
Tracks recently used colors for quick access

This provides a "Recent Colors" feature that shows the last N colors
the user has actually used while drawing.
"""

from typing import List, Tuple, Optional, Callable
import json
import os


class RecentColorsManager:
    """
    Manages a list of recently used colors.
    
    Features:
    - Tracks last 16 colors used
    - No duplicates (most recent use moves color to front)
    - Persists across sessions
    - Callback for UI updates
    """
    
    MAX_RECENT = 16
    
    def __init__(self, save_path: Optional[str] = None):
        """
        Initialize the recent colors manager.
        
        Args:
            save_path: Optional path to save/load recent colors.
                       If None, colors won't persist across sessions.
        """
        self.recent: List[Tuple[int, int, int, int]] = []
        self.save_path = save_path
        self.on_colors_changed: Optional[Callable] = None
        
        # Load saved colors if path provided
        if self.save_path:
            self._load()
    
    def add_color(self, color: Tuple[int, int, int, int]):
        """
        Add a color to the recent colors list.
        
        If the color already exists, it's moved to the front.
        The list is limited to MAX_RECENT colors.
        
        Args:
            color: RGBA color tuple
        """
        color = tuple(color)
        
        # Skip transparent colors
        if color[3] == 0:
            return
        
        # Remove if already exists (we'll add it to front)
        if color in self.recent:
            self.recent.remove(color)
        
        # Add to front of list
        self.recent.insert(0, color)
        
        # Limit size
        if len(self.recent) > self.MAX_RECENT:
            self.recent = self.recent[:self.MAX_RECENT]
        
        # Notify listeners
        if self.on_colors_changed:
            self.on_colors_changed()
        
        # Auto-save
        if self.save_path:
            self._save()
    
    def get_colors(self) -> List[Tuple[int, int, int, int]]:
        """Get the list of recent colors (most recent first)."""
        return self.recent.copy()
    
    def clear(self):
        """Clear all recent colors."""
        self.recent.clear()
        
        if self.on_colors_changed:
            self.on_colors_changed()
        
        if self.save_path:
            self._save()
    
    def get_color_at(self, index: int) -> Optional[Tuple[int, int, int, int]]:
        """Get color at a specific index, or None if out of range."""
        if 0 <= index < len(self.recent):
            return self.recent[index]
        return None
    
    def _save(self):
        """Save recent colors to file."""
        if not self.save_path:
            return
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
            
            data = {
                "recent_colors": [list(c) for c in self.recent]
            }
            
            with open(self.save_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass  # Silently fail on save errors
    
    def _load(self):
        """Load recent colors from file."""
        if not self.save_path or not os.path.exists(self.save_path):
            return
        
        try:
            with open(self.save_path, 'r') as f:
                data = json.load(f)
            
            colors = data.get("recent_colors", [])
            self.recent = [tuple(c) for c in colors[:self.MAX_RECENT]]
        except Exception:
            pass  # Silently fail on load errors
