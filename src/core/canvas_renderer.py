'''
canvas_renderer.py

Manages all rendering operations on the main canvas.
This includes drawing the pixel grid, rendering the image data,
displaying selection overlays, and other visual elements.
'''

import numpy as np

class CanvasRenderer:
    def __init__(self, app_instance):
        """
        Initializes the CanvasRenderer.

        Args:
            app_instance: The main application instance, providing access
                          to the canvas, project data, and other components.
        """
        self.app = app_instance
        self.canvas = app_instance.canvas

    def init_drawing_surface(self):
        """Initialize the tkinter drawing surface"""
        # Schedule initial draw after window is fully loaded
        self.app.root.after(100, self.initial_draw)
    
    def get_background_color(self):
        """Get background color based on background mode"""
        if self.app.canvas.background_mode == "auto":
            return self.app.theme_manager.get_current_theme().canvas_bg
        elif self.app.canvas.background_mode == "dark":
            # Force dark background (visible on light themes)
            return "#0d1117"  # Very dark background
        elif self.app.canvas.background_mode == "light":
            # Force light background (visible on dark themes)
            return "#fafafa"  # Light background
        else:  # texture mode
            # Return base texture color for background texture mode
            return self.app.canvas.background_texture_base_color

    def initial_draw(self):
        """Do the initial drawing of the canvas"""
        try:
            # Get canvas size
            self.app.drawing_canvas.update_idletasks()
            width = self.app.drawing_canvas.winfo_width()
            height = self.app.drawing_canvas.winfo_height()

            if width > 1 and height > 1:
                # Set canvas size to match our pixel grid
                canvas_pixel_width = self.app.canvas.width * self.app.canvas.zoom
                canvas_pixel_height = self.app.canvas.height * self.app.canvas.zoom

                # Center the canvas in the available space
                x_offset = (width - canvas_pixel_width) // 2
                y_offset = (height - canvas_pixel_height) // 2

                # Clear canvas
                self.app.drawing_canvas.delete("all")

                # Draw grid if enabled
                if self.app.canvas.show_grid:
                    self.draw_tkinter_grid(x_offset, y_offset, canvas_pixel_width, canvas_pixel_height)
                
                # Draw symmetry axes
                self.draw_symmetry_axes(x_offset, y_offset, canvas_pixel_width, canvas_pixel_height)

                # Draw a border around the canvas area with theme color
                theme = self.app.theme_manager.get_current_theme()
                self.app.drawing_canvas.create_rectangle(
                    x_offset, y_offset,
                    x_offset + canvas_pixel_width, y_offset + canvas_pixel_height,
                    outline=theme.canvas_border, width=2, tags="border"
                )

                # Draw any existing pixels
                self.draw_all_pixels_on_tkinter(x_offset, y_offset)
                
            else:
                # Try again in a moment
                self.app.root.after(200, self.initial_draw)
        except Exception as e:
            print(f"Error in initial draw: {e}")
            import traceback
            traceback.print_exc()

    def draw_symmetry_axes(self, x_offset, y_offset, canvas_pixel_width, canvas_pixel_height):
        """Draw symmetry axes if enabled"""
        zoom = self.app.canvas.zoom
        width = self.app.canvas.width
        height = self.app.canvas.height
        
        # Horizontal Symmetry Axis (Vertical line at center X)
        if hasattr(self.app.canvas, 'symmetry_x') and self.app.canvas.symmetry_x:
            center_x = width / 2
            screen_x = x_offset + (center_x * zoom)
            self.app.drawing_canvas.create_line(
                screen_x, y_offset,
                screen_x, y_offset + canvas_pixel_height,
                fill="#00FFFF", width=2, dash=(4, 4), tags="symmetry_axis"
            )

        # Vertical Symmetry Axis (Horizontal line at center Y)
        if hasattr(self.app.canvas, 'symmetry_y') and self.app.canvas.symmetry_y:
            center_y = height / 2
            screen_y = y_offset + (center_y * zoom)
            self.app.drawing_canvas.create_line(
                x_offset, screen_y,
                x_offset + canvas_pixel_width, screen_y,
                fill="#00FFFF", width=2, dash=(4, 4), tags="symmetry_axis"
            )

    def draw_tkinter_grid(self, x_offset, y_offset, canvas_width, canvas_height):
        """Draw grid lines on tkinter canvas with mode support"""
        theme = self.app.theme_manager.get_current_theme()
        
        # Handle paper texture mode
        if self.app.canvas.grid_mode == "paper":
            self.draw_paper_texture_grid(x_offset, y_offset, canvas_width, canvas_height)
            return
        
        # Determine grid color based on mode
        if self.app.canvas.grid_mode == "auto":
            grid_color = theme.grid_color  # Use theme default
        elif self.app.canvas.grid_mode == "dark":
            # Force dark grid (visible on light backgrounds)
            grid_color = "#404040"  # Dark grey
        else:  # light mode
            # Force light grid (visible on dark backgrounds)
            grid_color = "#e0e0e0"  # Light grey

        for x in range(0, self.app.canvas.width + 1):
            screen_x = x_offset + (x * self.app.canvas.zoom)
            self.app.drawing_canvas.create_line(
                screen_x, y_offset,
                screen_x, y_offset + canvas_height,
                fill=grid_color, width=1, tags="grid"
            )

        for y in range(0, self.app.canvas.height + 1):
            screen_y = y_offset + (y * self.app.canvas.zoom)
            self.app.drawing_canvas.create_line(
                x_offset, screen_y,
                x_offset + canvas_width, screen_y,
                fill=grid_color, width=1, tags="grid"
            )

    def draw_paper_texture_grid(self, x_offset, y_offset, canvas_width, canvas_height):
        """Draw organic paper texture as grid background"""
        import random
        import math
        
        zoom = self.app.canvas.zoom
        base_color = self.app.canvas.paper_base_color
        grain_color = self.app.canvas.paper_grain_color
        intensity = self.app.canvas.paper_texture_intensity
        
        # Create paper texture background
        self.app.drawing_canvas.create_rectangle(
            x_offset, y_offset,
            x_offset + canvas_width, y_offset + canvas_height,
            fill=base_color, outline="", tags="grid"
        )
        
        # Add organic grain patterns
        random.seed(42)  # Consistent seed for stable texture
        
        # Draw subtle grain lines (organic, not straight)
        for i in range(int(canvas_width * canvas_height / (zoom * zoom * 4))):
            # Random position
            x1 = x_offset + random.randint(0, canvas_width)
            y1 = y_offset + random.randint(0, canvas_height)
            
            # Random length and direction
            length = random.randint(2, 8)
            angle = random.uniform(0, 2 * math.pi)
            x2 = x1 + int(length * math.cos(angle))
            y2 = y1 + int(length * math.sin(angle))
            
            # Keep within bounds
            x2 = max(x_offset, min(x_offset + canvas_width, x2))
            y2 = max(y_offset, min(y_offset + canvas_height, y2))
            
            # Draw grain line with varying opacity
            opacity = random.uniform(0.1, intensity)
            if opacity > 0.15:  # Only draw visible grain
                self.app.drawing_canvas.create_line(
                    x1, y1, x2, y2,
                    fill=grain_color, width=1, tags="grid"
                )
        
        # Add subtle paper fiber patterns
        for i in range(int(canvas_width * canvas_height / (zoom * zoom * 8))):
            x = x_offset + random.randint(0, canvas_width)
            y = y_offset + random.randint(0, canvas_height)
            
            # Small fiber dots
            if random.random() < intensity * 0.3:
                self.app.drawing_canvas.create_oval(
                    x-1, y-1, x+1, y+1,
                    fill=grain_color, outline="", tags="grid"
                )
        
        # Draw subtle grid lines (very light)
        grid_alpha = intensity * 0.2
        if grid_alpha > 0.05:
            for x in range(0, self.app.canvas.width + 1):
                screen_x = x_offset + (x * zoom)
                self.app.drawing_canvas.create_line(
                    screen_x, y_offset,
                    screen_x, y_offset + canvas_height,
                    fill=grain_color, width=1, tags="grid"
                )

            for y in range(0, self.app.canvas.height + 1):
                screen_y = y_offset + (y * zoom)
                self.app.drawing_canvas.create_line(
                    x_offset, screen_y,
                    x_offset + canvas_width, screen_y,
                    fill=grain_color, width=1, tags="grid"
                )

    def draw_background_texture(self, x_offset, y_offset, canvas_width, canvas_height):
        """Draw organic background texture"""
        import random
        import math
        
        zoom = self.app.canvas.zoom
        base_color = self.app.canvas.background_texture_base_color
        grain_color = self.app.canvas.background_texture_grain_color
        intensity = self.app.canvas.background_texture_intensity
        
        # Create background texture
        self.app.drawing_canvas.create_rectangle(
            x_offset, y_offset,
            x_offset + canvas_width, y_offset + canvas_height,
            fill=base_color, outline="", tags="background"
        )
        
        # Add organic texture patterns
        random.seed(123)  # Different seed from paper texture for variety
        
        # Draw subtle texture lines (more subtle than paper)
        for i in range(int(canvas_width * canvas_height / (zoom * zoom * 6))):
            # Random position
            x1 = x_offset + random.randint(0, canvas_width)
            y1 = y_offset + random.randint(0, canvas_height)
            
            # Random length and direction
            length = random.randint(1, 6)
            angle = random.uniform(0, 2 * math.pi)
            x2 = x1 + int(length * math.cos(angle))
            y2 = y1 + int(length * math.sin(angle))
            
            # Keep within bounds
            x2 = max(x_offset, min(x_offset + canvas_width, x2))
            y2 = max(y_offset, min(y_offset + canvas_height, y2))
            
            # Draw texture line with varying opacity
            opacity = random.uniform(0.05, intensity * 0.5)
            if opacity > 0.08:  # Only draw visible texture
                self.app.drawing_canvas.create_line(
                    x1, y1, x2, y2,
                    fill=grain_color, width=1, tags="background"
                )
        
        # Add subtle texture dots
        for i in range(int(canvas_width * canvas_height / (zoom * zoom * 12))):
            x = x_offset + random.randint(0, canvas_width)
            y = y_offset + random.randint(0, canvas_height)
            
            # Small texture dots
            if random.random() < intensity * 0.2:
                self.app.drawing_canvas.create_oval(
                    x-1, y-1, x+1, y+1,
                    fill=grain_color, outline="", tags="background"
                )

    def update_pixel_display(self):
        """Update tkinter display to show all pixel changes (full redraw)"""
        if self.app._updating_display:
            return
        self.app._updating_display = True
        
        try:
            # Force canvas to update its dimensions before calculating centering
            self.app.drawing_canvas.update_idletasks()
            width = self.app.drawing_canvas.winfo_width()
            height = self.app.drawing_canvas.winfo_height()
            
            # Double-check: if dimensions seem wrong, try again after a brief delay
            if width <= 1 or height <= 1:
                self.app.root.after(50, self.update_pixel_display)
                return

            if width > 1 and height > 1:
                canvas_pixel_width = self.app.canvas.width * self.app.canvas.zoom
                canvas_pixel_height = self.app.canvas.height * self.app.canvas.zoom

                x_offset = (width - canvas_pixel_width) // 2
                y_offset = (height - canvas_pixel_height) // 2
                
                x_offset += self.app.pan_offset_x * self.app.canvas.zoom
                y_offset += self.app.pan_offset_y * self.app.canvas.zoom

                self.app.drawing_canvas.delete("all")

                # Draw background texture FIRST if in texture mode (so grid appears on top)
                if self.app.canvas.background_mode == "texture":
                    self.draw_background_texture(x_offset, y_offset, canvas_pixel_width, canvas_pixel_height)

                if self.app.canvas.show_grid:
                    self.draw_tkinter_grid(x_offset, y_offset, canvas_pixel_width, canvas_pixel_height)

                # Draw symmetry axes
                self.draw_symmetry_axes(x_offset, y_offset, canvas_pixel_width, canvas_pixel_height)

                theme = self.app.theme_manager.get_current_theme()
                self.app.drawing_canvas.create_rectangle(
                    x_offset, y_offset,
                    x_offset + canvas_pixel_width, y_offset + canvas_pixel_height,
                    outline=theme.canvas_border, width=2, tags="border"
                )

                # Draw tile preview FIRST (behind everything, shows repeating pattern)
                if self.app.canvas.show_tile_preview:
                    self.draw_tile_preview(x_offset, y_offset, canvas_pixel_width, canvas_pixel_height)
                
                # Draw onion skin frames first (behind current frame)
                if hasattr(self.app, 'timeline') and self.app.timeline.onion_skin_enabled:
                    self.draw_onion_skin(x_offset, y_offset, canvas_pixel_width, canvas_pixel_height)
                
                self.draw_all_pixels_on_tkinter(x_offset, y_offset)
                
                # Draw tile seam preview if enabled
                if self.app.canvas.show_tile_seam_preview:
                    self.draw_tile_seam_preview(x_offset, y_offset, canvas_pixel_width, canvas_pixel_height)

                # Live move preview: draw selected pixels at current drag position (non-destructive)
                move_tool = self.app.tools.get("move")
                sel_tool = self.app.tools.get("selection")
                if (move_tool and sel_tool and getattr(move_tool, "is_moving", False)
                    and sel_tool.selected_pixels is not None and sel_tool.selection_rect):
                    zoom = self.app.canvas.zoom
                    left, top, width, height = sel_tool.selection_rect
                    # Draw preview pixels using a lightweight overlay tag
                    preview_tag = "move_preview"
                    # No need to delete specifically because we wiped the canvas with delete("all") above
                    for py in range(min(height, sel_tool.selected_pixels.shape[0])):
                        for px in range(min(width, sel_tool.selected_pixels.shape[1])):
                            rgba = tuple(sel_tool.selected_pixels[py, px])
                            if rgba and rgba[3] > 0:
                                screen_x = x_offset + ((left + px) * zoom)
                                screen_y = y_offset + ((top + py) * zoom)
                                hex_color = f"#{rgba[0]:02x}{rgba[1]:02x}{rgba[2]:02x}"
                                self.app.drawing_canvas.create_rectangle(
                                    screen_x, screen_y,
                                    screen_x + zoom, screen_y + zoom,
                                    fill=hex_color, outline="", tags=preview_tag
                                )

                # Edge lines: during a move, preview the selected edges at the drag position
                move_tool = self.app.tools.get("move")
                sel_tool = self.app.tools.get("selection")
                
                # ALWAYS redraw all edge lines first (so non-selected edges remain visible)
                self._redraw_edge_lines_using_tool()
                
                # During a move, also draw the selected edge lines at their new position
                if (move_tool and getattr(move_tool, "is_moving", False)
                    and sel_tool and getattr(sel_tool, "selected_edge_lines", None)):
                    zoom = self.app.canvas.zoom
                    # Compute offset relative to the ORIGINAL selection
                    if move_tool.original_selection and sel_tool.selection_rect:
                        orig_left, orig_top, _, _ = move_tool.original_selection
                        left, top, _, _ = sel_tool.selection_rect
                        off_x = left - orig_left
                        off_y = top - orig_top
                    else:
                        off_x = 0
                        off_y = 0
                    # Draw each edge line as a preview at the moved position
                    for edge_data in sel_tool.selected_edge_lines:
                        px = edge_data.get('pixel_x', 0) + off_x
                        py = edge_data.get('pixel_y', 0) + off_y
                        edge = edge_data.get('edge', 'top')
                        color = edge_data.get('color', (255, 0, 0, 255))
                        thickness = edge_data.get('thickness', 0.1)
                        color_hex = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                        line_width = max(1, int(thickness * zoom))
                        # Compute screen coords for each edge type
                        if edge == 'top':
                            sx1 = x_offset + (px * zoom)
                            sx2 = x_offset + ((px + 1) * zoom)
                            sy = y_offset + (py * zoom)
                            self.app.drawing_canvas.create_line(sx1, sy, sx2, sy, fill=color_hex, width=line_width, tags="edge_preview")
                        elif edge == 'bottom':
                            sx1 = x_offset + (px * zoom)
                            sx2 = x_offset + ((px + 1) * zoom)
                            sy = y_offset + ((py + 1) * zoom)
                            self.app.drawing_canvas.create_line(sx1, sy, sx2, sy, fill=color_hex, width=line_width, tags="edge_preview")
                        elif edge == 'left':
                            sx = x_offset + (px * zoom)
                            sy1 = y_offset + (py * zoom)
                            sy2 = y_offset + ((py + 1) * zoom)
                            self.app.drawing_canvas.create_line(sx, sy1, sx, sy2, fill=color_hex, width=line_width, tags="edge_preview")
                        elif edge == 'right':
                            sx = x_offset + ((px + 1) * zoom)
                            sy1 = y_offset + (py * zoom)
                            sy2 = y_offset + ((py + 1) * zoom)
                            self.app.drawing_canvas.create_line(sx, sy1, sx, sy2, fill=color_hex, width=line_width, tags="edge_preview")
                
                self.draw_selection_on_tkinter(x_offset, y_offset)
                
                if self.app.grid_control_mgr.grid_overlay and self.app.canvas.show_grid:
                    self.app.drawing_canvas.tag_raise("grid")
        finally:
            self.app._updating_display = False

    def draw_selection_on_tkinter(self, x_offset: int, y_offset: int):
        """Draw selection rectangle on tkinter canvas"""
        selection_tool = self.app.tools.get("selection")
        if not selection_tool:
            return
        
        if selection_tool.selection_rect and (selection_tool.is_selecting or selection_tool.has_selection):
            left, top, width, height = selection_tool.selection_rect
            zoom = self.app.canvas.zoom
            
            screen_x1 = x_offset + (left * zoom)
            screen_y1 = y_offset + (top * zoom)
            screen_x2 = x_offset + ((left + width) * zoom)
            screen_y2 = y_offset + ((top + height) * zoom)
            
            self.app.drawing_canvas.create_rectangle(
                screen_x1, screen_y1, screen_x2, screen_y2,
                outline="white", width=2, tags="selection"
            )
            
            corner_size = 6
            self.app.drawing_canvas.create_line(screen_x1, screen_y1, screen_x1 + corner_size, screen_y1, fill="white", width=3, tags="selection")
            self.app.drawing_canvas.create_line(screen_x1, screen_y1, screen_x1, screen_y1 + corner_size, fill="white", width=3, tags="selection")
            self.app.drawing_canvas.create_line(screen_x2, screen_y1, screen_x2 - corner_size, screen_y1, fill="white", width=3, tags="selection")
            self.app.drawing_canvas.create_line(screen_x2, screen_y1, screen_x2, screen_y1 + corner_size, fill="white", width=3, tags="selection")
            self.app.drawing_canvas.create_line(screen_x1, screen_y2, screen_x1 + corner_size, screen_y2, fill="white", width=3, tags="selection")
            self.app.drawing_canvas.create_line(screen_x1, screen_y2, screen_x1, screen_y2 - corner_size, fill="white", width=3, tags="selection")
            self.app.drawing_canvas.create_line(screen_x2, screen_y2, screen_x2 - corner_size, screen_y2, fill="white", width=3, tags="selection")
            self.app.drawing_canvas.create_line(screen_x2, screen_y2, screen_x2, screen_y2 - corner_size, fill="white", width=3, tags="selection")
            
            # Draw selection handles (always visible when there's a selection)
            handle_size = 8
            self.draw_scale_handle(screen_x1, screen_y1, handle_size, "yellow")
            self.draw_scale_handle(screen_x2, screen_y1, handle_size, "yellow")
            self.draw_scale_handle(screen_x1, screen_y2, handle_size, "yellow")
            self.draw_scale_handle(screen_x2, screen_y2, handle_size, "yellow")
            
            mid_x = (screen_x1 + screen_x2) / 2
            mid_y = (screen_y1 + screen_y2) / 2
            self.draw_scale_handle(mid_x, screen_y1, handle_size, "orange")
            self.draw_scale_handle(mid_x, screen_y2, handle_size, "orange")
            self.draw_scale_handle(screen_x1, mid_y, handle_size, "orange")
            self.draw_scale_handle(screen_x2, mid_y, handle_size, "orange")
        
        move_tool = self.app.tools.get("move")
        if (move_tool and move_tool.is_moving and selection_tool and 
            selection_tool.selected_pixels is not None and selection_tool.selection_rect):
            left, top, width, height = selection_tool.selection_rect
            zoom = self.app.canvas.zoom
            
            for py in range(height):
                for px in range(width):
                    if (py < selection_tool.selected_pixels.shape[0] and 
                        px < selection_tool.selected_pixels.shape[1]):
                        pixel_color = tuple(selection_tool.selected_pixels[py, px])
                        if pixel_color[3] > 0:
                            screen_x = x_offset + ((left + px) * zoom)
                            screen_y = y_offset + ((top + py) * zoom)
                            
                            hex_color = f"#{pixel_color[0]:02x}{pixel_color[1]:02x}{pixel_color[2]:02x}"
                            
                            self.app.drawing_canvas.create_rectangle(
                                screen_x, screen_y,
                                screen_x + zoom, screen_y + zoom,
                                fill=hex_color, outline="", tags="move_preview"
                            )
        
        # Draw rotation preview pixels
        if (hasattr(self.app, 'selection_mgr') and self.app.selection_mgr.is_rotating and selection_tool and 
            self.app.selection_mgr.rotated_pixels_preview is not None and selection_tool.selection_rect):
            left, top, width, height = selection_tool.selection_rect
            zoom = self.app.canvas.zoom
            rotated_pixels = self.app.selection_mgr.rotated_pixels_preview
            
            for py in range(height):
                for px in range(width):
                    if (py < rotated_pixels.shape[0] and 
                        px < rotated_pixels.shape[1]):
                        pixel_color = tuple(rotated_pixels[py, px])
                        if pixel_color[3] > 0:
                            screen_x = x_offset + ((left + px) * zoom)
                            screen_y = y_offset + ((top + py) * zoom)
                            
                            hex_color = f"#{pixel_color[0]:02x}{pixel_color[1]:02x}{pixel_color[2]:02x}"
                            
                            self.app.drawing_canvas.create_rectangle(
                                screen_x, screen_y,
                                screen_x + zoom, screen_y + zoom,
                                fill=hex_color, outline="", tags="rotate_preview"
                            )
        
        if (hasattr(self.app, 'selection_mgr') and self.app.selection_mgr.is_placing_copy and 
            self.app.selection_mgr.copy_preview_pos and self.app.selection_mgr.copy_buffer is not None and 
            self.app.selection_mgr.copy_dimensions):
            preview_x, preview_y = self.app.selection_mgr.copy_preview_pos
            width, height = self.app.selection_mgr.copy_dimensions
            zoom = self.app.canvas.zoom
            
            for py in range(height):
                for px in range(width):
                    if py < self.app.selection_mgr.copy_buffer.shape[0] and px < self.app.selection_mgr.copy_buffer.shape[1]:
                        pixel_color = tuple(self.app.selection_mgr.copy_buffer[py, px])
                        if pixel_color[3] > 0:
                            canvas_x = preview_x + px
                            canvas_y = preview_y + py
                            if 0 <= canvas_x < self.app.canvas.width and 0 <= canvas_y < self.app.canvas.height:
                                screen_x = x_offset + (canvas_x * zoom)
                                screen_y = y_offset + (canvas_y * zoom)
                                
                                color_hex = f'#{pixel_color[0]:02x}{pixel_color[1]:02x}{pixel_color[2]:02x}'
                                self.app.drawing_canvas.create_rectangle(
                                    screen_x, screen_y,
                                    screen_x + zoom, screen_y + zoom,
                                    fill=color_hex,
                                    outline="",
                                    stipple="gray50",
                                    tags="copy_preview"
                                )
            
            preview_screen_x1 = x_offset + (preview_x * zoom)
            preview_screen_y1 = y_offset + (preview_y * zoom)
            preview_screen_x2 = x_offset + ((preview_x + width) * zoom)
            preview_screen_y2 = y_offset + ((preview_y + height) * zoom)
            self.app.drawing_canvas.create_rectangle(
                preview_screen_x1, preview_screen_y1,
                preview_screen_x2, preview_screen_y2,
                outline="cyan",
                width=2,
                dash=(4, 4),
                tags="copy_preview"
            )

    def draw_brush_preview(self, canvas_x: int, canvas_y: int):
        """Draw live preview of brush tool on tkinter canvas"""
        self.app.drawing_canvas.delete("brush_preview")
        canvas_width = self.app.drawing_canvas.winfo_width()
        canvas_height = self.app.drawing_canvas.winfo_height()
        canvas_pixel_width = self.app.canvas.width * self.app.canvas.zoom
        canvas_pixel_height = self.app.canvas.height * self.app.canvas.zoom
        x_offset = (canvas_width - canvas_pixel_width) // 2 + self.app.pan_offset_x * self.app.canvas.zoom
        y_offset = (canvas_height - canvas_pixel_height) // 2 + self.app.pan_offset_y * self.app.canvas.zoom
        offset = self.app.tool_size_mgr.brush_size // 2
        
        # Check if any part of the brush would be in bounds
        min_x = canvas_x - offset
        max_x = canvas_x - offset + self.app.tool_size_mgr.brush_size
        min_y = canvas_y - offset
        max_y = canvas_y - offset + self.app.tool_size_mgr.brush_size
        
        # Only draw preview if brush area intersects with canvas bounds
        if max_x > 0 and min_x < self.app.canvas.width and max_y > 0 and min_y < self.app.canvas.height:
            for dy in range(self.app.tool_size_mgr.brush_size):
                for dx in range(self.app.tool_size_mgr.brush_size):
                    px = canvas_x - offset + dx
                    py = canvas_y - offset + dy
                    if 0 <= px < self.app.canvas.width and 0 <= py < self.app.canvas.height:
                        screen_x = x_offset + (px * self.app.canvas.zoom)
                        screen_y = y_offset + (py * self.app.canvas.zoom)
                        r, g, b, a = self.app.get_current_color()
                        color_hex = f"#{r:02x}{g:02x}{b:02x}"
                        self.app.drawing_canvas.create_rectangle(
                            screen_x, screen_y,
                            screen_x + self.app.canvas.zoom, screen_y + self.app.canvas.zoom,
                            fill=color_hex, outline=color_hex, stipple="gray50",
                            tags="brush_preview"
                        )
            screen_x1 = x_offset + ((canvas_x - offset) * self.app.canvas.zoom)
            screen_y1 = y_offset + ((canvas_y - offset) * self.app.canvas.zoom)
            screen_x2 = x_offset + ((canvas_x - offset + self.app.tool_size_mgr.brush_size) * self.app.canvas.zoom)
            screen_y2 = y_offset + ((canvas_y - offset + self.app.tool_size_mgr.brush_size) * self.app.canvas.zoom)
            self.app.drawing_canvas.create_rectangle(
                screen_x1, screen_y1, screen_x2, screen_y2,
                outline="#ffffff", width=2, dash=(4, 4),
                tags="brush_preview"
            )

    def draw_eraser_preview(self, canvas_x: int, canvas_y: int):
        """Draw live preview of eraser tool on tkinter canvas"""
        self.app.drawing_canvas.delete("eraser_preview")
        canvas_width = self.app.drawing_canvas.winfo_width()
        canvas_height = self.app.drawing_canvas.winfo_height()
        canvas_pixel_width = self.app.canvas.width * self.app.canvas.zoom
        canvas_pixel_height = self.app.canvas.height * self.app.canvas.zoom
        x_offset = (canvas_width - canvas_pixel_width) // 2 + self.app.pan_offset_x * self.app.canvas.zoom
        y_offset = (canvas_height - canvas_pixel_height) // 2 + self.app.pan_offset_y * self.app.canvas.zoom
        offset = self.app.tool_size_mgr.eraser_size // 2
        
        # Check if any part of the eraser would be in bounds
        min_x = canvas_x - offset
        max_x = canvas_x - offset + self.app.tool_size_mgr.eraser_size
        min_y = canvas_y - offset
        max_y = canvas_y - offset + self.app.tool_size_mgr.eraser_size
        
        # Only draw preview if eraser area intersects with canvas bounds
        if max_x > 0 and min_x < self.app.canvas.width and max_y > 0 and min_y < self.app.canvas.height:
            for dy in range(self.app.tool_size_mgr.eraser_size):
                for dx in range(self.app.tool_size_mgr.eraser_size):
                    px = canvas_x - offset + dx
                    py = canvas_y - offset + dy
                    if 0 <= px < self.app.canvas.width and 0 <= py < self.app.canvas.height:
                        screen_x = x_offset + (px * self.app.canvas.zoom)
                        screen_y = y_offset + (py * self.app.canvas.zoom)
                        self.app.drawing_canvas.create_rectangle(
                            screen_x, screen_y,
                            screen_x + self.app.canvas.zoom, screen_y + self.app.canvas.zoom,
                            fill="#ff0000", outline="#ff0000", stipple="gray50",
                            tags="eraser_preview"
                        )
            screen_x1 = x_offset + ((canvas_x - offset) * self.app.canvas.zoom)
            screen_y1 = y_offset + ((canvas_y - offset) * self.app.canvas.zoom)
            screen_x2 = x_offset + ((canvas_x - offset + self.app.tool_size_mgr.eraser_size) * self.app.canvas.zoom)
            screen_y2 = y_offset + ((canvas_y - offset + self.app.tool_size_mgr.eraser_size) * self.app.canvas.zoom)
            self.app.drawing_canvas.create_rectangle(
                screen_x1, screen_y1, screen_x2, screen_y2,
                outline="#ff0000", width=2, dash=(4, 4),
                tags="eraser_preview"
            )

    def draw_dither_preview(self, canvas_x: int, canvas_y: int):
        """Draw checkerboard preview for Dither tool at the cursor position.
        Shows which pixels will be drawn in the checkerboard pattern."""
        self.app.drawing_canvas.delete("dither_preview")
        canvas_width = self.app.drawing_canvas.winfo_width()
        canvas_height = self.app.drawing_canvas.winfo_height()
        canvas_pixel_width = self.app.canvas.width * self.app.canvas.zoom
        canvas_pixel_height = self.app.canvas.height * self.app.canvas.zoom
        x_offset = (canvas_width - canvas_pixel_width) // 2 + self.app.pan_offset_x * self.app.canvas.zoom
        y_offset = (canvas_height - canvas_pixel_height) // 2 + self.app.pan_offset_y * self.app.canvas.zoom
        
        # Dither uses brush size for preview area
        brush_size = self.app.tool_size_mgr.brush_size
        offset = brush_size // 2
        
        # Check if any part of the dither area would be in bounds
        min_x = canvas_x - offset
        max_x = canvas_x - offset + brush_size
        min_y = canvas_y - offset
        max_y = canvas_y - offset + brush_size
        
        # Only draw preview if area intersects with canvas bounds
        if max_x > 0 and min_x < self.app.canvas.width and max_y > 0 and min_y < self.app.canvas.height:
            r, g, b, a = self.app.get_current_color()
            color_hex = f"#{r:02x}{g:02x}{b:02x}"
            
            for dy in range(brush_size):
                for dx in range(brush_size):
                    px = canvas_x - offset + dx
                    py = canvas_y - offset + dy
                    if 0 <= px < self.app.canvas.width and 0 <= py < self.app.canvas.height:
                        # Checkerboard pattern: only draw where (x + y) % 2 == 0
                        if (px + py) % 2 == 0:
                            screen_x = x_offset + (px * self.app.canvas.zoom)
                            screen_y = y_offset + (py * self.app.canvas.zoom)
                            self.app.drawing_canvas.create_rectangle(
                                screen_x, screen_y,
                                screen_x + self.app.canvas.zoom, screen_y + self.app.canvas.zoom,
                                fill=color_hex, outline=color_hex, stipple="gray50",
                                tags="dither_preview"
                            )
            
            # Draw bounding box outline
            screen_x1 = x_offset + ((canvas_x - offset) * self.app.canvas.zoom)
            screen_y1 = y_offset + ((canvas_y - offset) * self.app.canvas.zoom)
            screen_x2 = x_offset + ((canvas_x - offset + brush_size) * self.app.canvas.zoom)
            screen_y2 = y_offset + ((canvas_y - offset + brush_size) * self.app.canvas.zoom)
            self.app.drawing_canvas.create_rectangle(
                screen_x1, screen_y1, screen_x2, screen_y2,
                outline="#ffffff", width=2, dash=(4, 4),
                tags="dither_preview"
            )

    def draw_spray_preview(self, canvas_x: int, canvas_y: int):
        """Draw circular preview for Spray tool at the cursor position."""
        self.app.drawing_canvas.delete("spray_preview")
        canvas_width = self.app.drawing_canvas.winfo_width()
        canvas_height = self.app.drawing_canvas.winfo_height()
        canvas_pixel_width = self.app.canvas.width * self.app.canvas.zoom
        canvas_pixel_height = self.app.canvas.height * self.app.canvas.zoom
        x_offset = (canvas_width - canvas_pixel_width) // 2 + self.app.pan_offset_x * self.app.canvas.zoom
        y_offset = (canvas_height - canvas_pixel_height) // 2 + self.app.pan_offset_y * self.app.canvas.zoom

        # Bounds check: only draw if circle intersects canvas
        radius = max(1, int(self.app.tool_size_mgr.spray_radius))
        min_x = canvas_x - radius
        max_x = canvas_x + radius
        min_y = canvas_y - radius
        max_y = canvas_y + radius
        if max_x > 0 and min_x < self.app.canvas.width and max_y > 0 and min_y < self.app.canvas.height:
            # Convert to screen coordinates
            screen_cx = x_offset + (canvas_x * self.app.canvas.zoom) + (self.app.canvas.zoom // 2)
            screen_cy = y_offset + (canvas_y * self.app.canvas.zoom) + (self.app.canvas.zoom // 2)
            r_screen = radius * self.app.canvas.zoom
            x1 = screen_cx - r_screen
            y1 = screen_cy - r_screen
            x2 = screen_cx + r_screen
            y2 = screen_cy + r_screen
            # Outline uses current color for clarity
            r, g, b, a = self.app.get_current_color()
            color_hex = f"#{r:02x}{g:02x}{b:02x}"
            self.app.drawing_canvas.create_oval(
                x1, y1, x2, y2,
                outline=color_hex,
                width=2,
                dash=(4, 4),
                tags="spray_preview"
            )

    def draw_texture_preview(self, tool, canvas_x: int, canvas_y: int):
        """Draw live preview of texture tool on tkinter canvas"""
        self.app.drawing_canvas.delete("texture_preview")
        texture_data = tool.get_preview_texture()
        if texture_data is None:
            return
        canvas_width = self.app.drawing_canvas.winfo_width()
        canvas_height = self.app.drawing_canvas.winfo_height()
        canvas_pixel_width = self.app.canvas.width * self.app.canvas.zoom
        canvas_pixel_height = self.app.canvas.height * self.app.canvas.zoom
        x_offset = (canvas_width - canvas_pixel_width) // 2 + self.app.pan_offset_x * self.app.canvas.zoom
        y_offset = (canvas_height - canvas_pixel_height) // 2 + self.app.pan_offset_y * self.app.canvas.zoom
        tex_height, tex_width = texture_data.shape[0], texture_data.shape[1]
        
        # Check if any part of the texture would be in bounds
        if canvas_x + tex_width > 0 and canvas_x < self.app.canvas.width and canvas_y + tex_height > 0 and canvas_y < self.app.canvas.height:
            for ty in range(tex_height):
                for tx in range(tex_width):
                    pixel_color = texture_data[ty, tx]
                    if pixel_color[3] > 0:
                        px = canvas_x + tx
                        py = canvas_y + ty
                        if 0 <= px < self.app.canvas.width and 0 <= py < self.app.canvas.height:
                            screen_x = x_offset + (px * self.app.canvas.zoom)
                            screen_y = y_offset + (py * self.app.canvas.zoom)
                            color_hex = f'#{pixel_color[0]:02x}{pixel_color[1]:02x}{pixel_color[2]:02x}'
                            self.app.drawing_canvas.create_rectangle(
                                screen_x, screen_y,
                                screen_x + self.app.canvas.zoom, screen_y + self.app.canvas.zoom,
                                fill=color_hex, outline=color_hex, stipple="gray50",
                                tags="texture_preview"
                            )
            screen_x1 = x_offset + (canvas_x * self.app.canvas.zoom)
            screen_y1 = y_offset + (canvas_y * self.app.canvas.zoom)
            screen_x2 = x_offset + ((canvas_x + tex_width) * self.app.canvas.zoom)
            screen_y2 = y_offset + ((canvas_y + tex_height) * self.app.canvas.zoom)
            self.app.drawing_canvas.create_rectangle(
                screen_x1, screen_y1, screen_x2, screen_y2,
                outline="#ffffff", width=2, dash=(4, 4),
                tags="texture_preview"
            )

    def draw_shape_preview(self, tool, canvas_x: int, canvas_y: int, color: tuple):
        """Draw live preview of shape tools (Line, Square, Circle) on tkinter canvas"""
        import math
        self.app.drawing_canvas.delete("shape_preview")
        canvas_width = self.app.drawing_canvas.winfo_width()
        canvas_height = self.app.drawing_canvas.winfo_height()
        canvas_pixel_width = self.app.canvas.width * self.app.canvas.zoom
        canvas_pixel_height = self.app.canvas.height * self.app.canvas.zoom
        x_offset = (canvas_width - canvas_pixel_width) // 2 + self.app.pan_offset_x * self.app.canvas.zoom
        y_offset = (canvas_height - canvas_pixel_height) // 2 + self.app.pan_offset_y * self.app.canvas.zoom
        color_hex = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
        if self.app.current_tool == "line" and tool.is_drawing:
            start_x, start_y = tool.start_point
            screen_x1 = x_offset + (start_x * self.app.canvas.zoom) + (self.app.canvas.zoom // 2)
            screen_y1 = y_offset + (start_y * self.app.canvas.zoom) + (self.app.canvas.zoom // 2)
            screen_x2 = x_offset + (canvas_x * self.app.canvas.zoom) + (self.app.canvas.zoom // 2)
            screen_y2 = y_offset + (canvas_y * self.app.canvas.zoom) + (self.app.canvas.zoom // 2)
            self.app.drawing_canvas.create_line(
                screen_x1, screen_y1, screen_x2, screen_y2,
                fill=color_hex, width=3, tags="shape_preview"
            )
        elif self.app.current_tool == "rectangle" and tool.is_drawing:
            start_x, start_y = tool.start_point
            left = min(start_x, canvas_x)
            right = max(start_x, canvas_x)
            top = min(start_y, canvas_y)
            bottom = max(start_y, canvas_y)
            screen_x1 = x_offset + (left * self.app.canvas.zoom)
            screen_y1 = y_offset + (top * self.app.canvas.zoom)
            screen_x2 = x_offset + ((right + 1) * self.app.canvas.zoom)
            screen_y2 = y_offset + ((bottom + 1) * self.app.canvas.zoom)
            if tool.filled:
                self.app.drawing_canvas.create_rectangle(
                    screen_x1, screen_y1, screen_x2, screen_y2,
                    fill=color_hex, outline="", tags="shape_preview"
                )
            else:
                self.app.drawing_canvas.create_rectangle(
                    screen_x1, screen_y1, screen_x2, screen_y2,
                    outline=color_hex, width=3, tags="shape_preview"
                )
        elif self.app.current_tool == "circle" and tool.is_drawing:
            center_x, center_y = tool.center
            dx = canvas_x - center_x
            dy = canvas_y - center_y
            radius_pixels = int(math.sqrt(dx * dx + dy * dy))
            radius_screen = radius_pixels * self.app.canvas.zoom
            screen_cx = x_offset + (center_x * self.app.canvas.zoom) + (self.app.canvas.zoom // 2)
            screen_cy = y_offset + (center_y * self.app.canvas.zoom) + (self.app.canvas.zoom // 2)
            screen_x1 = screen_cx - radius_screen
            screen_y1 = screen_cy - radius_screen
            screen_x2 = screen_cx + radius_screen
            screen_y2 = screen_cy + radius_screen
            if tool.filled:
                self.app.drawing_canvas.create_oval(
                    screen_x1, screen_y1, screen_x2, screen_y2,
                    fill=color_hex, outline="", tags="shape_preview"
                )
            else:
                self.app.drawing_canvas.create_oval(
                    screen_x1, screen_y1, screen_x2, screen_y2,
                    outline=color_hex, width=3, tags="shape_preview"
                )

    def draw_scale_handle(self, x: float, y: float, size: int, color: str):
        """Draw a scale handle at the given position"""
        half_size = size // 2
        self.app.drawing_canvas.create_rectangle(
            x - half_size, y - half_size,
            x + half_size, y + half_size,
            fill=color, outline="black", width=1,
            tags="scale_handle"
        )

    def draw_all_pixels_on_tkinter(self, x_offset: int, y_offset: int):
        """Draw all pixels from the canvas onto the tkinter canvas"""
        zoom = self.app.canvas.zoom
        
        # During live move or rotate preview, hide the source area so pixels don't appear doubled.
        move_tool = self.app.tools.get("move")
        selection_tool = self.app.tools.get("selection")
        skip_orig = False
        orig_left, orig_top, orig_width, orig_height = 0, 0, 0, 0
        # Also hide the last placed area while dragging (background is restored on pick-up,
        # but the flattened canvas may lag until we resync layers).
        skip_last = False
        last_left, last_top, last_width, last_height = 0, 0, 0, 0
        rotating_preview = bool(getattr(self.app, 'selection_mgr', None) and self.app.selection_mgr.is_rotating)
        if move_tool and move_tool.is_moving:
            if move_tool.original_selection:
                skip_orig = True
                orig_left, orig_top, orig_width, orig_height = move_tool.original_selection
            sel_tool = selection_tool
            if move_tool.last_drawn_position and sel_tool and sel_tool.selection_rect:
                skip_last = True
                last_left, last_top = move_tool.last_drawn_position
                _, _, last_width, last_height = sel_tool.selection_rect
        elif rotating_preview and selection_tool and selection_tool.selection_rect:
            # Hide the current selection area during rotate preview to avoid double-draw
            skip_last = True
            last_left, last_top, last_width, last_height = selection_tool.selection_rect
        
        # Get canvas pixels as numpy array for efficient processing
        canvas_pixels = self.app.canvas.pixels
        
        # Find all non-transparent pixels using NumPy (much faster than nested loops)
        non_transparent_mask = canvas_pixels[:, :, 3] > 0
        
        # Apply exclusion masks for move/rotate operations
        if skip_orig:
            for y in range(orig_top, min(orig_top + orig_height, self.app.canvas.height)):
                for x in range(orig_left, min(orig_left + orig_width, self.app.canvas.width)):
                    if 0 <= y < self.app.canvas.height and 0 <= x < self.app.canvas.width:
                        non_transparent_mask[y, x] = False
        
        if skip_last:
            for y in range(last_top, min(last_top + last_height, self.app.canvas.height)):
                for x in range(last_left, min(last_left + last_width, self.app.canvas.width)):
                    if 0 <= y < self.app.canvas.height and 0 <= x < self.app.canvas.width:
                        non_transparent_mask[y, x] = False
        
        # Get coordinates of non-transparent pixels
        y_coords, x_coords = np.where(non_transparent_mask)
        
        # Draw only the non-transparent pixels (much more efficient for sparse canvases)
        for i in range(len(y_coords)):
            y = y_coords[i]
            x = x_coords[i]
            color = tuple(canvas_pixels[y, x])
            screen_x = x_offset + (x * zoom)
            screen_y = y_offset + (y * zoom)
            
            hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            
            self.app.drawing_canvas.create_rectangle(
                screen_x, screen_y,
                screen_x + zoom, screen_y + zoom,
                fill=hex_color, outline="", tags="pixel"
            )

    def update_single_pixel(self, canvas_x: int, canvas_y: int, old_color):
        """Update only a single pixel for better performance"""
        # For now, just trigger a full update to ensure consistency
        # This prevents the disappearing pixel bug
        self.update_pixel_display()

    def draw_onion_skin(self, x_offset: int, y_offset: int, canvas_pixel_width: int, canvas_pixel_height: int):
        """Draw onion skin frames (previous and next frames with alpha blending)"""
        zoom = self.app.canvas.zoom
        timeline = self.app.timeline
        
        if not timeline.onion_skin_enabled:
            return
        
        # Draw previous frames (behind current)
        prev_frames = timeline.get_previous_frames(timeline.onion_skin_prev_frames)
        for i, frame in enumerate(prev_frames):
            opacity = timeline.onion_skin_prev_opacity * (1.0 - i * 0.2)  # Fade out older frames
            opacity = max(0.1, opacity)  # Minimum visibility
            self._draw_frame_with_opacity(frame.pixels, x_offset, y_offset, opacity, "#0000ff")  # Blue tint for previous
        
        # Draw next frames (behind current)
        next_frames = timeline.get_next_frames(timeline.onion_skin_next_frames)
        for i, frame in enumerate(next_frames):
            opacity = timeline.onion_skin_next_opacity * (1.0 - i * 0.2)  # Fade out future frames
            opacity = max(0.1, opacity)  # Minimum visibility
            self._draw_frame_with_opacity(frame.pixels, x_offset, y_offset, opacity, "#ff0000")  # Red tint for next
    
    def _draw_frame_with_opacity(self, pixels: np.ndarray, x_offset: int, y_offset: int, opacity: float, tint_color: str = None):
        """Draw a frame with alpha blending and optional color tint"""
        zoom = self.app.canvas.zoom
        
        # Find non-transparent pixels
        non_transparent_mask = pixels[:, :, 3] > 0
        y_coords, x_coords = np.where(non_transparent_mask)
        
        # Parse tint color if provided
        tint_r, tint_g, tint_b = 255, 255, 255
        if tint_color:
            tint_r = int(tint_color[1:3], 16)
            tint_g = int(tint_color[3:5], 16)
            tint_b = int(tint_color[5:7], 16)
        
        # Draw pixels with opacity
        for i in range(len(y_coords)):
            y = y_coords[i]
            x = x_coords[i]
            rgba = tuple(pixels[y, x])
            
            # Apply tint and opacity
            r = int(rgba[0] * (1 - 0.3) + tint_r * 0.3)  # 30% tint blend
            g = int(rgba[1] * (1 - 0.3) + tint_g * 0.3)
            b = int(rgba[2] * (1 - 0.3) + tint_b * 0.3)
            
            # Create semi-transparent color (Tkinter doesn't support alpha directly, so we blend with background)
            # For simplicity, we'll use a lighter/darker version based on opacity
            alpha = rgba[3] / 255.0 * opacity
            final_r = int(r * alpha + 128 * (1 - alpha))  # Blend with gray background
            final_g = int(g * alpha + 128 * (1 - alpha))
            final_b = int(b * alpha + 128 * (1 - alpha))
            
            hex_color = f"#{final_r:02x}{final_g:02x}{final_b:02x}"
            
            screen_x = x_offset + (x * zoom)
            screen_y = y_offset + (y * zoom)
            
            self.app.drawing_canvas.create_rectangle(
                screen_x, screen_y,
                screen_x + zoom, screen_y + zoom,
                fill=hex_color, outline="", tags="onion_skin"
            )
    
    def draw_tile_seam_preview(self, x_offset: int, y_offset: int, canvas_pixel_width: int, canvas_pixel_height: int):
        """Draw tile seam preview overlay showing edge mismatches"""
        zoom = self.app.canvas.zoom
        width = self.app.canvas.width
        height = self.app.canvas.height
        
        # Get current pixel data
        pixels = self.app.canvas.pixels
        
        # Check left vs right edges (vertical seams)
        for y in range(height):
            left_pixel = tuple(pixels[y, 0])
            right_pixel = tuple(pixels[y, width - 1])
            if left_pixel != right_pixel:
                # Highlight mismatch with red indicator
                screen_y = y_offset + (y * zoom)
                # Draw vertical line on left edge
                self.app.drawing_canvas.create_line(
                    x_offset, screen_y,
                    x_offset, screen_y + zoom,
                    fill="#ff0000", width=2, tags="tile_seam"
                )
                # Draw vertical line on right edge
                self.app.drawing_canvas.create_line(
                    x_offset + canvas_pixel_width - 1, screen_y,
                    x_offset + canvas_pixel_width - 1, screen_y + zoom,
                    fill="#ff0000", width=2, tags="tile_seam"
                )
        
        # Check top vs bottom edges (horizontal seams)
        for x in range(width):
            top_pixel = tuple(pixels[0, x])
            bottom_pixel = tuple(pixels[height - 1, x])
            if top_pixel != bottom_pixel:
                # Highlight mismatch with red indicator
                screen_x = x_offset + (x * zoom)
                # Draw horizontal line on top edge
                self.app.drawing_canvas.create_line(
                    screen_x, y_offset,
                    screen_x + zoom, y_offset,
                    fill="#ff0000", width=2, tags="tile_seam"
                )
                # Draw horizontal line on bottom edge
                self.app.drawing_canvas.create_line(
                    screen_x, y_offset + canvas_pixel_height - 1,
                    screen_x + zoom, y_offset + canvas_pixel_height - 1,
                    fill="#ff0000", width=2, tags="tile_seam"
                )
    
    def draw_tile_preview(self, x_offset: int, y_offset: int, canvas_pixel_width: int, canvas_pixel_height: int):
        """Draw repeating tile preview - shows canvas repeated in 3x3 grid for pattern visualization.
        
        This is optimized for performance:
        - Uses NumPy to find non-transparent pixels efficiently
        - Draws ghost tiles with stipple pattern for transparency effect
        - Only draws 8 surrounding tiles (not the center which is the main canvas)
        """
        zoom = self.app.canvas.zoom
        canvas_pixels = self.app.canvas.pixels
        
        # Find all non-transparent pixels using NumPy (much faster than nested loops)
        non_transparent_mask = canvas_pixels[:, :, 3] > 0
        y_coords, x_coords = np.where(non_transparent_mask)
        
        # If no pixels to draw, skip
        if len(y_coords) == 0:
            return
        
        # Define tile offsets for 3x3 grid (excluding center [0,0] which is main canvas)
        tile_offsets = [
            (-1, -1), (0, -1), (1, -1),  # Top row
            (-1,  0),          (1,  0),  # Middle row (no center)
            (-1,  1), (0,  1), (1,  1),  # Bottom row
        ]
        
        # Get view bounds to only draw tiles that are visible
        view_width = self.app.drawing_canvas.winfo_width()
        view_height = self.app.drawing_canvas.winfo_height()
        
        # Draw each surrounding tile
        for tile_dx, tile_dy in tile_offsets:
            # Calculate tile offset in screen coordinates
            tile_x_offset = x_offset + (tile_dx * canvas_pixel_width)
            tile_y_offset = y_offset + (tile_dy * canvas_pixel_height)
            
            # Skip tiles that are completely outside the view (performance optimization)
            if (tile_x_offset + canvas_pixel_width < 0 or tile_x_offset > view_width or
                tile_y_offset + canvas_pixel_height < 0 or tile_y_offset > view_height):
                continue
            
            # Draw non-transparent pixels for this tile with ghost effect
            for i in range(len(y_coords)):
                y = y_coords[i]
                x = x_coords[i]
                color = tuple(canvas_pixels[y, x])
                
                screen_x = tile_x_offset + (x * zoom)
                screen_y = tile_y_offset + (y * zoom)
                
                # Skip pixels outside view bounds
                if (screen_x + zoom < 0 or screen_x > view_width or
                    screen_y + zoom < 0 or screen_y > view_height):
                    continue
                
                # Use dimmed color for ghost tiles (50% brightness)
                ghost_r = color[0] // 2
                ghost_g = color[1] // 2
                ghost_b = color[2] // 2
                hex_color = f"#{ghost_r:02x}{ghost_g:02x}{ghost_b:02x}"
                
                self.app.drawing_canvas.create_rectangle(
                    screen_x, screen_y,
                    screen_x + zoom, screen_y + zoom,
                    fill=hex_color, outline="", 
                    stipple="gray50",  # Add transparency effect
                    tags="tile_preview"
                )
        
        # Draw subtle border around center tile to distinguish it
        self.app.drawing_canvas.create_rectangle(
            x_offset - 1, y_offset - 1,
            x_offset + canvas_pixel_width + 1, y_offset + canvas_pixel_height + 1,
            outline="#00ffff", width=2, dash=(6, 3),
            tags="tile_preview"
        )
    
    def force_canvas_update(self):
        """Force immediate tkinter canvas display update"""
        # Redraw the canvas surface (pixels + grid)
        self.app.canvas._redraw_surface()
        # Update the tkinter canvas to show current grid state
        self.update_pixel_display()
        # Force tkinter to process all pending events and update display
        self.app.root.update_idletasks()
        self.app.root.update()
    
    def _redraw_edge_lines_using_tool(self):
        """Redraw edge lines using the Edge tool's stored data"""
        if hasattr(self.app, 'tools') and 'edge' in self.app.tools:
            edge_tool = self.app.tools['edge']
            if hasattr(edge_tool, 'redraw_all_edges'):
                # Force redraw to ensure edges are restored after canvas clears
                edge_tool.redraw_all_edges(force=True)
