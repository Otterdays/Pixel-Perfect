"""
Theme Manager - Centralized theme system for Pixel Perfect
Manages color schemes and applies them to UI elements
"""
import customtkinter as ctk
from typing import Dict, Tuple

class Theme:
    """Base theme configuration"""
    def __init__(self, name: str):
        self.name = name
        # Main window colors
        self.bg_primary = "#2b2b2b"
        self.bg_secondary = "#1e1e1e"
        self.bg_tertiary = "#363636"
        
        # Text colors
        self.text_primary = "#ffffff"
        self.text_secondary = "#d4d4d4"
        self.text_disabled = "#808080"
        
        # Button colors
        self.button_normal = "#3b3b3b"
        self.button_hover = "#505050"
        self.button_active = "#1f6aa5"
        
        # Border colors
        self.border_normal = "#4a4a4a"
        self.border_focus = "#1f6aa5"
        
        # Canvas colors
        self.canvas_bg = "#2b2b2b"
        self.canvas_border = "#000000"
        self.grid_color = "#404040"
        
        # Tool colors
        self.tool_selected = "#1f6aa5"
        self.tool_unselected = "#3b3b3b"
        
        # Selection colors
        self.selection_outline = "#ffffff"
        self.selection_handle = "#ffff00"
        self.selection_edge = "#ffa500"

class BasicGreyTheme(Theme):
    """Default dark grey theme"""
    def __init__(self):
        super().__init__("Basic Grey")
        # Already set to default dark colors in base Theme class
        # Adjust tertiary for better contrast with custom colors grid
        self.bg_tertiary = "#3a3a3a"

class AngelicTheme(Theme):
    """Light, angelic theme with soft colors"""
    def __init__(self):
        super().__init__("Angelic")
        # Main window colors - light and airy
        self.bg_primary = "#f5f5f5"
        self.bg_secondary = "#ffffff"
        self.bg_tertiary = "#dfe6f0"  # Soft blue-grey for custom colors grid
        
        # Text colors
        self.text_primary = "#1a1a1a"
        self.text_secondary = "#4a4a4a"
        self.text_disabled = "#a0a0a0"
        
        # Button colors - soft blues and whites
        self.button_normal = "#e0e7ff"
        self.button_hover = "#c7d2fe"
        self.button_active = "#818cf8"
        
        # Border colors
        self.border_normal = "#cbd5e1"
        self.border_focus = "#818cf8"
        
        # Canvas colors
        self.canvas_bg = "#fafafa"
        self.canvas_border = "#cbd5e1"
        self.grid_color = "#e2e8f0"
        
        # Tool colors
        self.tool_selected = "#818cf8"
        self.tool_unselected = "#e0e7ff"
        
        # Selection colors
        self.selection_outline = "#4338ca"
        self.selection_handle = "#fbbf24"
        self.selection_edge = "#f97316"

class ThemeManager:
    """Manages application themes"""
    
    def __init__(self):
        self.themes: Dict[str, Theme] = {
            "Basic Grey": BasicGreyTheme(),
            "Angelic": AngelicTheme()
        }
        self.current_theme = self.themes["Basic Grey"]
        self.on_theme_changed = None  # Callback when theme changes
        
    def get_theme(self, name: str) -> Theme:
        """Get theme by name"""
        return self.themes.get(name, self.current_theme)
    
    def set_theme(self, name: str):
        """Set active theme"""
        if name in self.themes:
            self.current_theme = self.themes[name]
            if self.on_theme_changed:
                self.on_theme_changed(self.current_theme)
    
    def get_theme_names(self):
        """Get list of available theme names"""
        return list(self.themes.keys())
    
    def get_current_theme(self) -> Theme:
        """Get current active theme"""
        return self.current_theme
    
    def apply_to_frame(self, frame: ctk.CTkFrame):
        """Apply theme colors to a frame"""
        frame.configure(fg_color=self.current_theme.bg_primary)
    
    def apply_to_button(self, button: ctk.CTkButton, selected: bool = False):
        """Apply theme colors to a button"""
        if selected:
            button.configure(
                fg_color=self.current_theme.tool_selected,
                hover_color=self.current_theme.button_hover
            )
        else:
            button.configure(
                fg_color=self.current_theme.tool_unselected,
                hover_color=self.current_theme.button_hover
            )
    
    def apply_to_label(self, label: ctk.CTkLabel):
        """Apply theme colors to a label"""
        label.configure(text_color=self.current_theme.text_primary)
    
    def get_ctk_theme_mode(self) -> str:
        """Get CustomTkinter appearance mode based on theme"""
        # Basic Grey is dark, Angelic is light
        if self.current_theme.name == "Angelic":
            return "light"
        return "dark"

