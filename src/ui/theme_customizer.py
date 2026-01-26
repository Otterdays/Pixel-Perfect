"""
Theme Customizer for Pixel Perfect
Allows users to customize theme colors and save custom themes

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from src.ui.theme_manager import Theme


class ThemeCustomizer:
    """Manages theme customization dialog and custom theme storage"""
    
    def __init__(self, main_window, theme_manager):
        self.main_window = main_window
        self.theme_manager = theme_manager
        self.customizer_dialog: Optional[ctk.CTkToplevel] = None
        self.preview_theme: Optional[Theme] = None
        self.original_theme: Optional[Theme] = None
        
        # Storage path for custom themes
        self.storage_path = self._get_storage_path()
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def _get_storage_path(self) -> Path:
        """Get user-specific storage path for custom themes"""
        if os.name == 'nt':  # Windows
            base_path = Path(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')))
            return base_path / 'PixelPerfect' / 'themes'
        else:  # Mac/Linux
            return Path.home() / '.pixelperfect' / 'themes'
    
    def show_customizer(self):
        """Show theme customization dialog"""
        if self.customizer_dialog is not None:
            self.customizer_dialog.destroy()
        
        # Store original theme for cancel
        self.original_theme = self.theme_manager.get_current_theme()
        
        # Create preview theme (copy of current)
        self.preview_theme = self._copy_theme(self.original_theme)
        
        # Create dialog
        self.customizer_dialog = ctk.CTkToplevel(self.main_window.root)
        self.customizer_dialog.title("Theme Customizer")
        self.customizer_dialog.geometry("900x700")
        self.customizer_dialog.resizable(True, True)
        self.customizer_dialog.minsize(800, 600)
        self.customizer_dialog.transient(self.main_window.root)
        
        # Center dialog
        self.customizer_dialog.update_idletasks()
        x = self.main_window.root.winfo_x() + (self.main_window.root.winfo_width() // 2) - (450)
        y = self.main_window.root.winfo_y() + (self.main_window.root.winfo_height() // 2) - (350)
        self.customizer_dialog.geometry(f"+{x}+{y}")
        
        # Create UI
        self._create_ui()
        
        # Show dialog
        self.customizer_dialog.deiconify()
        self.customizer_dialog.grab_set()
        self.customizer_dialog.lift()
        self.customizer_dialog.focus_force()
    
    def _create_ui(self):
        """Create the customization UI"""
        # Main container with scroll
        main_frame = ctk.CTkScrollableFrame(
            self.customizer_dialog,
            fg_color=self.theme_manager.get_current_theme().bg_primary
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎨 Theme Customizer",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.theme_manager.get_current_theme().text_primary
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Customize colors and save your own themes",
            font=ctk.CTkFont(size=14),
            text_color=self.theme_manager.get_current_theme().text_secondary
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Theme name section
        name_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 20))
        
        name_label = ctk.CTkLabel(
            name_frame,
            text="Theme Name:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.theme_manager.get_current_theme().text_primary
        )
        name_label.pack(side="left", padx=(0, 10))
        
        self.theme_name_var = ctk.StringVar(value="Custom Theme")
        name_entry = ctk.CTkEntry(
            name_frame,
            textvariable=self.theme_name_var,
            width=200,
            font=ctk.CTkFont(size=13)
        )
        name_entry.pack(side="left")
        
        # Color picker sections
        self.color_widgets = {}
        
        # Background Colors
        self._create_color_section(main_frame, "Background Colors", [
            ("bg_primary", "Primary Background", "Main window background"),
            ("bg_secondary", "Secondary Background", "Panel backgrounds"),
            ("bg_tertiary", "Tertiary Background", "Accent panels"),
        ])
        
        # Text Colors
        self._create_color_section(main_frame, "Text Colors", [
            ("text_primary", "Primary Text", "Main text color"),
            ("text_secondary", "Secondary Text", "Secondary text color"),
            ("text_disabled", "Disabled Text", "Disabled/greyed text"),
        ])
        
        # Button Colors
        self._create_color_section(main_frame, "Button Colors", [
            ("button_normal", "Normal Button", "Default button color"),
            ("button_hover", "Button Hover", "Button hover state"),
            ("button_active", "Active Button", "Selected/active button"),
        ])
        
        # Canvas Colors
        self._create_color_section(main_frame, "Canvas Colors", [
            ("canvas_bg", "Canvas Background", "Drawing area background"),
            ("canvas_border", "Canvas Border", "Canvas border color"),
            ("grid_color", "Grid Color", "Grid line color"),
        ])
        
        # Tool Colors
        self._create_color_section(main_frame, "Tool Colors", [
            ("tool_selected", "Selected Tool", "Active tool highlight"),
            ("tool_unselected", "Unselected Tool", "Inactive tool color"),
        ])
        
        # Selection Colors
        self._create_color_section(main_frame, "Selection Colors", [
            ("selection_outline", "Selection Outline", "Selection box outline"),
            ("selection_handle", "Selection Handle", "Corner/edge handles"),
            ("selection_edge", "Selection Edge", "Edge highlight"),
        ])
        
        # Scrollbar Colors
        self._create_color_section(main_frame, "Scrollbar Colors", [
            ("scrollbar_button_color", "Scrollbar Button", "Scrollbar button color"),
            ("scrollbar_button_hover_color", "Scrollbar Hover", "Scrollbar hover state"),
            ("scrollbar_track_color", "Scrollbar Track", "Scrollbar track background"),
        ])
        
        # Border Colors
        self._create_color_section(main_frame, "Border Colors", [
            ("border_normal", "Normal Border", "Default border color"),
            ("border_focus", "Focus Border", "Focused element border"),
        ])
        
        # Buttons frame
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))
        
        # Left side buttons
        left_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        left_buttons.pack(side="left")
        
        preview_btn = ctk.CTkButton(
            left_buttons,
            text="Preview",
            width=120,
            height=35,
            command=self._preview_theme,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        preview_btn.pack(side="left", padx=(0, 10))
        
        reset_btn = ctk.CTkButton(
            left_buttons,
            text="Reset",
            width=120,
            height=35,
            command=self._reset_to_original,
            font=ctk.CTkFont(size=13)
        )
        reset_btn.pack(side="left", padx=(0, 10))
        
        # Right side buttons
        right_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        right_buttons.pack(side="right")
        
        import_btn = ctk.CTkButton(
            right_buttons,
            text="Import",
            width=100,
            height=35,
            command=self._import_theme,
            font=ctk.CTkFont(size=13)
        )
        import_btn.pack(side="left", padx=(0, 10))
        
        export_btn = ctk.CTkButton(
            right_buttons,
            text="Export",
            width=100,
            height=35,
            command=self._export_theme,
            font=ctk.CTkFont(size=13)
        )
        export_btn.pack(side="left", padx=(0, 10))
        
        save_btn = ctk.CTkButton(
            right_buttons,
            text="Save Theme",
            width=120,
            height=35,
            command=self._save_theme,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1f6aa5",
            hover_color="#1557b0"
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            right_buttons,
            text="Cancel",
            width=100,
            height=35,
            command=self._cancel,
            font=ctk.CTkFont(size=13)
        )
        cancel_btn.pack(side="left")
    
    def _create_color_section(self, parent, section_title: str, color_props: list):
        """Create a section with color pickers"""
        section_frame = ctk.CTkFrame(
            parent,
            fg_color=self.theme_manager.get_current_theme().bg_secondary
        )
        section_frame.pack(fill="x", pady=(0, 15))
        
        # Section title
        title_label = ctk.CTkLabel(
            section_frame,
            text=section_title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.theme_manager.get_current_theme().text_primary
        )
        title_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Color pickers grid
        colors_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        colors_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        for prop_name, display_name, description in color_props:
            self._create_color_picker(colors_frame, prop_name, display_name, description)
    
    def _create_color_picker(self, parent, prop_name: str, display_name: str, description: str):
        """Create a single color picker row"""
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", pady=5)
        
        # Label
        label_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        label_frame.pack(side="left", padx=(0, 15))
        
        name_label = ctk.CTkLabel(
            label_frame,
            text=display_name,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.theme_manager.get_current_theme().text_primary,
            width=180,
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        desc_label = ctk.CTkLabel(
            label_frame,
            text=description,
            font=ctk.CTkFont(size=11),
            text_color=self.theme_manager.get_current_theme().text_secondary,
            width=180,
            anchor="w"
        )
        desc_label.pack(anchor="w")
        
        # Color preview button
        current_color = getattr(self.preview_theme, prop_name, "#000000")
        color_btn = ctk.CTkButton(
            row_frame,
            text="",
            width=60,
            height=40,
            fg_color=current_color,
            hover_color=current_color,
            command=lambda pn=prop_name: self._pick_color(pn)
        )
        color_btn.pack(side="left", padx=(0, 10))
        
        # Hex value display
        hex_var = ctk.StringVar(value=current_color)
        hex_entry = ctk.CTkEntry(
            row_frame,
            textvariable=hex_var,
            width=100,
            font=ctk.CTkFont(size=12, family="monospace")
        )
        hex_entry.pack(side="left", padx=(0, 10))
        
        # Update hex when color changes
        def update_hex():
            color = getattr(self.preview_theme, prop_name, "#000000")
            hex_var.set(color)
            color_btn.configure(fg_color=color, hover_color=color)
        
        # Update color when hex changes
        def update_from_hex(*args):
            try:
                hex_value = hex_var.get().strip()
                if hex_value.startswith('#'):
                    # Validate hex color
                    if len(hex_value) == 7:
                        int(hex_value[1:], 16)  # Validate it's valid hex
                        setattr(self.preview_theme, prop_name, hex_value)
                        color_btn.configure(fg_color=hex_value, hover_color=hex_value)
            except:
                pass  # Invalid hex, ignore
        
        hex_var.trace('w', update_from_hex)
        
        # Store widgets for updates
        self.color_widgets[prop_name] = {
            'button': color_btn,
            'hex_var': hex_var,
            'update_hex': update_hex
        }
    
    def _pick_color(self, prop_name: str):
        """Open color picker for a property"""
        current_color = getattr(self.preview_theme, prop_name, "#000000")
        
        # Convert hex to RGB tuple for colorchooser
        if current_color.startswith('#'):
            r = int(current_color[1:3], 16)
            g = int(current_color[3:5], 16)
            b = int(current_color[5:7], 16)
            color = (r, g, b)
        else:
            color = (0, 0, 0)
        
        # Open color picker
        color_result = colorchooser.askcolor(
            color=color,
            title=f"Choose {prop_name} color"
        )
        
        if color_result[0] is not None:
            r, g, b = [int(c) for c in color_result[0]]
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            
            # Update theme
            setattr(self.preview_theme, prop_name, hex_color)
            
            # Update UI
            self.color_widgets[prop_name]['button'].configure(
                fg_color=hex_color,
                hover_color=hex_color
            )
            self.color_widgets[prop_name]['hex_var'].set(hex_color)
    
    def _preview_theme(self):
        """Apply preview theme to see changes"""
        if self.preview_theme:
            # Temporarily apply preview theme
            self.theme_manager.current_theme = self.preview_theme
            if self.theme_manager.on_theme_changed:
                self.theme_manager.on_theme_changed(self.preview_theme)
    
    def _reset_to_original(self):
        """Reset to original theme"""
        if self.original_theme:
            # Restore original theme
            self.preview_theme = self._copy_theme(self.original_theme)
            
            # Update all color pickers
            for prop_name, widgets in self.color_widgets.items():
                color = getattr(self.preview_theme, prop_name, "#000000")
                widgets['hex_var'].set(color)
                widgets['button'].configure(fg_color=color, hover_color=color)
            
            # Apply reset
            self._preview_theme()
    
    def _save_theme(self):
        """Save custom theme"""
        theme_name = self.theme_name_var.get().strip()
        if not theme_name:
            messagebox.showerror("Error", "Please enter a theme name")
            return
        
        # Check if name conflicts with built-in themes
        if theme_name in self.theme_manager.get_theme_names():
            if not messagebox.askyesno(
                "Overwrite Theme?",
                f"A theme named '{theme_name}' already exists. Overwrite it?"
            ):
                return
        
        # Save theme to file
        theme_file = self.storage_path / f"{theme_name.lower().replace(' ', '_')}.json"
        
        try:
            theme_data = self._theme_to_dict(self.preview_theme, theme_name)
            with open(theme_file, 'w') as f:
                json.dump(theme_data, f, indent=2)
            
            # Add to theme manager
            custom_theme = self._dict_to_theme(theme_data)
            self.theme_manager.themes[theme_name] = custom_theme
            
            # Update theme dropdown
            if hasattr(self.main_window, 'theme_menu'):
                current_value = self.main_window.theme_var.get()
                new_values = self.theme_manager.get_theme_names()
                self.main_window.theme_menu.configure(values=new_values)
                # Set to new theme name (it should be in the list)
                if theme_name in new_values:
                    self.main_window.theme_var.set(theme_name)
                elif current_value in new_values:
                    # Keep current if new name somehow not in list
                    self.main_window.theme_var.set(current_value)
            
            # Apply the saved theme
            self.theme_manager.set_theme(theme_name)
            
            messagebox.showinfo("Success", f"Theme '{theme_name}' saved successfully!")
            self._cancel()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save theme: {e}")
    
    def _export_theme(self):
        """Export theme to a file"""
        theme_name = self.theme_name_var.get().strip() or "Custom Theme"
        theme_data = self._theme_to_dict(self.preview_theme, theme_name)
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"{theme_name.lower().replace(' ', '_')}.json"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(theme_data, f, indent=2)
                messagebox.showinfo("Success", f"Theme exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export theme: {e}")
    
    def _import_theme(self):
        """Import theme from a file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    theme_data = json.load(f)
                
                # Load theme
                imported_theme = self._dict_to_theme(theme_data)
                self.preview_theme = imported_theme
                
                # Update theme name
                self.theme_name_var.set(imported_theme.name)
                
                # Update all color pickers
                for prop_name, widgets in self.color_widgets.items():
                    color = getattr(imported_theme, prop_name, "#000000")
                    widgets['hex_var'].set(color)
                    widgets['button'].configure(fg_color=color, hover_color=color)
                
                # Preview imported theme
                self._preview_theme()
                
                messagebox.showinfo("Success", f"Theme '{imported_theme.name}' imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import theme: {e}")
    
    def _cancel(self):
        """Cancel and restore original theme"""
        if self.original_theme:
            self.theme_manager.current_theme = self.original_theme
            if self.theme_manager.on_theme_changed:
                self.theme_manager.on_theme_changed(self.original_theme)
        
        if self.customizer_dialog:
            self.customizer_dialog.destroy()
            self.customizer_dialog = None
    
    def _copy_theme(self, theme: Theme) -> Theme:
        """Create a copy of a theme"""
        copy = Theme(theme.name)
        for attr in dir(theme):
            if not attr.startswith('_') and not callable(getattr(theme, attr)):
                setattr(copy, attr, getattr(theme, attr))
        return copy
    
    def _theme_to_dict(self, theme: Theme, name: str) -> Dict[str, Any]:
        """Convert theme to dictionary for JSON storage"""
        return {
            'name': name,
            'version': '1.0',
            'colors': {
                'bg_primary': theme.bg_primary,
                'bg_secondary': theme.bg_secondary,
                'bg_tertiary': theme.bg_tertiary,
                'text_primary': theme.text_primary,
                'text_secondary': theme.text_secondary,
                'text_disabled': theme.text_disabled,
                'button_normal': theme.button_normal,
                'button_hover': theme.button_hover,
                'button_active': theme.button_active,
                'border_normal': theme.border_normal,
                'border_focus': theme.border_focus,
                'canvas_bg': theme.canvas_bg,
                'canvas_border': theme.canvas_border,
                'grid_color': theme.grid_color,
                'tool_selected': theme.tool_selected,
                'tool_unselected': theme.tool_unselected,
                'selection_outline': theme.selection_outline,
                'selection_handle': theme.selection_handle,
                'selection_edge': theme.selection_edge,
                'scrollbar_button_color': theme.scrollbar_button_color,
                'scrollbar_button_hover_color': theme.scrollbar_button_hover_color,
                'scrollbar_track_color': theme.scrollbar_track_color,
            }
        }
    
    def _dict_to_theme(self, data: Dict[str, Any]) -> Theme:
        """Convert dictionary to Theme object"""
        theme = Theme(data['name'])
        colors = data.get('colors', {})
        
        for key, value in colors.items():
            if hasattr(theme, key):
                setattr(theme, key, value)
        
        return theme
    
    def load_custom_themes(self):
        """Load all custom themes from storage"""
        if not self.storage_path.exists():
            return
        
        for theme_file in self.storage_path.glob("*.json"):
            try:
                with open(theme_file, 'r') as f:
                    theme_data = json.load(f)
                
                custom_theme = self._dict_to_theme(theme_data)
                self.theme_manager.themes[custom_theme.name] = custom_theme
            except Exception as e:
                print(f"Error loading theme {theme_file}: {e}")
