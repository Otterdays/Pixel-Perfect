"""
Main application window for Pixel Perfect
Coordinates all UI components and handles events
"""

import pygame
import customtkinter as ctk
from typing import Optional, Tuple
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.canvas import Canvas, CanvasSize
from core.color_palette import ColorPalette
from tools.brush import BrushTool
from tools.eraser import EraserTool
from tools.fill import FillTool
from tools.eyedropper import EyedropperTool
from tools.selection import SelectionTool, MoveTool
from tools.shapes import LineTool, RectangleTool, CircleTool
from core.layer_manager import LayerManager
from core.undo_manager import UndoManager, UndoState
from ui.layer_panel import LayerPanel
from animation.timeline import AnimationTimeline
from ui.timeline_panel import TimelinePanel

class MainWindow:
    """Main application window"""
    
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Set up CustomTkinter theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Pixel Perfect - Retro Pixel Art Editor")
        self.root.geometry("1200x800")
        
        # Initialize core systems
        self.canvas = Canvas(32, 32, zoom=16)  # Higher zoom for better grid visibility
        self.palette = ColorPalette()
        self.layer_manager = LayerManager(32, 32)
        self.undo_manager = UndoManager()
        self.timeline = AnimationTimeline(32, 32)
        
        # Initialize project and export managers
        from src.core.project import ProjectManager
        from src.utils.export import ExportManager
        self.project = ProjectManager()
        self.export_manager = ExportManager()
        
        # Initialize presets
        from src.utils.presets import PresetManager
        self.presets = PresetManager()
        
        # Initialize tools
        self.tools = {
            "brush": BrushTool(),
            "eraser": EraserTool(),
            "fill": FillTool(),
            "eyedropper": EyedropperTool(),
            "selection": SelectionTool(),
            "move": MoveTool(),
            "line": LineTool(),
            "rectangle": RectangleTool(),
            "circle": CircleTool()
        }
        self.current_tool = "brush"
        
        # Connect selection and move tools
        self.tools["move"].set_selection_tool(self.tools["selection"])
        
        # UI state
        self.is_drawing = False
        self.last_mouse_pos = (0, 0)
        self._last_drawn_pixel = None  # Track last drawn pixel for efficient updates
        self._updating_display = False  # Flag to prevent recursion
        
        # Create UI
        self._create_ui()
        
        # Bind events
        self._bind_events()
        
        # Initialize canvas integration
        self._sync_canvas_with_layers()
    
    def _create_ui(self):
        """Create the user interface"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top toolbar
        self._create_toolbar()
        
        # Main content area
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Left panel (tools and palette) - with scrollbar
        self.left_panel = ctk.CTkScrollableFrame(self.content_frame, width=250)
        self.left_panel.pack(side="left", fill="both", padx=(0, 10))
        
        # Canvas area
        self.canvas_frame = ctk.CTkFrame(self.content_frame)
        self.canvas_frame.pack(side="left", fill="both", expand=True)
        
        # Right panel (layers, etc.) - with scrollbar
        self.right_panel = ctk.CTkScrollableFrame(self.content_frame, width=250)
        self.right_panel.pack(side="right", fill="both", padx=(10, 0))
        
        # Create panels
        self._create_tool_panel()
        self._create_palette_panel()
        self._create_canvas_panel()
        self._create_layer_panel()
        
        # Initialize layer panel
        self.layer_panel = LayerPanel(self.right_panel, self.layer_manager)
        self.layer_panel.on_layer_changed = self._on_layer_changed
        
        # Initialize timeline panel
        self.timeline_panel = TimelinePanel(self.right_panel, self.timeline)
        self.timeline_panel.on_frame_changed = self._on_frame_changed
    
    def _create_toolbar(self):
        """Create top toolbar"""
        self.toolbar = ctk.CTkFrame(self.main_frame)
        self.toolbar.pack(fill="x", pady=(0, 10))
        
        # File menu
        self.file_button = ctk.CTkButton(self.toolbar, text="File", width=60, command=self._show_file_menu)
        self.file_button.pack(side="left", padx=5)
        
        # Canvas size selector
        self.size_label = ctk.CTkLabel(self.toolbar, text="Size:")
        self.size_label.pack(side="left", padx=(20, 5))
        
        self.size_var = ctk.StringVar(value="32x32")
        self.size_menu = ctk.CTkOptionMenu(
            self.toolbar, 
            variable=self.size_var,
            values=["16x16", "32x32", "16x32", "32x64"],
            command=self._on_size_change
        )
        self.size_menu.pack(side="left", padx=5)
        
        # Zoom controls
        self.zoom_label = ctk.CTkLabel(self.toolbar, text="Zoom:")
        self.zoom_label.pack(side="left", padx=(20, 5))
        
        self.zoom_var = ctk.StringVar(value="16x")
        self.zoom_menu = ctk.CTkOptionMenu(
            self.toolbar,
            variable=self.zoom_var,
            values=["0.25x", "0.5x", "1x", "2x", "4x", "8x", "16x", "32x"],
            command=self._on_zoom_change
        )
        self.zoom_menu.pack(side="left", padx=5)
        
        # Undo/Redo buttons
        self._create_undo_redo_buttons()
        
        # Grid toggle
        self.grid_button = ctk.CTkButton(self.toolbar, text="Grid", width=60)
        self.grid_button.pack(side="right", padx=5)
        self.grid_button.configure(command=self._toggle_grid)
        self._update_grid_button_text()
    
    def _create_undo_redo_buttons(self):
        """Create stylized undo/redo buttons with arrows"""
        # Undo/Redo button frame
        undo_redo_frame = ctk.CTkFrame(self.toolbar)
        undo_redo_frame.pack(side="left", padx=(20, 0))
        
        # Undo button with left arrow
        self.undo_button = ctk.CTkButton(
            undo_redo_frame,
            text="↶",  # Left curved arrow
            width=40,
            height=30,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self._undo,
            fg_color=("gray75", "gray25")
        )
        self.undo_button.pack(side="left", padx=2)
        
        # Redo button with right arrow
        self.redo_button = ctk.CTkButton(
            undo_redo_frame,
            text="↷",  # Right curved arrow
            width=40,
            height=30,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self._redo,
            fg_color=("gray75", "gray25")
        )
        self.redo_button.pack(side="left", padx=2)
        
        # Connect undo manager callback
        self.undo_manager.on_state_changed = self._update_undo_redo_buttons
    
    def _update_undo_redo_buttons(self):
        """Update undo/redo button states"""
        if hasattr(self, 'undo_button') and hasattr(self, 'redo_button'):
            # Update button colors based on availability
            if self.undo_manager.can_undo():
                self.undo_button.configure(fg_color=("blue", "blue"))
            else:
                self.undo_button.configure(fg_color=("gray75", "gray25"))
            
            if self.undo_manager.can_redo():
                self.redo_button.configure(fg_color=("blue", "blue"))
            else:
                self.redo_button.configure(fg_color=("gray75", "gray25"))
    
    def _create_tool_panel(self):
        """Create tool selection panel"""
        self.tool_frame = ctk.CTkFrame(self.left_panel)
        self.tool_frame.pack(fill="x", padx=10, pady=10)
        
        tool_label = ctk.CTkLabel(self.tool_frame, text="Tools", font=ctk.CTkFont(size=16, weight="bold"))
        tool_label.pack(pady=(10, 5))
        
        # Tool buttons
        self.tool_buttons = {}
        tools = [
            ("brush", "Brush"),
            ("eraser", "Eraser"),
            ("fill", "Fill"),
            ("eyedropper", "Eyedropper"),
            ("selection", "Select"),
            ("move", "Move"),
            ("line", "Line"),
            ("rectangle", "Rect"),
            ("circle", "Circle")
        ]
        
        for tool_id, tool_name in tools:
            btn = ctk.CTkButton(
                self.tool_frame,
                text=tool_name,
                width=100,
                command=lambda t=tool_id: self._select_tool(t)
            )
            btn.pack(pady=2)
            self.tool_buttons[tool_id] = btn
        
        # Highlight current tool
        self._update_tool_selection()
    
    def _create_palette_panel(self):
        """Create color palette panel"""
        self.palette_frame = ctk.CTkFrame(self.left_panel)
        self.palette_frame.pack(fill="x", padx=10, pady=10)
        
        palette_label = ctk.CTkLabel(self.palette_frame, text="Palette", font=ctk.CTkFont(size=16, weight="bold"))
        palette_label.pack(pady=(10, 5))
        
        # Palette selector
        self.palette_var = ctk.StringVar(value="SNES Classic")
        self.palette_menu = ctk.CTkOptionMenu(
            self.palette_frame,
            variable=self.palette_var,
            values=list(self.palette.get_preset_palettes().keys()),
            command=self._on_palette_change
        )
        self.palette_menu.pack(pady=5)
        
        # View mode selector
        view_mode_frame = ctk.CTkFrame(self.palette_frame)
        view_mode_frame.pack(fill="x", padx=10, pady=5)
        
        self.view_mode_var = ctk.StringVar(value="grid")
        
        # Create a grid layout for radio buttons to ensure they all fit
        self.grid_view_btn = ctk.CTkRadioButton(
            view_mode_frame,
            text="Grid",
            variable=self.view_mode_var,
            value="grid",
            command=self._on_view_mode_change
        )
        self.grid_view_btn.grid(row=0, column=0, padx=2, pady=2, sticky="w")
        
        self.primary_view_btn = ctk.CTkRadioButton(
            view_mode_frame,
            text="Primary",
            variable=self.view_mode_var,
            value="primary",
            command=self._on_view_mode_change
        )
        self.primary_view_btn.grid(row=0, column=1, padx=2, pady=2, sticky="w")
        
        self.wheel_view_btn = ctk.CTkRadioButton(
            view_mode_frame,
            text="Wheel",
            variable=self.view_mode_var,
            value="wheel",
            command=self._on_view_mode_change
        )
        self.wheel_view_btn.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky="w")
        
        # Color display container
        self.color_display_frame = ctk.CTkFrame(self.palette_frame)
        self.color_display_frame.pack(fill="both", expand=True, pady=10)
        
        # Initialize with grid view
        self._create_color_grid()
        self.color_wheel = None
        
        # Primary colors state
        self.primary_colors_mode = "primary"  # "primary" or "variations"
        self.selected_primary_color = None
    
    def _create_color_grid(self):
        """Create color palette grid"""
        # Clear existing widgets
        for widget in self.color_display_frame.winfo_children():
            widget.destroy()
        
        # Create grid frame
        self.color_frame = ctk.CTkFrame(self.color_display_frame)
        self.color_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Store color button references for easy updating
        if not hasattr(self, 'color_buttons'):
            self.color_buttons = []
        else:
            self.color_buttons.clear()
        
        colors = self.palette.colors
        cols = 4
        rows = (len(colors) + cols - 1) // cols
        
        for i, color in enumerate(colors):
            row = i // cols
            col = i % cols
            
            # Create color button with hover effects
            btn = ctk.CTkButton(
                self.color_frame,
                text="",
                width=30,
                height=30,
                fg_color=f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}",
                hover_color=f"#{min(255, color[0] + 30):02x}{min(255, color[1] + 30):02x}{min(255, color[2] + 30):02x}",
                border_width=0,
                command=lambda idx=i: self._select_color(idx)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            
            # Store button reference
            self.color_buttons.append(btn)
            
            # Add hover effects
            btn.bind("<Enter>", lambda e, b=btn: self._on_color_hover_enter(b))
            btn.bind("<Leave>", lambda e, b=btn: self._on_color_hover_leave(b))
            
            # Highlight primary/secondary colors
            if i == self.palette.primary_color:
                btn.configure(border_width=3, border_color="white")
            elif i == self.palette.secondary_color:
                btn.configure(border_width=2, border_color="gray")
    
    def _create_primary_colors(self):
        """Create primary colors view with variations"""
        # Clear existing widgets
        for widget in self.color_display_frame.winfo_children():
            widget.destroy()
        
        if self.primary_colors_mode == "primary":
            self._create_primary_colors_grid()
        else:  # variations mode
            self._create_color_variations_grid()
    
    def _create_primary_colors_grid(self):
        """Create the main primary colors grid"""
        # Title frame
        title_frame = ctk.CTkFrame(self.color_display_frame)
        title_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(title_frame, text="Primary Colors", font=ctk.CTkFont(size=14, weight="bold"))
        title_label.pack(pady=5)
        
        # Primary colors grid
        self.primary_frame = ctk.CTkFrame(self.color_display_frame)
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
        back_frame = ctk.CTkFrame(self.color_display_frame)
        back_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        back_btn = ctk.CTkButton(
            back_frame,
            text="✕ Back to Primary",
            width=120,
            height=30,
            fg_color="gray",
            command=self._back_to_primary_colors
        )
        back_btn.pack(pady=5)
        
        # Color name label
        color_name = self._get_color_name(self.selected_primary_color)
        title_label = ctk.CTkLabel(back_frame, text=f"{color_name} Variations", font=ctk.CTkFont(size=14, weight="bold"))
        title_label.pack(pady=(0, 5))
        
        # Variations grid
        self.variations_frame = ctk.CTkFrame(self.color_display_frame)
        self.variations_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Generate color variations
        variations = self._generate_color_variations(self.selected_primary_color)
        
        # Store buttons for hover effects
        if not hasattr(self, 'variation_buttons'):
            self.variation_buttons = []
        else:
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
        import colorsys
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
        self.primary_colors_mode = "variations"
        self._create_primary_colors()
    
    def _back_to_primary_colors(self):
        """Return to primary colors grid"""
        self.primary_colors_mode = "primary"
        self.selected_primary_color = None
        self._create_primary_colors()
    
    def _on_variation_hover_enter(self, button):
        """Handle hover enter on variation button"""
        # Find the button data to check if it's selected
        button_data = None
        if hasattr(self, 'variation_buttons'):
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
        if hasattr(self, 'variation_buttons'):
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
        
        # Update current tool color
        if hasattr(self, 'current_tool') and self.current_tool:
            if hasattr(self.current_tool, 'color'):
                self.current_tool.color = color
        
        # Highlight the selected variation button
        self._highlight_selected_variation(color)
        
        # Update pixel display
        self._update_pixel_display()
        
        print(f"Selected color variation: {color}")
    
    def _highlight_selected_variation(self, selected_color):
        """Highlight the selected variation button"""
        if hasattr(self, 'variation_buttons'):
            # First, remove all highlights
            for btn_data in self.variation_buttons:
                btn = btn_data['button']
                btn.configure(border_width=0, border_color="")
                btn.configure(width=30, height=30)
            
            # Find and highlight the selected button using stored color data
            for btn_data in self.variation_buttons:
                btn = btn_data['button']
                btn_color = btn_data['color']
                # Direct color comparison using stored color data
                if (btn_color[0] == selected_color[0] and 
                    btn_color[1] == selected_color[1] and 
                    btn_color[2] == selected_color[2]):
                    # Highlight this button
                    btn.configure(border_width=3, border_color="white")
                    break

    def _create_canvas_panel(self):
        """Create canvas display panel"""
        canvas_label = ctk.CTkLabel(self.canvas_frame, text="Canvas", font=ctk.CTkFont(size=16, weight="bold"))
        canvas_label.pack(pady=10)

        # Canvas container
        self.canvas_container = ctk.CTkFrame(self.canvas_frame)
        self.canvas_container.pack(expand=True, fill="both", padx=20, pady=20)

        # Create tkinter Canvas for drawing (much simpler than pygame integration)
        self.drawing_canvas = ctk.CTkCanvas(
            self.canvas_container,
            bg="lightgray",
            highlightthickness=1,
            highlightbackground="black"
        )
        self.drawing_canvas.pack(expand=True, fill="both")

        # Bind mouse events to the tkinter canvas
        self.drawing_canvas.bind("<Button-1>", self._on_tkinter_canvas_mouse_down)
        self.drawing_canvas.bind("<ButtonRelease-1>", self._on_tkinter_canvas_mouse_up)
        self.drawing_canvas.bind("<B1-Motion>", self._on_tkinter_canvas_mouse_drag)
        self.drawing_canvas.bind("<Motion>", self._on_tkinter_canvas_mouse_move)

        # Initialize the drawing surface
        self._init_drawing_surface()
    
    def _create_layer_panel(self):
        """Create layer management panel"""
        # Layer panel is now created by LayerPanel class
        pass
    
    def _init_drawing_surface(self):
        """Initialize the tkinter drawing surface"""
        # Schedule initial draw after window is fully loaded
        self.root.after(100, self._initial_draw)

    def _initial_draw(self):
        """Do the initial drawing of the canvas"""
        try:
            # Get canvas size
            self.drawing_canvas.update_idletasks()
            width = self.drawing_canvas.winfo_width()
            height = self.drawing_canvas.winfo_height()

            print(f"Initial draw - Canvas size: {width}x{height}")  # Debug
            
            if width > 1 and height > 1:
                # Set canvas size to match our pixel grid
                canvas_pixel_width = self.canvas.width * self.canvas.zoom
                canvas_pixel_height = self.canvas.height * self.canvas.zoom

                print(f"Pixel canvas size: {canvas_pixel_width}x{canvas_pixel_height}")  # Debug

                # Center the canvas in the available space
                x_offset = (width - canvas_pixel_width) // 2
                y_offset = (height - canvas_pixel_height) // 2

                print(f"Offsets: {x_offset}, {y_offset}")  # Debug

                # Clear canvas
                self.drawing_canvas.delete("all")

                # Draw grid if enabled
                if self.canvas.show_grid:
                    print("Drawing grid...")  # Debug
                    self._draw_tkinter_grid(x_offset, y_offset, canvas_pixel_width, canvas_pixel_height)

                # Draw a border around the canvas area
                self.drawing_canvas.create_rectangle(
                    x_offset, y_offset,
                    x_offset + canvas_pixel_width, y_offset + canvas_pixel_height,
                    outline="black", width=2
                )

                # Draw any existing pixels
                self._draw_all_pixels_on_tkinter(x_offset, y_offset)
                
                print("Initial draw complete!")  # Debug
            else:
                print(f"Canvas not ready yet: {width}x{height}, retrying...")
                # Try again in a moment
                self.root.after(200, self._initial_draw)
        except Exception as e:
            print(f"Error in initial draw: {e}")
            import traceback
            traceback.print_exc()

    def _draw_tkinter_grid(self, x_offset, y_offset, canvas_width, canvas_height):
        """Draw grid lines on tkinter canvas"""
        grid_color = "#666666"  # Dark gray

        # Draw vertical lines
        for x in range(0, self.canvas.width + 1):
            screen_x = x_offset + (x * self.canvas.zoom)
            self.drawing_canvas.create_line(
                screen_x, y_offset,
                screen_x, y_offset + canvas_height,
                fill=grid_color, width=1
            )

        # Draw horizontal lines
        for y in range(0, self.canvas.height + 1):
            screen_y = y_offset + (y * self.canvas.zoom)
            self.drawing_canvas.create_line(
                x_offset, screen_y,
                x_offset + canvas_width, screen_y,
                fill=grid_color, width=1
            )


    def _draw_all_pixels_on_tkinter(self, x_offset, y_offset):
        """Draw all pixels from canvas onto tkinter canvas"""
        # Draw each pixel as a rectangle on the tkinter canvas
        for y in range(self.canvas.height):
            for x in range(self.canvas.width):
                pixel_color = self.canvas.get_pixel(x, y)
                if pixel_color[3] > 0:  # Only draw non-transparent pixels
                    screen_x = x_offset + (x * self.canvas.zoom)
                    screen_y = y_offset + (y * self.canvas.zoom)

                    # Convert RGBA to hex color for tkinter
                    r, g, b, a = pixel_color
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"

                    # Draw pixel as rectangle with "pixels" tag
                    self.drawing_canvas.create_rectangle(
                        screen_x, screen_y,
                        screen_x + self.canvas.zoom, screen_y + self.canvas.zoom,
                        fill=hex_color, outline="", tags="pixels"
                    )
    
    def _bind_events(self):
        """Bind keyboard and mouse events"""
        self.root.bind("<Key>", self._on_key_press)
        self.root.focus_set()
        
        # Bind window resize event to fix grid centering
        self.root.bind("<Configure>", self._on_window_resize)
        
        # Mouse events are now bound to the tkinter drawing canvas
    
    def _on_window_resize(self, event):
        """Handle window resize events to maintain grid centering"""
        # Only handle main window resize, not child widget events
        if event.widget == self.root:
            # Schedule a delayed redraw to avoid excessive updates during resize
            if hasattr(self, '_resize_timer'):
                self.root.after_cancel(self._resize_timer)
            
            self._resize_timer = self.root.after(100, self._redraw_canvas_after_resize)
    
    def _redraw_canvas_after_resize(self):
        """Redraw canvas after window resize to maintain grid centering"""
        try:
            if hasattr(self, 'drawing_canvas') and self.drawing_canvas:
                # Force a complete redraw of the canvas
                self._initial_draw()
        except Exception as e:
            print(f"Error redrawing canvas after resize: {e}")
    
    def _on_key_press(self, event):
        """Handle keyboard shortcuts"""
        key = event.keysym.lower()
        
        # Tool shortcuts
        if key == 'b':
            self._select_tool("brush")
        elif key == 'e':
            self._select_tool("eraser")
        elif key == 'f':
            self._select_tool("fill")
        elif key == 'i':
            self._select_tool("eyedropper")
        elif key == 's':
            self._select_tool("selection")
        elif key == 'm':
            self._select_tool("move")
        elif key == 'l':
            self._select_tool("line")
        elif key == 'r':
            self._select_tool("rectangle")
        elif key == 'c':
            self._select_tool("circle")
        
        # Undo/Redo shortcuts
        elif key == 'z' and event.state & 0x4:  # Ctrl+Z
            self._undo()
        elif (key == 'y' and event.state & 0x4) or (key == 'z' and event.state & 0x6):  # Ctrl+Y or Ctrl+Shift+Z
            self._redo()
        
        # Canvas shortcuts
        elif key == 'g':
            self._toggle_grid()
        
        # Undo/redo shortcuts
        elif event.state & 0x4 and key == 'z':  # Ctrl+Z
            self._undo()
        elif event.state & 0x4 and key == 'y':  # Ctrl+Y
            self._redo()
        
        # Layer shortcuts
        elif event.state & 0x4 and key == 'n':  # Ctrl+N (new layer)
            self._add_layer()
        
        # Animation shortcuts
        elif key == 'space':
            self._toggle_animation()
        elif key == 'comma':  # < key
            self._previous_frame()
        elif key == 'period':  # > key
            self._next_frame()
    
    def _select_tool(self, tool_id: str):
        """Select a drawing tool"""
        self.current_tool = tool_id
        self._update_tool_selection()
    
    def _update_tool_selection(self):
        """Update tool button appearance"""
        for tool_id, btn in self.tool_buttons.items():
            if tool_id == self.current_tool:
                btn.configure(fg_color="blue")
            else:
                btn.configure(fg_color="gray")
    
    def _on_color_hover_enter(self, button):
        """Handle hover enter on color button"""
        # Find the button index to check if it's selected
        button_index = None
        if hasattr(self, 'color_buttons'):
            for i, btn in enumerate(self.color_buttons):
                if btn == button:
                    button_index = i
                    break
        
        # Only add hover effects if button is not currently selected
        if button_index is not None:
            if button_index != self.palette.primary_color and button_index != self.palette.secondary_color:
                button.configure(border_width=2, border_color="white")
                button.configure(width=32, height=32)
    
    def _on_color_hover_leave(self, button):
        """Handle hover leave on color button"""
        # Find the button index to check if it's selected
        button_index = None
        if hasattr(self, 'color_buttons'):
            for i, btn in enumerate(self.color_buttons):
                if btn == button:
                    button_index = i
                    break
        
        # Only remove hover effects if button is not selected
        if button_index is not None:
            if button_index != self.palette.primary_color and button_index != self.palette.secondary_color:
                button.configure(border_width=0, border_color="")
                button.configure(width=30, height=30)
    
    def _select_color(self, color_index: int):
        """Select a color from the palette"""
        self.palette.set_primary_color(color_index)
        
        # Update the color grid to show new selection
        if hasattr(self, 'color_frame'):
            self._update_color_grid_selection()
    
    def _update_color_grid_selection(self):
        """Update color grid selection without recreating the grid"""
        if hasattr(self, 'color_buttons'):
            # Update all button borders based on current selection
            for i, btn in enumerate(self.color_buttons):
                if i == self.palette.primary_color:
                    btn.configure(border_width=3, border_color="white")
                elif i == self.palette.secondary_color:
                    btn.configure(border_width=2, border_color="gray")
                else:
                    btn.configure(border_width=0, border_color="")
    
    def _on_size_change(self, size_str: str):
        """Handle canvas size change"""
        size_map = {
            "16x16": CanvasSize.SMALL,
            "32x32": CanvasSize.MEDIUM,
            "16x32": CanvasSize.WIDE,
            "32x64": CanvasSize.LARGE
        }
        
        if size_str in size_map:
            self.canvas.set_preset_size(size_map[size_str])
            # Update display immediately
            self._force_tkinter_canvas_update()
    
    def _on_zoom_change(self, zoom_str: str):
        """Handle zoom level change"""
        zoom_map = {
            "0.25x": 0.25, "0.5x": 0.5, "1x": 1, "2x": 2, "4x": 4, "8x": 8, "16x": 16, "32x": 32
        }
        
        if zoom_str in zoom_map:
            self.canvas.set_zoom(zoom_map[zoom_str])
            # Update display immediately
            self._force_tkinter_canvas_update()
    
    def _on_palette_change(self, palette_name: str):
        """Handle palette change"""
        self.palette.load_preset(palette_name)
        if self.view_mode_var.get() == "grid":
            self._create_color_grid()
        else:
            self._create_color_wheel()
    
    def _on_view_mode_change(self):
        """Handle view mode change between grid, primary colors, and color wheel"""
        mode = self.view_mode_var.get()
        if mode == "grid":
            self._create_color_grid()
        elif mode == "primary":
            self._create_primary_colors()
        else:  # wheel
            self._create_color_wheel()
    
    def _create_color_wheel(self):
        """Create color wheel view"""
        # Clear existing widgets
        for widget in self.color_display_frame.winfo_children():
            widget.destroy()
        
        # Import and create color wheel
        from src.ui.color_wheel import ColorWheel
        self.color_wheel = ColorWheel(self.color_display_frame)
        self.color_wheel.on_color_changed = self._on_color_wheel_changed
        
        # Connect color wheel buttons to palette management
        self.color_wheel._add_to_palette = self._add_color_to_palette
        self.color_wheel._replace_color = self._replace_color_in_palette
    
    def _on_color_wheel_changed(self, rgb_color):
        """Handle color wheel color change - now just for UI updates"""
        # Update color display in UI
        self._update_pixel_display()
        print(f"Color wheel color changed: {rgb_color}")
    
    def _add_color_to_palette(self):
        """Add current color wheel color to palette"""
        if self.color_wheel and len(self.palette.colors) < 16:
            rgb_color = self.color_wheel.get_color()
            # Convert to RGBA format
            rgba_color = (rgb_color[0], rgb_color[1], rgb_color[2], 255)
            self.palette.add_color(rgba_color)
            
            # Update display if in grid mode
            if self.view_mode_var.get() == "grid":
                self._create_color_grid()
    
    def _replace_color_in_palette(self):
        """Replace selected palette color with color wheel color"""
        if self.color_wheel:
            rgb_color = self.color_wheel.get_color()
            rgba_color = (rgb_color[0], rgb_color[1], rgb_color[2], 255)
            
            # Replace primary color
            if self.palette.primary_color < len(self.palette.colors):
                self.palette.set_color(self.palette.primary_color, rgba_color)
                
                # Update display if in grid mode
                if self.view_mode_var.get() == "grid":
                    self._create_color_grid()
    
    def _toggle_grid(self):
        """Toggle grid visibility"""
        self.canvas.toggle_grid()
        self._update_grid_button_text()
        self._force_tkinter_canvas_update()

    def _update_grid_button_text(self):
        """Update grid button text to show current state"""
        if self.canvas.show_grid:
            self.grid_button.configure(text="Grid: ON")
            self.grid_button.configure(fg_color="green")
        else:
            self.grid_button.configure(text="Grid: OFF")
            self.grid_button.configure(fg_color="red")
    
    def _show_file_menu(self):
        """Show file menu options"""
        # Create a popup menu
        file_menu = ctk.CTkToplevel(self.root)
        file_menu.title("File Menu")
        file_menu.geometry("200x300")
        file_menu.transient(self.root)
        file_menu.grab_set()
        
        # Center the menu
        file_menu.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Menu options
        new_btn = ctk.CTkButton(file_menu, text="New Project", command=lambda: [self._new_project(), file_menu.destroy()])
        new_btn.pack(pady=5, padx=10, fill="x")
        
        open_btn = ctk.CTkButton(file_menu, text="Open Project", command=lambda: [self._open_project(), file_menu.destroy()])
        open_btn.pack(pady=5, padx=10, fill="x")
        
        save_btn = ctk.CTkButton(file_menu, text="Save Project", command=lambda: [self._save_project(), file_menu.destroy()])
        save_btn.pack(pady=5, padx=10, fill="x")
        
        save_as_btn = ctk.CTkButton(file_menu, text="Save As...", command=lambda: [self._save_project_as(), file_menu.destroy()])
        save_as_btn.pack(pady=5, padx=10, fill="x")
        
        # Separator
        sep = ctk.CTkFrame(file_menu, height=2)
        sep.pack(fill="x", padx=10, pady=10)
        
        # Export options
        export_png_btn = ctk.CTkButton(file_menu, text="Export as PNG", command=lambda: [self._export_png(), file_menu.destroy()])
        export_png_btn.pack(pady=5, padx=10, fill="x")
        
        export_gif_btn = ctk.CTkButton(file_menu, text="Export as GIF", command=lambda: [self._export_gif(), file_menu.destroy()])
        export_gif_btn.pack(pady=5, padx=10, fill="x")
        
        export_spritesheet_btn = ctk.CTkButton(file_menu, text="Export Sprite Sheet", command=lambda: [self._export_spritesheet(), file_menu.destroy()])
        export_spritesheet_btn.pack(pady=5, padx=10, fill="x")
        
        # Separator
        sep2 = ctk.CTkFrame(file_menu, height=2)
        sep2.pack(fill="x", padx=10, pady=10)
        
        # Templates
        template_btn = ctk.CTkButton(file_menu, text="Load Template", command=lambda: [self._show_templates(), file_menu.destroy()])
        template_btn.pack(pady=5, padx=10, fill="x")
        
        # Close button
        close_btn = ctk.CTkButton(file_menu, text="Close", command=file_menu.destroy)
        close_btn.pack(pady=10, padx=10, fill="x")
    
    def _new_project(self):
        """Create a new project"""
        # Clear canvas
        self.canvas.clear()
        self._force_tkinter_canvas_update()
        
        # Reset layers
        self.layer_manager.clear_layers()
        self.layer_manager.add_layer("Background")
        
        # Reset timeline
        self.timeline.clear_frames()
        self.timeline.add_frame()
        
        print("New project created")
    
    def _open_project(self):
        """Open an existing project"""
        try:
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(
                title="Open Pixel Perfect Project",
                filetypes=[("Pixel Perfect Files", "*.pixpf"), ("All Files", "*.*")]
            )
            
            if file_path:
                self.project.load_project(file_path)
                # Update canvas with loaded data
                if hasattr(self.project, 'canvas_data'):
                    self.canvas.pixels = self.project.canvas_data
                    self._force_tkinter_canvas_update()
                print(f"Project opened: {file_path}")
        except Exception as e:
            print(f"Error opening project: {e}")
    
    def _save_project(self):
        """Save current project"""
        try:
            if self.project.current_project_path:
                self.project.save_project(
                    self.project.current_project_path,
                    self.canvas,
                    self.palette,
                    self.layer_manager,
                    self.timeline
                )
                print(f"Project saved: {self.project.current_project_path}")
            else:
                self._save_project_as()
        except Exception as e:
            print(f"Error saving project: {e}")
    
    def _save_project_as(self):
        """Save project with new name"""
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                title="Save Pixel Perfect Project",
                defaultextension=".pixpf",
                filetypes=[("Pixel Perfect Files", "*.pixpf"), ("All Files", "*.*")]
            )
            
            if file_path:
                self.project.save_project(
                    file_path,
                    self.canvas,
                    self.palette,
                    self.layer_manager,
                    self.timeline
                )
                self.project.current_project_path = file_path
                print(f"Project saved as: {file_path}")
        except Exception as e:
            print(f"Error saving project: {e}")
    
    def _export_png(self):
        """Export canvas as PNG"""
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                title="Export as PNG",
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
            )
            
            if file_path:
                # Export with high quality (8x scaling) and transparency
                success = self.export_manager.export_png(
                    self.canvas.pixels, 
                    file_path, 
                    scale=8, 
                    transparent=True
                )
                if success:
                    print(f"Exported high-quality PNG (8x scale): {file_path}")
                else:
                    print(f"Failed to export PNG: {file_path}")
        except Exception as e:
            print(f"Error exporting PNG: {e}")
    
    def _export_gif(self):
        """Export animation as GIF"""
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                title="Export as GIF",
                defaultextension=".gif",
                filetypes=[("GIF Files", "*.gif"), ("All Files", "*.*")]
            )
            
            if file_path:
                # Get frames from timeline
                frames = [frame.pixels for frame in self.timeline.frames]
                success = self.export_manager.export_gif(
                    frames, 
                    file_path, 
                    scale=8,
                    duration=100  # 100ms per frame for smooth animation
                )
                if success:
                    print(f"Exported high-quality animated GIF (8x scale): {file_path}")
                else:
                    print(f"Failed to export GIF: {file_path}")
        except Exception as e:
            print(f"Error exporting GIF: {e}")
    
    def _export_spritesheet(self):
        """Export as sprite sheet"""
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                title="Export Sprite Sheet",
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
            )
            
            if file_path:
                # Get frames from timeline for sprite sheet
                frames = [frame.pixels for frame in self.timeline.frames]
                success = self.export_manager.export_sprite_sheet(
                    frames, 
                    file_path, 
                    scale=8,
                    layout="horizontal"  # Default to horizontal layout
                )
                if success:
                    print(f"Exported high-quality sprite sheet (8x scale): {file_path}")
                else:
                    print(f"Failed to export sprite sheet: {file_path}")
        except Exception as e:
            print(f"Error exporting sprite sheet: {e}")
    
    def _show_templates(self):
        """Show template selection dialog"""
        template_menu = ctk.CTkToplevel(self.root)
        template_menu.title("Load Template")
        template_menu.geometry("300x400")
        template_menu.transient(self.root)
        template_menu.grab_set()
        
        # Center the menu
        template_menu.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))
        
        # Template categories
        categories = ["Characters", "Items", "Tiles", "UI Elements"]
        
        for category in categories:
            cat_frame = ctk.CTkFrame(template_menu)
            cat_frame.pack(fill="x", padx=10, pady=5)
            
            cat_label = ctk.CTkLabel(cat_frame, text=category, font=ctk.CTkFont(weight="bold"))
            cat_label.pack(pady=5)
            
            # Add template buttons for each category
            if category == "Characters":
                templates = ["32x32 Character (top-down)", "16x32 Character (side-view)"]
            elif category == "Items":
                templates = ["16x16 Item icon", "32x32 Item icon (detailed)"]
            elif category == "Tiles":
                templates = ["16x16 Grass tile", "16x16 Stone tile"]
            elif category == "UI Elements":
                templates = ["32x16 Button (UI)", "16x16 Icon (UI)"]
            
            for template in templates:
                btn = ctk.CTkButton(
                    cat_frame, 
                    text=template,
                    command=lambda t=template: [self._load_template(t), template_menu.destroy()]
                )
                btn.pack(pady=2, padx=5, fill="x")
        
        close_btn = ctk.CTkButton(template_menu, text="Close", command=template_menu.destroy)
        close_btn.pack(pady=10, padx=10, fill="x")
    
    def _load_template(self, template_name):
        """Load a template"""
        try:
            template_data = self.presets.get_template(template_name)
            if template_data:
                # Set canvas size based on template
                width, height = template_data.get('size', (32, 32))
                self.canvas.resize(width, height)
                
                # Load template pixels if available
                if 'pixels' in template_data:
                    self.canvas.pixels = template_data['pixels']
                    self._force_tkinter_canvas_update()
                
                print(f"Loaded template: {template_name}")
            else:
                print(f"Template not found: {template_name}")
        except Exception as e:
            print(f"Error loading template: {e}")

    def _force_tkinter_canvas_update(self):
        """Force immediate tkinter canvas display update"""
        # Update the tkinter canvas to show current grid state
        self._update_pixel_display()

    def _on_layer_changed(self):
        """Handle layer changes"""
        # Update canvas to show all visible layers combined
        self._update_canvas_from_layers()
    
    def _update_canvas_from_layers(self):
        """Update canvas to show all visible layers combined"""
        # Always show all visible layers combined
        flattened_pixels = self.layer_manager.flatten_layers()
        
        # Update canvas with the flattened result
        self.canvas.pixels = flattened_pixels
        self.canvas._redraw_surface()
        
        # Refresh the tkinter display
        self._initial_draw()
    
    def _get_drawing_layer(self):
        """Get the layer to draw on (active layer or topmost visible layer)"""
        active_layer = self.layer_manager.get_active_layer()
        if active_layer is None:
            # No layer selected (all layers view) - find topmost visible layer
            for i in range(len(self.layer_manager.layers) - 1, -1, -1):
                layer = self.layer_manager.layers[i]
                if layer.visible:
                    return layer
        return active_layer
    
    def _handle_eyedropper_click(self, canvas_x: int, canvas_y: int, button: int):
        """Handle eyedropper tool click to sample colors"""
        # Sample color from the canvas
        sampled_color = self.canvas.get_pixel(canvas_x, canvas_y)
        
        # Convert to RGB (remove alpha for comparison)
        rgb_color = sampled_color[:3]
        
        if button == 1:  # Left click - set primary color
            self._set_color_from_eyedropper(rgb_color, is_primary=True)
        elif button == 3:  # Right click - set secondary color
            self._set_color_from_eyedropper(rgb_color, is_primary=False)
    
    def _set_color_from_eyedropper(self, rgb_color: tuple, is_primary: bool = True):
        """Set color from eyedropper, either in palette or color wheel"""
        # First, try to find the color in the current palette
        found_in_palette = False
        
        for i, palette_color in enumerate(self.palette.colors):
            # Compare RGB values (ignore alpha)
            if palette_color[:3] == rgb_color:
                if is_primary:
                    self.palette.set_primary_color(i)
                else:
                    self.palette.set_secondary_color(i)
                found_in_palette = True
                break
        
        if found_in_palette:
            # Color found in palette, update UI
            self._update_color_grid_selection()
            print(f"Color found in palette: {rgb_color}")
        else:
            # Color not in palette, switch to color wheel mode
            self.view_mode_var.set("wheel")
            self._create_color_wheel()
            
            # Set the color in the color wheel
            if hasattr(self, 'color_wheel') and self.color_wheel:
                # Set the color directly in the color wheel
                self.color_wheel.set_color(rgb_color[0], rgb_color[1], rgb_color[2])
                print(f"Color set in color wheel: {rgb_color}")
    
    def _undo(self):
        """Undo last action"""
        # Get current state before undoing
        active_layer = self.layer_manager.get_active_layer()
        current_pixels = active_layer.pixels.copy() if active_layer else None
        current_layer_index = self.layer_manager.active_layer_index
        
        state = self.undo_manager.undo(current_pixels, current_layer_index)
        if state:
            # Restore layer state
            layer = self.layer_manager.get_layer(state.layer_index)
            if layer:
                layer.pixels = state.pixels
                self._on_layer_changed()
                # Force immediate tkinter canvas update for instant visual feedback
                self._force_tkinter_canvas_update()
                # Force immediate GUI refresh for instant response
                self.root.update_idletasks()
    
    def _redo(self):
        """Redo last undone action"""
        # Get current state before redoing
        active_layer = self.layer_manager.get_active_layer()
        current_pixels = active_layer.pixels.copy() if active_layer else None
        current_layer_index = self.layer_manager.active_layer_index
        
        state = self.undo_manager.redo(current_pixels, current_layer_index)
        if state:
            # Restore layer state
            layer = self.layer_manager.get_layer(state.layer_index)
            if layer:
                layer.pixels = state.pixels
                self._on_layer_changed()
                # Force immediate tkinter canvas update for instant visual feedback
                self._force_tkinter_canvas_update()
                # Force immediate GUI refresh for instant response
                self.root.update_idletasks()
    
    def _add_layer(self):
        """Add a new layer"""
        if self.layer_manager.add_layer():
            self.layer_panel.refresh()
            self._on_layer_changed()
    
    def _sync_canvas_with_layers(self):
        """Sync canvas with layer manager"""
        # Update layer manager canvas size
        self.layer_manager.resize_layers(self.canvas.width, self.canvas.height)
        
        # Set canvas pixels from active layer
        active_layer = self.layer_manager.get_active_layer()
        if active_layer:
            self.canvas.pixels = active_layer.pixels.copy()
            self.canvas._redraw_surface()
    
    def _on_tkinter_canvas_mouse_down(self, event):
        """Handle mouse down on tkinter canvas"""
        # Convert tkinter screen coordinates to canvas coordinates
        canvas_x, canvas_y = self._tkinter_screen_to_canvas_coords(event.x, event.y)

        if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
            # Get current tool
            tool = self.tools[self.current_tool]
            
            # Special handling for eyedropper tool
            if self.current_tool == "eyedropper":
                self._handle_eyedropper_click(canvas_x, canvas_y, event.num)
                return
            
            # Use color wheel color if in color wheel mode, otherwise use palette
            if (hasattr(self, 'color_wheel') and self.color_wheel and 
                self.view_mode_var.get() == "wheel"):
                rgb_color = self.color_wheel.get_color()
                color = (rgb_color[0], rgb_color[1], rgb_color[2], 255)
            else:
                color = self.palette.get_primary_color()

            # Get the layer to draw on
            draw_layer = self._get_drawing_layer()
            
            # Save state for undo
            if draw_layer:
                self.undo_manager.save_state(draw_layer.pixels.copy(),
                                           self.layer_manager.active_layer_index)

            # Store old color for efficient updating
            self._last_drawn_pixel = (canvas_x, canvas_y)
            old_color = self.canvas.get_pixel(canvas_x, canvas_y)

            # Set drawing state
            self.is_drawing = True

            # Apply the tool to the drawing layer
            if draw_layer:
                tool.on_mouse_down(draw_layer, canvas_x, canvas_y, 1, color)
                
                # Also update the current frame with the layer changes
                current_frame = self.timeline.get_current_frame()
                if current_frame:
                    current_frame.pixels = draw_layer.pixels.copy()
                
                # Update canvas to show all visible layers
                self._update_canvas_from_layers()
                
                # Update only the pixel that was drawn
                self._update_single_pixel(canvas_x, canvas_y, old_color)

    def _on_tkinter_canvas_mouse_up(self, event):
        """Handle mouse up on tkinter canvas"""
        canvas_x, canvas_y = self._tkinter_screen_to_canvas_coords(event.x, event.y)

        if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
            tool = self.tools[self.current_tool]
            color = self.palette.get_primary_color()

            # Store old color for efficient updating
            old_color = self.canvas.get_pixel(canvas_x, canvas_y)

            # Apply tool to drawing layer
            draw_layer = self._get_drawing_layer()
            if draw_layer:
                tool.on_mouse_up(draw_layer, canvas_x, canvas_y, 1, color)
                
                # Also update the current frame with the layer changes
                current_frame = self.timeline.get_current_frame()
                if current_frame:
                    current_frame.pixels = draw_layer.pixels.copy()
                
                # Update canvas to show all visible layers
                self._update_canvas_from_layers()

                # Update only the pixel that was affected
                self._update_single_pixel(canvas_x, canvas_y, old_color)

            # Clear drawing state
            self.is_drawing = False

    def _on_tkinter_canvas_mouse_drag(self, event):
        """Handle mouse drag on tkinter canvas"""
        canvas_x, canvas_y = self._tkinter_screen_to_canvas_coords(event.x, event.y)

        if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
            # Ensure we're in drawing state
            self.is_drawing = True

            tool = self.tools[self.current_tool]
            
            # Use color wheel color if in color wheel mode, otherwise use palette
            if (hasattr(self, 'color_wheel') and self.color_wheel and 
                self.view_mode_var.get() == "wheel"):
                rgb_color = self.color_wheel.get_color()
                color = (rgb_color[0], rgb_color[1], rgb_color[2], 255)
            else:
                color = self.palette.get_primary_color()

            # Store the previous pixel color for efficient updating
            old_color = self.canvas.get_pixel(canvas_x, canvas_y)

            # Apply tool to drawing layer
            draw_layer = self._get_drawing_layer()
            if draw_layer:
                tool.on_mouse_move(draw_layer, canvas_x, canvas_y, color)
                
                # Also update the current frame with the layer changes
                current_frame = self.timeline.get_current_frame()
                if current_frame:
                    current_frame.pixels = draw_layer.pixels.copy()
                
                # Update canvas to show all visible layers
                self._update_canvas_from_layers()

                # Only update the specific pixel that changed for better performance
                self._update_single_pixel(canvas_x, canvas_y, old_color)

    def _on_tkinter_canvas_mouse_move(self, event):
        """Handle mouse move on tkinter canvas"""
        canvas_x, canvas_y = self._tkinter_screen_to_canvas_coords(event.x, event.y)

        if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
            tool = self.tools[self.current_tool]
            
            # Use color wheel color if in color wheel mode, otherwise use palette
            if (hasattr(self, 'color_wheel') and self.color_wheel and 
                self.view_mode_var.get() == "wheel"):
                rgb_color = self.color_wheel.get_color()
                color = (rgb_color[0], rgb_color[1], rgb_color[2], 255)
            else:
                color = self.palette.get_primary_color()

            tool.on_mouse_move(self.canvas, canvas_x, canvas_y, color)
    
    def _tkinter_screen_to_canvas_coords(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """Convert tkinter screen coordinates to canvas coordinates"""
        # Get drawing canvas bounds and dimensions
        canvas_x = self.drawing_canvas.winfo_x()
        canvas_y = self.drawing_canvas.winfo_y()
        canvas_width = self.drawing_canvas.winfo_width()
        canvas_height = self.drawing_canvas.winfo_height()

        # Calculate the canvas display size and offsets (same as in _update_tkinter_canvas)
        canvas_pixel_width = self.canvas.width * self.canvas.zoom
        canvas_pixel_height = self.canvas.height * self.canvas.zoom
        x_offset = (canvas_width - canvas_pixel_width) // 2
        y_offset = (canvas_height - canvas_pixel_height) // 2

        # Convert screen coordinates to canvas-relative coordinates
        relative_x = screen_x - canvas_x - x_offset
        relative_y = screen_y - canvas_y - y_offset

        # Convert to canvas pixel coordinates
        canvas_coord_x = relative_x // self.canvas.zoom
        canvas_coord_y = relative_y // self.canvas.zoom

        return canvas_coord_x, canvas_coord_y
    

    def _update_pixel_display(self):
        """Update tkinter display to show all pixel changes (full redraw)"""
        # Prevent recursion
        if self._updating_display:
            return
        self._updating_display = True
        
        try:
            width = self.drawing_canvas.winfo_width()
            height = self.drawing_canvas.winfo_height()

            if width > 1 and height > 1:
                # Calculate canvas display size
                canvas_pixel_width = self.canvas.width * self.canvas.zoom
                canvas_pixel_height = self.canvas.height * self.canvas.zoom

                # Calculate offsets to center the canvas
                x_offset = (width - canvas_pixel_width) // 2
                y_offset = (height - canvas_pixel_height) // 2

                # Clear canvas
                self.drawing_canvas.delete("all")

                # Draw grid if enabled
                if self.canvas.show_grid:
                    self._draw_tkinter_grid(x_offset, y_offset, canvas_pixel_width, canvas_pixel_height)

                # Draw a border around the canvas area
                self.drawing_canvas.create_rectangle(
                    x_offset, y_offset,
                    x_offset + canvas_pixel_width, y_offset + canvas_pixel_height,
                    outline="black", width=2
                )

                # Draw all pixels from the canvas
                self._draw_all_pixels_on_tkinter(x_offset, y_offset)
        finally:
            self._updating_display = False

    def _update_single_pixel(self, canvas_x: int, canvas_y: int, old_color):
        """Update only a single pixel for better performance"""
        # For now, just trigger a full update to ensure consistency
        # This prevents the disappearing pixel bug
        self._update_pixel_display()

    def _on_frame_changed(self):
        """Handle frame change in timeline"""
        current_frame = self.timeline.get_current_frame()
        if current_frame:
            # Update canvas with current frame pixels
            self.canvas.pixels = current_frame.pixels.copy()
            self.canvas._redraw_surface()
            # Update the tkinter display
            self._update_pixel_display()
    
    def _toggle_animation(self):
        """Toggle animation playback"""
        if self.timeline.is_playing:
            self.timeline.pause()
        else:
            self.timeline.play()
        self.timeline_panel.refresh()
    
    def _previous_frame(self):
        """Go to previous frame"""
        self.timeline.previous_frame()
        self.timeline_panel.refresh()
        self._on_frame_changed()
    
    def _next_frame(self):
        """Go to next frame"""
        self.timeline.next_frame()
        self.timeline_panel.refresh()
        self._on_frame_changed()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
        pygame.quit()
