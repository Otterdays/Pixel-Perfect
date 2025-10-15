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
        
        # Scrollbar colors
        self.scrollbar_button_color = "#3b3b3b"
        self.scrollbar_button_hover_color = "#505050"
        self.scrollbar_track_color = "#2b2b2b"

class BasicGreyTheme(Theme):
    """Default dark grey theme with darker canvas and buttons"""
    def __init__(self):
        super().__init__("Basic Grey")
        # Main window colors - darker for better contrast
        self.bg_primary = "#1a1a1a"      # Darker primary background
        self.bg_secondary = "#2b2b2b"    # Dark secondary background
        self.bg_tertiary = "#3a3a3a"     # Tertiary background
        
        # Canvas colors - much darker like in the "broken" state
        self.canvas_bg = "#0d1117"       # Very dark canvas (like GitHub dark)
        self.canvas_border = "#000000"   # Black border
        self.grid_color = "#21262d"      # Dark grid lines
        
        # Button colors - darker theme with transparent-like appearance
        self.button_normal = "#2b2b2b"   # Match bg_secondary for floating appearance
        self.button_hover = "#3a3a3a"    # Slightly lighter on hover
        self.button_active = "#1f6aa5"   # Keep blue active color
        
        # Tool colors - match backgrounds for floating appearance
        self.tool_selected = "#1f6aa5"   # Blue for selected tools
        self.tool_unselected = "#2b2b2b" # Match bg_secondary for invisible background
        
        # Scrollbar colors - darker theme (more distinct from blue)
        self.scrollbar_button_color = "#404040"   # Medium grey - clearly visible
        self.scrollbar_button_hover_color = "#505050"  # Lighter grey on hover
        self.scrollbar_track_color = "#2a2a2a"    # Dark grey track

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
        
        # Scrollbar colors - light theme
        self.scrollbar_button_color = "#e0e7ff"
        self.scrollbar_button_hover_color = "#c7d2fe"
        self.scrollbar_track_color = "#f5f5f5"

class AmericanTheme(Theme):
    """Patriotic American theme with red, white, and blue colors"""
    def __init__(self):
        super().__init__("American")
        # Main window colors - clean white with red/blue accents
        self.bg_primary = "#f8fafc"      # Light grey-white (stars background)
        self.bg_secondary = "#ffffff"    # Pure white (flag white)
        self.bg_tertiary = "#f1f5f9"     # Soft blue-grey (subtle accent)
        
        # Text colors - navy blue for readability
        self.text_primary = "#1e293b"    # Navy blue text
        self.text_secondary = "#475569"  # Medium blue-grey
        self.text_disabled = "#94a3b8"   # Light blue-grey
        
        # Button colors - patriotic red, white, and blue
        self.button_normal = "#fef2f2"   # Light red background
        self.button_hover = "#fee2e2"    # Medium red hover
        self.button_active = "#dc2626"   # Bold red active (American flag red)
        
        # Border colors
        self.border_normal = "#e2e8f0"   # Light blue-grey
        self.border_focus = "#1d4ed8"    # Bold blue focus (American flag blue)
        
        # Canvas colors
        self.canvas_bg = "#ffffff"       # Pure white canvas
        self.canvas_border = "#e2e8f0"   # Light blue border
        self.grid_color = "#f1f5f9"      # Very light blue grid
        
        # Tool colors - red and blue patriotic scheme
        self.tool_selected = "#1d4ed8"   # Bold blue for selected tools
        self.tool_unselected = "#fef2f2" # Light red for unselected tools
        
        # Selection colors - patriotic theme
        self.selection_outline = "#dc2626"  # Red outline (American flag red)
        self.selection_handle = "#1d4ed8"   # Blue handle (American flag blue)
        self.selection_edge = "#f59e0b"     # Gold accent
        
        # Scrollbar colors - patriotic theme
        self.scrollbar_button_color = "#fef2f2"   # Light red background
        self.scrollbar_button_hover_color = "#fee2e2"  # Medium red hover
        self.scrollbar_track_color = "#f8fafc"    # Light grey-white

class GeminiTheme(Theme):
    """A polished, modern dark theme with blue and purple accents."""
    def __init__(self):
        super().__init__("Gemini")
        # A deep, dark blue-grey for the main background
        self.bg_primary = "#1d2025" 
        # A slightly lighter grey for secondary panels
        self.bg_secondary = "#282c34"
        # A subtle grey for tertiary elements
        self.bg_tertiary = "#3a4049"
        
        # Text colors with good contrast
        self.text_primary = "#e6e6e6"
        self.text_secondary = "#b0b0b0"
        self.text_disabled = "#6a6a6a"
        
        # Buttons that are dark but pop with a Gemini blue on hover/selection
        self.button_normal = "#282c34"
        self.button_hover = "#3a4049"
        self.button_active = "#4285F4"  # Google Blue
        
        # Borders
        self.border_normal = "#3a4049"
        self.border_focus = "#8ab4f8" # Lighter Google Blue for focus
        
        # A neutral, dark canvas that doesn't distract
        self.canvas_bg = "#212121"
        self.canvas_border = "#4a4a4a"
        self.grid_color = "#303030"
        
        # Tools
        self.tool_selected = "#4285F4"
        self.tool_unselected = "#282c34"
        
        # Selection highlights
        self.selection_outline = "#8ab4f8"
        self.selection_handle = "#fdd835" # A bright yellow for contrast
        self.selection_edge = "#4285F4"
        
        # Scrollbar colors - Gemini theme (toned down)
        self.scrollbar_button_color = "#3a4049"  # More subtle grey
        self.scrollbar_button_hover_color = "#4a5159"  # Slightly lighter
        self.scrollbar_track_color = "#2d3239"  # Toned down track

class ThemeManager:
    """Manages application themes"""
    
    def __init__(self):
        self.themes: Dict[str, Theme] = {
            "Basic Grey": BasicGreyTheme(),
            "Gemini": GeminiTheme(),
            "Angelic": AngelicTheme(),
            "American": AmericanTheme()
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
        # Basic Grey is dark, Angelic and American are light
        if self.current_theme.name in ["Angelic", "American"]:
            return "light"
        return "dark"

