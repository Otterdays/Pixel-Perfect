"""
Constants View for Pixel Perfect
Displays colors currently used on the canvas
"""

import customtkinter as ctk
from typing import Callable, List, Set, Tuple


class ConstantsView:
    """Manages the canvas constants (used colors) view"""
    
    def __init__(self, parent_frame: ctk.CTkFrame, canvas, palette, color_wheel,
                 view_mode_var, on_show_view: Callable):
        """
        Initialize the constants view
        
        Args:
            parent_frame: Parent frame to pack widgets into
            canvas: Canvas instance
            palette: ColorPalette instance
            color_wheel: ColorWheel instance
            view_mode_var: StringVar for current view mode
            on_show_view: Callback to show a specific view
        """
        self.parent_frame = parent_frame
        self.canvas = canvas
        self.palette = palette
        self.color_wheel = color_wheel
        self.view_mode_var = view_mode_var
        self.on_show_view = on_show_view
        
        # UI components
        self.color_buttons: List[ctk.CTkButton] = []
    
    def create(self):
        """Create the constants grid showing colors used on canvas"""
        # Clear existing widgets
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Extract unique colors from canvas
        used_colors = self._get_canvas_colors()
        
        if not used_colors:
            # Show message if no colors are used yet
            no_colors_label = ctk.CTkLabel(
                self.parent_frame,
                text="No colors used yet.\nDraw on canvas to see\ncolors here.",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            no_colors_label.pack(pady=20)
            return
        
        # Create grid of used colors
        grid_frame = ctk.CTkFrame(self.parent_frame)
        grid_frame.pack()
        
        # Configure grid - 4 columns
        for col in range(4):
            grid_frame.grid_columnconfigure(col, weight=1)
        
        # Create buttons for each unique color
        self.color_buttons.clear()
        for idx, color in enumerate(used_colors):
            row = idx // 4
            col = idx % 4
            
            r, g, b, a = color
            if a == 0:  # Skip transparent pixels
                continue
                
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            
            btn = ctk.CTkButton(
                grid_frame,
                text="",
                width=50,
                height=50,
                fg_color=hex_color,
                hover_color=hex_color,
                border_width=2,
                border_color="gray",
                corner_radius=3,
                command=lambda c=color: self._on_constant_color_click(c)
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            self.color_buttons.append(btn)
        
        # Show count label
        count_label = ctk.CTkLabel(
            self.parent_frame,
            text=f"{len(used_colors)} colors in use",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        count_label.pack(pady=(5, 0))
    
    def _get_canvas_colors(self) -> List[Tuple[int, int, int, int]]:
        """Extract unique colors from the canvas (all layers combined)"""
        unique_colors: Set[Tuple[int, int, int, int]] = set()
        
        # Get all pixels from all visible layers
        for y in range(self.canvas.height):
            for x in range(self.canvas.width):
                # Get pixel from the composited canvas (all visible layers)
                pixel_color = self.canvas.get_pixel(x, y)
                
                # Only add non-transparent pixels
                if pixel_color[3] > 0:
                    unique_colors.add(tuple(pixel_color))
        
        # Convert set to sorted list for consistent ordering
        return sorted(list(unique_colors))
    
    def _on_constant_color_click(self, color):
        """Handle click on a constant color button"""
        # Find if this color exists in the current palette
        r, g, b, a = color
        rgb_color = (r, g, b)
        
        # Try to find the color in the palette
        palette_colors = self.palette.colors
        found_index = None
        
        for i, pal_color in enumerate(palette_colors):
            if (pal_color[0], pal_color[1], pal_color[2]) == rgb_color:
                found_index = i
                break
        
        if found_index is not None:
            # Color found in palette, select it
            self.palette.set_primary_color(found_index)
        else:
            # Color not in current palette, switch to color wheel and set the color
            self.view_mode_var.set("wheel")
            if self.on_show_view:
                self.on_show_view("wheel")
            
            # Set the color on the existing color wheel
            if self.color_wheel:
                self.color_wheel.set_color(rgb_color[0], rgb_color[1], rgb_color[2])
    
    def apply_theme(self, theme):
        """Apply theme to constants view"""
        # Color buttons maintain their actual colors
        pass

