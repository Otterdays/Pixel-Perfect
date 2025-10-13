"""
Tooltip system for Pixel Perfect
Shows helpful tooltips after hovering for 1 second
"""

import tkinter as tk
from typing import Optional

class ToolTip:
    """Simple tooltip that appears after 1 second hover"""
    
    def __init__(self, widget, text: str, delay: int = 1000):
        """
        Create a tooltip for a widget
        
        Args:
            widget: The widget to attach tooltip to
            text: Tooltip text to display
            delay: Delay in milliseconds before showing (default 1000ms = 1 second)
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window: Optional[tk.Toplevel] = None
        self.after_id: Optional[str] = None
        
        # Bind hover events
        self.widget.bind("<Enter>", self._on_enter)
        self.widget.bind("<Leave>", self._on_leave)
        self.widget.bind("<Button-1>", self._on_click)
    
    def _on_enter(self, event=None):
        """Mouse entered widget - schedule tooltip"""
        self._cancel_tooltip()
        self.after_id = self.widget.after(self.delay, self._show_tooltip)
    
    def _on_leave(self, event=None):
        """Mouse left widget - hide tooltip"""
        self._cancel_tooltip()
        self._hide_tooltip()
    
    def _on_click(self, event=None):
        """Widget clicked - hide tooltip immediately"""
        self._cancel_tooltip()
        self._hide_tooltip()
    
    def _cancel_tooltip(self):
        """Cancel scheduled tooltip"""
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
    
    def _show_tooltip(self):
        """Display the tooltip"""
        if self.tooltip_window or not self.text:
            return
        
        # Get widget position
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        
        # Create tooltip window
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)  # No window decorations
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        # Create tooltip label with styling
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="#ffffe0",  # Light yellow background
            foreground="#000000",  # Black text
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 9, "normal"),
            padx=8,
            pady=4
        )
        label.pack()
    
    def _hide_tooltip(self):
        """Hide the tooltip"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


def create_tooltip(widget, text: str, delay: int = 1000) -> ToolTip:
    """
    Convenience function to create a tooltip
    
    Args:
        widget: The widget to attach tooltip to
        text: Tooltip text to display
        delay: Delay in milliseconds before showing (default 1000ms = 1 second)
    
    Returns:
        ToolTip instance
    """
    return ToolTip(widget, text, delay)

