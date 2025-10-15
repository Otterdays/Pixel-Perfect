"""
File Operations Manager for Pixel Perfect
Handles all file I/O operations: new, open, save, import, export, templates

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import os
import numpy as np
from tkinter import filedialog, messagebox
from PIL import Image


class FileOperationsManager:
    """Manages all file operations for the application"""
    
    def __init__(self, root, canvas, palette, layer_manager, timeline, project, 
                 export_manager, presets, layer_panel, timeline_panel):
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
        
        # Callback for forcing canvas updates (will be set by main_window)
        self.force_canvas_update_callback = None
        self.update_canvas_from_layers_callback = None
    
    def new_project(self):
        """Create a new project"""
        # Clear canvas
        self.canvas.clear()
        
        # Reset layers (clear_layers() already adds a "Background" layer)
        self.layer_manager.clear_layers()
        
        # Reset timeline
        self.timeline.clear_frames()
        self.timeline.add_frame()
        
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
                    f"Valid sizes: 16x16, 32x32, or 64x64\n"
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
    
    def export_png(self):
        """Export canvas as PNG"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Export as PNG",
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
            )
            
            if file_path:
                # Export with high quality (8x scaling) and transparency
                success = self.export_manager.export_png(
                    self.canvas.pixels, 
                    file_path, 
                    scale=8, 
                    transparent=True
                )
                if success:
                    print(f"Exported high-quality PNG (8x scale): {file_path}")
                else:
                    print(f"Failed to export PNG: {file_path}")
        except Exception as e:
            print(f"Error exporting PNG: {e}")
    
    def export_gif(self):
        """Export animation as GIF"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Export as GIF",
                defaultextension=".gif",
                filetypes=[("GIF Files", "*.gif"), ("All Files", "*.*")]
            )
            
            if file_path:
                # Get frames from timeline
                frames = [frame.pixels for frame in self.timeline.frames]
                success = self.export_manager.export_gif(
                    frames, 
                    file_path, 
                    scale=8,
                    duration=100  # 100ms per frame for smooth animation
                )
                if success:
                    print(f"Exported high-quality animated GIF (8x scale): {file_path}")
                else:
                    print(f"Failed to export GIF: {file_path}")
        except Exception as e:
            print(f"Error exporting GIF: {e}")
    
    def export_spritesheet(self):
        """Export as sprite sheet"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Export Sprite Sheet",
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
            )
            
            if file_path:
                # Get frames from timeline for sprite sheet
                frames = [frame.pixels for frame in self.timeline.frames]
                success = self.export_manager.export_sprite_sheet(
                    frames, 
                    file_path, 
                    scale=8,
                    layout="horizontal"  # Default to horizontal layout
                )
                if success:
                    print(f"Exported high-quality sprite sheet (8x scale): {file_path}")
                else:
                    print(f"Failed to export sprite sheet: {file_path}")
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

