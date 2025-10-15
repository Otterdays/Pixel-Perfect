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

