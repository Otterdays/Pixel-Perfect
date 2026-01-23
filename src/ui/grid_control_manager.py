"""
Grid Control Manager
Handles grid visibility and overlay controls

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

class GridControlManager:
    """Manages grid visibility and overlay mode controls"""
    
    def __init__(self, canvas, theme_manager):
        """
        Initialize grid control manager
        
        Args:
            canvas: Canvas instance with grid controls
            theme_manager: ThemeManager instance for button colors
        """
        self.canvas = canvas
        self.theme_manager = theme_manager
        self.grid_overlay = False  # Grid overlay mode (grid on top of pixels)
        
        # Callbacks (set by main_window after initialization)
        self.force_canvas_update_callback = None
        
        # Widget references (set by main_window after UI creation)
        self.grid_button = None
        self.grid_overlay_button = None
        self.grid_mode_button = None
        self.tile_seam_button = None
    
    def toggle_grid(self):
        """Toggle grid visibility"""
        self.canvas.toggle_grid()
        self.update_grid_button_text()
        if self.force_canvas_update_callback:
            self.force_canvas_update_callback()
    
    def update_grid_button_text(self):
        """Update grid button text to show current state"""
        if self.grid_button:
            if self.canvas.show_grid:
                self.grid_button.configure(text="Grid: ON")
                self.grid_button.configure(fg_color="green")
            else:
                self.grid_button.configure(text="Grid: OFF")
                self.grid_button.configure(fg_color="red")
    
    def toggle_grid_overlay(self):
        """Toggle grid overlay mode (grid on top of pixels)"""
        self.grid_overlay = not self.grid_overlay
        self.update_grid_overlay_button_text()
        if self.force_canvas_update_callback:
            self.force_canvas_update_callback()
    
    def update_grid_overlay_button_text(self):
        """Update grid overlay button text to show current state"""
        if self.grid_overlay_button:
            if self.grid_overlay:
                self.grid_overlay_button.configure(text="Overlay: ON")
                self.grid_overlay_button.configure(fg_color="#1f538d")
            else:
                self.grid_overlay_button.configure(text="Overlay: OFF")
                self.grid_overlay_button.configure(fg_color=self.theme_manager.get_current_theme().button_normal)
    
    def toggle_grid_mode(self):
        """Toggle between auto, dark, light, and paper grid modes"""
        if self.canvas.grid_mode == "auto":
            self.canvas.grid_mode = "dark"
        elif self.canvas.grid_mode == "dark":
            self.canvas.grid_mode = "light"
        elif self.canvas.grid_mode == "light":
            self.canvas.grid_mode = "paper"
        else:  # paper
            self.canvas.grid_mode = "auto"
        
        self.update_grid_mode_button()
        if self.force_canvas_update_callback:
            self.force_canvas_update_callback()

    def update_grid_mode_button(self):
        """Update grid mode button icon and appearance"""
        if self.grid_mode_button:
            theme = self.theme_manager.get_current_theme()
            
            # Determine if current theme is light or dark
            is_light_theme = theme.name in ["Angelic", "American"]
            
            # Choose icon based on current mode and theme
            if self.canvas.grid_mode == "auto":
                icon = "🌓"  # Auto mode - half moon
                tooltip = f"Grid Mode: Auto ({'Light' if is_light_theme else 'Dark'} theme)"
            elif self.canvas.grid_mode == "dark":
                icon = "🌙"  # Dark mode - moon
                tooltip = "Grid Mode: Dark"
            elif self.canvas.grid_mode == "light":
                icon = "☀️"  # Light mode - sun
                tooltip = "Grid Mode: Light"
            else:  # paper
                icon = "📄"  # Paper mode - document
                tooltip = "Grid Mode: Paper Texture"
            
            # Update button
            self.grid_mode_button.configure(text=icon)
            
            # Update tooltip if possible
            try:
                from src.ui.tooltip import update_tooltip
                update_tooltip(self.grid_mode_button, tooltip)
            except (ImportError, AttributeError):
                # Tooltip update not available, that's okay
                pass
            
            # Set button color based on mode
            if self.canvas.grid_mode == "auto":
                self.grid_mode_button.configure(fg_color=theme.button_active)
            else:
                self.grid_mode_button.configure(fg_color=theme.button_normal)
    
    def toggle_tile_seam_preview(self):
        """Toggle tile seam preview (shows edge mismatches for tiling)"""
        self.canvas.show_tile_seam_preview = not self.canvas.show_tile_seam_preview
        self.update_tile_seam_button_text()
        if self.force_canvas_update_callback:
            self.force_canvas_update_callback()
    
    def update_tile_seam_button_text(self):
        """Update tile seam preview button text to show current state"""
        if self.tile_seam_button:
            if self.canvas.show_tile_seam_preview:
                self.tile_seam_button.configure(text="Seam: ON")
                self.tile_seam_button.configure(fg_color="#ff6600")  # Orange for visibility
            else:
                self.tile_seam_button.configure(text="Seam: OFF")
                self.tile_seam_button.configure(fg_color=self.theme_manager.get_current_theme().button_normal)

