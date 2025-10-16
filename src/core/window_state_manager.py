"""
Window State Manager for Pixel Perfect
Handles window geometry, panel state, and collapse/restore functionality
"""

import json
import os
import tkinter as tk


class WindowStateManager:
    """Manages window and panel state persistence and manipulation"""
    
    def __init__(self, root, left_container, right_container, paned_window, 
                 left_collapse_btn, right_collapse_btn, redraw_callback):
        """
        Initialize the window state manager
        
        Args:
            root: The main Tkinter root window
            left_container: Left panel container widget
            right_container: Right panel container widget
            paned_window: The PanedWindow widget
            left_collapse_btn: Left panel collapse button
            right_collapse_btn: Right panel collapse button
            redraw_callback: Callback function to redraw canvas after resize
        """
        self.root = root
        self.left_container = left_container
        self.right_container = right_container
        self.paned_window = paned_window
        self.left_collapse_btn = left_collapse_btn
        self.right_collapse_btn = right_collapse_btn
        self.redraw_callback = redraw_callback
        
        # State tracking
        self.left_panel_collapsed = False
        self.right_panel_collapsed = False
        self.is_resizing_panels = False
        self.resize_timer = None
        
        # Restore buttons (created on demand)
        self.left_restore_btn = None
        self.right_restore_btn = None
        
        # Default panel widths (510px each for best first impression)
        self.left_panel_width = 510
        self.right_panel_width = 510
    
    def save_state(self):
        """Save current window and panel state to config file"""
        try:
            # Get current state
            state = {
                'window_geometry': self.root.geometry(),
                'left_panel_width': self.left_container.winfo_width(),
                'right_panel_width': self.right_container.winfo_width(),
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
    
    def restore_state(self):
        """Restore saved window state on startup"""
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
            
            if (state.get('screen_width') != current_screen_width or 
                state.get('screen_height') != current_screen_height):
                print(f"[Window State] Screen resolution changed, recalculating panel sizes")
                return False
            
            # Restore window geometry, but ensure minimum size and taskbar clearance
            if 'window_geometry' in state:
                # Parse the geometry string (e.g., "851x987+1105+122")
                geometry_parts = state['window_geometry'].split('+')
                size_part = geometry_parts[0]
                width, height = map(int, size_part.split('x'))
                
                # Get position if available
                x_pos = int(geometry_parts[1]) if len(geometry_parts) > 1 else 100
                y_pos = int(geometry_parts[2]) if len(geometry_parts) > 2 else 100
                
                # Get screen dimensions
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                taskbar_margin = 70  # Increased margin for safety
                
                # Ensure minimum window size for proper panel display
                min_width = 1200
                min_height = 700
                
                # Calculate maximum safe height (leave room for taskbar)
                max_height = screen_height - taskbar_margin
                
                # Force reasonable default height if saved state is too tall
                # This prevents the window from ever going below taskbar
                preferred_height = 800  # Our new default (increased by 150px)
                if height > max_height or height > 900:  # If saved height is too tall
                    height = min(preferred_height, max_height)
                    print(f"[Window State] Reduced excessive height to: {height}px (was too tall)")
                
                # Ensure minimum and maximum sizes
                width = max(width, min_width)
                height = max(min_height, min(height, max_height))
                
                print(f"[Window State] Final dimensions: {width}x{height} (max allowed: {max_height})")
                
                # Ensure position doesn't cause window to go below taskbar
                max_y = screen_height - height - taskbar_margin
                if y_pos > max_y or y_pos + height > screen_height - taskbar_margin:
                    # Recalculate position to center window above taskbar
                    y_pos = (screen_height - height - taskbar_margin) // 2
                    print(f"[Window State] Adjusted Y position to avoid taskbar: {y_pos}")
                
                # Ensure position doesn't go off screen horizontally
                if x_pos < 0:
                    x_pos = 0
                elif x_pos + width > screen_width:
                    x_pos = screen_width - width - 20
                
                # Apply the adjusted geometry
                new_geometry = f"{width}x{height}+{x_pos}+{y_pos}"
                self.root.geometry(new_geometry)
                print(f"[Window State] Applied geometry: {new_geometry} (screen: {screen_width}x{screen_height})")
            
            # Restore panel widths, but ensure they're reasonable
            if 'left_panel_width' in state and 'right_panel_width' in state:
                saved_left = state['left_panel_width']
                saved_right = state['right_panel_width']
                
                # If saved widths are too small, use better defaults
                min_reasonable_width = 400
                if saved_left < min_reasonable_width or saved_right < min_reasonable_width:
                    print(f"[Window State] Saved panel widths too small ({saved_left}x{saved_right}), using better defaults")
                    self.left_panel_width = 510  # Good size for tools and palette
                    self.right_panel_width = 510  # Good size for layers and animation
                else:
                    self.left_panel_width = saved_left
                    self.right_panel_width = saved_right
                
                print(f"[Window State] Using panel widths: {self.left_panel_width}x{self.right_panel_width}")
                
                # Apply the restored widths to the paned window
                self._apply_panel_widths()
                return True
            
        except Exception as e:
            print(f"[Window State] Error restoring state: {e}")
        
        return False
    
    def _apply_panel_widths(self):
        """Apply panel widths to the paned window"""
        try:
            # Force window to update and render first
            self.root.update_idletasks()
            self.root.update()
            
            # Schedule the application after the window is fully initialized
            # Increased delay to ensure window is rendered
            self.root.after(500, self._do_apply_panel_widths)
        except Exception as e:
            print(f"[Window State] Error scheduling panel width application: {e}")
    
    def _do_apply_panel_widths(self):
        """Actually apply the panel widths to the paned window"""
        try:
            if hasattr(self, 'paned_window') and self.paned_window:
                # Get the actual paned window width (not root window width)
                paned_width = self.paned_window.winfo_width()
                if paned_width > 100:  # Make sure paned window is actually visible
                    
                    # Calculate the right panel width from the total paned window width
                    # Total width = left_width + right_width
                    # So right_width = total_width - left_width
                    available_width = paned_width
                    
                    # If the saved widths don't fit in the current window, recalculate proportionally
                    total_saved_width = self.left_panel_width + self.right_panel_width
                    if total_saved_width > available_width:
                        # Scale down proportionally to fit
                        scale_factor = available_width / total_saved_width
                        self.left_panel_width = int(self.left_panel_width * scale_factor)
                        self.right_panel_width = int(self.right_panel_width * scale_factor)
                        print(f"[Window State] Scaled panel widths to fit window (scale: {scale_factor:.2f})")
                    
                    right_panel_actual_width = available_width - self.left_panel_width
                    
                    # Ensure minimum panel widths
                    min_panel_width = 250  # Increased minimum for better usability
                    if self.left_panel_width < min_panel_width:
                        self.left_panel_width = min_panel_width
                    if right_panel_actual_width < min_panel_width:
                        # Adjust left panel to accommodate minimum right panel
                        self.left_panel_width = available_width - min_panel_width
                        right_panel_actual_width = min_panel_width
                    
                    # Configure the paned window panels with proper widths
                    sash_position = self.left_panel_width
                    
                    # Configure left panel
                    self.paned_window.paneconfig(self.left_container, width=self.left_panel_width, minsize=200)
                    
                    # Configure right panel  
                    self.paned_window.paneconfig(self.right_container, width=self.right_panel_width, minsize=200)
                    
                    # Set the sash position
                    self.paned_window.sash_place(0, sash_position, 0)
                    
                    # Force the paned window to update its layout
                    self.paned_window.update()
                    
                    print(f"[Window State] Applied panel widths to paned window:")
                    print(f"  - Paned window width: {paned_width}")
                    print(f"  - Left panel: {self.left_panel_width}px")
                    print(f"  - Right panel: {right_panel_actual_width}px")
                    print(f"  - Sash position: {sash_position}")
                else:
                    print(f"[Window State] Paned window not ready (width: {paned_width}), retrying...")
                    # Retry after a short delay (max 3 attempts)
                    if not hasattr(self, '_panel_width_retry_count'):
                        self._panel_width_retry_count = 0
                    self._panel_width_retry_count += 1
                    
                    if self._panel_width_retry_count < 5:
                        self.root.after(200, self._do_apply_panel_widths)
                    else:
                        print(f"[Window State] ERROR: Paned window failed to initialize properly after {self._panel_width_retry_count} attempts")
                        # Force a reasonable default anyway
                        try:
                            self.paned_window.sash_place(0, self.left_panel_width, 0)
                            print(f"[Window State] Forced sash position to {self.left_panel_width} as fallback")
                        except:
                            pass
        except Exception as e:
            print(f"[Window State] Error applying panel widths: {e}")
    
    def on_window_resize(self, event):
        """Handle window resize events to maintain grid centering"""
        # Skip if we're resizing panels (not the window)
        if self.is_resizing_panels:
            return
            
        # Only handle main window resize, not child widget events
        if event.widget == self.root:
            # Schedule a delayed redraw to avoid excessive updates during resize
            if self.resize_timer is not None:
                try:
                    self.root.after_cancel(self.resize_timer)
                except:
                    pass  # Timer already executed or cancelled
            
            self.resize_timer = self.root.after(100, self.redraw_callback)
    
    def toggle_left_panel(self, show_loading_callback=None, finish_toggle_callback=None):
        """Collapse or expand the left panel"""
        if self.left_panel_collapsed:
            # Show loading indicator
            if show_loading_callback:
                show_loading_callback("left")
            
            # Expand panel - remove restore button overlay
            if self.left_restore_btn:
                try:
                    self.left_restore_btn.place_forget()
                except:
                    pass
            
            # Show the container (INSTANT - no widget recreation!)
            self.paned_window.paneconfigure(self.left_container, hide=False)
            
            self.left_collapse_btn.configure(text="◀")
            self.left_panel_collapsed = False
            
            # Hide loading indicator and redraw canvas (give more time for rendering)
            if finish_toggle_callback:
                self.root.after(100, lambda: finish_toggle_callback("left"))
        else:
            # Hide the container (INSTANT - no widget destruction!)
            self.paned_window.paneconfigure(self.left_container, hide=True)
            self.left_collapse_btn.configure(text="▶")
            self.left_panel_collapsed = True
            
            # Create restore button if it doesn't exist (overlay on left edge)
            if not self.left_restore_btn:
                # Use regular tkinter button with custom styling for true transparency
                self.left_restore_btn = tk.Button(
                    self.paned_window,
                    text="▶",
                    font=("Arial", 18, "bold"),
                    fg="white",
                    bg="#1f538d",
                    activebackground="#2a6bb3",
                    activeforeground="white",
                    relief=tk.FLAT,
                    borderwidth=0,
                    highlightthickness=0,
                    width=3,
                    height=4,
                    cursor="hand2",
                    command=lambda: self.toggle_left_panel(show_loading_callback, finish_toggle_callback)
                )
                # Bind hover events for color change
                self.left_restore_btn.bind("<Enter>", lambda e: self.left_restore_btn.configure(bg="#2a6bb3"))
                self.left_restore_btn.bind("<Leave>", lambda e: self.left_restore_btn.configure(bg="#1f538d"))
            
            # Place restore button directly on left edge
            self.left_restore_btn.place(x=5, y=100)
            
            # Redraw canvas to re-center grid after panel collapse (minimal delay)
            self.root.after(1, self.redraw_callback)
    
    def toggle_right_panel(self, show_loading_callback=None, finish_toggle_callback=None):
        """Collapse or expand the right panel"""
        if self.right_panel_collapsed:
            # Show loading indicator
            if show_loading_callback:
                show_loading_callback("right")
            
            # Expand panel - remove restore button overlay
            if self.right_restore_btn:
                try:
                    self.right_restore_btn.place_forget()
                except:
                    pass
            
            # Show the container (INSTANT - no widget recreation!)
            self.paned_window.paneconfigure(self.right_container, hide=False)
            
            self.right_collapse_btn.configure(text="▶")
            self.right_panel_collapsed = False
            
            # Hide loading indicator and redraw canvas (give more time for rendering)
            if finish_toggle_callback:
                self.root.after(100, lambda: finish_toggle_callback("right"))
        else:
            # Hide the container (INSTANT - no widget destruction!)
            self.paned_window.paneconfigure(self.right_container, hide=True)
            self.right_collapse_btn.configure(text="◀")
            self.right_panel_collapsed = True
            
            # Create restore button if it doesn't exist (overlay on right edge)
            if not self.right_restore_btn:
                # Use regular tkinter button with custom styling for true transparency
                self.right_restore_btn = tk.Button(
                    self.paned_window,
                    text="◀",
                    font=("Arial", 18, "bold"),
                    fg="white",
                    bg="#1f538d",
                    activebackground="#2a6bb3",
                    activeforeground="white",
                    relief=tk.FLAT,
                    borderwidth=0,
                    highlightthickness=0,
                    width=3,
                    height=4,
                    cursor="hand2",
                    command=lambda: self.toggle_right_panel(show_loading_callback, finish_toggle_callback)
                )
                # Bind hover events for color change
                self.right_restore_btn.bind("<Enter>", lambda e: self.right_restore_btn.configure(bg="#2a6bb3"))
                self.right_restore_btn.bind("<Leave>", lambda e: self.right_restore_btn.configure(bg="#1f538d"))
            
            # Place restore button directly on right edge
            # Use anchor='ne' to position from right edge (match left button offset)
            self.right_restore_btn.place(relx=1.0, x=-5, y=100, anchor='ne')
            
            # Redraw canvas to re-center grid after panel collapse (minimal delay)
            self.root.after(1, self.redraw_callback)

