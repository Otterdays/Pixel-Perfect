"""
Status Bar and Canvas HUD
Displays cursor position, tool info, zoom, layer, and other status information

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import customtkinter as ctk
import tkinter as tk
from typing import Optional


class StatusBar:
    """Bottom status bar showing application status"""
    
    def __init__(self, parent, theme_manager):
        """
        Initialize status bar
        
        Args:
            parent: Parent widget (main window frame)
            theme_manager: Theme manager for colors
        """
        self.theme_manager = theme_manager
        self.parent = parent
        
        # Create status bar frame
        self.status_frame = ctk.CTkFrame(
            parent,
            height=24,
            fg_color=self.theme_manager.get_current_theme().bg_secondary,
            corner_radius=0
        )
        self.status_frame.pack(side="bottom", fill="x", padx=0, pady=0)
        self.status_frame.pack_propagate(False)
        
        # Status sections
        self.cursor_label = ctk.CTkLabel(
            self.status_frame,
            text="X: --  Y: --",
            font=ctk.CTkFont(size=10),
            anchor="w"
        )
        self.cursor_label.pack(side="left", padx=(10, 20))
        
        self.tool_label = ctk.CTkLabel(
            self.status_frame,
            text="Tool: --",
            font=ctk.CTkFont(size=10),
            anchor="w"
        )
        self.tool_label.pack(side="left", padx=(0, 20))
        
        self.size_label = ctk.CTkLabel(
            self.status_frame,
            text="Size: --",
            font=ctk.CTkFont(size=10),
            anchor="w"
        )
        self.size_label.pack(side="left", padx=(0, 20))
        
        self.zoom_label = ctk.CTkLabel(
            self.status_frame,
            text="Zoom: --",
            font=ctk.CTkFont(size=10),
            anchor="w"
        )
        self.zoom_label.pack(side="left", padx=(0, 20))
        
        self.layer_label = ctk.CTkLabel(
            self.status_frame,
            text="Layer: --",
            font=ctk.CTkFont(size=10),
            anchor="w"
        )
        self.layer_label.pack(side="left", padx=(0, 20))
        
        self.frame_label = ctk.CTkLabel(
            self.status_frame,
            text="Frame: --",
            font=ctk.CTkFont(size=10),
            anchor="w"
        )
        self.frame_label.pack(side="left", padx=(0, 20))
        
        # Right side: status messages
        self.message_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=ctk.CTkFont(size=10),
            anchor="e"
        )
        self.message_label.pack(side="right", padx=(0, 10))
        
        # Apply theme
        self.apply_theme(self.theme_manager.get_current_theme())
    
    def apply_theme(self, theme):
        """Apply theme colors to status bar"""
        self.status_frame.configure(fg_color=theme.bg_secondary)
        text_color = theme.text_primary
        self.cursor_label.configure(text_color=text_color)
        self.tool_label.configure(text_color=text_color)
        self.size_label.configure(text_color=text_color)
        self.zoom_label.configure(text_color=text_color)
        self.layer_label.configure(text_color=text_color)
        self.frame_label.configure(text_color=text_color)
        self.message_label.configure(text_color=text_color)
    
    def update_cursor(self, x: int, y: int):
        """Update cursor position display"""
        self.cursor_label.configure(text=f"X: {x}  Y: {y}")
    
    def update_tool(self, tool_name: str):
        """Update tool name display"""
        display_name = tool_name.capitalize()
        self.tool_label.configure(text=f"Tool: {display_name}")
    
    def update_size(self, size: str):
        """Update tool size display"""
        self.size_label.configure(text=f"Size: {size}")
    
    def update_zoom(self, zoom: float):
        """Update zoom level display"""
        self.zoom_label.configure(text=f"Zoom: {zoom:.1f}x")
    
    def update_layer(self, layer_name: str, layer_index: Optional[int] = None):
        """Update active layer display"""
        if layer_index is not None:
            self.layer_label.configure(text=f"Layer: {layer_name} ({layer_index + 1})")
        else:
            self.layer_label.configure(text=f"Layer: {layer_name}")
    
    def update_frame(self, frame_index: int, total_frames: int):
        """Update current frame display"""
        self.frame_label.configure(text=f"Frame: {frame_index + 1}/{total_frames}")
    
    def show_message(self, message: str, duration: int = 3000):
        """Show temporary status message"""
        self.message_label.configure(text=message)
        if duration > 0:
            self.parent.after(duration, lambda: self.message_label.configure(text=""))


class CanvasHUD:
    """On-canvas mini HUD overlay"""
    
    def __init__(self, canvas_widget, theme_manager):
        """
        Initialize canvas HUD
        
        Args:
            canvas_widget: Tkinter canvas widget
            theme_manager: Theme manager for colors
        """
        self.canvas = canvas_widget
        self.theme_manager = theme_manager
        self.visible = False
        
        # HUD elements (drawn on canvas)
        self.hud_tag = "canvas_hud"
        
        # Default position (top-left)
        self.hud_x = 10
        self.hud_y = 10
        
        # Current values
        self.cursor_x = None
        self.cursor_y = None
        self.tool_name = None
        self.tool_size = None
        self.zoom_level = None
        self.layer_name = None
        self.frame_info = None
    
    def set_visible(self, visible: bool):
        """Show or hide HUD"""
        self.visible = visible
        if visible:
            self._draw_hud()
        else:
            self.canvas.delete(self.hud_tag)
    
    def _draw_hud(self):
        """Draw HUD overlay on canvas"""
        if not self.visible:
            return
        
        # Clear previous HUD
        self.canvas.delete(self.hud_tag)
        
        theme = self.theme_manager.get_current_theme()
        bg_color = theme.bg_secondary
        text_color = theme.text_primary
        
        # Build HUD text
        lines = []
        if self.cursor_x is not None and self.cursor_y is not None:
            lines.append(f"X: {self.cursor_x}  Y: {self.cursor_y}")
        if self.tool_name:
            lines.append(f"Tool: {self.tool_name.capitalize()}")
        if self.tool_size:
            lines.append(f"Size: {self.tool_size}")
        if self.zoom_level is not None:
            lines.append(f"Zoom: {self.zoom_level:.1f}x")
        if self.layer_name:
            lines.append(f"Layer: {self.layer_name}")
        if self.frame_info:
            lines.append(f"Frame: {self.frame_info}")
        
        if not lines:
            return
        
        # Calculate background size
        line_height = 14
        padding = 6
        width = 150
        height = len(lines) * line_height + padding * 2
        
        # Draw semi-transparent background
        # Note: Tkinter doesn't support alpha directly, so we use a lighter color
        self.canvas.create_rectangle(
            self.hud_x, self.hud_y,
            self.hud_x + width, self.hud_y + height,
            fill=bg_color, outline=text_color, width=1,
            tags=self.hud_tag
        )
        
        # Draw text lines
        y = self.hud_y + padding + line_height // 2
        for line in lines:
            self.canvas.create_text(
                self.hud_x + padding, y,
                text=line,
                fill=text_color,
                anchor="w",
                font=("Arial", 9),
                tags=self.hud_tag
            )
            y += line_height
    
    def update_cursor(self, x: int, y: int):
        """Update cursor position"""
        self.cursor_x = x
        self.cursor_y = y
        if self.visible:
            self._draw_hud()
    
    def update_tool(self, tool_name: str):
        """Update tool name"""
        self.tool_name = tool_name
        if self.visible:
            self._draw_hud()
    
    def update_size(self, size: str):
        """Update tool size"""
        self.tool_size = size
        if self.visible:
            self._draw_hud()
    
    def update_zoom(self, zoom: float):
        """Update zoom level"""
        self.zoom_level = zoom
        if self.visible:
            self._draw_hud()
    
    def update_layer(self, layer_name: str):
        """Update layer name"""
        self.layer_name = layer_name
        if self.visible:
            self._draw_hud()
    
    def update_frame(self, frame_info: str):
        """Update frame info"""
        self.frame_info = frame_info
        if self.visible:
            self._draw_hud()
    
    def apply_theme(self, theme):
        """Update HUD colors when theme changes"""
        if self.visible:
            self._draw_hud()
