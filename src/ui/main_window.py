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

from core.canvas import Canvas
from core.event_dispatcher import EventDispatcher
from core.canvas_renderer import CanvasRenderer
from core.window_state_manager import WindowStateManager
from .palette_views import GridView, PrimaryView, SavedView, ConstantsView
from core.color_palette import ColorPalette
from tools.brush import BrushTool
from tools.eraser import EraserTool
from tools.spray import SprayTool
from tools.fill import FillTool
from tools.eyedropper import EyedropperTool
from tools.selection import SelectionTool, MoveTool
from tools.shapes import LineTool, RectangleTool, CircleTool
from tools.pan import PanTool
from tools.texture import TextureTool, TextureLibrary
from tools.magic_wand import MagicWandTool
from core.layer_manager import LayerManager
from core.undo_manager import UndoManager
from .layer_panel import LayerPanel
from animation.timeline import AnimationTimeline
from .timeline_panel import TimelinePanel
from .tooltip import create_tooltip
from .theme_manager import ThemeManager
from .ui_builder import UIBuilder
from .theme_dialog_manager import ThemeDialogManager
from .theme_customizer import ThemeCustomizer
from .context_menu_manager import ContextMenuManager
from .file_operations_manager import FileOperationsManager
from .dialog_manager import DialogManager
from .selection_manager import SelectionManager
from .tool_size_manager import ToolSizeManager
from .canvas_zoom_manager import CanvasZoomManager
from .grid_control_manager import GridControlManager
from .background_control_manager import BackgroundControlManager
from .notes_panel import NotesPanel
from .import_png_dialog import ImportPNGDialog
from .canvas_operations_manager import CanvasOperationsManager
from .layer_animation_manager import LayerAnimationManager
from .color_view_manager import ColorViewManager
from .loading_screen import LoadingManager
from .canvas_scrollbar import CanvasScrollbar
from .reference_panel import ReferencePanel
from .token_preview_panel import TokenPreviewPanel
from .status_bar import StatusBar, CanvasHUD

