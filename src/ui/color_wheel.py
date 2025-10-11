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
    
    def __init__(self, parent_frame: ctk.CTkFrame, size: int = 200):
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
        
        # Interaction state
        self.is_dragging_hue = False
        self.is_dragging_saturation = False
        self.is_dragging_brightness = False
        
        self._create_ui()
        self._update_displays()
    
    def _create_ui(self):
        """Create the color wheel UI"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.parent_frame)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Color Wheel", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(10, 5))
        
        # Top section - Color wheel and saturation square
        top_frame = ctk.CTkFrame(self.main_frame)
        top_frame.pack(fill="x", padx=10, pady=5)
        
        # Hue wheel (centered)
        wheel_container = ctk.CTkFrame(top_frame)
        wheel_container.pack(pady=10)
        
        self.wheel_canvas = ctk.CTkCanvas(
            wheel_container,
            width=self.size,
            height=self.size,
            bg="black",
            highlightthickness=0
        )
        self.wheel_canvas.pack()
        self.wheel_canvas.bind("<Button-1>", self._on_wheel_click)
        self.wheel_canvas.bind("<B1-Motion>", self._on_wheel_drag)
        self.wheel_canvas.bind("<ButtonRelease-1>", self._on_wheel_release)
        
        # Saturation/Value square (centered below wheel)
        saturation_container = ctk.CTkFrame(top_frame)
        saturation_container.pack(pady=5)
        
        self.saturation_canvas = ctk.CTkCanvas(
            saturation_container,
            width=150,
            height=150,
            bg="black",
            highlightthickness=0
        )
        self.saturation_canvas.pack()
        self.saturation_canvas.bind("<Button-1>", self._on_saturation_click)
        self.saturation_canvas.bind("<B1-Motion>", self._on_saturation_drag)
        self.saturation_canvas.bind("<ButtonRelease-1>", self._on_saturation_release)
        
        # Bottom section - All controls below saturation square
        bottom_frame = ctk.CTkFrame(self.main_frame)
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Controls in a horizontal layout
        controls_row = ctk.CTkFrame(bottom_frame)
        controls_row.pack(fill="x", pady=5)
        
        # Left column - Preview and Brightness
        left_col = ctk.CTkFrame(controls_row)
        left_col.pack(side="left", padx=10, pady=5)
        
        preview_label = ctk.CTkLabel(left_col, text="Preview", font=ctk.CTkFont(size=12, weight="bold"))
        preview_label.pack(pady=(0, 5))
        
        self.color_preview = ctk.CTkFrame(left_col, width=80, height=80)
        self.color_preview.pack(pady=5)
        
        brightness_label = ctk.CTkLabel(left_col, text="Brightness", font=ctk.CTkFont(size=12, weight="bold"))
        brightness_label.pack(pady=(10, 5))
        
        self.brightness_slider = ctk.CTkSlider(
            left_col,
            from_=0,
            to=100,
            number_of_steps=100,
            width=150,
            command=self._on_brightness_change
        )
        self.brightness_slider.pack(pady=5)
        self.brightness_slider.set(100)  # Start at full brightness
        
        # Middle column - HSV values
        middle_col = ctk.CTkFrame(controls_row)
        middle_col.pack(side="left", padx=10, pady=5)
        
        hsv_title = ctk.CTkLabel(middle_col, text="HSV", font=ctk.CTkFont(size=12, weight="bold"))
        hsv_title.pack(pady=(0, 5))
        
        hsv_values_frame = ctk.CTkFrame(middle_col)
        hsv_values_frame.pack()
        
        # H label and value in same row
        h_row = ctk.CTkFrame(hsv_values_frame)
        h_row.pack(fill="x", pady=2)
        h_label = ctk.CTkLabel(h_row, text="H:", width=25, anchor="w")
        h_label.pack(side="left")
        self.h_value_label = ctk.CTkLabel(h_row, text="0°", width=50, anchor="e")
        self.h_value_label.pack(side="left")
        
        # S label and value in same row
        s_row = ctk.CTkFrame(hsv_values_frame)
        s_row.pack(fill="x", pady=2)
        s_label = ctk.CTkLabel(s_row, text="S:", width=25, anchor="w")
        s_label.pack(side="left")
        self.s_value_label = ctk.CTkLabel(s_row, text="100%", width=50, anchor="e")
        self.s_value_label.pack(side="left")
        
        # V label and value in same row
        v_row = ctk.CTkFrame(hsv_values_frame)
        v_row.pack(fill="x", pady=2)
        v_label = ctk.CTkLabel(v_row, text="V:", width=25, anchor="w")
        v_label.pack(side="left")
        self.v_value_label = ctk.CTkLabel(v_row, text="100%", width=50, anchor="e")
        self.v_value_label.pack(side="left")
        
        # Right column - RGB values
        right_col = ctk.CTkFrame(controls_row)
        right_col.pack(side="left", padx=10, pady=5)
        
        rgb_title = ctk.CTkLabel(right_col, text="RGB", font=ctk.CTkFont(size=12, weight="bold"))
        rgb_title.pack(pady=(0, 5))
        
        rgb_values_frame = ctk.CTkFrame(right_col)
        rgb_values_frame.pack()
        
        # R label and value in same row
        r_row = ctk.CTkFrame(rgb_values_frame)
        r_row.pack(fill="x", pady=2)
        r_label = ctk.CTkLabel(r_row, text="R:", width=25, anchor="w")
        r_label.pack(side="left")
        self.r_value_label = ctk.CTkLabel(r_row, text="255", width=50, anchor="e")
        self.r_value_label.pack(side="left")
        
        # G label and value in same row
        g_row = ctk.CTkFrame(rgb_values_frame)
        g_row.pack(fill="x", pady=2)
        g_label = ctk.CTkLabel(g_row, text="G:", width=25, anchor="w")
        g_label.pack(side="left")
        self.g_value_label = ctk.CTkLabel(g_row, text="0", width=50, anchor="e")
        self.g_value_label.pack(side="left")
        
        # B label and value in same row
        b_row = ctk.CTkFrame(rgb_values_frame)
        b_row.pack(fill="x", pady=2)
        b_label = ctk.CTkLabel(b_row, text="B:", width=25, anchor="w")
        b_label.pack(side="left")
        self.b_value_label = ctk.CTkLabel(b_row, text="0", width=50, anchor="e")
        self.b_value_label.pack(side="left")
        
        # Action buttons at bottom (full width)
        button_frame = ctk.CTkFrame(bottom_frame)
        button_frame.pack(fill="x", pady=10, padx=10)
        
        self.save_custom_btn = ctk.CTkButton(
            button_frame,
            text="Save Custom Color",
            command=self._save_custom_color,
            height=30,
            fg_color="green"
        )
        self.save_custom_btn.pack(fill="x", pady=2)
        
        self.delete_color_btn = ctk.CTkButton(
            button_frame,
            text="Delete Color",
            command=self._delete_selected_color,
            height=30,
            fg_color="red"
        )
        self.delete_color_btn.pack(fill="x", pady=2)
        
        # Custom Colors Section
        custom_colors_frame = ctk.CTkFrame(bottom_frame)
        custom_colors_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        custom_title = ctk.CTkLabel(
            custom_colors_frame,
            text="Custom Colors",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        custom_title.pack(pady=(5, 10))
        
        # Scrollable frame for custom colors grid
        self.custom_colors_container = ctk.CTkScrollableFrame(
            custom_colors_frame,
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
        """Draw the saturation/value square"""
        self.saturation_canvas.delete("all")
        
        # Create saturation/value square image
        square_size = 150
        img = Image.new('RGB', (square_size, square_size), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Get current hue
        current_hue = self.hue
        
        # Draw saturation/value gradient
        for y in range(square_size):
            for x in range(square_size):
                saturation = x / (square_size - 1)
                value = 1.0 - (y / (square_size - 1))  # Invert Y for value
                
                rgb = self._hsv_to_rgb(current_hue, saturation, value)
                img.putpixel((x, y), rgb)
        
        # Convert to PhotoImage and display
        self.saturation_image = ImageTk.PhotoImage(img)
        self.saturation_canvas.create_image(square_size//2, square_size//2, image=self.saturation_image)
        
        # Draw saturation/value indicator
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
        
        # Draw indicator circle
        self.wheel_canvas.create_oval(
            x-6, y-6, x+6, y+6,
            fill="white", outline="black", width=2
        )
    
    def _draw_saturation_indicator(self):
        """Draw the saturation/value selection indicator"""
        square_size = 150
        
        # Calculate position based on current saturation and value
        x = self.saturation * (square_size - 1)
        y = (1.0 - self.value) * (square_size - 1)  # Invert Y for value
        
        # Draw indicator cross
        self.saturation_canvas.create_line(
            x-8, y, x+8, y,
            fill="white", width=2
        )
        self.saturation_canvas.create_line(
            x, y-8, x, y+8,
            fill="white", width=2
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
    
    def _update_displays(self):
        """Update all color displays"""
        # Update hue wheel
        self._draw_hue_wheel()
        
        # Update saturation square
        self._draw_saturation_square()
        
        # Update color preview
        rgb = self._hsv_to_rgb(self.hue, self.saturation, self.value)
        hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        self.color_preview.configure(fg_color=hex_color)
        
        # Update labels
        self.h_value_label.configure(text=f"{int(self.hue)}°")
        self.s_value_label.configure(text=f"{int(self.saturation * 100)}%")
        self.v_value_label.configure(text=f"{int(self.value * 100)}%")
        
        self.r_value_label.configure(text=str(rgb[0]))
        self.g_value_label.configure(text=str(rgb[1]))
        self.b_value_label.configure(text=str(rgb[2]))
        
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
            self._update_displays()
    
    def _update_saturation_from_position(self, x: int, y: int):
        """Update saturation and value based on square position"""
        square_size = 150
        
        # Clamp coordinates
        x = max(0, min(square_size - 1, x))
        y = max(0, min(square_size - 1, y))
        
        self.saturation = x / (square_size - 1)
        self.value = 1.0 - (y / (square_size - 1))  # Invert Y for value
        
        # Update displays and trigger callback
        self._update_displays()
    
    def _on_brightness_change(self, value):
        """Handle brightness slider change"""
        self.value = float(value) / 100.0
        self._update_displays()
    
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
        
        # Create grid of color buttons (4 columns)
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
                width=40,
                height=40,
                fg_color=hex_color,
                hover_color=f"#{min(255, r+30):02x}{min(255, g+30):02x}{min(255, b+30):02x}",
                border_width=border_width,
                border_color=border_color
            )
            btn.grid(row=row, column=col, padx=3, pady=3)
            
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