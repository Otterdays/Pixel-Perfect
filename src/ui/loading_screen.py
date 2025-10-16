"""
Loading Screen Manager for Pixel Perfect
Provides a professional loading screen that covers the UI during initialization

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import customtkinter as ctk
import tkinter as tk
import threading
import time
from typing import Callable, Optional


class LoadingScreen:
    """Professional loading screen that covers the UI during initialization"""

    def __init__(self, root: ctk.CTk):
        """
        Initialize the loading screen

        Args:
            root: The main CustomTkinter root window
        """
        print(f"[Loading Screen] Initializing for root: {root}")
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

        # Create the loading screen UI
        print("[Loading Screen] Creating loading UI...")
        self._create_loading_ui()
        print("[Loading Screen] Loading UI created successfully")
    
    def _create_loading_ui(self):
        """Create the loading screen UI"""
        print(f"[Loading Screen] Creating UI elements...")
        # Create main loading frame that covers the entire window
        try:
            self.loading_frame = ctk.CTkFrame(
                self.root,
                fg_color="#1a1a1a",  # Dark background
                corner_radius=0
            )
            print(f"[Loading Screen] Created main frame: {self.loading_frame}")

            # Make it cover the entire window
            self.loading_frame.place(x=0, y=0, relwidth=1, relheight=1)
            print("[Loading Screen] Placed main frame to cover window")

            # Main container for centered content
            main_container = ctk.CTkFrame(
                self.loading_frame,
                fg_color="transparent"
            )
            main_container.place(relx=0.5, rely=0.5, anchor="center")
            print("[Loading Screen] Created and placed main container")

            # App title
            title_label = ctk.CTkLabel(
                main_container,
                text="Pixel Perfect",
                font=("Arial", 36, "bold"),
                text_color="#ffffff"
            )
            title_label.pack(pady=(0, 10))
            print("[Loading Screen] Created title label")

            # Subtitle
            subtitle_label = ctk.CTkLabel(
                main_container,
                text="Retro Pixel Art Editor",
                font=("Arial", 16),
                text_color="#cccccc"
            )
            subtitle_label.pack(pady=(0, 40))
            print("[Loading Screen] Created subtitle label")

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
            print(f"[Loading Screen] Created progress bar: {self.progress_bar}")

            # Status label
            self.status_label = ctk.CTkLabel(
                main_container,
                text="Starting...",
                font=("Arial", 14),
                text_color="#ffffff"
            )
            self.status_label.pack()
            print(f"[Loading Screen] Created status label: {self.status_label}")

            # Version info
            version_label = ctk.CTkLabel(
                main_container,
                text="Version 2.1.0",
                font=("Arial", 10),
                text_color="#888888"
            )
            version_label.pack(pady=(40, 0))
            print("[Loading Screen] Created version label")

            # Initially hidden
            self.loading_frame.place_forget()
            print("[Loading Screen] Initially hidden loading frame")
        except Exception as e:
            print(f"[Loading Screen] Error creating UI: {e}")
            raise
    
    def show(self):
        """Show the loading screen"""
        print(f"[Loading Screen] Show called, visible: {self.is_visible}")
        if not self.is_visible:
            try:
                print(f"[Loading Screen] Showing loading frame: {self.loading_frame}")
                if self.loading_frame and self.loading_frame.winfo_exists():
                    self.loading_frame.place(x=0, y=0, relwidth=1, relheight=1)
                    self.loading_frame.lift()  # Raise above all other widgets
                    print("[Loading Screen] Loading frame placed and lifted")
                else:
                    print("[Loading Screen] Loading frame does not exist!")
                self.is_visible = True
                print(f"[Loading Screen] Set visible to True, now: {self.is_visible}")
                if self.root and self.root.winfo_exists():
                    # Use update_idletasks to avoid flickering
                    self.root.update_idletasks()
                    print("[Loading Screen] Root updated (idletasks only)")
                else:
                    print("[Loading Screen] Root does not exist!")
            except Exception as e:
                print(f"[Loading Screen] Error showing: {e}")
    
    def hide(self):
        """Hide the loading screen"""
        print(f"[Loading Screen] Hide called, visible: {self.is_visible}")
        if self.is_visible:
            try:
                print(f"[Loading Screen] Hiding loading frame: {self.loading_frame}")
                if hasattr(self, 'loading_frame') and self.loading_frame and self.loading_frame.winfo_exists():
                    self.loading_frame.place_forget()
                    print("[Loading Screen] Loading frame forgotten")
                else:
                    print("[Loading Screen] Loading frame does not exist for hiding!")
                self.is_visible = False
                print(f"[Loading Screen] Set visible to False, now: {self.is_visible}")
                if self.root and self.root.winfo_exists():
                    # Use update_idletasks to avoid flickering
                    self.root.update_idletasks()
                    print("[Loading Screen] Root updated after hide (idletasks only)")
                else:
                    print("[Loading Screen] Root does not exist for hide update!")
            except Exception as e:
                print(f"[Loading Screen] Error hiding: {e}")
    
    def update_progress(self, step_name: str, progress: int):
        """
        Update the loading progress

        Args:
            step_name: Name of the current loading step
            progress: Progress value (0-100)
        """
        print(f"[Loading Screen] Update progress called: '{step_name}' ({progress}%)")
        print(f"[Loading Screen] Visible: {self.is_visible}")
        if self.is_visible:
            try:
                # Check if widgets still exist before updating
                status_exists = hasattr(self, 'status_label') and self.status_label and self.status_label.winfo_exists()
                progress_exists = hasattr(self, 'progress_bar') and self.progress_bar and self.progress_bar.winfo_exists()
                root_exists = self.root and self.root.winfo_exists()
                frame_exists = hasattr(self, 'loading_frame') and self.loading_frame and self.loading_frame.winfo_exists()

                print(f"[Loading Screen] Status label exists: {status_exists}")
                print(f"[Loading Screen] Progress bar exists: {progress_exists}")
                print(f"[Loading Screen] Frame exists: {frame_exists}")
                print(f"[Loading Screen] Root exists: {root_exists}")

                if status_exists:
                    self.status_label.configure(text=step_name)
                    print(f"[Loading Screen] Status label updated to: '{step_name}'")
                if progress_exists:
                    self.progress_bar.set(progress / 100.0)
                    print(f"[Loading Screen] Progress bar set to: {progress}%")
                
                # Keep loading screen on top after each update
                if frame_exists:
                    self.loading_frame.lift()
                    print("[Loading Screen] Frame lifted to stay on top")
                
                if root_exists:
                    # Use update_idletasks instead of update to avoid rendering flicker
                    self.root.update_idletasks()
                    print("[Loading Screen] Root updated (idletasks only)")
                else:
                    print("[Loading Screen] Cannot update - widgets don't exist!")
            except Exception as e:
                print(f"[Loading Screen] Error updating progress: {e}")
                print(f"[Loading Screen] Exception type: {type(e)}")
        else:
            print("[Loading Screen] Not updating - screen not visible")
    
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
        print("[Loading Manager] Starting loading screen...")
        self.loading_screen.show()
        print("[Loading Manager] Loading screen shown")
        self.loading_screen.next_step()  # "Initializing core systems..."
        print("[Loading Manager] Next step called")
    
    def update_loading(self, step_name: str, progress: int):
        """
        Update loading progress

        Args:
            step_name: Name of the current step
            progress: Progress value (0-100)
        """
        print(f"[Loading Manager] Update loading: '{step_name}' ({progress}%)")
        if not self.loading_complete:
            print(f"[Loading Manager] Loading not complete, updating screen...")
            self.loading_screen.set_custom_progress(step_name, progress)
        else:
            print("[Loading Manager] Loading already complete, ignoring update")
    
    def complete_loading(self):
        """Complete the loading process"""
        print(f"[Loading Manager] Complete loading called, loading_complete: {self.loading_complete}")
        if not self.loading_complete:
            try:
                print("[Loading Manager] Completing loading...")
                self.loading_screen.update_progress("Ready!", 100)
                print("[Loading Manager] Progress updated to Ready!")
                time.sleep(0.5)  # Brief pause to show completion
                print("[Loading Manager] Sleeping for 0.5 seconds...")
                self.loading_screen.hide()
                print("[Loading Manager] Loading screen hidden")
                self.loading_complete = True
                print(f"[Loading Manager] Loading complete set to True, now: {self.loading_complete}")
            except Exception as e:
                print(f"[Loading Manager] Error completing loading: {e}")
                print(f"[Loading Manager] Exception type: {type(e)}")
                self.loading_complete = True
                print(f"[Loading Manager] Loading complete set to True after error, now: {self.loading_complete}")
        else:
            print("[Loading Manager] Loading already complete, ignoring complete call")

    def finish_loading(self):
        """Alternative completion method for delayed finishing"""
        print(f"[Loading Manager] Finish loading called, loading_complete: {self.loading_complete}")
        if not self.loading_complete:
            try:
                print("[Loading Manager] Finishing loading...")
                self.loading_screen.update_progress("Ready!", 100)
                print("[Loading Manager] Progress updated to Ready!")
                time.sleep(0.3)  # Shorter pause for delayed completion
                print("[Loading Manager] Sleeping for 0.3 seconds...")
                self.loading_screen.hide()
                print("[Loading Manager] Loading screen hidden")
                self.loading_complete = True
                print(f"[Loading Manager] Loading complete set to True, now: {self.loading_complete}")
            except Exception as e:
                print(f"[Loading Manager] Error finishing loading: {e}")
                print(f"[Loading Manager] Exception type: {type(e)}")
                self.loading_complete = True
                print(f"[Loading Manager] Loading complete set to True after error, now: {self.loading_complete}")
        else:
            print("[Loading Manager] Loading already complete, ignoring finish call")
    
    def is_loading(self) -> bool:
        """Check if loading is in progress"""
        return not self.loading_complete
