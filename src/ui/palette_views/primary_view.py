"""
Primary Colors View for Pixel Perfect
Displays primary colors and their variations
"""

import customtkinter as ctk
import colorsys
from typing import Callable, List, Tuple, Optional


class PrimaryView:
    """Manages the primary colors view with variations"""
    
    def __init__(self, parent_frame: ctk.CTkFrame, palette, canvas,
                 on_color_select: Callable, on_tool_switch: Callable):
        """
        Initialize the primary colors view
        
        Args:
            parent_frame: Parent frame to pack widgets into
            palette: ColorPalette instance
            canvas: Canvas instance
            on_color_select: Callback when color is selected
            on_tool_switch: Callback to switch tools
        """
        self.parent_frame = parent_frame
        self.palette = palette
        self.canvas = canvas
        self.on_color_select = on_color_select
        self.on_tool_switch = on_tool_switch
        
        # UI components
        self.primary_frame = None
        self.variations_frame = None
        self.variation_buttons: List[dict] = []
        
        # State
        self.mode = "primary"  # "primary" or "variations"
        self.selected_primary_color = None
    
    def create(self):
        """Create the primary colors view"""
        # Clear existing widgets
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        if self.mode == "primary":
            self._create_primary_colors_grid()
        else:  # variations mode
            self._create_color_variations_grid()
    
    def _create_primary_colors_grid(self):
        """Create the main primary colors grid"""
        # Title frame
        title_frame = ctk.CTkFrame(self.parent_frame)
        title_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(title_frame, text="Primary Colors", font=ctk.CTkFont(size=14, weight="bold"))
        title_label.pack(pady=5)
        
        # Primary colors grid
        self.primary_frame = ctk.CTkFrame(self.parent_frame)
        self.primary_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Define primary colors (bright, vibrant colors)
        primary_colors = [
            ("Red", (255, 0, 0, 255)),
            ("Blue", (0, 0, 255, 255)),
            ("Green", (0, 255, 0, 255)),
            ("Yellow", (255, 255, 0, 255)),
            ("Orange", (255, 165, 0, 255)),
            ("Purple", (128, 0, 128, 255)),
            ("Cyan", (0, 255, 255, 255)),
            ("Pink", (255, 192, 203, 255)),
            ("Black", (0, 0, 0, 255)),
            ("White", (255, 255, 255, 255)),
            ("Brown", (139, 69, 19, 255)),
            ("Gray", (128, 128, 128, 255))
        ]
        
        cols = 3
        for i, (name, color) in enumerate(primary_colors):
            row = i // cols
            col = i % cols
            
            # Create primary color button
            btn = ctk.CTkButton(
                self.primary_frame,
                text=name,
                width=60,
                height=35,
                fg_color=f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}",
                text_color="white" if color[0] + color[1] + color[2] < 400 else "black",
                font=ctk.CTkFont(size=10, weight="bold"),
                command=lambda c=color: self._select_primary_color(c)
            )
            btn.grid(row=row, column=col, padx=3, pady=3)
    
    def _create_color_variations_grid(self):
        """Create color variations grid for selected primary color"""
        if not self.selected_primary_color:
            return
            
        # Back button frame
        back_frame = ctk.CTkFrame(self.parent_frame)
        back_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        back_btn = ctk.CTkButton(
            back_frame,
            text="✕ Back to Primary",
            width=120,
            height=30,
            command=self._back_to_primary_colors
        )
        back_btn.pack(pady=5)
        
        # Color name label
        color_name = self._get_color_name(self.selected_primary_color)
        title_label = ctk.CTkLabel(back_frame, text=f"{color_name} Variations", font=ctk.CTkFont(size=14, weight="bold"))
        title_label.pack(pady=(0, 5))
        
        # Variations grid
        self.variations_frame = ctk.CTkFrame(self.parent_frame)
        self.variations_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Generate color variations
        variations = self._generate_color_variations(self.selected_primary_color)
        
        # Clear button references
        self.variation_buttons.clear()
        
        # Only create buttons for actual color variations (no grey placeholders)
        if variations:
            cols = 4
            for i, color in enumerate(variations):
                row = i // cols
                col = i % cols
                
                # Create variation button with proper styling
                btn = ctk.CTkButton(
                    self.variations_frame,
                    text="",
                    width=30,
                    height=30,
                    fg_color=f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}",
                    hover_color=f"#{min(255, color[0] + 30):02x}{min(255, color[1] + 30):02x}{min(255, color[2] + 30):02x}",
                    border_width=0,
                    command=lambda c=color: self._select_color_variation(c)
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                
                # Store button reference with its color for hover effects
                self.variation_buttons.append({'button': btn, 'color': color})
                
                # Add hover effects
                btn.bind("<Enter>", lambda e, b=btn: self._on_variation_hover_enter(b))
                btn.bind("<Leave>", lambda e, b=btn: self._on_variation_hover_leave(b))
    
    def _get_color_name(self, color):
        """Get color name from RGB values"""
        r, g, b = color[0], color[1], color[2]
        
        if r > 200 and g < 100 and b < 100:
            return "Red"
        elif r < 100 and g < 100 and b > 200:
            return "Blue"
        elif r < 100 and g > 200 and b < 100:
            return "Green"
        elif r > 200 and g > 200 and b < 100:
            return "Yellow"
        elif r > 200 and g > 100 and b < 100:
            return "Orange"
        elif r > 100 and g < 100 and b > 100:
            return "Purple"
        elif r < 100 and g > 200 and b > 200:
            return "Cyan"
        elif r > 200 and g > 150 and b > 150:
            return "Pink"
        elif r < 50 and g < 50 and b < 50:
            return "Black"
        elif r > 200 and g > 200 and b > 200:
            return "White"
        elif r > 100 and g < 100 and b < 100:
            return "Brown"
        else:
            return "Gray"
    
    def _generate_color_variations(self, base_color):
        """Generate color variations for a primary color"""
        r, g, b, a = base_color
        variations = []
        seen_colors = set()
        
        # Helper function to add unique colors with minimum difference check
        def add_unique_color(color_tuple):
            # Check if color is significantly different from existing colors
            is_unique = True
            for existing_color in seen_colors:
                # Calculate color difference (simple RGB distance)
                diff = abs(color_tuple[0] - existing_color[0]) + abs(color_tuple[1] - existing_color[1]) + abs(color_tuple[2] - existing_color[2])
                if diff < 30:  # Minimum difference threshold
                    is_unique = False
                    break
            
            if is_unique:
                variations.append(color_tuple)
                seen_colors.add(color_tuple)
                return True
            return False
        
        # Add original color first
        add_unique_color((r, g, b, a))
        
        # Generate lighter variations (tints)
        for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
            new_r = min(255, int(r + (255 - r) * i))
            new_g = min(255, int(g + (255 - g) * i))
            new_b = min(255, int(b + (255 - b) * i))
            add_unique_color((new_r, new_g, new_b, a))
        
        # Generate darker variations (shades)
        for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
            new_r = max(0, int(r * (1 - i)))
            new_g = max(0, int(g * (1 - i)))
            new_b = max(0, int(b * (1 - i)))
            add_unique_color((new_r, new_g, new_b, a))
        
        # Generate saturation variations (more/less saturated versions)
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        
        # More saturated versions
        for sat_mult in [1.2, 1.4, 1.6]:
            new_s = min(1.0, s * sat_mult)
            new_r, new_g, new_b = colorsys.hsv_to_rgb(h, new_s, v)
            new_r = max(0, min(255, int(new_r * 255)))
            new_g = max(0, min(255, int(new_g * 255)))
            new_b = max(0, min(255, int(new_b * 255)))
            add_unique_color((new_r, new_g, new_b, a))
        
        # Less saturated versions (more grayish)
        for sat_mult in [0.8, 0.6, 0.4]:
            new_s = max(0.0, s * sat_mult)
            new_r, new_g, new_b = colorsys.hsv_to_rgb(h, new_s, v)
            new_r = max(0, min(255, int(new_r * 255)))
            new_g = max(0, min(255, int(new_g * 255)))
            new_b = max(0, min(255, int(new_b * 255)))
            add_unique_color((new_r, new_g, new_b, a))
        
        # Generate brightness variations (same hue and saturation, different brightness)
        for bright_mult in [0.8, 0.6, 0.4, 1.2, 1.4]:
            new_v = max(0.0, min(1.0, v * bright_mult))
            new_r, new_g, new_b = colorsys.hsv_to_rgb(h, s, new_v)
            new_r = max(0, min(255, int(new_r * 255)))
            new_g = max(0, min(255, int(new_g * 255)))
            new_b = max(0, min(255, int(new_b * 255)))
            add_unique_color((new_r, new_g, new_b, a))
        
        # Return only the unique variations we generated (no padding with blank spots)
        return variations
    
    def _select_primary_color(self, color):
        """Handle primary color selection"""
        self.selected_primary_color = color
        self.mode = "variations"
        self.create()
    
    def _back_to_primary_colors(self):
        """Return to primary colors grid"""
        self.mode = "primary"
        self.selected_primary_color = None
        self.create()
    
    def _on_variation_hover_enter(self, button):
        """Handle hover enter on variation button"""
        # Find the button data to check if it's selected
        button_data = None
        for btn_data in self.variation_buttons:
            if btn_data['button'] == button:
                button_data = btn_data
                break
        
        # Only add hover effects if button is not currently selected
        if button_data is not None:
            btn_color = button_data['color']
            # Check if this color is currently selected
            current_color = self.palette.get_primary_color()
            if not (btn_color[0] == current_color[0] and btn_color[1] == current_color[1] and btn_color[2] == current_color[2]):
                button.configure(border_width=2, border_color="white")
                button.configure(width=32, height=32)
    
    def _on_variation_hover_leave(self, button):
        """Handle hover leave on variation button"""
        # Find the button data to check if it's selected
        button_data = None
        for btn_data in self.variation_buttons:
            if btn_data['button'] == button:
                button_data = btn_data
                break
        
        # Only remove hover effects if button is not selected
        if button_data is not None:
            btn_color = button_data['color']
            # Check if this color is currently selected
            current_color = self.palette.get_primary_color()
            if not (btn_color[0] == current_color[0] and btn_color[1] == current_color[1] and btn_color[2] == current_color[2]):
                button.configure(border_width=0, border_color="")
                button.configure(width=30, height=30)
    
    def _select_color_variation(self, color):
        """Handle color variation selection"""
        # Set this color as the primary color in the palette
        self.palette.set_primary_color_by_rgba(color)
        
        # Update canvas color
        self.canvas.current_color = color
        
        # Notify parent
        if self.on_color_select:
            self.on_color_select(color)
        
        # Auto-switch to brush tool
        if self.on_tool_switch:
            self.on_tool_switch("brush")
    
    def apply_theme(self, theme):
        """Apply theme to primary view"""
        # Primary color buttons maintain their actual colors
        pass

