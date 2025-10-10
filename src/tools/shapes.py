"""
Shape tools for Pixel Perfect
Line, rectangle, and circle drawing tools
"""

from .base_tool import Tool
from typing import Tuple, List
import pygame
import math

class LineTool(Tool):
    """Pixel-perfect line drawing tool"""
    
    def __init__(self):
        super().__init__("Line")
        self.is_drawing = False
        self.start_point = (0, 0)
        self.end_point = (0, 0)
    
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Start line drawing"""
        if button == 1:  # Left mouse button
            self.is_drawing = True
            self.start_point = (x, y)
            self.end_point = (x, y)
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Finish line drawing"""
        if button == 1 and self.is_drawing:
            self.is_drawing = False
            self.end_point = (x, y)
            self._draw_line(canvas, self.start_point, self.end_point, color)
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Update line preview"""
        if self.is_drawing:
            self.end_point = (x, y)
    
    def _draw_line(self, canvas, start: Tuple[int, int], end: Tuple[int, int], color: Tuple[int, int, int, int]):
        """Draw a pixel-perfect line using Bresenham's algorithm"""
        x0, y0 = start
        x1, y1 = end
        
        # Bresenham's line algorithm
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while True:
            canvas.set_pixel(x0, y0, color)
            
            if x0 == x1 and y0 == y1:
                break
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
    
    def draw_preview(self, surface: pygame.Surface, x: int, y: int, color: Tuple[int, int, int, int]):
        """Draw line preview"""
        if self.is_drawing:
            pygame.draw.line(surface, color[:3], self.start_point, (x, y), 1)

class RectangleTool(Tool):
    """Rectangle drawing tool"""
    
    def __init__(self):
        super().__init__("Rectangle")
        self.is_drawing = False
        self.start_point = (0, 0)
        self.end_point = (0, 0)
        self.filled = False
    
    def set_filled(self, filled: bool):
        """Set whether rectangle should be filled"""
        self.filled = filled
    
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Start rectangle drawing"""
        if button == 1:  # Left mouse button
            self.is_drawing = True
            self.start_point = (x, y)
            self.end_point = (x, y)
        elif button == 3:  # Right mouse button - toggle fill mode
            self.filled = not self.filled
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Finish rectangle drawing"""
        if button == 1 and self.is_drawing:
            self.is_drawing = False
            self.end_point = (x, y)
            self._draw_rectangle(canvas, self.start_point, self.end_point, color)
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Update rectangle preview"""
        if self.is_drawing:
            self.end_point = (x, y)
    
    def _draw_rectangle(self, canvas, start: Tuple[int, int], end: Tuple[int, int], color: Tuple[int, int, int, int]):
        """Draw rectangle"""
        x1, y1 = start
        x2, y2 = end
        
        left = min(x1, x2)
        right = max(x1, x2)
        top = min(y1, y2)
        bottom = max(y1, y2)
        
        if self.filled:
            # Fill rectangle
            for y in range(top, bottom + 1):
                for x in range(left, right + 1):
                    canvas.set_pixel(x, y, color)
        else:
            # Draw rectangle outline
            for x in range(left, right + 1):
                canvas.set_pixel(x, top, color)
                canvas.set_pixel(x, bottom, color)
            for y in range(top, bottom + 1):
                canvas.set_pixel(left, y, color)
                canvas.set_pixel(right, y, color)
    
    def draw_preview(self, surface: pygame.Surface, x: int, y: int, color: Tuple[int, int, int, int]):
        """Draw rectangle preview"""
        if self.is_drawing:
            x1, y1 = self.start_point
            x2, y2 = (x, y)
            left = min(x1, x2)
            right = max(x1, x2)
            top = min(y1, y2)
            bottom = max(y1, y2)
            
            if self.filled:
                pygame.draw.rect(surface, color[:3], (left, top, right - left, bottom - top))
            else:
                pygame.draw.rect(surface, color[:3], (left, top, right - left, bottom - top), 1)

class CircleTool(Tool):
    """Circle drawing tool"""
    
    def __init__(self):
        super().__init__("Circle")
        self.is_drawing = False
        self.center = (0, 0)
        self.radius = 0
        self.filled = False
    
    def set_filled(self, filled: bool):
        """Set whether circle should be filled"""
        self.filled = filled
    
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Start circle drawing"""
        if button == 1:  # Left mouse button
            self.is_drawing = True
            self.center = (x, y)
            self.radius = 0
        elif button == 3:  # Right mouse button - toggle fill mode
            self.filled = not self.filled
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Finish circle drawing"""
        if button == 1 and self.is_drawing:
            self.is_drawing = False
            dx = x - self.center[0]
            dy = y - self.center[1]
            self.radius = int(math.sqrt(dx * dx + dy * dy))
            self._draw_circle(canvas, self.center, self.radius, color)
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Update circle preview"""
        if self.is_drawing:
            dx = x - self.center[0]
            dy = y - self.center[1]
            self.radius = int(math.sqrt(dx * dx + dy * dy))
    
    def _draw_circle(self, canvas, center: Tuple[int, int], radius: int, color: Tuple[int, int, int, int]):
        """Draw circle using midpoint circle algorithm"""
        x0, y0 = center
        
        if self.filled:
            # Fill circle
            for y in range(-radius, radius + 1):
                for x in range(-radius, radius + 1):
                    if x * x + y * y <= radius * radius:
                        canvas.set_pixel(x0 + x, y0 + y, color)
        else:
            # Draw circle outline
            x = 0
            y = radius
            d = 1 - radius
            
            while x <= y:
                # Draw 8 symmetric points
                points = [
                    (x0 + x, y0 + y), (x0 + y, y0 + x),
                    (x0 - x, y0 + y), (x0 - y, y0 + x),
                    (x0 + x, y0 - y), (x0 + y, y0 - x),
                    (x0 - x, y0 - y), (x0 - y, y0 - x)
                ]
                
                for px, py in points:
                    canvas.set_pixel(px, py, color)
                
                if d < 0:
                    d += 2 * x + 3
                else:
                    d += 2 * (x - y) + 5
                    y -= 1
                x += 1
    
    def draw_preview(self, surface: pygame.Surface, x: int, y: int, color: Tuple[int, int, int, int]):
        """Draw circle preview"""
        if self.is_drawing and self.radius > 0:
            if self.filled:
                pygame.draw.circle(surface, color[:3], self.center, self.radius)
            else:
                pygame.draw.circle(surface, color[:3], self.center, self.radius, 1)
