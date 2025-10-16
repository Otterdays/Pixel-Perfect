"""
Color View Manager
Handles color view switching, color wheel creation, and custom colors management

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import customtkinter as ctk


class ColorViewManager:
    """Manages color view modes and custom colors"""
    
    def __init__(self, root, palette, theme_manager, custom_colors, left_panel):
        """
        Initialize color view manager
        
        Args:
            root: Main tkinter root window
            palette: ColorPalette instance
            theme_manager: ThemeManager instance
            custom_colors: CustomColorManager instance
            left_panel: Left panel scrollable frame
        """
        self.root = root
        self.palette = palette
        self.theme_manager = theme_manager
        self.custom_colors = custom_colors
        self.left_panel = left_panel
        
        # UI components (set after UI creation)
        self.palette_content_frame = None
        self.color_display_frame = None
        self.saved_view_frame = None
        self.view_mode_var = None
        self.color_wheel = None
        
        # View instances (set after initialization)
        self.grid_view = None
        self.primary_view = None
        self.saved_view = None
        self.constants_view = None
        
        # Callbacks
        self.update_canvas_callback = None
        self.select_tool_callback = None
    
    def initialize_all_views(self):
        """Initialize all palette views for instant switching"""
        # Initialize grid view
        if hasattr(self, 'grid_view') and self.grid_view:
            self.grid_view.create()
        
        # Initialize primary view
        if hasattr(self, 'primary_view') and self.primary_view:
            self.primary_view.create()
        
        # Color wheel is already created during initialization
        
        # Initialize saved view
        if hasattr(self, 'saved_view') and self.saved_view:
            self.saved_view.create()
        
        # Initialize constants view
        if hasattr(self, 'constants_view') and self.constants_view:
            self.constants_view.create()
    
    def show_view(self, mode: str):
        """Show specific view by toggling visibility (INSTANT)"""
        # Hide all view frames first
        for frame_name in ['grid_view_frame', 'primary_view_frame', 'wheel_view_frame', 
                          'constants_view_frame', 'saved_view_frame']:
            frame = getattr(self, frame_name, None)
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
            self.color_wheel.on_color_changed = self.on_color_wheel_changed
            self.color_wheel.on_save_custom_color = self.save_custom_color
            self.color_wheel.on_remove_custom_color = self.remove_custom_color
            
            # Update MainWindow's color wheel reference
            if hasattr(self, 'main_window') and self.main_window:
                self.main_window.color_wheel = self.color_wheel
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
            if hasattr(self.saved_view, 'update_buttons'):
                self.saved_view.update_buttons()
            
            # Force scroll to absolute top
            self.left_panel._parent_canvas.yview_moveto(0)
            self.root.after(10, lambda: self.left_panel._parent_canvas.yview_moveto(0))
    
    def on_view_mode_change(self):
        """Handle view mode change - now instant!"""
        mode = self.view_mode_var.get()
        self.show_view(mode)
    
    def create_color_wheel(self):
        """Create color wheel view"""
        # Clear existing widgets
        for widget in self.color_display_frame.winfo_children():
            widget.destroy()
        
        # Import and create color wheel
        from src.ui.color_wheel import ColorWheel
        self.color_wheel = ColorWheel(self.color_display_frame, theme=self.theme_manager.current_theme)
        self.color_wheel.on_color_changed = self.on_color_wheel_changed
        
        # Connect color wheel callbacks to custom colors management
        self.color_wheel.on_save_custom_color = self.save_custom_color
        self.color_wheel.on_remove_custom_color = self.remove_custom_color
        
        # Update custom colors grid with existing colors
        self.update_custom_colors_display()
    
    def on_color_wheel_changed(self, rgb_color):
        """Handle color wheel color change"""
        # Color wheel colors are NOT added to the palette grid
        # The get_current_color() method will get the color from the wheel when in wheel mode
        # This prevents colors from being added to the preset palette grid
        
        # Update color display in UI
        if self.update_canvas_callback:
            self.update_canvas_callback()
        
        # Auto-switch to brush tool for immediate painting
        if self.select_tool_callback:
            self.select_tool_callback("brush")
    
    def save_custom_color(self, rgb_color):
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
            self.update_custom_colors_display()
        else:
            if self.custom_colors.has_color(rgba_color):
                print(f"[WARN] Color already in custom colors: {rgba_color}")
            elif self.custom_colors.is_full():
                print(f"[WARN] Custom colors full (max {self.custom_colors.max_colors})")
    
    def remove_custom_color(self, color):
        """Remove a custom color"""
        if self.custom_colors.remove_color_by_value(color):
            print(f"[DELETE] Removed custom color: {color}")
            # Update the display
            self.update_custom_colors_display()
    
    def update_custom_colors_display(self):
        """Update custom colors display in color wheel"""
        if hasattr(self, 'color_wheel') and self.color_wheel:
            # Color wheel has its own method to update custom colors grid
            pass  # Color wheel updates itself via callbacks

