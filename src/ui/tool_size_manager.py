"""
Tool Size Manager for Pixel Perfect
Manages brush and eraser size selection and multi-pixel drawing/erasing

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import tkinter as tk
import math


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
        # Spray tool parameters
        self.spray_radius = 8
        self.spray_density = 40  # droplets per application tick
        
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

    # ========================================
    # SPRAY TOOL METHODS
    # ========================================

    def show_spray_size_menu(self, event):
        """Show spray radius and density selection popup menu"""
        import tkinter as tk
        menu = tk.Menu(self.root, tearoff=0, bg="#2d2d2d", fg="white",
                       activebackground="#1a73e8", activeforeground="white",
                       relief=tk.FLAT, borderwidth=0)

        # Radius options
        radius_options = [
            (4, "Radius 4 • Fine"),
            (8, "Radius 8 • Small"),
            (12, "Radius 12 • Medium"),
            (16, "Radius 16 • Large"),
            (24, "Radius 24 • XL"),
        ]
        menu.add_command(label="— Size —", state="disabled")
        for r, label in radius_options:
            display_label = f"✓ {label}" if r == self.spray_radius else f"   {label}"
            menu.add_command(label=display_label, command=lambda rv=r: self.set_spray_radius(rv), font=("Segoe UI", 10))

        # Density options
        density_map = [
            (15, "Low Density"),
            (40, "Medium Density"),
            (80, "High Density"),
            (120, "Ultra Density"),
        ]
        menu.add_separator()
        menu.add_command(label="— Density —", state="disabled")
        for d, label in density_map:
            display_label = f"✓ {label}" if d == self.spray_density else f"   {label}"
            menu.add_command(label=display_label, command=lambda dv=d: self.set_spray_density(dv), font=("Segoe UI", 10))

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def set_spray_radius(self, radius: int):
        """Set spray radius and update button text; auto-select Spray."""
        self.spray_radius = radius
        self.update_spray_button_text()
        if self.select_tool_callback:
            self.select_tool_callback("spray")

    def set_spray_density(self, density: int):
        """Set spray density and update button text; auto-select Spray."""
        self.spray_density = density
        self.update_spray_button_text()
        if self.select_tool_callback:
            self.select_tool_callback("spray")

    def update_spray_button_text(self):
        """Update Spray button to show current radius and density"""
        if self.tool_buttons and "spray" in self.tool_buttons:
            # Show density as L/M/H/U based on numeric value
            if self.spray_density <= 20:
                d_text = "L"
            elif self.spray_density <= 50:
                d_text = "M"
            elif self.spray_density <= 90:
                d_text = "H"
            else:
                d_text = "U"
            self.tool_buttons["spray"].configure(text=f"Spray [R:{self.spray_radius} D:{d_text}]")

    def spray_at(self, layer, x: int, y: int, color: tuple):
        """Apply spray droplets centered at (x, y) using current radius/density."""
        import random
        # Convert radius to pixel units (already pixels); sample points in disk
        r = max(1, int(self.spray_radius))
        for _ in range(int(self.spray_density)):
            # Polar sampling with sqrt for uniform disk distribution
            angle = random.random() * 6.283185307179586  # 2*pi
            dist = r * (random.random() ** 0.5)
            px = int(round(x + dist * (math.cos(angle))))
            py = int(round(y + dist * (math.sin(angle))))
            if 0 <= px < layer.width and 0 <= py < layer.height:
                layer.set_pixel(px, py, color)

