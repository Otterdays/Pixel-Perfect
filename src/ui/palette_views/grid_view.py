"""
Grid View for Pixel Perfect
Displays the main color palette in an 8-column grid
"""

import customtkinter as ctk
from typing import Callable, List, Optional
from src.ui.tooltip import create_color_hex_tooltip


class GridView:
    """Manages the main palette grid view"""
    
    def __init__(self, parent_frame: ctk.CTkFrame, palette, theme_manager, 
                 on_color_select: Callable, on_tool_switch: Callable):
        """
        Initialize the grid view
        
        Args:
            parent_frame: Parent frame to pack widgets into
            palette: ColorPalette instance
            theme_manager: ThemeManager instance
            on_color_select: Callback when color is selected
            on_tool_switch: Callback to switch tools
        """
        self.parent_frame = parent_frame
        self.palette = palette
        self.theme_manager = theme_manager
        self.on_color_select = on_color_select
        self.on_tool_switch = on_tool_switch
        
        # UI components
        self.color_frame = None
        self.color_buttons: List[ctk.CTkButton] = []
        self._hex_tooltips = []  # Keep references to prevent GC
    
    def create(self):
        """Create the color grid view"""
        # Clear existing widgets
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Create grid frame - centered
        self.color_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self.color_frame.pack(padx=10, pady=10)
        
        # Clear button references
        self.color_buttons.clear()
        self._hex_tooltips.clear()
        
        colors = self.palette.colors
        cols = 8
        rows = (len(colors) + cols - 1) // cols
        
        for i, color in enumerate(colors):
            row = i // cols
            col = i % cols
            
            # Create color button with hover effects
            btn = ctk.CTkButton(
                self.color_frame,
                text="",
                width=30,
                height=30,
                fg_color=f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}",
                hover_color=f"#{min(255, color[0] + 30):02x}{min(255, color[1] + 30):02x}{min(255, color[2] + 30):02x}",
                border_width=0,
                command=lambda idx=i: self._select_color(idx)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            
            # Store button reference
            self.color_buttons.append(btn)
            
            # Add hover effects
            btn.bind("<Enter>", lambda e, b=btn: self._on_color_hover_enter(b))
            btn.bind("<Leave>", lambda e, b=btn: self._on_color_hover_leave(b))
            
            # Add hex code tooltip
            self._hex_tooltips.append(create_color_hex_tooltip(btn, color))
            
            # Highlight primary/secondary colors
            if i == self.palette.primary_color:
                btn.configure(border_width=3, border_color="white")
            elif i == self.palette.secondary_color:
                btn.configure(border_width=2, border_color="gray")
    
    def update_selection(self):
        """Update color grid selection without recreating the grid"""
        if not self.color_buttons:
            return
        
        for i, btn in enumerate(self.color_buttons):
            if i == self.palette.primary_color:
                btn.configure(border_width=3, border_color="white")
            elif i == self.palette.secondary_color:
                btn.configure(border_width=2, border_color="gray")
            else:
                btn.configure(border_width=0, border_color="")
    
    def _select_color(self, color_index: int):
        """Select a color from the palette"""
        self.palette.set_primary_color(color_index)
        
        # Update the color grid to show new selection
        self.update_selection()
        
        # Notify parent
        if self.on_color_select:
            self.on_color_select(color_index)
        
        # Auto-switch to brush tool for immediate painting
        if self.on_tool_switch:
            self.on_tool_switch("brush")
    
    def _on_color_hover_enter(self, button):
        """Handle hover enter on color button"""
        # Find the button index to check if it's selected
        button_index = None
        for i, btn in enumerate(self.color_buttons):
            if btn == button:
                button_index = i
                break
        
        # Only add hover effects if button is not currently selected
        if button_index is not None:
            if button_index != self.palette.primary_color and button_index != self.palette.secondary_color:
                button.configure(border_width=2, border_color="white")
                button.configure(width=32, height=32)
    
    def _on_color_hover_leave(self, button):
        """Handle hover leave on color button"""
        # Find the button index to check if it's selected
        button_index = None
        for i, btn in enumerate(self.color_buttons):
            if btn == button:
                button_index = i
                break
        
        # Only remove hover effects if button is not selected
        if button_index is not None:
            if button_index != self.palette.primary_color and button_index != self.palette.secondary_color:
                button.configure(border_width=0, border_color="")
                button.configure(width=30, height=30)
    
    def apply_theme(self, theme):
        """Apply theme to grid view (color buttons are skipped in main theme application)"""
        # Color buttons maintain their actual colors, so nothing to do here
        pass

