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
        
        # Color wheel and controls frame
        controls_frame = ctk.CTkFrame(self.main_frame)
        controls_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Left side - Color wheel
        left_frame = ctk.CTkFrame(controls_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        # Hue wheel
        self.wheel_canvas = ctk.CTkCanvas(
            left_frame,
            width=self.size,
            height=self.size,
            bg="black",
            highlightthickness=0
        )
        self.wheel_canvas.pack(pady=10)
        self.wheel_canvas.bind("<Button-1>", self._on_wheel_click)
        self.wheel_canvas.bind("<B1-Motion>", self._on_wheel_drag)
        self.wheel_canvas.bind("<ButtonRelease-1>", self._on_wheel_release)
        
        # Saturation/Value square
        self.saturation_canvas = ctk.CTkCanvas(
            left_frame,
            width=150,
            height=150,
            bg="black",
            highlightthickness=0
        )
        self.saturation_canvas.pack(pady=5)
        self.saturation_canvas.bind("<Button-1>", self._on_saturation_click)
        self.saturation_canvas.bind("<B1-Motion>", self._on_saturation_drag)
        self.saturation_canvas.bind("<ButtonRelease-1>", self._on_saturation_release)
        
        # Right side - Controls
        right_frame = ctk.CTkFrame(controls_frame)
        right_frame.pack(side="right", fill="y", padx=(5, 10), pady=10)
        
        # Color preview
        preview_label = ctk.CTkLabel(right_frame, text="Preview", font=ctk.CTkFont(size=12, weight="bold"))
        preview_label.pack(pady=(10, 5))
        
        self.color_preview = ctk.CTkFrame(right_frame, width=80, height=80)
        self.color_preview.pack(pady=5)
        
        # Brightness slider
        brightness_label = ctk.CTkLabel(right_frame, text="Brightness", font=ctk.CTkFont(size=12, weight="bold"))
        brightness_label.pack(pady=(10, 5))
        
        self.brightness_slider = ctk.CTkSlider(
            right_frame,
            from_=0,
            to=100,
            number_of_steps=100,
            orientation="vertical",
            height=150,
            command=self._on_brightness_change
        )
        self.brightness_slider.pack(pady=5)
        self.brightness_slider.set(100)  # Start at full brightness
        
        # HSV values display
        self.hsv_labels = ctk.CTkFrame(right_frame)
        self.hsv_labels.pack(fill="x", pady=10)
        
        # H, S, V labels
        h_label = ctk.CTkLabel(self.hsv_labels, text="H:", width=20, anchor="w")
        h_label.pack(pady=2)
        self.h_value_label = ctk.CTkLabel(self.hsv_labels, text="0°", width=40, anchor="w")
        self.h_value_label.pack(pady=2)
        
        s_label = ctk.CTkLabel(self.hsv_labels, text="S:", width=20, anchor="w")
        s_label.pack(pady=2)
        self.s_value_label = ctk.CTkLabel(self.hsv_labels, text="100%", width=40, anchor="w")
        self.s_value_label.pack(pady=2)
        
        v_label = ctk.CTkLabel(self.hsv_labels, text="V:", width=20, anchor="w")
        v_label.pack(pady=2)
        self.v_value_label = ctk.CTkLabel(self.hsv_labels, text="100%", width=40, anchor="w")
        self.v_value_label.pack(pady=2)
        
        # RGB values display
        rgb_label = ctk.CTkLabel(right_frame, text="RGB", font=ctk.CTkFont(size=12, weight="bold"))
        rgb_label.pack(pady=(10, 5))
        
        self.rgb_labels = ctk.CTkFrame(right_frame)
        self.rgb_labels.pack(fill="x", pady=5)
        
        r_label = ctk.CTkLabel(self.rgb_labels, text="R:", width=20, anchor="w")
        r_label.pack(pady=2)
        self.r_value_label = ctk.CTkLabel(self.rgb_labels, text="255", width=40, anchor="w")
        self.r_value_label.pack(pady=2)
        
        g_label = ctk.CTkLabel(self.rgb_labels, text="G:", width=20, anchor="w")
        g_label.pack(pady=2)
        self.g_value_label = ctk.CTkLabel(self.rgb_labels, text="0", width=40, anchor="w")
        self.g_value_label.pack(pady=2)
        
        b_label = ctk.CTkLabel(self.rgb_labels, text="B:", width=20, anchor="w")
        b_label.pack(pady=2)
        self.b_value_label = ctk.CTkLabel(self.rgb_labels, text="0", width=40, anchor="w")
        self.b_value_label.pack(pady=2)
        
        # Action buttons
        button_frame = ctk.CTkFrame(right_frame)
        button_frame.pack(fill="x", pady=10)
        
        self.add_to_palette_btn = ctk.CTkButton(
            button_frame,
            text="Add to Palette",
            command=self._add_to_palette,
            height=30
        )
        self.add_to_palette_btn.pack(fill="x", pady=2)
        
        self.replace_color_btn = ctk.CTkButton(
            button_frame,
            text="Replace Color",
            command=self._replace_color,
            height=30
        )
        self.replace_color_btn.pack(fill="x", pady=2)
    
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
        angle = math.radians(self.hue)
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
    
    def _add_to_palette(self):
        """Add current color to palette"""
        rgb = self._hsv_to_rgb(self.hue, self.saturation, self.value)
        # This will be connected to the main palette system
        print(f"Adding color to palette: {rgb}")
    
    def _replace_color(self):
        """Replace selected palette color with current color"""
        rgb = self._hsv_to_rgb(self.hue, self.saturation, self.value)
        # This will be connected to the main palette system
        print(f"Replacing color in palette: {rgb}")
    
    def set_color(self, r: int, g: int, b: int):
        """Set color from RGB values"""
        self.hue, self.saturation, self.value = self._rgb_to_hsv(r, g, b)
        self.brightness_slider.set(self.value * 100)
        self._update_displays()
    
    def get_color(self) -> Tuple[int, int, int]:
        """Get current color as RGB"""
        return self._hsv_to_rgb(self.hue, self.saturation, self.value)