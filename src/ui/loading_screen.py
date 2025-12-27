"""
Loading Screen Manager for Pixel Perfect
Provides a professional loading screen that covers the UI during initialization

TECHNICAL NOTES:
1. This loading screen uses a Toplevel window as a system-level overlay
2. This design is CRITICAL for preventing the loading screen from being displaced
   by widget geometry changes during UI creation
3. Key components:
   - Toplevel window with overrideredirect and -topmost attributes
   - Dynamic positioning to stay aligned with main window
   - Focus management to prevent interaction
   - Proper show/hide methods (withdraw/deiconify)

DO NOT MODIFY THIS DESIGN WITHOUT UNDERSTANDING THE IMPLICATIONS:
- Don't change to regular Frame/CTkFrame (will break overlay behavior)
- Don't remove topmost/overrideredirect (will allow window to be hidden)
- Don't skip geometry updates (will misalign overlay)
- Don't use place/place_forget (use withdraw/deiconify)

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import customtkinter as ctk
import tkinter as tk
import time


class LoadingScreen:
    """Professional loading screen that covers the UI during initialization"""

    def __init__(self, root: ctk.CTk):
        """
        Initialize the loading screen

        Args:
            root: The main CustomTkinter root window
        """
        self.root = root
        self.loading_frame = None
        self.progress_bar = None
        self.status_label = None
        self.progress_value = 0
        self.is_visible = False

        # Loading steps and their progress values
        self.loading_steps = [
            ("Initializing core systems...", 10),
            ("Loading UI components...", 25),
            ("Setting up canvas and tools...", 40),
            ("Configuring panels...", 55),
            ("Applying themes...", 70),
            ("Finalizing interface...", 85),
            ("Ready!", 100)
        ]
        self.current_step = 0

        self._create_loading_ui()
        
        # Keep overlay synced to the window at all times
        try:
            self.root.bind('<Configure>', self._sync_overlay_bounds)
        except Exception:
            pass

    def _get_main_window_bounds(self):
        """Return screen-aligned bounds (x, y, width, height) of the main window."""
        try:
            if self.root and self.root.winfo_exists():
                self.root.update_idletasks()

            x = int(self.root.winfo_rootx())
            y = int(self.root.winfo_rooty())
            width = int(self.root.winfo_width())
            height = int(self.root.winfo_height())

            # On Windows, prefer the real outer window rect (includes decorations)
            import platform
            if platform.system() == 'Windows':
                try:
                    import ctypes
                    from ctypes import wintypes

                    hwnd = int(self.root.winfo_id())
                    rect = wintypes.RECT()
                    if ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                        win_x = int(rect.left)
                        win_y = int(rect.top)
                        win_w = int(rect.right - rect.left)
                        win_h = int(rect.bottom - rect.top)

                        x = min(x, win_x)
                        y = min(y, win_y)
                        width = max(width, win_w)
                        height = max(height, win_h)
                except Exception:
                    pass

            return x, y, width, height
        except Exception:
            return 0, 0, max(1, self.root.winfo_width()), max(1, self.root.winfo_height())

    def _sync_overlay_bounds(self, *args):
        """Synchronize overlay to main window bounds when it moves/resizes."""
        try:
            if not self.is_visible:
                return
            if not (self.loading_frame and self.loading_frame.winfo_exists()):
                return

            x, y, width, height = self._get_main_window_bounds()
            self.loading_frame.geometry(f"{width}x{height}+{x}+{y}")
            self.loading_frame.lift()
        except Exception:
            pass
    
    def _create_loading_ui(self):
        """Create the loading screen UI"""
        try:
            # Create loading frame as a system-level overlay window
            self.loading_frame = tk.Toplevel(self.root)
            self.loading_frame.withdraw()
            self.loading_frame.overrideredirect(True)
            self.loading_frame.attributes('-topmost', True)
            self.loading_frame.configure(bg="#1a1a1a")
            
            # Inner frame for CustomTkinter widgets
            self.inner_frame = ctk.CTkFrame(
                self.loading_frame,
                fg_color="#1a1a1a",
                corner_radius=0
            )
            self.inner_frame.place(x=0, y=0, relwidth=1, relheight=1)

            # Main container for centered content
            main_container = ctk.CTkFrame(
                self.inner_frame,
                fg_color="transparent"
            )
            main_container.place(relx=0.5, rely=0.5, anchor="center")

            # App title
            title_label = ctk.CTkLabel(
                main_container,
                text="Pixel Perfect",
                font=("Arial", 36, "bold"),
                text_color="#ffffff"
            )
            title_label.pack(pady=(0, 10))

            # Subtitle
            subtitle_label = ctk.CTkLabel(
                main_container,
                text="Retro Pixel Art Editor",
                font=("Arial", 16),
                text_color="#cccccc"
            )
            subtitle_label.pack(pady=(0, 40))

            # Progress bar
            self.progress_bar = ctk.CTkProgressBar(
                main_container,
                width=300,
                height=20,
                progress_color="#4a9eff",
                fg_color="#333333"
            )
            self.progress_bar.pack(pady=(0, 20))
            self.progress_bar.set(0)

            # Status label
            self.status_label = ctk.CTkLabel(
                main_container,
                text="Starting...",
                font=("Arial", 14),
                text_color="#ffffff"
            )
            self.status_label.pack()

            # Version info
            version_label = ctk.CTkLabel(
                main_container,
                text="Version 2.6.0",
                font=("Arial", 10),
                text_color="#888888"
            )
            version_label.pack(pady=(40, 0))

            self.loading_frame.withdraw()
        except Exception as e:
            print(f"[Loading Screen] Error creating UI: {e}")
            raise
    
    def show(self):
        """Show the loading screen"""
        if not self.is_visible:
            try:
                if self.loading_frame and self.loading_frame.winfo_exists():
                    self.root.update()
                    self.root.update_idletasks()

                    x, y, width, height = self._get_main_window_bounds()
                    self.loading_frame.geometry(f"{width}x{height}+{x}+{y}")
                    self.loading_frame.update_idletasks()
                    self.loading_frame.update()
                    
                    self.loading_frame.deiconify()
                    self.loading_frame.lift()
                    self.loading_frame.focus_force()
                self.is_visible = True
                if self.root and self.root.winfo_exists():
                    self.root.update_idletasks()
            except Exception:
                pass
    
    def hide(self):
        """Hide the loading screen"""
        if self.is_visible:
            try:
                if hasattr(self, 'loading_frame') and self.loading_frame and self.loading_frame.winfo_exists():
                    self.loading_frame.withdraw()
                self.is_visible = False
                if self.root and self.root.winfo_exists():
                    self.root.update_idletasks()
            except Exception:
                pass
    
    def update_progress(self, step_name: str, progress: int):
        """
        Update the loading progress

        Args:
            step_name: Name of the current loading step
            progress: Progress value (0-100)
        """
        if self.is_visible:
            try:
                status_exists = hasattr(self, 'status_label') and self.status_label and self.status_label.winfo_exists()
                progress_exists = hasattr(self, 'progress_bar') and self.progress_bar and self.progress_bar.winfo_exists()
                frame_exists = hasattr(self, 'loading_frame') and self.loading_frame and self.loading_frame.winfo_exists()

                if status_exists:
                    self.status_label.configure(text=step_name)
                if progress_exists:
                    self.progress_bar.set(progress / 100.0)
                
                if frame_exists:
                    self.loading_frame.lift()
                    self.loading_frame.focus_force()
                    x, y, width, height = self._get_main_window_bounds()
                    self.loading_frame.geometry(f"{width}x{height}+{x}+{y}")
                    self.loading_frame.update_idletasks()
                
                if self.root and self.root.winfo_exists():
                    self.root.update_idletasks()
            except Exception:
                pass
    
    def next_step(self):
        """Move to the next loading step"""
        if self.current_step < len(self.loading_steps):
            step_name, progress = self.loading_steps[self.current_step]
            self.update_progress(step_name, progress)
            self.current_step += 1
    
    def set_custom_progress(self, step_name: str, progress: int):
        """
        Set custom progress (for specific loading operations)
        
        Args:
            step_name: Custom step name
            progress: Progress value (0-100)
        """
        self.update_progress(step_name, progress)


class LoadingManager:
    """Manages the loading screen lifecycle and coordinates with initialization"""
    
    def __init__(self, root: ctk.CTk):
        """
        Initialize the loading manager
        
        Args:
            root: The main CustomTkinter root window
        """
        self.root = root
        self.loading_screen = LoadingScreen(root)
        self.loading_complete = False
        self.loading_thread = None
    
    def start_loading(self):
        """Start the loading screen"""
        self.loading_screen.show()
        self.loading_screen.next_step()
    
    def update_loading(self, step_name: str, progress: int):
        """
        Update loading progress

        Args:
            step_name: Name of the current step
            progress: Progress value (0-100)
        """
        if not self.loading_complete:
            self.loading_screen.set_custom_progress(step_name, progress)
    
    def complete_loading(self):
        """Complete the loading process"""
        if not self.loading_complete:
            try:
                self.loading_screen.update_progress("Ready!", 100)
                time.sleep(0.5)
                self.loading_screen.hide()
                self.loading_complete = True
            except Exception:
                self.loading_complete = True

    def finish_loading(self):
        """Alternative completion method for delayed finishing"""
        if not self.loading_complete:
            try:
                self.loading_screen.update_progress("Ready!", 100)
                time.sleep(0.3)
                self.loading_screen.hide()
                self.loading_complete = True
            except Exception:
                self.loading_complete = True
    
    def is_loading(self) -> bool:
        """Check if loading is in progress"""
        return not self.loading_complete
