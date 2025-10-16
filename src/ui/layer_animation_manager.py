"""
Layer and Animation Manager
Handles layer operations and animation timeline coordination

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import customtkinter as ctk
from typing import Optional


class LayerAnimationManager:
    """Manages layer operations and animation timeline coordination"""
    
    def __init__(self, root, canvas, layer_manager, timeline, layer_panel, timeline_panel):
        """
        Initialize layer and animation manager
        
        Args:
            root: Main tkinter root window
            canvas: Canvas object with pixel data
            layer_manager: LayerManager instance
            timeline: AnimationTimeline instance
            layer_panel: LayerPanel UI component
            timeline_panel: TimelinePanel UI component
        """
        self.root = root
        self.canvas = canvas
        self.layer_manager = layer_manager
        self.timeline = timeline
        self.layer_panel = layer_panel
        self.timeline_panel = timeline_panel
        
        # Callbacks (set by main_window after init)
        self.update_canvas_callback = None
        self.clear_selection_callback = None
        self.update_pixel_display_callback = None
    
    def create_layer_and_timeline_panels(self, right_panel, theme_manager):
        """
        Create layer and animation timeline panels
        
        Args:
            right_panel: Parent panel for layers/timeline
            theme_manager: ThemeManager instance
            
        Returns:
            tuple: (layer_panel, timeline_panel) UI components
        """
        from ui.layer_panel import LayerPanel
        from ui.timeline_panel import TimelinePanel
        
        theme = theme_manager.current_theme
        
        # Layer panel
        layer_section = ctk.CTkFrame(right_panel, fg_color="transparent")
        layer_section.pack(fill="both", expand=True, pady=(0, 5))
        
        # Layer section title
        layer_title_frame = ctk.CTkFrame(layer_section, fg_color="transparent")
        layer_title_frame.pack(fill="x", padx=10, pady=(5, 2))
        
        layer_title = ctk.CTkLabel(
            layer_title_frame,
            text="Layers",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=theme.text_primary
        )
        layer_title.pack(side="left")
        
        # Add Layer button (+ icon)
        add_layer_btn = ctk.CTkButton(
            layer_title_frame,
            text="+",
            width=30,
            height=28,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=theme.button_active,
            hover_color=theme.button_hover,
            command=self.add_layer
        )
        add_layer_btn.pack(side="right")
        
        # Layer panel container
        layer_panel_container = ctk.CTkFrame(layer_section, fg_color=theme.bg_secondary)
        layer_panel_container.pack(fill="both", expand=True, padx=10, pady=2)
        
        # Create layer panel
        layer_panel = LayerPanel(layer_panel_container, self.layer_manager)
        layer_panel.on_layer_changed = self.on_layer_changed
        
        # Animation section
        anim_section = ctk.CTkFrame(right_panel, fg_color="transparent")
        anim_section.pack(fill="x", pady=(5, 10))
        
        # Animation section title
        anim_title_frame = ctk.CTkFrame(anim_section, fg_color="transparent")
        anim_title_frame.pack(fill="x", padx=10, pady=(0, 2))
        
        anim_title = ctk.CTkLabel(
            anim_title_frame,
            text="Animation",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=theme.text_primary
        )
        anim_title.pack(side="left")
        
        # Timeline panel container
        timeline_panel_container = ctk.CTkFrame(anim_section, fg_color=theme.bg_secondary)
        timeline_panel_container.pack(fill="x", padx=10, pady=2)
        
        # Create timeline panel
        timeline_panel = TimelinePanel(timeline_panel_container, self.timeline)
        timeline_panel.on_frame_changed = self.on_frame_changed
        timeline_panel.on_play_pause = self.toggle_animation
        timeline_panel.on_previous_frame = self.previous_frame
        timeline_panel.on_next_frame = self.next_frame
        
        return layer_panel, timeline_panel
    
    def on_layer_changed(self):
        """Handle layer change callback"""
        if self.update_canvas_callback:
            self.update_canvas_callback()
    
    def add_layer(self):
        """Add a new layer"""
        if self.layer_manager.add_layer():
            self.layer_panel.refresh()
            self.on_layer_changed()
    
    def sync_canvas_with_layers(self):
        """Sync canvas with layer manager"""
        # Update layer manager canvas size
        self.layer_manager.resize_layers(self.canvas.width, self.canvas.height)
        
        # Set canvas pixels from active layer
        active_layer = self.layer_manager.get_active_layer()
        if active_layer:
            self.canvas.pixels = active_layer.pixels.copy()
            self.canvas._redraw_surface()
    
    def on_frame_changed(self):
        """Handle frame change in timeline"""
        current_frame = self.timeline.get_current_frame()
        if current_frame:
            # Update canvas with current frame pixels
            self.canvas.pixels = current_frame.pixels.copy()
            self.canvas._redraw_surface()
            # Update the tkinter display
            if self.update_pixel_display_callback:
                self.update_pixel_display_callback()
    
    def toggle_animation(self):
        """Toggle animation playback"""
        if self.timeline.is_playing:
            self.timeline.pause()
        else:
            self.timeline.play()
        self.timeline_panel.refresh()
    
    def previous_frame(self):
        """Go to previous frame"""
        self.timeline.previous_frame()
        self.timeline_panel.refresh()
        self.on_frame_changed()
    
    def next_frame(self):
        """Go to next frame"""
        self.timeline.next_frame()
        self.timeline_panel.refresh()
        self.on_frame_changed()
    
    def update_canvas_from_layers(self):
        """Update canvas display from all layers"""
        if self.update_canvas_callback:
            self.update_canvas_callback()
    
    def clear_selection_and_reset_tools(self):
        """Clear selection box and reset tool states"""
        if self.clear_selection_callback:
            self.clear_selection_callback()
    
    def get_drawing_layer(self):
        """
        Get the layer to draw on
        
        Returns:
            Layer object or None
        """
        # If a specific layer is selected, use it
        if self.layer_manager.active_layer_index is not None:
            return self.layer_manager.get_active_layer()
        
        # Otherwise, if in "show all layers" mode (active_layer_index is None),
        # we'll draw on the first layer (background)
        if len(self.layer_manager.layers) > 0:
            return self.layer_manager.layers[0]
        
        return None

