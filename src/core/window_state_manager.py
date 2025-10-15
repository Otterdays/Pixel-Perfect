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
        
        # Default panel widths
        self.left_panel_width = 350
        self.right_panel_width = 320
    
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
            
            # Restore window geometry
            if 'window_geometry' in state:
                self.root.geometry(state['window_geometry'])
                print(f"[Window State] Restored window geometry: {state['window_geometry']}")
            
            # Restore panel widths
            if 'left_panel_width' in state and 'right_panel_width' in state:
                self.left_panel_width = state['left_panel_width']
                self.right_panel_width = state['right_panel_width']
                print(f"[Window State] Restored panel widths: {self.left_panel_width}x{self.right_panel_width}")
                return True
            
        except Exception as e:
            print(f"[Window State] Error restoring state: {e}")
        
        return False
    
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

