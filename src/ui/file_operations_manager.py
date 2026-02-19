"""
File Operations Manager for Pixel Perfect
Handles all file I/O operations: new, open, save, import, export, templates

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import os
import json
import numpy as np
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image


class FileOperationsManager:
    """Manages all file operations for the application"""
    
    def __init__(self, root, canvas, palette, layer_manager, timeline, project, 
                 export_manager, presets, layer_panel, timeline_panel, tools):
        """
        Initialize the FileOperationsManager.
        
        Args:
            root: The main Tkinter root window
            canvas: The canvas object
            palette: The color palette object
            layer_manager: The layer manager object
            timeline: The animation timeline object
            project: The project manager object
            export_manager: The export manager object
            presets: The presets manager object
            layer_panel: The layer panel UI object
            timeline_panel: The timeline panel UI object
            tools: Dictionary of all tools (including edge tool)
        """
        self.root = root
        self.canvas = canvas
        self.palette = palette
        self.layer_manager = layer_manager
        self.timeline = timeline
        self.project = project
        self.export_manager = export_manager
        self.presets = presets
        self.layer_panel = layer_panel
        self.timeline_panel = timeline_panel
        self.tools = tools
        
        # Callbacks for forcing canvas updates (will be set by main_window)
        self.force_canvas_update_callback = None
        self.update_canvas_from_layers_callback = None
        self.clear_selection_and_reset_tools_callback = None
        self.purge_canvas_overlays_callback = None

        # Export presets and last export (loaded from disk)
        self.export_presets = self._load_export_presets()
    
    def new_project(self):
        """Create a new project"""
        # First, purge any transient overlays/edge artifacts
        if self.purge_canvas_overlays_callback:
            try:
                self.purge_canvas_overlays_callback()
            except Exception:
                pass
        # Clear canvas
        self.canvas.clear()
        
        # Reset layers (clear_layers() already adds a "Background" layer)
        self.layer_manager.clear_layers()
        
        # Reset timeline
        self.timeline.clear_frames()
        self.timeline.add_frame()
        
        # Clear edge lines if edge tool exists
        if hasattr(self, 'tools') and 'edge' in self.tools:
            edge_tool = self.tools['edge']
            if hasattr(edge_tool, 'clear_all_edges'):
                edge_tool.clear_all_edges()
        
        # Clear selection and reset tools to brush
        if self.clear_selection_and_reset_tools_callback:
            self.clear_selection_and_reset_tools_callback()
        
        # Force canvas redraw with grid and update UI
        if self.force_canvas_update_callback:
            self.force_canvas_update_callback()
        self.layer_panel.refresh()
        self.timeline_panel.refresh()
        
        print("[OK] New project created")
    
    def open_project(self):
        """Open an existing project"""
        try:
            file_path = filedialog.askopenfilename(
                parent=self.root,  # Set parent to keep dialog on top
                title="Open Pixel Perfect Project",
                filetypes=[("Pixel Perfect Files", "*.pixpf"), ("All Files", "*.*")]
            )
            
            if file_path:
                # Load project with all required parameters
                success = self.project.load_project(
                    file_path,
                    self.canvas,
                    self.palette,
                    self.layer_manager,
                    self.timeline
                )
                
                if success:
                    # Update canvas from loaded layers (this composites all layers)
                    if self.update_canvas_from_layers_callback:
                        self.update_canvas_from_layers_callback()
                    
                    # Update UI components to reflect loaded project
                    self.layer_panel.refresh()
                    self.timeline_panel.refresh()
                    
                    # Force immediate display update
                    self.root.update_idletasks()
                    self.root.update()
                    
                    print(f"[OK] Project opened: {file_path}")
                else:
                    print(f"[ERROR] Failed to open project: {file_path}")
        except Exception as e:
            print(f"[ERROR] Error opening project: {e}")
            import traceback
            traceback.print_exc()
    
    def save_project(self):
        """Save current project"""
        try:
            if self.project.current_project_path:
                self.project.save_project(
                    self.project.current_project_path,
                    self.canvas,
                    self.palette,
                    self.layer_manager,
                    self.timeline
                )
                print(f"Project saved: {self.project.current_project_path}")
            else:
                self.save_project_as()
        except Exception as e:
            print(f"Error saving project: {e}")
    
    def save_project_as(self):
        """Save project with new name"""
        try:
            file_path = filedialog.asksaveasfilename(
                parent=self.root,  # Set parent to keep dialog on top
                title="Save Pixel Perfect Project",
                defaultextension=".pixpf",
                filetypes=[("Pixel Perfect Files", "*.pixpf"), ("All Files", "*.*")]
            )
            
            if file_path:
                self.project.save_project(
                    file_path,
                    self.canvas,
                    self.palette,
                    self.layer_manager,
                    self.timeline
                )
                self.project.current_project_path = file_path
                print(f"Project saved as: {file_path}")
        except Exception as e:
            print(f"Error saving project: {e}")
    
    def import_png(self):
        """Import PNG directly into current canvas"""
        try:
            # Open file dialog for PNG selection
            png_path = filedialog.askopenfilename(
                parent=self.root,  # Set parent to keep dialog on top
                title="Import PNG Image",
                filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
            )
            
            if not png_path:
                return  # User cancelled
            
            # Load and validate PNG
            from src.utils.import_png import PNGImporter
            importer = PNGImporter()
            is_valid, message, width, height = importer.validate_png_dimensions(png_path)
            
            if not is_valid:
                messagebox.showerror(
                    "Invalid PNG Dimensions",
                    f"{message}\n\n"
                    f"Valid sizes: 8x8, 16x16, 32x32, or 64x64\n"
                    f"(or scaled versions: 128x128, 256x256, 512x512)"
                )
                return
            
            # Load the PNG
            image = Image.open(png_path)
            original_width, original_height = image.size
            
            # Check if we need to downscale
            needs_downscale = False
            scale_factor = 1
            
            if original_width != width or original_height != height:
                # Calculate scale factor
                scale_factor = original_width // width
                needs_downscale = True
                
                # Downscale using nearest neighbor
                rgba_image = image.convert('RGBA')
                rgba_image = rgba_image.resize((width, height), Image.NEAREST)
                print(f"Auto-downscaled from {original_width}x{original_height} to {width}x{height} ({scale_factor}x)")
            else:
                rgba_image = image.convert('RGBA')
            
            # Convert to numpy array
            pixels = np.array(rgba_image, dtype=np.uint8)
            
            # Update dimensions FIRST (before clearing layers)
            self.canvas.width = width
            self.canvas.height = height
            self.layer_manager.width = width
            self.layer_manager.height = height
            
            # Initialize canvas pixels array with correct dimensions
            self.canvas.pixels = np.zeros((height, width, 4), dtype=np.uint8)
            
            # Now clear layers (this will create layers with the NEW dimensions)
            self.layer_manager.clear_layers()
            
            # Set the imported pixels and layer name
            self.layer_manager.layers[0].name = "Imported"
            self.layer_manager.layers[0].pixels = pixels
            
            # Update canvas from layers (copies layer data to canvas.pixels)
            if self.update_canvas_from_layers_callback:
                self.update_canvas_from_layers_callback()
            
            # NOW create the pygame surface with the correct pixel data
            self.canvas._create_surface()
            
            # Clear animation frames
            self.timeline.frames.clear()
            self.timeline.current_frame = 0
            
            # Update UI
            self.layer_panel.refresh()
            self.timeline_panel.refresh()
            self.root.update_idletasks()
            self.root.update()
            
            # Clear project path (this is now a new unsaved project)
            self.project.current_project_path = None
            
            # Show success message
            if needs_downscale:
                messagebox.showinfo(
                    "Import Successful",
                    f"Imported {original_width}x{original_height} PNG\n"
                    f"(Auto-downscaled {scale_factor}x to {width}x{height})\n\n"
                    f"Ready to edit! Use File → Save Project when ready."
                )
            else:
                messagebox.showinfo(
                    "Import Successful",
                    f"Imported {width}x{height} PNG\n\n"
                    f"Ready to edit! Use File → Save Project when ready."
                )
            
            print(f"[OK] Imported PNG to canvas: {os.path.basename(png_path)}")
                
        except Exception as e:
            messagebox.showerror("Import Error", f"An error occurred:\n{e}")
            print(f"Error importing PNG: {e}")
            import traceback
            traceback.print_exc()
    
    def _get_export_presets_path(self) -> str:
        """Return the file path for export presets."""
        if os.name == 'nt':
            base_dir = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
            return os.path.join(base_dir, 'PixelPerfect', 'export_presets.json')
        return os.path.expanduser('~/.pixelperfect/export_presets.json')

    def _default_export_presets(self) -> dict:
        """Return default export presets."""
        return {
            "PNG": {"scale": 8, "transparent": True},
            "GIF": {"scale": 8, "duration": 100},
            "Sprite Sheet": {"scale": 8, "layout": "horizontal", "spacing": 1},
            "Godot Sprite Sheet": {"scale": 4, "fps": 10, "loop": True},
            "recent_directories": [],  # MRU list of export directories
            "last_directory": None,  # Most recently used directory
            "last_export": None
        }

    def _load_export_presets(self) -> dict:
        """Load export presets from disk or return defaults."""
        path = self._get_export_presets_path()
        if not os.path.exists(path):
            return self._default_export_presets()
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            defaults = self._default_export_presets()
            defaults.update({k: v for k, v in data.items() if k in defaults})
            defaults["last_export"] = data.get("last_export")
            return defaults
        except Exception:
            return self._default_export_presets()

    def _save_export_presets(self):
        """Persist export presets to disk."""
        path = self._get_export_presets_path()
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                json.dump(self.export_presets, f, indent=2)
        except Exception:
            pass
    
    def _show_export_message(self, message: str, is_error: bool = False):
        """Show export status message in status bar or print fallback."""
        # Try to find main window via root
        try:
            # Get the main window (root might be CTk root)
            main_window = self.root
            if hasattr(main_window, 'status_bar'):
                main_window.status_bar.show_message(message, 3000)
                return
            # Try to find via toplevel
            if hasattr(main_window, 'winfo_toplevel'):
                top = main_window.winfo_toplevel()
                if hasattr(top, 'status_bar'):
                    top.status_bar.show_message(message, 3000)
                    return
        except Exception:
            pass
        # Fallback to print
        prefix = "[ERROR] " if is_error else "[OK] "
        print(f"{prefix}{message}")

    def _set_last_export(self, format_name: str, file_path: str, settings: dict):
        """Record last export and save presets."""
        self.export_presets[format_name] = settings
        self.export_presets["last_export"] = {
            "format": format_name,
            "path": file_path,
            "settings": settings
        }
        
        # Track recent directories
        import os
        directory = os.path.dirname(file_path)
        if directory:
            # Update last directory
            self.export_presets["last_directory"] = directory
            
            # Add to recent directories (MRU, max 10)
            recent_dirs = self.export_presets.get("recent_directories", [])
            if directory in recent_dirs:
                recent_dirs.remove(directory)
            recent_dirs.insert(0, directory)
            self.export_presets["recent_directories"] = recent_dirs[:10]  # Keep max 10
        
        self._save_export_presets()

    def _prompt_export_settings(self, format_name: str) -> dict:
        """Show export settings dialog and return settings or None."""
        preset = self.export_presets.get(format_name, {})
        result = {}

        dialog = ctk.CTkToplevel(self.root)
        dialog.title(f"{format_name} Export Settings")
        dialog.geometry("320x240")
        dialog.transient(self.root)
        dialog.grab_set()

        def close_dialog():
            dialog.grab_release()
            dialog.destroy()

        frame = ctk.CTkFrame(dialog)
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Scale
        scale_label = ctk.CTkLabel(frame, text="Scale:")
        scale_label.pack(anchor="w")
        scale_values = [f"{s}x" for s in self.export_manager.get_scale_factors()]
        scale_var = ctk.StringVar(value=f"{preset.get('scale', 8)}x")
        scale_menu = ctk.CTkOptionMenu(frame, values=scale_values, variable=scale_var)
        scale_menu.pack(fill="x", pady=(0, 10))

        # Format-specific options
        transparent_var = ctk.BooleanVar(value=preset.get("transparent", True))
        duration_var = ctk.StringVar(value=str(preset.get("duration", 100)))
        layout_var = ctk.StringVar(value=preset.get("layout", "horizontal"))
        spacing_var = ctk.StringVar(value=str(preset.get("spacing", 1)))

        if format_name == "PNG":
            transparent_check = ctk.CTkCheckBox(frame, text="Transparent Background", variable=transparent_var)
            transparent_check.pack(anchor="w", pady=(0, 10))
        elif format_name == "GIF":
            duration_label = ctk.CTkLabel(frame, text="Frame Duration (ms):")
            duration_label.pack(anchor="w")
            duration_entry = ctk.CTkEntry(frame, textvariable=duration_var)
            duration_entry.pack(fill="x", pady=(0, 10))
        elif format_name == "Sprite Sheet":
            layout_label = ctk.CTkLabel(frame, text="Layout:")
            layout_label.pack(anchor="w")
            layout_menu = ctk.CTkOptionMenu(
                frame,
                values=["horizontal", "vertical", "grid"],
                variable=layout_var
            )
            layout_menu.pack(fill="x", pady=(0, 10))

            spacing_entry = ctk.CTkEntry(frame, textvariable=spacing_var)
            spacing_entry.pack(fill="x", pady=(0, 10))
        elif format_name == "Godot Sprite Sheet":
            fps_label = ctk.CTkLabel(frame, text="Animation FPS:")
            fps_label.pack(anchor="w")
            fps_entry = ctk.CTkEntry(frame, textvariable=ctk.StringVar(value=str(preset.get("fps", 10))))
            fps_entry.pack(fill="x", pady=(0, 10))
            
            loop_var = ctk.BooleanVar(value=preset.get("loop", True))
            loop_check = ctk.CTkCheckBox(frame, text="Loop Animation", variable=loop_var)
            loop_check.pack(anchor="w", pady=(0, 10))

        # Buttons
        button_row = ctk.CTkFrame(frame, fg_color="transparent")
        button_row.pack(fill="x", pady=(10, 0))

        def on_confirm():
            try:
                scale_value = int(scale_var.get().replace("x", ""))
                if format_name == "PNG":
                    result.update({"scale": scale_value, "transparent": bool(transparent_var.get())})
                elif format_name == "GIF":
                    result.update({
                        "scale": scale_value,
                        "duration": max(10, int(duration_var.get()))
                    })
                else:
                    result.update({
                        "scale": scale_value,
                        "layout": layout_var.get(),
                        "layout": layout_var.get(),
                        "spacing": max(0, int(spacing_var.get()))
                    })
                elif format_name == "Godot Sprite Sheet":
                    result.update({
                        "scale": scale_value,
                        "fps": float(fps_entry.get()),
                        "loop": loop_var.get()
                    })
                close_dialog()
            except Exception:
                messagebox.showerror("Invalid Settings", "Please enter valid export settings.")

        def on_cancel():
            result.clear()
            close_dialog()

        confirm_btn = ctk.CTkButton(button_row, text="Export", command=on_confirm)
        confirm_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))
        cancel_btn = ctk.CTkButton(button_row, text="Cancel", command=on_cancel)
        cancel_btn.pack(side="left", expand=True, fill="x", padx=(5, 0))

        dialog.wait_window()
        return result if result else None

    def quick_export(self):
        """Quick export using last export settings and path."""
        last_export = self.export_presets.get("last_export")
        if not last_export:
            messagebox.showinfo(
                "Quick Export",
                "No previous export found.\nUse File → Export first to set a preset."
            )
            return

        format_name = last_export.get("format")
        file_path = last_export.get("path")
        settings = last_export.get("settings", {})

        if not format_name or not file_path:
            messagebox.showinfo(
                "Quick Export",
                "Last export settings are incomplete.\nUse File → Export to reset."
            )
            return

        try:
            if format_name == "PNG":
                success = self.export_manager.export_png(
                    self.canvas.pixels,
                    file_path,
                    scale=settings.get("scale", 8),
                    transparent=settings.get("transparent", True)
                )
            elif format_name == "GIF":
                frames = [frame.pixels for frame in self.timeline.frames]
                success = self.export_manager.export_gif(
                    frames,
                    file_path,
                    scale=settings.get("scale", 8),
                    duration=settings.get("duration", 100)
                )
                )
            elif format_name == "Godot Sprite Sheet":
                frames = [frame.pixels for frame in self.timeline.frames]
                success = self.export_manager.export_godot_sheet(
                    frames,
                    file_path,
                    scale=settings.get("scale", 4),
                    fps=settings.get("fps", 10.0),
                    loop=settings.get("loop", True)
                )
            else:
                frames = [frame.pixels for frame in self.timeline.frames]
                success = self.export_manager.export_sprite_sheet(
                    frames,
                    file_path,
                    scale=settings.get("scale", 8),
                    layout=settings.get("layout", "horizontal"),
                    spacing=settings.get("spacing", 1)
                )

            if success:
                self._show_export_message(f"Exported {format_name}: {os.path.basename(file_path)}")
            else:
                self._show_export_message(f"Export failed: {format_name}", is_error=True)
        except Exception as e:
            self._show_export_message(f"Export error: {str(e)[:50]}", is_error=True)

    def export_png(self):
        """Export canvas as PNG"""
        try:
            settings = self._prompt_export_settings("PNG")
            if not settings:
                return

            # Use last directory if available
            initialdir = self.export_presets.get("last_directory")
            file_path = filedialog.asksaveasfilename(
                parent=self.root,  # Set parent to keep dialog on top
                title="Export as PNG",
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")],
                initialdir=initialdir
            )
            
            if file_path:
                # Export using preset settings
                success = self.export_manager.export_png(
                    self.canvas.pixels, 
                    file_path, 
                    scale=settings["scale"], 
                    transparent=settings["transparent"]
                )
                if success:
                    self._set_last_export("PNG", file_path, settings)
                    # Show success in status bar
                    self._show_export_message(f"Exported PNG ({settings['scale']}x): {os.path.basename(file_path)}")
                else:
                    self._show_export_message("Failed to export PNG", is_error=True)
        except Exception as e:
            print(f"Error exporting PNG: {e}")
    
    def export_gif(self):
        """Export animation as GIF"""
        try:
            settings = self._prompt_export_settings("GIF")
            if not settings:
                return

            # Use last directory if available
            initialdir = self.export_presets.get("last_directory")
            file_path = filedialog.asksaveasfilename(
                parent=self.root,  # Set parent to keep dialog on top
                title="Export as GIF",
                defaultextension=".gif",
                filetypes=[("GIF Files", "*.gif"), ("All Files", "*.*")],
                initialdir=initialdir
            )
            
            if file_path:
                # Get frames from timeline
                frames = [frame.pixels for frame in self.timeline.frames]
                success = self.export_manager.export_gif(
                    frames, 
                    file_path, 
                    scale=settings["scale"],
                    duration=settings["duration"]
                )
                if success:
                    self._set_last_export("GIF", file_path, settings)
                    self._show_export_message(f"Exported GIF ({settings['scale']}x): {os.path.basename(file_path)}")
                else:
                    self._show_export_message("Failed to export GIF", is_error=True)
        except Exception as e:
            print(f"Error exporting GIF: {e}")
    
    def export_godot_sheet(self):
        """Export as Godot-ready sprite sheet"""
        try:
            settings = self._prompt_export_settings("Godot Sprite Sheet")
            if not settings:
                return

            # Use last directory if available
            initialdir = self.export_presets.get("last_directory")
            file_path = filedialog.asksaveasfilename(
                parent=self.root,
                title="Export for Godot",
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")],
                initialdir=initialdir
            )
            
            if file_path:
                frames = [frame.pixels for frame in self.timeline.frames]
                success = self.export_manager.export_godot_sheet(
                    frames, 
                    file_path, 
                    scale=settings["scale"],
                    fps=settings["fps"],
                    loop=settings["loop"]
                )
                if success:
                    self._set_last_export("Godot Sprite Sheet", file_path, settings)
                    self._show_export_message(f"Exported to Godot ({settings['scale']}x): {os.path.basename(file_path)}")
                else:
                    self._show_export_message("Failed to export Godot Sheet", is_error=True)
        except Exception as e:
            print(f"Error exporting Godot sheet: {e}")
    
    def export_spritesheet(self):
        """Export as sprite sheet"""
        try:
            settings = self._prompt_export_settings("Sprite Sheet")
            if not settings:
                return

            # Use last directory if available
            initialdir = self.export_presets.get("last_directory")
            file_path = filedialog.asksaveasfilename(
                parent=self.root,  # Set parent to keep dialog on top
                title="Export Sprite Sheet",
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")],
                initialdir=initialdir
            )
            
            if file_path:
                # Get frames from timeline for sprite sheet
                frames = [frame.pixels for frame in self.timeline.frames]
                success = self.export_manager.export_sprite_sheet(
                    frames, 
                    file_path, 
                    scale=settings["scale"],
                    layout=settings["layout"],
                    spacing=settings["spacing"]
                )
                if success:
                    self._set_last_export("Sprite Sheet", file_path, settings)
                    self._show_export_message(f"Exported Sprite Sheet ({settings['scale']}x): {os.path.basename(file_path)}")
                else:
                    self._show_export_message("Failed to export Sprite Sheet", is_error=True)
        except Exception as e:
            print(f"Error exporting sprite sheet: {e}")
    
    def show_templates(self):
        """Show template selection dialog"""
        import customtkinter as ctk
        
        template_menu = ctk.CTkToplevel(self.root)
        template_menu.title("Load Template")
        template_menu.geometry("300x400")
        template_menu.transient(self.root)
        template_menu.grab_set()
        
        # Center the menu
        template_menu.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))
        
        # Template categories
        categories = ["Characters", "Items", "Tiles", "UI Elements"]
        
        for category in categories:
            cat_frame = ctk.CTkFrame(template_menu)
            cat_frame.pack(fill="x", padx=10, pady=5)
            
            cat_label = ctk.CTkLabel(cat_frame, text=category, font=ctk.CTkFont(weight="bold"))
            cat_label.pack(pady=5)
            
            # Add template buttons for each category
            if category == "Characters":
                templates = ["32x32 Character (top-down)", "16x32 Character (side-view)"]
            elif category == "Items":
                templates = ["16x16 Item icon", "32x32 Item icon (detailed)"]
            elif category == "Tiles":
                templates = ["16x16 Grass tile", "16x16 Stone tile"]
            elif category == "UI Elements":
                templates = ["32x16 Button (UI)", "16x16 Icon (UI)"]
            
            for template in templates:
                btn = ctk.CTkButton(
                    cat_frame, 
                    text=template,
                    command=lambda t=template: [self.load_template(t), template_menu.destroy()]
                )
                btn.pack(pady=2, padx=5, fill="x")
        
        close_btn = ctk.CTkButton(template_menu, text="Close", command=template_menu.destroy)
        close_btn.pack(pady=10, padx=10, fill="x")
    
    def load_template(self, template_name):
        """Load a template"""
        try:
            template_data = self.presets.get_template(template_name)
            if template_data:
                # Set canvas size based on template
                width, height = template_data.get('size', (32, 32))
                self.canvas.resize(width, height)
                
                # Load template pixels if available
                if 'pixels' in template_data:
                    self.canvas.pixels = template_data['pixels']
                    if self.force_canvas_update_callback:
                        self.force_canvas_update_callback()
                
                print(f"Loaded template: {template_name}")
            else:
                print(f"Template not found: {template_name}")
        except Exception as e:
            print(f"Error loading template: {e}")

