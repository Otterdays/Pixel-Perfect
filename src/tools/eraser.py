"""
Eraser tool for Pixel Perfect
Pixel removal tool

Left-click: Erase pixels (set to transparent)
Right-click: Erase edge lines on canvas
"""

from .base_tool import Tool
from typing import Tuple

class EraserTool(Tool):
    """Eraser tool for removing pixels and edge lines"""
    
    def __init__(self):
        super().__init__("Eraser", cursor="X_cursor")
        self.is_erasing = False
        self.is_erasing_edges = False
        self.main_window = None
    
    def set_main_window(self, window):
        """Set reference to main window for edge tool access"""
        self.main_window = window
    
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Start erasing - left click for pixels, right click for edges"""
        if button == 1:  # Left mouse button - erase pixels
            self.is_erasing = True
            canvas.set_pixel(x, y, (0, 0, 0, 0))  # Transparent
        elif button == 3:  # Right mouse button - erase edge lines
            self.is_erasing_edges = True
            self._erase_edge_at_position(canvas, x, y)
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Stop erasing"""
        if button == 1:
            self.is_erasing = False
        elif button == 3:
            self.is_erasing_edges = False
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Continue erasing while mouse is down"""
        if self.is_erasing:
            canvas.set_pixel(x, y, (0, 0, 0, 0))  # Transparent
    
    def on_right_drag(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Continue erasing edges while right mouse is down"""
        if self.is_erasing_edges:
            self._erase_edge_at_position(canvas, x, y)
    
    def _erase_edge_at_position(self, canvas, x: int, y: int):
        """Erase edge line near the position"""
        if not self.main_window:
            return
        
        edge_tool = self.main_window.tools.get("edge")
        if not edge_tool or not hasattr(edge_tool, 'edge_lines'):
            return
        
        pixel_x = int(x)
        pixel_y = int(y)
        
        if not (0 <= pixel_x < canvas.width and 0 <= pixel_y < canvas.height):
            return
        
        edges_to_remove = []
        for edge_data in edge_tool.edge_lines:
            ex = edge_data['pixel_x']
            ey = edge_data['pixel_y']
            edge = edge_data['edge']
            
            if self._is_edge_near_pixel(ex, ey, edge, pixel_x, pixel_y):
                edges_to_remove.append(edge_data)
        
        for edge_data in edges_to_remove:
            edge_tool.edge_lines.remove(edge_data)
        
        if edges_to_remove:
            edge_tool.pending_redraw = True
            edge_tool.redraw_all_edges(force=True)
    
    def _is_edge_near_pixel(self, edge_x: int, edge_y: int, edge_type: str, 
                            pixel_x: int, pixel_y: int) -> bool:
        """Check if an edge is at or adjacent to a pixel position"""
        if edge_x == pixel_x and edge_y == pixel_y:
            return True
        
        if edge_type == 'right' and edge_x + 1 == pixel_x and edge_y == pixel_y:
            return True
        if edge_type == 'left' and edge_x - 1 == pixel_x and edge_y == pixel_y:
            return True
        if edge_type == 'bottom' and edge_x == pixel_x and edge_y + 1 == pixel_y:
            return True
        if edge_type == 'top' and edge_x == pixel_x and edge_y - 1 == pixel_y:
            return True
        
        return False
