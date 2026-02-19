"""
UI Builder for Pixel Perfect
Extracts UI creation logic from the main window to a dedicated builder class.
This is part of a major refactoring effort to modularize the codebase.
"""

import customtkinter as ctk
import os
from PIL import Image
from typing import Dict, Callable
from src.ui.tooltip import create_tooltip

class UIBuilder:
    """Builds all UI components for the main window."""
    
    def __init__(self, parent, callbacks: Dict[str, Callable], theme_manager):
        """
        Initializes the UIBuilder.

        Args:
            parent: The parent widget (main_frame).
            callbacks: A dictionary of callback functions from the main window.
            theme_manager: The application's theme manager.
        """
        self.parent = parent
        self.callbacks = callbacks
        self.theme_manager = theme_manager
        self.widgets = {}  # Dictionary to store all created widgets
    def create_toolbar(self):
        """Create top toolbar"""
        self.widgets['toolbar'] = ctk.CTkFrame(self.parent)
        self.widgets['toolbar'].pack(fill="x", pady=(0, 10))
        
        # File menu
        self.widgets['file_button'] = ctk.CTkButton(self.widgets['toolbar'], text="File", width=60, command=self.callbacks['show_file_menu'])
        self.widgets['file_button'].pack(side="left", padx=5)
        
        # Canvas size selector
        self.widgets['size_label'] = ctk.CTkLabel(self.widgets['toolbar'], text="Size:")
        self.widgets['size_label'].pack(side="left", padx=(20, 5))
        
        self.widgets['size_var'] = ctk.StringVar(value="32x32")
        self.widgets['size_menu'] = ctk.CTkOptionMenu(
            self.widgets['toolbar'], 
            variable=self.widgets['size_var'],
            values=["8x8", "16x16", "32x32", "16x32", "32x64", "64x64", "128x128", "256x256", "Custom..."],
            command=self.callbacks['on_size_change']
        )
        self.widgets['size_menu'].pack(side="left", padx=5)
        
        # Zoom controls
        self.widgets['zoom_label'] = ctk.CTkLabel(self.widgets['toolbar'], text="Zoom:")
        self.widgets['zoom_label'].pack(side="left", padx=(20, 5))
        
        self.widgets['zoom_var'] = ctk.StringVar(value="16x")
        self.widgets['zoom_menu'] = ctk.CTkOptionMenu(
            self.widgets['toolbar'],
            variable=self.widgets['zoom_var'],
            values=["0.25x", "0.5x", "1x", "2x", "4x", "8x", "16x", "32x", "64x"],
            command=self.callbacks['on_zoom_change']
        )
        self.widgets['zoom_menu'].pack(side="left", padx=5)

        # Zoom utility buttons
        self.widgets['zoom_fit_button'] = ctk.CTkButton(
            self.widgets['toolbar'],
            text="Fit",
            width=50,
            command=self.callbacks['zoom_fit']
        )
        self.widgets['zoom_fit_button'].pack(side="left", padx=(8, 2))
        create_tooltip(self.widgets['zoom_fit_button'], "Fit canvas to view", delay=500)

        self.widgets['zoom_100_button'] = ctk.CTkButton(
            self.widgets['toolbar'],
            text="100%",
            width=60,
            command=self.callbacks['zoom_100']
        )
        self.widgets['zoom_100_button'].pack(side="left", padx=2)
        create_tooltip(self.widgets['zoom_100_button'], "Set zoom to 100%", delay=500)
        
        # Undo/Redo buttons
        self.create_undo_redo_buttons()
        
        # Theme selector with brand logo
        try:
            # This path needs to be relative to the main execution context
            logo_path = os.path.join("assets", "icons", "dcs.png")
            if os.path.exists(logo_path):
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((24, 24), Image.Resampling.LANCZOS)
                logo_ctk = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(24, 24))
                self.widgets['theme_label'] = ctk.CTkLabel(self.widgets['toolbar'], image=logo_ctk, text="")
            else:
                self.widgets['theme_label'] = ctk.CTkLabel(self.widgets['toolbar'], text="🎨", font=ctk.CTkFont(size=16))
        except Exception as e:
            print(f"[WARN] Could not load DCS logo for UIBuilder: {e}")
            self.widgets['theme_label'] = ctk.CTkLabel(self.widgets['toolbar'], text="🎨", font=ctk.CTkFont(size=16))
        
        self.widgets['theme_label'].pack(side="right", padx=(20, 2))
        create_tooltip(self.widgets['theme_label'], "Color Theme - Diamond Clad Studios", delay=1000)
        
        self.widgets['theme_var'] = ctk.StringVar(value="Basic Grey")
        self.widgets['theme_menu'] = ctk.CTkOptionMenu(
            self.widgets['toolbar'],
            variable=self.widgets['theme_var'],
            values=self.theme_manager.get_theme_names(),
            command=self.callbacks['on_theme_selected'],
            width=120
        )
        self.widgets['theme_menu'].pack(side="right", padx=5)
        
        # Notes button
        self.widgets['notes_button'] = ctk.CTkButton(
            self.widgets['toolbar'],
            text="Notes",
            width=60,
            command=self.callbacks['toggle_notes']
        )
        self.widgets['notes_button'].pack(side="right", padx=5)
        create_tooltip(self.widgets['notes_button'], "Toggle Notes Panel", delay=500)
        
        # Settings button
        self.widgets['settings_button'] = ctk.CTkButton(
            self.widgets['toolbar'], 
            text="⚙️", 
            width=40,
            command=self.callbacks['show_settings_dialog'],
            font=ctk.CTkFont(size=18)
        )
        self.widgets['settings_button'].pack(side="right", padx=5)
        create_tooltip(self.widgets['settings_button'], "Settings (Coming Soon)", delay=500)

        # Background mode toggle (new button)
        self.widgets['background_mode_button'] = ctk.CTkButton(
            self.widgets['toolbar'], 
            text="🌗",  # Default auto icon
            width=40,
            command=self.callbacks['toggle_background_mode'],
            font=ctk.CTkFont(size=16)
        )
        self.widgets['background_mode_button'].pack(side="right", padx=5)
        create_tooltip(self.widgets['background_mode_button'], "Background Mode: Auto", delay=500)
        
        # Grid mode toggle (new button)
        self.widgets['grid_mode_button'] = ctk.CTkButton(
            self.widgets['toolbar'], 
            text="🌓",  # Default auto icon
            width=40,
            command=self.callbacks['toggle_grid_mode'],
            font=ctk.CTkFont(size=16)
        )
        self.widgets['grid_mode_button'].pack(side="right", padx=5)
        create_tooltip(self.widgets['grid_mode_button'], "Grid Mode: Auto", delay=500)

        # Grid toggles
        self.widgets['grid_button'] = ctk.CTkButton(self.widgets['toolbar'], text="Grid", width=60, command=self.callbacks['toggle_grid'])
        self.widgets['grid_button'].pack(side="right", padx=5)
        
        self.widgets['grid_overlay_button'] = ctk.CTkButton(self.widgets['toolbar'], text="Grid Overlay", width=90, command=self.callbacks['toggle_grid_overlay'])
        self.widgets['grid_overlay_button'].pack(side="right", padx=5)
        
        self.widgets['tile_seam_button'] = ctk.CTkButton(self.widgets['toolbar'], text="Seam", width=70, command=self.callbacks.get('toggle_tile_seam', lambda: None))
        self.widgets['tile_seam_button'].pack(side="right", padx=5)
        
        # Tile preview button (shows repeating pattern preview)
        self.widgets['tile_preview_button'] = ctk.CTkButton(
            self.widgets['toolbar'], 
            text="Tile", 
            width=60, 
            command=self.callbacks.get('toggle_tile_preview', lambda: None)
        )
        self.widgets['tile_preview_button'].pack(side="right", padx=5)
        create_tooltip(self.widgets['tile_preview_button'], "Tile Preview: Show canvas repeated for pattern visualization", delay=500)

    def create_undo_redo_buttons(self):
        """Create undo/redo buttons in the toolbar"""
        undo_redo_frame = ctk.CTkFrame(self.widgets['toolbar'])
        undo_redo_frame.pack(side="left", padx=(20, 0))
        
        self.widgets['undo_button'] = ctk.CTkButton(
            undo_redo_frame,
            text="↶",
            width=40,
            height=30,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.callbacks['undo'],
            fg_color=("gray75", "gray25")
        )
        self.widgets['undo_button'].pack(side="left", padx=2)
        
        self.widgets['redo_button'] = ctk.CTkButton(
            undo_redo_frame,
            text="↷",
            width=40,
            height=30,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.callbacks['redo'],
            fg_color=("gray75", "gray25")
        )
        self.widgets['redo_button'].pack(side="left", padx=2)
    
    def create_tool_panel(self, left_panel, tool_buttons_ref, callbacks):
        """Create tool selection panel"""
        tool_frame = left_panel  # Use the panel directly, no container frame
        
        tool_label = ctk.CTkLabel(tool_frame, text="Tools", font=ctk.CTkFont(size=16, weight="bold"))
        tool_label.pack(pady=(15, 3), padx=10)
        
        # Tool buttons container for grid layout
        tool_grid = ctk.CTkFrame(tool_frame, fg_color="transparent")
        tool_grid.pack(pady=(0, 5), padx=5)
        
        # Tool buttons in 3x3 grid for compact layout
        tool_buttons = {}
        tools = [
            ("brush", "Brush", "Draw pixels (B) | Right-click for size"),
            ("dither", "Dither", "Checkerboard pattern brush"),
            ("eraser", "Eraser", "Erase pixels (E) | Right-click for size"),
            ("spray", "Spray", "Spray paint (Y) | Right-click for radius/density"),
            ("fill", "Fill", "Fill areas with color (F)"),
            ("eyedropper", "Eyedropper", "Sample colors from canvas (I)"),
            ("selection", "Select", "Select rectangular areas (S)"),
            ("magic_wand", "Wand", "Select by color similarity (W)"),
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
                command=lambda t=tool_id: callbacks['select_tool'](t)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            tool_buttons[tool_id] = btn
            
            # Add right-click menu for brush size
            if tool_id == "brush":
                btn.bind("<Button-3>", callbacks['show_brush_size_menu'])
            
            # Add right-click menu for eraser size
            if tool_id == "eraser":
                btn.bind("<Button-3>", callbacks['show_eraser_size_menu'])

            # Add right-click menu for spray radius/density
            if tool_id == "spray":
                btn.bind("<Button-3>", callbacks['show_spray_size_menu'])
            
            # Add right-click menu for edge thickness
            if tool_id == "edge":
                btn.bind("<Button-3>", callbacks['show_edge_thickness_menu'])
            
            # Add tooltip
            create_tooltip(btn, tooltip_text, delay=1000)
        
        # Note: Button text updates will be called after UIBuilder completes
        
        # Texture button (squished to make room for Edge button)
        texture_btn = ctk.CTkButton(
            tool_grid,
            text="Texture",
            width=85,  # Reduced from 175px to standard button size
            height=28,
            command=callbacks['open_texture_panel']
        )
        # Place Texture on a new row to avoid overlapping Pan
        texture_btn.grid(row=4, column=1, padx=2, pady=2)
        tool_buttons["texture"] = texture_btn  # Add to tool buttons for highlighting
        create_tooltip(texture_btn, "Open texture panel (T)", delay=1000)
        
        # Edge button (new tool for drawing edges around pixel shapes)
        edge_btn = ctk.CTkButton(
            tool_grid,
            text="Edge",
            width=85,
            height=28,
            command=lambda: callbacks['select_tool']('edge')
        )
        # Place Edge on the new row as well
        edge_btn.grid(row=4, column=2, padx=2, pady=2)
        tool_buttons["edge"] = edge_btn
        create_tooltip(edge_btn, "Draw edges around pixel shapes (G) | Right-click for thickness", delay=1000)
        # Bind right-click on Edge button to open thickness menu (parity with brush/eraser)
        edge_btn.bind("<Button-3>", callbacks['show_edge_thickness_menu'])
        
        # Configure grid columns - buttons stay fixed size
        for col in range(3):
            tool_grid.grid_columnconfigure(col, weight=0)
        
        # Highlight current tool
        callbacks['update_tool_selection']()
        
        # Selection operations section
        selection_ops_label = ctk.CTkLabel(tool_frame, text="Selection", font=ctk.CTkFont(size=14, weight="bold"))
        selection_ops_label.pack(pady=(10, 3))
        
        # Selection operations buttons in 3 columns
        selection_ops_grid = ctk.CTkFrame(tool_frame, fg_color="transparent")
        selection_ops_grid.pack(pady=(0, 5), padx=5)
        
        # Create selection operation buttons
        mirror_btn = ctk.CTkButton(
            selection_ops_grid,
            text="Mirror",
            width=85,
            height=28,
            command=callbacks['mirror_selection']
        )
        mirror_btn.grid(row=0, column=0, padx=2, pady=2)
        create_tooltip(mirror_btn, "Flip selection horizontally", delay=1000)
        
        rotate_btn = ctk.CTkButton(
            selection_ops_grid,
            text="Rotate",
            width=85,
            height=28,
            command=callbacks['rotate_selection']
        )
        rotate_btn.grid(row=0, column=1, padx=2, pady=2)
        create_tooltip(rotate_btn, "Rotate selection 90° clockwise", delay=1000)
        
        copy_btn = ctk.CTkButton(
            selection_ops_grid,
            text="Copy",
            width=85,
            height=28,
            command=callbacks['copy_selection']
        )
        copy_btn.grid(row=0, column=2, padx=2, pady=2)
        create_tooltip(copy_btn, "Copy selection for placement", delay=1000)
        
        # Second row for Scale button
        scale_btn = ctk.CTkButton(
            selection_ops_grid,
            text="Scale",
            width=85,
            height=28,
            command=callbacks['scale_selection']
        )
        scale_btn.grid(row=1, column=0, padx=2, pady=2, columnspan=3, sticky="ew")
        create_tooltip(scale_btn, "Scale selection with draggable corners", delay=1000)
        
        # Store references
        selection_buttons = {
            'mirror_btn': mirror_btn,
            'rotate_btn': rotate_btn,
            'copy_btn': copy_btn,
            'scale_btn': scale_btn
        }
        
        # Configure grid columns
        for col in range(3):
            selection_ops_grid.grid_columnconfigure(col, weight=0)
            
        # Symmetry section
        symmetry_label = ctk.CTkLabel(tool_frame, text="Symmetry", font=ctk.CTkFont(size=14, weight="bold"))
        symmetry_label.pack(pady=(10, 3))
        
        symmetry_grid = ctk.CTkFrame(tool_frame, fg_color="transparent")
        symmetry_grid.pack(pady=(0, 5), padx=5)
        
        # Horizontal Symmetry Button
        sym_x_btn = ctk.CTkButton(
            symmetry_grid,
            text="Sym X",
            width=85,
            height=28,
            command=callbacks['toggle_symmetry_x']
        )
        sym_x_btn.grid(row=0, column=0, padx=2, pady=2)
        create_tooltip(sym_x_btn, "Toggle Horizontal Symmetry", delay=1000)
        
        # Vertical Symmetry Button
        sym_y_btn = ctk.CTkButton(
            symmetry_grid,
            text="Sym Y",
            width=85,
            height=28,
            command=callbacks['toggle_symmetry_y']
        )
        sym_y_btn.grid(row=0, column=1, padx=2, pady=2)
        create_tooltip(sym_y_btn, "Toggle Vertical Symmetry", delay=1000)
        
        # Store references for main window
        tool_buttons_ref.update(tool_buttons)
        return {
            'mirror_btn': mirror_btn,
            'rotate_btn': rotate_btn,
            'copy_btn': copy_btn,
            'scale_btn': scale_btn,
            'sym_x_btn': sym_x_btn,
            'sym_y_btn': sym_y_btn,
            'tool_frame': tool_frame
        }
    
    def create_palette_panel(self, left_panel, palette, callbacks):
        """Create color palette panel"""
        palette_frame = left_panel  # Use the panel directly, no container frame
        
        palette_label = ctk.CTkLabel(palette_frame, text="Palette", font=ctk.CTkFont(size=16, weight="bold"))
        palette_label.pack(pady=(15, 3), padx=10)
        
        # Palette selector
        available_names = palette.get_available_palette_names()
        default_palette_name = available_names[0] if available_names else palette.palette_name
        palette_var = ctk.StringVar(value=default_palette_name)
        palette_menu = ctk.CTkOptionMenu(
            palette_frame,
            variable=palette_var,
            values=available_names,
            command=callbacks['on_palette_change']
        )
        palette_menu.pack(pady=3, padx=10)
        
        # View mode selector - centered container (moved before content frame)
        view_mode_container = ctk.CTkFrame(palette_frame, fg_color="transparent")
        view_mode_container.pack(pady=3, padx=10)
        
        view_mode_frame = ctk.CTkFrame(view_mode_container, fg_color="transparent")
        view_mode_frame.pack()
        
        view_mode_var = ctk.StringVar(value="grid")
        
        # Create a grid layout for radio buttons - centered
        grid_view_btn = ctk.CTkRadioButton(
            view_mode_frame,
            text="Grid",
            variable=view_mode_var,
            value="grid",
            command=callbacks['on_view_mode_change']
        )
        grid_view_btn.grid(row=0, column=0, padx=5, pady=2)
        
        primary_view_btn = ctk.CTkRadioButton(
            view_mode_frame,
            text="Primary",
            variable=view_mode_var,
            value="primary",
            command=callbacks['on_view_mode_change']
        )
        primary_view_btn.grid(row=0, column=1, padx=5, pady=2)
        
        wheel_view_btn = ctk.CTkRadioButton(
            view_mode_frame,
            text="Wheel",
            variable=view_mode_var,
            value="wheel",
            command=callbacks['on_view_mode_change']
        )
        wheel_view_btn.grid(row=1, column=0, padx=5, pady=2)
        
        constants_view_btn = ctk.CTkRadioButton(
            view_mode_frame,
            text="Constants",
            variable=view_mode_var,
            value="constants",
            command=callbacks['on_view_mode_change']
        )
        constants_view_btn.grid(row=1, column=1, padx=5, pady=2)
        
        saved_view_btn = ctk.CTkRadioButton(
            view_mode_frame,
            text="Saved",
            variable=view_mode_var,
            value="saved",
            command=callbacks['on_view_mode_change']
        )
        saved_view_btn.grid(row=2, column=0, padx=5, pady=2)
        
        # Recent colors view button
        recent_view_btn = ctk.CTkRadioButton(
            view_mode_frame,
            text="Recent",
            variable=view_mode_var,
            value="recent",
            command=callbacks['on_view_mode_change']
        )
        recent_view_btn.grid(row=2, column=1, padx=5, pady=2)
        
        # Create a container frame for palette views (after radio buttons)
        palette_content_frame = ctk.CTkFrame(palette_frame, fg_color="transparent")
        palette_content_frame.pack(fill="x", expand=False, padx=10, pady=0)
        
        # Color display container - centered (no top padding to eliminate gap)
        color_display_container = ctk.CTkFrame(palette_frame, fg_color="transparent")
        color_display_container.pack(fill="both", expand=True, pady=0, padx=10)
        
        # Create container frames for each view (create once, toggle visibility)
        grid_view_frame = ctk.CTkFrame(color_display_container)
        primary_view_frame = ctk.CTkFrame(color_display_container)
        wheel_view_frame = ctk.CTkFrame(color_display_container)
        constants_view_frame = ctk.CTkFrame(color_display_container)
        saved_view_frame = ctk.CTkFrame(color_display_container)
        recent_view_frame = ctk.CTkFrame(color_display_container)  # New frame for recent colors
        
        # Keep reference to old color_display_frame for compatibility
        color_display_frame = grid_view_frame
        
        # Primary colors state (must be set BEFORE initializing views)
        primary_colors_mode = "primary"  # "primary" or "variations"
        selected_primary_color = None
        color_wheel = None
        
        # Note: initialize_all_views() and show_view() will be called after widget references are assigned
        
        # Return references for main window
        return {
            'palette_label': palette_label,
            'palette_frame': palette_frame,
            'palette_content_frame': palette_content_frame,
            'palette_var': palette_var,
            'palette_menu': palette_menu,
            'view_mode_var': view_mode_var,
            'grid_view_btn': grid_view_btn,
            'primary_view_btn': primary_view_btn,
            'wheel_view_btn': wheel_view_btn,
            'constants_view_btn': constants_view_btn,
            'saved_view_btn': saved_view_btn,
            'recent_view_btn': recent_view_btn,  # Add new button reference
            'color_display_container': color_display_container,
            'grid_view_frame': grid_view_frame,
            'primary_view_frame': primary_view_frame,
            'wheel_view_frame': wheel_view_frame,
            'constants_view_frame': constants_view_frame,
            'saved_view_frame': saved_view_frame,
            'recent_view_frame': recent_view_frame,  # Add new frame reference
            'color_display_frame': color_display_frame,
            'primary_colors_mode': primary_colors_mode,
            'selected_primary_color': selected_primary_color,
            'color_wheel': color_wheel
        }
    
    def create_canvas_panel(self, canvas_frame, canvas_renderer, current_tool, tools, callbacks):
        """Create canvas display panel"""
        canvas_label = ctk.CTkLabel(canvas_frame, text="Canvas", font=ctk.CTkFont(size=16, weight="bold"))
        canvas_label.pack(pady=10)

        # Canvas container
        canvas_container = ctk.CTkFrame(canvas_frame)
        canvas_container.pack(expand=True, fill="both", padx=20, pady=20)

        # Create tkinter Canvas for drawing (much simpler than pygame integration)
        drawing_canvas = ctk.CTkCanvas(
            canvas_container,
            bg="lightgray",
            highlightthickness=1,
            highlightbackground="black"
        )
        drawing_canvas.pack(expand=True, fill="both")
        # Mouse and focus events are now bound by EventDispatcher
        
        # Set initial cursor (brush tool is default)
        drawing_canvas.configure(cursor=tools[current_tool].cursor)

        # Initialize the drawing surface
        canvas_renderer.init_drawing_surface()
        
        # Return references for main window
        return {
            'canvas_container': canvas_container,
            'drawing_canvas': drawing_canvas
        }