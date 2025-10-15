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
from core.event_dispatcher import EventDispatcher
from core.canvas_renderer import CanvasRenderer
from core.window_state_manager import WindowStateManager
from ui.palette_views import GridView, PrimaryView, SavedView, ConstantsView
from core.color_palette import ColorPalette
from tools.brush import BrushTool
from tools.eraser import EraserTool
from tools.fill import FillTool
from tools.eyedropper import EyedropperTool
from tools.selection import SelectionTool, MoveTool
from tools.shapes import LineTool, RectangleTool, CircleTool
from tools.pan import PanTool
from tools.texture import TextureTool, TextureLibrary
from core.layer_manager import LayerManager
from core.undo_manager import UndoManager, UndoState
from ui.layer_panel import LayerPanel
from animation.timeline import AnimationTimeline
from ui.timeline_panel import TimelinePanel
from ui.tooltip import create_tooltip
from ui.theme_manager import ThemeManager
from ui.ui_builder import UIBuilder
from ui.theme_dialog_manager import ThemeDialogManager
from ui.file_operations_manager import FileOperationsManager

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
        
        # Initialize responsive panel sizing
        # Try to restore saved window state first, fallback to calculated optimal sizes
        if not self._restore_window_state():
            self.left_panel_width, self.right_panel_width = self._calculate_optimal_panel_widths()
        
        # Initialize custom colors manager
        from src.core.custom_colors import CustomColorManager
        self.custom_colors = CustomColorManager()
        
        # Initialize saved colors manager (local user storage)
        from src.core.saved_colors import SavedColorsManager
        self.saved_colors = SavedColorsManager(max_colors=24)
        
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
            "pan": PanTool(),
            "texture": TextureTool()
        }
        self.current_tool = "brush"
        
        # Texture library
        self.texture_library = TextureLibrary()
        
        # Brush size (1x1, 2x2, 3x3)
        self.brush_size = 1
        self.brush_drawing = False
        
        # Eraser size (1x1, 2x2, 3x3)
        self.eraser_size = 1
        
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
        
        # Grid overlay state
        self.grid_overlay = False
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        # Initialize theme dialog manager
        self.theme_dialog_manager = ThemeDialogManager(self)
        
        # Initialize canvas renderer (before UI creation)
        from src.core.canvas_renderer import CanvasRenderer
        self.canvas_renderer = CanvasRenderer(self)
        
        # Initialize event dispatcher (bind events after UI creation)
        self.event_dispatcher = EventDispatcher(self)
        
        # Initialize tool buttons dictionary
        self.tool_buttons = {}
        
        # Initialize palette-related attributes
        self.grid_view_frame = None
        self.primary_view_frame = None
        self.wheel_view_frame = None
        self.constants_view_frame = None
        self.saved_view_frame = None
        self.color_frame = None
        self.primary_frame = None
        self.variations_frame = None
        self.palette_frame = None
        self.palette_var = None
        self.palette_label = None
        self.palette_menu = None
        self.view_mode_var = None
        self.color_wheel = None
        self.theme_manager.on_theme_changed = self.theme_dialog_manager.apply_theme
        
        # Create UI
        self._create_ui()
        
        # Apply initial theme (Basic Grey) to all UI elements
        self.theme_dialog_manager.apply_theme(self.theme_manager.get_current_theme())
        
        # Update tool selection to highlight brush
        self._update_tool_selection()
        
        # Initialize palette views and show grid
        self._initialize_all_views()
        self._show_view("grid")
        
        # Initialize canvas integration
        self._sync_canvas_with_layers()
    
    def _create_ui(self):
        """Create the user interface"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initialize UI Builder and create toolbar first (so it appears at top)
        self.ui_builder = UIBuilder(self.main_frame, self._get_ui_callbacks(), self.theme_manager)
        self.ui_builder.create_toolbar()
        
        # Assign toolbar widget references
        self.toolbar = self.ui_builder.widgets['toolbar']
        self.file_button = self.ui_builder.widgets['file_button']
        self.size_label = self.ui_builder.widgets['size_label']
        self.size_var = self.ui_builder.widgets['size_var']
        self.size_menu = self.ui_builder.widgets['size_menu']
        self.zoom_label = self.ui_builder.widgets['zoom_label']
        self.zoom_var = self.ui_builder.widgets['zoom_var']
        self.zoom_menu = self.ui_builder.widgets['zoom_menu']
        self.undo_button = self.ui_builder.widgets['undo_button']
        self.redo_button = self.ui_builder.widgets['redo_button']
        self.theme_label = self.ui_builder.widgets['theme_label']
        self.theme_var = self.ui_builder.widgets['theme_var']
        self.theme_menu = self.ui_builder.widgets['theme_menu']
        self.settings_button = self.ui_builder.widgets['settings_button']
        self.grid_button = self.ui_builder.widgets['grid_button']
        self.grid_overlay_button = self.ui_builder.widgets['grid_overlay_button']
        
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
        
        # Left panel container (wrapper for CTk widget) - OPTIMIZED for instant visibility
        self.left_container = tk.Frame(self.paned_window, bg=self.theme_manager.get_current_theme().bg_primary)
        self.paned_window.add(self.left_container, minsize=200, width=self.left_panel_width, stretch="never")
        
        # Left collapse button (visible when expanded)
        left_collapse_btn = ctk.CTkButton(
            self.left_container,
            text="◀",
            width=25,
            font=("Arial", 14, "bold"),
            fg_color=self.theme_manager.get_current_theme().button_active,
            hover_color=self.theme_manager.get_current_theme().button_hover,
            corner_radius=8,
            command=self._toggle_left_panel
        )
        left_collapse_btn.pack(side="right", fill="y", padx=0, pady=0)
        self.left_collapse_btn = left_collapse_btn
        
        # Left panel (tools and palette) - with scrollbar (optimized for smooth resize)
        self.left_panel = ctk.CTkScrollableFrame(
            self.left_container, 
            width=self.left_panel_width,
            fg_color=self.theme_manager.get_current_theme().bg_secondary
        )
        self.left_panel.pack(side="left", fill="both", expand=True)
        
        # Canvas area container
        canvas_container = tk.Frame(self.paned_window, bg=self.theme_manager.get_current_theme().bg_primary)
        self.paned_window.add(canvas_container, minsize=400, stretch="always")
        
        # Canvas area
        self.canvas_frame = ctk.CTkFrame(canvas_container)
        self.canvas_frame.pack(fill="both", expand=True)
        
        # Right panel container (wrapper for CTk widget) - OPTIMIZED for instant visibility
        self.right_container = tk.Frame(self.paned_window, bg="#1a1a1a")
        self.paned_window.add(self.right_container, minsize=200, width=self.right_panel_width, stretch="never")
        
        # Right collapse button (visible when expanded)
        right_collapse_btn = ctk.CTkButton(
            self.right_container,
            text="▶",
            width=25,
            font=("Arial", 14, "bold"),
            fg_color=self.theme_manager.get_current_theme().button_active,
            hover_color=self.theme_manager.get_current_theme().button_hover,
            corner_radius=8,
            command=self._toggle_right_panel
        )
        right_collapse_btn.pack(side="left", fill="y", padx=0, pady=0)
        self.right_collapse_btn = right_collapse_btn
        
        # Right panel (layers, etc.) - with scrollbar (optimized for smooth resize)
        self.right_panel = ctk.CTkScrollableFrame(
            self.right_container, 
            width=self.right_panel_width,
            fg_color="transparent"
        )
        self.right_panel.pack(side="right", fill="both", expand=True)
        
        # Create panels using UIBuilder
        selection_buttons = self.ui_builder.create_tool_panel(self.left_panel, self.tool_buttons, self._get_ui_callbacks())
        self.tool_frame = selection_buttons['tool_frame']
        
        # Update tool button text to show sizes
        self._update_brush_button_text()
        self._update_eraser_button_text()
        
        palette_widgets = self.ui_builder.create_palette_panel(self.left_panel, self.palette, self._get_ui_callbacks())
        # Assign palette widget references
        self.color_display_frame = palette_widgets['color_display_container']
        self.palette_content_frame = palette_widgets['palette_content_frame']
        self.grid_view_frame = palette_widgets['grid_view_frame']
        self.primary_view_frame = palette_widgets['primary_view_frame']
        self.wheel_view_frame = palette_widgets['wheel_view_frame']
        self.constants_view_frame = palette_widgets['constants_view_frame']
        self.saved_view_frame = palette_widgets['saved_view_frame']
        self.view_mode_var = palette_widgets['view_mode_var']
        self.palette_var = palette_widgets['palette_var']
        self.palette_menu = palette_widgets['palette_menu']
        self.palette_label = palette_widgets['palette_label']
        self.palette_frame = palette_widgets.get('palette_frame')
        self.color_frame = palette_widgets.get('color_display_frame')
        self.primary_frame = palette_widgets.get('primary_frame')
        self.variations_frame = palette_widgets.get('variations_frame')
        
        canvas_widgets = self.ui_builder.create_canvas_panel(self.canvas_frame, self.canvas_renderer, self.current_tool, self.tools, self._get_ui_callbacks())
        self.tkinter_canvas = canvas_widgets['drawing_canvas']
        self.drawing_canvas = canvas_widgets['drawing_canvas']  # Alias for compatibility
        
        # Pre-create layer and timeline panels for instant loading (OPTIMIZATION)
        self._create_layer_and_timeline_panels()
    
    def _create_layer_and_timeline_panels(self):
        """Create layer and timeline panels once for instant loading (OPTIMIZATION)"""
        # Initialize layer panel
        self.layer_panel = LayerPanel(self.right_panel, self.layer_manager)
        self.layer_panel.on_layer_changed = self._on_layer_changed
        
        # Initialize timeline panel
        self.timeline_panel = TimelinePanel(self.right_panel, self.timeline)
        self.timeline_panel.on_frame_changed = self._on_frame_changed
        
        # Initialize file operations manager
        self.file_ops = FileOperationsManager(
            self.root, self.canvas, self.palette, self.layer_manager,
            self.timeline, self.project, self.export_manager, self.presets,
            self.layer_panel, self.timeline_panel
        )
        self.file_ops.force_canvas_update_callback = self._force_tkinter_canvas_update
        self.file_ops.update_canvas_from_layers_callback = self._update_canvas_from_layers
        
        # Force immediate render of all panel widgets (pre-render optimization)
        # This "warms up" CustomTkinter widgets so they appear instantly later
        self.root.update_idletasks()
        
        # Mark panels as pre-created for optimization
        self._panels_pre_created = True
        
        # Initialize window state manager (after UI creation)
        self.window_state_manager = WindowStateManager(
            root=self.root,
            left_container=self.left_container,
            right_container=self.right_container,
            paned_window=self.paned_window,
            left_collapse_btn=self.left_collapse_btn,
            right_collapse_btn=self.right_collapse_btn,
            redraw_callback=self._redraw_canvas_after_resize
        )
        # Transfer panel width values to manager
        self.window_state_manager.left_panel_width = self.left_panel_width
        self.window_state_manager.right_panel_width = self.right_panel_width
        
        # Try to restore saved window state (overrides calculated sizes if successful)
        self._restore_window_state()
        
        # Initialize palette views (after UI creation so palette_content_frame exists)
        self.grid_view = GridView(
            self.palette_content_frame, 
            self.palette, 
            self.theme_manager,
            on_color_select=self._select_color,
            on_tool_switch=self._select_tool
        )
        self.primary_view = PrimaryView(
            self.palette_content_frame, 
            self.palette, 
            self.canvas,
            on_color_select=self._select_color,
            on_tool_switch=self._select_tool
        )
        # Initialize color wheel first (needed by other views)
        from src.ui.color_wheel import ColorWheel
        self.color_wheel = ColorWheel(self.palette_content_frame, theme=self.theme_manager.current_theme)
        self.color_wheel.on_color_changed = self._on_color_wheel_changed
        self.color_wheel.on_save_custom_color = self._save_custom_color
        self.color_wheel.on_remove_custom_color = self._remove_custom_color
        
        self.saved_view = SavedView(
            self.palette_content_frame, 
            self.saved_colors, 
            self.palette, 
            self.canvas,
            self.color_wheel,
            self.view_mode_var,
            on_update_display=self._update_pixel_display
        )
        self.constants_view = ConstantsView(
            self.palette_content_frame, 
            self.canvas, 
            self.palette, 
            self.color_wheel,
            self.view_mode_var,
            on_show_view=self._show_view
        )
        
        # Bind all events (after UI creation so widgets exist)
        self.event_dispatcher.bind_all_events()
    
    def _toggle_left_panel(self):
        """Toggle left panel visibility"""
        if hasattr(self, 'window_state_manager'):
            self.window_state_manager.toggle_left_panel()
    
    def _toggle_right_panel(self):
        """Toggle right panel visibility"""
        if hasattr(self, 'window_state_manager'):
            self.window_state_manager.toggle_right_panel()
    
    def _redraw_canvas_after_resize(self):
        """Redraw canvas after window/panel resize"""
        if hasattr(self, 'canvas_renderer'):
            self.canvas_renderer.update_pixel_display()
    
    def _get_ui_callbacks(self):
        """Returns a dictionary of callbacks for the UI builder."""
        return {
            'show_file_menu': self._show_file_menu,
            'on_size_change': self._on_size_change,
            'on_zoom_change': self._on_zoom_change,
            'undo': self._undo,
            'redo': self._redo,
            'on_theme_selected': self._on_theme_selected,
            'show_settings_dialog': self.theme_dialog_manager.show_settings_dialog,
            'toggle_grid': self._toggle_grid,
            'toggle_grid_overlay': self._toggle_grid_overlay,
            'select_tool': self._select_tool,
            'update_tool_selection': self._update_tool_selection,
            'show_brush_size_menu': self._show_brush_size_menu,
            'show_eraser_size_menu': self._show_eraser_size_menu,
            'open_texture_panel': self._open_texture_panel,
            'mirror_selection': self._mirror_selection,
            'rotate_selection': self._rotate_selection,
            'copy_selection': self._copy_selection,
            'scale_selection': self._scale_selection,
            'on_palette_change': self._on_palette_change,
            'on_view_mode_change': self._on_view_mode_change,
            'initialize_all_views': self._initialize_all_views,
            'show_view': self._show_view,
        }

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

            # Debug: Initial draw - Canvas size (removed for clean console)
            
            if width > 1 and height > 1:
                # Set canvas size to match our pixel grid
                canvas_pixel_width = self.canvas.width * self.canvas.zoom
                canvas_pixel_height = self.canvas.height * self.canvas.zoom

                # Debug: Pixel canvas size (removed for clean console)

                # Center the canvas in the available space
                x_offset = (width - canvas_pixel_width) // 2
                y_offset = (height - canvas_pixel_height) // 2

                # Debug: Offsets (removed for clean console)

                # Clear canvas
                self.drawing_canvas.delete("all")

                # Draw grid if enabled
                if self.canvas.show_grid:
                    # Debug: Drawing grid (removed for clean console)
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
                
                # Debug: Initial draw complete (removed for clean console)
            else:
                # Debug: Canvas not ready yet (removed for clean console)
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
    
    def _show_brush_size_menu(self, event):
        """Show brush size selection popup menu"""
        # Create popup menu
        menu = tk.Menu(self.root, tearoff=0, bg="#2d2d2d", fg="white", 
                      activebackground="#1a73e8", activeforeground="white",
                      relief=tk.FLAT, borderwidth=0)
        
        # Add size options with visual indicators
        sizes = [
            (1, "1x1 • Single Pixel"),
            (2, "2x2 • Small Brush"),
            (3, "3x3 • Medium Brush")
        ]
        
        for size, label in sizes:
            # Add checkmark for current size
            display_label = f"✓ {label}" if size == self.brush_size else f"   {label}"
            menu.add_command(
                label=display_label,
                command=lambda s=size: self._set_brush_size(s),
                font=("Segoe UI", 10)
            )
        
        # Show menu at mouse position
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def _set_brush_size(self, size: int):
        """Set brush size"""
        self.brush_size = size
        self._update_brush_button_text()
        
        # Auto-select brush tool
        if self.current_tool != "brush":
            self._select_tool("brush")
    
    def _update_brush_button_text(self):
        """Update brush button to show current size"""
        if "brush" in self.tool_buttons:
            size_text = f"{self.brush_size}x{self.brush_size}"
            self.tool_buttons["brush"].configure(text=f"Brush [{size_text}]")
    
    def _draw_brush_at(self, layer, x: int, y: int, color: tuple):
        """Draw brush at position with current size"""
        # Calculate offset for centering (makes odd sizes like 3x3 centered properly)
        offset = self.brush_size // 2
        
        # Draw NxN square
        for dy in range(self.brush_size):
            for dx in range(self.brush_size):
                px = x - offset + dx
                py = y - offset + dy
                
                # Check bounds
                if 0 <= px < layer.width and 0 <= py < layer.height:
                    layer.set_pixel(px, py, color)
    
    def _draw_eraser_at(self, layer, x: int, y: int):
        """Draw eraser at position with current size"""
        # Calculate offset for centering (makes odd sizes like 3x3 centered properly)
        offset = self.eraser_size // 2
        
        # Erase NxN square (set to transparent)
        for dy in range(self.eraser_size):
            for dx in range(self.eraser_size):
                px = x - offset + dx
                py = y - offset + dy
                
                # Check bounds
                if 0 <= px < layer.width and 0 <= py < layer.height:
                    layer.set_pixel(px, py, (0, 0, 0, 0))  # Transparent
    
    def _show_eraser_size_menu(self, event):
        """Show eraser size selection popup menu"""
        # Create popup menu
        menu = tk.Menu(self.root, tearoff=0, bg="#2d2d2d", fg="white", 
                      activebackground="#1a73e8", activeforeground="white",
                      relief=tk.FLAT, borderwidth=0)
        
        # Eraser sizes
        sizes = [
            (1, "1×1 (Single Pixel)"),
            (2, "2×2 (Small)"),
            (3, "3×3 (Medium)")
        ]
        
        for size, label in sizes:
            # Add checkmark for current size
            display_label = f"✓ {label}" if size == self.eraser_size else f"   {label}"
            menu.add_command(
                label=display_label,
                command=lambda s=size: self._set_eraser_size(s),
                font=("Segoe UI", 10)
            )
        
        # Show menu at mouse position
        try:
            menu.post(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def _set_eraser_size(self, size: int):
        """Set eraser size"""
        self.eraser_size = size
        self._update_eraser_button_text()
        
        # Auto-select eraser tool
        if self.current_tool != "eraser":
            self._select_tool("eraser")
    
    def _update_eraser_button_text(self):
        """Update eraser button to show current size"""
        if "eraser" in self.tool_buttons:
            size_text = f"{self.eraser_size}x{self.eraser_size}"
            self.tool_buttons["eraser"].configure(text=f"Eraser [{size_text}]")
    
    def _erase_at(self, layer, x: int, y: int):
        """Erase at position with current size"""
        # Calculate offset for centering (makes odd sizes like 3x3 centered properly)
        offset = self.eraser_size // 2
        
        # Erase NxN square (set to transparent)
        for dy in range(self.eraser_size):
            for dx in range(self.eraser_size):
                px = x - offset + dx
                py = y - offset + dy
                
                # Check bounds
                if 0 <= px < layer.width and 0 <= py < layer.height:
                    layer.set_pixel(px, py, (0, 0, 0, 0))  # Transparent
    
    def _select_tool(self, tool_id: str):
        """Select a drawing tool"""
        # Clear any tool previews when changing tools
        self.drawing_canvas.delete("brush_preview")
        self.drawing_canvas.delete("eraser_preview")
        self.drawing_canvas.delete("texture_preview")
        
        # Exit scaling mode if active
        if self.is_scaling:
            self.is_scaling = False
            self.scale_handle = None
            self.scale_original_rect = None
            self.scale_true_original_rect = None
            self.scale_is_dragging = False
            self.scale_btn.configure(fg_color=self.theme_manager.get_current_theme().button_normal)
            # Debug: Exited scaling mode (removed for clean console)
        
        # Finalize move and clear selection when switching away from selection/move tools
        if (self.current_tool in ["selection", "move"] and 
            tool_id not in ["selection", "move"]):
            # Finalize any pending move operation first
            move_tool = self.tools.get("move")
            if move_tool and hasattr(move_tool, 'finalize_move'):
                draw_layer = self._get_drawing_layer()
                if draw_layer:
                    move_tool.finalize_move(draw_layer)
                    # Debug: Finalized move operation before tool switch (removed for clean console)
            
            selection_tool = self.tools.get("selection")
            if selection_tool and selection_tool.has_selection:
                selection_tool.clear_selection()
                self._update_pixel_display()
                # Debug: Selection cleared - switched to different tool (removed for clean console)
        
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
        # Debug: Selection complete - switched to Move tool (removed for clean console)
    
    def _mirror_selection(self):
        """Mirror (flip horizontally) the selected pixels"""
        # Exit scaling mode if active
        if self.is_scaling:
            self.is_scaling = False
            self.scale_handle = None
            self.scale_original_rect = None
            self.scale_true_original_rect = None
            self.scale_is_dragging = False
            self.scale_btn.configure(fg_color=self.theme_manager.get_current_theme().button_normal)
            self._update_tool_selection()
            # Debug: Exited scaling mode (removed for clean console)
        
        selection_tool = self.tools.get("selection")
        if not selection_tool or not selection_tool.has_active_selection():
            # Debug: No selection to mirror (removed for clean console)
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
            
        # Debug: Selection mirrored (removed for clean console)
    
    def _rotate_selection(self):
        """Rotate the selected pixels 90 degrees clockwise"""
        # Exit scaling mode if active
        if self.is_scaling:
            self.is_scaling = False
            self.scale_handle = None
            self.scale_original_rect = None
            self.scale_true_original_rect = None
            self.scale_is_dragging = False
            self.scale_btn.configure(fg_color=self.theme_manager.get_current_theme().button_normal)
            self._update_tool_selection()
            # Debug: Exited scaling mode (removed for clean console)
        
        selection_tool = self.tools.get("selection")
        if not selection_tool or not selection_tool.has_active_selection():
            # Debug: No selection to rotate (removed for clean console)
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
            
        # Debug: Selection rotated 90° clockwise (removed for clean console)
    
    def _copy_selection(self):
        """Enter copy mode - allows placing a copy of the selection"""
        # Exit scaling mode if active
        if self.is_scaling:
            self.is_scaling = False
            self.scale_handle = None
            self.scale_original_rect = None
            self.scale_true_original_rect = None
            self.scale_is_dragging = False
            self.scale_btn.configure(fg_color=self.theme_manager.get_current_theme().button_normal)
            self._update_tool_selection()
            # Debug: Exited scaling mode (removed for clean console)
        
        selection_tool = self.tools.get("selection")
        if not selection_tool or not selection_tool.has_active_selection():
            # Debug: No selection to copy (removed for clean console)
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
            
            # Debug: Selection copied - click on canvas to place (removed for clean console)
    
    def _scale_selection(self):
        """Enter scaling mode for the selection"""
        selection_tool = self.tools.get("selection")
        if not selection_tool or not selection_tool.has_active_selection():
            # Debug: No selection to scale (removed for clean console)
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
            btn.configure(fg_color=self.theme_manager.get_current_theme().button_normal)
        self.scale_btn.configure(fg_color="blue")
        
        # Update display to show handles
        self._update_pixel_display()
        
        # Debug: Scaling mode messages (removed for clean console)
        # Debug: Click away from selection to exit (removed for clean console)
    
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
        # Debug: Copy placed (removed for clean console)
    
    def _update_tool_selection(self):
        """Update tool button appearance"""
        for tool_id, btn in self.tool_buttons.items():
            if tool_id == self.current_tool:
                btn.configure(fg_color="blue")
            else:
                btn.configure(fg_color=self.theme_manager.get_current_theme().button_normal)
    
    def _select_color(self, color_index: int):
        """Select a color from the palette"""
        self.palette.set_primary_color(color_index)
        
        # Update the color grid to show new selection
        if hasattr(self, 'color_frame'):
            self._update_color_grid_selection()
        
        # Auto-switch to brush tool for immediate painting
        if self.current_tool != "brush":
            self._select_tool("brush")
    
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
    
    def _open_custom_size_dialog(self):
        """Open dialog for custom canvas size input"""
        # Create custom size dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Custom Canvas Size")
        dialog.geometry("400x280")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center on main window
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (400 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (280 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Header with icon
        header_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        header_frame.pack(pady=20, padx=20, fill="x")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📐 Custom Canvas Size",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack()
        
        # Input frame
        input_frame = ctk.CTkFrame(dialog)
        input_frame.pack(padx=20, pady=10, fill="x")
        
        # Width input
        width_label = ctk.CTkLabel(input_frame, text="Width (pixels):", font=ctk.CTkFont(size=14))
        width_label.pack(pady=(10, 5))
        
        width_entry = ctk.CTkEntry(
            input_frame,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16),
            placeholder_text="e.g., 48"
        )
        width_entry.pack(pady=5)
        width_entry.insert(0, str(self.canvas.width))
        
        # Height input
        height_label = ctk.CTkLabel(input_frame, text="Height (pixels):", font=ctk.CTkFont(size=14))
        height_label.pack(pady=(10, 5))
        
        height_entry = ctk.CTkEntry(
            input_frame,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16),
            placeholder_text="e.g., 48"
        )
        height_entry.pack(pady=5)
        height_entry.insert(0, str(self.canvas.height))
        
        # Result storage
        result = [None, None]
        
        def on_apply():
            try:
                width = int(width_entry.get())
                height = int(height_entry.get())
                
                # Validate dimensions
                if width < 1 or height < 1:
                    from tkinter import messagebox
                    messagebox.showerror("Invalid Size", "Width and height must be at least 1 pixel!")
                    return
                
                if width > 512 or height > 512:
                    from tkinter import messagebox
                    messagebox.showerror("Invalid Size", "Maximum size is 512x512 pixels!")
                    return
                
                result[0] = width
                result[1] = height
                dialog.destroy()
            except ValueError:
                from tkinter import messagebox
                messagebox.showerror("Invalid Input", "Please enter valid numbers!")
        
        def on_cancel():
            dialog.destroy()
        
        # Button frame
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20, padx=20, fill="x")
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=120,
            height=35,
            fg_color="#4a4a4a",
            hover_color="#5a5a5a",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=on_cancel
        )
        cancel_btn.pack(side="right", padx=5)
        
        apply_btn = ctk.CTkButton(
            button_frame,
            text="Apply",
            width=120,
            height=35,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=on_apply
        )
        apply_btn.pack(side="right", padx=5)
        
        # Bind Enter key to apply
        width_entry.bind("<Return>", lambda e: height_entry.focus())
        height_entry.bind("<Return>", lambda e: on_apply())
        
        # Focus width entry and select all (delayed to ensure dialog is rendered)
        def focus_and_select():
            width_entry.focus_force()
            width_entry.select_range(0, 'end')
            width_entry.icursor('end')  # Move cursor to end after selection
        
        dialog.after(100, focus_and_select)
        
        # Wait for dialog
        self.root.wait_window(dialog)
        
        return result[0], result[1]
    
    def _on_size_change(self, size_str: str):
        """Handle canvas size change - WARNING: Downsizing clips pixels!"""
        # Handle custom size dialog
        if size_str == "Custom...":
            width, height = self._open_custom_size_dialog()
            
            if width is None or height is None:
                # User cancelled - restore previous size
                if self.custom_canvas_size:
                    self.size_var.set(f"CUSTOM ({self.custom_canvas_size[0]}x{self.custom_canvas_size[1]})")
                else:
                    # Restore to current actual size
                    current_size = f"{self.canvas.width}x{self.canvas.height}"
                    if current_size in ["16x16", "32x32", "16x32", "32x64", "64x64"]:
                        self.size_var.set(current_size)
                    else:
                        self.size_var.set("32x32")
                return
            
            # Apply custom size
            self._apply_custom_canvas_size(width, height)
            return
        
        size_map = {
            "16x16": CanvasSize.SMALL,
            "32x32": CanvasSize.MEDIUM,
            "16x32": CanvasSize.WIDE,
            "32x64": CanvasSize.LARGE,
            "64x64": CanvasSize.XLARGE
        }
        
        # Clear custom size when switching to preset
        self.custom_canvas_size = None
        
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
                # Show custom styled warning dialog
                result = self._show_downsize_warning(old_width, old_height, new_width, new_height)
                
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
    
    def _apply_custom_canvas_size(self, width: int, height: int):
        """Apply custom canvas size with same safety checks as preset sizes"""
        # Store old dimensions
        old_width = self.canvas.width
        old_height = self.canvas.height
        
        # CHECK: Will this resize clip pixels?
        will_clip_width = width < old_width
        will_clip_height = height < old_height
        
        if will_clip_width or will_clip_height:
            # WARN USER: Pixels will be permanently lost!
            # Show custom styled warning dialog
            result = self._show_downsize_warning(old_width, old_height, width, height)
            
            if not result:
                # User cancelled - restore previous size in dropdown
                if self.custom_canvas_size:
                    self.size_var.set(f"CUSTOM ({self.custom_canvas_size[0]}x{self.custom_canvas_size[1]})")
                else:
                    old_size_str = f"{old_width}x{old_height}"
                    self.size_var.set(old_size_str)
                print(f"[Custom Canvas Resize] Cancelled by user")
                return
        
        # Apply custom size
        self.canvas.resize(width, height)
        
        # Store custom size
        self.custom_canvas_size = (width, height)
        
        # Update dropdown to show CUSTOM
        self.size_var.set(f"CUSTOM ({width}x{height})")
        
        # Auto-adjust zoom based on size
        if width <= 16 or height <= 16:
            if self.canvas.zoom < 16:
                self.canvas.set_zoom(16)
                self.zoom_var.set("16x")
        elif width <= 32 or height <= 32:
            if self.canvas.zoom < 16:
                self.canvas.set_zoom(16)
                self.zoom_var.set("16x")
        elif width >= 64 or height >= 64:
            if self.canvas.zoom > 8:
                    self.canvas.set_zoom(8)
                    self.zoom_var.set("8x")
            
        # Resize layer manager and timeline
        preserve_width = min(old_width, width)
        preserve_height = min(old_height, height)
        
        self.layer_manager.resize_layers(width, height)
        self.timeline.resize_frames(width, height)
        
        # Sync canvas display with resized layer data
        self._update_canvas_from_layers()
        
        # Update display
        self._force_tkinter_canvas_update()
        
        print(f"[Custom Canvas Resize] Resized to {width}x{height}, preserved {preserve_width}x{preserve_height} pixels")
    
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
        """Handle palette change - automatically switch to Grid view"""
        self.palette.load_preset(palette_name)
        
        # Always switch to Grid view when changing palette
        self.view_mode_var.set("grid")
        
        # Update grid view with new palette
        if hasattr(self, 'grid_view') and self.grid_view:
            self.grid_view.create()
        
        # Show grid view
        self._show_view("grid")
    
    def _initialize_all_views(self):
        """Initialize all palette views once at startup (OPTIMIZED)"""
        # Initialize grid view
        if hasattr(self, 'grid_view') and self.grid_view:
            self.grid_view.create()
        
        # Initialize primary view
        if hasattr(self, 'primary_view') and self.primary_view:
            self.primary_view.create()
        
        # Initialize wheel view (ColorWheel creates UI in __init__, no create() method needed)
        # Color wheel is already created during initialization
        
        # Initialize saved view
        if hasattr(self, 'saved_view') and self.saved_view:
            self.saved_view.create()
        
        # Initialize constants view
        if hasattr(self, 'constants_view') and self.constants_view:
            self.constants_view.create()
        
        # Set color display frame to the left panel for palette views
        self.color_display_frame = self.left_panel
    
    def _show_view(self, mode: str):
        """Show specific view by toggling visibility (INSTANT)"""
        # Clear existing palette content
        if hasattr(self, 'palette_content_frame') and self.palette_content_frame:
            for widget in self.palette_content_frame.winfo_children():
                widget.destroy()
        
        # Show requested view
        if mode == "grid" and hasattr(self, 'grid_view') and self.grid_view:
            self.grid_view.create()
        elif mode == "primary" and hasattr(self, 'primary_view') and self.primary_view:
            self.primary_view.create()
        elif mode == "wheel" and hasattr(self, 'color_wheel') and self.color_wheel:
            # Recreate color wheel since it was destroyed when clearing the frame
            from src.ui.color_wheel import ColorWheel
            self.color_wheel = ColorWheel(self.palette_content_frame, theme=self.theme_manager.current_theme)
            self.color_wheel.on_color_changed = self._on_color_wheel_changed
            self.color_wheel.on_save_custom_color = self._save_custom_color
            self.color_wheel.on_remove_custom_color = self._remove_custom_color
        elif mode == "constants" and hasattr(self, 'constants_view') and self.constants_view:
            self.constants_view.create()
        elif mode == "saved" and hasattr(self, 'saved_view') and self.saved_view:
            self.saved_view.create()
            # Update button states in case colors changed
            if hasattr(self, '_saved_view_created') and self._saved_view_created:
                self._update_saved_color_buttons()
    
    def _on_view_mode_change(self):
        """Handle view mode change - now instant!"""
        mode = self.view_mode_var.get()
        self._show_view(mode)
    
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
    
    def _create_saved_colors_view(self):
        """Create saved colors view with empty slots and export button (OPTIMIZED)"""
        # Check if view already exists - just update buttons instead of recreating
        if hasattr(self, '_saved_view_created') and self._saved_view_created:
            self._update_saved_color_buttons()
            return
        
        # Clear existing widgets
        for widget in self.color_display_frame.winfo_children():
            widget.destroy()
        
        # Title
        title_label = ctk.CTkLabel(
            self.color_display_frame,
            text="Saved Colors",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.pack(pady=(5, 2))
        
        # Instructions
        info_label = ctk.CTkLabel(
            self.color_display_frame,
            text="Click empty slot to save current color",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        info_label.pack(pady=(0, 5))
        
        # Grid for saved colors
        grid_frame = ctk.CTkFrame(self.color_display_frame)
        grid_frame.pack(padx=10, pady=5)
        
        # Configure grid - 4 columns x 6 rows = 24 slots
        for col in range(4):
            grid_frame.grid_columnconfigure(col, weight=1)
        
        # Create 24 color slots (create once, update later)
        self.saved_color_buttons = []
        for idx in range(24):
            row = idx // 4
            col = idx % 4
            
            # Create button (will be configured in _update_saved_color_buttons)
            btn = ctk.CTkButton(
                grid_frame,
                text="+",
                width=50,
                height=50,
                fg_color="transparent",
                hover_color="#3a3a3a",
                border_width=2,
                border_color="gray",
                corner_radius=3
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            self.saved_color_buttons.append(btn)
        
        # Export button
        export_btn = ctk.CTkButton(
            self.color_display_frame,
            text="Export Saved Colors",
            height=32,
            fg_color="#1f6aa5",
            hover_color="#1f5a95",
            command=self._export_saved_colors
        )
        export_btn.pack(fill="x", padx=10, pady=(5, 2))
        
        # Import button
        import_btn = ctk.CTkButton(
            self.color_display_frame,
            text="Import Saved Colors",
            height=32,
            fg_color="#4a4a4a",
            hover_color="#5a5a5a",
            command=self._import_saved_colors
        )
        import_btn.pack(fill="x", padx=10, pady=2)
        
        # Clear all button
        clear_btn = ctk.CTkButton(
            self.color_display_frame,
            text="Clear All Slots",
            height=32,
            fg_color="red",
            hover_color="#cc0000",
            command=self._clear_all_saved_colors
        )
        clear_btn.pack(fill="x", padx=10, pady=2)
        
        # Mark view as created
        self._saved_view_created = True
        
        # Now update button states
        self._update_saved_color_buttons()
    
    def _update_saved_color_buttons(self):
        """Update saved color button states without recreating them (FAST)"""
        if not hasattr(self, 'saved_color_buttons'):
            return
        
        for idx, btn in enumerate(self.saved_color_buttons):
            saved_color = self.saved_colors.get_color(idx)
            
            if saved_color:
                # Slot has a color - configure as filled
                r, g, b, a = saved_color
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                btn.configure(
                    text="",
                    fg_color=hex_color,
                    hover_color=hex_color,
                    command=lambda i=idx: self._on_saved_color_click(i)
                )
            else:
                # Empty slot - configure as empty
                btn.configure(
                    text="+",
                    fg_color="transparent",
                    hover_color="#3a3a3a",
                    command=lambda i=idx: self._on_saved_slot_click(i)
                )
    
    def _on_saved_slot_click(self, slot_index: int):
        """Handle click on empty saved color slot - save current color"""
        # Get current color from appropriate source
        # If color wheel view is active, get from wheel; otherwise from palette
        if (hasattr(self, 'color_wheel') and self.color_wheel and 
            self.view_mode_var.get() == "wheel"):
            rgb_color = self.color_wheel.get_color()
            current_color = (rgb_color[0], rgb_color[1], rgb_color[2], 255)
        else:
            current_color = self.palette.get_primary_color()
        
        # Save to slot
        self.saved_colors.set_color(slot_index, current_color)
        
        # Fast refresh - just update button states
        self._update_saved_color_buttons()
        
        print(f"[SAVED] Color {current_color} saved to slot {slot_index}")
    
    def _on_saved_color_click(self, slot_index: int):
        """Handle click on filled saved color slot - load color"""
        saved_color = self.saved_colors.get_color(slot_index)
        if saved_color:
            # Set as primary color
            self.palette.set_primary_color_by_rgba(saved_color)
            self._update_pixel_display()
            print(f"[SAVED] Loaded color {saved_color} from slot {slot_index}")
    
    def _export_saved_colors(self):
        """Export saved colors to a file"""
        from tkinter import filedialog
        filepath = filedialog.asksaveasfilename(
            title="Export Saved Colors",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            if self.saved_colors.export_to_file(filepath):
                print(f"[EXPORT] Saved colors exported to: {filepath}")
            else:
                print("[EXPORT] Failed to export saved colors")
    
    def _import_saved_colors(self):
        """Import saved colors from a file"""
        from tkinter import filedialog
        filepath = filedialog.askopenfilename(
            title="Import Saved Colors",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            if self.saved_colors.import_from_file(filepath):
                self._update_saved_color_buttons()  # Fast refresh
                print(f"[IMPORT] Saved colors imported from: {filepath}")
            else:
                print("[IMPORT] Failed to import saved colors")
    
    def _show_downsize_warning(self, old_width, old_height, new_width, new_height):
        """Show custom styled downsize warning dialog"""
        # Create custom warning dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Canvas Downsize Warning")
        dialog.geometry("500x280")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog on the main window
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (500 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (280 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Icon and title frame
        header_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        header_frame.pack(pady=20, padx=20, fill="x")
        
        # Large warning icon (⚠️ emoji)
        icon_label = ctk.CTkLabel(
            header_frame,
            text="⚠️",
            font=ctk.CTkFont(size=48)
        )
        icon_label.pack(side="left", padx=(10, 20))
        
        # Title text
        title_label = ctk.CTkLabel(
            header_frame,
            text="DOWNSIZING WARNING",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ff9800"  # Orange warning color
        )
        title_label.pack(side="left", anchor="w")
        
        # Warning details
        details_text = f"Current size: {old_width}x{old_height}\n"
        details_text += f"New size: {new_width}x{new_height}\n\n"
        details_text += f"This will PERMANENTLY DELETE pixels outside the {new_width}x{new_height} region!\n"
        details_text += "Lost pixels CANNOT be recovered!"
        
        message_label = ctk.CTkLabel(
            dialog,
            text=details_text,
            font=ctk.CTkFont(size=14),
            text_color="#e0e0e0",
            justify="left"
        )
        message_label.pack(pady=(0, 10), padx=20)
        
        # Continue question
        question_label = ctk.CTkLabel(
            dialog,
            text="Continue with resize?",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff"
        )
        question_label.pack(pady=(0, 20), padx=20)
        
        # Button frame
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        # Result storage
        result = [False]
        
        def on_yes():
            result[0] = True
            dialog.destroy()
        
        def on_no():
            result[0] = False
            dialog.destroy()
        
        # No button (safe option)
        no_btn = ctk.CTkButton(
            button_frame,
            text="No",
            width=140,
            height=40,
            fg_color="#4a4a4a",
            hover_color="#5a5a5a",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=on_no
        )
        no_btn.pack(side="right", padx=5)
        
        # Yes button (destructive action)
        yes_btn = ctk.CTkButton(
            button_frame,
            text="Yes",
            width=140,
            height=40,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=on_yes
        )
        yes_btn.pack(side="right", padx=5)
        
        # Wait for dialog to close
        self.root.wait_window(dialog)
        
        # Return result
        return result[0]
    
    def _clear_all_saved_colors(self):
        """Clear all saved color slots with confirmation"""
        # Create custom confirmation dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Clear All Slots")
        dialog.geometry("450x220")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog on the main window
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (450 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (220 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Icon and title frame
        header_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        header_frame.pack(pady=20, padx=20, fill="x")
        
        # Large colorful icon (🎨 emoji)
        icon_label = ctk.CTkLabel(
            header_frame,
            text="🎨",
            font=ctk.CTkFont(size=48)
        )
        icon_label.pack(side="left", padx=(10, 20))
        
        # Title text
        title_label = ctk.CTkLabel(
            header_frame,
            text="Clear All Slots",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", anchor="w")
        
        # Warning message
        message_label = ctk.CTkLabel(
            dialog,
            text="Are you sure you want to clear all saved colors?\nThis cannot be undone.",
            font=ctk.CTkFont(size=14),
            text_color="#e0e0e0"
        )
        message_label.pack(pady=(0, 25), padx=20)
        
        # Button frame
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        # Result storage
        result = [False]
        
        def on_yes():
            result[0] = True
            dialog.destroy()
        
        def on_no():
            result[0] = False
            dialog.destroy()
        
        # No button (cancel)
        no_btn = ctk.CTkButton(
            button_frame,
            text="No",
            width=140,
            height=40,
            fg_color="#4a4a4a",
            hover_color="#5a5a5a",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=on_no
        )
        no_btn.pack(side="right", padx=5)
        
        # Yes button (destructive action)
        yes_btn = ctk.CTkButton(
            button_frame,
            text="Yes",
            width=140,
            height=40,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=on_yes
        )
        yes_btn.pack(side="right", padx=5)
        
        # Wait for dialog to close
        self.root.wait_window(dialog)
        
        # Process result
        if result[0]:
            self.saved_colors.clear_all()
            self._update_saved_color_buttons()  # Fast refresh
    
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
        else:
            # Color not in current palette, switch to color wheel and set the color
            # Use optimized view switching (don't recreate wheel!)
            self.view_mode_var.set("wheel")
            self._show_view("wheel")
            
            # Set the color on the existing color wheel
            if hasattr(self, 'color_wheel') and self.color_wheel:
                self.color_wheel.set_color(rgb_color[0], rgb_color[1], rgb_color[2])
    
    def _create_color_wheel(self):
        """Create color wheel view"""
        # Clear existing widgets
        for widget in self.color_display_frame.winfo_children():
            widget.destroy()
        
        # Import and create color wheel
        from src.ui.color_wheel import ColorWheel
        self.color_wheel = ColorWheel(self.color_display_frame, theme=self.theme_manager.current_theme)
        self.color_wheel.on_color_changed = self._on_color_wheel_changed
        
        # Connect color wheel callbacks to custom colors management
        self.color_wheel.on_save_custom_color = self._save_custom_color
        self.color_wheel.on_remove_custom_color = self._remove_custom_color
        
        # Update custom colors grid with existing colors
        self._update_custom_colors_display()
    
    def _on_color_wheel_changed(self, rgb_color):
        """Handle color wheel color change"""
        # Convert RGB to RGBA and set as primary color
        if len(rgb_color) == 3:
            rgba_color = (rgb_color[0], rgb_color[1], rgb_color[2], 255)
        else:
            rgba_color = rgb_color
        
        # Set the color as the primary color for the brush
        self.palette.set_primary_color_by_rgba(rgba_color)
        
        # Update color display in UI
        self._update_pixel_display()
        
        # Auto-switch to brush tool for immediate painting
        if self.current_tool != "brush":
            self._select_tool("brush")
    
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
    
    def _open_texture_panel(self):
        """Open texture panel with clickable textures"""
        # Create texture panel window
        texture_window = ctk.CTkToplevel(self.root)
        texture_window.title("Texture Library")
        texture_window.geometry("400x300")
        texture_window.resizable(False, False)
        texture_window.transient(self.root)
        texture_window.grab_set()  # Modal
        
        # Center on main window
        texture_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (400 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (300 // 2)
        texture_window.geometry(f"+{x}+{y}")
        
        # Header
        header_frame = ctk.CTkFrame(texture_window, fg_color="transparent")
        header_frame.pack(pady=15, padx=20, fill="x")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎨 Texture Library",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Select a texture to apply to canvas",
            font=ctk.CTkFont(size=12),
            text_color="#a0a0a0"
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Textures grid
        content_frame = ctk.CTkFrame(texture_window)
        content_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        
        # Get all textures
        textures = self.texture_library.get_all_textures()
        
        # Create texture buttons
        for idx, (name, texture_data) in enumerate(textures.items()):
            self._create_texture_button(content_frame, name, texture_data, texture_window, idx)
    
    def _create_texture_button(self, parent, name, texture_data, window, index):
        """Create a clickable texture preview button"""
        # Container for texture button
        texture_frame = ctk.CTkFrame(parent, fg_color="#2a2a2a", corner_radius=8)
        texture_frame.pack(pady=10, padx=10, fill="x")
        
        # Create canvas to render texture preview
        preview_size = 64  # 8x8 texture * 8 scale = 64px
        preview_canvas = tk.Canvas(
            texture_frame,
            width=preview_size,
            height=preview_size,
            bg="#1a1a1a",
            highlightthickness=0
        )
        preview_canvas.pack(side="left", padx=10, pady=10)
        
        # Render texture on canvas (scaled up)
        scale = 8
        for y in range(texture_data.shape[0]):
            for x in range(texture_data.shape[1]):
                color = texture_data[y, x]
                hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                preview_canvas.create_rectangle(
                    x * scale, y * scale,
                    (x + 1) * scale, (y + 1) * scale,
                    fill=hex_color,
                    outline=""
                )
        
        # Texture info
        info_frame = ctk.CTkFrame(texture_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=name,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        dims = f"{texture_data.shape[1]}×{texture_data.shape[0]} pixels"
        dims_label = ctk.CTkLabel(
            info_frame,
            text=dims,
            font=ctk.CTkFont(size=11),
            text_color="#a0a0a0",
            anchor="w"
        )
        dims_label.pack(anchor="w", pady=(2, 0))
        
        # Select button
        select_btn = ctk.CTkButton(
            info_frame,
            text="Select",
            width=80,
            height=28,
            fg_color="#4a9eff",
            hover_color="#3a8eef",
            command=lambda: self._select_texture(texture_data, window)
        )
        select_btn.pack(anchor="w", pady=(8, 0))
        
        # Make entire frame clickable
        texture_frame.bind("<Button-1>", lambda e: self._select_texture(texture_data, window))
        preview_canvas.bind("<Button-1>", lambda e: self._select_texture(texture_data, window))
    
    def _select_texture(self, texture_data, window):
        """Select a texture and activate texture tool"""
        # Set texture on tool
        self.tools["texture"].set_texture(texture_data)
        
        # Switch to texture tool
        self._select_tool("texture")
        
        # Close texture panel
        window.destroy()
        
        print(f"[TEXTURE] Selected {texture_data.shape[1]}x{texture_data.shape[0]} texture")
    
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
            self.grid_overlay_button.configure(fg_color=self.theme_manager.get_current_theme().button_normal)
    
    def _on_theme_selected(self, theme_name: str):
        """Handle theme selection from dropdown"""
        self.theme_manager.set_theme(theme_name)
        print(f"[OK] Theme changed to: {theme_name}")
    
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
        new_btn = ctk.CTkButton(file_menu, text="New Project", command=lambda: [self.file_ops.new_project(), file_menu.destroy()])
        new_btn.pack(pady=5, padx=10, fill="x")
        
        open_btn = ctk.CTkButton(file_menu, text="Open Project", command=lambda: [self.file_ops.open_project(), file_menu.destroy()])
        open_btn.pack(pady=5, padx=10, fill="x")
        
        import_png_btn = ctk.CTkButton(file_menu, text="Import PNG", command=lambda: [self.file_ops.import_png(), file_menu.destroy()])
        import_png_btn.pack(pady=5, padx=10, fill="x")
        
        save_btn = ctk.CTkButton(file_menu, text="Save Project", command=lambda: [self.file_ops.save_project(), file_menu.destroy()])
        save_btn.pack(pady=5, padx=10, fill="x")
        
        save_as_btn = ctk.CTkButton(file_menu, text="Save As...", command=lambda: [self.file_ops.save_project_as(), file_menu.destroy()])
        save_as_btn.pack(pady=5, padx=10, fill="x")
        
        # Separator
        sep = ctk.CTkFrame(file_menu, height=2)
        sep.pack(fill="x", padx=10, pady=10)
        
        # Export options
        export_png_btn = ctk.CTkButton(file_menu, text="Export as PNG", command=lambda: [self.file_ops.export_png(), file_menu.destroy()])
        export_png_btn.pack(pady=5, padx=10, fill="x")
        
        export_gif_btn = ctk.CTkButton(file_menu, text="Export as GIF", command=lambda: [self.file_ops.export_gif(), file_menu.destroy()])
        export_gif_btn.pack(pady=5, padx=10, fill="x")
        
        export_spritesheet_btn = ctk.CTkButton(file_menu, text="Export Sprite Sheet", command=lambda: [self.file_ops.export_spritesheet(), file_menu.destroy()])
        export_spritesheet_btn.pack(pady=5, padx=10, fill="x")
        
        # Separator
        sep2 = ctk.CTkFrame(file_menu, height=2)
        sep2.pack(fill="x", padx=10, pady=10)
        
        # Templates
        template_btn = ctk.CTkButton(file_menu, text="Load Template", command=lambda: [self.file_ops.show_templates(), file_menu.destroy()])
        template_btn.pack(pady=5, padx=10, fill="x")
        
        # Close button
        close_btn = ctk.CTkButton(file_menu, text="Close", command=file_menu.destroy)
        close_btn.pack(pady=10, padx=10, fill="x")
    

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
        
        # Check if pixel is fully transparent (empty/not drawn)
        if sampled_color[3] == 0:  # Alpha channel is 0
            # Don't sample transparent pixels - they're empty!
            return
        
        # Convert to RGB (remove alpha for comparison)
        rgb_color = sampled_color[:3]
        
        if button == 1:  # Left click - set primary color
            self._set_color_from_eyedropper(rgb_color, is_primary=True)
            # Auto-switch back to brush tool for immediate painting
            self._select_tool("brush")
        elif button == 3:  # Right click - set secondary color
            self._set_color_from_eyedropper(rgb_color, is_primary=False)
            # Auto-switch back to brush tool for immediate painting
            self._select_tool("brush")
    
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
        
        # ALWAYS update color wheel to show the sampled color (improves flow)
        if hasattr(self, 'color_wheel') and self.color_wheel:
            self.color_wheel.set_color(rgb_color[0], rgb_color[1], rgb_color[2])
        
        if found_in_palette:
            # Color found in palette, update grid UI (stays in current view)
            self._update_color_grid_selection()
        else:
            # Color not in palette, switch to color wheel view
            self.view_mode_var.set("wheel")
            self._show_view("wheel")
    
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
    
    def _draw_brush_preview(self, canvas_x: int, canvas_y: int):
        """Draw live preview of brush tool on tkinter canvas"""
        # Clear any existing preview
        self.drawing_canvas.delete("brush_preview")
        
        # Get canvas dimensions and offsets
        canvas_width = self.drawing_canvas.winfo_width()
        canvas_height = self.drawing_canvas.winfo_height()
        canvas_pixel_width = self.canvas.width * self.canvas.zoom
        canvas_pixel_height = self.canvas.height * self.canvas.zoom
        x_offset = (canvas_width - canvas_pixel_width) // 2 + self.pan_offset_x
        y_offset = (canvas_height - canvas_pixel_height) // 2 + self.pan_offset_y
        
        # Calculate offset for centering (like _draw_brush_at)
        offset = self.brush_size // 2
        
        # Draw preview for each pixel in the brush
        for dy in range(self.brush_size):
            for dx in range(self.brush_size):
                px = canvas_x - offset + dx
                py = canvas_y - offset + dy
                
                # Check bounds
                if 0 <= px < self.canvas.width and 0 <= py < self.canvas.height:
                    screen_x = x_offset + (px * self.canvas.zoom)
                    screen_y = y_offset + (py * self.canvas.zoom)
                    
                    # Draw semi-transparent preview with current color
                    r, g, b, a = self.palette.get_primary_color()
                    color_hex = f"#{r:02x}{g:02x}{b:02x}"
                    
                    self.drawing_canvas.create_rectangle(
                        screen_x, screen_y,
                        screen_x + self.canvas.zoom, screen_y + self.canvas.zoom,
                        fill=color_hex, outline=color_hex, stipple="gray50",
                        tags="brush_preview"
                    )
        
        # Draw outline around brush area
        screen_x1 = x_offset + ((canvas_x - offset) * self.canvas.zoom)
        screen_y1 = y_offset + ((canvas_y - offset) * self.canvas.zoom)
        screen_x2 = x_offset + ((canvas_x - offset + self.brush_size) * self.canvas.zoom)
        screen_y2 = y_offset + ((canvas_y - offset + self.brush_size) * self.canvas.zoom)
        
        self.drawing_canvas.create_rectangle(
            screen_x1, screen_y1, screen_x2, screen_y2,
            outline="#ffffff", width=2, dash=(4, 4),
            tags="brush_preview"
        )
    
    def _draw_eraser_preview(self, canvas_x: int, canvas_y: int):
        """Draw live preview of eraser tool on tkinter canvas"""
        # Clear any existing preview
        self.drawing_canvas.delete("eraser_preview")
        
        # Get canvas dimensions and offsets
        canvas_width = self.drawing_canvas.winfo_width()
        canvas_height = self.drawing_canvas.winfo_height()
        canvas_pixel_width = self.canvas.width * self.canvas.zoom
        canvas_pixel_height = self.canvas.height * self.canvas.zoom
        x_offset = (canvas_width - canvas_pixel_width) // 2 + self.pan_offset_x
        y_offset = (canvas_height - canvas_pixel_height) // 2 + self.pan_offset_y
        
        # Calculate offset for centering (like _erase_at)
        offset = self.eraser_size // 2
        
        # Draw preview for each pixel in the eraser (show as red X pattern)
        for dy in range(self.eraser_size):
            for dx in range(self.eraser_size):
                px = canvas_x - offset + dx
                py = canvas_y - offset + dy
                
                # Check bounds
                if 0 <= px < self.canvas.width and 0 <= py < self.canvas.height:
                    screen_x = x_offset + (px * self.canvas.zoom)
                    screen_y = y_offset + (py * self.canvas.zoom)
                    
                    # Draw semi-transparent red square to indicate erasing
                    self.drawing_canvas.create_rectangle(
                        screen_x, screen_y,
                        screen_x + self.canvas.zoom, screen_y + self.canvas.zoom,
                        fill="#ff0000", outline="#ff0000", stipple="gray50",
                        tags="eraser_preview"
                    )
        
        # Draw outline around eraser area
        screen_x1 = x_offset + ((canvas_x - offset) * self.canvas.zoom)
        screen_y1 = y_offset + ((canvas_y - offset) * self.canvas.zoom)
        screen_x2 = x_offset + ((canvas_x - offset + self.eraser_size) * self.canvas.zoom)
        screen_y2 = y_offset + ((canvas_y - offset + self.eraser_size) * self.canvas.zoom)
        
        self.drawing_canvas.create_rectangle(
            screen_x1, screen_y1, screen_x2, screen_y2,
            outline="#ff0000", width=2, dash=(4, 4),
            tags="eraser_preview"
        )
    
    def _draw_texture_preview(self, tool, canvas_x: int, canvas_y: int):
        """Draw live preview of texture tool on tkinter canvas"""
        # Clear any existing preview
        self.drawing_canvas.delete("texture_preview")
        
        # Get texture data
        texture_data = tool.get_preview_texture()
        if texture_data is None:
            return
        
        # Get canvas dimensions and offsets
        canvas_width = self.drawing_canvas.winfo_width()
        canvas_height = self.drawing_canvas.winfo_height()
        canvas_pixel_width = self.canvas.width * self.canvas.zoom
        canvas_pixel_height = self.canvas.height * self.canvas.zoom
        x_offset = (canvas_width - canvas_pixel_width) // 2 + self.pan_offset_x
        y_offset = (canvas_height - canvas_pixel_height) // 2 + self.pan_offset_y
        
        # Get texture dimensions
        tex_height, tex_width = texture_data.shape[0], texture_data.shape[1]
        
        # Draw each pixel of the texture
        for ty in range(tex_height):
            for tx in range(tex_width):
                pixel_color = texture_data[ty, tx]
                if pixel_color[3] > 0:  # Only draw non-transparent pixels
                    # Calculate screen position
                    px = canvas_x + tx
                    py = canvas_y + ty
                    
                    # Check bounds
                    if 0 <= px < self.canvas.width and 0 <= py < self.canvas.height:
                        screen_x = x_offset + (px * self.canvas.zoom)
                        screen_y = y_offset + (py * self.canvas.zoom)
                        
                        # Convert color to hex
                        color_hex = f'#{pixel_color[0]:02x}{pixel_color[1]:02x}{pixel_color[2]:02x}'
                        
                        # Draw pixel rectangle with semi-transparency effect
                        self.drawing_canvas.create_rectangle(
                            screen_x, screen_y,
                            screen_x + self.canvas.zoom, screen_y + self.canvas.zoom,
                            fill=color_hex, outline=color_hex, stipple="gray50",
                            tags="texture_preview"
                        )
        
        # Draw outline around texture area
        screen_x1 = x_offset + (canvas_x * self.canvas.zoom)
        screen_y1 = y_offset + (canvas_y * self.canvas.zoom)
        screen_x2 = x_offset + ((canvas_x + tex_width) * self.canvas.zoom)
        screen_y2 = y_offset + ((canvas_y + tex_height) * self.canvas.zoom)
        
        self.drawing_canvas.create_rectangle(
            screen_x1, screen_y1, screen_x2, screen_y2,
            outline="#ffffff", width=2, dash=(4, 4),
            tags="texture_preview"
        )

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
                self.canvas_renderer.draw_scale_handle(screen_x1, screen_y1, handle_size, "yellow")  # Top-left
                self.canvas_renderer.draw_scale_handle(screen_x2, screen_y1, handle_size, "yellow")  # Top-right
                self.canvas_renderer.draw_scale_handle(screen_x1, screen_y2, handle_size, "yellow")  # Bottom-left
                self.canvas_renderer.draw_scale_handle(screen_x2, screen_y2, handle_size, "yellow")  # Bottom-right
                
                # Draw edge handles
                mid_x = (screen_x1 + screen_x2) / 2
                mid_y = (screen_y1 + screen_y2) / 2
                self.canvas_renderer.draw_scale_handle(mid_x, screen_y1, handle_size, "orange")  # Top
                self.canvas_renderer.draw_scale_handle(mid_x, screen_y2, handle_size, "orange")  # Bottom
                self.canvas_renderer.draw_scale_handle(screen_x1, mid_y, handle_size, "orange")  # Left
                self.canvas_renderer.draw_scale_handle(screen_x2, mid_y, handle_size, "orange")  # Right
        
        # Draw move preview if actively moving selection
        move_tool = self.tools.get("move")
        if (move_tool and move_tool.is_moving and selection_tool and 
            selection_tool.selected_pixels is not None and selection_tool.selection_rect):
            left, top, width, height = selection_tool.selection_rect
            zoom = self.canvas.zoom
            
            # Draw the selected pixels at the current position
            for py in range(height):
                for px in range(width):
                    if (py < selection_tool.selected_pixels.shape[0] and 
                        px < selection_tool.selected_pixels.shape[1]):
                        pixel_color = tuple(selection_tool.selected_pixels[py, px])
                        # Only draw non-transparent pixels for preview
                        if pixel_color[3] > 0:
                            screen_x = x_offset + ((left + px) * zoom)
                            screen_y = y_offset + ((top + py) * zoom)
                            
                            # Convert RGBA to hex for tkinter
                            hex_color = f"#{pixel_color[0]:02x}{pixel_color[1]:02x}{pixel_color[2]:02x}"
                            
                            # Draw pixel
                            self.drawing_canvas.create_rectangle(
                                screen_x, screen_y,
                                screen_x + zoom, screen_y + zoom,
                                fill=hex_color, outline="", tags="move_preview"
                            )
        
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
    
    def _calculate_optimal_panel_widths(self):
        """Calculate optimal panel widths based on screen resolution"""
        try:
            # Get screen dimensions
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            print(f"[Panel Sizing] Screen resolution: {screen_width}x{screen_height}")
            
            # Calculate optimal panel widths based on screen size
            if screen_width <= 1366:  # Small laptop screens (1366x768)
                left_width, right_width = 280, 260
                print(f"[Panel Sizing] Small screen detected - using compact panels: {left_width}x{right_width}")
            elif screen_width <= 1920:  # Standard desktop (1920x1080)
                left_width, right_width = 350, 320
                print(f"[Panel Sizing] Standard desktop detected - using balanced panels: {left_width}x{right_width}")
            elif screen_width <= 2560:  # Large desktop (2560x1440)
                left_width, right_width = 400, 380
                print(f"[Panel Sizing] Large desktop detected - using spacious panels: {left_width}x{right_width}")
            else:  # Ultra-wide or 4K (2560+)
                left_width, right_width = 450, 420
                print(f"[Panel Sizing] Ultra-wide/4K detected - using wide panels: {left_width}x{right_width}")
            
            # Ensure minimum widths
            left_width = max(left_width, 200)
            right_width = max(right_width, 200)
            
            # Calculate total panel usage percentage
            total_panel_width = left_width + right_width
            panel_percentage = (total_panel_width / screen_width) * 100
            
            print(f"[Panel Sizing] Panel usage: {total_panel_width}px ({panel_percentage:.1f}% of screen)")
            print(f"[Panel Sizing] Canvas space: {screen_width - total_panel_width}px")
            
            return left_width, right_width
            
        except Exception as e:
            print(f"[Panel Sizing] Error calculating panel widths: {e}")
            # Fallback to reasonable defaults
            return 350, 320
    
    def _save_window_state(self):
        """Save current window and panel state to config file"""
        try:
            import json
            import os
            
            # Get current state
            state = {
                'window_geometry': self.root.geometry(),
                'left_panel_width': self.left_container.winfo_width(),
                'right_panel_width': self.right_container.winfo_width(),
                'screen_width': self.root.winfo_screenwidth(),
                'screen_height': self.root.winfo_screenheight()
            }
            
            # Save to user config directory
            config_dir = os.path.join(os.path.expanduser("~"), ".pixelperfect")
            os.makedirs(config_dir, exist_ok=True)
            config_file = os.path.join(config_dir, "window_state.json")
            
            with open(config_file, 'w') as f:
                json.dump(state, f, indent=2)
                
            print(f"[Window State] Saved to: {config_file}")
            
        except Exception as e:
            print(f"[Window State] Error saving state: {e}")
    
    def _restore_window_state(self):
        """Restore saved window state on startup"""
        try:
            import json
            import os
            
            config_dir = os.path.join(os.path.expanduser("~"), ".pixelperfect")
            config_file = os.path.join(config_dir, "window_state.json")
            
            if not os.path.exists(config_file):
                print("[Window State] No saved state found, using defaults")
                return False
            
            with open(config_file, 'r') as f:
                state = json.load(f)
            
            # Check if screen resolution matches (don't restore if resolution changed)
            current_screen_width = self.root.winfo_screenwidth()
            current_screen_height = self.root.winfo_screenheight()
            
            if (state.get('screen_width') != current_screen_width or 
                state.get('screen_height') != current_screen_height):
                print(f"[Window State] Screen resolution changed, recalculating panel sizes")
                return False
            
            # Restore window geometry
            if 'window_geometry' in state:
                self.root.geometry(state['window_geometry'])
                print(f"[Window State] Restored window geometry: {state['window_geometry']}")
            
            # Restore panel widths
            if 'left_panel_width' in state and 'right_panel_width' in state:
                self.left_panel_width = state['left_panel_width']
                self.right_panel_width = state['right_panel_width']
                print(f"[Window State] Restored panel widths: {self.left_panel_width}x{self.right_panel_width}")
                return True
            
        except Exception as e:
            print(f"[Window State] Error restoring state: {e}")
        
        return False
    
    def _on_window_close(self):
        """Handle window close event - save state before closing"""
        print("[Window State] Application closing, saving window state...")
        self._save_window_state()
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
