"""
Spray tool for Pixel Perfect
Simulates spray paint with circular radius and droplet density
"""

from typing import Tuple
from .base_tool import Tool


class SprayTool(Tool):
    """Spray paint tool with continuous droplet application while dragging."""

    def __init__(self):
        super().__init__("Spray", cursor="spraycan")
        self.is_spraying = False

    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Start spraying (actual pixel placement handled by ToolSizeManager)."""
        if button == 1:
            self.is_spraying = True

    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Stop spraying."""
        self.is_spraying = False

    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """During spray drag, dispatcher calls ToolSizeManager to place droplets."""
        # Intentionally empty; spraying handled by EventDispatcher using ToolSizeManager
        pass