class MainWindow:
    """Main application window"""
    
    def __init__(self):
        # Set up CustomTkinter theme
        ctk.set_appearance_mode("dark")
        # Note: Removed ctk.set_default_color_theme("blue") to allow custom theme colors
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Pixel Perfect - Retro Pixel Art Editor")
        
        # Get screen dimensions and calculate appropriate window size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate window size that leaves space for taskbar
        # Most taskbars are 40-50px, so use 60px margin to be safe
        available_height = screen_height - 60
        
        # Set reasonable window size that fits above taskbar
        # Increased width to 1600px to accommodate all toolbar buttons (including Tile button)
        window_width = min(1600, screen_width - 40)  # Leave some margin on sides
        window_height = min(800, available_height)   # Increased by 150px from 650, still above taskbar
        
        # Center the window on screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2 - 30  # Slightly above center to account for taskbar
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # HIDE the window completely until loading finishes
        # This prevents any UI elements from showing before loading screen is ready
        self.root.withdraw()
        
        # Set window icon BEFORE showing anything
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
                
            else:
                # Fallback to PNG
                png_path = os.path.join(base_path, "assets", "icons", "app_icon.png")
                png_path = os.path.abspath(png_path)
                if os.path.exists(png_path):
                    icon_photo = tk.PhotoImage(file=png_path)
                    self.root.iconphoto(True, icon_photo)
        except Exception:
            pass  # Icon loading is non-critical
        
        # Initialize loading screen manager NOW - after icon but before any UI
        self.loading_manager = LoadingManager(self.root)
        
        # NOW show the window FIRST so geometry is correct
        self.root.deiconify()
        self.root.update()
        self.root.update_idletasks()
        
        # THEN start the loading screen with correct geometry
        self.loading_manager.start_loading()
        
        # Initialize core systems
        self.loading_manager.update_loading("Initializing core systems...", 15)
        self.canvas = Canvas(32, 32, zoom=16)  # Higher zoom for better grid visibility
        self.palette = ColorPalette()
        self.layer_manager = LayerManager(32, 32)
        self.undo_manager = UndoManager()
        self.undo_manager.on_state_changed = self._update_undo_redo_buttons
        self.timeline = AnimationTimeline(32, 32)
        
        # Initialize responsive panel sizing
        temp_canvas_ops = CanvasOperationsManager(self.root, self.canvas, None)
        self.left_panel_width, self.right_panel_width = temp_canvas_ops.calculate_optimal_panel_widths()
        
        # Initialize custom colors manager
        self.loading_manager.update_loading("Loading color systems...", 25)
        from src.core.custom_colors import CustomColorManager
        self.custom_colors = CustomColorManager()
        
        # Initialize saved colors manager (local user storage)
        from src.core.saved_colors import SavedColorsManager
        self.saved_colors = SavedColorsManager(max_colors=24)
        
        # Initialize recent colors manager (tracks last 16 colors used)
        from src.core.recent_colors import RecentColorsManager
        # Get save path for recent colors
        if os.name == 'nt':  # Windows
            app_data = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
            recent_colors_path = os.path.join(app_data, 'PixelPerfect', 'recent_colors.json')
        else:  # macOS/Linux
            recent_colors_path = os.path.expanduser('~/.pixelperfect/recent_colors.json')
        self.recent_colors = RecentColorsManager(save_path=recent_colors_path)
        
        # Initialize project and export managers
        from src.core.project import ProjectManager
        from src.utils.export import ExportManager
        self.project = ProjectManager()
        self.export_manager = ExportManager()
        
        # Initialize presets
        from src.utils.presets import PresetManager
        self.presets = PresetManager()
        
        # Initialize tools
        self.loading_manager.update_loading("Setting up drawing tools...", 35)
        from src.tools.edge import EdgeTool
        from src.tools.dither import DitherTool
        self.tools = {
            "brush": BrushTool(),
            "dither": DitherTool(),
            "eraser": EraserTool(),
            "spray": SprayTool(),
            "fill": FillTool(),
            "eyedropper": EyedropperTool(),
            "selection": SelectionTool(),
            "magic_wand": MagicWandTool(),
            "move": MoveTool(),
            "line": LineTool(),
            "rectangle": RectangleTool(),
            "circle": CircleTool(),
            "pan": PanTool(),
            "texture": TextureTool(),
            "edge": EdgeTool()
        }
        self.current_tool = "brush"
        
        # Set main window reference for tools that need it
        for tool in self.tools.values():
            if hasattr(tool, 'set_main_window'):
                tool.set_main_window(self)
        
        # Texture library
        self.texture_library = TextureLibrary()
        
        # Initialize dialog manager (needed before UI creation)
        self.dialog_mgr = DialogManager(
            self.root, self.canvas, self.texture_library, self.tools
        )
        
        # Initialize tool size manager
        self.tool_size_mgr = ToolSizeManager(self.root, self.canvas)
        
        # Initialize canvas/zoom manager
        self.canvas_zoom_mgr = CanvasZoomManager(
            self.root, self.canvas, self.layer_manager, 
            self.timeline, self.dialog_mgr
        )
        
        # Initialize grid control manager (after theme manager initialization)
        # Note: Theme manager is initialized below, so we'll set callback after
        
        # UI state
        self.brush_drawing = False
        self.is_drawing = False
        self.last_mouse_pos = (0, 0)
        self._last_drawn_pixel = None  # Track last drawn pixel for efficient updates
        self._updating_display = False  # Flag to prevent recursion
        self.is_fullscreen = False  # Track fullscreen state
        self._windowed_geometry = None  # Store window geometry before fullscreen
        self._windowed_overrideredirect = False  # Store overrideredirect state before fullscreen
        
        # Copy preview position (EventDispatcher needs this)
        self.copy_preview_pos = None  # Mouse position for copy preview
        
        # Scale state for EventDispatcher (points to selection_mgr)
        self.scale_start_pos = None
        
        # Pan state
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        self.recent_selected_color = None
        self.zoom_levels = [0.25, 0.5, 1, 2, 4, 8, 16, 32, 64]
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        # Initialize theme dialog manager
        self.theme_dialog_manager = ThemeDialogManager(self)
        # Initialize theme customizer
        self.theme_customizer = ThemeCustomizer(self, self.theme_manager)
        # Load custom themes from storage
        self.theme_customizer.load_custom_themes()
        # Wire customizer to dialog manager
        self.theme_dialog_manager.set_theme_customizer(self.theme_customizer)
        
        # Initialize context menu manager
        self.context_menu_mgr = ContextMenuManager(self)
        
        # Initialize grid control manager (after theme manager)
        self.grid_control_mgr = GridControlManager(self.canvas, self.theme_manager)
        
        # Notes panel will be initialized after UI creation
        self.notes_panel = None
        self.notes_visible = False
        
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
        
        # Initialize background control manager (after canvas_renderer)
        self.background_control_mgr = BackgroundControlManager(
            self.canvas, 
            self.theme_manager,
            self.canvas_renderer,
            self
        )
        
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
        self.loading_manager.update_loading("Building user interface...", 50)
        self._create_ui()
        
        # Apply initial theme (Basic Grey) to all UI elements IMMEDIATELY after UI creation
        self.loading_manager.update_loading("Applying theme...", 60)
        self.theme_dialog_manager.apply_theme(self.theme_manager.get_current_theme())

        # Initialize canvas operations manager (after UI creation)
        self.loading_manager.update_loading("Initializing canvas...", 70)
        self.canvas_ops_mgr = CanvasOperationsManager(self.root, self.canvas, self.drawing_canvas)
        self.canvas_ops_mgr.left_container = self.left_container
        self.canvas_ops_mgr.right_container = self.right_container
        self.canvas_ops_mgr.update_canvas_callback = self.canvas_renderer.update_pixel_display
        
        # Initialize canvas scrollbar (zoom control on right side of canvas)
        self.canvas_scrollbar = CanvasScrollbar(
            self.drawing_canvas,
            self.theme_manager,
            self._on_scrollbar_zoom_change
        )
        
        # Update tool selection to highlight brush
        self.loading_manager.update_loading("Configuring tools...", 80)
        self._update_tool_selection()
        
        # Initialize palette views and show grid (only once)
        self.loading_manager.update_loading("Setting up palette views...", 85)
        self._initialize_all_views()
        self._show_view("grid")
        
        # Update theme dropdown with custom themes (after UI creation)
        if hasattr(self, 'theme_menu'):
            self.theme_menu.configure(values=self.theme_manager.get_theme_names())
        
        # Initialize canvas integration
        self.loading_manager.update_loading("Finalizing...", 95)
        self._sync_canvas_with_layers()

        # Complete loading after everything is initialized
        # Delay completion until after window is fully rendered and visible
        self.root.after(100, self._finish_loading)

    def _finish_loading(self):
        """Finish the loading process after window is fully rendered"""
        self.loading_manager.finish_loading()
        
        # Force a final update to ensure everything is visible
        self.root.update_idletasks()
        self.root.after(100, lambda: self.root.update())

    
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
        self.zoom_fit_button = self.ui_builder.widgets.get('zoom_fit_button')
        self.zoom_100_button = self.ui_builder.widgets.get('zoom_100_button')
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
        
        # Left collapse button container (for centering)
        left_btn_container = tk.Frame(self.left_container, bg=self.theme_manager.get_current_theme().bg_primary, width=16)
        left_btn_container.pack(side="right", fill="y", padx=0, pady=0)
        left_btn_container.pack_propagate(False)
        
        # Left collapse button (minimalistic centered button)
        left_collapse_btn = ctk.CTkButton(
            left_btn_container,
            text="‹",
            width=14,
            height=40,
            font=("Arial", 16),
            fg_color="transparent",
            hover_color=self.theme_manager.get_current_theme().button_hover,
            text_color=self.theme_manager.get_current_theme().text_secondary,
            corner_radius=4,
            command=self._toggle_left_panel
        )
        left_collapse_btn.place(relx=0.5, rely=0.5, anchor="center")
        self.left_collapse_btn = left_collapse_btn
        self.left_btn_container = left_btn_container
        
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
        self.canvas_frame.pack(fill="both", expand=True, side="left")
        
        # Notes panel (hidden by default)
        self.notes_panel = NotesPanel(canvas_container, self)
        self.notes_panel.hide()
        
        # Right panel container (wrapper for CTk widget) - OPTIMIZED for instant visibility
        self.right_container = tk.Frame(self.paned_window, bg="#1a1a1a")
        self.paned_window.add(self.right_container, minsize=200, width=self.right_panel_width, stretch="never")
        
        # Right collapse button container (for centering)
        right_btn_container = tk.Frame(self.right_container, bg=self.theme_manager.get_current_theme().bg_primary, width=16)
        right_btn_container.pack(side="left", fill="y", padx=0, pady=0)
        right_btn_container.pack_propagate(False)
        
        # Right collapse button (minimalistic centered button)
        right_collapse_btn = ctk.CTkButton(
            right_btn_container,
            text="›",
            width=14,
            height=40,
            font=("Arial", 16),
            fg_color="transparent",
            hover_color=self.theme_manager.get_current_theme().button_hover,
            text_color=self.theme_manager.get_current_theme().text_secondary,
            corner_radius=4,
            command=self._toggle_right_panel
        )
        right_collapse_btn.place(relx=0.5, rely=0.5, anchor="center")
        self.right_collapse_btn = right_collapse_btn
        self.right_btn_container = right_btn_container
        
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
        self.sym_x_btn = selection_buttons['sym_x_btn']
        self.sym_y_btn = selection_buttons['sym_y_btn']
        
        # Update tool button text to show sizes
        # Set tool size manager references and callbacks
        self.tool_size_mgr.tool_buttons = self.tool_buttons
        self.tool_size_mgr.select_tool_callback = self._select_tool
        
        # Update edge button text to show current thickness
        self.tool_size_mgr.update_edge_button_text()
        
        # Update brush and eraser button text to show default sizes
        self.tool_size_mgr.update_brush_button_text()
        self.tool_size_mgr.update_eraser_button_text()
        # Update spray button text
        if hasattr(self.tool_size_mgr, 'update_spray_button_text'):
            self.tool_size_mgr.update_spray_button_text()
        
        # Set canvas/zoom manager references and callbacks
        self.canvas_zoom_mgr.size_var = self.size_var
        self.canvas_zoom_mgr.zoom_var = self.zoom_var
        self.canvas_zoom_mgr.update_canvas_callback = self._update_canvas_from_layers
        self.canvas_zoom_mgr.force_canvas_update_callback = self.canvas_renderer.force_canvas_update
        self.canvas_zoom_mgr.sync_scrollbar_callback = self._sync_scrollbar_with_zoom
        
        # Set grid control manager references and callbacks
        self.grid_control_mgr.grid_button = self.grid_button
        self.grid_control_mgr.grid_overlay_button = self.grid_overlay_button
        self.grid_control_mgr.grid_mode_button = self.ui_builder.widgets['grid_mode_button']
        self.grid_control_mgr.tile_seam_button = self.ui_builder.widgets.get('tile_seam_button')
        self.grid_control_mgr.tile_preview_button = self.ui_builder.widgets.get('tile_preview_button')
        self.grid_control_mgr.force_canvas_update_callback = self.canvas_renderer.force_canvas_update
        
        # Set background control manager references and callbacks
        self.background_control_mgr.background_mode_button = self.ui_builder.widgets['background_mode_button']
        self.background_control_mgr.force_canvas_update_callback = self.canvas_renderer.force_canvas_update
        
        # Initialize grid button states
        self.grid_control_mgr.update_grid_button_text()
        self.grid_control_mgr.update_grid_overlay_button_text()
        self.grid_control_mgr.update_grid_mode_button()
        if self.grid_control_mgr.tile_seam_button:
            self.grid_control_mgr.update_tile_seam_button_text()
        if self.grid_control_mgr.tile_preview_button:
            self.grid_control_mgr.update_tile_preview_button_text()
        
        # Initialize background mode button state
        self.background_control_mgr.update_background_mode_button()
        
        palette_widgets = self.ui_builder.create_palette_panel(self.left_panel, self.palette, self._get_ui_callbacks())
        # Assign palette widget references
        self.color_display_frame = palette_widgets['color_display_container']
        self.palette_content_frame = palette_widgets['palette_content_frame']
        self.grid_view_frame = palette_widgets['grid_view_frame']
        self.primary_view_frame = palette_widgets['primary_view_frame']
        self.wheel_view_frame = palette_widgets['wheel_view_frame']
        self.constants_view_frame = palette_widgets['constants_view_frame']
        self.saved_view_frame = palette_widgets['saved_view_frame']
        self.recent_view_frame = palette_widgets.get('recent_view_frame')  # Recent colors frame
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
        # Initialize layer animation manager
        self.layer_anim_mgr = LayerAnimationManager(
            self.root, self.canvas, self.layer_manager, self.timeline,
            None, None  # layer_panel and timeline_panel will be created below
        )
        self.layer_panel, self.timeline_panel = self.layer_anim_mgr.create_layer_and_timeline_panels(
            self.right_panel, self.theme_manager
        )
        # Update manager with created panels
        self.layer_anim_mgr.layer_panel = self.layer_panel
        self.layer_anim_mgr.timeline_panel = self.timeline_panel
        # Set callbacks
        self.layer_anim_mgr.update_canvas_callback = self._update_canvas_from_layers
        self.layer_anim_mgr.clear_selection_callback = self._clear_selection_and_reset_tools
        self.layer_anim_mgr.update_pixel_display_callback = self.canvas_renderer.update_pixel_display
        # Wire timeline panel onion skin callbacks
        if self.timeline_panel:
            self.timeline_panel.update_pixel_display_callback = self.canvas_renderer.update_pixel_display
        
        # Initialize Reference Image Panel (in right sidebar, below layers/timeline)
        self.reference_panel = ReferencePanel(self.right_panel, self)
        
        # Initialize 3D Token Preview Panel (in right sidebar, below reference)
        self.token_preview_panel = TokenPreviewPanel(self.right_panel, self)
        
        # Initialize file operations manager
        self.file_ops = FileOperationsManager(
            self.root, self.canvas, self.palette, self.layer_manager,
            self.timeline, self.project, self.export_manager, self.presets,
            self.layer_panel, self.timeline_panel, self.tools
        )
        self.file_ops.force_canvas_update_callback = self.canvas_renderer.force_canvas_update
        self.file_ops.update_canvas_from_layers_callback = self._update_canvas_from_layers
        self.file_ops.clear_selection_and_reset_tools_callback = self._clear_selection_and_reset_tools
        self.file_ops.purge_canvas_overlays_callback = self._purge_canvas_overlays
        
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
        
        # Pass loading screen reference to window state manager
        self.window_state_manager.loading_screen_frame = self.loading_manager.loading_screen.loading_frame
        
        # DON'T restore window state during loading - it interferes with panel sizing
        # Window state will be restored after loading completes
        
        # Initialize color view manager
        self.color_view_mgr = ColorViewManager(
            self.root, self.palette, self.theme_manager, 
            self.custom_colors, self.left_panel
        )
        # Set UI component references
        self.color_view_mgr.palette_content_frame = self.palette_content_frame
        self.color_view_mgr.color_display_frame = self.color_display_frame
        self.color_view_mgr.saved_view_frame = self.saved_view_frame
        self.color_view_mgr.recent_view_frame = self.recent_view_frame
        self.color_view_mgr.view_mode_var = self.view_mode_var
        # Set callbacks
        self.color_view_mgr.update_canvas_callback = self.canvas_renderer.update_pixel_display
        self.color_view_mgr.select_tool_callback = self._select_tool
        # Set MainWindow reference
        self.color_view_mgr.main_window = self
        
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
        # Initialize color wheel lazily (only when wheel view is requested)
        # This prevents the color wheel from being created during startup
        self.color_wheel = None
        
        self.saved_view = SavedView(
            self.saved_view_frame, 
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
        
        # Set view references in color view manager
        self.color_view_mgr.grid_view = self.grid_view
        self.color_view_mgr.primary_view = self.primary_view
        self.color_view_mgr.saved_view = self.saved_view
        self.color_view_mgr.constants_view = self.constants_view
        self.color_view_mgr.color_wheel = self.color_wheel
        
        # Set cross-references between views
        self.saved_view.primary_view = self.primary_view
        self.saved_view.main_window = self
        
        # Track last active view for proper color saving
        self.last_active_view = "grid"  # Default to grid
        
        # Create status bar (after all UI is created)
        self.status_bar = StatusBar(self.main_frame, self.theme_manager)
        self.canvas_hud = CanvasHUD(self.drawing_canvas, self.theme_manager)
        
        # Initialize status bar with current values
        self._update_status_bar()
        
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
        """Redraw canvas after window/panel resize - delegates to canvas operations manager"""
        if hasattr(self, 'canvas_ops_mgr'):
            self.canvas_ops_mgr.redraw_canvas_after_resize()
    
    def _get_ui_callbacks(self):
        """Returns a dictionary of callbacks for the UI builder."""
        return {
            'show_file_menu': self._show_file_menu,
            'on_size_change': self.canvas_zoom_mgr.on_size_change,
            'on_zoom_change': self.canvas_zoom_mgr.on_zoom_change,
            'zoom_fit': self._zoom_fit,
            'zoom_100': self._zoom_100,
            'undo': self._undo,
            'redo': self._redo,
            'on_theme_selected': self._on_theme_selected,
            'show_settings_dialog': self.theme_dialog_manager.show_settings_dialog,
            'toggle_grid': self.grid_control_mgr.toggle_grid,
            'toggle_grid_overlay': self.grid_control_mgr.toggle_grid_overlay,
            'toggle_grid_mode': self.grid_control_mgr.toggle_grid_mode,
            'toggle_tile_seam': self.grid_control_mgr.toggle_tile_seam_preview,
            'toggle_tile_preview': self.grid_control_mgr.toggle_tile_preview,
            'toggle_background_mode': self.background_control_mgr.toggle_background_mode,
            'toggle_notes': self._toggle_notes,
            'select_tool': self._select_tool,
            'update_tool_selection': self._update_tool_selection,
            'show_brush_size_menu': self.tool_size_mgr.show_brush_size_menu,
            'show_eraser_size_menu': self.tool_size_mgr.show_eraser_size_menu,
            'show_spray_size_menu': self.tool_size_mgr.show_spray_size_menu,
            'show_edge_thickness_menu': self.tool_size_mgr.show_edge_thickness_menu,
            'open_texture_panel': self.dialog_mgr.open_texture_panel,
            'mirror_selection': self.selection_mgr.mirror_selection,
            'rotate_selection': self.selection_mgr.rotate_selection,
            'copy_selection': self.selection_mgr.copy_selection,
            'scale_selection': self.selection_mgr.scale_selection,
            'toggle_symmetry_x': self._toggle_symmetry_x,
            'toggle_symmetry_y': self._toggle_symmetry_y,
            'on_palette_change': self._on_palette_change,
            'on_view_mode_change': self._on_view_mode_change,
            'initialize_all_views': self._initialize_all_views,
            'show_view': self._show_view,
        }

    def _toggle_symmetry_x(self):
        """Toggle horizontal symmetry"""
        self.canvas.toggle_symmetry_x()
        self._update_symmetry_buttons()

    def _toggle_symmetry_y(self):
        """Toggle vertical symmetry"""
        self.canvas.toggle_symmetry_y()
        self._update_symmetry_buttons()

    def _update_symmetry_buttons(self):
        """Update symmetry button appearance"""
        theme = self.theme_manager.get_current_theme()
        
        if hasattr(self, 'sym_x_btn'):
            if self.canvas.symmetry_x:
                self.sym_x_btn.configure(fg_color=theme.tool_selected, text_color=theme.text_primary)
            else:
                self.sym_x_btn.configure(fg_color=theme.button_normal, text_color=theme.text_primary)
                
        if hasattr(self, 'sym_y_btn'):
            if self.canvas.symmetry_y:
                self.sym_y_btn.configure(fg_color=theme.tool_selected, text_color=theme.text_primary)
            else:
                self.sym_y_btn.configure(fg_color=theme.button_normal, text_color=theme.text_primary)

    def _purge_canvas_overlays(self):
        """Delete all transient canvas overlays and clear edge tool previews/lines.
        This is a safety purge to resolve any 'immortal' overlay items that may
        survive redraws due to tag ordering or throttled redraws.
        """
        if hasattr(self, 'drawing_canvas') and self.drawing_canvas:
            # Remove all known transient tags
            for tag in [
                "edge_preview", "edge_lines", "shape_preview", "brush_preview",
                "eraser_preview", "spray_preview", "texture_preview", "selection", "move_preview",
                "rotate_preview", "copy_preview", "scale_handle", "border"
            ]:
                try:
                    self.drawing_canvas.delete(tag)
                except Exception:
                    pass
        # Ask edge tool to forget stored lines as well (full purge scenario)
        edge_tool = self.tools.get("edge") if hasattr(self, 'tools') else None
        if edge_tool and hasattr(edge_tool, 'clear_all_edges'):
            try:
                edge_tool.clear_all_edges()
            except Exception:
                pass

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
    
    def _update_size_display(self):
        """Update the canvas size display in the toolbar"""
        if hasattr(self, 'ui_builder') and 'size_var' in self.ui_builder.widgets:
            size_text = f"{self.canvas.width}x{self.canvas.height}"
            self.ui_builder.widgets['size_var'].set(size_text)
    
    def _tkinter_screen_to_canvas_coords(self, screen_x: int, screen_y: int) -> tuple[int, int]:
        """Convert tkinter screen coordinates to canvas coordinates"""
        if not hasattr(self, 'drawing_canvas') or not self.drawing_canvas:
            return (0, 0)
        
        # Get canvas dimensions
        canvas_width = self.drawing_canvas.winfo_width()
        canvas_height = self.drawing_canvas.winfo_height()
        
        # Calculate canvas pixel dimensions
        canvas_pixel_width = self.canvas.width * self.canvas.zoom
        canvas_pixel_height = self.canvas.height * self.canvas.zoom
        
        # Calculate canvas offset (centered in the drawing area)
        x_offset = (canvas_width - canvas_pixel_width) // 2
        y_offset = (canvas_height - canvas_pixel_height) // 2
        
        # Add pan offset
        x_offset += self.pan_offset_x * self.canvas.zoom
        y_offset += self.pan_offset_y * self.canvas.zoom
        
        # Convert screen coordinates to canvas pixel coordinates
        canvas_x = int((screen_x - x_offset) / self.canvas.zoom)
        canvas_y = int((screen_y - y_offset) / self.canvas.zoom)
        
        # Clamp to canvas bounds
        canvas_x = max(0, min(canvas_x, self.canvas.width - 1))
        canvas_y = max(0, min(canvas_y, self.canvas.height - 1))
        
        return (canvas_x, canvas_y)
    
    def _tkinter_screen_to_canvas_coords_float(self, screen_x: int, screen_y: int) -> tuple[float, float]:
        """Convert tkinter screen coordinates to canvas coordinates with float precision (for edge tool)"""
        if not hasattr(self, 'drawing_canvas') or not self.drawing_canvas:
            return (0.0, 0.0)
        
        # Get canvas dimensions
        canvas_width = self.drawing_canvas.winfo_width()
        canvas_height = self.drawing_canvas.winfo_height()
        
        # Calculate canvas pixel dimensions
        canvas_pixel_width = self.canvas.width * self.canvas.zoom
        canvas_pixel_height = self.canvas.height * self.canvas.zoom
        
        # Calculate canvas offset (centered in the drawing area)
        x_offset = (canvas_width - canvas_pixel_width) // 2
        y_offset = (canvas_height - canvas_pixel_height) // 2
        
        # Add pan offset
        x_offset += self.pan_offset_x * self.canvas.zoom
        y_offset += self.pan_offset_y * self.canvas.zoom
        
        # Convert screen coordinates to canvas pixel coordinates (preserve float precision)
        canvas_x = (screen_x - x_offset) / self.canvas.zoom
        canvas_y = (screen_y - y_offset) / self.canvas.zoom
        
        # Clamp to canvas bounds
        canvas_x = max(0.0, min(canvas_x, self.canvas.width - 1.0))
        canvas_y = max(0.0, min(canvas_y, self.canvas.height - 1.0))
        
        return (canvas_x, canvas_y)
    
    def _select_tool(self, tool_id: str):
        """Select a drawing tool"""
        # Clear any tool previews when changing tools
        self.drawing_canvas.delete("brush_preview")
        self.drawing_canvas.delete("eraser_preview")
        self.drawing_canvas.delete("spray_preview")
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
            # Only finalize move if it hasn't been finalized yet
            move_tool = self.tools.get("move")
            if move_tool and hasattr(move_tool, 'finalize_move') and move_tool.has_been_moved:
                draw_layer = self._get_drawing_layer()
                if draw_layer:
                    move_tool.finalize_move(draw_layer)
            
            selection_tool = self.tools.get("selection")
            move_tool = self.tools.get("move")
            if selection_tool and selection_tool.has_selection:
                selection_tool.clear_selection()
                # Reset move tool state when clearing selection
                if move_tool:
                    move_tool.reset_state()
                self.canvas_renderer.update_pixel_display()
        
        self.current_tool = tool_id
        
        # Update tool button appearance
        self._update_tool_selection()
        
        # Clear scale button if not in scaling mode
        if hasattr(self, 'selection_mgr') and self.selection_mgr.scale_btn and not self.selection_mgr.is_scaling:
            self.selection_mgr.scale_btn.configure(fg_color=self.theme_manager.get_current_theme().button_normal)
        
        # Update status bar
        if hasattr(self, 'status_bar'):
            self._update_status_bar()
        
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

    def _on_palette_change(self, palette_name: str):
        """Handle palette change - automatically switch to Grid view"""
        self.palette.load_by_name(palette_name)
        
        # Always switch to Grid view when changing palette
        self.view_mode_var.set("grid")
        
        # Update grid view with new palette
        if hasattr(self, 'grid_view') and self.grid_view:
            self.grid_view.create()
        
        # Show grid view
        self._show_view("grid")
    
    def _initialize_all_views(self):
        """Initialize all palette views once at startup - delegates to color view manager"""
        if hasattr(self, 'color_view_mgr'):
            self.color_view_mgr.initialize_all_views()
    
    def _show_view(self, mode: str):
        """Show specific view - delegates to color view manager"""
        if hasattr(self, 'color_view_mgr'):
            self.color_view_mgr.show_view(mode)
    
    def _on_view_mode_change(self):
        """Handle view mode change - delegates to color view manager"""
        # Track the last active view before switching
        current_mode = self.view_mode_var.get()
        if current_mode != "saved":
            self.last_active_view = current_mode
        
        if hasattr(self, 'color_view_mgr'):
            self.color_view_mgr.on_view_mode_change()
        else:
            mode = self.view_mode_var.get()
            self._show_view(mode)
    
    def _create_color_wheel(self):
        """Create color wheel view - delegates to color view manager"""
        if hasattr(self, 'color_view_mgr'):
            self.color_view_mgr.create_color_wheel()
    
    def _on_color_wheel_changed(self, rgb_color):
        """Handle color wheel color change - delegates to color view manager"""
        if hasattr(self, 'color_view_mgr'):
            self.color_view_mgr.on_color_wheel_changed(rgb_color)
    
    def _save_custom_color(self, rgb_color):
        """Save current color wheel color to custom colors - delegates to color view manager"""
        if hasattr(self, 'color_view_mgr'):
            self.color_view_mgr.save_custom_color(rgb_color)
    
    def _remove_custom_color(self, color):
        """Remove a custom color - delegates to color view manager"""
        if hasattr(self, 'color_view_mgr'):
            self.color_view_mgr.remove_custom_color(color)
    
    def _on_scrollbar_zoom_change(self, zoom_value: float):
        """Handle zoom change from canvas scrollbar"""
        # Convert float zoom to string format (e.g., 4.0 -> "4x")
        if zoom_value >= 1:
            zoom_str = f"{int(zoom_value)}x"
        else:
            zoom_str = f"{zoom_value}x"
        
        # Update the zoom dropdown
        if hasattr(self, 'zoom_var'):
            self.zoom_var.set(zoom_str)
        
        # Apply zoom through canvas zoom manager
        if hasattr(self, 'canvas_zoom_mgr'):
            self.canvas_zoom_mgr.on_zoom_change(zoom_str)
    
    def _sync_scrollbar_with_zoom(self):
        """Sync scrollbar position when zoom changes from dropdown or other source"""
        if hasattr(self, 'canvas_scrollbar') and hasattr(self, 'canvas'):
            self.canvas_scrollbar.update_zoom_index(self.canvas.zoom)

    def _format_zoom_str(self, zoom_value: float) -> str:
        """Return zoom dropdown string for a zoom value."""
        if zoom_value >= 1:
            return f"{int(zoom_value)}x"
        return f"{zoom_value}x"

    def _apply_zoom_with_focus(self, zoom_value: float, focus_x: int, focus_y: int, reset_pan: bool = False):
        """Apply zoom and keep the focus point stable in screen space."""
        if not hasattr(self, 'drawing_canvas') or not self.drawing_canvas:
            return
        if zoom_value == self.canvas.zoom:
            return

        canvas_width = self.drawing_canvas.winfo_width()
        canvas_height = self.drawing_canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1:
            return

        # Compute canvas coords under focus before zoom change
        canvas_x, canvas_y = self._tkinter_screen_to_canvas_coords_float(focus_x, focus_y)

        # Apply zoom
        self.canvas.set_zoom(zoom_value)

        if reset_pan:
            self.pan_offset_x = 0
            self.pan_offset_y = 0
        else:
            # Recalculate pan offsets to keep the focus point stable
            canvas_pixel_width = self.canvas.width * zoom_value
            canvas_pixel_height = self.canvas.height * zoom_value
            x_offset = (canvas_width - canvas_pixel_width) / 2
            y_offset = (canvas_height - canvas_pixel_height) / 2
            self.pan_offset_x = (focus_x - x_offset - canvas_x * zoom_value) / zoom_value
            self.pan_offset_y = (focus_y - y_offset - canvas_y * zoom_value) / zoom_value

        # Update zoom dropdown
        if hasattr(self, 'zoom_var'):
            self.zoom_var.set(self._format_zoom_str(zoom_value))

        # Force redraw and sync scrollbar
        if hasattr(self, 'canvas_renderer'):
            self.canvas_renderer.force_canvas_update()
        self._sync_scrollbar_with_zoom()

    def _get_fit_zoom(self) -> float:
        """Return the largest zoom level that fits the canvas in the view."""
        if not hasattr(self, 'drawing_canvas') or not self.drawing_canvas:
            return 1

        canvas_width = self.drawing_canvas.winfo_width()
        canvas_height = self.drawing_canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1:
            return 1

        fit_zoom = min(canvas_width / self.canvas.width, canvas_height / self.canvas.height)
        # Pick the largest allowed zoom <= fit_zoom
        candidates = [z for z in self.zoom_levels if z <= fit_zoom]
        return max(candidates) if candidates else min(self.zoom_levels)

    def _zoom_fit(self):
        """Zoom to fit the entire canvas in the view."""
        if not hasattr(self, 'drawing_canvas'):
            return
        canvas_width = self.drawing_canvas.winfo_width()
        canvas_height = self.drawing_canvas.winfo_height()
        zoom_value = self._get_fit_zoom()
        self._apply_zoom_with_focus(zoom_value, canvas_width // 2, canvas_height // 2, reset_pan=True)

    def _zoom_100(self):
        """Set zoom to 100% and center the canvas."""
        if not hasattr(self, 'drawing_canvas'):
            return
        canvas_width = self.drawing_canvas.winfo_width()
        canvas_height = self.drawing_canvas.winfo_height()
        self._apply_zoom_with_focus(1, canvas_width // 2, canvas_height // 2, reset_pan=True)

    def _zoom_at_cursor(self, direction: int, cursor_x: int, cursor_y: int):
        """Zoom in/out around the cursor position."""
        if not self.zoom_levels:
            return
        current_zoom = self.canvas.zoom
        try:
            current_index = self.zoom_levels.index(current_zoom)
        except ValueError:
            current_index = min(range(len(self.zoom_levels)), key=lambda i: abs(self.zoom_levels[i] - current_zoom))

        next_index = current_index + (1 if direction > 0 else -1)
        next_index = max(0, min(next_index, len(self.zoom_levels) - 1))
        next_zoom = self.zoom_levels[next_index]
        self._apply_zoom_with_focus(next_zoom, cursor_x, cursor_y)
    
    def _on_theme_selected(self, theme_name: str):
        """Handle theme selection from dropdown"""
        self.theme_manager.set_theme(theme_name)
    
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
        
        import_png_btn = ctk.CTkButton(file_menu, text="Import PNG", command=lambda: [file_menu.destroy(), self._show_import_png_dialog()])
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
        
        quick_export_btn = ctk.CTkButton(file_menu, text="Quick Export (Ctrl+Shift+E)", command=lambda: [self.file_ops.quick_export(), file_menu.destroy()])
        quick_export_btn.pack(pady=5, padx=10, fill="x")
        export_gif_btn.pack(pady=5, padx=10, fill="x")
        
        export_spritesheet_btn = ctk.CTkButton(file_menu, text="Export Sprite Sheet", command=lambda: [self.file_ops.export_spritesheet(), file_menu.destroy()])
        export_spritesheet_btn.pack(pady=5, padx=10, fill="x")

        quick_export_btn = ctk.CTkButton(file_menu, text="Quick Export", command=lambda: [self.file_ops.quick_export(), file_menu.destroy()])
        quick_export_btn.pack(pady=5, padx=10, fill="x")
        
        # Separator
        sep2 = ctk.CTkFrame(file_menu, height=2)
        sep2.pack(fill="x", padx=10, pady=10)
        
        # Templates
        template_btn = ctk.CTkButton(file_menu, text="Load Template", command=lambda: [self.file_ops.show_templates(), file_menu.destroy()])
        template_btn.pack(pady=5, padx=10, fill="x")
        
        # Close button
        close_btn = ctk.CTkButton(file_menu, text="Close", command=file_menu.destroy)
        close_btn.pack(pady=10, padx=10, fill="x")
    
    def _show_import_png_dialog(self):
        """Show import PNG dialog with preview and scale options"""
        try:
            dialog = ImportPNGDialog(
                self.root,
                on_import=self._handle_png_import,
                theme=self.theme_manager.current_theme
            )
            dialog.show()
        except Exception as e:
            self.dialog_mgr.show_error("Dialog Error", f"Failed to open import dialog:\n{e}")
    
    def _handle_png_import(self, file_path: str, scale_factor: int):
        """Handle PNG import with scale factor"""
        from src.utils.import_png import PNGImporter
        import tempfile
        import os
        
        # Create temp pixpf file
        temp_dir = tempfile.gettempdir()
        temp_pixpf = os.path.join(temp_dir, "imported_temp.pixpf")
        
        # Import PNG with scale factor
        importer = PNGImporter()
        success, message = importer.import_png_to_pixpf(
            file_path,
            temp_pixpf,
            scale_factor=scale_factor
        )
        
        if success:
            # Load the imported project directly
            load_success = self.project.load_project(
                temp_pixpf,
                self.canvas,
                self.palette,
                self.layer_manager,
                self.timeline
            )
            
            if load_success:
                # Update canvas from loaded layers (composite all layers)
                self._update_canvas_from_layers()

                # Update UI components to reflect loaded project
                self.layer_panel.refresh()
                self.timeline_panel.refresh()
                
                # Update size display in toolbar
                self._update_size_display()
                
                # Force immediate display update
                self.root.update_idletasks()
                self.root.update()
            else:
                import tkinter.messagebox as msgbox
                msgbox.showerror("Import Failed", "Failed to load imported project")
                return
            
            # Show success message using messagebox (no focus issues)
            import tkinter.messagebox as msgbox
            msgbox.showinfo("Import Successful", message)
        else:
            # Show error message
            self.dialog_mgr.show_error("Import Failed", message)
    

    def _on_layer_changed(self):
        """Handle layer changes - delegates to layer animation manager"""
        if hasattr(self, 'layer_anim_mgr'):
            self.layer_anim_mgr.on_layer_changed()
    
    def _update_canvas_from_layers(self):
        """Update canvas to show all visible layers combined"""
        # Update status bar when layers change
        if hasattr(self, 'status_bar'):
            self._update_status_bar()
        # Always show all visible layers combined
        flattened_pixels = self.layer_manager.flatten_layers()
        
        # Update canvas with the flattened result
        self.canvas.pixels = flattened_pixels
        
        # Trigger display update to show the changes
        self.canvas_renderer.update_pixel_display()
    
    def _clear_selection_and_reset_tools(self):
        """Clear any active selection and reset tools to brush"""
        # Clear selection if there is one
        selection_tool = self.tools.get("selection")
        move_tool = self.tools.get("move")
        if selection_tool and selection_tool.has_selection:
            selection_tool.clear_selection()
            # Reset move tool state when clearing selection
            if move_tool:
                move_tool.reset_state()
        
        # Reset tool to brush
        self._select_tool("brush")
    
    def _get_drawing_layer(self):
        """Get the layer to draw on - delegates to layer animation manager"""
        if hasattr(self, 'layer_anim_mgr'):
            return self.layer_anim_mgr.get_drawing_layer()
        return None
    
    def get_current_color(self):
        """Get current color based on view mode (palette or color wheel)"""
        # If color wheel view is active, get from wheel; otherwise from palette
        if (hasattr(self, 'color_wheel') and self.color_wheel and 
            hasattr(self, 'view_mode_var') and self.view_mode_var.get() == "wheel"):
            rgb_color = self.color_wheel.get_color()
            return (rgb_color[0], rgb_color[1], rgb_color[2], 255)
        elif (hasattr(self, 'view_mode_var') and self.view_mode_var.get() == "primary" and
              hasattr(self, 'primary_view') and self.primary_view):
            # Get color from Primary view (separate from main palette)
            primary_color = self.primary_view.get_current_color()
            if primary_color:
                return primary_color
            else:
                # Fallback to palette if no Primary color selected
                return self.palette.get_primary_color()
        elif (hasattr(self, 'view_mode_var') and self.view_mode_var.get() == "saved" and
              hasattr(self, 'saved_view') and self.saved_view):
            # Get color from Saved view (separate from main palette)
            saved_color = self.saved_view.get_current_color()
            if saved_color:
                return saved_color
            else:
                # Fallback to palette if no Saved color selected
                return self.palette.get_primary_color()
        elif (hasattr(self, 'view_mode_var') and self.view_mode_var.get() == "recent" and
              hasattr(self, 'recent_colors') and self.recent_colors):
            if self.recent_selected_color:
                return self.recent_selected_color
            recent_colors = self.recent_colors.get_colors()
            if recent_colors:
                return recent_colors[0]
            return self.palette.get_primary_color()
        else:
            return self.palette.get_primary_color()
    
    def get_source_color(self):
        """Get current color from the actual source view (ignoring saved view mode)"""
        # Determine which view to get color from
        current_mode = self.view_mode_var.get() if hasattr(self, 'view_mode_var') else "grid"
        
        # If in saved view mode, use the last active view to determine source
        if current_mode == "saved":
            source_mode = getattr(self, 'last_active_view', 'grid')
        else:
            source_mode = current_mode
        
        # Get color from the appropriate source view
        if source_mode == "grid":
            # If in grid view, get from palette
            return self.palette.get_primary_color()
        elif source_mode == "primary" and hasattr(self, 'primary_view') and self.primary_view:
            # Get color from Primary view
            primary_color = self.primary_view.get_current_color()
            if primary_color:
                return primary_color
            else:
                # Fallback to palette if no Primary color selected
                return self.palette.get_primary_color()
        elif source_mode == "wheel" and hasattr(self, 'color_wheel') and self.color_wheel:
            # Get color from Wheel view
            rgb_color = self.color_wheel.get_color()
            return (rgb_color[0], rgb_color[1], rgb_color[2], 255)
        
        # Fallback: Check Primary view first (most recent selection)
        if (hasattr(self, 'primary_view') and self.primary_view):
            primary_color = self.primary_view.get_current_color()
            if primary_color:
                return primary_color
        
        # Check Wheel view
        if (hasattr(self, 'color_wheel') and self.color_wheel):
            rgb_color = self.color_wheel.get_color()
            return (rgb_color[0], rgb_color[1], rgb_color[2], 255)
        
        # Fallback to palette
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
            # Color not in current palette, search across ALL available JSON palettes
            preset_result = self.palette.find_color_in_presets(rgba_color)
            
            if preset_result:
                # Color found in another preset!
                preset_name, color_index = preset_result
                
                # Switch to that palette by name (JSON-backed)
                self.palette.load_by_name(preset_name)
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
    
    def _undo(self):
        """Undo last action"""
        # Get current state before undoing
        active_layer = self.layer_manager.get_active_layer()
        current_pixels = active_layer.pixels.copy() if active_layer else None
        current_layer_index = self.layer_manager.active_layer_index
        
        # Get current edge lines
        edge_tool = self.tools.get("edge")
        current_edge_lines = edge_tool.edge_lines if edge_tool else None
        
        state = self.undo_manager.undo(current_pixels, current_layer_index, current_edge_lines)
        if state:
            # Restore layer state
            if state.pixels is not None:
                layer = self.layer_manager.get_layer(state.layer_index)
                if layer:
                    layer.pixels = state.pixels
                    layer.mark_modified()  # Mark layer as modified for cache invalidation
                    self._on_layer_changed()
            
            # Restore edge lines
            if state.edge_lines is not None and edge_tool:
                edge_tool.edge_lines = state.edge_lines
                edge_tool.redraw_all_edges()

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
        
        # Get current edge lines
        edge_tool = self.tools.get("edge")
        current_edge_lines = edge_tool.edge_lines if edge_tool else None
        
        state = self.undo_manager.redo(current_pixels, current_layer_index, current_edge_lines)
        if state:
            # Restore layer state
            if state.pixels is not None:
                layer = self.layer_manager.get_layer(state.layer_index)
                if layer:
                    layer.pixels = state.pixels
                    layer.mark_modified()  # Mark layer as modified for cache invalidation
                    self._on_layer_changed()
            
            # Restore edge lines
            if state.edge_lines is not None and edge_tool:
                edge_tool.edge_lines = state.edge_lines
                edge_tool.redraw_all_edges()

            # Force immediate tkinter canvas update for instant visual feedback
            self.canvas_renderer.force_canvas_update()
            # Force immediate GUI refresh for instant response
            self.root.update_idletasks()
    
    def _add_layer(self):
        """Add a new layer - delegates to layer animation manager"""
        if hasattr(self, 'layer_anim_mgr'):
            self.layer_anim_mgr.add_layer()
    
    def _sync_canvas_with_layers(self):
        """Sync canvas with layer manager - delegates to layer animation manager"""
        if hasattr(self, 'layer_anim_mgr'):
            self.layer_anim_mgr.sync_canvas_with_layers()

    def _on_frame_changed(self):
        """Handle frame change in timeline - delegates to layer animation manager"""
        if hasattr(self, 'layer_anim_mgr'):
            self.layer_anim_mgr.on_frame_changed()
    
    def _toggle_animation(self):
        """Toggle animation playback - delegates to layer animation manager"""
        if hasattr(self, 'layer_anim_mgr'):
            self.layer_anim_mgr.toggle_animation()
    
    def _previous_frame(self):
        """Go to previous frame - delegates to layer animation manager"""
        if hasattr(self, 'layer_anim_mgr'):
            self.layer_anim_mgr.previous_frame()
    
    def _next_frame(self):
        """Go to next frame - delegates to layer animation manager"""
        if hasattr(self, 'layer_anim_mgr'):
            self.layer_anim_mgr.next_frame()
    
    def _save_window_state(self):
        """Save current window and panel state - delegates to canvas operations manager"""
        if hasattr(self, 'canvas_ops_mgr'):
            self.canvas_ops_mgr.save_window_state()
    
    def _toggle_notes(self):
        """Toggle notes panel visibility"""
        if self.notes_visible:
            # Hide notes panel
            self.notes_panel.hide()
            self.canvas_frame.pack(fill="both", expand=True, side="left")
            self.notes_visible = False
        else:
            # Show notes panel
            self.canvas_frame.pack(fill="both", expand=True, side="left")
            self.notes_panel.frame.pack(fill="both", expand=False, side="right", padx=(5, 0))
            self.notes_panel.frame.configure(width=300)
            self.notes_visible = True
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode (F11)"""
        if not self.is_fullscreen:
            # Entering fullscreen - save current window geometry and state
            self._windowed_geometry = self.root.geometry()
            self._windowed_overrideredirect = self.root.overrideredirect()
            self.is_fullscreen = True
            
            # Ensure window is visible and updated before fullscreen
            self.root.deiconify()
            self.root.update_idletasks()
            
            # Get screen dimensions
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # On Windows, use overrideredirect + geometry for true fullscreen
            # This avoids CustomTkinter's fullscreen attribute issues
            import sys
            if sys.platform == 'win32':
                # Remove window decorations for true fullscreen
                self.root.overrideredirect(True)
                # Set geometry to full screen
                self.root.geometry(f"{screen_width}x{screen_height}+0+0")
                self.root.update_idletasks()
            else:
                # On Linux/Mac, use standard fullscreen attribute
                self.root.attributes('-fullscreen', True)
                self.root.update_idletasks()
        else:
            # Exiting fullscreen - restore previous window state
            self.is_fullscreen = False
            
            # Restore window decorations if we removed them
            if hasattr(self, '_windowed_overrideredirect'):
                self.root.overrideredirect(self._windowed_overrideredirect)
            
            # Remove fullscreen attribute
            self.root.attributes('-fullscreen', False)
            self.root.update_idletasks()
            
            # Restore window geometry if we saved it
            if self._windowed_geometry:
                self.root.after(50, lambda: self.root.geometry(self._windowed_geometry))
        
        # Force canvas redraw after fullscreen toggle
        if hasattr(self, 'canvas_renderer'):
            self.root.after(100, self.canvas_renderer.force_canvas_update)
    
    def _exit_fullscreen(self):
        """Exit fullscreen mode if active"""
        if self.is_fullscreen:
            self.is_fullscreen = False
            
            # Restore window decorations if we removed them
            if hasattr(self, '_windowed_overrideredirect'):
                self.root.overrideredirect(self._windowed_overrideredirect)
            
            # Remove fullscreen attribute
            self.root.attributes('-fullscreen', False)
            self.root.update_idletasks()
            
            # Restore window geometry if we saved it
            if self._windowed_geometry:
                self.root.after(50, lambda: self.root.geometry(self._windowed_geometry))
            
            # Force canvas redraw after exiting fullscreen
            if hasattr(self, 'canvas_renderer'):
                self.root.after(100, self.canvas_renderer.force_canvas_update)
    
    def _update_status_bar(self, cursor_x=None, cursor_y=None):
        """Update status bar with current application state"""
        if not hasattr(self, 'status_bar'):
            return
        
        # Update cursor position if provided
        if cursor_x is not None and cursor_y is not None:
            self.status_bar.update_cursor(cursor_x, cursor_y)
            if hasattr(self, 'canvas_hud'):
                self.canvas_hud.update_cursor(cursor_x, cursor_y)
        
        # Update tool
        tool_name = self.current_tool if hasattr(self, 'current_tool') else "--"
        self.status_bar.update_tool(tool_name)
        if hasattr(self, 'canvas_hud'):
            self.canvas_hud.update_tool(tool_name)
        
        # Update tool size
        size_str = "--"
        if hasattr(self, 'tool_size_mgr'):
            if self.current_tool == "brush":
                size = self.tool_size_mgr.brush_size
                size_str = f"{size}x{size}"
            elif self.current_tool == "eraser":
                size = self.tool_size_mgr.eraser_size
                size_str = f"{size}x{size}"
            elif self.current_tool == "spray":
                radius = self.tool_size_mgr.spray_radius
                size_str = f"R{radius}"
            elif self.current_tool == "edge":
                thickness = self.tool_size_mgr.edge_thickness
                size_str = f"{thickness}P"
        self.status_bar.update_size(size_str)
        if hasattr(self, 'canvas_hud'):
            self.canvas_hud.update_size(size_str)
        
        # Update zoom
        zoom = self.canvas.zoom if hasattr(self, 'canvas') else 1.0
        self.status_bar.update_zoom(zoom)
        if hasattr(self, 'canvas_hud'):
            self.canvas_hud.update_zoom(zoom)
        
        # Update layer
        if hasattr(self, 'layer_manager'):
            active_layer = self.layer_manager.get_active_layer()
            if active_layer:
                layer_index = self.layer_manager.layers.index(active_layer)
                self.status_bar.update_layer(active_layer.name, layer_index)
                if hasattr(self, 'canvas_hud'):
                    self.canvas_hud.update_layer(f"{active_layer.name} ({layer_index + 1})")
            else:
                self.status_bar.update_layer("None")
                if hasattr(self, 'canvas_hud'):
                    self.canvas_hud.update_layer("None")
        
        # Update frame
        if hasattr(self, 'timeline'):
            current_frame = self.timeline.current_frame
            total_frames = len(self.timeline.frames)
            self.status_bar.update_frame(current_frame, total_frames)
            if hasattr(self, 'canvas_hud'):
                self.canvas_hud.update_frame(f"{current_frame + 1}/{total_frames}")
    
    def _on_window_close(self):
        """Handle window close event - save state before closing"""
        self._save_window_state()
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
