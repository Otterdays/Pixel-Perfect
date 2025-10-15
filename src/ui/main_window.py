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
from ui.dialog_manager import DialogManager
from ui.selection_manager import SelectionManager

class MainWindow:
    """Main application window"""
    
    def __init__(self):
        # Set up CustomTkinter theme
        ctk.set_appearance_mode("dark")
        # Note: Removed ctk.set_default_color_theme("blue") to allow custom theme colors
        
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
        self.undo_manager.on_state_changed = self._update_undo_redo_buttons
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
        
        # Initialize dialog manager (needed before UI creation)
        self.dialog_mgr = DialogManager(
            self.root, self.canvas, self.texture_library, self.tools
        )
        
        # Brush size (1x1, 2x2, 3x3)
        self.brush_size = 1
        self.brush_drawing = False
        
        # Eraser size (1x1, 2x2, 3x3)
        self.eraser_size = 1
        
        
        # UI state
        self.is_drawing = False
        self.last_mouse_pos = (0, 0)
        self._last_drawn_pixel = None  # Track last drawn pixel for efficient updates
        self._updating_display = False  # Flag to prevent recursion
        
        # Copy preview position (EventDispatcher needs this)
        self.copy_preview_pos = None  # Mouse position for copy preview
        
        # Scale state for EventDispatcher (points to selection_mgr)
        self.scale_start_pos = None
        
        # Pan state
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        
        # Grid overlay state
        self.grid_overlay = False
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        # Initialize theme dialog manager
        self.theme_dialog_manager = ThemeDialogManager(self)
        
        # Initialize selection manager (needed before tool connections)
        self.selection_mgr = SelectionManager(
            self.canvas, self.layer_manager, self.tools, self.theme_manager
        )
        
        # Connect selection and move tools (after SelectionManager is initialized)
        self.tools["move"].set_selection_tool(self.tools["selection"])
        
        # Set up auto-switch to move tool after selection
        self.tools["selection"].on_selection_complete = self.selection_mgr.on_selection_complete
        
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
            fg_color=self.theme_manager.get_current_theme().bg_secondary,
            scrollbar_button_color=self.theme_manager.get_current_theme().scrollbar_button_color,
            scrollbar_button_hover_color=self.theme_manager.get_current_theme().scrollbar_button_hover_color
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
            fg_color="transparent",
            scrollbar_button_color=self.theme_manager.get_current_theme().scrollbar_button_color,
            scrollbar_button_hover_color=self.theme_manager.get_current_theme().scrollbar_button_hover_color
        )
        self.right_panel.pack(side="right", fill="both", expand=True)
        
        # Create panels using UIBuilder
        selection_buttons = self.ui_builder.create_tool_panel(self.left_panel, self.tool_buttons, self._get_ui_callbacks())
        self.tool_frame = selection_buttons['tool_frame']
        
        # Assign selection button references
        self.mirror_btn = selection_buttons['mirror_btn']
        self.rotate_btn = selection_buttons['rotate_btn']
        self.copy_btn = selection_buttons['copy_btn']
        self.scale_btn = selection_buttons['scale_btn']
        
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
        self.file_ops.force_canvas_update_callback = self.canvas_renderer.force_canvas_update
        self.file_ops.update_canvas_from_layers_callback = self._update_canvas_from_layers
        self.file_ops.clear_selection_and_reset_tools_callback = self._clear_selection_and_reset_tools
        
        # Set dialog manager callback (dialog_mgr initialized earlier)
        self.dialog_mgr.select_tool_callback = self._select_tool
        
        # Set selection manager callbacks and widget references
        self.selection_mgr.update_canvas_callback = self._update_canvas_from_layers
        self.selection_mgr.update_display_callback = self.canvas_renderer.update_pixel_display
        self.selection_mgr.select_tool_callback = self._select_tool
        self.selection_mgr.update_tool_selection_callback = self._update_tool_selection
        self.selection_mgr.get_drawing_layer_callback = self._get_drawing_layer
        self.selection_mgr.drawing_canvas = self.drawing_canvas
        self.selection_mgr.scale_btn = self.scale_btn
        self.selection_mgr.tool_buttons = self.tool_buttons
        
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
            on_update_display=self.canvas_renderer.update_pixel_display
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
            'open_texture_panel': self.dialog_mgr.open_texture_panel,
            'mirror_selection': self.selection_mgr.mirror_selection,
            'rotate_selection': self.selection_mgr.rotate_selection,
            'copy_selection': self.selection_mgr.copy_selection,
            'scale_selection': self.selection_mgr.scale_selection,
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
        if hasattr(self, 'selection_mgr') and self.selection_mgr.is_scaling:
            self.selection_mgr.is_scaling = False
            self.selection_mgr.scale_handle = None
            self.selection_mgr.scale_original_rect = None
            self.selection_mgr.scale_true_original_rect = None
            self.selection_mgr.scale_is_dragging = False
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
                self.canvas_renderer.update_pixel_display()
                # Debug: Selection cleared - switched to different tool (removed for clean console)
        
        self.current_tool = tool_id
        
        # Update tool button appearance
        self._update_tool_selection()
        
        # Clear scale button if not in scaling mode
        if hasattr(self, 'selection_mgr') and self.selection_mgr.scale_btn and not self.selection_mgr.is_scaling:
            self.selection_mgr.scale_btn.configure(fg_color=self.theme_manager.get_current_theme().button_normal)
        
        # Update canvas cursor based on selected tool
        if hasattr(self, 'drawing_canvas') and tool_id in self.tools:
            tool = self.tools[tool_id]
            self.drawing_canvas.configure(cursor=tool.cursor)
    
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
    
    def _on_size_change(self, size_str: str):
        """Handle canvas size change - WARNING: Downsizing clips pixels!"""
        # Handle custom size dialog
        if size_str == "Custom...":
            width, height = self.dialog_mgr.open_custom_size_dialog()
            
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
                result = self.dialog_mgr.show_downsize_warning(old_width, old_height, new_width, new_height)
                
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
            self.canvas_renderer.force_canvas_update()
            
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
            result = self.dialog_mgr.show_downsize_warning(old_width, old_height, width, height)
            
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
        self.canvas_renderer.force_canvas_update()
        
        print(f"[Custom Canvas Resize] Resized to {width}x{height}, preserved {preserve_width}x{preserve_height} pixels")
    
    def _on_zoom_change(self, zoom_str: str):
        """Handle zoom level change"""
        zoom_map = {
            "0.25x": 0.25, "0.5x": 0.5, "1x": 1, "2x": 2, "4x": 4, "8x": 8, "16x": 16, "32x": 32
        }
        
        if zoom_str in zoom_map:
            self.canvas.set_zoom(zoom_map[zoom_str])
            # Update display immediately
        self.canvas_renderer.force_canvas_update()

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
            self.canvas_renderer.update_pixel_display()
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
                self._update_saved_color_buttons()
                print(f"[IMPORT] Saved colors imported from: {filepath}")
            else:
                print("[IMPORT] Failed to import saved colors")
    
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
        # Color wheel colors are NOT added to the palette grid
        # The get_current_color() method will get the color from the wheel when in wheel mode
        # This prevents colors from being added to the preset palette grid
        
        # Update color display in UI
        self.canvas_renderer.update_pixel_display()
        
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
    
        self._select_tool("texture")
        
        # Close texture panel
        window.destroy()
        
        print(f"[TEXTURE] Selected {texture_data.shape[1]}x{texture_data.shape[0]} texture")
    
    def _toggle_grid(self):
        """Toggle grid visibility"""
        self.canvas.toggle_grid()
        self._update_grid_button_text()
        self.canvas_renderer.force_canvas_update()
    
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
        self.canvas_renderer.force_canvas_update()
    
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
    
    def _clear_selection_and_reset_tools(self):
        """Clear any active selection and reset tools to brush"""
        # Clear selection if there is one
        selection_tool = self.tools.get("selection")
        if selection_tool and selection_tool.has_selection:
            selection_tool.clear_selection()
        
        # Reset tool to brush
        self._select_tool("brush")
    
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
    
    def get_current_color(self):
        """Get current color based on view mode (palette or color wheel)"""
        # If color wheel view is active, get from wheel; otherwise from palette
        if (hasattr(self, 'color_wheel') and self.color_wheel and 
            hasattr(self, 'view_mode_var') and self.view_mode_var.get() == "wheel"):
            rgb_color = self.color_wheel.get_color()
            return (rgb_color[0], rgb_color[1], rgb_color[2], 255)
        else:
            return self.palette.get_primary_color()
    
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
        # Convert to RGBA for consistency
        if len(rgb_color) == 3:
            rgba_color = (rgb_color[0], rgb_color[1], rgb_color[2], 255)
        else:
            rgba_color = rgb_color
        
        # First, try to find the color in the current palette
        found_in_current_palette = False
        for i, palette_color in enumerate(self.palette.colors):
            # Compare RGB values (ignore alpha)
            if palette_color[:3] == rgb_color:
                if is_primary:
                    self.palette.set_primary_color(i)
                else:
                    self.palette.set_secondary_color(i)
                found_in_current_palette = True
                break
        
        if found_in_current_palette:
            # Color found in current palette, switch to grid view and update selection
            self.view_mode_var.set("grid")
            self._show_view("grid")
            self._update_color_grid_selection()
        else:
            # Color not in current palette, search across ALL presets
            preset_result = self.palette.find_color_in_presets(rgba_color)
            
            if preset_result:
                # Color found in another preset!
                preset_name, color_index = preset_result
                
                # Switch to that preset
                self.palette.load_preset(preset_name)
                self.palette_var.set(preset_name)
                
                # Set the found color as primary/secondary
                if is_primary:
                    self.palette.set_primary_color(color_index)
                else:
                    self.palette.set_secondary_color(color_index)
                
                # Switch to grid view and update display
                self.view_mode_var.set("grid")
                self._show_view("grid")
                self._update_color_grid_selection()
                
                print(f"[EYEDROPPER] Found color in preset '{preset_name}', switched to it")
            else:
                # Color not found in any preset, switch to color wheel view
                self.view_mode_var.set("wheel")
                self._show_view("wheel")
                
                # Update color wheel to show the sampled color AFTER switching to wheel view
                if hasattr(self, 'color_wheel') and self.color_wheel:
                    try:
                        self.color_wheel.set_color(rgb_color[0], rgb_color[1], rgb_color[2])
                    except (AttributeError, tk.TclError):
                        # Color wheel might not be fully initialized yet, skip update
                        pass
                
                print(f"[EYEDROPPER] Color not found in any preset, switched to wheel")
    
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
                self.canvas_renderer.force_canvas_update()
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
                self.canvas_renderer.force_canvas_update()
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


    def _on_frame_changed(self):
        """Handle frame change in timeline"""
        current_frame = self.timeline.get_current_frame()
        if current_frame:
            # Update canvas with current frame pixels
            self.canvas.pixels = current_frame.pixels.copy()
            self.canvas._redraw_surface()
            # Update the tkinter display
            self.canvas_renderer.update_pixel_display()
    
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
