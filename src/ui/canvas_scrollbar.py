"""
Canvas Scrollbar Widget for Pixel Perfect
Provides draggable scrollbar for canvas zoom control with +/- buttons

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import customtkinter as ctk
import tkinter as tk


class CanvasScrollbar:
    """Custom scrollbar widget for canvas zoom control"""
    
    def __init__(self, parent_canvas, theme_manager, on_zoom_callback):
        """
        Initialize the canvas scrollbar
        
        Args:
            parent_canvas: The tkinter canvas to overlay scrollbar on
            theme_manager: Theme manager for color matching
            on_zoom_callback: Function to call when zoom changes (takes zoom_level_float as arg)
        """
        self.parent_canvas = parent_canvas
        self.theme_manager = theme_manager
        self.on_zoom_callback = on_zoom_callback
        
        # Zoom levels configuration
        self.zoom_levels = [0.25, 0.5, 1, 2, 4, 8, 16, 32, 64]
        self.current_zoom_index = 4  # Default to 4x
        
        # Scrollbar dimensions
        self.scrollbar_width = 20
        self.button_height = 20
        self.handle_min_height = 15
        
        # State tracking
        self.is_dragging = False
        self.drag_start_y = 0
        self.handle_y = 0
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        """Create scrollbar UI components"""
        # Get current theme
        theme = self.theme_manager.get_current_theme()
        
        # Bind canvas resize to update scrollbar position
        self.parent_canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Bind mouse wheel events
        self.parent_canvas.bind("<MouseWheel>", self._on_mouse_wheel_internal)
        self.parent_canvas.bind("<Button-4>", self._on_mouse_wheel_internal)
        self.parent_canvas.bind("<Button-5>", self._on_mouse_wheel_internal)
        
        # Bind draw after to render scrollbar
        self.parent_canvas.bind("<Configure>", self._draw_scrollbar, add="+")
    
    def _on_canvas_configure(self, event):
        """Called when canvas is resized"""
        self._draw_scrollbar()
    
    def _draw_scrollbar(self, event=None):
        """Draw the scrollbar on canvas"""
        # Delete old scrollbar elements
        self.parent_canvas.delete("scrollbar_plus")
        self.parent_canvas.delete("scrollbar_minus")
        self.parent_canvas.delete("scrollbar_bg")
        self.parent_canvas.delete("scrollbar_handle")
        
        # Get canvas dimensions
        canvas_width = self.parent_canvas.winfo_width()
        canvas_height = self.parent_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            return
        
        # Get theme colors
        theme = self.theme_manager.get_current_theme()
        bg_color = theme.button_normal
        fg_color = theme.accent_color if hasattr(theme, 'accent_color') else "#0066ff"
        border_color = theme.button_hover
        
        # Calculate scrollbar position (right side, inset 15px)
        scrollbar_x = canvas_width - self.scrollbar_width - 15
        
        # Draw plus button (top)
        self.parent_canvas.create_rectangle(
            scrollbar_x, 10,
            scrollbar_x + self.scrollbar_width, 10 + self.button_height,
            fill=bg_color, outline=border_color, width=1,
            tags="scrollbar_plus"
        )
        self.parent_canvas.create_text(
            scrollbar_x + self.scrollbar_width // 2, 10 + self.button_height // 2,
            text="+", fill=fg_color, font=("Arial", 12, "bold"),
            tags="scrollbar_plus"
        )
        
        # Calculate scrollbar track
        track_top = 10 + self.button_height + 5
        track_bottom = canvas_height - 10 - self.button_height - 5
        track_height = max(track_bottom - track_top, 50)
        
        # Draw scrollbar background (track)
        self.parent_canvas.create_rectangle(
            scrollbar_x, track_top,
            scrollbar_x + self.scrollbar_width, track_bottom,
            fill=theme.bg_secondary, outline=border_color, width=1,
            tags="scrollbar_bg"
        )
        
        # Calculate handle position and size
        # Handle size scales with available zoom range
        zoom_range = len(self.zoom_levels) - 1
        handle_height = max(self.handle_min_height, int(track_height / (zoom_range + 1)))
        
        # Position handle based on current zoom
        available_track = track_height - handle_height
        position_ratio = self.current_zoom_index / zoom_range if zoom_range > 0 else 0
        self.handle_y = track_top + int(available_track * position_ratio)
        
        # Draw handle
        self.parent_canvas.create_rectangle(
            scrollbar_x + 2, self.handle_y,
            scrollbar_x + self.scrollbar_width - 2, self.handle_y + handle_height,
            fill=fg_color, outline=border_color, width=1,
            tags="scrollbar_handle"
        )
        
        # Draw minus button (bottom)
        self.parent_canvas.create_rectangle(
            scrollbar_x, canvas_height - 10 - self.button_height,
            scrollbar_x + self.scrollbar_width, canvas_height - 10,
            fill=bg_color, outline=border_color, width=1,
            tags="scrollbar_minus"
        )
        self.parent_canvas.create_text(
            scrollbar_x + self.scrollbar_width // 2, canvas_height - 10 - self.button_height // 2,
            text="−", fill=fg_color, font=("Arial", 12, "bold"),
            tags="scrollbar_minus"
        )
        
        # Bind mouse events on scrollbar elements
        self.parent_canvas.tag_bind("scrollbar_plus", "<Button-1>", self._on_plus_click)
        self.parent_canvas.tag_bind("scrollbar_minus", "<Button-1>", self._on_minus_click)
        self.parent_canvas.tag_bind("scrollbar_handle", "<Button-1>", self._on_handle_press)
        self.parent_canvas.tag_bind("scrollbar_handle", "<B1-Motion>", self._on_handle_drag)
        self.parent_canvas.tag_bind("scrollbar_handle", "<ButtonRelease-1>", self._on_handle_release)
    
    def _on_plus_click(self, event=None):
        """Handle plus button click"""
        if self.current_zoom_index < len(self.zoom_levels) - 1:
            self.current_zoom_index += 1
            self._apply_zoom()
    
    def _on_minus_click(self, event=None):
        """Handle minus button click"""
        if self.current_zoom_index > 0:
            self.current_zoom_index -= 1
            self._apply_zoom()
    
    def _on_handle_press(self, event):
        """Handle drag start on scrollbar handle"""
        self.is_dragging = True
        self.drag_start_y = event.y
    
    def _on_handle_drag(self, event):
        """Handle dragging scrollbar handle"""
        if not self.is_dragging:
            return
        
        # Get canvas height and calculate track bounds
        canvas_height = self.parent_canvas.winfo_height()
        track_top = 10 + self.button_height + 5
        track_bottom = canvas_height - 10 - self.button_height - 5
        
        # Calculate handle size
        zoom_range = len(self.zoom_levels) - 1
        handle_height = max(self.handle_min_height, int((track_bottom - track_top) / (zoom_range + 1)))
        
        # Calculate new handle position
        new_y = event.y - (self.drag_start_y - self.handle_y)
        new_y = max(track_top, min(new_y, track_bottom - handle_height))
        
        # Convert position to zoom index
        available_track = track_bottom - track_top - handle_height
        if available_track > 0:
            position_ratio = (new_y - track_top) / available_track
            new_index = round(position_ratio * zoom_range)
            new_index = max(0, min(new_index, zoom_range))
            
            if new_index != self.current_zoom_index:
                self.current_zoom_index = new_index
                self._apply_zoom()
    
    def _on_handle_release(self, event):
        """Handle drag end on scrollbar handle"""
        self.is_dragging = False
        self._draw_scrollbar()
    
    def _on_mouse_wheel_internal(self, event):
        """Handle mouse wheel events on canvas (internal to scrollbar)"""
        # Windows: event.delta > 0 = up, < 0 = down
        # Linux: event.num == 4 = up, == 5 = down
        
        if hasattr(event, 'delta'):
            # Windows
            if event.delta > 0:
                self._on_plus_click()
            else:
                self._on_minus_click()
        else:
            # Linux
            if event.num == 4:
                self._on_plus_click()
            elif event.num == 5:
                self._on_minus_click()
    
    def _apply_zoom(self):
        """Apply zoom change and redraw"""
        zoom_value = self.zoom_levels[self.current_zoom_index]
        self.on_zoom_callback(zoom_value)
        self._draw_scrollbar()
    
    def update_zoom_index(self, zoom_value: float):
        """Update scrollbar when zoom changes from other sources (dropdown, keyboard, etc)"""
        if zoom_value in self.zoom_levels:
            self.current_zoom_index = self.zoom_levels.index(zoom_value)
            self._draw_scrollbar()
    
    def update_theme(self):
        """Update colors when theme changes"""
        self._draw_scrollbar()
    
    def get_scrollbar_position(self):
        """Get current scrollbar handle position info"""
        return {
            'zoom_index': self.current_zoom_index,
            'zoom_level': self.zoom_levels[self.current_zoom_index],
            'is_max': self.current_zoom_index == len(self.zoom_levels) - 1,
            'is_min': self.current_zoom_index == 0
        }
