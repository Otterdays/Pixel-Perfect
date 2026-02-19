"""
Theme and Dialog Manager for Pixel Perfect
Handles theme application and settings dialog management

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import customtkinter as ctk
import tkinter as tk
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ui.main_window import MainWindow

class ThemeDialogManager:
    """Manages theme application and settings dialog functionality"""
    
    def __init__(self, main_window: 'MainWindow'):
        self.main_window = main_window
        self.settings_dialog: Optional[ctk.CTkToplevel] = None
        self.theme_customizer = None  # Will be set after theme_customizer is initialized
        
        # Create settings dialog at startup for instant display
        self._create_settings_dialog()
    
    def _create_settings_dialog(self):
        """Create settings dialog once at startup (OPTIMIZED - pre-render for instant display)"""
        dialog = ctk.CTkToplevel(self.main_window.root)
        dialog.title("Settings")
        dialog.geometry("500x550")
        dialog.resizable(True, True)
        dialog.minsize(500, 550)
        dialog.transient(self.main_window.root)
        
        # Header frame with gear icon
        header_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        header_frame.pack(pady=(15, 10), padx=20, fill="x")
        
        icon_label = ctk.CTkLabel(
            header_frame,
            text="⚙️",
            font=ctk.CTkFont(size=64)
        )
        icon_label.pack(pady=10)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="SETTINGS",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1a73e8"
        )
        title_label.pack()
        
        # Settings options
        options_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        options_frame.pack(pady=(5, 15), padx=20, fill="both", expand=True)
        
        # Theme Customizer button (main feature)
        theme_customizer_btn = ctk.CTkButton(
            options_frame,
            text="🎨 Customize Theme",
            width=300,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#1f6aa5",
            hover_color="#1557b0",
            command=self._open_theme_customizer
        )
        theme_customizer_btn.pack(pady=15)
        
        theme_desc = ctk.CTkLabel(
            options_frame,
            text="Customize colors, save themes, and export/import theme files",
            font=ctk.CTkFont(size=12),
            text_color="#b0b0b0"
        )
        theme_desc.pack(pady=(0, 20))
        
        # Separator
        separator = ctk.CTkFrame(options_frame, height=2, fg_color="#404040")
        separator.pack(fill="x", pady=10)
        
        # Coming soon message for other settings
        message_label = ctk.CTkLabel(
            options_frame,
            text="More Settings Coming Soon!",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#e0e0e0"
        )
        message_label.pack(pady=(10, 10))
        
        info_text = "Additional settings are in development:\n"
        info_text += "• Canvas & Grid preferences\n"
        info_text += "• Tool defaults & behavior\n"
        info_text += "• UI scale & DPI controls\n"
        info_text += "• Keyboard shortcuts\n"
        info_text += "• And much more!\n\n"
        info_text += "See MAX_SETTINGS.md for the full list of 127 planned settings."
        
        info_label = ctk.CTkLabel(
            options_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            text_color="#b0b0b0",
            justify="left"
        )
        info_label.pack(pady=10)
        
        # Credits section
        credits_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        credits_frame.pack(pady=(10, 5), padx=20, fill="x")
        
        credits_label = ctk.CTkLabel(
            credits_frame,
            text="Developed with the power of AI",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#1a73e8"
        )
        credits_label.pack()
        
        credits_text = "Ryan - Developer\nJames - Designer"
        
        credits_text_label = ctk.CTkLabel(
            credits_frame,
            text=credits_text,
            font=ctk.CTkFont(size=11),
            text_color="#888888",
            justify="center"
        )
        credits_text_label.pack(pady=(5, 0))
        
        # Close button
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        close_btn = ctk.CTkButton(
            button_frame,
            text="OK",
            width=140,
            height=40,
            fg_color="#1a73e8",
            hover_color="#1557b0",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._hide_settings_dialog
        )
        close_btn.pack()
        
        # Store dialog reference
        self.settings_dialog = dialog
        
        # Hide dialog initially (withdraw instead of destroy)
        dialog.withdraw()
    
    def _show_settings_dialog(self):
        """Show settings dialog with latest changes"""
        # Force recreation to pick up any code changes
        if self.settings_dialog is not None:
            self.settings_dialog.destroy()
            self.settings_dialog = None
        
        # Create fresh dialog with latest changes
        self._create_settings_dialog()
        
        # Center dialog on screen
        self.settings_dialog.update_idletasks()
        x = self.main_window.root.winfo_x() + (self.main_window.root.winfo_width() // 2) - (500 // 2)
        y = self.main_window.root.winfo_y() + (self.main_window.root.winfo_height() // 2) - (550 // 2)
        self.settings_dialog.geometry(f"+{x}+{y}")
        
        # Show dialog
        self.settings_dialog.deiconify()
        self.settings_dialog.grab_set()
        self.settings_dialog.lift()
        self.settings_dialog.focus_force()
    
    def _hide_settings_dialog(self):
        """Hide settings dialog (withdraw for instant re-show)"""
        if self.settings_dialog:
            self.settings_dialog.grab_release()
            self.settings_dialog.withdraw()
    
    def show_settings_dialog(self):
        """Public method to show settings dialog"""
        self._show_settings_dialog()
    
    def hide_settings_dialog(self):
        """Public method to hide settings dialog"""
        self._hide_settings_dialog()
    
    def _open_theme_customizer(self):
        """Open theme customizer dialog"""
        if self.theme_customizer:
            self.theme_customizer.show_customizer()
        else:
            # Fallback if customizer not initialized
            import tkinter.messagebox as msgbox
            msgbox.showinfo("Theme Customizer", "Theme customizer is being initialized...")
    
    def set_theme_customizer(self, customizer):
        """Set the theme customizer instance"""
        self.theme_customizer = customizer
    
    def apply_theme(self, theme):
        """Apply theme colors to all UI elements - optimized for instant switching"""
        # SKIP appearance mode change - it causes full UI refresh!
        # Instead, manually configure all widget colors
        
        # Direct widget configuration (fast and immediate, no UI refresh)
        self.main_window.main_frame.configure(fg_color=theme.bg_primary)
        self.main_window.toolbar.configure(fg_color=theme.bg_secondary)
        self.main_window.tool_frame.configure(fg_color=theme.bg_primary)
        self.main_window.canvas_frame.configure(fg_color="transparent")
        # Use background mode logic for canvas background
        if getattr(self.main_window.canvas, "checkerboard", False):
            self.main_window.drawing_canvas.configure(bg="#e8e8e8")
        else:
            bg_color = self.main_window.canvas_renderer.get_background_color()
            self.main_window.drawing_canvas.configure(bg=bg_color)
        
        # Update panel containers and buttons
        self.main_window.left_container.configure(bg=theme.bg_primary)
        self.main_window.right_container.configure(bg=theme.bg_primary)
        if hasattr(self.main_window, 'left_btn_container'):
            self.main_window.left_btn_container.configure(bg=theme.bg_primary)
        if hasattr(self.main_window, 'right_btn_container'):
            self.main_window.right_btn_container.configure(bg=theme.bg_primary)
        self.main_window.left_collapse_btn.configure(
            fg_color="transparent",
            hover_color=theme.button_hover,
            text_color=theme.text_secondary
        )
        self.main_window.right_collapse_btn.configure(
            fg_color="transparent",
            hover_color=theme.button_hover,
            text_color=theme.text_secondary
        )
        
        # Update scrollable panel backgrounds to match theme
        self.main_window.left_panel.configure(fg_color=theme.bg_secondary)
        self.main_window.right_panel.configure(fg_color="transparent")
        
        # Update all tool buttons
        for tool_id, btn in self.main_window.tool_buttons.items():
            if tool_id == self.main_window.current_tool:
                btn.configure(
                    fg_color=theme.tool_selected,
                    hover_color=theme.button_hover,
                    text_color=theme.text_primary
                )
            else:
                btn.configure(
                    fg_color=theme.tool_unselected,
                    hover_color=theme.button_hover,
                    text_color=theme.text_primary
                )
        
        # Update operation buttons (Mirror, Rotate, Copy, Scale, Symmetry)
        if hasattr(self.main_window, 'mirror_btn'):
            for btn in [self.main_window.mirror_btn, self.main_window.rotate_btn, 
                       self.main_window.copy_btn, self.main_window.scale_btn]:
                btn.configure(
                    fg_color=theme.button_normal,
                    hover_color=theme.button_hover,
                    text_color=theme.text_primary
                )
        
        # Update symmetry buttons based on state
        if hasattr(self.main_window, 'sym_x_btn') and hasattr(self.main_window, 'sym_y_btn'):
            self.main_window._update_symmetry_buttons()
        
        # Update grid button
        if self.main_window.canvas.show_grid:
            self.main_window.grid_button.configure(fg_color="green", text_color=theme.text_primary)
        else:
            self.main_window.grid_button.configure(fg_color=theme.button_normal, text_color=theme.text_primary)
        
        # Update other toolbar buttons (different configure params for different widget types)
        self.main_window.file_button.configure(
            fg_color=theme.button_normal,
            hover_color=theme.button_hover,
            text_color=theme.text_primary
        )
        
        # Update dropdowns (CTkOptionMenu has different params) - FORCE update to prevent boxes
        for dropdown in [self.main_window.size_menu, self.main_window.zoom_menu, self.main_window.theme_menu]:
            try:
                dropdown.configure(
                    fg_color=theme.button_normal,
                    text_color=theme.text_primary,
                    dropdown_fg_color=theme.bg_secondary,
                    dropdown_hover_color=theme.button_hover,
                    button_color=theme.button_normal,  # Force button background
                    button_hover_color=theme.button_hover
                )
                # Force immediate update
                dropdown.update_idletasks()
            except Exception as e:
                print(f"[DEBUG] Dropdown theme error: {e}")
                pass  # Skip if params not supported
        
        # Update labels
        self.main_window.size_label.configure(text_color=theme.text_primary)
        self.main_window.zoom_label.configure(text_color=theme.text_primary)
        self.main_window.theme_label.configure(text_color=theme.text_primary)
        
        # Update left and right panel backgrounds
        self.main_window.left_panel.configure(
            fg_color=theme.bg_secondary,
            scrollbar_button_color=theme.button_normal,
            scrollbar_button_hover_color=theme.button_hover
        )
        self.main_window.right_panel.configure(
            fg_color="transparent",
            scrollbar_button_color=theme.button_normal,
            scrollbar_button_hover_color=theme.button_hover
        )
        
        # Update palette panel label
        if hasattr(self.main_window, 'palette_label'):
            self.main_window.palette_label.configure(text_color=theme.text_primary)
        
        # Update all section labels and frames in tool panel
        for widget in self.main_window.tool_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=theme.text_primary)
            elif isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color=theme.bg_primary)
        
        # Update color display frames (palette views) - CRITICAL for preventing boxes
        if hasattr(self.main_window, 'grid_view_frame'):
            self.main_window.grid_view_frame.configure(fg_color=theme.bg_secondary)
        if hasattr(self.main_window, 'primary_view_frame'):
            self.main_window.primary_view_frame.configure(fg_color=theme.bg_secondary)
        if hasattr(self.main_window, 'wheel_view_frame'):
            self.main_window.wheel_view_frame.configure(fg_color=theme.bg_secondary)
        if hasattr(self.main_window, 'constants_view_frame'):
            self.main_window.constants_view_frame.configure(fg_color=theme.bg_secondary)
        if hasattr(self.main_window, 'saved_view_frame'):
            self.main_window.saved_view_frame.configure(fg_color=theme.bg_secondary)
        
        # Update color_frame if it exists
        if hasattr(self.main_window, 'color_frame') and self.main_window.color_frame:
            self.main_window.color_frame.configure(fg_color="transparent")
        
        # Update primary and variations frames
        if hasattr(self.main_window, 'primary_frame') and self.main_window.primary_frame:
            self.main_window.primary_frame.configure(fg_color=theme.bg_secondary)
        if hasattr(self.main_window, 'variations_frame') and self.main_window.variations_frame:
            self.main_window.variations_frame.configure(fg_color=theme.bg_secondary)
        
        # Update palette panel and its children recursively
        if hasattr(self.main_window, 'palette_frame') and self.main_window.palette_frame:
            self.main_window.palette_frame.configure(fg_color=theme.bg_primary)
            self._apply_theme_to_children(self.main_window.palette_frame, theme)
        
        # Update color wheel canvas backgrounds
        if hasattr(self.main_window, 'color_wheel') and self.main_window.color_wheel:
            self.main_window.color_wheel.update_theme(theme)
        
        # Update palette dropdown
        if hasattr(self.main_window, 'palette_menu'):
            try:
                self.main_window.palette_menu.configure(
                    fg_color=theme.button_normal,
                    text_color=theme.text_primary
                )
            except:
                pass
        
        # Update layer panel if it exists (comprehensive)
        if hasattr(self.main_window, 'layer_panel'):
            try:
                # Layer panel now uses parent frame directly, no background needed
                # Recursively update all children of the layer panel
                self._apply_theme_to_children(self.main_window.layer_panel.layer_frame, theme)
            except Exception as e:
                print(f"[DEBUG] Layer panel theme error: {e}")
        
        # Update timeline panel if it exists (comprehensive)
        if hasattr(self.main_window, 'timeline_panel'):
            try:
                # Timeline panel now uses parent frame directly, no background needed
                # Recursively update all children of the timeline panel
                self._apply_theme_to_children(self.main_window.timeline_panel.timeline_frame, theme)
                
                # Update frame list area specifically (regular frame, no scrollbar colors)
                if hasattr(self.main_window.timeline_panel, 'frame_list_frame'):
                    self.main_window.timeline_panel.frame_list_frame.configure(
                        fg_color=theme.bg_tertiary
                    )
            except Exception as e:
                print(f"[DEBUG] Timeline panel theme error: {e}")
        
        # Update undo/redo buttons if they exist
        if hasattr(self.main_window, 'undo_button') and hasattr(self.main_window, 'redo_button'):
            self.main_window.undo_button.configure(
                fg_color=theme.button_normal,
                hover_color=theme.button_hover,
                text_color=theme.text_primary
            )
            self.main_window.redo_button.configure(
                fg_color=theme.button_normal,
                hover_color=theme.button_hover,
                text_color=theme.text_primary
            )
        
        # Update grid overlay button if it exists
        if hasattr(self.main_window, 'grid_overlay_button'):
            if self.main_window.grid_control_mgr.grid_overlay:
                self.main_window.grid_overlay_button.configure(fg_color="green", text_color=theme.text_primary)
            else:
                self.main_window.grid_overlay_button.configure(fg_color=theme.button_normal, text_color=theme.text_primary)
        
        # Update grid mode button if it exists
        if hasattr(self.main_window, 'grid_control_mgr') and hasattr(self.main_window.grid_control_mgr, 'grid_mode_button'):
            self.main_window.grid_control_mgr.update_grid_mode_button()
        
        # Update background mode button if it exists
        if hasattr(self.main_window, 'background_control_mgr') and hasattr(self.main_window.background_control_mgr, 'background_mode_button'):
            self.main_window.background_control_mgr.update_background_mode_button()
        
        # Update canvas elements (grid, borders) without full redraw
        self._update_theme_canvas_elements(theme)
        
        # Update status bar and HUD theme
        if hasattr(self.main_window, 'status_bar'):
            self.main_window.status_bar.apply_theme(theme)
        if hasattr(self.main_window, 'canvas_hud'):
            self.main_window.canvas_hud.apply_theme(theme)
        
        print(f"[OK] Theme '{theme.name}' applied (instant mode)")
    
    def _apply_theme_to_children(self, parent_widget, theme):
        """Recursively apply theme to all children widgets"""
        for widget in parent_widget.winfo_children():
            try:
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color=theme.text_primary)
                elif isinstance(widget, ctk.CTkScrollableFrame):
                    # Style scrollable frames (like custom colors)
                    widget.configure(
                        fg_color=theme.bg_tertiary,
                        scrollbar_button_color=theme.scrollbar_button_color,
                        scrollbar_button_hover_color=theme.scrollbar_button_hover_color
                    )
                    # Recursively update children
                    self._apply_theme_to_children(widget, theme)
                elif isinstance(widget, ctk.CTkCanvas):
                    # Skip canvas widgets - they should be handled by their specific components
                    # (like color wheel, which has its own update_theme method)
                    pass
                elif isinstance(widget, ctk.CTkFrame):
                    # Check if this is a color preview frame (don't override its color)
                    try:
                        widget_width = widget.cget("width")
                        widget_height = widget.cget("height")
                        
                        # If it's a color preview frame (100x100), skip theme application
                        if widget_width == 100 and widget_height == 100:
                            # This is likely a color preview frame, don't override its color
                            pass
                        else:
                            # Regular frame, apply theme
                            current_fg = widget.cget("fg_color")
                            if current_fg == "transparent":
                                widget.configure(fg_color="transparent")
                            else:
                                widget.configure(fg_color=theme.bg_primary)
                    except:
                        widget.configure(fg_color=theme.bg_primary)
                    # Recursively update children
                    self._apply_theme_to_children(widget, theme)
                elif isinstance(widget, ctk.CTkRadioButton):
                    widget.configure(text_color=theme.text_primary)
                elif isinstance(widget, ctk.CTkButton):
                    # Check if this is a color button (has no text and specific size)
                    try:
                        button_text = widget.cget("text")
                        button_width = widget.cget("width")
                        button_height = widget.cget("height")
                        
                        # If it's a color button (no text, 30x30 size), don't override its color
                        if button_text == "" and button_width == 30 and button_height == 30:
                            # This is a color button, skip theme application
                            pass
                        else:
                            # Regular button, apply theme
                            widget.configure(
                                fg_color=theme.button_normal,
                                hover_color=theme.button_hover,
                                text_color=theme.text_primary
                            )
                    except:
                        # If we can't determine, apply theme to be safe
                        widget.configure(
                            fg_color=theme.button_normal,
                            hover_color=theme.button_hover,
                            text_color=theme.text_primary
                        )
            except Exception as e:
                # Skip widgets that don't support these properties
                pass
    
    def _update_theme_canvas_elements(self, theme):
        """Update only theme-dependent canvas elements (grid, borders) without full redraw"""
        width = self.main_window.drawing_canvas.winfo_width()
        height = self.main_window.drawing_canvas.winfo_height()
        
        if width > 1 and height > 1:
            # Calculate canvas display size
            canvas_pixel_width = self.main_window.canvas.width * self.main_window.canvas.zoom
            canvas_pixel_height = self.main_window.canvas.height * self.main_window.canvas.zoom
            
            # Calculate offsets
            x_offset = (width - canvas_pixel_width) // 2
            y_offset = (height - canvas_pixel_height) // 2
            x_offset += self.main_window.pan_offset_x * self.main_window.canvas.zoom
            y_offset += self.main_window.pan_offset_y * self.main_window.canvas.zoom
            
            # Only redraw grid and border (not pixels!)
            # Delete old theme-dependent elements
            self.main_window.drawing_canvas.delete("grid")
            self.main_window.drawing_canvas.delete("border")
            
            # Draw grid if enabled (with new theme color)
            if self.main_window.canvas.show_grid:
                for x in range(self.main_window.canvas.width + 1):
                    screen_x = x_offset + (x * self.main_window.canvas.zoom)
                    self.main_window.drawing_canvas.create_line(
                        screen_x, y_offset,
                        screen_x, y_offset + canvas_pixel_height,
                        fill=theme.grid_color, tags="grid"
                    )
                for y in range(self.main_window.canvas.height + 1):
                    screen_y = y_offset + (y * self.main_window.canvas.zoom)
                    self.main_window.drawing_canvas.create_line(
                        x_offset, screen_y,
                        x_offset + canvas_pixel_width, screen_y,
                        fill=theme.grid_color, tags="grid"
                    )
            
            # Draw border with new theme color
            self.main_window.drawing_canvas.create_rectangle(
                x_offset, y_offset,
                x_offset + canvas_pixel_width, y_offset + canvas_pixel_height,
                outline=theme.canvas_border, width=2, tags="border"
            )
            
            # Bring pixels and selection to front (keep existing rendering)
            self.main_window.drawing_canvas.tag_raise("pixels")
            self.main_window.drawing_canvas.tag_raise("selection")
            
            # Raise grid above pixels if overlay mode is enabled
            if self.main_window.grid_control_mgr.grid_overlay and self.main_window.canvas.show_grid:
                self.main_window.drawing_canvas.tag_raise("grid")
            
            # Update scrollbar colors for theme change
            if hasattr(self.main_window, 'canvas_scrollbar'):
                self.main_window.canvas_scrollbar.update_theme()