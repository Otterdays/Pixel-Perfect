"""
UI Builder for Pixel Perfect
Extracts UI creation logic from the main window to a dedicated builder class.
This is part of a major refactoring effort to modularize the codebase.
"""

import customtkinter as ctk
import os
from PIL import Image
from typing import Dict, Callable
from ui.tooltip import create_tooltip

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
            values=["16x16", "32x32", "16x32", "32x64", "64x64", "Custom..."],
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
            values=["0.25x", "0.5x", "1x", "2x", "4x", "8x", "16x", "32x"],
            command=self.callbacks['on_zoom_change']
        )
        self.widgets['zoom_menu'].pack(side="left", padx=5)
        
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

        # Grid toggles
        self.widgets['grid_button'] = ctk.CTkButton(self.widgets['toolbar'], text="Grid", width=60, command=self.callbacks['toggle_grid'])
        self.widgets['grid_button'].pack(side="right", padx=5)
        
        self.widgets['grid_overlay_button'] = ctk.CTkButton(self.widgets['toolbar'], text="Grid Overlay", width=90, command=self.callbacks['toggle_grid_overlay'])
        self.widgets['grid_overlay_button'].pack(side="right", padx=5)

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
