"""
Recent Colors View for Pixel Perfect
Displays recently used colors in the palette panel
"""

import customtkinter as ctk
from typing import Callable, Optional, Tuple


class RecentColorsView:
    """
    UI component for displaying recent colors.
    
    Shows a grid of the most recently used colors for quick access.
    Clicking a color selects it as the current drawing color.
    """
    
    def __init__(self, 
                 parent: ctk.CTkFrame,
                 recent_colors_manager,
                 on_color_select: Callable[[Tuple[int, int, int, int]], None],
                 theme_manager=None):
        """
        Initialize the recent colors view.
        
        Args:
            parent: Parent frame to attach to
            recent_colors_manager: RecentColorsManager instance
            on_color_select: Callback when a color is clicked
            theme_manager: Optional theme manager for styling
        """
        self.parent = parent
        self.recent_manager = recent_colors_manager
        self.on_color_select = on_color_select
        self.theme_manager = theme_manager
        
        self.frame: Optional[ctk.CTkFrame] = None
        self.color_buttons = []
        
        # Register for updates
        if self.recent_manager:
            self.recent_manager.on_colors_changed = self.refresh
    
    def create_view(self, container: ctk.CTkFrame) -> ctk.CTkFrame:
        """
        Create and return the recent colors view frame.
        
        Args:
            container: Frame to place the view in
            
        Returns:
            The created frame
        """
        # Create main frame
        self.frame = ctk.CTkFrame(container, fg_color="transparent")
        
        # Title
        title_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 5))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="Recent Colors",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        title_label.pack(side="left")
        
        # Clear button
        clear_btn = ctk.CTkButton(
            title_frame,
            text="Clear",
            width=40,
            height=20,
            font=ctk.CTkFont(size=10),
            command=self._on_clear
        )
        clear_btn.pack(side="right")
        
        # Colors grid
        self.colors_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.colors_frame.pack(fill="x")
        
        # Initial render
        self.refresh()
        
        return self.frame
    
    def refresh(self):
        """Refresh the color grid with current recent colors."""
        if not self.colors_frame:
            return
        
        # Clear existing buttons
        for btn in self.color_buttons:
            btn.destroy()
        self.color_buttons.clear()
        
        # Get recent colors
        colors = self.recent_manager.get_colors() if self.recent_manager else []
        
        if not colors:
            # Show empty message
            empty_label = ctk.CTkLabel(
                self.colors_frame,
                text="No recent colors yet",
                font=ctk.CTkFont(size=10),
                text_color="gray"
            )
            empty_label.pack(pady=10)
            self.color_buttons.append(empty_label)
            return
        
        # Create grid of color buttons
        # 8 columns, 2 rows max (16 colors)
        row_frame = None
        for i, color in enumerate(colors):
            if i % 8 == 0:
                row_frame = ctk.CTkFrame(self.colors_frame, fg_color="transparent")
                row_frame.pack(fill="x", pady=1)
            
            # Convert RGBA to hex for button color
            hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            
            btn = ctk.CTkButton(
                row_frame,
                text="",
                width=24,
                height=24,
                fg_color=hex_color,
                hover_color=hex_color,
                border_width=1,
                border_color="gray50",
                corner_radius=3,
                command=lambda c=color: self._on_color_click(c)
            )
            btn.pack(side="left", padx=1)
            self.color_buttons.append(btn)
            
            # Track rows as well for cleanup
            if i % 8 == 0:
                self.color_buttons.append(row_frame)
    
    def _on_color_click(self, color: Tuple[int, int, int, int]):
        """Handle color button click."""
        if self.on_color_select:
            self.on_color_select(color)
    
    def _on_clear(self):
        """Handle clear button click."""
        if self.recent_manager:
            self.recent_manager.clear()
