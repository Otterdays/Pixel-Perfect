"""
Context Menu Manager for Pixel Perfect
Handles right-click context menus on the canvas

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import tkinter as tk
from typing import Optional, Callable


class ContextMenuManager:
    """Manages context menus for canvas right-click actions"""
    
    def __init__(self, main_window):
        """
        Initialize context menu manager
        
        Args:
            main_window: Reference to MainWindow instance
        """
        self.main_window = main_window
        self.current_menu: Optional[tk.Menu] = None
    
    def show_canvas_context_menu(self, event):
        """Show context menu on canvas right-click"""
        # Don't show context menu for edge/eraser tools (they have special right-click behavior)
        if self.main_window.current_tool in ["edge", "eraser"]:
            return
        
        # Create menu
        menu = tk.Menu(
            self.main_window.root,
            tearoff=0,
            bg="#2d2d2d",
            fg="white",
            activebackground="#1a73e8",
            activeforeground="white",
            relief=tk.FLAT,
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        
        # Get current state
        selection_tool = self.main_window.tools.get("selection")
        has_selection = selection_tool and selection_tool.has_active_selection()
        has_copy_buffer = (hasattr(self.main_window, 'selection_mgr') and 
                          self.main_window.selection_mgr.copy_buffer is not None)
        
        # Selection operations (if there's a selection)
        if has_selection:
            menu.add_command(
                label="Copy",
                command=self._copy_selection,
                accelerator="Ctrl+C"
            )
            menu.add_separator()
            
            menu.add_command(
                label="Cut",
                command=self._cut_selection,
                accelerator="Ctrl+X"
            )
            
            menu.add_command(
                label="Delete",
                command=self._delete_selection,
                accelerator="Del"
            )
            menu.add_separator()
            
            menu.add_command(
                label="Mirror",
                command=self._mirror_selection
            )
            
            menu.add_command(
                label="Rotate",
                command=self._rotate_selection
            )
            
            menu.add_command(
                label="Scale",
                command=self._scale_selection
            )
            menu.add_separator()
        
        # Paste (if there's something copied)
        if has_copy_buffer:
            menu.add_command(
                label="Paste",
                command=self._paste_selection,
                accelerator="Ctrl+V"
            )
            menu.add_separator()
        
        # Tool-specific actions
        if self.main_window.current_tool == "fill":
            menu.add_command(
                label="Fill Here",
                command=lambda: self._fill_at_position(event)
            )
            menu.add_separator()
        
        # Common tools
        menu.add_command(
            label="Eyedropper",
            command=lambda: self._switch_to_eyedropper(event),
            accelerator="I"
        )
        
        menu.add_command(
            label="Brush",
            command=lambda: self.main_window._select_tool("brush"),
            accelerator="B"
        )
        
        menu.add_command(
            label="Eraser",
            command=lambda: self.main_window._select_tool("eraser"),
            accelerator="E"
        )
        
        menu.add_separator()
        
        # Canvas operations
        menu.add_command(
            label="Zoom Fit",
            command=self.main_window._zoom_fit
        )
        
        menu.add_command(
            label="Zoom 100%",
            command=self.main_window._zoom_100
        )
        
        menu.add_separator()
        
        # Grid/View options
        menu.add_command(
            label="Toggle Grid",
            command=self.main_window.grid_control_mgr.toggle_grid,
            accelerator="G"
        )
        
        menu.add_command(
            label="Toggle Tile Preview",
            command=self.main_window.grid_control_mgr.toggle_tile_preview
        )
        
        # Show menu at mouse position
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
            self.current_menu = None
    
    def _copy_selection(self):
        """Copy current selection"""
        if hasattr(self.main_window, 'selection_mgr'):
            self.main_window.selection_mgr.copy_selection()
            self.main_window.canvas_renderer.update_pixel_display()
    
    def _cut_selection(self):
        """Cut current selection (copy and delete)"""
        if hasattr(self.main_window, 'selection_mgr'):
            selection_tool = self.main_window.tools.get("selection")
            if selection_tool and selection_tool.has_active_selection():
                # Save undo state before cutting
                draw_layer = self.main_window._get_drawing_layer()
                if draw_layer:
                    edge_lines = None
                    edge_tool = self.main_window.tools.get("edge")
                    if edge_tool and hasattr(edge_tool, 'edge_lines'):
                        edge_lines = edge_tool.edge_lines
                    
                    self.main_window.undo_manager.save_state(
                        draw_layer.pixels.copy(),
                        self.main_window.layer_manager.active_layer_index,
                        edge_lines
                    )
                
                # Copy first
                self.main_window.selection_mgr.copy_selection()
                
                # Then delete selection
                if draw_layer:
                    bounds = selection_tool.get_selection_bounds()
                    if bounds:
                        left, top, width, height = bounds
                        # Clear the selection area
                        for y in range(top, top + height):
                            for x in range(left, left + width):
                                if 0 <= x < self.main_window.canvas.width and 0 <= y < self.main_window.canvas.height:
                                    draw_layer.set_pixel(x, y, (0, 0, 0, 0))
                        
                        # Clear selection
                        selection_tool.clear_selection()
                        self.main_window.layer_manager.invalidate_cache()
                        self.main_window._update_canvas_from_layers()
                        self.main_window.canvas_renderer.update_pixel_display()
    
    def _delete_selection(self):
        """Delete current selection"""
        selection_tool = self.main_window.tools.get("selection")
        if selection_tool and selection_tool.has_active_selection():
            draw_layer = self.main_window._get_drawing_layer()
            if draw_layer:
                # Save undo state before deleting
                edge_lines = None
                edge_tool = self.main_window.tools.get("edge")
                if edge_tool and hasattr(edge_tool, 'edge_lines'):
                    edge_lines = edge_tool.edge_lines
                
                self.main_window.undo_manager.save_state(
                    draw_layer.pixels.copy(),
                    self.main_window.layer_manager.active_layer_index,
                    edge_lines
                )
                
                bounds = selection_tool.get_selection_bounds()
                if bounds:
                    left, top, width, height = bounds
                    # Clear the selection area
                    for y in range(top, top + height):
                        for x in range(left, left + width):
                            if 0 <= x < self.main_window.canvas.width and 0 <= y < self.main_window.canvas.height:
                                draw_layer.set_pixel(x, y, (0, 0, 0, 0))
                    
                    # Clear selection
                    selection_tool.clear_selection()
                    self.main_window.layer_manager.invalidate_cache()
                    self.main_window._update_canvas_from_layers()
                    self.main_window.canvas_renderer.update_pixel_display()
    
    def _paste_selection(self):
        """Paste copied selection (enter placement mode)"""
        if hasattr(self.main_window, 'selection_mgr'):
            if self.main_window.selection_mgr.copy_buffer is not None:
                # Enter paste/placement mode (undo state will be saved when actually placing)
                self.main_window.selection_mgr.is_placing_copy = True
                self.main_window.canvas_renderer.update_pixel_display()
    
    def _mirror_selection(self):
        """Mirror the selection"""
        if hasattr(self.main_window, 'selection_mgr'):
            self.main_window.selection_mgr.mirror_selection()
    
    def _rotate_selection(self):
        """Rotate the selection"""
        if hasattr(self.main_window, 'selection_mgr'):
            self.main_window.selection_mgr.rotate_selection()
    
    def _scale_selection(self):
        """Scale the selection"""
        if hasattr(self.main_window, 'selection_mgr'):
            self.main_window.selection_mgr.scale_selection()
    
    def _fill_at_position(self, event):
        """Fill at the clicked position"""
        # Convert screen coordinates to canvas coordinates
        canvas_x, canvas_y = self.main_window._tkinter_screen_to_canvas_coords(event.x, event.y)
        
        # Check bounds
        if 0 <= canvas_x < self.main_window.canvas.width and 0 <= canvas_y < self.main_window.canvas.height:
            # Switch to fill tool and execute fill
            self.main_window._select_tool("fill")
            fill_tool = self.main_window.tools.get("fill")
            if fill_tool:
                draw_layer = self.main_window._get_drawing_layer()
                if draw_layer:
                    current_color = self.main_window.get_current_color()
                    fill_tool.on_mouse_down(draw_layer, canvas_x, canvas_y, 1, current_color)
                    self.main_window._update_canvas_from_layers()
                    self.main_window.canvas_renderer.update_pixel_display()
    
    def _switch_to_eyedropper(self, event):
        """Switch to eyedropper and sample at position"""
        # Convert screen coordinates to canvas coordinates
        canvas_x, canvas_y = self.main_window._tkinter_screen_to_canvas_coords(event.x, event.y)
        
        # Check bounds
        if 0 <= canvas_x < self.main_window.canvas.width and 0 <= canvas_y < self.main_window.canvas.height:
            # Switch to eyedropper and sample
            self.main_window._select_tool("eyedropper")
            self.main_window._handle_eyedropper_click(canvas_x, canvas_y, 1)
