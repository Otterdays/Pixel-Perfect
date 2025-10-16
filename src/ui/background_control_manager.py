"""
Background Control Manager
Handles canvas background mode controls

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

class BackgroundControlManager:
    """Manages canvas background mode controls"""
    
    def __init__(self, canvas, theme_manager, canvas_renderer, main_window):
        """
        Initialize background control manager
        
        Args:
            canvas: Canvas instance with background controls
            theme_manager: ThemeManager instance for button colors
            canvas_renderer: CanvasRenderer instance for background color logic
            main_window: MainWindow instance for canvas widget access
        """
        self.canvas = canvas
        self.theme_manager = theme_manager
        self.canvas_renderer = canvas_renderer
        self.main_window = main_window
        
        # Callbacks (set by main_window after initialization)
        self.force_canvas_update_callback = None
        
        # Widget references (set by main_window after UI creation)
        self.background_mode_button = None
    
    def toggle_background_mode(self):
        """Toggle between auto, dark, and light background modes"""
        if self.canvas.background_mode == "auto":
            self.canvas.background_mode = "dark"
        elif self.canvas.background_mode == "dark":
            self.canvas.background_mode = "light"
        else:  # light
            self.canvas.background_mode = "auto"
        
        self.update_background_mode_button()
        
        # Immediately update canvas background color
        bg_color = self.canvas_renderer.get_background_color()
        self.main_window.drawing_canvas.configure(bg=bg_color)
        
        # Also trigger canvas update for any other elements
        if self.force_canvas_update_callback:
            self.force_canvas_update_callback()

    def update_background_mode_button(self):
        """Update background mode button icon and appearance"""
        if self.background_mode_button:
            theme = self.theme_manager.get_current_theme()
            
            # Determine if current theme is light or dark
            is_light_theme = theme.name in ["Angelic", "American"]
            
            # Choose icon based on current mode and theme
            if self.canvas.background_mode == "auto":
                icon = "🌗"  # Auto mode - half light/half dark
                tooltip = f"Background Mode: Auto ({'Light' if is_light_theme else 'Dark'} theme)"
            elif self.canvas.background_mode == "dark":
                icon = "⚫"  # Dark mode - black circle
                tooltip = "Background Mode: Dark"
            else:  # light
                icon = "⚪"  # Light mode - white circle
                tooltip = "Background Mode: Light"
            
            # Update button
            self.background_mode_button.configure(text=icon)
            
            # Set button color based on mode
            if self.canvas.background_mode == "auto":
                self.background_mode_button.configure(fg_color=theme.button_active)
            else:
                self.background_mode_button.configure(fg_color=theme.button_normal)
