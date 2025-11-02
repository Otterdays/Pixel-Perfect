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
from .palette_views import GridView, PrimaryView, SavedView, ConstantsView
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
from .layer_panel import LayerPanel
from animation.timeline import AnimationTimeline
from .timeline_panel import TimelinePanel
from .tooltip import create_tooltip
from .theme_manager import ThemeManager
from .ui_builder import UIBuilder
from .theme_dialog_manager import ThemeDialogManager
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
        window_width = min(1400, screen_width - 40)  # Leave some margin on sides
        window_height = min(800, available_height)   # Increased by 150px from 650, still above taskbar
        
        # Center the window on screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2 - 30  # Slightly above center to account for taskbar
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        print(f"[Window] Initialized at {window_width}x{window_height} (screen: {screen_width}x{screen_height})")
        
        # HIDE the window completely until loading finishes
        # This prevents any UI elements from showing before loading screen is ready
        self.root.withdraw()
        print("[Window] Window withdrawn (hidden) until loading completes")
        
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
        
        # Initialize loading screen manager NOW - after icon but before any UI
        print("[Main Window] Initializing loading manager...")
        self.loading_manager = LoadingManager(self.root)
        print("[Main Window] Loading manager initialized")
        
        # NOW show the window FIRST so geometry is correct
        self.root.deiconify()
        print("[Main Window] Window shown (deiconified) with loading screen")
        self.root.update()
        self.root.update_idletasks()  # Ensure all rendering is complete
        print("[Main Window] Window fully rendered")
        
        # THEN start the loading screen with correct geometry
        self.loading_manager.start_loading()
        print("[Main Window] Loading screen started with correct geometry")
        
        # Initialize core systems
        self.loading_manager.update_loading("Initializing core systems...", 15)
        self.canvas = Canvas(32, 32, zoom=16)  # Higher zoom for better grid visibility
        self.palette = ColorPalette()
        self.layer_manager = LayerManager(32, 32)
        self.undo_manager = UndoManager()
        self.undo_manager.on_state_changed = self._update_undo_redo_buttons
        self.timeline = AnimationTimeline(32, 32)
        
        # Initialize responsive panel sizing
        # ALWAYS use 510px panel widths for consistent UI
        temp_canvas_ops = CanvasOperationsManager(self.root, self.canvas, None)
        self.left_panel_width, self.right_panel_width = temp_canvas_ops.calculate_optimal_panel_widths()
        print(f"[Main Window] Using panel widths: {self.left_panel_width}x{self.right_panel_width}")
        
        # Initialize custom colors manager
        self.loading_manager.update_loading("Loading color systems...", 25)
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
        self.loading_manager.update_loading("Setting up drawing tools...", 35)
        from src.tools.edge import EdgeTool
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
        
        # Copy preview position (EventDispatcher needs this)
        self.copy_preview_pos = None  # Mouse position for copy preview
        
        # Scale state for EventDispatcher (points to selection_mgr)
        self.scale_start_pos = None
        
        # Pan state
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        # Initialize theme dialog manager
        self.theme_dialog_manager = ThemeDialogManager(self)
        
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
        print("[Main Window] Creating UI...")
        self.loading_manager.update_loading("Building user interface...", 50)
        self._create_ui()
        print("[Main Window] UI created")
        
        # Apply initial theme (Basic Grey) to all UI elements IMMEDIATELY after UI creation
        print("[Main Window] Applying theme...")
        self.loading_manager.update_loading("Applying theme...", 60)
        self.theme_dialog_manager.apply_theme(self.theme_manager.get_current_theme())
        print("[Main Window] Theme applied")

        # Initialize canvas operations manager (after UI creation)
        print("[Main Window] Initializing canvas operations manager...")
        self.loading_manager.update_loading("Initializing canvas...", 70)
        self.canvas_ops_mgr = CanvasOperationsManager(self.root, self.canvas, self.drawing_canvas)
        self.canvas_ops_mgr.left_container = self.left_container
        self.canvas_ops_mgr.right_container = self.right_container
        self.canvas_ops_mgr.update_canvas_callback = self.canvas_renderer.update_pixel_display
        print("[Main Window] Canvas operations manager initialized")
        
        # Initialize canvas scrollbar (zoom control on right side of canvas)
        print("[Main Window] Initializing canvas scrollbar...")
        self.canvas_scrollbar = CanvasScrollbar(
            self.drawing_canvas,
            self.theme_manager,
            self._on_scrollbar_zoom_change
        )
        print("[Main Window] Canvas scrollbar initialized")
        
        # Update tool selection to highlight brush
        print("[Main Window] Updating tool selection...")
        self.loading_manager.update_loading("Configuring tools...", 80)
        self._update_tool_selection()
        print("[Main Window] Tool selection updated")
        
        # Initialize palette views and show grid (only once)
        print("[Main Window] Initializing palette views...")
        self.loading_manager.update_loading("Setting up palette views...", 85)
        self._initialize_all_views()
        print("[Main Window] Palette views initialized")
        print("[Main Window] Showing grid view...")
        self._show_view("grid")
        print("[Main Window] Grid view shown")
        
        # Initialize canvas integration
        print("[Main Window] Syncing canvas with layers...")
        self.loading_manager.update_loading("Finalizing...", 95)
        self._sync_canvas_with_layers()
        print("[Main Window] Canvas synced with layers")

        # Complete loading after everything is initialized
        print("[Main Window] Completing loading...")
        # Delay completion until after window is fully rendered and visible
        self.root.after(100, self._finish_loading)

    def _finish_loading(self):
        """Finish the loading process after window is fully rendered"""
        print("[Main Window] Finishing loading process...")
        self.loading_manager.finish_loading()
        print("[Main Window] Loading completed")
        
        # Force a final update to ensure everything is visible
        self.root.update_idletasks()
        # Final update to render the window after loading screen is hidden
        self.root.after(100, lambda: [self.root.update(), print("[Main Window] Window fully rendered and visible")])

    
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
        self.canvas_frame.pack(fill="both", expand=True, side="left")
        
        # Notes panel (hidden by default)
        self.notes_panel = NotesPanel(canvas_container, self)
        self.notes_panel.hide()
        
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
        # Set tool size manager references and callbacks
        self.tool_size_mgr.tool_buttons = self.tool_buttons
        self.tool_size_mgr.select_tool_callback = self._select_tool
        
        # Update edge button text to show current thickness
        self.tool_size_mgr.update_edge_button_text()
        
        # Update brush and eraser button text to show default sizes
        self.tool_size_mgr.update_brush_button_text()
        self.tool_size_mgr.update_eraser_button_text()
        
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
        self.grid_control_mgr.force_canvas_update_callback = self.canvas_renderer.force_canvas_update
        
        # Set background control manager references and callbacks
        self.background_control_mgr.background_mode_button = self.ui_builder.widgets['background_mode_button']
        self.background_control_mgr.force_canvas_update_callback = self.canvas_renderer.force_canvas_update
        
        # Initialize grid button states
        self.grid_control_mgr.update_grid_button_text()
        self.grid_control_mgr.update_grid_overlay_button_text()
        self.grid_control_mgr.update_grid_mode_button()
        
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
        print("[Main Window] Skipping window state restoration during loading")
        
        # Initialize color view manager
        self.color_view_mgr = ColorViewManager(
            self.root, self.palette, self.theme_manager, 
            self.custom_colors, self.left_panel
        )
        # Set UI component references
        self.color_view_mgr.palette_content_frame = self.palette_content_frame
        self.color_view_mgr.color_display_frame = self.color_display_frame
        self.color_view_mgr.saved_view_frame = self.saved_view_frame
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
            'undo': self._undo,
            'redo': self._redo,
            'on_theme_selected': self._on_theme_selected,
            'show_settings_dialog': self.theme_dialog_manager.show_settings_dialog,
            'toggle_grid': self.grid_control_mgr.toggle_grid,
            'toggle_grid_overlay': self.grid_control_mgr.toggle_grid_overlay,
            'toggle_grid_mode': self.grid_control_mgr.toggle_grid_mode,
            'toggle_background_mode': self.background_control_mgr.toggle_background_mode,
            'toggle_notes': self._toggle_notes,
            'select_tool': self._select_tool,
            'update_tool_selection': self._update_tool_selection,
            'show_brush_size_menu': self.tool_size_mgr.show_brush_size_menu,
            'show_eraser_size_menu': self.tool_size_mgr.show_eraser_size_menu,
            'show_edge_thickness_menu': self.tool_size_mgr.show_edge_thickness_menu,
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

    def _purge_canvas_overlays(self):
        """Delete all transient canvas overlays and clear edge tool previews/lines.
        This is a safety purge to resolve any 'immortal' overlay items that may
        survive redraws due to tag ordering or throttled redraws.
        """
        if hasattr(self, 'drawing_canvas') and self.drawing_canvas:
            # Remove all known transient tags
            for tag in [
                "edge_preview", "edge_lines", "shape_preview", "brush_preview",
                "eraser_preview", "texture_preview", "selection", "move_preview",
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
                    print("[TOOL SWITCH] Finalized pending move operation")
            
            selection_tool = self.tools.get("selection")
            move_tool = self.tools.get("move")
            if selection_tool and selection_tool.has_selection:
                selection_tool.clear_selection()
                # Reset move tool state when clearing selection
                if move_tool:
                    move_tool.reset_state()
                self.canvas_renderer.update_pixel_display()
                print("[TOOL SWITCH] Selection cleared and move tool reset - switched to different tool")
        
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
        """Initialize all palette views once at startup - delegates to color view manager"""
        if hasattr(self, 'color_view_mgr'):
            self.color_view_mgr.initialize_all_views()
            return
        
        # Fallback if manager not ready yet (OLD IMPLEMENTATION)"""
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
        
        # Note: color_display_frame should remain as the palette container, not left_panel
    
    def _show_view(self, mode: str):
        """Show specific view - delegates to color view manager"""
        if hasattr(self, 'color_view_mgr'):
            self.color_view_mgr.show_view(mode)
            return
        
        # Fallback if manager not ready yet (OLD IMPLEMENTATION)"""
        # Hide all view frames first
        for frame_name in ['grid_view_frame', 'primary_view_frame', 'wheel_view_frame', 
                          'constants_view_frame', 'saved_view_frame']:
            if hasattr(self, frame_name):
                frame = getattr(self, frame_name)
                if frame:
                    frame.pack_forget()
        
        # Clear palette_content_frame for views that use it
        if hasattr(self, 'palette_content_frame') and self.palette_content_frame:
            for widget in self.palette_content_frame.winfo_children():
                widget.destroy()
            # Hide the palette_content_frame itself (it's the empty box!)
            self.palette_content_frame.pack_forget()
        
        # Show requested view
        if mode == "grid" and hasattr(self, 'grid_view') and self.grid_view:
            # Pack palette_content_frame before color_display_container (maintains order)
            self.palette_content_frame.pack(fill="x", expand=False, padx=10, pady=0, 
                                           before=self.color_display_frame if hasattr(self, 'color_display_frame') else None)
            self.grid_view.create()
        elif mode == "primary" and hasattr(self, 'primary_view') and self.primary_view:
            # Pack palette_content_frame before color_display_container (maintains order)
            self.palette_content_frame.pack(fill="x", expand=False, padx=10, pady=0,
                                           before=self.color_display_frame if hasattr(self, 'color_display_frame') else None)
            self.primary_view.create()
        elif mode == "wheel":
            # Pack palette_content_frame before color_display_container (maintains order)
            self.palette_content_frame.pack(fill="x", expand=False, padx=10, pady=0,
                                           before=self.color_display_frame if hasattr(self, 'color_display_frame') else None)
            # Recreate color wheel since it was destroyed when clearing the frame
            from src.ui.color_wheel import ColorWheel
            self.color_wheel = ColorWheel(self.palette_content_frame, theme=self.theme_manager.current_theme)
            self.color_wheel.on_color_changed = self._on_color_wheel_changed
            self.color_wheel.on_save_custom_color = self._save_custom_color
            self.color_wheel.on_remove_custom_color = self._remove_custom_color
        elif mode == "constants" and hasattr(self, 'constants_view') and self.constants_view:
            # Pack palette_content_frame before color_display_container (maintains order)
            self.palette_content_frame.pack(fill="x", expand=False, padx=10, pady=0,
                                           before=self.color_display_frame if hasattr(self, 'color_display_frame') else None)
            self.constants_view.create()
        elif mode == "saved" and hasattr(self, 'saved_view') and self.saved_view:
            # Pack saved view frame to fill the container (removes blank space)
            self.saved_view_frame.pack(fill="both", expand=True, pady=(0, 0), before=None)
            self.saved_view.create()
            # Update button states in case colors changed
            if hasattr(self, '_saved_view_created') and self._saved_view_created:
                self._update_saved_color_buttons()
            
            # Force scroll to absolute top
            self.left_panel._parent_canvas.yview_moveto(0)
            self.root.after(10, lambda: self.left_panel._parent_canvas.yview_moveto(0))
    
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
            print(f"[ERROR] Failed to show import dialog: {e}")
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
                
                print(f"[IMPORT] {message}")
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
    
    def _on_window_close(self):
        """Handle window close event - save state before closing"""
        print("[Window State] Application closing, saving window state...")
        self._save_window_state()
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
