'''
canvas_renderer.py

Manages all rendering operations on the main canvas.
This includes drawing the pixel grid, rendering the image data,
displaying selection overlays, and other visual elements.
'''

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
        else:  # light mode
            # Force light background (visible on dark themes)
            return "#fafafa"  # Light background

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

                if self.app.canvas.show_grid:
                    self.draw_tkinter_grid(x_offset, y_offset, canvas_pixel_width, canvas_pixel_height)

                theme = self.app.theme_manager.get_current_theme()
                self.app.drawing_canvas.create_rectangle(
                    x_offset, y_offset,
                    x_offset + canvas_pixel_width, y_offset + canvas_pixel_height,
                    outline=theme.canvas_border, width=2, tags="border"
                )

                self.draw_all_pixels_on_tkinter(x_offset, y_offset)
                
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
        
        # Check if we're in a move operation to skip original selection area
        move_tool = self.app.tools.get("move")
        skip_original_selection = False
        orig_left, orig_top, orig_width, orig_height = 0, 0, 0, 0
        
        if (move_tool and move_tool.is_moving and move_tool.original_selection):
            skip_original_selection = True
            orig_left, orig_top, orig_width, orig_height = move_tool.original_selection
        
        # Draw all visible layers combined
        for y in range(self.app.canvas.height):
            for x in range(self.app.canvas.width):
                # Skip pixels in original selection area during move
                if skip_original_selection:
                    if (orig_left <= x < orig_left + orig_width and 
                        orig_top <= y < orig_top + orig_height):
                        continue  # Don't draw original selection pixels during move
                
                color = self.app.canvas.get_pixel(x, y)
                if color and color[3] > 0:  # Only draw non-transparent pixels
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

    def force_canvas_update(self):
        """Force immediate tkinter canvas display update"""
        # Redraw the canvas surface (pixels + grid)
        self.app.canvas._redraw_surface()
        # Update the tkinter canvas to show current grid state
        self.update_pixel_display()
        # Force tkinter to process all pending events and update display
        self.app.root.update_idletasks()
        self.app.root.update()
