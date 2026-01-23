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
        
        # Loading completion callback
        self.on_loading_complete = None
        
        # Loading screen reference (set by main window)
        self.loading_screen_frame = None
    
    def save_state(self):
        """Save current window and panel state to config file"""
        try:
            state = {
                'window_geometry': self.root.geometry(),
                'left_panel_width': self.left_container.winfo_width(),
                'right_panel_width': self.right_container.winfo_width(),
                'screen_width': self.root.winfo_screenwidth(),
                'screen_height': self.root.winfo_screenheight()
            }
            
            config_dir = os.path.join(os.path.expanduser("~"), ".pixelperfect")
            os.makedirs(config_dir, exist_ok=True)
            config_file = os.path.join(config_dir, "window_state.json")
            
            with open(config_file, 'w') as f:
                json.dump(state, f, indent=2)
                
        except Exception:
            pass
    
    def restore_state(self):
        """Restore saved window state on startup"""
        try:
            config_dir = os.path.join(os.path.expanduser("~"), ".pixelperfect")
            config_file = os.path.join(config_dir, "window_state.json")
            
            if not os.path.exists(config_file):
                return False
            
            with open(config_file, 'r') as f:
                state = json.load(f)
            
            # Check if screen resolution matches
            current_screen_width = self.root.winfo_screenwidth()
            current_screen_height = self.root.winfo_screenheight()
            
            if (state.get('screen_width') != current_screen_width or 
                state.get('screen_height') != current_screen_height):
                return False
            
            # Restore window geometry with safety checks
            if 'window_geometry' in state:
                geometry_parts = state['window_geometry'].split('+')
                size_part = geometry_parts[0]
                width, height = map(int, size_part.split('x'))
                
                x_pos = int(geometry_parts[1]) if len(geometry_parts) > 1 else 100
                y_pos = int(geometry_parts[2]) if len(geometry_parts) > 2 else 100
                
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                taskbar_margin = 70
                
                min_width = 1200
                min_height = 700
                max_height = screen_height - taskbar_margin
                
                preferred_height = 800
                if height > max_height or height > 900:
                    height = min(preferred_height, max_height)
                
                width = max(width, min_width)
                height = max(min_height, min(height, max_height))
                
                max_y = screen_height - height - taskbar_margin
                if y_pos > max_y or y_pos + height > screen_height - taskbar_margin:
                    y_pos = (screen_height - height - taskbar_margin) // 2
                
                if x_pos < 0:
                    x_pos = 0
                elif x_pos + width > screen_width:
                    x_pos = screen_width - width - 20
                
                new_geometry = f"{width}x{height}+{x_pos}+{y_pos}"
                self.root.geometry(new_geometry)
                
                if self.loading_screen_frame and self.loading_screen_frame.winfo_exists():
                    self.loading_screen_frame.lift()
                    self.root.update_idletasks()
            
            # Use default panel widths for consistent UI
            if 'left_panel_width' in state and 'right_panel_width' in state:
                self.left_panel_width = 510
                self.right_panel_width = 510
                self._apply_panel_widths()
                return True
            else:
                self._apply_panel_widths()
                return True
            
        except Exception:
            pass
        
        return False
    
    def _apply_panel_widths(self):
        """Apply panel widths to the paned window"""
        try:
            self.root.update_idletasks()
            
            if self.loading_screen_frame and self.loading_screen_frame.winfo_exists():
                self.loading_screen_frame.lift()
            
            if self._do_apply_panel_widths_immediate():
                return
            
            self.root.after(10, self._do_apply_panel_widths)
        except Exception:
            pass
    
    def _do_apply_panel_widths_immediate(self):
        """Try to apply panel widths immediately"""
        try:
            if hasattr(self, 'paned_window') and self.paned_window:
                paned_width = self.paned_window.winfo_width()
                if paned_width > 200:
                    return self._configure_panels(paned_width)
            return False
        except Exception:
            return False
    
    def _configure_panels(self, paned_width):
        """Configure panel widths and return True if successful"""
        try:
            available_width = paned_width
            
            total_saved_width = self.left_panel_width + self.right_panel_width
            if total_saved_width > available_width:
                scale_factor = available_width / total_saved_width
                self.left_panel_width = int(self.left_panel_width * scale_factor)
                self.right_panel_width = int(self.right_panel_width * scale_factor)
            
            right_panel_actual_width = available_width - self.left_panel_width
            
            min_panel_width = 250
            if self.left_panel_width < min_panel_width:
                self.left_panel_width = min_panel_width
            if right_panel_actual_width < min_panel_width:
                self.left_panel_width = available_width - min_panel_width
                right_panel_actual_width = min_panel_width
            
            sash_position = self.left_panel_width
            
            self.paned_window.paneconfig(self.left_container, width=self.left_panel_width, minsize=200)
            self.paned_window.paneconfig(self.right_container, width=self.right_panel_width, minsize=200)
            self.paned_window.sash_place(0, sash_position, 0)
            self.paned_window.update()
            
            if self.loading_screen_frame and self.loading_screen_frame.winfo_exists():
                self.loading_screen_frame.lift()
                self.root.update_idletasks()
            
            return True
            
        except Exception:
            return False
    
    def _do_apply_panel_widths(self):
        """Actually apply the panel widths to the paned window"""
        try:
            if hasattr(self, 'paned_window') and self.paned_window:
                paned_width = self.paned_window.winfo_width()
                if paned_width > 100:
                    if self._configure_panels(paned_width):
                        return
                else:
                    if not hasattr(self, '_panel_width_retry_count'):
                        self._panel_width_retry_count = 0
                    self._panel_width_retry_count += 1
                    
                    if self._panel_width_retry_count < 5:
                        self.root.after(10, self._do_apply_panel_widths)
                    else:
                        try:
                            self.paned_window.sash_place(0, self.left_panel_width, 0)
                        except Exception:
                            pass
        except Exception:
            pass
    
    def on_window_resize(self, event):
        """Handle window resize events to maintain grid centering"""
        if self.is_resizing_panels:
            return
            
        if event.widget == self.root:
            if self.resize_timer is not None:
                try:
                    self.root.after_cancel(self.resize_timer)
                except Exception:
                    pass
            
            self.resize_timer = self.root.after(150, self._delayed_redraw)
    
    def _delayed_redraw(self):
        """Delayed redraw callback"""
        if self.redraw_callback:
            self.redraw_callback()
    
    def toggle_left_panel(self, show_loading_callback=None, finish_toggle_callback=None):
        """Collapse or expand the left panel"""
        if self.left_panel_collapsed:
            if show_loading_callback:
                show_loading_callback("left")
            
            if self.left_restore_btn:
                try:
                    self.left_restore_btn.place_forget()
                except Exception:
                    pass
            
            self.paned_window.paneconfigure(self.left_container, hide=False)
            self.left_collapse_btn.configure(text="‹")
            self.left_panel_collapsed = False
            
            # Redraw canvas to recenter after panel size change
            self.root.after(50, self.redraw_callback)
            
            if finish_toggle_callback:
                self.root.after(100, lambda: finish_toggle_callback("left"))
        else:
            self.paned_window.paneconfigure(self.left_container, hide=True)
            self.left_collapse_btn.configure(text="›")
            self.left_panel_collapsed = True
            
            if not self.left_restore_btn:
                self.left_restore_btn = tk.Button(
                    self.paned_window,
                    text="›",
                    font=("Arial", 14),
                    fg="#888888",
                    bg="#2b2b2b",
                    activebackground="#3a3a3a",
                    activeforeground="#ffffff",
                    relief=tk.FLAT,
                    borderwidth=0,
                    highlightthickness=0,
                    width=2,
                    height=2,
                    cursor="hand2",
                    command=lambda: self.toggle_left_panel(show_loading_callback, finish_toggle_callback)
                )
                self.left_restore_btn.bind("<Enter>", lambda e: self.left_restore_btn.configure(fg="#ffffff"))
                self.left_restore_btn.bind("<Leave>", lambda e: self.left_restore_btn.configure(fg="#888888"))
            
            self.left_restore_btn.place(x=5, rely=0.5, anchor='w')
            self.root.after(1, self.redraw_callback)
    
    def toggle_right_panel(self, show_loading_callback=None, finish_toggle_callback=None):
        """Collapse or expand the right panel"""
        if self.right_panel_collapsed:
            if show_loading_callback:
                show_loading_callback("right")
            
            if self.right_restore_btn:
                try:
                    self.right_restore_btn.place_forget()
                except Exception:
                    pass
            
            self.paned_window.paneconfigure(self.right_container, hide=False)
            self.right_collapse_btn.configure(text="›")
            self.right_panel_collapsed = False
            
            # Redraw canvas to recenter after panel size change
            self.root.after(50, self.redraw_callback)
            
            if finish_toggle_callback:
                self.root.after(100, lambda: finish_toggle_callback("right"))
        else:
            self.paned_window.paneconfigure(self.right_container, hide=True)
            self.right_collapse_btn.configure(text="‹")
            self.right_panel_collapsed = True
            
            if not self.right_restore_btn:
                self.right_restore_btn = tk.Button(
                    self.paned_window,
                    text="‹",
                    font=("Arial", 14),
                    fg="#888888",
                    bg="#2b2b2b",
                    activebackground="#3a3a3a",
                    activeforeground="#ffffff",
                    relief=tk.FLAT,
                    borderwidth=0,
                    highlightthickness=0,
                    width=2,
                    height=2,
                    cursor="hand2",
                    command=lambda: self.toggle_right_panel(show_loading_callback, finish_toggle_callback)
                )
                self.right_restore_btn.bind("<Enter>", lambda e: self.right_restore_btn.configure(fg="#ffffff"))
                self.right_restore_btn.bind("<Leave>", lambda e: self.right_restore_btn.configure(fg="#888888"))
            
            self.right_restore_btn.place(relx=1.0, x=-5, rely=0.5, anchor='e')
            self.root.after(1, self.redraw_callback)
