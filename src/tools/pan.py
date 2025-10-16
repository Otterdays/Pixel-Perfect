"""
Pan Tool - Move the camera view around the canvas
"""
from src.tools.base_tool import Tool

class PanTool(Tool):
    def __init__(self):
        super().__init__(name="pan", cursor="hand2")
        self.pan_start_screen_x = None  # Store in SCREEN coordinates
        self.pan_start_screen_y = None
        self.start_offset_x = None  # Store original offset when pan started
        self.start_offset_y = None
        self.is_panning = False
        
    def start_pan(self, screen_x, screen_y, current_offset_x, current_offset_y):
        """Start panning - use screen coordinates"""
        self.pan_start_screen_x = screen_x
        self.pan_start_screen_y = screen_y
        self.start_offset_x = current_offset_x
        self.start_offset_y = current_offset_y
        self.is_panning = True
        
    def update_pan(self, screen_x, screen_y, zoom):
        """Update pan - returns new absolute offset (not delta)"""
        if self.is_panning and self.pan_start_screen_x is not None:
            # Calculate screen space delta
            screen_dx = screen_x - self.pan_start_screen_x
            screen_dy = screen_y - self.pan_start_screen_y
            
            # Convert screen delta to canvas pixel delta
            canvas_dx = screen_dx // zoom
            canvas_dy = screen_dy // zoom
            
            # Return absolute offset (not delta)
            new_offset_x = self.start_offset_x + canvas_dx
            new_offset_y = self.start_offset_y + canvas_dy
            return (new_offset_x, new_offset_y)
        return None
    
    def end_pan(self):
        """End panning"""
        self.is_panning = False
        self.pan_start_screen_x = None
        self.pan_start_screen_y = None
        self.start_offset_x = None
        self.start_offset_y = None
    
    # Required abstract methods (not used for pan tool)
    def on_mouse_down(self, canvas, x, y, button, color):
        pass
    
    def on_mouse_move(self, canvas, x, y, color):
        pass
        
    def on_mouse_up(self, canvas, x, y, button, color):
        pass

