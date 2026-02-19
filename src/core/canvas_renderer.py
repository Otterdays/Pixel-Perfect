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
        
        # Mini preview state (Aseprite-style bottom-right overlay)
        self.show_mini_preview = True
        self._preview_photo = None  # Keep reference to prevent GC
        self._PREVIEW_MAX_SIZE = 128  # Max width/height of preview image
        self._PREVIEW_PADDING = 12  # Distance from canvas edges
        self._PREVIEW_HEADER_HEIGHT = 18  # Title bar height

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
                
                # Clear cached photo references from previous render cycle
                self._onion_photos = []

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
                
                # Draw mini preview overlay last (always on top)
                if self.show_mini_preview:
                    self.draw_mini_preview(width, height)
        finally:
            self.app._updating_display = False
            # Notify token preview (debounced) if panel exists
            if hasattr(self.app, 'token_preview_panel'):
                try:
                    self.app.token_preview_panel.notify_canvas_changed()
                except Exception:
                    pass

    def toggle_mini_preview(self):
        """Toggle the mini preview window visibility."""
        self.show_mini_preview = not self.show_mini_preview
        self.update_pixel_display()

    def draw_mini_preview(self, canvas_widget_width, canvas_widget_height):
        """Draw an Aseprite-style mini preview overlay in the bottom-right corner.
        
        Shows the full canvas artwork fitted into a small preview box with:
        - Checkerboard transparency background
        - Dark frame with 'Preview' header
        - Viewport rectangle showing the currently visible area
        """
        from PIL import Image, ImageTk, ImageDraw
        
        pad = self._PREVIEW_PADDING
        header_h = self._PREVIEW_HEADER_HEIGHT
        max_size = self._PREVIEW_MAX_SIZE
        
        cw = self.app.canvas.width
        ch = self.app.canvas.height
        if cw <= 0 or ch <= 0:
            return
        
        # --- Compute preview image size (fit canvas into max_size box) ---
        scale = min(max_size / cw, max_size / ch)
        # For small canvases make preview at least 2x to be useful
        if scale > 4:
            scale = 4
        prev_w = max(16, int(cw * scale))
        prev_h = max(16, int(ch * scale))
        
        # --- Build checkerboard transparency background ---
        checker_size = max(2, int(scale * 2))  # Scale checkerboard cells with preview
        checker = Image.new("RGB", (prev_w, prev_h), (200, 200, 200))
        checker_draw = ImageDraw.Draw(checker)
        dark_color = (160, 160, 160)
        for cy in range(0, prev_h, checker_size):
            for cx in range(0, prev_w, checker_size):
                if (cx // checker_size + cy // checker_size) % 2 == 1:
                    checker_draw.rectangle(
                        [cx, cy, cx + checker_size - 1, cy + checker_size - 1],
                        fill=dark_color
                    )
        checker = checker.convert("RGBA")
        
        # --- Build preview from canvas pixels ---
        pil_img = Image.fromarray(self.app.canvas.pixels, mode="RGBA")
        pil_img = pil_img.resize((prev_w, prev_h), Image.Resampling.NEAREST)
        
        # Composite artwork over checkerboard
        preview_img = Image.alpha_composite(checker, pil_img)
        
        # --- Build the full preview frame (header + image + border) ---
        border = 2
        frame_w = prev_w + border * 2
        frame_h = prev_h + header_h + border * 2
        
        # Dark semi-transparent frame background
        frame_img = Image.new("RGBA", (frame_w, frame_h), (30, 30, 30, 220))
        frame_draw = ImageDraw.Draw(frame_img)
        
        # Header bar (slightly lighter)
        frame_draw.rectangle([0, 0, frame_w - 1, header_h - 1], fill=(50, 50, 50, 230))
        
        # 'Preview' title text (simple pixel text since we may not have fonts)
        # Draw "Preview" as small block letters
        title = "Preview"
        # Use a small built-in font
        try:
            from PIL import ImageFont
            font = ImageFont.truetype("arial.ttf", 11)
        except Exception:
            font = ImageFont.load_default()
        
        # Center title in header
        try:
            bbox = font.getbbox(title)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
        except Exception:
            tw, th = 40, 10
        tx = (frame_w - tw) // 2
        ty = (header_h - th) // 2
        frame_draw.text((tx, ty), title, fill=(200, 200, 200, 255), font=font)
        
        # Subtle border highlight on top and left edges
        frame_draw.line([(0, 0), (frame_w - 1, 0)], fill=(80, 80, 80, 255))
        frame_draw.line([(0, 0), (0, frame_h - 1)], fill=(80, 80, 80, 255))
        # Dark border on bottom and right
        frame_draw.line([(frame_w - 1, 0), (frame_w - 1, frame_h - 1)], fill=(15, 15, 15, 255))
        frame_draw.line([(0, frame_h - 1), (frame_w - 1, frame_h - 1)], fill=(15, 15, 15, 255))
        
        # Paste preview image into frame
        frame_img.paste(preview_img, (border, header_h))
        
        # --- Draw viewport indicator (shows visible portion of canvas) ---
        zoom = self.app.canvas.zoom
        canvas_pixel_w = cw * zoom
        canvas_pixel_h = ch * zoom
        
        # Compute which part of the canvas is visible on screen
        cx_offset = (canvas_widget_width - canvas_pixel_w) / 2 + self.app.pan_offset_x * zoom
        cy_offset = (canvas_widget_height - canvas_pixel_h) / 2 + self.app.pan_offset_y * zoom
        
        # Visible area in canvas pixel coordinates
        vis_left = max(0, -cx_offset / zoom)
        vis_top = max(0, -cy_offset / zoom)
        vis_right = min(cw, (canvas_widget_width - cx_offset) / zoom)
        vis_bottom = min(ch, (canvas_widget_height - cy_offset) / zoom)
        
        # Only draw viewport rect if we're zoomed in enough that not everything is visible
        if vis_right - vis_left < cw - 0.5 or vis_bottom - vis_top < ch - 0.5:
            vr_x1 = border + int(vis_left * scale)
            vr_y1 = header_h + int(vis_top * scale)
            vr_x2 = border + int(vis_right * scale) - 1
            vr_y2 = header_h + int(vis_bottom * scale) - 1
            
            # Clamp to preview bounds
            vr_x1 = max(border, min(vr_x1, border + prev_w - 1))
            vr_y1 = max(header_h, min(vr_y1, header_h + prev_h - 1))
            vr_x2 = max(border, min(vr_x2, border + prev_w - 1))
            vr_y2 = max(header_h, min(vr_y2, header_h + prev_h - 1))
            
            # Draw white viewport rectangle
            frame_draw.rectangle([vr_x1, vr_y1, vr_x2, vr_y2], outline=(255, 255, 255, 200))
        
        # --- Position in bottom-right of canvas widget ---
        anchor_x = canvas_widget_width - pad
        anchor_y = canvas_widget_height - pad
        
        # Convert to PhotoImage and display
        self._preview_photo = ImageTk.PhotoImage(frame_img)
        self.app.drawing_canvas.create_image(
            anchor_x, anchor_y,
            image=self._preview_photo,
            anchor="se",
            tags="mini_preview"
        )

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
            
            # Floating size label near bottom-right of selection
            if width > 0 or height > 0:
                size_text = f"{width} x {height}"
                label_x = screen_x2 + 6
                label_y = screen_y2 + 6
                self.app.drawing_canvas.create_text(
                    label_x + 1, label_y + 1,
                    text=size_text, anchor="nw",
                    fill="black", font=("Consolas", 9, "bold"),
                    tags="selection"
                )
                self.app.drawing_canvas.create_text(
                    label_x, label_y,
                    text=size_text, anchor="nw",
                    fill="white", font=("Consolas", 9, "bold"),
                    tags="selection"
                )
        
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
        """Draw all pixels from the canvas onto the tkinter canvas using Pillow image rendering.
        
        Builds a PIL Image from the numpy pixel array, scales it to zoom level with
        NEAREST resampling (preserving crisp pixel art edges), and displays as a single
        canvas image item. This is dramatically faster than creating individual rectangles
        per pixel, especially for larger canvases (128×128, 256×256).
        """
        from PIL import Image, ImageTk
        
        zoom = self.app.canvas.zoom
        
        # During live move or rotate preview, hide the source area so pixels don't appear doubled.
        move_tool = self.app.tools.get("move")
        selection_tool = self.app.tools.get("selection")
        skip_orig = False
        orig_left, orig_top, orig_width, orig_height = 0, 0, 0, 0
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
            skip_last = True
            last_left, last_top, last_width, last_height = selection_tool.selection_rect
        
        # Get canvas pixels as numpy array
        canvas_pixels = self.app.canvas.pixels.copy()
        
        # Apply exclusion masks for move/rotate operations (zero out skipped areas)
        if skip_orig:
            y_start = max(0, orig_top)
            y_end = min(self.app.canvas.height, orig_top + orig_height)
            x_start = max(0, orig_left)
            x_end = min(self.app.canvas.width, orig_left + orig_width)
            if y_start < y_end and x_start < x_end:
                canvas_pixels[y_start:y_end, x_start:x_end] = 0
        
        if skip_last:
            y_start = max(0, last_top)
            y_end = min(self.app.canvas.height, last_top + last_height)
            x_start = max(0, last_left)
            x_end = min(self.app.canvas.width, last_left + last_width)
            if y_start < y_end and x_start < x_end:
                canvas_pixels[y_start:y_end, x_start:x_end] = 0
        
        # Build PIL Image from numpy RGBA array
        pil_img = Image.fromarray(canvas_pixels, mode="RGBA")
        
        # Scale up to zoom level using NEAREST for crisp pixel art
        display_width = int(self.app.canvas.width * zoom)
        display_height = int(self.app.canvas.height * zoom)
        
        if display_width > 0 and display_height > 0:
            pil_img = pil_img.resize((display_width, display_height), Image.Resampling.NEAREST)
            
            # Convert to PhotoImage and display as a single canvas image item
            self._pixel_photo = ImageTk.PhotoImage(pil_img)
            self.app.drawing_canvas.create_image(
                x_offset, y_offset,
                image=self._pixel_photo,
                anchor="nw",
                tags="pixel"
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
        """Draw a frame with alpha blending and optional color tint using Pillow image rendering"""
        from PIL import Image, ImageTk
        
        zoom = self.app.canvas.zoom
        
        # Parse tint color
        tint_r, tint_g, tint_b = 255, 255, 255
        if tint_color:
            tint_r = int(tint_color[1:3], 16)
            tint_g = int(tint_color[3:5], 16)
            tint_b = int(tint_color[5:7], 16)
        
        # Build tinted, opacity-adjusted image using numpy
        frame_pixels = pixels.copy().astype(np.float32)
        
        # Apply tint (30% blend)
        tint_blend = 0.3
        frame_pixels[:, :, 0] = frame_pixels[:, :, 0] * (1 - tint_blend) + tint_r * tint_blend
        frame_pixels[:, :, 1] = frame_pixels[:, :, 1] * (1 - tint_blend) + tint_g * tint_blend
        frame_pixels[:, :, 2] = frame_pixels[:, :, 2] * (1 - tint_blend) + tint_b * tint_blend
        
        # Apply opacity to alpha channel
        frame_pixels[:, :, 3] = frame_pixels[:, :, 3] * opacity
        
        # Clip and convert back to uint8
        frame_pixels = np.clip(frame_pixels, 0, 255).astype(np.uint8)
        
        # Build PIL Image
        pil_img = Image.fromarray(frame_pixels, mode="RGBA")
        
        # Scale up with NEAREST
        display_width = int(self.app.canvas.width * zoom)
        display_height = int(self.app.canvas.height * zoom)
        
        if display_width > 0 and display_height > 0:
            pil_img = pil_img.resize((display_width, display_height), Image.Resampling.NEAREST)
            
            # Store reference to prevent GC and display
            if not hasattr(self, '_onion_photos'):
                self._onion_photos = []
            photo = ImageTk.PhotoImage(pil_img)
            self._onion_photos.append(photo)
            
            self.app.drawing_canvas.create_image(
                x_offset, y_offset,
                image=photo,
                anchor="nw",
                tags="onion_skin"
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
        """Draw repeating tile preview - shows canvas repeated in 3x3 grid.
        
        Uses Pillow image rendering for performance - builds a dimmed ghost image
        of the canvas and stamps it around the center tile.
        """
        from PIL import Image, ImageTk
        
        zoom = self.app.canvas.zoom
        canvas_pixels = self.app.canvas.pixels
        
        # Check if canvas has any content
        if not np.any(canvas_pixels[:, :, 3] > 0):
            return
        
        # Build ghost tile image: dimmed to 50% brightness with 60% opacity
        ghost_pixels = canvas_pixels.copy().astype(np.float32)
        ghost_pixels[:, :, 0:3] = ghost_pixels[:, :, 0:3] * 0.5  # 50% brightness
        ghost_pixels[:, :, 3] = ghost_pixels[:, :, 3] * 0.6       # 60% opacity
        ghost_pixels = np.clip(ghost_pixels, 0, 255).astype(np.uint8)
        
        pil_ghost = Image.fromarray(ghost_pixels, mode="RGBA")
        
        # Scale up
        display_width = int(self.app.canvas.width * zoom)
        display_height = int(self.app.canvas.height * zoom)
        
        if display_width <= 0 or display_height <= 0:
            return
        
        pil_ghost = pil_ghost.resize((display_width, display_height), Image.Resampling.NEAREST)
        
        # Store photo references to prevent GC
        if not hasattr(self, '_tile_photos'):
            self._tile_photos = []
        self._tile_photos = []
        
        # Define tile offsets for 3x3 grid (excluding center)
        tile_offsets = [
            (-1, -1), (0, -1), (1, -1),
            (-1,  0),          (1,  0),
            (-1,  1), (0,  1), (1,  1),
        ]
        
        # Get view bounds for culling
        view_width = self.app.drawing_canvas.winfo_width()
        view_height = self.app.drawing_canvas.winfo_height()
        
        for tile_dx, tile_dy in tile_offsets:
            tile_x = x_offset + (tile_dx * canvas_pixel_width)
            tile_y = y_offset + (tile_dy * canvas_pixel_height)
            
            # Skip tiles outside the view
            if (tile_x + canvas_pixel_width < 0 or tile_x > view_width or
                tile_y + canvas_pixel_height < 0 or tile_y > view_height):
                continue
            
            photo = ImageTk.PhotoImage(pil_ghost)
            self._tile_photos.append(photo)
            
            self.app.drawing_canvas.create_image(
                tile_x, tile_y,
                image=photo,
                anchor="nw",
                tags="tile_preview"
            )
        
        # Draw subtle border around center tile 
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
