"""
Color wheel component for Pixel Perfect
HSV-based color selection with CustomTkinter
"""

import customtkinter as ctk
import math
from typing import Tuple, Optional, Callable
from PIL import Image, ImageDraw, ImageTk

class ColorWheel:
    """HSV color wheel component for color selection"""
    
    def __init__(self, parent_frame: ctk.CTkFrame, size: int = 250):
        self.parent_frame = parent_frame
        self.size = size
        self.on_color_changed: Optional[Callable] = None
        self.on_save_custom_color: Optional[Callable] = None  # Callback for saving custom color
        self.on_remove_custom_color: Optional[Callable] = None  # Callback for removing custom color
        
        # Color state (HSV)
        self.hue = 0.0  # 0-360
        self.saturation = 1.0  # 0-1
        self.value = 1.0  # 0-1 (brightness)
        
        # UI components
        self.wheel_canvas = None
        self.saturation_canvas = None
        self.brightness_slider = None
        self.color_preview = None
        self.hsv_labels = None
        self.hex_label = None
        
        # Interaction state
        self.is_dragging_hue = False
        self.is_dragging_saturation = False
        self.is_dragging_brightness = False
        self.cursor_y = 90  # Track cursor Y position in saturation box for indicator
        
        self._create_ui()
        self._update_displays()
    
    def _create_ui(self):
        """Create the color wheel UI - floating components on grey background"""
        # No main container frame - pack directly to parent for transparent look
        
        # Hue wheel (floating)
        self.wheel_canvas = ctk.CTkCanvas(
            self.parent_frame,
            width=self.size,
            height=self.size,
            bg="black",
            highlightthickness=0,
            cursor="crosshair"
        )
        self.wheel_canvas.pack(pady=5)
        self.wheel_canvas.bind("<Button-1>", self._on_wheel_click)
        self.wheel_canvas.bind("<B1-Motion>", self._on_wheel_drag)
        self.wheel_canvas.bind("<ButtonRelease-1>", self._on_wheel_release)
        
        # Saturation/Value square (floating)
        self.saturation_canvas = ctk.CTkCanvas(
            self.parent_frame,
            width=180,
            height=180,
            bg="black",
            highlightthickness=0,
            cursor="crosshair"
        )
        self.saturation_canvas.pack(pady=5)
        self.saturation_canvas.bind("<Button-1>", self._on_saturation_click)
        self.saturation_canvas.bind("<B1-Motion>", self._on_saturation_drag)
        self.saturation_canvas.bind("<ButtonRelease-1>", self._on_saturation_release)
        
        # Color preview with label (floating)
        preview_label = ctk.CTkLabel(self.parent_frame, text="Preview", font=ctk.CTkFont(size=12, weight="bold"))
        preview_label.pack(pady=(10, 2))
        
        self.color_preview = ctk.CTkFrame(self.parent_frame, width=100, height=100)
        self.color_preview.pack(pady=5)
        
        # HEX display (floating, centered)
        hex_container = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        hex_container.pack(pady=5)
        
        hex_label = ctk.CTkLabel(hex_container, text="HEX:", font=ctk.CTkFont(size=12, weight="bold"))
        hex_label.pack(side="left", padx=2)
        
        self.hex_label = ctk.CTkLabel(
            hex_container, 
            text="#FF0000", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.hex_label.pack(side="left", padx=2)
        
        # HSV and RGB values side by side (floating)
        values_container = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        values_container.pack(pady=5)
        
        # HSV column
        hsv_col = ctk.CTkFrame(values_container, fg_color="transparent")
        hsv_col.pack(side="left", padx=15)
        
        hsv_title = ctk.CTkLabel(hsv_col, text="HSV", font=ctk.CTkFont(size=12, weight="bold"))
        hsv_title.pack()
        
        self.h_value_label = ctk.CTkLabel(hsv_col, text="H: 0°", font=ctk.CTkFont(size=11))
        self.h_value_label.pack(pady=1)
        
        self.s_value_label = ctk.CTkLabel(hsv_col, text="S: 100%", font=ctk.CTkFont(size=11))
        self.s_value_label.pack(pady=1)
        
        self.v_value_label = ctk.CTkLabel(hsv_col, text="V: 100%", font=ctk.CTkFont(size=11))
        self.v_value_label.pack(pady=1)
        
        # RGB column
        rgb_col = ctk.CTkFrame(values_container, fg_color="transparent")
        rgb_col.pack(side="left", padx=15)
        
        rgb_title = ctk.CTkLabel(rgb_col, text="RGB", font=ctk.CTkFont(size=12, weight="bold"))
        rgb_title.pack()
        
        self.r_value_label = ctk.CTkLabel(rgb_col, text="R: 255", font=ctk.CTkFont(size=11))
        self.r_value_label.pack(pady=1)
        
        self.g_value_label = ctk.CTkLabel(rgb_col, text="G: 0", font=ctk.CTkFont(size=11))
        self.g_value_label.pack(pady=1)
        
        self.b_value_label = ctk.CTkLabel(rgb_col, text="B: 0", font=ctk.CTkFont(size=11))
        self.b_value_label.pack(pady=1)
        
        # Brightness slider (floating)
        brightness_label = ctk.CTkLabel(self.parent_frame, text="Brightness", font=ctk.CTkFont(size=12, weight="bold"))
        brightness_label.pack(pady=(10, 2))
        
        self.brightness_slider = ctk.CTkSlider(
            self.parent_frame,
            from_=0,
            to=100,
            number_of_steps=100,
            command=self._on_brightness_change
        )
        self.brightness_slider.pack(padx=20, pady=5)
        self.brightness_slider.set(100)  # Start at full brightness
        
        # Action buttons (floating)
        self.save_custom_btn = ctk.CTkButton(
            self.parent_frame,
            text="Save Custom Color",
            command=self._save_custom_color,
            height=32,
            fg_color="green"
        )
        self.save_custom_btn.pack(fill="x", padx=10, pady=2)
        
        self.delete_color_btn = ctk.CTkButton(
            self.parent_frame,
            text="Delete Color",
            command=self._delete_selected_color,
            height=32,
            fg_color="red"
        )
        self.delete_color_btn.pack(fill="x", padx=10, pady=2)
        
        # Custom Colors Section (floating)
        custom_title = ctk.CTkLabel(
            self.parent_frame,
            text="Custom Colors",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        custom_title.pack(pady=(10, 5))
        
        # Scrollable frame for custom colors grid
        self.custom_colors_container = ctk.CTkScrollableFrame(
            self.parent_frame,
            height=150
        )
        self.custom_colors_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Grid will be populated dynamically
        self.custom_color_buttons = []
        self.selected_custom_color = None  # Track selected color for deletion
    
    def _draw_hue_wheel(self):
        """Draw the HSV hue wheel"""
        self.wheel_canvas.delete("all")
        
        # Create hue wheel image
        wheel_size = self.size - 20  # Leave margin
        center_x = self.size // 2
        center_y = self.size // 2
        radius = wheel_size // 2
        
        # Create PIL image for the wheel
        img = Image.new('RGB', (self.size, self.size), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw hue wheel
        for y in range(self.size):
            for x in range(self.size):
                dx = x - center_x
                dy = y - center_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance <= radius and distance >= radius - 30:  # Wheel thickness
                    angle = math.atan2(dy, dx)
                    hue = (math.degrees(angle) + 180) % 360
                    rgb = self._hsv_to_rgb(hue, 1.0, 1.0)
                    img.putpixel((x, y), rgb)
        
        # Convert to PhotoImage and display
        self.wheel_image = ImageTk.PhotoImage(img)
        self.wheel_canvas.create_image(center_x, center_y, image=self.wheel_image)
        
        # Draw hue indicator
        self._draw_hue_indicator()
    
    def _draw_saturation_square(self):
        """Draw the saturation square (respects current brightness)"""
        self.saturation_canvas.delete("all")
        
        # Create saturation square image
        square_size = 180
        img = Image.new('RGB', (square_size, square_size), (0, 0, 0))
        
        # Get current hue and brightness (value)
        current_hue = self.hue
        current_value = self.value  # Use current brightness from slider
        
        # Draw saturation gradient from white (left) to full color (right) at current brightness
        for y in range(square_size):
            for x in range(square_size):
                # X-axis: 0% saturation (left/white) to 100% saturation (right/full color)
                saturation = x / (square_size - 1)
                
                # Y-axis: White (top) to Black (bottom) - controls lightness at current saturation
                # This creates a natural gradient from light to dark
                brightness_mod = 1.0 - (y / (square_size - 1))
                adjusted_value = current_value * brightness_mod
                
                rgb = self._hsv_to_rgb(current_hue, saturation, adjusted_value)
                img.putpixel((x, y), rgb)
        
        # Convert to PhotoImage and display
        self.saturation_image = ImageTk.PhotoImage(img)
        self.saturation_canvas.create_image(square_size//2, square_size//2, image=self.saturation_image)
        
        # Draw saturation indicator
        self._draw_saturation_indicator()
    
    def _draw_hue_indicator(self):
        """Draw the hue selection indicator"""
        center_x = self.size // 2
        center_y = self.size // 2
        radius = (self.size - 20) // 2 - 15  # Position on wheel
        
        # Calculate position based on current hue
        # Apply the same offset as the wheel drawing: subtract 180 degrees
        # to match the visual position on the wheel
        display_hue = (self.hue - 180) % 360
        angle = math.radians(display_hue)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        # Draw indicator circle with tag for easy deletion
        self.wheel_canvas.create_oval(
            x-6, y-6, x+6, y+6,
            fill="white", outline="black", width=2, tags="indicator"
        )
    
    def _draw_saturation_indicator(self):
        """Draw the saturation selection indicator"""
        square_size = 180
        
        # Calculate position based on current saturation
        # X-axis represents saturation (0% left to 100% right)
        x = self.saturation * (square_size - 1)
        # Y follows cursor position for natural dragging feel (stored in self.cursor_y)
        y = getattr(self, 'cursor_y', square_size // 2)
        
        # Draw indicator circle with tag for easy deletion
        self.saturation_canvas.create_oval(
            x-6, y-6, x+6, y+6,
            fill="", outline="white", width=3, tags="indicator"
        )
        self.saturation_canvas.create_oval(
            x-5, y-5, x+5, y+5,
            fill="", outline="black", width=1, tags="indicator"
        )
    
    def _hsv_to_rgb(self, h: float, s: float, v: float) -> Tuple[int, int, int]:
        """Convert HSV to RGB"""
        h = h % 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))
    
    def _rgb_to_hsv(self, r: int, g: int, b: int) -> Tuple[float, float, float]:
        """Convert RGB to HSV"""
        r, g, b = r/255.0, g/255.0, b/255.0
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        diff = max_val - min_val
        
        # Value
        v = max_val
        
        # Saturation
        s = 0 if max_val == 0 else diff / max_val
        
        # Hue
        if diff == 0:
            h = 0
        elif max_val == r:
            h = (60 * ((g - b) / diff) + 360) % 360
        elif max_val == g:
            h = (60 * ((b - r) / diff) + 120) % 360
        else:
            h = (60 * ((r - g) / diff) + 240) % 360
        
        return h, s, v
    
    def _update_displays(self, redraw_wheel=True, redraw_square=True):
        """Update all color displays
        
        Args:
            redraw_wheel: If True, redraw entire hue wheel (expensive)
            redraw_square: If True, redraw entire saturation square (expensive)
        """
        # Only redraw wheel if needed (hue changed or initial draw)
        if redraw_wheel:
            self._draw_hue_wheel()
        else:
            # Just update the indicator position (cheap)
            self.wheel_canvas.delete("indicator")
            self._draw_hue_indicator()
        
        # Only redraw square if needed (hue or brightness changed)
        if redraw_square:
            self._draw_saturation_square()
        else:
            # Just update the indicator position (cheap)
            self.saturation_canvas.delete("indicator")
            self._draw_saturation_indicator()
        
        # Update color preview
        rgb = self._hsv_to_rgb(self.hue, self.saturation, self.value)
        hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        self.color_preview.configure(fg_color=hex_color)
        
        # Update HEX label
        self.hex_label.configure(text=hex_color.upper())
        
        # Update HSV labels
        self.h_value_label.configure(text=f"H: {int(self.hue)}°")
        self.s_value_label.configure(text=f"S: {int(self.saturation * 100)}%")
        self.v_value_label.configure(text=f"V: {int(self.value * 100)}%")
        
        # Update RGB labels
        self.r_value_label.configure(text=f"R: {rgb[0]}")
        self.g_value_label.configure(text=f"G: {rgb[1]}")
        self.b_value_label.configure(text=f"B: {rgb[2]}")
        
        # Call callback if set
        if self.on_color_changed:
            self.on_color_changed(rgb)
    
    def _on_wheel_click(self, event):
        """Handle hue wheel click"""
        self.is_dragging_hue = True
        self._update_hue_from_position(event.x, event.y)
    
    def _on_wheel_drag(self, event):
        """Handle hue wheel drag"""
        if self.is_dragging_hue:
            self._update_hue_from_position(event.x, event.y)
    
    def _on_wheel_release(self, event):
        """Handle hue wheel release"""
        self.is_dragging_hue = False
    
    def _on_saturation_click(self, event):
        """Handle saturation square click"""
        self.is_dragging_saturation = True
        self._update_saturation_from_position(event.x, event.y)
    
    def _on_saturation_drag(self, event):
        """Handle saturation square drag"""
        if self.is_dragging_saturation:
            self._update_saturation_from_position(event.x, event.y)
    
    def _on_saturation_release(self, event):
        """Handle saturation square release"""
        self.is_dragging_saturation = False
    
    def _update_hue_from_position(self, x: int, y: int):
        """Update hue based on wheel position"""
        center_x = self.size // 2
        center_y = self.size // 2
        
        dx = x - center_x
        dy = y - center_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        radius = (self.size - 20) // 2
        if 15 <= distance <= radius:  # Within wheel bounds
            angle = math.atan2(dy, dx)
            # Match the drawing calculation: use +180 to align with wheel
            self.hue = (math.degrees(angle) + 180) % 360
            # Redraw square (depends on hue) but not wheel (just update indicator)
            self._update_displays(redraw_wheel=False, redraw_square=True)
    
    def _update_saturation_from_position(self, x: int, y: int):
        """Update saturation from horizontal position only"""
        square_size = 180
        
        # Clamp coordinates
        x = max(0, min(square_size - 1, x))
        y = max(0, min(square_size - 1, y))
        
        # Store cursor Y position for indicator display
        self.cursor_y = y
        
        # Only update saturation (X-axis controls saturation)
        self.saturation = x / (square_size - 1)
        # Brightness/Value is controlled by the slider only (Y-axis doesn't affect value)
        
        # Update displays - no need to redraw wheel or square when just dragging
        self._update_displays(redraw_wheel=False, redraw_square=False)
    
    def _on_brightness_change(self, value):
        """Handle brightness slider change"""
        self.value = float(value) / 100.0
        # Redraw square (depends on brightness) but not wheel
        self._update_displays(redraw_wheel=False, redraw_square=True)
    
    def _save_custom_color(self):
        """Save current color to custom colors"""
        if self.on_save_custom_color:
            rgb = self._hsv_to_rgb(self.hue, self.saturation, self.value)
            self.on_save_custom_color(rgb)
        else:
            print("[WARN] Custom colors not connected")
    
    def _delete_selected_color(self):
        """Delete the currently selected custom color"""
        if self.selected_custom_color:
            if self.on_remove_custom_color:
                self.on_remove_custom_color(self.selected_custom_color)
            else:
                print("[WARN] Custom colors not connected")
        else:
            print("[WARN] No custom color selected. Click a custom color first.")
    
    def update_custom_colors_grid(self, colors):
        """Update the custom colors grid display"""
        # Clear existing buttons
        for btn in self.custom_color_buttons:
            btn.destroy()
        self.custom_color_buttons.clear()
        
        # Reset selection if current selected color is not in the list
        if self.selected_custom_color and self.selected_custom_color not in colors:
            self.selected_custom_color = None
        
        # Configure grid columns to expand equally (4 columns)
        for col_idx in range(4):
            self.custom_colors_container.grid_columnconfigure(col_idx, weight=1, uniform="custom_color")
        
        # Create grid of color buttons (4 columns) that expand to fill space
        for i, color in enumerate(colors):
            r, g, b, a = color
            row = i // 4
            col = i % 4
            
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            
            # Check if this color is selected
            is_selected = (self.selected_custom_color == color)
            border_width = 3 if is_selected else 0
            border_color = "white" if is_selected else None
            
            btn = ctk.CTkButton(
                self.custom_colors_container,
                text="",
                width=50,
                height=50,
                fg_color=hex_color,
                hover_color=f"#{min(255, r+30):02x}{min(255, g+30):02x}{min(255, b+30):02x}",
                border_width=border_width,
                border_color=border_color
            )
            # Make buttons sticky to fill their grid cells
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
            
            # Bind click to select this color
            btn.bind("<Button-1>", lambda e, c=color, b=btn: self._select_custom_color(c, b))
            
            self.custom_color_buttons.append(btn)
    
    def _select_custom_color(self, color, button):
        """Select a custom color from the grid"""
        r, g, b, a = color
        
        # Update selected color
        self.selected_custom_color = color
        
        # Update all button borders to show selection
        for btn in self.custom_color_buttons:
            btn.configure(border_width=0)
        button.configure(border_width=3, border_color="white")
        
        # Load color into wheel
        self.set_color(r, g, b)
        print(f"[SELECT] Custom color: ({r}, {g}, {b})")
    
    
    def set_color(self, r: int, g: int, b: int):
        """Set color from RGB values"""
        self.hue, self.saturation, self.value = self._rgb_to_hsv(r, g, b)
        self.brightness_slider.set(self.value * 100)
        self._update_displays()
    
    def get_color(self) -> Tuple[int, int, int]:
        """Get current color as RGB"""
        return self._hsv_to_rgb(self.hue, self.saturation, self.value)