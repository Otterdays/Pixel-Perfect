"""
Selection tools for Pixel Perfect
Rectangle selection and move functionality
"""

from .base_tool import Tool
from typing import Tuple, Optional, List
import numpy as np

class SelectionTool(Tool):
    """Rectangle selection tool"""
    
    def __init__(self):
        super().__init__("Selection", cursor="crosshair")
        self.is_selecting = False
        self.selection_start = (0, 0)
        self.selection_end = (0, 0)
        self.selection_rect = None
        self.selected_pixels = None
        self.has_selection = False
        self.on_selection_complete = None  # Callback for when selection is finalized
    
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Start selection"""
        if button == 1:  # Left mouse button
            self.is_selecting = True
            self.selection_start = (x, y)
            self.selection_end = (x, y)
            self.has_selection = False
            # Clear old selection to start fresh
            self.selection_rect = None
            self.selected_pixels = None
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """End selection"""
        if button == 1 and self.is_selecting:
            self.is_selecting = False
            self.selection_end = (x, y)
            self._finalize_selection(canvas)
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Update selection while dragging"""
        if self.is_selecting:
            self.selection_end = (x, y)
            self._update_selection_rect()
    
    def _update_selection_rect(self):
        """Update selection rectangle"""
        x1, y1 = self.selection_start
        x2, y2 = self.selection_end
        
        # Calculate rectangle bounds
        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        self.selection_rect = (left, top, width, height)
    
    def _finalize_selection(self, canvas):
        """Finalize the selection and capture pixels"""
        if not self.selection_rect:
            return
        
        left, top, width, height = self.selection_rect
        
        # Clamp to canvas bounds
        left = max(0, min(left, canvas.width))
        top = max(0, min(top, canvas.height))
        width = min(width, canvas.width - left)
        height = min(height, canvas.height - top)
        
        if width <= 0 or height <= 0:
            self.has_selection = False
            return
        
        # ONLY capture pixels if we don't already have them stored
        # This prevents re-capturing after a move operation
        if self.selected_pixels is None:
            # Capture selected pixels
            self.selected_pixels = np.zeros((height, width, 4), dtype=np.uint8)
            
            for y in range(height):
                for x in range(width):
                    canvas_x = left + x
                    canvas_y = top + y
                    if 0 <= canvas_x < canvas.width and 0 <= canvas_y < canvas.height:
                        self.selected_pixels[y, x] = canvas.get_pixel(canvas_x, canvas_y)
        
        self.has_selection = True
        self.selection_rect = (left, top, width, height)
        
        # Notify that selection is complete
        if self.on_selection_complete:
            self.on_selection_complete()
    
    def clear_selection(self):
        """Clear current selection"""
        self.has_selection = False
        self.selection_rect = None
        self.selected_pixels = None
        self.is_selecting = False
    
    def get_selection_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get selection bounds (left, top, width, height)"""
        return self.selection_rect
    
    def has_active_selection(self) -> bool:
        """Check if there's an active selection"""
        return self.has_selection

