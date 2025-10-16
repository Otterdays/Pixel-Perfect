"""
Tool Size Manager for Pixel Perfect
Manages brush and eraser size selection and multi-pixel drawing/erasing

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import tkinter as tk


class ToolSizeManager:
    """Manages brush and eraser size selection and operations"""
    
    def __init__(self, root, canvas):
        """
        Initialize the Tool Size Manager
        
        Args:
            root: Main tkinter window
            canvas: Canvas object for bounds checking
        """
        self.root = root
        self.canvas = canvas
        
        # Tool sizes
        self.brush_size = 1
        self.eraser_size = 1
        self.edge_thickness = 0.1  # Default edge thickness in pixels
        
        # Widget references (set after UI creation)
        self.tool_buttons = None
        
        # Callbacks (set by main_window)
        self.update_canvas_callback = None
        self.select_tool_callback = None
    
    # ========================================
    # EDGE THICKNESS METHODS
    # ========================================
    
    def show_edge_thickness_menu(self, event):
        """Show edge thickness selection popup menu"""
        # Create popup menu
        menu = tk.Menu(self.root, tearoff=0, bg="#2d2d2d", fg="white", 
                      activebackground="#1a73e8", activeforeground="white",
                      relief=tk.FLAT, borderwidth=0)
        
        # Add thickness options with visual indicators
        thicknesses = [
            (0.1, "0.1P • Ultra Fine"),
            (0.25, "0.25P • Fine"),
            (0.5, "0.5P • Medium"),
            (1.0, "1.0P • Thick"),
            (2.0, "2.0P • Extra Thick")
        ]
        
        for thickness, label in thicknesses:
            # Add checkmark for current thickness
            display_label = f"✓ {label}" if thickness == self.edge_thickness else f"   {label}"
            menu.add_command(
                label=display_label,
                command=lambda t=thickness: self.set_edge_thickness(t),
                font=("Segoe UI", 10)
            )
        
        # Show menu at mouse position
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def set_edge_thickness(self, thickness: float):
        """Set edge thickness"""
        self.edge_thickness = thickness
        self.update_edge_button_text()
        
        # Auto-select edge tool
        if self.select_tool_callback:
            self.select_tool_callback("edge")
    
    def update_edge_button_text(self):
        """Update edge button to show current thickness"""
        if self.tool_buttons and "edge" in self.tool_buttons:
            thickness_text = f"{self.edge_thickness:.1f}P" if self.edge_thickness < 1.0 else f"{self.edge_thickness:.0f}P"
            self.tool_buttons["edge"].configure(text=f"Edge [{thickness_text}]")
    
    # ========================================
    # BRUSH SIZE METHODS
    # ========================================
    
    def show_brush_size_menu(self, event):
        """Show brush size selection popup menu"""
        # Create popup menu
        menu = tk.Menu(self.root, tearoff=0, bg="#2d2d2d", fg="white", 
                      activebackground="#1a73e8", activeforeground="white",
                      relief=tk.FLAT, borderwidth=0)
        
        # Add size options with visual indicators
        sizes = [
            (1, "1x1 • Single Pixel"),
            (2, "2x2 • Small Brush"),
            (3, "3x3 • Medium Brush")
        ]
        
        for size, label in sizes:
            # Add checkmark for current size
            display_label = f"✓ {label}" if size == self.brush_size else f"   {label}"
            menu.add_command(
                label=display_label,
                command=lambda s=size: self.set_brush_size(s),
                font=("Segoe UI", 10)
            )
        
        # Show menu at mouse position
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def set_brush_size(self, size: int):
        """Set brush size"""
        self.brush_size = size
        self.update_brush_button_text()
        
        # Auto-select brush tool
        if self.select_tool_callback:
            self.select_tool_callback("brush")
    
    def update_brush_button_text(self):
        """Update brush button to show current size"""
        if self.tool_buttons and "brush" in self.tool_buttons:
            size_text = f"{self.brush_size}x{self.brush_size}"
            self.tool_buttons["brush"].configure(text=f"Brush [{size_text}]")
    
    def draw_brush_at(self, layer, x: int, y: int, color: tuple):
        """Draw brush at position with current size"""
        # Calculate offset for centering (makes odd sizes like 3x3 centered properly)
        offset = self.brush_size // 2
        
        # Draw NxN square
        for dy in range(self.brush_size):
            for dx in range(self.brush_size):
                px = x - offset + dx
                py = y - offset + dy
                
                # Check bounds
                if 0 <= px < layer.width and 0 <= py < layer.height:
                    layer.set_pixel(px, py, color)
    
    # ========================================
    # ERASER SIZE METHODS
    # ========================================
    
    def show_eraser_size_menu(self, event):
        """Show eraser size selection popup menu"""
        # Create popup menu
        menu = tk.Menu(self.root, tearoff=0, bg="#2d2d2d", fg="white",
                      activebackground="#1a73e8", activeforeground="white",
                      relief=tk.FLAT, borderwidth=0)
        
        # Add size options with visual indicators
        sizes = [
            (1, "1x1 • Single Pixel"),
            (2, "2x2 • Small Eraser"),
            (3, "3x3 • Medium Eraser")
        ]
        
        for size, label in sizes:
            # Add checkmark for current size
            display_label = f"✓ {label}" if size == self.eraser_size else f"   {label}"
            menu.add_command(
                label=display_label,
                command=lambda s=size: self.set_eraser_size(s),
                font=("Segoe UI", 10)
            )
        
        # Show menu at mouse position
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def set_eraser_size(self, size: int):
        """Set eraser size"""
        self.eraser_size = size
        self.update_eraser_button_text()
        
        # Auto-select eraser tool
        if self.select_tool_callback:
            self.select_tool_callback("eraser")
    
    def update_eraser_button_text(self):
        """Update eraser button to show current size"""
        if self.tool_buttons and "eraser" in self.tool_buttons:
            size_text = f"{self.eraser_size}x{self.eraser_size}"
            self.tool_buttons["eraser"].configure(text=f"Eraser [{size_text}]")
    
    def erase_at(self, layer, x: int, y: int):
        """Erase at position with current size"""
        # Calculate offset for centering
        offset = self.eraser_size // 2
        
        # Erase NxN square
        for dy in range(self.eraser_size):
            for dx in range(self.eraser_size):
                px = x - offset + dx
                py = y - offset + dy
                
                # Check bounds
                if 0 <= px < layer.width and 0 <= py < layer.height:
                    # Set to transparent (0, 0, 0, 0)
                    layer.set_pixel(px, py, (0, 0, 0, 0))

