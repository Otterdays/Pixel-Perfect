"""
Canvas Operations Manager
Handles coordinate conversion, panel sizing, and window state management

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import os
import json
from typing import Tuple, Optional


class CanvasOperationsManager:
    """Manages canvas coordinate operations and window state"""
    
    def __init__(self, root, canvas, drawing_canvas):
        """
        Initialize canvas operations manager
        
        Args:
            root: Main tkinter root window
            canvas: Canvas object with pixel data
            drawing_canvas: Tkinter drawing canvas widget
        """
        self.root = root
        self.canvas = canvas
        self.drawing_canvas = drawing_canvas
        
        # Pan offset (managed externally)
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        
        # Panel containers (set after UI creation)
        self.left_container = None
        self.right_container = None
        
        # Callbacks
        self.update_canvas_callback = None
    
    def tkinter_screen_to_canvas_coords(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """Convert tkinter screen coordinates to canvas coordinates"""
        # Get drawing canvas dimensions
        canvas_width = self.drawing_canvas.winfo_width()
        canvas_height = self.drawing_canvas.winfo_height()

        # Calculate the canvas display size and offsets
        canvas_pixel_width = self.canvas.width * self.canvas.zoom
        canvas_pixel_height = self.canvas.height * self.canvas.zoom
        x_offset = (canvas_width - canvas_pixel_width) // 2
        y_offset = (canvas_height - canvas_pixel_height) // 2

        # Convert screen coordinates to canvas-relative coordinates
        relative_x = screen_x - x_offset
        relative_y = screen_y - y_offset

        # Convert to canvas pixel coordinates
        canvas_coord_x = relative_x // self.canvas.zoom
        canvas_coord_y = relative_y // self.canvas.zoom
        
        # Apply pan offset
        canvas_coord_x -= self.pan_offset_x
        canvas_coord_y -= self.pan_offset_y

        return canvas_coord_x, canvas_coord_y
    
    def calculate_optimal_panel_widths(self) -> Tuple[int, int]:
        """Calculate optimal panel widths based on screen resolution"""
        try:
            # Get screen dimensions
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            print(f"[Panel Sizing] Screen resolution: {screen_width}x{screen_height}")
            
            # Calculate optimal panel widths based on screen size
            if screen_width <= 1366:  # Small laptop screens (1366x768)
                left_width, right_width = 280, 260
                print(f"[Panel Sizing] Small screen detected - using compact panels: {left_width}x{right_width}")
            elif screen_width <= 1920:  # Standard desktop (1920x1080)
                left_width, right_width = 350, 320
                print(f"[Panel Sizing] Standard desktop detected - using balanced panels: {left_width}x{right_width}")
            elif screen_width <= 2560:  # Large desktop (2560x1440)
                left_width, right_width = 400, 380
                print(f"[Panel Sizing] Large desktop detected - using spacious panels: {left_width}x{right_width}")
            else:  # Ultra-wide or 4K (2560+)
                left_width, right_width = 450, 420
                print(f"[Panel Sizing] Ultra-wide/4K detected - using wide panels: {left_width}x{right_width}")
            
            # Ensure minimum widths
            left_width = max(left_width, 200)
            right_width = max(right_width, 200)
            
            # Calculate total panel usage percentage
            total_panel_width = left_width + right_width
            panel_percentage = (total_panel_width / screen_width) * 100
            
            print(f"[Panel Sizing] Panel usage: {total_panel_width}px ({panel_percentage:.1f}% of screen)")
            print(f"[Panel Sizing] Canvas space: {screen_width - total_panel_width}px")
            
            return left_width, right_width
            
        except Exception as e:
            print(f"[Panel Sizing] Error calculating panel widths: {e}")
            # Fallback to reasonable defaults
            return 350, 320
    
    def save_window_state(self):
        """Save current window and panel state to config file"""
        try:
            # Get current state
            state = {
                'window_geometry': self.root.geometry(),
                'left_panel_width': self.left_container.winfo_width() if self.left_container else 350,
                'right_panel_width': self.right_container.winfo_width() if self.right_container else 320,
                'screen_width': self.root.winfo_screenwidth(),
                'screen_height': self.root.winfo_screenheight()
            }
            
            # Save to user config directory
            config_dir = os.path.join(os.path.expanduser("~"), ".pixelperfect")
            os.makedirs(config_dir, exist_ok=True)
            config_file = os.path.join(config_dir, "window_state.json")
            
            with open(config_file, 'w') as f:
                json.dump(state, f, indent=2)
                
            print(f"[Window State] Saved to: {config_file}")
            
        except Exception as e:
            print(f"[Window State] Error saving state: {e}")
    
    def restore_window_state(self) -> bool:
        """
        Restore saved window state on startup
        
        Returns:
            bool: True if state was restored, False otherwise
        """
        try:
            config_dir = os.path.join(os.path.expanduser("~"), ".pixelperfect")
            config_file = os.path.join(config_dir, "window_state.json")
            
            if not os.path.exists(config_file):
                print("[Window State] No saved state found, using defaults")
                return False
            
            with open(config_file, 'r') as f:
                state = json.load(f)
            
            # Check if screen resolution matches (don't restore if resolution changed)
            current_screen_width = self.root.winfo_screenwidth()
            current_screen_height = self.root.winfo_screenheight()
            
            saved_screen_width = state.get('screen_width', 0)
            saved_screen_height = state.get('screen_height', 0)
            
            # Allow 10% tolerance for resolution changes (different DPI scaling, etc.)
            width_tolerance = abs(current_screen_width - saved_screen_width) / saved_screen_width if saved_screen_width > 0 else 1
            height_tolerance = abs(current_screen_height - saved_screen_height) / saved_screen_height if saved_screen_height > 0 else 1
            
            if width_tolerance > 0.1 or height_tolerance > 0.1:
                print(f"[Window State] Screen resolution changed ({saved_screen_width}x{saved_screen_height} → "
                      f"{current_screen_width}x{current_screen_height}), recalculating panel sizes")
                return False
            
            # Restore window geometry
            if 'window_geometry' in state:
                self.root.geometry(state['window_geometry'])
                print(f"[Window State] Restored window geometry: {state['window_geometry']}")
            
            # Return panel widths to be used during UI creation
            left_width = state.get('left_panel_width', 350)
            right_width = state.get('right_panel_width', 320)
            
            print(f"[Window State] Restored panel widths: {left_width}x{right_width}")
            return left_width, right_width
            
        except Exception as e:
            print(f"[Window State] Error restoring state: {e}")
            return False
    
    def redraw_canvas_after_resize(self):
        """Redraw canvas after window/panel resize"""
        if self.update_canvas_callback:
            self.update_canvas_callback()

