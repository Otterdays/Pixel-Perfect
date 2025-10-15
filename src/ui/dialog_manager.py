"""
Dialog Manager for Pixel Perfect
Handles all custom dialog windows (custom size, downsize warning, texture panel)

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import customtkinter as ctk
import tkinter as tk
import numpy as np


class DialogManager:
    """Manages custom dialogs for the application"""
    
    def __init__(self, root, canvas, texture_library, tools):
        """
        Initialize the DialogManager.
        
        Args:
            root: The main Tkinter root window
            canvas: The canvas object
            texture_library: The texture library object
            tools: Dictionary of tool objects
        """
        self.root = root
        self.canvas = canvas
        self.texture_library = texture_library
        self.tools = tools
        
        # Callback for tool selection (set by main_window after init)
        self.select_tool_callback = None
    
    def open_custom_size_dialog(self):
        """Open dialog for custom canvas size input"""
        # Create custom size dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Custom Canvas Size")
        dialog.geometry("400x280")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center on main window
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (400 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (280 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Header with icon
        header_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        header_frame.pack(pady=20, padx=20, fill="x")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📐 Custom Canvas Size",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack()
        
        # Input frame
        input_frame = ctk.CTkFrame(dialog)
        input_frame.pack(padx=20, pady=10, fill="x")
        
        # Width input
        width_label = ctk.CTkLabel(input_frame, text="Width (pixels):", font=ctk.CTkFont(size=14))
        width_label.pack(pady=(10, 5))
        
        width_entry = ctk.CTkEntry(
            input_frame,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16),
            placeholder_text="e.g., 48"
        )
        width_entry.pack(pady=5)
        width_entry.insert(0, str(self.canvas.width))
        
        # Height input
        height_label = ctk.CTkLabel(input_frame, text="Height (pixels):", font=ctk.CTkFont(size=14))
        height_label.pack(pady=(10, 5))
        
        height_entry = ctk.CTkEntry(
            input_frame,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16),
            placeholder_text="e.g., 48"
        )
        height_entry.pack(pady=5)
        height_entry.insert(0, str(self.canvas.height))
        
        # Result storage
        result = [None, None]
        
        def on_apply():
            try:
                width = int(width_entry.get())
                height = int(height_entry.get())
                
                # Validate dimensions
                if width < 1 or height < 1:
                    from tkinter import messagebox
                    messagebox.showerror("Invalid Size", "Width and height must be at least 1 pixel!")
                    return
                
                if width > 512 or height > 512:
                    from tkinter import messagebox
                    messagebox.showerror("Invalid Size", "Maximum size is 512x512 pixels!")
                    return
                
                result[0] = width
                result[1] = height
                dialog.destroy()
            except ValueError:
                from tkinter import messagebox
                messagebox.showerror("Invalid Input", "Please enter valid numbers!")
        
        def on_cancel():
            dialog.destroy()
        
        # Button frame
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20, padx=20, fill="x")
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=120,
            height=35,
            fg_color="#4a4a4a",
            hover_color="#5a5a5a",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=on_cancel
        )
        cancel_btn.pack(side="right", padx=5)
        
        apply_btn = ctk.CTkButton(
            button_frame,
            text="Apply",
            width=120,
            height=35,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=on_apply
        )
        apply_btn.pack(side="right", padx=5)
        
        # Bind Enter key to apply
        width_entry.bind("<Return>", lambda e: height_entry.focus())
        height_entry.bind("<Return>", lambda e: on_apply())
        
        # Focus width entry and select all (delayed to ensure dialog is rendered)
        def focus_and_select():
            width_entry.focus_force()
            width_entry.select_range(0, 'end')
            width_entry.icursor('end')  # Move cursor to end after selection
        
        dialog.after(100, focus_and_select)
        
        # Wait for dialog
        self.root.wait_window(dialog)
        
        return result[0], result[1]
    
    def show_downsize_warning(self, old_width, old_height, new_width, new_height):
        """Show custom styled downsize warning dialog"""
        # Create custom warning dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Canvas Downsize Warning")
        dialog.geometry("500x280")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog on the main window
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (500 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (280 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Icon and title frame
        header_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        header_frame.pack(pady=20, padx=20, fill="x")
        
        # Large warning icon (⚠️ emoji)
        icon_label = ctk.CTkLabel(
            header_frame,
            text="⚠️",
            font=ctk.CTkFont(size=48)
        )
        icon_label.pack(side="left", padx=(10, 20))
        
        # Title text
        title_label = ctk.CTkLabel(
            header_frame,
            text="DOWNSIZING WARNING",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ff9800"  # Orange warning color
        )
        title_label.pack(side="left", anchor="w")
        
        # Warning details
        details_text = f"Current size: {old_width}x{old_height}\n"
        details_text += f"New size: {new_width}x{new_height}\n\n"
        details_text += f"This will PERMANENTLY DELETE pixels outside the {new_width}x{new_height} region!\n"
        details_text += "Lost pixels CANNOT be recovered!"
        
        message_label = ctk.CTkLabel(
            dialog,
            text=details_text,
            font=ctk.CTkFont(size=14),
            text_color="#e0e0e0",
            justify="left"
        )
        message_label.pack(pady=(0, 10), padx=20)
        
        # Continue question
        question_label = ctk.CTkLabel(
            dialog,
            text="Continue with resize?",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff"
        )
        question_label.pack(pady=(0, 20), padx=20)
        
        # Button frame
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        # Result storage
        result = [False]
        
        def on_yes():
            result[0] = True
            dialog.destroy()
        
        def on_no():
            result[0] = False
            dialog.destroy()
        
        # No button (safe option)
        no_btn = ctk.CTkButton(
            button_frame,
            text="No",
            width=140,
            height=40,
            fg_color="#4a4a4a",
            hover_color="#5a5a5a",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=on_no
        )
        no_btn.pack(side="right", padx=5)
        
        # Yes button (destructive action)
        yes_btn = ctk.CTkButton(
            button_frame,
            text="Yes",
            width=140,
            height=40,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=on_yes
        )
        yes_btn.pack(side="right", padx=5)
        
        # Wait for dialog to close
        self.root.wait_window(dialog)
        
        # Return result
        return result[0]
    
    def open_texture_panel(self):
        """Open texture panel with clickable textures"""
        # Create texture panel window
        texture_window = ctk.CTkToplevel(self.root)
        texture_window.title("Texture Library")
        texture_window.geometry("400x300")
        texture_window.resizable(False, False)
        texture_window.transient(self.root)
        texture_window.grab_set()  # Modal
        
        # Center on main window
        texture_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (400 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (300 // 2)
        texture_window.geometry(f"+{x}+{y}")
        
        # Header
        header_frame = ctk.CTkFrame(texture_window, fg_color="transparent")
        header_frame.pack(pady=15, padx=20, fill="x")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎨 Texture Library",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Select a texture to apply to canvas",
            font=ctk.CTkFont(size=12),
            text_color="#a0a0a0"
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Textures grid
        content_frame = ctk.CTkFrame(texture_window)
        content_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        
        # Get all textures
        textures = self.texture_library.get_all_textures()
        
        # Create texture buttons
        for idx, (name, texture_data) in enumerate(textures.items()):
            self._create_texture_button(content_frame, name, texture_data, texture_window, idx)
    
    def _create_texture_button(self, parent, name, texture_data, window, index):
        """Create a clickable texture preview button"""
        # Container for texture button
        texture_frame = ctk.CTkFrame(parent, fg_color="#2a2a2a", corner_radius=8)
        texture_frame.pack(pady=10, padx=10, fill="x")
        
        # Create canvas to render texture preview
        preview_size = 64  # 8x8 texture * 8 scale = 64px
        preview_canvas = tk.Canvas(
            texture_frame,
            width=preview_size,
            height=preview_size,
            bg="#1a1a1a",
            highlightthickness=0
        )
        preview_canvas.pack(side="left", padx=10, pady=10)
        
        # Render texture on canvas (scaled up)
        scale = 8
        for y in range(texture_data.shape[0]):
            for x in range(texture_data.shape[1]):
                color = texture_data[y, x]
                hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                preview_canvas.create_rectangle(
                    x * scale, y * scale,
                    (x + 1) * scale, (y + 1) * scale,
                    fill=hex_color,
                    outline=""
                )
        
        # Texture info
        info_frame = ctk.CTkFrame(texture_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=name,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        dims = f"{texture_data.shape[1]}×{texture_data.shape[0]} pixels"
        dims_label = ctk.CTkLabel(
            info_frame,
            text=dims,
            font=ctk.CTkFont(size=11),
            text_color="#a0a0a0",
            anchor="w"
        )
        dims_label.pack(anchor="w", pady=(2, 0))
        
        # Select button
        select_btn = ctk.CTkButton(
            info_frame,
            text="Select",
            width=80,
            height=28,
            fg_color="#4a9eff",
            hover_color="#3a8eef",
            command=lambda: self._select_texture(texture_data, window)
        )
        select_btn.pack(anchor="w", pady=(8, 0))
        
        # Make entire frame clickable
        texture_frame.bind("<Button-1>", lambda e: self._select_texture(texture_data, window))
        preview_canvas.bind("<Button-1>", lambda e: self._select_texture(texture_data, window))
    
    def _select_texture(self, texture_data, window):
        """Select a texture and activate texture tool"""
        # Set texture on tool
        self.tools["texture"].set_texture(texture_data)
        
        # Switch to texture tool via callback
        if self.select_tool_callback:
            self.select_tool_callback("texture")
        
        # Close texture panel
        window.destroy()
        
        print(f"[TEXTURE] Selected {texture_data.shape[1]}x{texture_data.shape[0]} texture")

