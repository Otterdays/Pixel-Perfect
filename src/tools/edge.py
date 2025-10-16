"""
Edge Tool for Pixel Perfect
Draws thin edge lines between pixels
"""

from .base_tool import Tool
from typing import Tuple, Optional
import math

class EdgeTool(Tool):
    """Tool for drawing thin edge lines between pixels"""
    
    def __init__(self):
        super().__init__("Edge", cursor="crosshair")
        self.is_drawing = False
        self.hovered_pixel = None
        self.hovered_edge = None
        self.main_window = None  # Will be set by the main window
        self.edge_lines = []  # Store drawn edge lines persistently
        
    def set_main_window(self, main_window):
        """Set reference to main window for canvas access"""
        self.main_window = main_window
        
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Start edge drawing"""
        if button == 1:  # Left mouse button
            self.is_drawing = True
            self._draw_edge_at_position(canvas, x, y, color)
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Stop edge drawing"""
        self.is_drawing = False
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Handle mouse movement for hover preview and drawing"""
        # Update hover preview
        self._update_hover_preview(canvas, x, y, color)
        
        # Continue drawing if mouse is down
        if self.is_drawing:
            self._draw_edge_at_position(canvas, x, y, color)
    
    def _update_hover_preview(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Update hover preview for edge detection"""
        if not self.main_window:
            return
            
        # Get the pixel coordinates
        pixel_x = int(x)
        pixel_y = int(y)
        
        # Check if we're hovering over a valid pixel
        if not (0 <= pixel_x < canvas.width and 0 <= pixel_y < canvas.height):
            self._clear_preview()
            self.hovered_pixel = None
            self.hovered_edge = None
            return
        
        # Get mouse position within the pixel (0.0 to 1.0)
        mouse_in_pixel_x = x - pixel_x
        mouse_in_pixel_y = y - pixel_y
        
        # Determine which edge we're closest to
        edge = self._detect_edge_hover(mouse_in_pixel_x, mouse_in_pixel_y)
        
        # Update hover state
        if edge:
            self.hovered_pixel = (pixel_x, pixel_y)
            self.hovered_edge = edge
            self._draw_preview(pixel_x, pixel_y, edge, color)
        else:
            self._clear_preview()
            self.hovered_pixel = None
            self.hovered_edge = None
    
    def _detect_edge_hover(self, mouse_x: float, mouse_y: float) -> Optional[str]:
        """Detect which edge of a pixel the mouse is hovering over"""
        # Define edge detection zones (0.1 pixel width on each side)
        edge_zone = 0.1
        
        # Check top edge
        if mouse_y <= edge_zone:
            return "top"
        
        # Check bottom edge
        elif mouse_y >= (1.0 - edge_zone):
            return "bottom"
        
        # Check left edge
        elif mouse_x <= edge_zone:
            return "left"
        
        # Check right edge
        elif mouse_x >= (1.0 - edge_zone):
            return "right"
        
        # Not hovering over an edge
        return None
    
    def _draw_preview(self, pixel_x: int, pixel_y: int, edge: str, color: Tuple[int, int, int, int]):
        """Draw preview of edge line"""
        if not self.main_window:
            return
            
        # Clear any existing preview
        self._clear_preview()
        
        drawing_canvas = self.main_window.drawing_canvas
        zoom = self.main_window.canvas.zoom
        
        # Calculate screen coordinates for the edge line
        x_offset, y_offset = self._get_canvas_offsets()
        
        # Convert color to hex string
        color_hex = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        
        # Draw preview line based on edge type
        if edge == "top":
            # Draw horizontal line above pixel
            screen_x1 = x_offset + (pixel_x * zoom)
            screen_x2 = x_offset + ((pixel_x + 1) * zoom)
            screen_y = y_offset + (pixel_y * zoom)
            
            drawing_canvas.create_line(
                screen_x1, screen_y,
                screen_x2, screen_y,
                fill=color_hex, width=2, tags="edge_preview"
            )
        
        elif edge == "bottom":
            # Draw horizontal line below pixel
            screen_x1 = x_offset + (pixel_x * zoom)
            screen_x2 = x_offset + ((pixel_x + 1) * zoom)
            screen_y = y_offset + ((pixel_y + 1) * zoom)
            
            drawing_canvas.create_line(
                screen_x1, screen_y,
                screen_x2, screen_y,
                fill=color_hex, width=2, tags="edge_preview"
            )
        
        elif edge == "left":
            # Draw vertical line to the left of pixel
            screen_x = x_offset + (pixel_x * zoom)
            screen_y1 = y_offset + (pixel_y * zoom)
            screen_y2 = y_offset + ((pixel_y + 1) * zoom)
            
            drawing_canvas.create_line(
                screen_x, screen_y1,
                screen_x, screen_y2,
                fill=color_hex, width=2, tags="edge_preview"
            )
        
        elif edge == "right":
            # Draw vertical line to the right of pixel
            screen_x = x_offset + ((pixel_x + 1) * zoom)
            screen_y1 = y_offset + (pixel_y * zoom)
            screen_y2 = y_offset + ((pixel_y + 1) * zoom)
            
            drawing_canvas.create_line(
                screen_x, screen_y1,
                screen_x, screen_y2,
                fill=color_hex, width=2, tags="edge_preview"
            )
    
    def _clear_preview(self):
        """Clear the current preview line"""
        if self.main_window:
            self.main_window.drawing_canvas.delete("edge_preview")
    
    def _get_canvas_offsets(self):
        """Calculate canvas offsets the same way as canvas renderer"""
        if not self.main_window:
            return 0, 0
            
        # Get canvas dimensions
        width = self.main_window.drawing_canvas.winfo_width()
        height = self.main_window.drawing_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return 0, 0
        
        # Calculate canvas pixel dimensions
        canvas_pixel_width = self.main_window.canvas.width * self.main_window.canvas.zoom
        canvas_pixel_height = self.main_window.canvas.height * self.main_window.canvas.zoom
        
        # Calculate center offsets
        x_offset = (width - canvas_pixel_width) // 2
        y_offset = (height - canvas_pixel_height) // 2
        
        # Add pan offsets
        x_offset += self.main_window.pan_offset_x * self.main_window.canvas.zoom
        y_offset += self.main_window.pan_offset_y * self.main_window.canvas.zoom
        
        return x_offset, y_offset
    
    def _draw_edge_at_position(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Draw edge line at the current hover position"""
        if not self.hovered_pixel or not self.hovered_edge or not self.main_window:
            return
        
        pixel_x, pixel_y = self.hovered_pixel
        edge = self.hovered_edge
        
        # Draw the edge line
        self._draw_permanent_edge(pixel_x, pixel_y, edge, color)
    
    def _draw_permanent_edge(self, pixel_x: int, pixel_y: int, edge: str, color: Tuple[int, int, int, int]):
        """Draw a permanent edge line and store it"""
        if not self.main_window:
            return
        
        # Store the edge line data
        edge_data = {
            'pixel_x': pixel_x,
            'pixel_y': pixel_y,
            'edge': edge,
            'color': color
        }
        
        # Check if this edge line already exists
        if edge_data not in self.edge_lines:
            self.edge_lines.append(edge_data)
        
        # Draw the edge line immediately
        self._draw_edge_line_on_canvas(pixel_x, pixel_y, edge, color)
    
    def _draw_edge_line_on_canvas(self, pixel_x: int, pixel_y: int, edge: str, color: Tuple[int, int, int, int]):
        """Draw a single edge line on the canvas"""
        if not self.main_window:
            return
            
        drawing_canvas = self.main_window.drawing_canvas
        zoom = self.main_window.canvas.zoom
        
        # Calculate screen coordinates for the edge line
        x_offset, y_offset = self._get_canvas_offsets()
        
        # Convert color to hex string
        color_hex = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        
        # Draw edge line based on edge type
        if edge == "top":
            # Draw horizontal line above pixel
            screen_x1 = x_offset + (pixel_x * zoom)
            screen_x2 = x_offset + ((pixel_x + 1) * zoom)
            screen_y = y_offset + (pixel_y * zoom)
            
            drawing_canvas.create_line(
                screen_x1, screen_y,
                screen_x2, screen_y,
                fill=color_hex, width=2, tags="edge_lines"
            )
        
        elif edge == "bottom":
            # Draw horizontal line below pixel
            screen_x1 = x_offset + (pixel_x * zoom)
            screen_x2 = x_offset + ((pixel_x + 1) * zoom)
            screen_y = y_offset + ((pixel_y + 1) * zoom)
            
            drawing_canvas.create_line(
                screen_x1, screen_y,
                screen_x2, screen_y,
                fill=color_hex, width=2, tags="edge_lines"
            )
        
        elif edge == "left":
            # Draw vertical line to the left of pixel
            screen_x = x_offset + (pixel_x * zoom)
            screen_y1 = y_offset + (pixel_y * zoom)
            screen_y2 = y_offset + ((pixel_y + 1) * zoom)
            
            drawing_canvas.create_line(
                screen_x, screen_y1,
                screen_x, screen_y2,
                fill=color_hex, width=2, tags="edge_lines"
            )
        
        elif edge == "right":
            # Draw vertical line to the right of pixel
            screen_x = x_offset + ((pixel_x + 1) * zoom)
            screen_y1 = y_offset + (pixel_y * zoom)
            screen_y2 = y_offset + ((pixel_y + 1) * zoom)
            
            drawing_canvas.create_line(
                screen_x, screen_y1,
                screen_x, screen_y2,
                fill=color_hex, width=2, tags="edge_lines"
            )
    
    def redraw_all_edges(self):
        """Redraw all stored edge lines"""
        if not self.main_window:
            return
            
        # Clear existing edge lines
        self.main_window.drawing_canvas.delete("edge_lines")
        
        # Redraw all stored edge lines
        for edge_data in self.edge_lines:
            self._draw_edge_line_on_canvas(
                edge_data['pixel_x'],
                edge_data['pixel_y'],
                edge_data['edge'],
                edge_data['color']
            )
