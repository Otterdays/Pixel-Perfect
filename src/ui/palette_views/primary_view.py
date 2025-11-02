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
        
        # Store the currently selected Primary color (separate from main palette)
        self.current_primary_color = None
        
        # Track the currently selected variation button for visual feedback
        self.selected_variation_button = None
        
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
        # Title frame - transparent background
        title_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(title_frame, text="Primary Colors", font=ctk.CTkFont(size=14, weight="bold"))
        title_label.pack(pady=5)
        
        # Primary colors grid - transparent background
        self.primary_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
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
        
        # Configure grid to center the columns
        for col in range(cols):
            self.primary_frame.grid_columnconfigure(col, weight=1)
    
    def _create_color_variations_grid(self):
        """Create color variations grid for selected primary color"""
        if not self.selected_primary_color:
            return
            
        # Back button frame - transparent background
        back_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
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
        
        # Variations grid - transparent background
        self.variations_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self.variations_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Generate color variations
        variations = self._generate_color_variations(self.selected_primary_color)
        
        # Clear button references
        self.variation_buttons.clear()
        
        # Clear selection reference to prevent "bad window path name" errors
        self.selected_variation_button = None
        
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
                    border_color="",
                    command=lambda c=color: self._select_color_variation(c)
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                
                # Store button reference with its color for hover effects
                self.variation_buttons.append({'button': btn, 'color': color})
                
                # Add hover effects
                btn.bind("<Enter>", lambda e, b=btn: self._on_variation_hover_enter(b))
                btn.bind("<Leave>", lambda e, b=btn: self._on_variation_hover_leave(b))
            
            # Configure grid to center the columns
            for col in range(cols):
                self.variations_frame.grid_columnconfigure(col, weight=1)
    
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
        # Store the selected color for get_current_color()
        self.current_primary_color = color
        self.mode = "variations"
        self.create()
    
    def _back_to_primary_colors(self):
        """Return to primary colors grid"""
        self.mode = "primary"
        self.selected_primary_color = None
        # Clear variation selection
        self.selected_variation_button = None
        self.create()
    
    def _on_variation_hover_enter(self, button):
        """Handle hover enter on variation button"""
        # Only add hover effects if button is not currently selected
        if button != self.selected_variation_button:
            button.configure(border_width=2, border_color="white")
            button.configure(width=32, height=32)
    
    def _on_variation_hover_leave(self, button):
        """Handle hover leave on variation button"""
        # Only remove hover effects if button is not currently selected
        if button != self.selected_variation_button:
            button.configure(border_width=0, border_color="")
            button.configure(width=30, height=30)
    
    def _select_color_variation(self, color):
        """Handle color variation selection"""
        # Primary palette colors should NOT be added to the main palette
        # Store the selected color in the Primary view instead
        self.current_primary_color = color
        
        # Clear previous selection visual feedback
        if self.selected_variation_button:
            try:
                # Check if button still exists before configuring
                self.selected_variation_button.winfo_exists()
                # Reset button to original size and remove border
                self.selected_variation_button.configure(width=30, height=30, border_width=0, border_color="")
            except:
                # Button was destroyed, clear the reference
                self.selected_variation_button = None
        
        # Find and highlight the selected variation button
        for variation_data in self.variation_buttons:
            if variation_data['color'] == color:
                self.selected_variation_button = variation_data['button']
                # Add selection highlight - make it more visible
                try:
                    # Method 1: Change button size to make it stand out
                    self.selected_variation_button.configure(width=35, height=35)
                    # Method 2: Add a thick white border
                    self.selected_variation_button.configure(border_width=4, border_color="white")
                except Exception as e:
                    pass  # Silently handle any configuration errors
                break
        
        # Note: Primary view does NOT call on_color_select to prevent auto-switching to brush
        # This prevents color bleeding to grid when just selecting colors
    
    def get_current_color(self):
        """Get the currently selected Primary color"""
        return self.current_primary_color
    
    def apply_theme(self, theme):
        """Apply theme to primary view"""
        # Primary color buttons maintain their actual colors
        pass

