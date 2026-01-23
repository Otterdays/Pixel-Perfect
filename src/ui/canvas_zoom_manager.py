"""
Canvas Size and Zoom Manager for Pixel Perfect
Manages canvas sizing, resizing, and zoom level controls

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

from core.canvas import CanvasSize


class CanvasZoomManager:
    """Manages canvas size changes and zoom level adjustments"""
    
    def __init__(self, root, canvas, layer_manager, timeline, dialog_mgr):
        """
        Initialize the Canvas/Zoom Manager
        
        Args:
            root: Main tkinter window
            canvas: Canvas object
            layer_manager: Layer manager for resizing layers
            timeline: Timeline for resizing frames
            dialog_mgr: Dialog manager for custom size and warnings
        """
        self.root = root
        self.canvas = canvas
        self.layer_manager = layer_manager
        self.timeline = timeline
        self.dialog_mgr = dialog_mgr
        
        # Custom canvas size tracking
        self.custom_canvas_size = None
        
        # UI references (set after UI creation)
        self.size_var = None
        self.zoom_var = None
        
        # Callbacks (set by main_window)
        self.update_canvas_callback = None
        self.force_canvas_update_callback = None
        self.sync_scrollbar_callback = None
    
    # ========================================
    # CANVAS SIZE METHODS
    # ========================================
    
    def on_size_change(self, size_str: str):
        """Handle canvas size change - WARNING: Downsizing clips pixels!"""
        # Handle custom size dialog
        if size_str == "Custom...":
            width, height = self.dialog_mgr.open_custom_size_dialog()
            
            if width is None or height is None:
                # User cancelled - restore previous size
                if self.custom_canvas_size:
                    self.size_var.set(f"CUSTOM ({self.custom_canvas_size[0]}x{self.custom_canvas_size[1]})")
                else:
                    # Restore to current actual size
                    current_size = f"{self.canvas.width}x{self.canvas.height}"
                    if current_size in ["8x8", "16x16", "32x32", "16x32", "32x64", "64x64"]:
                        self.size_var.set(current_size)
                    else:
                        self.size_var.set("32x32")
                return
            
            # Apply custom size
            self.apply_custom_canvas_size(width, height)
            return
        
        size_map = {
            "8x8": CanvasSize.TINY,
            "16x16": CanvasSize.SMALL,
            "32x32": CanvasSize.MEDIUM,
            "16x32": CanvasSize.WIDE,
            "32x64": CanvasSize.LARGE,
            "64x64": CanvasSize.XLARGE
        }
        
        # Clear custom size when switching to preset
        self.custom_canvas_size = None
        
        if size_str in size_map:
            # Store old dimensions for preservation info
            old_width = self.canvas.width
            old_height = self.canvas.height
            
            # Get new dimensions
            new_size = size_map[size_str].value
            new_width, new_height = new_size
            
            # CHECK: Will this resize clip pixels?
            will_clip_width = new_width < old_width
            will_clip_height = new_height < old_height
            
            if will_clip_width or will_clip_height:
                # WARN USER: Pixels will be permanently lost!
                # Show custom styled warning dialog
                result = self.dialog_mgr.show_downsize_warning(old_width, old_height, new_width, new_height)
                
                if not result:
                    # User cancelled - restore old size in dropdown
                    old_size_str = f"{old_width}x{old_height}"
                    self.size_var.set(old_size_str)
                    print(f"[Canvas Resize] Cancelled by user")
                    return
            
            # Resize canvas (updates dimensions only)
            self.canvas.set_preset_size(size_map[size_str])
            
            # Auto-adjust zoom based on canvas size for optimal viewing
            # Smaller canvases get higher zoom, larger canvases get lower zoom
            if size_str == "16x16":
                # Very small canvas - use high zoom (16x minimum)
                if self.canvas.zoom < 16:
                    self.canvas.set_zoom(16)
                    self.zoom_var.set("16x")
            elif size_str == "16x32" or size_str == "32x32":
                # Small canvas - use medium-high zoom (16x minimum)
                if self.canvas.zoom < 16:
                    self.canvas.set_zoom(16)
                    self.zoom_var.set("16x")
            elif size_str in ["32x64", "64x64"]:
                # Large canvas - reduce zoom to fit (8x maximum)
                if self.canvas.zoom > 8:
                    self.canvas.set_zoom(8)
                    self.zoom_var.set("8x")
            
            # Resize layer manager and timeline (both automatically preserve pixel data)
            # These methods copy existing pixels to the top-left of new size
            self.layer_manager.resize_layers(new_width, new_height)
            self.timeline.resize_frames(new_width, new_height)
            
            # Sync canvas display with resized layer data
            if self.update_canvas_callback:
                self.update_canvas_callback()
            
            # Update display immediately
            if self.force_canvas_update_callback:
                self.force_canvas_update_callback()
            
            # Log resize info
            preserved_w = min(old_width, new_width)
            preserved_h = min(old_height, new_height)
            print(f"[Canvas Resize] {old_width}x{old_height} → {new_width}x{new_height}")
            print(f"[Pixel Preservation] Top-left {preserved_w}x{preserved_h} region preserved")
    
    def apply_custom_canvas_size(self, width: int, height: int):
        """Apply custom canvas size with same safety checks as preset sizes"""
        # Store old dimensions
        old_width = self.canvas.width
        old_height = self.canvas.height
        
        # CHECK: Will this resize clip pixels?
        will_clip_width = width < old_width
        will_clip_height = height < old_height
        
        if will_clip_width or will_clip_height:
            # WARN USER: Pixels will be permanently lost!
            # Show custom styled warning dialog
            result = self.dialog_mgr.show_downsize_warning(old_width, old_height, width, height)
            
            if not result:
                # User cancelled - restore previous size in dropdown
                if self.custom_canvas_size:
                    self.size_var.set(f"CUSTOM ({self.custom_canvas_size[0]}x{self.custom_canvas_size[1]})")
                else:
                    old_size_str = f"{old_width}x{old_height}"
                    self.size_var.set(old_size_str)
                print(f"[Custom Canvas Resize] Cancelled by user")
                return
        
        # Apply custom size
        self.canvas.resize(width, height)
        
        # Store custom size
        self.custom_canvas_size = (width, height)
        
        # Update dropdown to show CUSTOM
        self.size_var.set(f"CUSTOM ({width}x{height})")
        
        # Auto-adjust zoom based on size
        if width <= 16 or height <= 16:
            if self.canvas.zoom < 16:
                self.canvas.set_zoom(16)
                self.zoom_var.set("16x")
        elif width <= 32 or height <= 32:
            if self.canvas.zoom < 16:
                self.canvas.set_zoom(16)
                self.zoom_var.set("16x")
        elif width >= 64 or height >= 64:
            if self.canvas.zoom > 8:
                    self.canvas.set_zoom(8)
                    self.zoom_var.set("8x")
            
        # Resize layer manager and timeline
        preserve_width = min(old_width, width)
        preserve_height = min(old_height, height)
        
        self.layer_manager.resize_layers(width, height)
        self.timeline.resize_frames(width, height)
        
        # Sync canvas display with resized layer data
        if self.update_canvas_callback:
            self.update_canvas_callback()
        
        # Update display
        if self.force_canvas_update_callback:
            self.force_canvas_update_callback()
        
        print(f"[Custom Canvas Resize] Resized to {width}x{height}, preserved {preserve_width}x{preserve_height} pixels")
    
    # ========================================
    # ZOOM METHODS
    # ========================================
    
    def on_zoom_change(self, zoom_str: str):
        """Handle zoom level change"""
        zoom_map = {
            "0.25x": 0.25, "0.5x": 0.5, "1x": 1, "2x": 2, "4x": 4, "8x": 8, "16x": 16, "32x": 32, "64x": 64
        }
        
        if zoom_str in zoom_map:
            self.canvas.set_zoom(zoom_map[zoom_str])
            # Update display immediately
            if self.force_canvas_update_callback:
                self.force_canvas_update_callback()
            # Sync scrollbar position
            if self.sync_scrollbar_callback:
                self.sync_scrollbar_callback()
            # Update status bar
            if hasattr(self, 'main_window') and hasattr(self.main_window, '_update_status_bar'):
                self.main_window._update_status_bar()

