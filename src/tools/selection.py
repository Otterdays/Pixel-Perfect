"""
Selection tools for Pixel Perfect
Rectangle selection and move functionality
"""

from .base_tool import Tool
from typing import Tuple, Optional, List
import pygame

class SelectionTool(Tool):
    """Rectangle selection tool"""
    
    def __init__(self):
        super().__init__("Selection")
        self.is_selecting = False
        self.selection_start = (0, 0)
        self.selection_end = (0, 0)
        self.selection_rect = None
        self.selected_pixels = None
        self.has_selection = False
    
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Start selection"""
        if button == 1:  # Left mouse button
            self.is_selecting = True
            self.selection_start = (x, y)
            self.selection_end = (x, y)
            self.has_selection = False
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """End selection"""
        if button == 1 and self.is_selecting:
            self.is_selecting = False
            self.selection_end = (x, y)
            self._finalize_selection(canvas)
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Update selection while dragging"""
        if self.is_selecting:
            self.selection_end = (x, y)
            self._update_selection_rect()
    
    def _update_selection_rect(self):
        """Update selection rectangle"""
        x1, y1 = self.selection_start
        x2, y2 = self.selection_end
        
        # Calculate rectangle bounds
        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        self.selection_rect = (left, top, width, height)
    
    def _finalize_selection(self, canvas):
        """Finalize the selection and capture pixels"""
        if not self.selection_rect:
            return
        
        left, top, width, height = self.selection_rect
        
        # Clamp to canvas bounds
        left = max(0, min(left, canvas.width))
        top = max(0, min(top, canvas.height))
        width = min(width, canvas.width - left)
        height = min(height, canvas.height - top)
        
        if width <= 0 or height <= 0:
            self.has_selection = False
            return
        
        # Capture selected pixels
        self.selected_pixels = np.zeros((height, width, 4), dtype=np.uint8)
        
        for y in range(height):
            for x in range(width):
                canvas_x = left + x
                canvas_y = top + y
                if 0 <= canvas_x < canvas.width and 0 <= canvas_y < canvas.height:
                    self.selected_pixels[y, x] = canvas.get_pixel(canvas_x, canvas_y)
        
        self.has_selection = True
        self.selection_rect = (left, top, width, height)
    
    def clear_selection(self):
        """Clear current selection"""
        self.has_selection = False
        self.selection_rect = None
        self.selected_pixels = None
        self.is_selecting = False
    
    def get_selection_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get selection bounds (left, top, width, height)"""
        return self.selection_rect
    
    def has_active_selection(self) -> bool:
        """Check if there's an active selection"""
        return self.has_selection
    
    def draw_preview(self, surface: pygame.Surface, x: int, y: int, color: Tuple[int, int, int, int]):
        """Draw selection preview"""
        if self.is_selecting and self.selection_rect:
            left, top, width, height = self.selection_rect
            rect = pygame.Rect(left, top, width, height)
            pygame.draw.rect(surface, (255, 255, 255), rect, 1)

class MoveTool(Tool):
    """Move selection tool"""
    
    def __init__(self):
        super().__init__("Move")
        self.is_moving = False
        self.move_offset = (0, 0)
        self.original_selection = None
        self.selection_tool = None
    
    def set_selection_tool(self, selection_tool: SelectionTool):
        """Set reference to selection tool"""
        self.selection_tool = selection_tool
    
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Start moving selection"""
        if (button == 1 and self.selection_tool and 
            self.selection_tool.has_active_selection()):
            
            bounds = self.selection_tool.get_selection_bounds()
            if bounds:
                left, top, width, height = bounds
                # Check if click is within selection
                if left <= x < left + width and top <= y < top + height:
                    self.is_moving = True
                    self.move_offset = (x - left, y - top)
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """End moving selection"""
        if button == 1 and self.is_moving:
            self.is_moving = False
            # Selection tool will handle the final placement
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Update selection position while moving"""
        if self.is_moving and self.selection_tool:
            bounds = self.selection_tool.get_selection_bounds()
            if bounds:
                left, top, width, height = bounds
                new_left = x - self.move_offset[0]
                new_top = y - self.move_offset[1]
                
                # Update selection position
                self.selection_tool.selection_rect = (new_left, new_top, width, height)
    
    def draw_preview(self, surface: pygame.Surface, x: int, y: int, color: Tuple[int, int, int, int]):
        """Draw move preview"""
        if self.is_moving and self.selection_tool:
            bounds = self.selection_tool.get_selection_bounds()
            if bounds:
                left, top, width, height = bounds
                rect = pygame.Rect(left, top, width, height)
                pygame.draw.rect(surface, (0, 255, 0), rect, 2)
