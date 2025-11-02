"""
Saved Colors View for Pixel Perfect
Displays user-saved colors with import/export functionality
"""

import customtkinter as ctk
from tkinter import filedialog
from typing import Callable, List, Optional


class SavedView:
    """Manages the saved colors view"""
    
    def __init__(self, parent_frame: ctk.CTkFrame, saved_colors, palette, canvas,
                 color_wheel, view_mode_var, on_update_display: Callable):
        """
        Initialize the saved colors view
        
        Args:
            parent_frame: Parent frame to pack widgets into
            saved_colors: SavedColorsManager instance
            palette: ColorPalette instance
            canvas: Canvas instance
            color_wheel: ColorWheel instance
            view_mode_var: StringVar for current view mode
            on_update_display: Callback to update pixel display
        """
        self.parent_frame = parent_frame
        self.saved_colors = saved_colors
        self.palette = palette
        self.canvas = canvas
        self.color_wheel = color_wheel
        self.view_mode_var = view_mode_var
        self.on_update_display = on_update_display
        
        # UI components
        self.saved_color_buttons: List[ctk.CTkButton] = []
        self.view_created = False
        
        # View references (set later by main window)
        self.primary_view = None
        self.main_window = None
        
        # Store the currently selected Saved color (separate from main palette)
        self.current_saved_color = None
    
    def create(self):
        """Create the saved colors view"""
        # Check if view already exists - just update buttons instead of recreating
        if self.view_created:
            self.update_buttons()
            return
        
        # Clear existing widgets
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Title
        title_label = ctk.CTkLabel(
            self.parent_frame,
            text="Saved Colors",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.pack(pady=(0, 2))
        
        # Instructions
        info_label = ctk.CTkLabel(
            self.parent_frame,
            text="Click empty slot to save current color",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        info_label.pack(pady=(0, 5))
        
        # Grid for saved colors
        grid_frame = ctk.CTkFrame(self.parent_frame)
        grid_frame.pack(padx=10, pady=(0, 5))
        
        # Configure grid - 4 columns x 6 rows = 24 slots
        for col in range(4):
            grid_frame.grid_columnconfigure(col, weight=1)
        
        # Create 24 color slots (create once, update later)
        self.saved_color_buttons.clear()
        for idx in range(24):
            row = idx // 4
            col = idx % 4
            
            # Create button (will be configured in update_buttons)
            btn = ctk.CTkButton(
                grid_frame,
                text="+",
                width=50,
                height=50,
                fg_color="transparent",
                hover_color="#3a3a3a",
                border_width=2,
                border_color="gray",
                corner_radius=3
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            self.saved_color_buttons.append(btn)
        
        # Export button
        export_btn = ctk.CTkButton(
            self.parent_frame,
            text="Export Saved Colors",
            height=32,
            fg_color="#1f6aa5",
            hover_color="#1f5a95",
            command=self._export_saved_colors
        )
        export_btn.pack(fill="x", padx=10, pady=(5, 2))
        
        # Import button
        import_btn = ctk.CTkButton(
            self.parent_frame,
            text="Import Saved Colors",
            height=32,
            fg_color="#4a4a4a",
            hover_color="#5a5a5a",
            command=self._import_saved_colors
        )
        import_btn.pack(fill="x", padx=10, pady=2)
        
        # Clear all button
        clear_btn = ctk.CTkButton(
            self.parent_frame,
            text="Clear All Slots",
            height=32,
            fg_color="red",
            hover_color="#cc0000",
            command=self._clear_all_saved_colors
        )
        clear_btn.pack(fill="x", padx=10, pady=2)
        
        # Mark view as created
        self.view_created = True
        
        # Now update button states
        self.update_buttons()
    
    def update_buttons(self):
        """Update saved color button states without recreating them (FAST)"""
        if not self.saved_color_buttons:
            return
        
        for idx, btn in enumerate(self.saved_color_buttons):
            # Check if button still exists
            try:
                if not btn.winfo_exists():
                    continue
            except:
                continue
            
            saved_color = self.saved_colors.get_color(idx)
            
            try:
                if saved_color:
                    # Slot has a color - configure as filled
                    r, g, b, a = saved_color
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    btn.configure(
                        text="",
                        fg_color=hex_color,
                        hover_color=hex_color,
                        command=lambda i=idx: self._on_saved_color_click(i)
                    )
                else:
                    # Empty slot - configure as empty
                    btn.configure(
                        text="+",
                        fg_color="transparent",
                        hover_color="#3a3a3a",
                        command=lambda i=idx: self._on_saved_slot_click(i)
                    )
            except:
                # Widget was destroyed, skip it
                pass
    
    def _on_saved_slot_click(self, slot_index: int):
        """Handle click on empty saved color slot - save current color"""
        # Get current color from appropriate source using same logic as main window
        current_color = self._get_current_color()
        
        # Save to slot
        self.saved_colors.set_color(slot_index, current_color)
        
        # Automatically select the saved color as the current color for painting
        # This ensures the brush uses the color you just saved
        self.current_saved_color = current_color
        
        # Fast refresh - just update button states
        self.update_buttons()
        
        # Update display to show the selected color
        if self.on_update_display:
            self.on_update_display()
        
        print(f"[SAVED] Color {current_color} saved to slot {slot_index} and selected for painting")
    
    def _get_current_color(self):
        """Get current color from the actual source view (ignoring saved view mode)"""
        # Always get the current color from the main window's get_source_color method
        # This ensures we get the correct color from Primary/Wheel views even when in Saved view
        if hasattr(self, 'main_window') and self.main_window:
            return self.main_window.get_source_color()
        
        # Fallback logic if main_window reference is not available
        # Check Primary view first (most recent selection)
        if (hasattr(self, 'primary_view') and self.primary_view):
            primary_color = self.primary_view.get_current_color()
            if primary_color:
                return primary_color
        
        # Check Wheel view
        if (self.color_wheel):
            rgb_color = self.color_wheel.get_color()
            return (rgb_color[0], rgb_color[1], rgb_color[2], 255)
        
        # Fallback to palette
        return self.palette.get_primary_color()
    
    def _on_saved_color_click(self, slot_index: int):
        """Handle click on filled saved color slot - load color"""
        saved_color = self.saved_colors.get_color(slot_index)
        if saved_color:
            # Store the selected color in the Saved view (separate from main palette)
            # This prevents color bleeding to grid when just selecting colors
            self.current_saved_color = saved_color
            
            # Update display to show the selected color
            if self.on_update_display:
                self.on_update_display()
            print(f"[SAVED] Loaded color {saved_color} from slot {slot_index}")
    
    def get_current_color(self):
        """Get the currently selected Saved color"""
        return self.current_saved_color
    
    def _export_saved_colors(self):
        """Export saved colors to a file"""
        filepath = filedialog.asksaveasfilename(
            parent=self.parent_frame.winfo_toplevel(),  # Set parent to keep dialog on top
            title="Export Saved Colors",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            if self.saved_colors.export_to_file(filepath):
                print(f"[EXPORT] Saved colors exported to: {filepath}")
            else:
                print("[EXPORT] Failed to export saved colors")
    
    def _import_saved_colors(self):
        """Import saved colors from a file"""
        filepath = filedialog.askopenfilename(
            parent=self.parent_frame.winfo_toplevel(),  # Set parent to keep dialog on top
            title="Import Saved Colors",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            if self.saved_colors.import_from_file(filepath):
                self.update_buttons()  # Fast refresh
                print(f"[IMPORT] Saved colors imported from: {filepath}")
            else:
                print("[IMPORT] Failed to import saved colors")
    
    def _clear_all_saved_colors(self):
        """Clear all saved color slots with confirmation"""
        # Create custom confirmation dialog
        dialog = ctk.CTkToplevel(self.parent_frame.winfo_toplevel())
        dialog.title("Clear All Slots")
        dialog.geometry("450x220")
        dialog.resizable(False, False)
        dialog.transient(self.parent_frame.winfo_toplevel())
        dialog.grab_set()
        
        # Center the dialog on the main window
        root = self.parent_frame.winfo_toplevel()
        dialog.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() // 2) - (450 // 2)
        y = root.winfo_y() + (root.winfo_height() // 2) - (220 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Icon and title frame
        header_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        header_frame.pack(pady=20, padx=20, fill="x")
        
        # Large colorful icon (🎨 emoji)
        icon_label = ctk.CTkLabel(
            header_frame,
            text="🎨",
            font=ctk.CTkFont(size=48)
        )
        icon_label.pack(side="left", padx=(10, 20))
        
        # Title text
        title_label = ctk.CTkLabel(
            header_frame,
            text="Clear All Slots",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", anchor="w")
        
        # Warning message
        message_label = ctk.CTkLabel(
            dialog,
            text="Are you sure you want to clear all saved colors?\nThis cannot be undone.",
            font=ctk.CTkFont(size=14),
            text_color="#e0e0e0"
        )
        message_label.pack(pady=(0, 25), padx=20)
        
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
        
        # No button (cancel)
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
        root.wait_window(dialog)
        
        # Process result
        if result[0]:
            self.saved_colors.clear_all()
            self.update_buttons()  # Fast refresh
    
    def apply_theme(self, theme):
        """Apply theme to saved view"""
        # Saved color buttons maintain their actual colors
        pass

