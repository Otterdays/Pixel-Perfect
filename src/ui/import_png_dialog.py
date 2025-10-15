"""
Import PNG Dialog for Pixel Perfect
Shows preview with rotation animation and scale options
"""

import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from typing import Optional, Callable


class ImportPNGDialog:
    """Dialog for importing PNG with preview and scale options"""
    
    def __init__(self, parent, on_import: Callable, theme=None):
        """
        Initialize the import PNG dialog
        
        Args:
            parent: Parent window
            on_import: Callback function(file_path, scale_factor)
            theme: Theme manager for styling
        """
        self.parent = parent
        self.on_import = on_import
        self.theme = theme
        
        # Dialog state
        self.dialog = None
        self.selected_file = None
        self.preview_image = None
        self.preview_label = None
        self.rotation_angle = 0
        self.rotation_job = None
        self.scale_factor = 1
        
        # UI elements
        self.file_label = None
        self.dimension_label = None
        self.scale_buttons = []
    
    def show(self):
        """Show the import PNG dialog"""
        try:
            # Create dialog window
            self.dialog = ctk.CTkToplevel(self.parent)
            self.dialog.title("Import PNG")
            self.dialog.geometry("600x900")
            self.dialog.resizable(False, False)
            
            # Don't set transient to avoid focus issues
            # self.dialog.transient(self.parent)
            
            # Center dialog BEFORE showing with bounds checking
            self.dialog.withdraw()  # Hide temporarily
            self.dialog.update_idletasks()
            
            # Get parent window position and size
            parent_x = self.parent.winfo_x()
            parent_y = self.parent.winfo_y()
            parent_width = self.parent.winfo_width()
            parent_height = self.parent.winfo_height()
            
            # Dialog dimensions
            dialog_width = 600
            dialog_height = 900
            
            # Calculate center position
            center_x = parent_x + (parent_width // 2) - (dialog_width // 2)
            center_y = parent_y + (parent_height // 2) - (dialog_height // 2)
            
            # Get screen dimensions for bounds checking
            screen_width = self.parent.winfo_screenwidth()
            screen_height = self.parent.winfo_screenheight()
            
            # Clamp position to screen bounds
            x = max(0, min(center_x, screen_width - dialog_width))
            y = max(0, min(center_y, screen_height - dialog_height))
            
            self.dialog.geometry(f"+{x}+{y}")
            self.dialog.deiconify()  # Show after positioning
        except Exception as e:
            print(f"[ERROR] Dialog creation failed: {e}")
            return
        
        # Title
        title_label = ctk.CTkLabel(
            self.dialog,
            text="Import PNG Image",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # File selection section
        file_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        file_frame.pack(pady=10, padx=20, fill="x")
        
        select_btn = ctk.CTkButton(
            file_frame,
            text="Select PNG File",
            command=self._select_file,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        select_btn.pack()
        
        self.file_label = ctk.CTkLabel(
            file_frame,
            text="No file selected",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.file_label.pack(pady=(5, 0))
        
        # Preview section
        preview_frame = ctk.CTkFrame(self.dialog)
        preview_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        preview_title = ctk.CTkLabel(
            preview_frame,
            text="Preview (Slow Spin)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        preview_title.pack(pady=(10, 5))
        
        # Preview canvas (for spinning image) - NO fixed size to prevent clipping
        self.preview_label = ctk.CTkLabel(
            preview_frame,
            text="Select a PNG file to preview",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.preview_label.pack(pady=10, padx=10)
        
        self.dimension_label = ctk.CTkLabel(
            preview_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.dimension_label.pack(pady=(0, 10))
        
        # Scale options section
        scale_frame = ctk.CTkFrame(self.dialog)
        scale_frame.pack(pady=10, padx=20, fill="x")
        
        scale_title = ctk.CTkLabel(
            scale_frame,
            text="Import Scale",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        scale_title.pack(pady=(10, 5))
        
        scale_info = ctk.CTkLabel(
            scale_frame,
            text="Choose how much to scale the image when importing",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        scale_info.pack(pady=(0, 10))
        
        # Scale buttons (1x, 2x, 3x, 4x)
        scale_btn_frame = ctk.CTkFrame(scale_frame, fg_color="transparent")
        scale_btn_frame.pack(pady=(0, 10))
        
        for scale in [1, 2, 3, 4]:
            btn = ctk.CTkButton(
                scale_btn_frame,
                text=f"{scale}x",
                command=lambda s=scale: self._set_scale(s),
                width=80,
                height=50,
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color="#1f6aa5" if scale == 1 else "#4a4a4a",
                hover_color="#1f5a95" if scale == 1 else "#5a5a5a"
            )
            btn.pack(side="left", padx=5)
            self.scale_buttons.append(btn)
        
        # Result dimensions label
        self.result_label = ctk.CTkLabel(
            scale_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#1f6aa5"
        )
        self.result_label.pack(pady=(5, 10))
        
        # Action buttons
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(pady=(10, 20), padx=20, fill="x")
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self._cancel,
            width=140,
            height=40,
            fg_color="#4a4a4a",
            hover_color="#5a5a5a",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        cancel_btn.pack(side="right", padx=5)
        
        self.import_btn = ctk.CTkButton(
            button_frame,
            text="Import",
            command=self._do_import,
            width=140,
            height=40,
            fg_color="green",
            hover_color="#00cc00",
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled"
        )
        self.import_btn.pack(side="right", padx=5)
        
        # Bind dialog close
        self.dialog.protocol("WM_DELETE_WINDOW", self._cancel)
    
    def _select_file(self):
        """Open file dialog to select PNG"""
        try:
            filepath = filedialog.askopenfilename(
                title="Select PNG Image",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            
            if filepath:
                self.selected_file = filepath
                self._load_preview(filepath)
                self.import_btn.configure(state="normal")
        except Exception as e:
            print(f"[ERROR] File selection failed: {e}")
            self.file_label.configure(text=f"Error: {e}", text_color="red")
    
    def _load_preview(self, filepath: str):
        """Load and display preview with spinning animation"""
        try:
            # Load image
            image = Image.open(filepath)
            self.preview_image = image
            
            # Update file label
            filename = filepath.split("/")[-1].split("\\")[-1]
            self.file_label.configure(text=filename, text_color="white")
            
            # Update dimension label
            w, h = image.size
            self.dimension_label.configure(
                text=f"Original: {w}x{h} pixels",
                text_color="white"
            )
            
            # Update result label
            self._update_result_label(w, h)
            
            # Start rotation animation
            self._start_rotation()
            
        except Exception as e:
            self.file_label.configure(text=f"Error: {e}", text_color="red")
    
    def _start_rotation(self):
        """Start the slow spinning preview animation"""
        if self.preview_image:
            self._rotate_preview()
    
    def _rotate_preview(self):
        """Rotate preview image continuously"""
        try:
            # Check if dialog and all components still exist
            if (not self.preview_image or 
                not self.dialog or 
                not self.dialog.winfo_exists() or
                not self.preview_label or
                not self.preview_label.winfo_exists()):
                self.rotation_job = None
                return
            
            # Increment rotation angle (slow spin - 1 degree per frame)
            self.rotation_angle = (self.rotation_angle + 1) % 360
            
            # Rotate image with expand=True to prevent clipping
            rotated = self.preview_image.rotate(self.rotation_angle, expand=True)
            
            # Resize to fit preview area (max 280x280)
            display_size = self._get_display_size(rotated.size)
            display_image = rotated.resize(display_size, Image.NEAREST)
            
            # Convert to CTkImage for proper HighDPI scaling
            from customtkinter import CTkImage
            ctk_image = CTkImage(
                light_image=display_image,
                dark_image=display_image,
                size=display_size
            )
            
            # Update preview label
            self.preview_label.configure(image=ctk_image, text="")
            self.preview_label.image = ctk_image  # Keep reference
            
            # Schedule next frame (60fps = ~16ms, but we want slower rotation)
            self.rotation_job = self.dialog.after(50, self._rotate_preview)
        except Exception as e:
            # Dialog was destroyed or error occurred, stop animation
            print(f"[DEBUG] Rotation stopped: {e}")
            self.rotation_job = None
    
    def _get_display_size(self, original_size):
        """Calculate display size to fit preview area"""
        max_size = 280
        w, h = original_size
        
        if w > max_size or h > max_size:
            scale = min(max_size / w, max_size / h)
            return (int(w * scale), int(h * scale))
        else:
            # Scale up small images for better visibility
            scale = min(max_size / w, max_size / h)
            scale = min(scale, 8)  # Cap at 8x
            return (int(w * scale), int(h * scale))
    
    def _set_scale(self, scale: int):
        """Set the import scale factor"""
        self.scale_factor = scale
        
        # Update button colors
        for i, btn in enumerate(self.scale_buttons):
            if i + 1 == scale:
                btn.configure(fg_color="#1f6aa5", hover_color="#1f5a95")
            else:
                btn.configure(fg_color="#4a4a4a", hover_color="#5a5a5a")
        
        # Update result label
        if self.preview_image:
            w, h = self.preview_image.size
            self._update_result_label(w, h)
    
    def _update_result_label(self, orig_w: int, orig_h: int):
        """Update the result dimensions label"""
        result_w = orig_w * self.scale_factor
        result_h = orig_h * self.scale_factor
        
        if self.scale_factor == 1:
            self.result_label.configure(
                text=f"Import as: {result_w}x{result_h} (no scaling)"
            )
        else:
            self.result_label.configure(
                text=f"Import as: {result_w}x{result_h} ({self.scale_factor}x scaled from {orig_w}x{orig_h})"
            )
    
    def _do_import(self):
        """Execute the import"""
        if self.selected_file and self.on_import:
            # Stop rotation animation
            if self.rotation_job:
                try:
                    self.dialog.after_cancel(self.rotation_job)
                except:
                    pass
                self.rotation_job = None
            
            # Call import callback
            self.on_import(self.selected_file, self.scale_factor)
            
            # Close dialog
            try:
                self.dialog.destroy()
            except:
                pass
    
    def _cancel(self):
        """Cancel and close dialog"""
        # Stop rotation animation
        if self.rotation_job:
            try:
                self.dialog.after_cancel(self.rotation_job)
            except:
                pass
            self.rotation_job = None
        
        # Close dialog
        if self.dialog:
            try:
                self.dialog.destroy()
            except:
                pass