class MoveTool(Tool):
    """Move selection tool"""
    
    def __init__(self):
        super().__init__("Move", cursor="fleur")
        self.is_moving = False
        self.move_offset = (0, 0)
        self.original_selection = None
        self.selection_tool = None
        self.cleared_background = None  # Store what was cleared for undo if needed
        self.pixels_cleared = False  # Track if we've cleared original pixels yet
        self.has_been_moved = False  # Track if selection has been moved from original position
        self.last_drawn_position = None  # Track where pixels are currently drawn on canvas
        self.saved_background = None  # Store background pixels before placing selection
    
    def set_selection_tool(self, selection_tool: SelectionTool):
        """Set reference to selection tool"""
        self.selection_tool = selection_tool
    
    def on_mouse_down(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """Start moving selection"""
        if (button == 1 and self.selection_tool and 
            self.selection_tool.has_active_selection()):
            
            bounds = self.selection_tool.get_selection_bounds()
            if bounds:
                left, top, width, height = bounds
                # Check if click is within selection
                if left <= x < left + width and top <= y < top + height:
                    self.is_moving = True
                    self.move_offset = (x - left, y - top)
                    
                    # FIRST PICKUP: Clear original pixels
                    if not self.original_selection:
                        self.original_selection = (left, top)
                        # Clear the original pixels from canvas
                        for py in range(height):
                            for px in range(width):
                                if (py < self.selection_tool.selected_pixels.shape[0] and 
                                    px < self.selection_tool.selected_pixels.shape[1]):
                                    pixel_color = tuple(self.selection_tool.selected_pixels[py, px])
                                    if pixel_color[3] > 0:  # Non-transparent
                                        canvas_x = left + px
                                        canvas_y = top + py
                                        if 0 <= canvas_x < canvas.width and 0 <= canvas_y < canvas.height:
                                            canvas.set_pixel(canvas_x, canvas_y, (0, 0, 0, 0))
                        print("[MOVE] First pickup - cleared original pixels")
                    
                    # SUBSEQUENT PICKUPS: Restore saved background (from last drop)
                    elif self.saved_background and self.last_drawn_position:
                        restore_left, restore_top = self.last_drawn_position
                        for py in range(len(self.saved_background)):
                            for px in range(len(self.saved_background[0])):
                                bg_pixel = self.saved_background[py][px]
                                canvas_x = restore_left + px
                                canvas_y = restore_top + py
                                if 0 <= canvas_x < canvas.width and 0 <= canvas_y < canvas.height:
                                    canvas.set_pixel(canvas_x, canvas_y, bg_pixel)
                        print("[MOVE] Adjustment pickup - restored background from last drop")
                    
                    # Clear saved background for new move
                    self.saved_background = None
                    
                    print("[MOVE] Picked up selection")
    
    def on_mouse_up(self, canvas, x: int, y: int, button: int, color: Tuple[int, int, int, int]):
        """End moving selection"""
        if button == 1 and self.is_moving:
            self.is_moving = False
            
            # Save background and draw pixels at new position
            if self.selection_tool and self.selection_tool.selected_pixels is not None:
                bounds = self.selection_tool.get_selection_bounds()
                if bounds:
                    left, top, width, height = bounds
                    
                    # Save background pixels before overwriting
                    self.saved_background = []
                    for py in range(height):
                        row = []
                        for px in range(width):
                            canvas_x = left + px
                            canvas_y = top + py
                            if 0 <= canvas_x < canvas.width and 0 <= canvas_y < canvas.height:
                                row.append(canvas.get_pixel(canvas_x, canvas_y))
                            else:
                                row.append((0, 0, 0, 0))
                        self.saved_background.append(row)
                    
                    # Draw pixels at new position
                    for py in range(height):
                        for px in range(width):
                            if (py < self.selection_tool.selected_pixels.shape[0] and 
                                px < self.selection_tool.selected_pixels.shape[1]):
                                pixel_color = tuple(self.selection_tool.selected_pixels[py, px])
                                if pixel_color[3] > 0:  # Non-transparent
                                    canvas_x = left + px
                                    canvas_y = top + py
                                    if 0 <= canvas_x < canvas.width and 0 <= canvas_y < canvas.height:
                                        canvas.set_pixel(canvas_x, canvas_y, pixel_color)
                    
                    # Track this position for next pickup
                    self.last_drawn_position = (left, top)
                    
                    # Track if we've moved from original
                    if self.original_selection:
                        orig_left, orig_top = self.original_selection
                        if left != orig_left or top != orig_top:
                            self.has_been_moved = True
                            print(f"[MOVE] Pixels drawn (background saved for non-destructive adjustment)")
    
    def on_mouse_move(self, canvas, x: int, y: int, color: Tuple[int, int, int, int]):
        """Update selection position while moving"""
        if self.is_moving and self.selection_tool:
            bounds = self.selection_tool.get_selection_bounds()
            if bounds:
                left, top, width, height = bounds
                new_left = x - self.move_offset[0]
                new_top = y - self.move_offset[1]
                
                # Clamp to canvas bounds
                new_left = max(0, min(new_left, canvas.width - width))
                new_top = max(0, min(new_top, canvas.height - height))
                
                # Update selection position
                self.selection_tool.selection_rect = (new_left, new_top, width, height)
    
    def finalize_move(self, canvas):
        """Finalize the move operation - clear original pixels and place at new position"""
        if self.has_been_moved and self.original_selection and self.selection_tool:
            orig_left, orig_top = self.original_selection
            bounds = self.selection_tool.get_selection_bounds()
            
            if bounds:
                left, top, width, height = bounds
                
                # Step 1: Clear original pixels (only non-transparent)
                for py in range(height):
                    for px in range(width):
                        if (py < self.selection_tool.selected_pixels.shape[0] and 
                            px < self.selection_tool.selected_pixels.shape[1]):
                            pixel_color = tuple(self.selection_tool.selected_pixels[py, px])
                            if pixel_color[3] > 0:  # Non-transparent pixel
                                canvas_x = orig_left + px
                                canvas_y = orig_top + py
                                if 0 <= canvas_x < canvas.width and 0 <= canvas_y < canvas.height:
                                    canvas.set_pixel(canvas_x, canvas_y, (0, 0, 0, 0))
                
                # Step 2: Place pixels at new position (only non-transparent)
                for py in range(height):
                    for px in range(width):
                        if (py < self.selection_tool.selected_pixels.shape[0] and 
                            px < self.selection_tool.selected_pixels.shape[1]):
                            pixel_color = tuple(self.selection_tool.selected_pixels[py, px])
                            if pixel_color[3] > 0:  # Non-transparent pixel
                                canvas_x = left + px
                                canvas_y = top + py
                                if 0 <= canvas_x < canvas.width and 0 <= canvas_y < canvas.height:
                                    canvas.set_pixel(canvas_x, canvas_y, pixel_color)
                
                print(f"[MOVE] Finalized move - cleared original position, placed at new position")
                
                # Reset state
                self.has_been_moved = False
                self.pixels_cleared = False
                self.original_selection = None
