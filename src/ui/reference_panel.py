"""
Reference Image Panel for Pixel Perfect
Allows artists to load, view, and adjust reference images alongside their canvas.

Features:
- Load any image (PNG, JPG, BMP, GIF, WEBP)
- Adjustable opacity (10% - 100%)
- Fit / Fill display modes
- Drag to pan, scroll to zoom
- Toggle visibility with keyboard shortcut (R)
- Collapsible panel in right sidebar

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os


class ReferencePanel:
    """Reference image panel for displaying artist reference images"""
    
    def __init__(self, parent, app):
        """Initialize the reference panel.
        
        Args:
            parent: Parent widget (right panel)
            app: Main application (MainWindow) instance
        """
        self.parent = parent
        self.app = app
        self.ref_image = None           # Original PIL Image
        self.display_image = None       # Scaled/processed PIL Image  
        self.photo_image = None         # PhotoImage for tkinter display
        self.opacity = 1.0              # Current opacity (0.1 - 1.0)
        self.fit_mode = "fit"           # "fit" or "fill"
        self.is_visible = True          # Panel visibility state
        self.is_collapsed = True        # Section collapsed state (starts collapsed)
        self.image_path = None          # Path to loaded image
        
        # Pan/zoom state
        self.pan_x = 0
        self.pan_y = 0
        self.zoom_level = 1.0
        self._drag_start_x = 0
        self._drag_start_y = 0
        self._is_dragging = False
        
        self._build_ui()
    
    def _build_ui(self):
        """Build the reference panel UI"""
        theme = self.app.theme_manager.get_current_theme()
        
        # Main container frame
        self.frame = ctk.CTkFrame(
            self.parent,
            fg_color=theme.bg_secondary,
            corner_radius=8
        )
        self.frame.pack(fill="x", padx=5, pady=(5, 2))
        
        # Header with collapse toggle
        header_frame = ctk.CTkFrame(self.frame, fg_color="transparent", height=32)
        header_frame.pack(fill="x", padx=5, pady=(5, 0))
        header_frame.pack_propagate(False)
        
        # Collapse arrow + title
        self.collapse_btn = ctk.CTkButton(
            header_frame,
            text="▶ 🖼️ Reference Image",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="transparent",
            hover_color=theme.button_hover,
            text_color=theme.text_primary,
            anchor="w",
            height=28,
            command=self._toggle_collapse
        )
        self.collapse_btn.pack(side="left", fill="x", expand=True)
        
        # Collapsible content
        self.content_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        # Start collapsed - don't pack content_frame
        
        # --- Load / Clear buttons ---
        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=5, pady=(5, 2))
        
        self.load_btn = ctk.CTkButton(
            btn_frame,
            text="📂 Load",
            width=80,
            height=28,
            font=ctk.CTkFont(size=12),
            fg_color=theme.button_normal,
            hover_color=theme.button_hover,
            text_color=theme.text_primary,
            command=self._load_image
        )
        self.load_btn.pack(side="left", padx=2)
        
        self.clear_btn = ctk.CTkButton(
            btn_frame,
            text="✕ Clear",
            width=70,
            height=28,
            font=ctk.CTkFont(size=12),
            fg_color=theme.button_normal,
            hover_color="#cc4444",
            text_color=theme.text_primary,
            command=self._clear_image
        )
        self.clear_btn.pack(side="left", padx=2)
        
        # Fit/Fill toggle
        self.fit_btn = ctk.CTkButton(
            btn_frame,
            text="Fit",
            width=50,
            height=28,
            font=ctk.CTkFont(size=11),
            fg_color=theme.tool_selected,
            hover_color=theme.button_hover,
            text_color=theme.text_primary,
            command=self._toggle_fit_mode
        )
        self.fit_btn.pack(side="right", padx=2)
        
        # --- Opacity slider ---
        opacity_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        opacity_frame.pack(fill="x", padx=5, pady=(2, 2))
        
        opacity_label = ctk.CTkLabel(
            opacity_frame,
            text="Opacity:",
            font=ctk.CTkFont(size=11),
            text_color=theme.text_secondary
        )
        opacity_label.pack(side="left", padx=(0, 5))
        
        self.opacity_slider = ctk.CTkSlider(
            opacity_frame,
            from_=10,
            to=100,
            number_of_steps=18,
            width=100,
            height=16,
            command=self._on_opacity_change
        )
        self.opacity_slider.set(100)
        self.opacity_slider.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.opacity_label = ctk.CTkLabel(
            opacity_frame,
            text="100%",
            font=ctk.CTkFont(size=11),
            text_color=theme.text_secondary,
            width=40
        )
        self.opacity_label.pack(side="right")
        
        # --- Image display canvas ---
        self.canvas_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="#1a1a1a",
            corner_radius=6,
            height=200
        )
        self.canvas_frame.pack(fill="x", padx=5, pady=(2, 5))
        self.canvas_frame.pack_propagate(False)
        
        self.display_canvas = tk.Canvas(
            self.canvas_frame,
            bg="#1a1a1a",
            highlightthickness=0,
            cursor="hand2"
        )
        self.display_canvas.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Placeholder text
        self.display_canvas.create_text(
            100, 100,
            text="Drop or load\na reference image",
            fill="#555555",
            font=("Segoe UI", 11),
            justify="center",
            tags="placeholder"
        )
        
        # --- File info label ---
        self.info_label = ctk.CTkLabel(
            self.content_frame,
            text="No image loaded",
            font=ctk.CTkFont(size=10),
            text_color=theme.text_secondary,
            anchor="w"
        )
        self.info_label.pack(fill="x", padx=8, pady=(0, 5))
        
        # Bind mouse events for pan/zoom
        self.display_canvas.bind("<Button-1>", self._on_drag_start)
        self.display_canvas.bind("<B1-Motion>", self._on_drag)
        self.display_canvas.bind("<ButtonRelease-1>", self._on_drag_end)
        self.display_canvas.bind("<MouseWheel>", self._on_scroll_zoom)
        self.display_canvas.bind("<Double-Button-1>", self._reset_view)
        
        # Bind resize
        self.display_canvas.bind("<Configure>", self._on_canvas_resize)
    
    def _toggle_collapse(self):
        """Toggle the collapsed state of the panel content"""
        if self.is_collapsed:
            self.content_frame.pack(fill="x")
            self.collapse_btn.configure(text="▼ 🖼️ Reference Image")
            self.is_collapsed = False
            # Refresh display after expanding
            if self.ref_image:
                self.display_canvas.after(50, self._refresh_display)
        else:
            self.content_frame.pack_forget()
            self.collapse_btn.configure(text="▶ 🖼️ Reference Image")
            self.is_collapsed = True
    
    def _load_image(self):
        """Open file dialog to load a reference image"""
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.webp *.tiff"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("All files", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(
            title="Load Reference Image",
            filetypes=filetypes,
            parent=self.app.root
        )
        
        if filepath and os.path.exists(filepath):
            try:
                self.ref_image = Image.open(filepath).convert("RGBA")
                self.image_path = filepath
                
                # Reset pan/zoom
                self.pan_x = 0
                self.pan_y = 0
                self.zoom_level = 1.0
                
                # Update info
                filename = os.path.basename(filepath)
                w, h = self.ref_image.size
                self.info_label.configure(text=f"📎 {filename} ({w}×{h})")
                
                # Auto-expand if collapsed
                if self.is_collapsed:
                    self._toggle_collapse()
                
                self._refresh_display()
            except Exception as e:
                self.info_label.configure(text=f"❌ Error: {str(e)[:40]}")
    
    def _clear_image(self):
        """Clear the current reference image"""
        self.ref_image = None
        self.display_image = None
        self.photo_image = None
        self.image_path = None
        self.pan_x = 0
        self.pan_y = 0
        self.zoom_level = 1.0
        
        self.display_canvas.delete("all")
        self.display_canvas.create_text(
            self.display_canvas.winfo_width() // 2 or 100,
            self.display_canvas.winfo_height() // 2 or 100,
            text="Drop or load\na reference image",
            fill="#555555",
            font=("Segoe UI", 11),
            justify="center",
            tags="placeholder"
        )
        self.info_label.configure(text="No image loaded")
    
    def _toggle_fit_mode(self):
        """Toggle between fit and fill display modes"""
        theme = self.app.theme_manager.get_current_theme()
        
        if self.fit_mode == "fit":
            self.fit_mode = "fill"
            self.fit_btn.configure(text="Fill", fg_color=theme.tool_selected)
        else:
            self.fit_mode = "fit"
            self.fit_btn.configure(text="Fit", fg_color=theme.tool_selected)
        
        # Reset pan when switching modes
        self.pan_x = 0
        self.pan_y = 0
        self.zoom_level = 1.0
        
        self._refresh_display()
    
    def _on_opacity_change(self, value):
        """Handle opacity slider change"""
        self.opacity = value / 100.0
        self.opacity_label.configure(text=f"{int(value)}%")
        self._refresh_display()
    
    def _on_drag_start(self, event):
        """Start panning"""
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        self._is_dragging = True
    
    def _on_drag(self, event):
        """Pan the image"""
        if self._is_dragging and self.ref_image:
            dx = event.x - self._drag_start_x
            dy = event.y - self._drag_start_y
            self.pan_x += dx
            self.pan_y += dy
            self._drag_start_x = event.x
            self._drag_start_y = event.y
            self._refresh_display()
    
    def _on_drag_end(self, event):
        """Stop panning"""
        self._is_dragging = False
    
    def _on_scroll_zoom(self, event):
        """Zoom in/out with scroll wheel"""
        if not self.ref_image:
            return
        
        if event.delta > 0:
            self.zoom_level = min(5.0, self.zoom_level * 1.15)
        else:
            self.zoom_level = max(0.1, self.zoom_level / 1.15)
        
        self._refresh_display()
    
    def _reset_view(self, event=None):
        """Reset pan and zoom to default (double-click)"""
        self.pan_x = 0
        self.pan_y = 0
        self.zoom_level = 1.0
        self._refresh_display()
    
    def _on_canvas_resize(self, event=None):
        """Handle canvas resize"""
        if self.ref_image:
            self._refresh_display()
    
    def _refresh_display(self):
        """Refresh the reference image display"""
        if not self.ref_image:
            return
        
        canvas_w = self.display_canvas.winfo_width()
        canvas_h = self.display_canvas.winfo_height()
        
        if canvas_w <= 1 or canvas_h <= 1:
            return
        
        img_w, img_h = self.ref_image.size
        
        # Calculate base scale based on fit mode
        if self.fit_mode == "fit":
            scale = min(canvas_w / img_w, canvas_h / img_h)
        else:  # fill
            scale = max(canvas_w / img_w, canvas_h / img_h)
        
        # Apply zoom
        scale *= self.zoom_level
        
        # Calculate display size
        disp_w = max(1, int(img_w * scale))
        disp_h = max(1, int(img_h * scale))
        
        # Resize image
        resample = Image.Resampling.LANCZOS if scale < 1 else Image.Resampling.NEAREST
        display_img = self.ref_image.resize((disp_w, disp_h), resample)
        
        # Apply opacity
        if self.opacity < 1.0:
            # Reduce alpha channel
            r, g, b, a = display_img.split()
            a = a.point(lambda x: int(x * self.opacity))
            display_img = Image.merge("RGBA", (r, g, b, a))
        
        # Create a composited image on dark background
        bg = Image.new("RGBA", (canvas_w, canvas_h), (26, 26, 26, 255))
        
        # Calculate position (centered + pan offset)
        paste_x = (canvas_w - disp_w) // 2 + int(self.pan_x)
        paste_y = (canvas_h - disp_h) // 2 + int(self.pan_y)
        
        bg.paste(display_img, (paste_x, paste_y), display_img)
        
        # Convert to PhotoImage and display
        self.photo_image = ImageTk.PhotoImage(bg.convert("RGB"))
        
        self.display_canvas.delete("all")
        self.display_canvas.create_image(
            0, 0,
            image=self.photo_image,
            anchor="nw",
            tags="ref_image"
        )
    
    def toggle_visibility(self):
        """Toggle panel visibility (called by keyboard shortcut)"""
        if self.is_visible:
            self.frame.pack_forget()
            self.is_visible = False
        else:
            self.frame.pack(fill="x", padx=5, pady=(5, 2))
            self.is_visible = True
            if self.ref_image and not self.is_collapsed:
                self.display_canvas.after(50, self._refresh_display)
    
    def update_theme(self, theme):
        """Update panel colors when theme changes"""
        self.frame.configure(fg_color=theme.bg_secondary)
        self.collapse_btn.configure(
            hover_color=theme.button_hover,
            text_color=theme.text_primary
        )
        self.load_btn.configure(
            fg_color=theme.button_normal,
            hover_color=theme.button_hover,
            text_color=theme.text_primary
        )
        self.clear_btn.configure(
            fg_color=theme.button_normal,
            text_color=theme.text_primary
        )
        self.fit_btn.configure(
            fg_color=theme.tool_selected,
            hover_color=theme.button_hover,
            text_color=theme.text_primary
        )
        self.info_label.configure(text_color=theme.text_secondary)
