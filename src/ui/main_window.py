"""
Main application window for Pixel Perfect
Coordinates all UI components and handles events

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import customtkinter as ctk
import tkinter as tk
from typing import Optional, Tuple
import sys
import os
import numpy as np
from PIL import Image

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
from tools.pan import PanTool
from core.layer_manager import LayerManager
from core.undo_manager import UndoManager, UndoState
from ui.layer_panel import LayerPanel
from animation.timeline import AnimationTimeline
from ui.timeline_panel import TimelinePanel
from ui.tooltip import create_tooltip
from ui.theme_manager import ThemeManager

class MainWindow:
    """Main application window"""
    
    def __init__(self):
        # Set up CustomTkinter theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Pixel Perfect - Retro Pixel Art Editor")
        self.root.geometry("1200x800")
        
        # Set window icon
        try:
            # Get the correct base path (works for both dev and PyInstaller)
            if getattr(sys, 'frozen', False):
                # Running as compiled EXE
                base_path = os.path.dirname(sys.executable)
            else:
                # Running as script
                base_path = os.path.join(os.path.dirname(__file__), "..", "..")
            
            # Try ICO format first (best for Windows)
            icon_path = os.path.join(base_path, "assets", "icons", "app_icon.ico")
            icon_path = os.path.abspath(icon_path)
            
            if os.path.exists(icon_path):
                # Set window icon
                self.root.iconbitmap(icon_path)
                
                # Windows-specific: Set taskbar icon using Windows API
                if os.name == 'nt':
                    try:
                        import ctypes
                        # Set app user model ID for Windows taskbar grouping
                        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('PixelPerfect.PixelArtEditor.1.13')
                        # Force update the icon
                        self.root.after(100, lambda: self.root.iconbitmap(icon_path))
                    except:
                        pass
                
                print(f"[OK] Icon loaded: {icon_path}")
            else:
                # Fallback to PNG
                png_path = os.path.join(base_path, "assets", "icons", "app_icon.png")
                png_path = os.path.abspath(png_path)
                if os.path.exists(png_path):
                    icon_photo = tk.PhotoImage(file=png_path)
                    self.root.iconphoto(True, icon_photo)
                    print(f"[OK] Icon loaded (PNG): {png_path}")
                else:
                    print(f"[WARN] Icon not found at: {icon_path} or {png_path}")
        except Exception as e:
            print(f"[WARN] Could not load icon: {e}")
        
        # Initialize core systems
        self.canvas = Canvas(32, 32, zoom=16)  # Higher zoom for better grid visibility
        self.palette = ColorPalette()
        self.layer_manager = LayerManager(32, 32)
        self.undo_manager = UndoManager()
        self.timeline = AnimationTimeline(32, 32)
        
        # Initialize custom colors manager
        from src.core.custom_colors import CustomColorManager
        self.custom_colors = CustomColorManager()
        
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
            "circle": CircleTool(),
            "pan": PanTool()
        }
        self.current_tool = "brush"
        
        # Connect selection and move tools
        self.tools["move"].set_selection_tool(self.tools["selection"])
        
        # Set up auto-switch to move tool after selection
        self.tools["selection"].on_selection_complete = self._on_selection_complete
        
        # UI state
        self.is_drawing = False
        self.last_mouse_pos = (0, 0)
        self._last_drawn_pixel = None  # Track last drawn pixel for efficient updates
        self._updating_display = False  # Flag to prevent recursion
        
        # Copy/paste state
        self.is_placing_copy = False
        self.copy_buffer = None
        self.copy_dimensions = None
        self.copy_preview_pos = None  # Mouse position for copy preview
        
        # Scaling state
        self.is_scaling = False
        self.scale_handle = None  # Which handle is being dragged
        self.scale_start_pos = None
        self.scale_original_rect = None  # Reference rect for calculating deltas (updates between drags)
        self.scale_true_original_rect = None  # Never changes - used for final apply
        self.scale_is_dragging = False  # True while actively dragging (mouse down)
        
        # Pan state
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        self.theme_manager.on_theme_changed = self._apply_theme
        
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
        
        # Main content area with resizable panes (optimized for smooth resizing)
        self.paned_window = tk.PanedWindow(
            self.main_frame, 
            orient=tk.HORIZONTAL, 
            sashwidth=10,  # Wider for easier grabbing
            bg="#505050",  # Lighter grey for visibility
            sashrelief=tk.FLAT,  # Flat, no border
            bd=0,
            opaqueresize=False  # Don't show content during drag - faster!
        )
        self.paned_window.pack(fill="both", expand=True, pady=(10, 0))
        
        # Track panel resize state
        self._is_resizing_panels = False
        
        # Track panel collapse state
        self.left_panel_collapsed = False
        self.right_panel_collapsed = False
        
        # Left panel container (wrapper for CTk widget)
        self.left_container = tk.Frame(self.paned_window, bg="#2b2b2b")
        self.paned_window.add(self.left_container, minsize=220, width=520, stretch="never")
        
        # Left collapse button (visible when expanded)
        left_collapse_btn = ctk.CTkButton(
            self.left_container,
            text="◀",
            width=25,
            font=("Arial", 14, "bold"),
            fg_color="#1f538d",
            hover_color="#144870",
            corner_radius=8,
            command=self._toggle_left_panel
        )
        left_collapse_btn.pack(side="right", fill="y", padx=0, pady=0)
        self.left_collapse_btn = left_collapse_btn
        
        # Left panel (tools and palette) - with scrollbar (optimized for smooth resize)
        self.left_panel = ctk.CTkScrollableFrame(
            self.left_container, 
            width=520
        )
        self.left_panel.pack(side="left", fill="both", expand=True)
        
        # Canvas area container
        canvas_container = tk.Frame(self.paned_window, bg="#2b2b2b")
        self.paned_window.add(canvas_container, minsize=400, stretch="always")
        
        # Canvas area
        self.canvas_frame = ctk.CTkFrame(canvas_container)
        self.canvas_frame.pack(fill="both", expand=True)
        
        # Right panel container (wrapper for CTk widget)
        self.right_container = tk.Frame(self.paned_window, bg="#2b2b2b")
        self.paned_window.add(self.right_container, minsize=220, width=500, stretch="never")
        
        # Right collapse button (visible when expanded)
        right_collapse_btn = ctk.CTkButton(
            self.right_container,
            text="▶",
            width=25,
            font=("Arial", 14, "bold"),
            fg_color="#1f538d",
            hover_color="#144870",
            corner_radius=8,
            command=self._toggle_right_panel
        )
        right_collapse_btn.pack(side="left", fill="y", padx=0, pady=0)
        self.right_collapse_btn = right_collapse_btn
        
        # Right panel (layers, etc.) - with scrollbar (optimized for smooth resize)
        self.right_panel = ctk.CTkScrollableFrame(
            self.right_container, 
            width=500
        )
        self.right_panel.pack(side="right", fill="both", expand=True)
        
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
            values=["16x16", "32x32", "16x32", "32x64", "64x64"],
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
        
        # Theme selector with brand logo
        try:
            # Load DCS brand logo
            logo_path = os.path.join(os.path.dirname(__file__), "..", "..", "dcs.png")
            logo_path = os.path.abspath(logo_path)
            if os.path.exists(logo_path):
                logo_image = Image.open(logo_path)
                # Resize to fit toolbar (24x24)
                logo_image = logo_image.resize((24, 24), Image.Resampling.LANCZOS)
                logo_ctk = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(24, 24))
                self.theme_label = ctk.CTkLabel(self.toolbar, image=logo_ctk, text="")
            else:
                # Fallback to emoji if image not found
                self.theme_label = ctk.CTkLabel(self.toolbar, text="🎨", font=ctk.CTkFont(size=16))
        except Exception as e:
            print(f"[WARN] Could not load DCS logo: {e}")
            # Fallback to emoji if image loading fails
            self.theme_label = ctk.CTkLabel(self.toolbar, text="🎨", font=ctk.CTkFont(size=16))
        
        self.theme_label.pack(side="right", padx=(20, 2))
        create_tooltip(self.theme_label, "Color Theme - Diamond Clad Studios", delay=1000)
        
        self.theme_var = ctk.StringVar(value="Basic Grey")
        self.theme_menu = ctk.CTkOptionMenu(
            self.toolbar,
            variable=self.theme_var,
            values=self.theme_manager.get_theme_names(),
            command=self._on_theme_selected,
            width=120
        )
        self.theme_menu.pack(side="right", padx=5)
        
        # Grid toggle
        self.grid_button = ctk.CTkButton(self.toolbar, text="Grid", width=60)
        self.grid_button.pack(side="right", padx=5)
        self.grid_button.configure(command=self._toggle_grid)
        self._update_grid_button_text()
        
        # Grid overlay toggle (grid on top of pixels)
        self.grid_overlay = False
        self.grid_overlay_button = ctk.CTkButton(self.toolbar, text="Grid Overlay", width=90)
        self.grid_overlay_button.pack(side="right", padx=5)
        self.grid_overlay_button.configure(command=self._toggle_grid_overlay)
        self._update_grid_overlay_button_text()
    
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
        self.tool_frame.pack(fill="none", padx=10, pady=(5, 5))
        
        tool_label = ctk.CTkLabel(self.tool_frame, text="Tools", font=ctk.CTkFont(size=16, weight="bold"))
        tool_label.pack(pady=(5, 3))
        
        # Tool buttons container for grid layout
        tool_grid = ctk.CTkFrame(self.tool_frame)
        tool_grid.pack(pady=(0, 5), padx=5)
        
        # Tool buttons in 3x3 grid for compact layout
        self.tool_buttons = {}
        tools = [
            ("brush", "Brush", "Draw single pixels (B)"),
            ("eraser", "Eraser", "Erase pixels (E)"),
            ("fill", "Fill", "Fill areas with color (F)"),
            ("eyedropper", "Eyedropper", "Sample colors from canvas (I)"),
            ("selection", "Select", "Select rectangular areas (S)"),
            ("move", "Move", "Move selected pixels (M)"),
            ("line", "Line", "Draw straight lines (L)"),
            ("rectangle", "Square", "Draw rectangles and squares (R)"),
            ("circle", "Circle", "Draw circles (C)"),
            ("pan", "Pan", "Move camera view (Hold Space)")
        ]
        
        # Arrange in 3 columns
        for idx, (tool_id, tool_name, tooltip_text) in enumerate(tools):
            row = idx // 3
            col = idx % 3
            
            btn = ctk.CTkButton(
                tool_grid,
                text=tool_name,
                width=85,
                height=28,
                command=lambda t=tool_id: self._select_tool(t)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.tool_buttons[tool_id] = btn
            
            # Add tooltip
            create_tooltip(btn, tooltip_text, delay=1000)
        
        # Configure grid columns - buttons stay fixed size
        for col in range(3):
            tool_grid.grid_columnconfigure(col, weight=0)
        
        # Highlight current tool
        self._update_tool_selection()
        
        # Selection operations section
        selection_ops_label = ctk.CTkLabel(self.tool_frame, text="Selection", font=ctk.CTkFont(size=14, weight="bold"))
        selection_ops_label.pack(pady=(10, 3))
        
        # Selection operations buttons in 3 columns
        selection_ops_grid = ctk.CTkFrame(self.tool_frame)
        selection_ops_grid.pack(pady=(0, 5), padx=5)
        
        # Create selection operation buttons
        mirror_btn = ctk.CTkButton(
            selection_ops_grid,
            text="Mirror",
            width=85,
            height=28,
            command=self._mirror_selection,
            fg_color="gray"
        )
        mirror_btn.grid(row=0, column=0, padx=2, pady=2)
        create_tooltip(mirror_btn, "Flip selection horizontally", delay=1000)
        
        rotate_btn = ctk.CTkButton(
            selection_ops_grid,
            text="Rotate",
            width=85,
            height=28,
            command=self._rotate_selection,
            fg_color="gray"
        )
        rotate_btn.grid(row=0, column=1, padx=2, pady=2)
        create_tooltip(rotate_btn, "Rotate selection 90° clockwise", delay=1000)
        
        copy_btn = ctk.CTkButton(
            selection_ops_grid,
            text="Copy",
            width=85,
            height=28,
            command=self._copy_selection,
            fg_color="gray"
        )
        copy_btn.grid(row=0, column=2, padx=2, pady=2)
        create_tooltip(copy_btn, "Copy selection for placement", delay=1000)
        
        # Second row for Scale button
        scale_btn = ctk.CTkButton(
            selection_ops_grid,
            text="Scale",
            width=85,
            height=28,
            command=self._scale_selection,
            fg_color="gray"
        )
        scale_btn.grid(row=1, column=0, padx=2, pady=2, columnspan=3, sticky="ew")
        create_tooltip(scale_btn, "Scale selection with draggable corners", delay=1000)
        
        # Store references
        self.mirror_btn = mirror_btn
        self.rotate_btn = rotate_btn
        self.copy_btn = copy_btn
        self.scale_btn = scale_btn
        
        # Configure grid columns
        for col in range(3):
            selection_ops_grid.grid_columnconfigure(col, weight=0)
    
    def _create_palette_panel(self):
        """Create color palette panel"""
        self.palette_frame = ctk.CTkFrame(self.left_panel)
        self.palette_frame.pack(fill="x", padx=10, pady=(3, 5))
        
        palette_label = ctk.CTkLabel(self.palette_frame, text="Palette", font=ctk.CTkFont(size=16, weight="bold"))
        palette_label.pack(pady=(5, 3))
        
        # Palette selector
        self.palette_var = ctk.StringVar(value="SNES Classic")
        self.palette_menu = ctk.CTkOptionMenu(
            self.palette_frame,
            variable=self.palette_var,
            values=list(self.palette.get_preset_palettes().keys()),
            command=self._on_palette_change
        )
        self.palette_menu.pack(pady=3)
        
        # View mode selector - centered container
        view_mode_container = ctk.CTkFrame(self.palette_frame, fg_color="transparent")
        view_mode_container.pack(pady=3)
        
        view_mode_frame = ctk.CTkFrame(view_mode_container)
        view_mode_frame.pack()
        
        self.view_mode_var = ctk.StringVar(value="grid")
        
        # Create a grid layout for radio buttons - centered
        self.grid_view_btn = ctk.CTkRadioButton(
            view_mode_frame,
            text="Grid",
            variable=self.view_mode_var,
            value="grid",
            command=self._on_view_mode_change
        )
        self.grid_view_btn.grid(row=0, column=0, padx=5, pady=2)
        
        self.primary_view_btn = ctk.CTkRadioButton(
            view_mode_frame,
            text="Primary",
            variable=self.view_mode_var,
            value="primary",
            command=self._on_view_mode_change
        )
        self.primary_view_btn.grid(row=0, column=1, padx=5, pady=2)
        
        self.wheel_view_btn = ctk.CTkRadioButton(
            view_mode_frame,
            text="Wheel",
            variable=self.view_mode_var,
            value="wheel",
            command=self._on_view_mode_change
        )
        self.wheel_view_btn.grid(row=1, column=0, padx=5, pady=2)
        
        self.constants_view_btn = ctk.CTkRadioButton(
            view_mode_frame,
            text="Constants",
            variable=self.view_mode_var,
            value="constants",
            command=self._on_view_mode_change
        )
        self.constants_view_btn.grid(row=1, column=1, padx=5, pady=2)
        
        # Color display container - centered
        color_display_container = ctk.CTkFrame(self.palette_frame, fg_color="transparent")
        color_display_container.pack(fill="both", expand=True, pady=5)
        
        self.color_display_frame = ctk.CTkFrame(color_display_container)
        self.color_display_frame.pack(expand=True)
        
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
        
        # Create grid frame - centered
        self.color_frame = ctk.CTkFrame(self.color_display_frame)
        self.color_frame.pack(padx=10, pady=10)
        
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
        
        # Set initial cursor (brush tool is default)
        self.drawing_canvas.configure(cursor=self.tools[self.current_tool].cursor)

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

                # Draw a border around the canvas area with theme color
                theme = self.theme_manager.get_current_theme()
                self.drawing_canvas.create_rectangle(
                    x_offset, y_offset,
                    x_offset + canvas_pixel_width, y_offset + canvas_pixel_height,
                    outline=theme.canvas_border, width=2, tags="border"
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
        # Use theme color for grid
        theme = self.theme_manager.get_current_theme()
        grid_color = theme.grid_color

        # Draw vertical lines with 'grid' tag for easy theme updates
        for x in range(0, self.canvas.width + 1):
            screen_x = x_offset + (x * self.canvas.zoom)
            self.drawing_canvas.create_line(
                screen_x, y_offset,
                screen_x, y_offset + canvas_height,
                fill=grid_color, width=1, tags="grid"
            )

        # Draw horizontal lines with 'grid' tag
        for y in range(0, self.canvas.height + 1):
            screen_y = y_offset + (y * self.canvas.zoom)
            self.drawing_canvas.create_line(
                x_offset, screen_y,
                x_offset + canvas_width, screen_y,
                fill=grid_color, width=1, tags="grid"
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
        
        # Bind paned window for smooth resize detection
        self.paned_window.bind("<ButtonPress-1>", self._on_sash_drag_start)
        self.paned_window.bind("<ButtonRelease-1>", self._on_sash_drag_end)
        
        # Mouse events are now bound to the tkinter drawing canvas
    
    def _on_sash_drag_start(self, event):
        """Called when user starts dragging panel divider"""
        self._is_resizing_panels = True
    
    def _on_sash_drag_end(self, event):
        """Called when user stops dragging panel divider"""
        self._is_resizing_panels = False
        # Force a single update after drag completes
        self.root.update_idletasks()
    
    def _on_window_resize(self, event):
        """Handle window resize events to maintain grid centering"""
        # Skip if we're resizing panels (not the window)
        if self._is_resizing_panels:
            return
            
        # Only handle main window resize, not child widget events
        if event.widget == self.root:
            # Schedule a delayed redraw to avoid excessive updates during resize
            if hasattr(self, '_resize_timer') and self._resize_timer is not None:
                try:
                    self.root.after_cancel(self._resize_timer)
                except:
                    pass  # Timer already executed or cancelled
            
            self._resize_timer = self.root.after(100, self._redraw_canvas_after_resize)
    
    def _toggle_left_panel(self):
        """Collapse or expand the left panel"""
        if self.left_panel_collapsed:
            # Expand panel - remove restore button overlay
            if hasattr(self, 'left_restore_btn'):
                try:
                    self.left_restore_btn.place_forget()
                except:
                    pass
            
            # Re-add the container at the beginning
            # Get the current first pane to insert before it
            panes = self.paned_window.panes()
            if len(panes) > 0:
                self.paned_window.add(self.left_container, minsize=220, width=520, stretch="never", before=panes[0])
            else:
                self.paned_window.add(self.left_container, minsize=220, width=520, stretch="never")
            
            self.left_collapse_btn.configure(text="◀")
            self.left_panel_collapsed = False
            
            # Redraw canvas to re-center grid after panel expand
            self.root.after(50, self._redraw_canvas_after_resize)
        else:
            # Collapse panel
            self.paned_window.forget(self.left_container)
            self.left_collapse_btn.configure(text="▶")
            self.left_panel_collapsed = True
            
            # Create restore button if it doesn't exist (overlay on left edge)
            if not hasattr(self, 'left_restore_btn'):
                # Use regular tkinter button with custom styling for true transparency
                self.left_restore_btn = tk.Button(
                    self.paned_window,
                    text="▶",
                    font=("Arial", 18, "bold"),
                    fg="white",
                    bg="#1f538d",
                    activebackground="#2a6bb3",
                    activeforeground="white",
                    relief=tk.FLAT,
                    borderwidth=0,
                    highlightthickness=0,
                    width=3,
                    height=4,
                    cursor="hand2",
                    command=self._toggle_left_panel
                )
                # Bind hover events for color change
                self.left_restore_btn.bind("<Enter>", lambda e: self.left_restore_btn.configure(bg="#2a6bb3"))
                self.left_restore_btn.bind("<Leave>", lambda e: self.left_restore_btn.configure(bg="#1f538d"))
            
            # Place restore button directly on left edge
            self.left_restore_btn.place(x=5, y=100)
            
            # Redraw canvas to re-center grid after panel collapse
            self.root.after(50, self._redraw_canvas_after_resize)
    
    def _toggle_right_panel(self):
        """Collapse or expand the right panel"""
        if self.right_panel_collapsed:
            # Expand panel - remove restore button overlay
            if hasattr(self, 'right_restore_btn'):
                try:
                    self.right_restore_btn.place_forget()
                except:
                    pass
            
            # Re-add the container at the end
            self.paned_window.add(self.right_container, minsize=220, width=500, stretch="never")
            
            self.right_collapse_btn.configure(text="▶")
            self.right_panel_collapsed = False
            
            # Redraw canvas to re-center grid after panel expand
            self.root.after(50, self._redraw_canvas_after_resize)
        else:
            # Collapse panel
            self.paned_window.forget(self.right_container)
            self.right_collapse_btn.configure(text="◀")
            self.right_panel_collapsed = True
            
            # Create restore button if it doesn't exist (overlay on right edge)
            if not hasattr(self, 'right_restore_btn'):
                # Use regular tkinter button with custom styling for true transparency
                self.right_restore_btn = tk.Button(
                    self.paned_window,
                    text="◀",
                    font=("Arial", 18, "bold"),
                    fg="white",
                    bg="#1f538d",
                    activebackground="#2a6bb3",
                    activeforeground="white",
                    relief=tk.FLAT,
                    borderwidth=0,
                    highlightthickness=0,
                    width=3,
                    height=4,
                    cursor="hand2",
                    command=self._toggle_right_panel
                )
                # Bind hover events for color change
                self.right_restore_btn.bind("<Enter>", lambda e: self.right_restore_btn.configure(bg="#2a6bb3"))
                self.right_restore_btn.bind("<Leave>", lambda e: self.right_restore_btn.configure(bg="#1f538d"))
            
            # Place restore button directly on right edge
            # Use anchor='ne' to position from right edge (match left button offset)
            self.right_restore_btn.place(relx=1.0, x=-5, y=100, anchor='ne')
            
            # Redraw canvas to re-center grid after panel collapse
            self.root.after(50, self._redraw_canvas_after_resize)
    
    def _on_restore_btn_enter(self, button):
        """Hover effect - color already handled in bind"""
        pass
    
    def _on_restore_btn_leave(self, button):
        """Hover leave - color already handled in bind"""
        pass
    
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
        
        # Cancel copy placement mode
        if key == 'escape' and self.is_placing_copy:
            self.is_placing_copy = False
            self.copy_preview_pos = None
            self._update_pixel_display()
            print("[INFO] Copy placement cancelled")
            return
        
        # Cancel scaling mode
        if key == 'escape' and self.is_scaling:
            self.is_scaling = False
            self.scale_handle = None
            self.scale_is_dragging = False
            self.scale_original_rect = None
            self.scale_true_original_rect = None
            
            # Restore current tool's cursor and button highlighting
            tool = self.tools[self.current_tool]
            self.drawing_canvas.configure(cursor=tool.cursor)
            self.scale_btn.configure(fg_color="gray")
            self._update_tool_selection()
            
            self._update_pixel_display()
            print("[INFO] Scaling cancelled")
            return
        
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
        # Exit scaling mode if active
        if self.is_scaling:
            self.is_scaling = False
            self.scale_handle = None
            self.scale_original_rect = None
            self.scale_true_original_rect = None
            self.scale_is_dragging = False
            self.scale_btn.configure(fg_color="gray")
            print("[INFO] Exited scaling mode")
        
        self.current_tool = tool_id
        self._update_tool_selection()
        
        # Update canvas cursor based on selected tool
        if hasattr(self, 'drawing_canvas') and tool_id in self.tools:
            tool = self.tools[tool_id]
            self.drawing_canvas.configure(cursor=tool.cursor)
    
    def _on_selection_complete(self):
        """Called when selection is complete - auto-switch to move tool"""
        # Automatically switch to move tool after selection
        self._select_tool("move")
        print("Selection complete - switched to Move tool")
    
    def _mirror_selection(self):
        """Mirror (flip horizontally) the selected pixels"""
        # Exit scaling mode if active
        if self.is_scaling:
            self.is_scaling = False
            self.scale_handle = None
            self.scale_original_rect = None
            self.scale_true_original_rect = None
            self.scale_is_dragging = False
            self.scale_btn.configure(fg_color="gray")
            self._update_tool_selection()
            print("[INFO] Exited scaling mode")
        
        selection_tool = self.tools.get("selection")
        if not selection_tool or not selection_tool.has_active_selection():
            print("[INFO] No selection to mirror")
            return
        
        # Get selection data
        if selection_tool.selected_pixels is None:
            return
        
        bounds = selection_tool.get_selection_bounds()
        if not bounds:
            return
        
        left, top, width, height = bounds
        
        # Mirror the pixels horizontally (flip left-right)
        mirrored_pixels = np.flip(selection_tool.selected_pixels, axis=1).copy()
        
        # Update the selection with mirrored pixels
        selection_tool.selected_pixels = mirrored_pixels
        
        # Redraw on canvas
        draw_layer = self._get_drawing_layer()
        if draw_layer:
            for py in range(height):
                for px in range(width):
                    if py < mirrored_pixels.shape[0] and px < mirrored_pixels.shape[1]:
                        pixel_color = tuple(mirrored_pixels[py, px])
                        canvas_x = left + px
                        canvas_y = top + py
                        if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                            draw_layer.set_pixel(canvas_x, canvas_y, pixel_color)
            
            # Update canvas display
            self._update_canvas_from_layers()
            self._update_pixel_display()
            
        print("[OK] Selection mirrored")
    
    def _rotate_selection(self):
        """Rotate the selected pixels 90 degrees clockwise"""
        # Exit scaling mode if active
        if self.is_scaling:
            self.is_scaling = False
            self.scale_handle = None
            self.scale_original_rect = None
            self.scale_true_original_rect = None
            self.scale_is_dragging = False
            self.scale_btn.configure(fg_color="gray")
            self._update_tool_selection()
            print("[INFO] Exited scaling mode")
        
        selection_tool = self.tools.get("selection")
        if not selection_tool or not selection_tool.has_active_selection():
            print("[INFO] No selection to rotate")
            return
        
        # Get selection data
        if selection_tool.selected_pixels is None:
            return
        
        bounds = selection_tool.get_selection_bounds()
        if not bounds:
            return
        
        left, top, width, height = bounds
        
        # Rotate 90 degrees clockwise: transpose then flip horizontally
        rotated_pixels = np.rot90(selection_tool.selected_pixels, k=-1).copy()
        
        # Update the selection with rotated pixels
        selection_tool.selected_pixels = rotated_pixels
        
        # Note: rotation changes dimensions (width becomes height, height becomes width)
        new_width = rotated_pixels.shape[1]
        new_height = rotated_pixels.shape[0]
        
        # Update selection rectangle with new dimensions
        selection_tool.selection_rect = (left, top, new_width, new_height)
        
        # Clear old area
        draw_layer = self._get_drawing_layer()
        if draw_layer:
            # Clear original area
            for py in range(height):
                for px in range(width):
                    canvas_x = left + px
                    canvas_y = top + py
                    if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                        draw_layer.set_pixel(canvas_x, canvas_y, (0, 0, 0, 0))
            
            # Draw rotated pixels
            for py in range(new_height):
                for px in range(new_width):
                    if py < rotated_pixels.shape[0] and px < rotated_pixels.shape[1]:
                        pixel_color = tuple(rotated_pixels[py, px])
                        canvas_x = left + px
                        canvas_y = top + py
                        if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                            if pixel_color[3] > 0:  # Only draw non-transparent pixels
                                draw_layer.set_pixel(canvas_x, canvas_y, pixel_color)
            
            # Update canvas display
            self._update_canvas_from_layers()
            self._update_pixel_display()
            
        print("[OK] Selection rotated 90° clockwise")
    
    def _copy_selection(self):
        """Enter copy mode - allows placing a copy of the selection"""
        # Exit scaling mode if active
        if self.is_scaling:
            self.is_scaling = False
            self.scale_handle = None
            self.scale_original_rect = None
            self.scale_true_original_rect = None
            self.scale_is_dragging = False
            self.scale_btn.configure(fg_color="gray")
            self._update_tool_selection()
            print("[INFO] Exited scaling mode")
        
        selection_tool = self.tools.get("selection")
        if not selection_tool or not selection_tool.has_active_selection():
            print("[INFO] No selection to copy")
            return
        
        # Get selection data
        if selection_tool.selected_pixels is None:
            return
        
        # Store copy data
        self.copy_buffer = selection_tool.selected_pixels.copy()
        bounds = selection_tool.get_selection_bounds()
        if bounds:
            _, _, width, height = bounds
            self.copy_dimensions = (width, height)
            
            # Switch to a placement mode
            self.is_placing_copy = True
            
            print("[OK] Selection copied - click on canvas to place")
            print("     Press Escape to cancel placement")
    
    def _scale_selection(self):
        """Enter scaling mode for the selection"""
        selection_tool = self.tools.get("selection")
        if not selection_tool or not selection_tool.has_active_selection():
            print("[INFO] No selection to scale")
            return
        
        bounds = selection_tool.get_selection_bounds()
        if not bounds:
            return
        
        # Enter scaling mode
        self.is_scaling = True
        self.scale_original_rect = bounds  # Reference for calculating deltas
        self.scale_true_original_rect = bounds  # Never changes - for final apply
        
        # Change cursor to arrow for grabbing handles
        self.drawing_canvas.configure(cursor="arrow")
        
        # Update button states - deselect tool buttons, highlight Scale button
        for tool_id, btn in self.tool_buttons.items():
            btn.configure(fg_color="gray")
        self.scale_btn.configure(fg_color="blue")
        
        # Update display to show handles
        self._update_pixel_display()
        
        print("[OK] Scaling mode - drag corners/edges to resize")
        print("     Each drag applies scaling incrementally")
        print("     Click away from selection to exit")
    
    def _apply_scale(self, new_rect):
        """Apply scaling to the selection"""
        selection_tool = self.tools.get("selection")
        if not selection_tool or selection_tool.selected_pixels is None:
            return
        
        # Use the TRUE original rect (from when we entered scale mode)
        old_left, old_top, old_width, old_height = self.scale_true_original_rect
        new_left, new_top, new_width, new_height = new_rect
        
        # Ensure minimum size
        if new_width < 1 or new_height < 1:
            return
        
        # Scale the pixels using nearest neighbor (simple fallback method)
        self._simple_scale(selection_tool, old_width, old_height, new_width, new_height, new_left, new_top)
    
    def _simple_scale(self, selection_tool, old_width, old_height, new_width, new_height, new_left, new_top):
        """Simple scaling without scipy"""
        scaled_pixels = np.zeros((new_height, new_width, 4), dtype=np.uint8)
        
        for ny in range(new_height):
            for nx in range(new_width):
                # Map to original coordinates
                ox = int(nx * old_width / new_width)
                oy = int(ny * old_height / new_height)
                if oy < selection_tool.selected_pixels.shape[0] and ox < selection_tool.selected_pixels.shape[1]:
                    scaled_pixels[ny, nx] = selection_tool.selected_pixels[oy, ox]
        
        selection_tool.selected_pixels = scaled_pixels
        selection_tool.selection_rect = (new_left, new_top, new_width, new_height)
        
        # Redraw
        draw_layer = self._get_drawing_layer()
        if draw_layer:
            for py in range(new_height):
                for px in range(new_width):
                    pixel_color = tuple(scaled_pixels[py, px])
                    canvas_x = new_left + px
                    canvas_y = new_top + py
                    if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                        if pixel_color[3] > 0:
                            draw_layer.set_pixel(canvas_x, canvas_y, pixel_color)
            
            self._update_canvas_from_layers()
            self._update_pixel_display()
    
    def _preview_scaled_pixels(self, selection_tool, old_width, old_height, new_width, new_height, new_left, new_top):
        """Show a live preview of scaled pixels during drag (doesn't modify stored data)"""
        # Quick nearest-neighbor scaling for preview
        preview_pixels = np.zeros((new_height, new_width, 4), dtype=np.uint8)
        
        for ny in range(new_height):
            for nx in range(new_width):
                # Map to original coordinates
                ox = int(nx * old_width / new_width)
                oy = int(ny * old_height / new_height)
                if oy < selection_tool.selected_pixels.shape[0] and ox < selection_tool.selected_pixels.shape[1]:
                    preview_pixels[ny, nx] = selection_tool.selected_pixels[oy, ox]
        
        # Temporarily draw the preview on canvas
        draw_layer = self._get_drawing_layer()
        if draw_layer:
            # Clear the TRUE original area (where pixels actually were)
            true_orig_left, true_orig_top, true_orig_width, true_orig_height = self.scale_true_original_rect
            for py in range(true_orig_height):
                for px in range(true_orig_width):
                    canvas_x = true_orig_left + px
                    canvas_y = true_orig_top + py
                    if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                        draw_layer.set_pixel(canvas_x, canvas_y, (0, 0, 0, 0))
            
            # Draw the scaled preview
            for py in range(new_height):
                for px in range(new_width):
                    pixel_color = tuple(preview_pixels[py, px])
                    canvas_x = new_left + px
                    canvas_y = new_top + py
                    if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                        if pixel_color[3] > 0:
                            draw_layer.set_pixel(canvas_x, canvas_y, pixel_color)
            
            self._update_canvas_from_layers()
            self._update_pixel_display()
    
    def _get_scale_handle(self, x: int, y: int, left: int, top: int, width: int, height: int):
        """Detect which scale handle/edge the user clicked near"""
        handle_tolerance = max(3, 8 // self.canvas.zoom)  # Adjust based on zoom
        
        right = left + width
        bottom = top + height
        
        # Check corners first (higher priority)
        if abs(x - left) <= handle_tolerance and abs(y - top) <= handle_tolerance:
            return "tl"  # Top-left
        if abs(x - right) <= handle_tolerance and abs(y - top) <= handle_tolerance:
            return "tr"  # Top-right
        if abs(x - left) <= handle_tolerance and abs(y - bottom) <= handle_tolerance:
            return "bl"  # Bottom-left
        if abs(x - right) <= handle_tolerance and abs(y - bottom) <= handle_tolerance:
            return "br"  # Bottom-right
        
        # Check edges
        if abs(x - left) <= handle_tolerance and top <= y <= bottom:
            return "l"  # Left edge
        if abs(x - right) <= handle_tolerance and top <= y <= bottom:
            return "r"  # Right edge
        if abs(y - top) <= handle_tolerance and left <= x <= right:
            return "t"  # Top edge
        if abs(y - bottom) <= handle_tolerance and left <= x <= right:
            return "b"  # Bottom edge
        
        return None
    
    def _draw_scale_handle(self, x: float, y: float, size: int, color: str):
        """Draw a scale handle on the canvas"""
        half_size = size / 2
        self.drawing_canvas.create_rectangle(
            x - half_size, y - half_size,
            x + half_size, y + half_size,
            fill=color,
            outline="black",
            width=1,
            tags="selection"
        )
    
    def _place_copy_at(self, canvas_x: int, canvas_y: int):
        """Place the copied pixels at the specified position"""
        if self.copy_buffer is None or self.copy_dimensions is None:
            return
        
        width, height = self.copy_dimensions
        
        # Place pixels
        draw_layer = self._get_drawing_layer()
        if draw_layer:
            for py in range(height):
                for px in range(width):
                    if py < self.copy_buffer.shape[0] and px < self.copy_buffer.shape[1]:
                        pixel_color = tuple(self.copy_buffer[py, px])
                        dest_x = canvas_x + px
                        dest_y = canvas_y + py
                        if 0 <= dest_x < self.canvas.width and 0 <= dest_y < self.canvas.height:
                            # Only draw non-transparent pixels
                            if pixel_color[3] > 0:
                                draw_layer.set_pixel(dest_x, dest_y, pixel_color)
            
            # Update canvas display
            self._update_canvas_from_layers()
            self._update_pixel_display()
            
        # Exit placement mode
        self.is_placing_copy = False
        print(f"[OK] Copy placed at ({canvas_x}, {canvas_y})")
    
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
        """Handle canvas size change - WARNING: Downsizing clips pixels!"""
        from tkinter import messagebox
        
        size_map = {
            "16x16": CanvasSize.SMALL,
            "32x32": CanvasSize.MEDIUM,
            "16x32": CanvasSize.WIDE,
            "32x64": CanvasSize.LARGE,
            "64x64": CanvasSize.XLARGE
        }
        
        if size_str in size_map:
            # Store old dimensions for preservation info
            old_width = self.canvas.width
            old_height = self.canvas.height
            
            # Get new dimensions
            new_size = size_map[size_str].value
            new_width, new_height = new_size
            
            # CHECK: Will this resize clip pixels?
            will_clip_width = new_width < old_width
            will_clip_height = new_height < old_height
            
            if will_clip_width or will_clip_height:
                # WARN USER: Pixels will be permanently lost!
                clip_msg = f"⚠️ DOWNSIZING WARNING\n\n"
                clip_msg += f"Current size: {old_width}x{old_height}\n"
                clip_msg += f"New size: {new_width}x{new_height}\n\n"
                
                if will_clip_width and will_clip_height:
                    clip_msg += f"This will PERMANENTLY DELETE pixels outside the {new_width}x{new_height} region!\n\n"
                elif will_clip_width:
                    clip_msg += f"This will PERMANENTLY DELETE pixels beyond column {new_width-1} (right side)!\n\n"
                else:
                    clip_msg += f"This will PERMANENTLY DELETE pixels beyond row {new_height-1} (bottom)!\n\n"
                
                clip_msg += "Lost pixels CANNOT be recovered!\n\n"
                clip_msg += "Continue with resize?"
                
                # Show warning dialog
                result = messagebox.askyesno(
                    "Canvas Downsize Warning",
                    clip_msg,
                    icon='warning'
                )
                
                if not result:
                    # User cancelled - restore old size in dropdown
                    old_size_str = f"{old_width}x{old_height}"
                    self.size_var.set(old_size_str)
                    print(f"[Canvas Resize] Cancelled by user")
                    return
            
            # Resize canvas (updates dimensions only)
            self.canvas.set_preset_size(size_map[size_str])
            
            # Auto-adjust zoom based on canvas size for optimal viewing
            # Smaller canvases get higher zoom, larger canvases get lower zoom
            if size_str == "16x16":
                # Very small canvas - use high zoom (16x minimum)
                if self.canvas.zoom < 16:
                    self.canvas.set_zoom(16)
                    self.zoom_var.set("16x")
            elif size_str == "16x32" or size_str == "32x32":
                # Small canvas - use medium-high zoom (16x minimum)
                if self.canvas.zoom < 16:
                    self.canvas.set_zoom(16)
                    self.zoom_var.set("16x")
            elif size_str in ["32x64", "64x64"]:
                # Large canvas - reduce zoom to fit (8x maximum)
                if self.canvas.zoom > 8:
                    self.canvas.set_zoom(8)
                    self.zoom_var.set("8x")
            
            # Resize layer manager and timeline (both automatically preserve pixel data)
            # These methods copy existing pixels to the top-left of new size
            self.layer_manager.resize_layers(new_width, new_height)
            self.timeline.resize_frames(new_width, new_height)
            
            # Sync canvas display with resized layer data
            self._update_canvas_from_layers()
            
            # Update display immediately
            self._force_tkinter_canvas_update()
            
            # Log resize info
            preserved_w = min(old_width, new_width)
            preserved_h = min(old_height, new_height)
            print(f"[Canvas Resize] {old_width}x{old_height} → {new_width}x{new_height}")
            print(f"[Pixel Preservation] Top-left {preserved_w}x{preserved_h} region preserved")
    
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
        """Handle view mode change between grid, primary colors, color wheel, and constants"""
        mode = self.view_mode_var.get()
        if mode == "grid":
            self._create_color_grid()
        elif mode == "primary":
            self._create_primary_colors()
        elif mode == "constants":
            self._create_constants_grid()
        else:  # wheel
            self._create_color_wheel()
    
    def _create_constants_grid(self):
        """Create grid showing only colors currently used on the canvas"""
        # Clear existing widgets
        for widget in self.color_display_frame.winfo_children():
            widget.destroy()
        
        # Extract unique colors from canvas
        used_colors = self._get_canvas_colors()
        
        if not used_colors:
            # Show message if no colors are used yet
            no_colors_label = ctk.CTkLabel(
                self.color_display_frame,
                text="No colors used yet.\nDraw on canvas to see\ncolors here.",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            no_colors_label.pack(pady=20)
            return
        
        # Create grid of used colors
        grid_frame = ctk.CTkFrame(self.color_display_frame)
        grid_frame.pack()
        
        # Configure grid - 4 columns
        for col in range(4):
            grid_frame.grid_columnconfigure(col, weight=1)
        
        # Create buttons for each unique color
        self.color_buttons = []
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
            self.color_display_frame,
            text=f"{len(used_colors)} colors in use",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        count_label.pack(pady=(5, 0))
    
    def _get_canvas_colors(self):
        """Extract unique colors from the canvas (all layers combined)"""
        unique_colors = set()
        
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
            print(f"[OK] Selected color from constants: {rgb_color}")
        else:
            # Color not in current palette, switch to color wheel and set the color
            self.view_mode_var.set("wheel")
            self._create_color_wheel()
            
            if hasattr(self, 'color_wheel') and self.color_wheel:
                self.color_wheel.set_color(rgb_color)
                print(f"[OK] Selected color from constants (not in palette): {rgb_color}")
    
    def _create_color_wheel(self):
        """Create color wheel view"""
        # Clear existing widgets
        for widget in self.color_display_frame.winfo_children():
            widget.destroy()
        
        # Import and create color wheel
        from src.ui.color_wheel import ColorWheel
        self.color_wheel = ColorWheel(self.color_display_frame)
        self.color_wheel.on_color_changed = self._on_color_wheel_changed
        
        # Connect color wheel callbacks to custom colors management
        self.color_wheel.on_save_custom_color = self._save_custom_color
        self.color_wheel.on_remove_custom_color = self._remove_custom_color
        
        # Update custom colors grid with existing colors
        self._update_custom_colors_display()
    
    def _on_color_wheel_changed(self, rgb_color):
        """Handle color wheel color change - now just for UI updates"""
        # Update color display in UI
        self._update_pixel_display()
        print(f"Color wheel color changed: {rgb_color}")
    
    def _save_custom_color(self, rgb_color):
        """Save current color wheel color to custom colors"""
        # Convert RGB tuple to RGBA
        if len(rgb_color) == 3:
            rgba_color = (rgb_color[0], rgb_color[1], rgb_color[2], 255)
        else:
            rgba_color = rgb_color
        
        # Add to custom colors
        if self.custom_colors.add_color(rgba_color):
            print(f"[OK] Saved custom color: {rgba_color}")
            # Update the display
            self._update_custom_colors_display()
        else:
            if self.custom_colors.has_color(rgba_color):
                print(f"[WARN] Color already in custom colors: {rgba_color}")
            elif self.custom_colors.is_full():
                print(f"[WARN] Custom colors full (max {self.custom_colors.max_colors})")
    
    def _remove_custom_color(self, color):
        """Remove a custom color"""
        if self.custom_colors.remove_color_by_value(color):
            print(f"[DELETE] Removed custom color: {color}")
            # Update the display
            self._update_custom_colors_display()
    
    def _update_custom_colors_display(self):
        """Update the custom colors grid in color wheel"""
        if hasattr(self, 'color_wheel') and self.color_wheel:
            colors = self.custom_colors.get_colors()
            self.color_wheel.update_custom_colors_grid(colors)
    
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
    
    def _toggle_grid_overlay(self):
        """Toggle grid overlay mode (grid on top of pixels)"""
        self.grid_overlay = not self.grid_overlay
        self._update_grid_overlay_button_text()
        self._force_tkinter_canvas_update()
    
    def _update_grid_overlay_button_text(self):
        """Update grid overlay button text to show current state"""
        if self.grid_overlay:
            self.grid_overlay_button.configure(text="Overlay: ON")
            self.grid_overlay_button.configure(fg_color="#1f538d")
        else:
            self.grid_overlay_button.configure(text="Overlay: OFF")
            self.grid_overlay_button.configure(fg_color="gray")
    
    def _on_theme_selected(self, theme_name: str):
        """Handle theme selection from dropdown"""
        self.theme_manager.set_theme(theme_name)
        print(f"[OK] Theme changed to: {theme_name}")
    
    def _apply_theme(self, theme):
        """Apply theme colors to all UI elements - optimized for instant switching"""
        # SKIP appearance mode change - it causes full UI refresh!
        # Instead, manually configure all widget colors
        
        # Direct widget configuration (fast and immediate, no UI refresh)
        self.main_frame.configure(fg_color=theme.bg_primary)
        self.toolbar.configure(fg_color=theme.bg_secondary)
        self.tool_frame.configure(fg_color=theme.bg_primary)
        self.canvas_frame.configure(fg_color=theme.bg_primary)
        self.drawing_canvas.configure(bg=theme.canvas_bg)
        
        # Update all tool buttons
        for tool_id, btn in self.tool_buttons.items():
            if tool_id == self.current_tool:
                btn.configure(
                    fg_color=theme.tool_selected,
                    hover_color=theme.button_hover,
                    text_color=theme.text_primary
                )
            else:
                btn.configure(
                    fg_color=theme.tool_unselected,
                    hover_color=theme.button_hover,
                    text_color=theme.text_primary
                )
        
        # Update operation buttons (Mirror, Rotate, Copy, Scale)
        if hasattr(self, 'mirror_btn'):
            for btn in [self.mirror_btn, self.rotate_btn, self.copy_btn, self.scale_btn]:
                btn.configure(
                    fg_color=theme.button_normal,
                    hover_color=theme.button_hover,
                    text_color=theme.text_primary
                )
        
        # Update grid button
        if self.canvas.show_grid:
            self.grid_button.configure(fg_color="green", text_color=theme.text_primary)
        else:
            self.grid_button.configure(fg_color=theme.button_normal, text_color=theme.text_primary)
        
        # Update other toolbar buttons (different configure params for different widget types)
        self.file_button.configure(
            fg_color=theme.button_normal,
            hover_color=theme.button_hover,
            text_color=theme.text_primary
        )
        
        # Update dropdowns (CTkOptionMenu has different params)
        for dropdown in [self.size_menu, self.zoom_menu, self.theme_menu]:
            try:
                dropdown.configure(
                    fg_color=theme.button_normal,
                    text_color=theme.text_primary,
                    dropdown_fg_color=theme.bg_secondary,
                    dropdown_hover_color=theme.button_hover
                )
            except:
                pass  # Skip if params not supported
        
        # Update labels
        self.size_label.configure(text_color=theme.text_primary)
        self.zoom_label.configure(text_color=theme.text_primary)
        self.theme_label.configure(text_color=theme.text_primary)
        
        # Update left and right panel backgrounds
        self.left_panel.configure(
            fg_color=theme.bg_secondary,
            scrollbar_button_color=theme.button_normal,
            scrollbar_button_hover_color=theme.button_hover
        )
        self.right_panel.configure(
            fg_color=theme.bg_secondary,
            scrollbar_button_color=theme.button_normal,
            scrollbar_button_hover_color=theme.button_hover
        )
        
        # Update palette panel label
        if hasattr(self, 'palette_label'):
            self.palette_label.configure(text_color=theme.text_primary)
        
        # Update all section labels and frames in tool panel
        for widget in self.tool_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=theme.text_primary)
            elif isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color=theme.bg_primary)
        
        # Update palette panel and its children recursively
        if hasattr(self, 'palette_frame'):
            self.palette_frame.configure(fg_color=theme.bg_primary)
            self._apply_theme_to_children(self.palette_frame, theme)
        
        # Update palette dropdown
        if hasattr(self, 'palette_menu'):
            try:
                self.palette_menu.configure(
                    fg_color=theme.button_normal,
                    text_color=theme.text_primary
                )
            except:
                pass
        
        # Update layer panel if it exists (comprehensive)
        if hasattr(self, 'layer_panel'):
            try:
                # Update layer panel background - use layer_frame not frame
                if hasattr(self.layer_panel, 'layer_frame'):
                    self.layer_panel.layer_frame.configure(fg_color=theme.bg_secondary)
                    # Recursively update all children
                    self._apply_theme_to_children(self.layer_panel.layer_frame, theme)
            except Exception as e:
                print(f"[DEBUG] Layer panel theme error: {e}")
        
        # Update timeline panel if it exists (comprehensive)
        if hasattr(self, 'timeline_panel'):
            try:
                # Update timeline panel background - use timeline_frame not frame
                if hasattr(self.timeline_panel, 'timeline_frame'):
                    self.timeline_panel.timeline_frame.configure(fg_color=theme.bg_secondary)
                    # Recursively update all children
                    self._apply_theme_to_children(self.timeline_panel.timeline_frame, theme)
                
                # Update frame list scrollable area specifically
                if hasattr(self.timeline_panel, 'frame_list_frame'):
                    self.timeline_panel.frame_list_frame.configure(
                        fg_color=theme.bg_tertiary,
                        scrollbar_button_color=theme.button_normal,
                        scrollbar_button_hover_color=theme.button_hover
                    )
            except Exception as e:
                print(f"[DEBUG] Timeline panel theme error: {e}")
        
        # Update undo/redo buttons if they exist
        if hasattr(self, 'undo_button') and hasattr(self, 'redo_button'):
            self.undo_button.configure(
                fg_color=theme.button_normal,
                hover_color=theme.button_hover,
                text_color=theme.text_primary
            )
            self.redo_button.configure(
                fg_color=theme.button_normal,
                hover_color=theme.button_hover,
                text_color=theme.text_primary
            )
        
        # Update paned window sash (dividers between panels)
        if hasattr(self, 'paned_window'):
            try:
                self.paned_window.configure(bg=theme.bg_tertiary)
            except:
                pass
        
        # Update canvas elements (grid/border only, not pixels) - lightweight
        canvas_width = self.drawing_canvas.winfo_width()
        if canvas_width > 1:
            self._update_theme_canvas_elements(theme)
        
        print(f"[OK] Theme '{theme.name}' applied (instant mode)")
    
    def _apply_theme_to_children(self, parent_widget, theme):
        """Recursively apply theme to all children widgets"""
        for widget in parent_widget.winfo_children():
            try:
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color=theme.text_primary)
                elif isinstance(widget, ctk.CTkFrame):
                    # Check if it's supposed to be transparent
                    try:
                        current_fg = widget.cget("fg_color")
                        if current_fg == "transparent":
                            widget.configure(fg_color="transparent")
                        else:
                            widget.configure(fg_color=theme.bg_primary)
                    except:
                        widget.configure(fg_color=theme.bg_primary)
                    # Recursively update children
                    self._apply_theme_to_children(widget, theme)
                elif isinstance(widget, ctk.CTkRadioButton):
                    widget.configure(text_color=theme.text_primary)
                elif isinstance(widget, ctk.CTkButton):
                    widget.configure(
                        fg_color=theme.button_normal,
                        hover_color=theme.button_hover,
                        text_color=theme.text_primary
                    )
            except Exception as e:
                # Skip widgets that don't support these properties
                pass
    
    def _update_theme_canvas_elements(self, theme):
        """Update only theme-dependent canvas elements (grid, borders) without full redraw"""
        width = self.drawing_canvas.winfo_width()
        height = self.drawing_canvas.winfo_height()
        
        if width > 1 and height > 1:
            # Calculate canvas display size
            canvas_pixel_width = self.canvas.width * self.canvas.zoom
            canvas_pixel_height = self.canvas.height * self.canvas.zoom
            
            # Calculate offsets
            x_offset = (width - canvas_pixel_width) // 2
            y_offset = (height - canvas_pixel_height) // 2
            x_offset += self.pan_offset_x * self.canvas.zoom
            y_offset += self.pan_offset_y * self.canvas.zoom
            
            # Only redraw grid and border (not pixels!)
            # Delete old theme-dependent elements
            self.drawing_canvas.delete("grid")
            self.drawing_canvas.delete("border")
            
            # Draw grid if enabled (with new theme color)
            if self.canvas.show_grid:
                for x in range(self.canvas.width + 1):
                    screen_x = x_offset + (x * self.canvas.zoom)
                    self.drawing_canvas.create_line(
                        screen_x, y_offset,
                        screen_x, y_offset + canvas_pixel_height,
                        fill=theme.grid_color, tags="grid"
                    )
                for y in range(self.canvas.height + 1):
                    screen_y = y_offset + (y * self.canvas.zoom)
                    self.drawing_canvas.create_line(
                        x_offset, screen_y,
                        x_offset + canvas_pixel_width, screen_y,
                        fill=theme.grid_color, tags="grid"
                    )
            
            # Draw border with new theme color
            self.drawing_canvas.create_rectangle(
                x_offset, y_offset,
                x_offset + canvas_pixel_width, y_offset + canvas_pixel_height,
                outline=theme.canvas_border, width=2, tags="border"
            )
            
            # Bring pixels and selection to front (keep existing rendering)
            self.drawing_canvas.tag_raise("pixels")
            self.drawing_canvas.tag_raise("selection")
            
            # Raise grid above pixels if overlay mode is enabled
            if self.grid_overlay and self.canvas.show_grid:
                self.drawing_canvas.tag_raise("grid")
    
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
        
        import_png_btn = ctk.CTkButton(file_menu, text="Import PNG", command=lambda: [self._import_png(), file_menu.destroy()])
        import_png_btn.pack(pady=5, padx=10, fill="x")
        
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
        
        # Reset layers (clear_layers() already adds a "Background" layer)
        self.layer_manager.clear_layers()
        
        # Reset timeline
        self.timeline.clear_frames()
        self.timeline.add_frame()
        
        # Force canvas redraw with grid and update UI
        self._force_tkinter_canvas_update()
        self.layer_panel.refresh()
        self.timeline_panel.refresh()
        
        print("[OK] New project created")
    
    def _open_project(self):
        """Open an existing project"""
        try:
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(
                title="Open Pixel Perfect Project",
                filetypes=[("Pixel Perfect Files", "*.pixpf"), ("All Files", "*.*")]
            )
            
            if file_path:
                # Load project with all required parameters
                success = self.project.load_project(
                    file_path,
                    self.canvas,
                    self.palette,
                    self.layer_manager,
                    self.timeline
                )
                
                if success:
                    # Update canvas from loaded layers (this composites all layers)
                    self._update_canvas_from_layers()
                    
                    # Update UI components to reflect loaded project
                    self.layer_panel.refresh()
                    self.timeline_panel.refresh()
                    
                    # Force immediate display update
                    self.root.update_idletasks()
                    self.root.update()
                    
                    print(f"[OK] Project opened: {file_path}")
                else:
                    print(f"[ERROR] Failed to open project: {file_path}")
        except Exception as e:
            print(f"[ERROR] Error opening project: {e}")
            import traceback
            traceback.print_exc()
    
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
    
    def _import_png(self):
        """Import PNG directly into current canvas"""
        try:
            from tkinter import filedialog, messagebox
            from PIL import Image
            import numpy as np
            
            # Open file dialog for PNG selection
            png_path = filedialog.askopenfilename(
                title="Import PNG Image",
                filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
            )
            
            if not png_path:
                return  # User cancelled
            
            # Load and validate PNG
            from src.utils.import_png import PNGImporter
            importer = PNGImporter()
            is_valid, message, width, height = importer.validate_png_dimensions(png_path)
            
            if not is_valid:
                messagebox.showerror(
                    "Invalid PNG Dimensions",
                    f"{message}\n\n"
                    f"Valid sizes: 16x16, 32x32, or 64x64\n"
                    f"(or scaled versions: 128x128, 256x256, 512x512)"
                )
                return
            
            # Load the PNG
            image = Image.open(png_path)
            original_width, original_height = image.size
            
            # Check if we need to downscale
            needs_downscale = False
            scale_factor = 1
            
            if original_width != width or original_height != height:
                # Calculate scale factor
                scale_factor = original_width // width
                needs_downscale = True
                
                # Downscale using nearest neighbor
                rgba_image = image.convert('RGBA')
                rgba_image = rgba_image.resize((width, height), Image.NEAREST)
                print(f"Auto-downscaled from {original_width}x{original_height} to {width}x{height} ({scale_factor}x)")
            else:
                rgba_image = image.convert('RGBA')
            
            # Convert to numpy array
            pixels = np.array(rgba_image, dtype=np.uint8)
            
            # Update dimensions FIRST (before clearing layers)
            self.canvas.width = width
            self.canvas.height = height
            self.layer_manager.width = width
            self.layer_manager.height = height
            
            # Initialize canvas pixels array with correct dimensions
            self.canvas.pixels = np.zeros((height, width, 4), dtype=np.uint8)
            
            # Now clear layers (this will create layers with the NEW dimensions)
            self.layer_manager.clear_layers()
            
            # Set the imported pixels and layer name
            self.layer_manager.layers[0].name = "Imported"
            self.layer_manager.layers[0].pixels = pixels
            
            # Update canvas from layers (copies layer data to canvas.pixels)
            self._update_canvas_from_layers()
            
            # NOW create the pygame surface with the correct pixel data
            self.canvas._create_surface()
            
            # Clear animation frames
            self.timeline.frames.clear()
            self.timeline.current_frame = 0
            
            # Update UI
            self.layer_panel.refresh()
            self.timeline_panel.refresh()
            self.root.update_idletasks()
            self.root.update()
            
            # Clear project path (this is now a new unsaved project)
            self.project.current_project_path = None
            
            # Show success message
            if needs_downscale:
                messagebox.showinfo(
                    "Import Successful",
                    f"Imported {original_width}x{original_height} PNG\n"
                    f"(Auto-downscaled {scale_factor}x to {width}x{height})\n\n"
                    f"Ready to edit! Use File → Save Project when ready."
                )
            else:
                messagebox.showinfo(
                    "Import Successful",
                    f"Imported {width}x{height} PNG\n\n"
                    f"Ready to edit! Use File → Save Project when ready."
                )
            
            print(f"[OK] Imported PNG to canvas: {os.path.basename(png_path)}")
                
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Import Error", f"An error occurred:\n{e}")
            print(f"Error importing PNG: {e}")
            import traceback
            traceback.print_exc()
    
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
        # Redraw the canvas surface (pixels + grid)
        self.canvas._redraw_surface()
        # Update the tkinter canvas to show current grid state
        self._update_pixel_display()
        # Force tkinter to process all pending events and update display
        self.root.update_idletasks()
        self.root.update()

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
        
        # Refresh the tkinter display (use update instead of initial draw to prevent loop)
        self._update_pixel_display()
    
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
        # Handle pan tool start (use raw screen coords, not canvas coords!)
        if self.current_tool == "pan":
            tool = self.tools["pan"]
            tool.start_pan(event.x, event.y, self.pan_offset_x, self.pan_offset_y)
            return
        
        # Convert tkinter screen coordinates to canvas coordinates
        canvas_x, canvas_y = self._tkinter_screen_to_canvas_coords(event.x, event.y)

        # Handle copy placement mode
        if self.is_placing_copy and self.copy_buffer is not None:
            if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                self._place_copy_at(canvas_x, canvas_y)
            return
        
        # Handle scaling mode
        if self.is_scaling:
            selection_tool = self.tools.get("selection")
            if selection_tool and selection_tool.selection_rect:
                left, top, width, height = selection_tool.selection_rect
                
                # Check if clicking near a handle or edge
                handle = self._get_scale_handle(canvas_x, canvas_y, left, top, width, height)
                
                if handle:
                    # Start dragging a handle
                    # Update reference rect to current position before drag
                    self.scale_original_rect = selection_tool.selection_rect
                    self.scale_handle = handle
                    self.scale_start_pos = (canvas_x, canvas_y)
                    self.scale_is_dragging = True  # Mark as actively dragging
                    print(f"[DEBUG] Starting drag from {self.scale_original_rect} with handle {handle}")
                else:
                    # Click outside - exit scaling mode (pixels already scaled)
                    self.is_scaling = False
                    self.scale_handle = None
                    self.scale_original_rect = None
                    self.scale_true_original_rect = None
                    self.scale_is_dragging = False
                    
                    # Restore current tool's cursor and button highlighting
                    tool = self.tools[self.current_tool]
                    self.drawing_canvas.configure(cursor=tool.cursor)
                    self.scale_btn.configure(fg_color="gray")
                    self._update_tool_selection()
                    
                    print("[OK] Exited scaling mode")
            return

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
        # Handle pan tool end
        if self.current_tool == "pan":
            tool = self.tools["pan"]
            tool.end_pan()
            # Reset cursor back to open hand
            self.drawing_canvas.configure(cursor="hand2")
            return
        
        # Convert tkinter screen coordinates to canvas coordinates
        canvas_x, canvas_y = self._tkinter_screen_to_canvas_coords(event.x, event.y)
        
        # Handle scaling drag release - APPLY the scale incrementally
        if self.is_scaling and self.scale_is_dragging:
            selection_tool = self.tools.get("selection")
            if selection_tool and selection_tool.selection_rect and selection_tool.selected_pixels is not None:
                old_rect = self.scale_original_rect
                new_rect = selection_tool.selection_rect
                
                old_left, old_top, old_width, old_height = old_rect
                new_left, new_top, new_width, new_height = new_rect
                
                # If size actually changed, apply the scaling
                if old_width != new_width or old_height != new_height:
                    # Scale the stored pixel data
                    scaled_pixels = np.zeros((new_height, new_width, 4), dtype=np.uint8)
                    for ny in range(new_height):
                        for nx in range(new_width):
                            ox = int(nx * old_width / new_width)
                            oy = int(ny * old_height / new_height)
                            if oy < selection_tool.selected_pixels.shape[0] and ox < selection_tool.selected_pixels.shape[1]:
                                scaled_pixels[ny, nx] = selection_tool.selected_pixels[oy, ox]
                    
                    # Update the selection tool's stored pixels
                    selection_tool.selected_pixels = scaled_pixels
                    
                    # Redraw on canvas
                    draw_layer = self._get_drawing_layer()
                    if draw_layer:
                        # Clear old area
                        for py in range(old_height):
                            for px in range(old_width):
                                canvas_x = old_left + px
                                canvas_y = old_top + py
                                if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                                    draw_layer.set_pixel(canvas_x, canvas_y, (0, 0, 0, 0))
                        
                        # Draw new scaled pixels
                        for py in range(new_height):
                            for px in range(new_width):
                                pixel_color = tuple(scaled_pixels[py, px])
                                canvas_x = new_left + px
                                canvas_y = new_top + py
                                if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                                    if pixel_color[3] > 0:
                                        draw_layer.set_pixel(canvas_x, canvas_y, pixel_color)
                        
                        self._update_canvas_from_layers()
                    
                    print(f"[OK] Scaled from {old_width}x{old_height} to {new_width}x{new_height}")
                
                # Update both reference rects for next drag
                self.scale_original_rect = new_rect
                self.scale_true_original_rect = new_rect
            
            # End this drag operation but keep in scaling mode
            self.scale_is_dragging = False
            self._update_pixel_display()
            print("[INFO] Released - drag again to resize more, or click away to exit")
            return

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

            # Clear shape preview after finalizing shape
            self.drawing_canvas.delete("shape_preview")
            
            # Clear drawing state
            self.is_drawing = False

    def _on_tkinter_canvas_mouse_drag(self, event):
        """Handle mouse drag on tkinter canvas (button held down)"""
        # Handle pan drag (PRIORITY - check first, use raw screen coords!)
        if self.current_tool == "pan":
            tool = self.tools["pan"]
            if tool.is_panning:
                # Get new absolute offset from pan tool (not delta!)
                result = tool.update_pan(event.x, event.y, self.canvas.zoom)
                if result:
                    self.pan_offset_x, self.pan_offset_y = result
                    # Change cursor to grabbing hand
                    self.drawing_canvas.configure(cursor="fleur")
                    # Redraw canvas with new offset
                    self._update_pixel_display()
            return
        
        # Convert tkinter screen coordinates to canvas coordinates
        canvas_x, canvas_y = self._tkinter_screen_to_canvas_coords(event.x, event.y)
        
        # Handle scaling drag (PRIORITY - check second!)
        if self.is_scaling and self.scale_is_dragging and self.scale_handle and self.scale_start_pos:
            selection_tool = self.tools.get("selection")
            if selection_tool and selection_tool.selection_rect and selection_tool.selected_pixels is not None:
                old_left, old_top, old_width, old_height = self.scale_original_rect
                dx = canvas_x - self.scale_start_pos[0]
                dy = canvas_y - self.scale_start_pos[1]
                
                # Calculate new rectangle based on which handle is being dragged
                new_left, new_top, new_width, new_height = old_left, old_top, old_width, old_height
                
                if "t" in self.scale_handle:  # Top edge/corner
                    new_top = old_top + dy
                    new_height = old_height - dy
                if "b" in self.scale_handle:  # Bottom edge/corner
                    new_height = old_height + dy
                if "l" in self.scale_handle:  # Left edge/corner
                    new_left = old_left + dx
                    new_width = old_width - dx
                if "r" in self.scale_handle:  # Right edge/corner
                    new_width = old_width + dx
                
                # Ensure minimum size
                if new_width >= 1 and new_height >= 1:
                    # Update the selection rectangle for visual feedback
                    selection_tool.selection_rect = (new_left, new_top, new_width, new_height)
                    
                    # Show live preview of scaled pixels during drag
                    # This is a preview - not the actual scaling operation
                    self._preview_scaled_pixels(selection_tool, old_width, old_height, new_width, new_height, new_left, new_top)
                    
            return  # Don't do drawing when scaling

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

            # LIVE PREVIEW for shape tools (Line, Rectangle, Circle)
            if self.current_tool in ["line", "rectangle", "circle"]:
                # Update tool's tracking state
                tool.on_mouse_move(self.canvas, canvas_x, canvas_y, color)
                
                # Draw live preview on canvas (doesn't affect pixel data yet!)
                self._draw_shape_preview(tool, canvas_x, canvas_y, color)
                return  # Don't apply pixels until mouse up!

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
        
        # Update copy preview position
        if self.is_placing_copy:
            if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                self.copy_preview_pos = (canvas_x, canvas_y)
                self._update_pixel_display()  # Redraw with preview
            return
        
        # Handle scaling drag or cursor update
        if self.is_scaling:
            selection_tool = self.tools.get("selection")
            if selection_tool and selection_tool.selection_rect:
                # If actively dragging a handle (mouse button held down)
                if self.scale_is_dragging and self.scale_handle and self.scale_start_pos:
                    left, top, width, height = self.scale_original_rect
                    dx = canvas_x - self.scale_start_pos[0]
                    dy = canvas_y - self.scale_start_pos[1]
                    
                    # Calculate new rectangle based on which handle is being dragged
                    new_left, new_top, new_width, new_height = left, top, width, height
                    
                    if "t" in self.scale_handle:  # Top edge/corner
                        new_top = top + dy
                        new_height = height - dy
                    if "b" in self.scale_handle:  # Bottom edge/corner
                        new_height = height + dy
                    if "l" in self.scale_handle:  # Left edge/corner
                        new_left = left + dx
                        new_width = width - dx
                    if "r" in self.scale_handle:  # Right edge/corner
                        new_width = width + dx
                    
                    # Ensure minimum size
                    if new_width >= 1 and new_height >= 1:
                        selection_tool.selection_rect = (new_left, new_top, new_width, new_height)
                        self._update_pixel_display()
                else:
                    # Not dragging - update cursor based on what's under mouse
                    left, top, width, height = selection_tool.selection_rect
                    handle = self._get_scale_handle(canvas_x, canvas_y, left, top, width, height)
                    
                    # Change cursor based on handle type (Windows-compatible cursor names)
                    if handle in ["tl", "br"]:
                        self.drawing_canvas.configure(cursor="size_nw_se")  # Diagonal cursor
                    elif handle in ["tr", "bl"]:
                        self.drawing_canvas.configure(cursor="size_ne_sw")  # Diagonal cursor
                    elif handle == "t" or handle == "b":
                        self.drawing_canvas.configure(cursor="sb_v_double_arrow")  # Vertical cursor
                    elif handle == "l" or handle == "r":
                        self.drawing_canvas.configure(cursor="sb_h_double_arrow")  # Horizontal cursor
                    else:
                        self.drawing_canvas.configure(cursor="arrow")  # Default cursor
            return

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
    
    def _draw_shape_preview(self, tool, canvas_x: int, canvas_y: int, color: Tuple[int, int, int, int]):
        """Draw live preview of shape tools (Line, Square, Circle) on tkinter canvas"""
        import math
        
        # Clear any existing preview
        self.drawing_canvas.delete("shape_preview")
        
        # Get canvas dimensions and offsets
        canvas_width = self.drawing_canvas.winfo_width()
        canvas_height = self.drawing_canvas.winfo_height()
        canvas_pixel_width = self.canvas.width * self.canvas.zoom
        canvas_pixel_height = self.canvas.height * self.canvas.zoom
        x_offset = (canvas_width - canvas_pixel_width) // 2 + self.pan_offset_x
        y_offset = (canvas_height - canvas_pixel_height) // 2 + self.pan_offset_y
        
        # Convert color to hex for tkinter
        color_hex = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
        
        # LINE PREVIEW
        if self.current_tool == "line" and tool.is_drawing:
            start_x, start_y = tool.start_point
            
            # Convert canvas coords to screen coords
            screen_x1 = x_offset + (start_x * self.canvas.zoom) + (self.canvas.zoom // 2)
            screen_y1 = y_offset + (start_y * self.canvas.zoom) + (self.canvas.zoom // 2)
            screen_x2 = x_offset + (canvas_x * self.canvas.zoom) + (self.canvas.zoom // 2)
            screen_y2 = y_offset + (canvas_y * self.canvas.zoom) + (self.canvas.zoom // 2)
            
            # Draw preview line
            self.drawing_canvas.create_line(
                screen_x1, screen_y1, screen_x2, screen_y2,
                fill=color_hex, width=3, tags="shape_preview"
            )
        
        # SQUARE/RECTANGLE PREVIEW
        elif self.current_tool == "rectangle" and tool.is_drawing:
            start_x, start_y = tool.start_point
            
            # Calculate rectangle bounds
            left = min(start_x, canvas_x)
            right = max(start_x, canvas_x)
            top = min(start_y, canvas_y)
            bottom = max(start_y, canvas_y)
            
            # Convert to screen coords
            screen_x1 = x_offset + (left * self.canvas.zoom)
            screen_y1 = y_offset + (top * self.canvas.zoom)
            screen_x2 = x_offset + ((right + 1) * self.canvas.zoom)
            screen_y2 = y_offset + ((bottom + 1) * self.canvas.zoom)
            
            # Draw preview rectangle
            if tool.filled:
                self.drawing_canvas.create_rectangle(
                    screen_x1, screen_y1, screen_x2, screen_y2,
                    fill=color_hex, outline="", tags="shape_preview"
                )
            else:
                self.drawing_canvas.create_rectangle(
                    screen_x1, screen_y1, screen_x2, screen_y2,
                    outline=color_hex, width=3, tags="shape_preview"
                )
        
        # CIRCLE PREVIEW
        elif self.current_tool == "circle" and tool.is_drawing:
            center_x, center_y = tool.center
            
            # Calculate radius in screen coordinates
            dx = canvas_x - center_x
            dy = canvas_y - center_y
            radius_pixels = int(math.sqrt(dx * dx + dy * dy))
            radius_screen = radius_pixels * self.canvas.zoom
            
            # Convert center to screen coords
            screen_cx = x_offset + (center_x * self.canvas.zoom) + (self.canvas.zoom // 2)
            screen_cy = y_offset + (center_y * self.canvas.zoom) + (self.canvas.zoom // 2)
            
            # Calculate bounding box for oval
            screen_x1 = screen_cx - radius_screen
            screen_y1 = screen_cy - radius_screen
            screen_x2 = screen_cx + radius_screen
            screen_y2 = screen_cy + radius_screen
            
            # Draw preview circle (oval in tkinter)
            if tool.filled:
                self.drawing_canvas.create_oval(
                    screen_x1, screen_y1, screen_x2, screen_y2,
                    fill=color_hex, outline="", tags="shape_preview"
                )
            else:
                self.drawing_canvas.create_oval(
                    screen_x1, screen_y1, screen_x2, screen_y2,
                    outline=color_hex, width=3, tags="shape_preview"
                )
    
    def _tkinter_screen_to_canvas_coords(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """Convert tkinter screen coordinates to canvas coordinates"""
        # Get drawing canvas dimensions
        canvas_width = self.drawing_canvas.winfo_width()
        canvas_height = self.drawing_canvas.winfo_height()

        # Calculate the canvas display size and offsets (same as in _update_tkinter_canvas)
        canvas_pixel_width = self.canvas.width * self.canvas.zoom
        canvas_pixel_height = self.canvas.height * self.canvas.zoom
        x_offset = (canvas_width - canvas_pixel_width) // 2
        y_offset = (canvas_height - canvas_pixel_height) // 2

        # Convert screen coordinates to canvas-relative coordinates
        # event.x and event.y are already relative to the widget, so no need to subtract winfo_x/y
        relative_x = screen_x - x_offset
        relative_y = screen_y - y_offset

        # Convert to canvas pixel coordinates
        canvas_coord_x = relative_x // self.canvas.zoom
        canvas_coord_y = relative_y // self.canvas.zoom
        
        # Apply pan offset
        canvas_coord_x -= self.pan_offset_x
        canvas_coord_y -= self.pan_offset_y

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
                
                # Apply pan offset
                x_offset += self.pan_offset_x * self.canvas.zoom
                y_offset += self.pan_offset_y * self.canvas.zoom

                # Clear canvas
                self.drawing_canvas.delete("all")

                # Draw grid if enabled
                if self.canvas.show_grid:
                    self._draw_tkinter_grid(x_offset, y_offset, canvas_pixel_width, canvas_pixel_height)

                # Draw a border around the canvas area with theme color
                theme = self.theme_manager.get_current_theme()
                self.drawing_canvas.create_rectangle(
                    x_offset, y_offset,
                    x_offset + canvas_pixel_width, y_offset + canvas_pixel_height,
                    outline=theme.canvas_border, width=2, tags="border"
                )

                # Draw all pixels from the canvas
                self._draw_all_pixels_on_tkinter(x_offset, y_offset)
                
                # Draw selection rectangle if active
                self._draw_selection_on_tkinter(x_offset, y_offset)
                
                # Raise grid above pixels if overlay mode is enabled
                if self.grid_overlay and self.canvas.show_grid:
                    self.drawing_canvas.tag_raise("grid")
        finally:
            self._updating_display = False

    def _draw_selection_on_tkinter(self, x_offset: int, y_offset: int):
        """Draw selection rectangle on tkinter canvas"""
        # Check if selection tool is active or if there's an active selection
        selection_tool = self.tools.get("selection")
        if not selection_tool:
            return
        
        # Draw selection rectangle if it exists
        if selection_tool.selection_rect and (selection_tool.is_selecting or selection_tool.has_selection):
            left, top, width, height = selection_tool.selection_rect
            zoom = self.canvas.zoom
            
            # Convert canvas coordinates to screen coordinates
            screen_x1 = x_offset + (left * zoom)
            screen_y1 = y_offset + (top * zoom)
            screen_x2 = x_offset + ((left + width) * zoom)
            screen_y2 = y_offset + ((top + height) * zoom)
            
            # Draw white selection rectangle
            self.drawing_canvas.create_rectangle(
                screen_x1, screen_y1, screen_x2, screen_y2,
                outline="white", width=2, tags="selection"
            )
            
            # Draw corner markers for better visibility
            corner_size = 6
            # Top-left
            self.drawing_canvas.create_line(screen_x1, screen_y1, screen_x1 + corner_size, screen_y1, fill="white", width=3, tags="selection")
            self.drawing_canvas.create_line(screen_x1, screen_y1, screen_x1, screen_y1 + corner_size, fill="white", width=3, tags="selection")
            # Top-right
            self.drawing_canvas.create_line(screen_x2, screen_y1, screen_x2 - corner_size, screen_y1, fill="white", width=3, tags="selection")
            self.drawing_canvas.create_line(screen_x2, screen_y1, screen_x2, screen_y1 + corner_size, fill="white", width=3, tags="selection")
            # Bottom-left
            self.drawing_canvas.create_line(screen_x1, screen_y2, screen_x1 + corner_size, screen_y2, fill="white", width=3, tags="selection")
            self.drawing_canvas.create_line(screen_x1, screen_y2, screen_x1, screen_y2 - corner_size, fill="white", width=3, tags="selection")
            # Bottom-right
            self.drawing_canvas.create_line(screen_x2, screen_y2, screen_x2 - corner_size, screen_y2, fill="white", width=3, tags="selection")
            self.drawing_canvas.create_line(screen_x2, screen_y2, screen_x2, screen_y2 - corner_size, fill="white", width=3, tags="selection")
            
            # Draw scale handles if in scaling mode
            if self.is_scaling:
                handle_size = 8
                # Draw corner handles
                self._draw_scale_handle(screen_x1, screen_y1, handle_size, "yellow")  # Top-left
                self._draw_scale_handle(screen_x2, screen_y1, handle_size, "yellow")  # Top-right
                self._draw_scale_handle(screen_x1, screen_y2, handle_size, "yellow")  # Bottom-left
                self._draw_scale_handle(screen_x2, screen_y2, handle_size, "yellow")  # Bottom-right
                
                # Draw edge handles
                mid_x = (screen_x1 + screen_x2) / 2
                mid_y = (screen_y1 + screen_y2) / 2
                self._draw_scale_handle(mid_x, screen_y1, handle_size, "orange")  # Top
                self._draw_scale_handle(mid_x, screen_y2, handle_size, "orange")  # Bottom
                self._draw_scale_handle(screen_x1, mid_y, handle_size, "orange")  # Left
                self._draw_scale_handle(screen_x2, mid_y, handle_size, "orange")  # Right
        
        # Draw copy preview if in placement mode
        if self.is_placing_copy and self.copy_preview_pos and self.copy_buffer is not None and self.copy_dimensions:
            preview_x, preview_y = self.copy_preview_pos
            width, height = self.copy_dimensions
            zoom = self.canvas.zoom
            
            # Draw preview pixels with semi-transparency effect (stipple pattern)
            for py in range(height):
                for px in range(width):
                    if py < self.copy_buffer.shape[0] and px < self.copy_buffer.shape[1]:
                        pixel_color = tuple(self.copy_buffer[py, px])
                        if pixel_color[3] > 0:  # Only draw non-transparent pixels
                            canvas_x = preview_x + px
                            canvas_y = preview_y + py
                            if 0 <= canvas_x < self.canvas.width and 0 <= canvas_y < self.canvas.height:
                                screen_x = x_offset + (canvas_x * zoom)
                                screen_y = y_offset + (canvas_y * zoom)
                                
                                # Draw semi-transparent preview rectangle
                                color_hex = f'#{pixel_color[0]:02x}{pixel_color[1]:02x}{pixel_color[2]:02x}'
                                self.drawing_canvas.create_rectangle(
                                    screen_x, screen_y,
                                    screen_x + zoom, screen_y + zoom,
                                    fill=color_hex,
                                    outline="",
                                    stipple="gray50",  # Semi-transparent effect
                                    tags="copy_preview"
                                )
            
            # Draw preview boundary
            preview_screen_x1 = x_offset + (preview_x * zoom)
            preview_screen_y1 = y_offset + (preview_y * zoom)
            preview_screen_x2 = x_offset + ((preview_x + width) * zoom)
            preview_screen_y2 = y_offset + ((preview_y + height) * zoom)
            
            self.drawing_canvas.create_rectangle(
                preview_screen_x1, preview_screen_y1,
                preview_screen_x2, preview_screen_y2,
                outline="cyan",
                width=2,
                dash=(4, 4),  # Dashed line
                tags="copy_preview"
            )
    
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
