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
        self.last_redraw_time = 0  # Prevent excessive redraws
        self.pending_redraw = False  # Flag to indicate redraw is needed
        
    def set_main_window(self, main_window):
        """Set reference to main window for canvas access"""
        self.main_window = main_window
        
    def on_mouse_down(self, canvas, x: float, y: float, button: int, color: Tuple[int, int, int, int]):
        """Start edge drawing or erasing"""
        if button == 1:  # Left mouse button - draw edge
            # Update hover state based on current position
            has_target = self._update_hover_state(canvas, x, y)
            if not has_target:
                return  # Nothing to draw here
            
            self.is_drawing = True
            # Clear any existing preview before starting to draw
            self._clear_preview()
            self._draw_edge_at_position(canvas, x, y, color)
        elif button == 3:  # Right mouse button - erase edge
            self._erase_edge_at_position(canvas, x, y)
    
    def on_mouse_up(self, canvas, x: float, y: float, button: int, color: Tuple[int, int, int, int]):
        """Stop edge drawing"""
        self.is_drawing = False
        
        # Clear any remaining preview after drawing is complete
        self._clear_preview()

        # Execute any pending redraw now that drawing is complete
        if self.pending_redraw:
            self.redraw_all_edges()
            self.pending_redraw = False
    
    def on_mouse_move(self, canvas, x: float, y: float, color: Tuple[int, int, int, int]):
        """Handle mouse movement for hover preview and drawing"""
        if self.is_drawing:
            # Update hover state without rendering preview while actively drawing
            if self._update_hover_state(canvas, x, y):
                self._draw_edge_at_position(canvas, x, y, color)
        else:
            # Update preview when not actively drawing
            self._update_hover_preview(canvas, x, y, color)
    
    def _update_hover_preview(self, canvas, x: float, y: float, color: Tuple[int, int, int, int]):
        """Update hover preview for edge detection"""
        if not self.main_window:
            return
            
        if self._update_hover_state(canvas, x, y):
            target_pixel_x, target_pixel_y = self.hovered_pixel
            edge = self.hovered_edge
            self._draw_preview(target_pixel_x, target_pixel_y, edge, color)
        else:
            self._clear_preview()
    
    def _find_nearest_edge(self, canvas, x: float, y: float, center_pixel_x: int, center_pixel_y: int) -> Optional[tuple[int, int, str]]:
        """Find the nearest edge across current pixel and adjacent pixels"""
        # Enhanced edge detection zone - more forgiving
        edge_zone = 0.4  # Increased from 0.25 to 0.4 (40% of pixel)
        
        best_edge = None
        best_distance = float('inf')
        best_pixel = None
        
        # Check current pixel and adjacent pixels in a 3x3 area
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                check_pixel_x = center_pixel_x + dx
                check_pixel_y = center_pixel_y + dy
                
                # Skip if pixel is outside canvas bounds
                if not (0 <= check_pixel_x < canvas.width and 0 <= check_pixel_y < canvas.height):
                    continue
                
                # Calculate mouse position relative to this pixel
                mouse_relative_x = x - check_pixel_x
                mouse_relative_y = y - check_pixel_y
                
                # Skip if mouse is too far from this pixel (outside 1.5 pixel radius)
                if abs(mouse_relative_x) > 1.5 or abs(mouse_relative_y) > 1.5:
                    continue
                
                # Check if mouse is within this pixel's bounds
                if 0 <= mouse_relative_x <= 1 and 0 <= mouse_relative_y <= 1:
                    # Mouse is inside this pixel - check edges
                    edge = self._detect_edge_hover(mouse_relative_x, mouse_relative_y, edge_zone)
                    if edge:
                        # Calculate distance to edge for prioritization
                        dist = self._calculate_edge_distance(mouse_relative_x, mouse_relative_y, edge)
                        if dist < best_distance:
                            best_distance = dist
                            best_edge = edge
                            best_pixel = (check_pixel_x, check_pixel_y)
                else:
                    # Mouse is outside this pixel - check if we're close to any edge
                    edge = self._detect_edge_from_outside_pixel(mouse_relative_x, mouse_relative_y, edge_zone)
                    if edge:
                        # Calculate distance to edge for prioritization
                        dist = self._calculate_edge_distance(mouse_relative_x, mouse_relative_y, edge)
                        if dist < best_distance:
                            best_distance = dist
                            best_edge = edge
                            best_pixel = (check_pixel_x, check_pixel_y)
        
        if best_edge and best_pixel:
            return (best_pixel[0], best_pixel[1], best_edge)
        return None
    
    def _detect_edge_hover(self, mouse_x: float, mouse_y: float, edge_zone: float = 0.25) -> Optional[str]:
        """Detect which edge of a pixel the mouse is hovering over"""
        # Calculate distances to each edge
        dist_top = mouse_y
        dist_bottom = 1.0 - mouse_y
        dist_left = mouse_x
        dist_right = 1.0 - mouse_x
        
        # Find the minimum distance
        min_dist = min(dist_top, dist_bottom, dist_left, dist_right)
        
        # Only trigger if within edge zone
        if min_dist > edge_zone:
            return None
        
        # Return the edge with minimum distance
        if min_dist == dist_top:
            return "top"
        elif min_dist == dist_bottom:
            return "bottom"
        elif min_dist == dist_left:
            return "left"
        elif min_dist == dist_right:
            return "right"
        
        return None
    
    def _detect_edge_from_outside_pixel(self, mouse_x: float, mouse_y: float, edge_zone: float) -> Optional[str]:
        """Detect edge when mouse is outside pixel bounds but close to an edge"""
        # Check if we're close to any edge of the pixel (0,0) to (1,1)
        
        # Check top edge (y=0)
        if mouse_y < edge_zone and 0 <= mouse_x <= 1:
            return "top"
        
        # Check bottom edge (y=1)
        elif mouse_y > (1 - edge_zone) and 0 <= mouse_x <= 1:
            return "bottom"
        
        # Check left edge (x=0)
        elif mouse_x < edge_zone and 0 <= mouse_y <= 1:
            return "left"
        
        # Check right edge (x=1)
        elif mouse_x > (1 - edge_zone) and 0 <= mouse_y <= 1:
            return "right"
        
        return None
    
    def _calculate_edge_distance(self, mouse_x: float, mouse_y: float, edge: str) -> float:
        """Calculate distance from mouse position to a specific edge"""
        if edge == "top":
            return abs(mouse_y)
        elif edge == "bottom":
            return abs(mouse_y - 1.0)
        elif edge == "left":
            return abs(mouse_x)
        elif edge == "right":
            return abs(mouse_x - 1.0)
        else:
            return float('inf')
    
    def _draw_preview(self, pixel_x: int, pixel_y: int, edge: str, color: Tuple[int, int, int, int], thickness: float = None):
        """Draw preview of edge line"""
        if not self.main_window:
            return
            
        # Clear any existing preview
        self._clear_preview()
        
        drawing_canvas = self.main_window.drawing_canvas
        zoom = self.main_window.canvas.zoom
        
        # Get thickness from tool size manager if not provided
        if thickness is None:
            thickness = getattr(self.main_window.tool_size_mgr, 'edge_thickness', 0.1)
        
        # Calculate screen coordinates for the edge line
        x_offset, y_offset = self._get_canvas_offsets()
        
        # Convert color to hex string
        color_hex = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        
        # Calculate line width based on thickness (minimum 1, scale with zoom)
        line_width = max(1, int(thickness * zoom))
        
        # Draw preview line based on edge type
        if edge == "top":
            # Draw horizontal line above pixel
            screen_x1 = x_offset + (pixel_x * zoom)
            screen_x2 = x_offset + ((pixel_x + 1) * zoom)
            screen_y = y_offset + (pixel_y * zoom)
            
            drawing_canvas.create_line(
                screen_x1, screen_y,
                screen_x2, screen_y,
                fill=color_hex, width=line_width, tags="edge_preview"
            )
        
        elif edge == "bottom":
            # Draw horizontal line below pixel
            screen_x1 = x_offset + (pixel_x * zoom)
            screen_x2 = x_offset + ((pixel_x + 1) * zoom)
            screen_y = y_offset + ((pixel_y + 1) * zoom)
            
            drawing_canvas.create_line(
                screen_x1, screen_y,
                screen_x2, screen_y,
                fill=color_hex, width=line_width, tags="edge_preview"
            )
        
        elif edge == "left":
            # Draw vertical line to the left of pixel
            screen_x = x_offset + (pixel_x * zoom)
            screen_y1 = y_offset + (pixel_y * zoom)
            screen_y2 = y_offset + ((pixel_y + 1) * zoom)
            
            drawing_canvas.create_line(
                screen_x, screen_y1,
                screen_x, screen_y2,
                fill=color_hex, width=line_width, tags="edge_preview"
            )
        
        elif edge == "right":
            # Draw vertical line to the right of pixel
            screen_x = x_offset + ((pixel_x + 1) * zoom)
            screen_y1 = y_offset + (pixel_y * zoom)
            screen_y2 = y_offset + ((pixel_y + 1) * zoom)
            
            drawing_canvas.create_line(
                screen_x, screen_y1,
                screen_x, screen_y2,
                fill=color_hex, width=line_width, tags="edge_preview"
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
    
    def _draw_edge_at_position(self, canvas, x: float, y: float, color: Tuple[int, int, int, int]):
        """Draw edge line at the current hover position"""
        if not self.hovered_pixel or not self.hovered_edge or not self.main_window:
            return
        
        pixel_x, pixel_y = self.hovered_pixel
        edge = self.hovered_edge
        
        # Draw the edge line
        self._draw_permanent_edge(pixel_x, pixel_y, edge, color)
    
    def _draw_permanent_edge(self, pixel_x: int, pixel_y: int, edge: str, color: Tuple[int, int, int, int], thickness: float = None):
        """Draw a permanent edge line and store it"""
        if not self.main_window:
            return
        
        # Get thickness from tool size manager if not provided
        if thickness is None:
            thickness = getattr(self.main_window.tool_size_mgr, 'edge_thickness', 0.1)
        
        # Store the edge line data
        edge_data = {
            'pixel_x': pixel_x,
            'pixel_y': pixel_y,
            'edge': edge,
            'color': color,
            'thickness': thickness
        }
        
        # Check if this edge line already exists (comparing without thickness for backward compatibility)
        edge_exists = False
        for existing_edge in self.edge_lines:
            if (existing_edge['pixel_x'] == edge_data['pixel_x'] and
                existing_edge['pixel_y'] == edge_data['pixel_y'] and
                existing_edge['edge'] == edge_data['edge'] and
                existing_edge['color'] == edge_data['color']):
                edge_exists = True
                break

        if not edge_exists:
            self.edge_lines.append(edge_data)
            # Schedule a redraw instead of immediately redrawing during active operations
            self.pending_redraw = True
    
    def _draw_edge_line_on_canvas(self, pixel_x: int, pixel_y: int, edge: str, color: Tuple[int, int, int, int], thickness: float = None):
        """Draw a single edge line on the canvas"""
        if not self.main_window:
            return
            
        drawing_canvas = self.main_window.drawing_canvas
        zoom = self.main_window.canvas.zoom
        
        # Get thickness from tool size manager if not provided
        if thickness is None:
            thickness = getattr(self.main_window.tool_size_mgr, 'edge_thickness', 0.1)
        
        # Calculate screen coordinates for the edge line
        x_offset, y_offset = self._get_canvas_offsets()
        
        # Convert color to hex string
        color_hex = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        
        # Calculate line width based on thickness (minimum 1, scale with zoom)
        line_width = max(1, int(thickness * zoom))
        
        # Draw edge line based on edge type
        if edge == "top":
            # Draw horizontal line above pixel
            screen_x1 = x_offset + (pixel_x * zoom)
            screen_x2 = x_offset + ((pixel_x + 1) * zoom)
            screen_y = y_offset + (pixel_y * zoom)
            
            drawing_canvas.create_line(
                screen_x1, screen_y,
                screen_x2, screen_y,
                fill=color_hex, width=line_width, tags="edge_lines"
            )
        
        elif edge == "bottom":
            # Draw horizontal line below pixel
            screen_x1 = x_offset + (pixel_x * zoom)
            screen_x2 = x_offset + ((pixel_x + 1) * zoom)
            screen_y = y_offset + ((pixel_y + 1) * zoom)
            
            drawing_canvas.create_line(
                screen_x1, screen_y,
                screen_x2, screen_y,
                fill=color_hex, width=line_width, tags="edge_lines"
            )
        
        elif edge == "left":
            # Draw vertical line to the left of pixel
            screen_x = x_offset + (pixel_x * zoom)
            screen_y1 = y_offset + (pixel_y * zoom)
            screen_y2 = y_offset + ((pixel_y + 1) * zoom)
            
            drawing_canvas.create_line(
                screen_x, screen_y1,
                screen_x, screen_y2,
                fill=color_hex, width=line_width, tags="edge_lines"
            )
        
        elif edge == "right":
            # Draw vertical line to the right of pixel
            screen_x = x_offset + ((pixel_x + 1) * zoom)
            screen_y1 = y_offset + (pixel_y * zoom)
            screen_y2 = y_offset + ((pixel_y + 1) * zoom)
            
            drawing_canvas.create_line(
                screen_x, screen_y1,
                screen_x, screen_y2,
                fill=color_hex, width=line_width, tags="edge_lines"
            )
    
    def redraw_all_edges(self, force: bool = False):
        """Redraw all stored edge lines"""
        if not self.main_window:
            return
        
        import time
        current_time = time.time()
        
        # Throttle redraws to prevent excessive calls (max 10 per second) unless forced
        if not force and current_time - self.last_redraw_time < 0.1:
            return
            
        self.last_redraw_time = current_time
            
        # Clear existing edge lines
        self.main_window.drawing_canvas.delete("edge_lines")
        
        # Ensure all edges have thickness field for backward compatibility
        for edge_data in self.edge_lines:
            if 'thickness' not in edge_data:
                edge_data['thickness'] = 0.1  # Default thickness
        
        # Redraw all stored edge lines
        for edge_data in self.edge_lines:
            self._draw_edge_line_on_canvas(
                edge_data['pixel_x'],
                edge_data['pixel_y'],
                edge_data['edge'],
                edge_data['color'],
                edge_data.get('thickness', 0.1)  # Use stored thickness or default
            )
    
    def clear_all_edges(self):
        """Clear all edge lines from canvas and storage"""
        if self.main_window:
            self.main_window.drawing_canvas.delete("edge_lines")
        self.edge_lines.clear()
        print("[Edge Tool] All edge lines cleared")
    
    def _erase_edge_at_position(self, canvas, x: float, y: float):
        """Erase edge line near the clicked position using enhanced detection"""
        if not self.main_window:
            return
        
        # Get the pixel coordinates
        pixel_x = int(x)
        pixel_y = int(y)
        
        # Check if we're within canvas bounds
        if not (0 <= pixel_x < canvas.width and 0 <= pixel_y < canvas.height):
            return
        
        # Use the same enhanced detection system as drawing
        edge_result = self._find_nearest_edge(canvas, x, y, pixel_x, pixel_y)
        
        if not edge_result:
            return
        
        target_pixel_x, target_pixel_y, target_edge = edge_result
        
        # Find edges to remove - look for edges that match the detected edge
        edges_to_remove = []
        
        for edge_data in self.edge_lines:
            edge_pixel_x = edge_data['pixel_x']
            edge_pixel_y = edge_data['pixel_y']
            edge_type = edge_data['edge']
            
            # Check if this edge matches the detected edge
            if (edge_pixel_x == target_pixel_x and 
                edge_pixel_y == target_pixel_y and 
                edge_type == target_edge):
                edges_to_remove.append(edge_data)
        
        # Remove the found edges
        for edge_data in edges_to_remove:
            self.edge_lines.remove(edge_data)
        
        if edges_to_remove:
            # Schedule a redraw instead of immediately redrawing during active operations
            self.pending_redraw = True

            print(f"[Edge Tool] Erased {len(edges_to_remove)} edge line(s) at {target_edge} edge of pixel ({target_pixel_x}, {target_pixel_y})")
    
    def _is_edge_near_pixel(self, edge_pixel_x: int, edge_pixel_y: int, edge_type: str, target_x: int, target_y: int) -> bool:
        """Check if an edge is near the target pixel"""
        # Check if edge pixel is the same as target pixel
        if edge_pixel_x == target_x and edge_pixel_y == target_y:
            return True
        
        # Check adjacent pixels based on edge type
        if edge_type == "top":
            # Top edge affects the pixel above
            return (edge_pixel_x == target_x and edge_pixel_y == target_y - 1)
        elif edge_type == "bottom":
            # Bottom edge affects the pixel below
            return (edge_pixel_x == target_x and edge_pixel_y == target_y + 1)
        elif edge_type == "left":
            # Left edge affects the pixel to the left
            return (edge_pixel_x == target_x - 1 and edge_pixel_y == target_y)
        elif edge_type == "right":
            # Right edge affects the pixel to the right
            return (edge_pixel_x == target_x + 1 and edge_pixel_y == target_y)
        
        return False

    def _update_hover_state(self, canvas, x: float, y: float) -> bool:
        """Update the current hovered pixel/edge based on position"""
        if not self.main_window:
            return False
        
        pixel_x = int(x)
        pixel_y = int(y)
        
        # Enhanced edge detection - check current pixel and adjacent pixels
        edge_result = self._find_nearest_edge(canvas, x, y, pixel_x, pixel_y)
        
        if edge_result:
            target_pixel_x, target_pixel_y, edge = edge_result
            self.hovered_pixel = (target_pixel_x, target_pixel_y)
            self.hovered_edge = edge
            return True
        
        self.hovered_pixel = None
        self.hovered_edge = None
        return False
