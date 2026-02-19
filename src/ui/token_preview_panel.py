"""
Token Preview Panel for Pixel Perfect
Interactive 3D coin/medallion preview of the current pixel art.

Features:
- Real-time 3D coin visualization (software rasterized)
- Mouse drag to rotate, scroll to zoom
- Thickness, light, and material controls
- Back face modes (mirrored, embossed, same, blank)
- Auto-rotate toggle
- Export as PNG / GIF
- Collapsible panel in right sidebar

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import threading


class TokenPreviewPanel:
    """3D Token/Coin preview panel using software voxel rasterization."""

    def __init__(self, parent, app):
        """Initialize the token preview panel.

        Args:
            parent: Parent widget (right sidebar)
            app: Main application (MainWindow) instance
        """
        self.parent = parent
        self.app = app
        self.is_visible = True
        self.is_collapsed = True  # Start collapsed

        # Import renderer lazily to avoid circular deps
        from src.core.voxel_renderer import VoxelRenderer
        self.renderer = VoxelRenderer()

        # Display state
        self._photo = None          # PhotoImage reference (prevent GC)
        self._render_size = 200     # Preview render resolution
        self._auto_rotate = False
        self._auto_rotate_job = None

        # Drag state
        self._drag_x = 0
        self._drag_y = 0
        self._dragging = False

        # Debounce: avoid rendering on every single pixel change
        self._render_pending = False
        self._render_job = None

        self._build_ui()

    # ------------------------------------------------------------------ #
    #  UI Construction
    # ------------------------------------------------------------------ #
    def _build_ui(self):
        """Build the panel widgets."""
        theme = self.app.theme_manager.get_current_theme()

        # Main container
        self.frame = ctk.CTkFrame(
            self.parent,
            fg_color=theme.bg_secondary,
            corner_radius=8,
        )
        self.frame.pack(fill="x", padx=5, pady=(5, 2))

        # Header (collapse toggle)
        hdr = ctk.CTkFrame(self.frame, fg_color="transparent", height=32)
        hdr.pack(fill="x", padx=5, pady=(5, 0))
        hdr.pack_propagate(False)

        self.collapse_btn = ctk.CTkButton(
            hdr,
            text="▶ 🪙 3D Token Preview",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="transparent",
            hover_color=theme.button_hover,
            text_color=theme.text_primary,
            anchor="w",
            height=28,
            command=self._toggle_collapse,
        )
        self.collapse_btn.pack(side="left", fill="x", expand=True)

        # Collapsible content (starts hidden)
        self.content = ctk.CTkFrame(self.frame, fg_color="transparent")

        # --- 3D render canvas ---
        self.render_frame = ctk.CTkFrame(
            self.content, fg_color="#111111", corner_radius=6, height=200
        )
        self.render_frame.pack(fill="x", padx=5, pady=(5, 2))
        self.render_frame.pack_propagate(False)

        self.render_canvas = tk.Canvas(
            self.render_frame, bg="#111111", highlightthickness=0, cursor="hand2"
        )
        self.render_canvas.pack(fill="both", expand=True, padx=2, pady=2)

        # Placeholder
        self.render_canvas.create_text(
            100, 100,
            text="Toggle open to preview\nyour pixel art as a 3D token",
            fill="#444444",
            font=("Segoe UI", 10),
            justify="center",
            tags="placeholder",
        )

        # Bind mouse for rotation
        self.render_canvas.bind("<Button-1>", self._on_drag_start)
        self.render_canvas.bind("<B1-Motion>", self._on_drag)
        self.render_canvas.bind("<ButtonRelease-1>", self._on_drag_end)
        self.render_canvas.bind("<MouseWheel>", self._on_scroll_zoom)
        self.render_canvas.bind("<Double-Button-1>", self._reset_rotation)

        # --- Controls ---
        ctrl = ctk.CTkFrame(self.content, fg_color="transparent")
        ctrl.pack(fill="x", padx=5, pady=(2, 2))

        # Thickness slider
        self._add_slider(ctrl, "Thickness:", 1, 8, 3, self._on_thickness, "thickness_lbl")

        # Light angle slider
        self._add_slider(ctrl, "Light:", 0, 360, 135, self._on_light, "light_lbl")

        # Material dropdown
        mat_row = ctk.CTkFrame(ctrl, fg_color="transparent")
        mat_row.pack(fill="x", pady=1)
        ctk.CTkLabel(
            mat_row, text="Material:", font=ctk.CTkFont(size=11),
            text_color=theme.text_secondary, width=65, anchor="w"
        ).pack(side="left")

        self.material_var = ctk.StringVar(value="Flat")
        self.material_menu = ctk.CTkOptionMenu(
            mat_row, variable=self.material_var,
            values=["Flat", "Gold", "Silver", "Bronze"],
            width=90, height=24, font=ctk.CTkFont(size=11),
            fg_color=theme.button_normal,
            button_color=theme.button_hover,
            command=self._on_material,
        )
        self.material_menu.pack(side="left", padx=(0, 5))

        # Back face dropdown
        self.backface_var = ctk.StringVar(value="Mirrored")
        self.backface_menu = ctk.CTkOptionMenu(
            mat_row, variable=self.backface_var,
            values=["Same", "Mirrored", "Embossed", "Blank"],
            width=90, height=24, font=ctk.CTkFont(size=11),
            fg_color=theme.button_normal,
            button_color=theme.button_hover,
            command=self._on_backface,
        )
        self.backface_menu.pack(side="left")

        # Bottom buttons row
        btn_row = ctk.CTkFrame(ctrl, fg_color="transparent")
        btn_row.pack(fill="x", pady=(4, 2))

        self.auto_btn = ctk.CTkButton(
            btn_row, text="🔄 Spin", width=60, height=26,
            font=ctk.CTkFont(size=11),
            fg_color=theme.button_normal,
            hover_color=theme.button_hover,
            text_color=theme.text_primary,
            command=self._toggle_auto_rotate,
        )
        self.auto_btn.pack(side="left", padx=2)

        ctk.CTkButton(
            btn_row, text="📤 PNG", width=55, height=26,
            font=ctk.CTkFont(size=11),
            fg_color=theme.button_normal,
            hover_color=theme.button_hover,
            text_color=theme.text_primary,
            command=self._export_png,
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            btn_row, text="🎞️ GIF", width=55, height=26,
            font=ctk.CTkFont(size=11),
            fg_color=theme.button_normal,
            hover_color=theme.button_hover,
            text_color=theme.text_primary,
            command=self._export_gif,
        ).pack(side="left", padx=2)

    def _add_slider(self, parent, label, lo, hi, default, callback, lbl_attr):
        """Helper to add a labeled slider row."""
        theme = self.app.theme_manager.get_current_theme()
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=1)

        ctk.CTkLabel(
            row, text=label, font=ctk.CTkFont(size=11),
            text_color=theme.text_secondary, width=65, anchor="w"
        ).pack(side="left")

        slider = ctk.CTkSlider(
            row, from_=lo, to=hi,
            number_of_steps=hi - lo,
            width=90, height=14,
            command=callback,
        )
        slider.set(default)
        slider.pack(side="left", fill="x", expand=True, padx=(0, 4))

        val_lbl = ctk.CTkLabel(
            row, text=str(default), font=ctk.CTkFont(size=11),
            text_color=theme.text_secondary, width=30,
        )
        val_lbl.pack(side="right")
        setattr(self, lbl_attr, val_lbl)

    # ------------------------------------------------------------------ #
    #  Collapse / Visibility
    # ------------------------------------------------------------------ #
    def _toggle_collapse(self):
        if self.is_collapsed:
            self.content.pack(fill="x")
            self.collapse_btn.configure(text="▼ 🪙 3D Token Preview")
            self.is_collapsed = False
            self._schedule_render()
        else:
            self.content.pack_forget()
            self.collapse_btn.configure(text="▶ 🪙 3D Token Preview")
            self.is_collapsed = True
            self._stop_auto_rotate()

    def toggle_visibility(self):
        """Toggle panel visibility (keyboard shortcut)."""
        if self.is_visible:
            self.frame.pack_forget()
            self.is_visible = False
            self._stop_auto_rotate()
        else:
            self.frame.pack(fill="x", padx=5, pady=(5, 2))
            self.is_visible = True
            if not self.is_collapsed:
                self._schedule_render()

    # ------------------------------------------------------------------ #
    #  Callbacks
    # ------------------------------------------------------------------ #
    def _on_thickness(self, value):
        t = max(1, int(float(value)))
        self.thickness_lbl.configure(text=str(t))
        self.renderer.thickness = t
        self.renderer.invalidate_cache()
        self._schedule_render()

    def _on_light(self, value):
        v = int(float(value))
        self.light_lbl.configure(text=f"{v}°")
        self.renderer.light_yaw = float(v)
        self._schedule_render()

    def _on_material(self, choice):
        self.renderer.material = choice.lower()
        self._schedule_render()

    def _on_backface(self, choice):
        self.renderer.back_face_mode = choice.lower()
        self.renderer.invalidate_cache()
        self._schedule_render()

    # ------------------------------------------------------------------ #
    #  Mouse rotation
    # ------------------------------------------------------------------ #
    def _on_drag_start(self, event):
        self._drag_x = event.x
        self._drag_y = event.y
        self._dragging = True

    def _on_drag(self, event):
        if not self._dragging:
            return
        dx = event.x - self._drag_x
        dy = event.y - self._drag_y
        self._drag_x = event.x
        self._drag_y = event.y

        self.renderer.rotation_y += dx * 0.8
        self.renderer.rotation_x -= dy * 0.8
        self.renderer.rotation_x = max(-90, min(90, self.renderer.rotation_x))
        self._do_render()  # immediate for smooth dragging

    def _on_drag_end(self, event):
        self._dragging = False

    def _on_scroll_zoom(self, event):
        if event.delta > 0:
            self.renderer.zoom = min(3.0, self.renderer.zoom * 1.12)
        else:
            self.renderer.zoom = max(0.3, self.renderer.zoom / 1.12)
        self._schedule_render()

    def _reset_rotation(self, event=None):
        self.renderer.rotation_x = 25.0
        self.renderer.rotation_y = -35.0
        self.renderer.zoom = 1.0
        self._schedule_render()

    # ------------------------------------------------------------------ #
    #  Auto-rotate
    # ------------------------------------------------------------------ #
    def _toggle_auto_rotate(self):
        if self._auto_rotate:
            self._stop_auto_rotate()
        else:
            self._auto_rotate = True
            theme = self.app.theme_manager.get_current_theme()
            self.auto_btn.configure(text="⏹ Stop", fg_color=theme.tool_selected)
            self._auto_step()

    def _stop_auto_rotate(self):
        self._auto_rotate = False
        if self._auto_rotate_job:
            try:
                self.app.root.after_cancel(self._auto_rotate_job)
            except Exception:
                pass
            self._auto_rotate_job = None
        theme = self.app.theme_manager.get_current_theme()
        self.auto_btn.configure(text="🔄 Spin", fg_color=theme.button_normal)

    def _auto_step(self):
        if not self._auto_rotate:
            return
        self.renderer.rotation_y += 2.0
        self._do_render()
        self._auto_rotate_job = self.app.root.after(33, self._auto_step)

    # ------------------------------------------------------------------ #
    #  Rendering
    # ------------------------------------------------------------------ #
    def _schedule_render(self, delay=50):
        """Debounced render (batches rapid changes)."""
        if self._render_job:
            try:
                self.app.root.after_cancel(self._render_job)
            except Exception:
                pass
        self._render_job = self.app.root.after(delay, self._do_render)

    def _do_render(self):
        """Perform the actual 3D render and display."""
        self._render_job = None
        if self.is_collapsed or not self.is_visible:
            return

        try:
            pixels = self.app.canvas.pixels
            if pixels is None or pixels.size == 0:
                return

            # Get canvas size for render
            cw = self.render_canvas.winfo_width()
            ch = self.render_canvas.winfo_height()
            rs = max(100, min(cw, ch, 300))

            img = self.renderer.render(pixels, render_size=rs)

            # Composite onto dark background
            bg = Image.new("RGBA", (rs, rs), (17, 17, 17, 255))
            bg = Image.alpha_composite(bg, img)

            self._photo = ImageTk.PhotoImage(bg.convert("RGB"))
            self.render_canvas.delete("all")
            self.render_canvas.create_image(
                cw // 2, ch // 2,
                image=self._photo, anchor="center", tags="render"
            )
        except Exception:
            pass  # Fail silently during rapid interaction

    def notify_canvas_changed(self):
        """Called when the canvas pixels change — invalidate & re-render."""
        self.renderer.invalidate_cache()
        if not self.is_collapsed and self.is_visible:
            self._schedule_render(delay=200)  # longer debounce for paint strokes

    # ------------------------------------------------------------------ #
    #  Export
    # ------------------------------------------------------------------ #
    def _export_png(self):
        """Export current 3D view as a high-res PNG."""
        path = filedialog.asksaveasfilename(
            title="Export 3D Token as PNG",
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            parent=self.app.root,
        )
        if not path:
            return

        try:
            pixels = self.app.canvas.pixels
            img = self.renderer.render(pixels, render_size=512)
            bg = Image.new("RGBA", (512, 512), (17, 17, 17, 255))
            bg = Image.alpha_composite(bg, img)
            bg.save(path)
        except Exception as e:
            print(f"[TokenPreview] Export PNG error: {e}")

    def _export_gif(self):
        """Export 360° spinning animation as GIF."""
        path = filedialog.asksaveasfilename(
            title="Export 3D Token as GIF",
            defaultextension=".gif",
            filetypes=[("GIF Animation", "*.gif")],
            parent=self.app.root,
        )
        if not path:
            return

        def _generate():
            try:
                pixels = self.app.canvas.pixels
                saved_ry = self.renderer.rotation_y
                frames = []
                n_frames = 36  # 10° per frame

                for i in range(n_frames):
                    self.renderer.rotation_y = saved_ry + i * (360.0 / n_frames)
                    img = self.renderer.render(pixels, render_size=256)
                    bg = Image.new("RGBA", (256, 256), (17, 17, 17, 255))
                    bg = Image.alpha_composite(bg, img)
                    frames.append(bg.convert("RGB"))

                self.renderer.rotation_y = saved_ry

                if frames:
                    frames[0].save(
                        path, save_all=True, append_images=frames[1:],
                        duration=66, loop=0, optimize=True,
                    )
            except Exception as e:
                print(f"[TokenPreview] Export GIF error: {e}")

        # Run in background thread to avoid freezing UI
        threading.Thread(target=_generate, daemon=True).start()

    # ------------------------------------------------------------------ #
    #  Theme
    # ------------------------------------------------------------------ #
    def update_theme(self, theme):
        """Update colors when theme changes."""
        self.frame.configure(fg_color=theme.bg_secondary)
        self.collapse_btn.configure(
            hover_color=theme.button_hover, text_color=theme.text_primary
        )
        self.auto_btn.configure(
            fg_color=theme.tool_selected if self._auto_rotate else theme.button_normal,
            hover_color=theme.button_hover,
            text_color=theme.text_primary,
        )
