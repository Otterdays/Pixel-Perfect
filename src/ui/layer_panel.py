"""
Layer panel UI for Pixel Perfect
Manages layer display and interactions
"""

import customtkinter as ctk
from typing import List, Callable, Optional
from core.layer_manager import LayerManager, Layer

class LayerPanel:
    """Layer management UI panel"""
    
    def __init__(self, parent_frame: ctk.CTkFrame, layer_manager: LayerManager):
        self.parent_frame = parent_frame
        self.layer_manager = layer_manager
        self.on_layer_changed: Optional[Callable] = None
        
        # UI components
        self.layer_frame = None
        self.layer_buttons = {}
        self._drag_start_index = None
        self._drag_indicator = None
        
        self._create_ui()
        self._update_display()
    
    def _create_ui(self):
        """Create the layer panel UI"""
        # Use the parent frame directly, no container frame
        self.layer_frame = self.parent_frame
        
        # Header with controls
        header_frame = ctk.CTkFrame(self.layer_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(15, 5))
        
        # Title removed - LayerAnimationManager already creates the title
        
        # Add layer button - centered since no title
        self.add_layer_btn = ctk.CTkButton(
            header_frame, 
            text="+", 
            width=30, 
            height=30,
            command=self._add_layer
        )
        self.add_layer_btn.pack(side="right", padx=(5, 0))
        
        # Layer list frame - transparent container for layer entries
        self.list_frame = ctk.CTkFrame(self.layer_frame, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Layer controls frame
        controls_frame = ctk.CTkFrame(self.layer_frame, fg_color="transparent")
        controls_frame.pack(fill="x", padx=10, pady=(5, 15))
        
        # Layer control buttons
        button_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        
        self.duplicate_btn = ctk.CTkButton(
            button_frame,
            text="Duplicate",
            width=80,
            height=28,
            font=ctk.CTkFont(size=12),
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            command=self._duplicate_layer
        )
        self.duplicate_btn.pack(side="left", padx=(0, 3))
        
        self.delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete",
            width=70,
            height=28,
            font=ctk.CTkFont(size=12),
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            command=self._delete_layer
        )
        self.delete_btn.pack(side="left", padx=(0, 3))
        
        self.merge_btn = ctk.CTkButton(
            button_frame,
            text="Merge Down",
            width=85,
            height=28,
            font=ctk.CTkFont(size=12),
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            command=self._merge_layer
        )
        self.merge_btn.pack(side="left")
        
    
    def _update_display(self):
        """Update the layer display"""
        # Clear existing layer buttons
        for layer_row in self.layer_buttons.values():
            if layer_row and layer_row.winfo_exists():
                layer_row.destroy()
        
        self.layer_buttons.clear()
        
        # Create layer buttons (from top to bottom, so reverse order)
        layers = self.layer_manager.layers
        for i in range(len(layers) - 1, -1, -1):
            layer = layers[i]
            self._create_layer_button(i, layer)
        
        # Update button states
        self._update_button_states()
    
    def _create_layer_button(self, index: int, layer: Layer):
        """Create a button for a specific layer"""
        # Create a horizontal frame for the layer row
        layer_row = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        layer_row.pack(fill="x", pady=1)
        
        # Visibility toggle
        visibility_var = ctk.BooleanVar(value=layer.visible)
        def on_visibility_change():
            """Handle visibility checkbox change"""
            self._toggle_visibility(index, visibility_var.get())
        
        visibility_cb = ctk.CTkCheckBox(
            layer_row,
            text="",
            width=18,
            height=18,
            variable=visibility_var,
            command=on_visibility_change
        )
        visibility_cb.pack(side="left", padx=(5, 0))
        
        # Layer name (clickable) - make it transparent
        layer_btn = ctk.CTkButton(
            layer_row,
            text=layer.name,
            height=28,
            anchor="w",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            hover_color="#3a3a3a",
            command=lambda: self._select_layer(index)
        )
        layer_btn.pack(side="left", fill="x", expand=True, padx=(5, 5))
        
        # Enable double-click to rename
        layer_btn.bind("<Double-Button-1>", lambda e, idx=index: self._start_rename(idx))
        
        # Enable drag-and-drop reorder
        layer_btn.bind("<Button-1>", lambda e, idx=index: self._on_drag_start(e, idx))
        layer_btn.bind("<B1-Motion>", lambda e, idx=index: self._on_drag_motion(e, idx))
        layer_btn.bind("<ButtonRelease-1>", lambda e, idx=index: self._on_drag_end(e, idx))
        
        # Active indicator
        if index == self.layer_manager.active_layer_index:
            layer_btn.configure(fg_color="blue")
        else:
            layer_btn.configure(fg_color="transparent")
        
        # Opacity slider (only show for active layer)
        if index == self.layer_manager.active_layer_index:
            opacity_frame = ctk.CTkFrame(layer_row, fg_color="transparent")
            opacity_frame.pack(side="right", padx=(0, 5))
            
            opacity_label = ctk.CTkLabel(opacity_frame, text="Op:", width=25)
            opacity_label.pack(side="left")
            
            opacity_var = ctk.DoubleVar(value=layer.opacity)
            
            def on_opacity_change(value, idx=index):
                self._set_layer_opacity(idx, float(value))
            
            opacity_slider = ctk.CTkSlider(
                opacity_frame,
                from_=0.0,
                to=1.0,
                variable=opacity_var,
                width=60,
                height=16,
                command=on_opacity_change
            )
            opacity_slider.pack(side="left")
        
        # Lock toggle button
        lock_var = ctk.BooleanVar(value=layer.locked)

        def on_lock_toggle(idx=index):
            new_state = not self.layer_manager.layers[idx].locked
            self._toggle_layer_lock(idx, new_state)

        lock_btn = ctk.CTkButton(
            layer_row,
            text="🔒" if layer.locked else "🔓",
            width=28,
            height=28,
            fg_color="transparent" if not layer.locked else "#3a3a3a",
            hover_color="#4a4a4a",
            command=on_lock_toggle
        )
        lock_btn.pack(side="right", padx=(0, 5))
        
        # Store button reference
        self.layer_buttons[index] = layer_row
    
    def _update_button_states(self):
        """Update the state of control buttons"""
        layer_count = self.layer_manager.get_layer_count()
        active_index = self.layer_manager.active_layer_index
        
        # Enable/disable buttons based on current state
        self.delete_btn.configure(state="normal" if layer_count > 1 else "disabled")
        self.duplicate_btn.configure(state="normal" if layer_count < 10 else "disabled")
        self.merge_btn.configure(state="normal" if active_index > 0 else "disabled")
    
    def _select_layer(self, index: int):
        """Select a layer"""
        # Always set the clicked layer as active (no deselect behavior)
        self.layer_manager.set_active_layer(index)
        
        self._update_display()
        
        if self.on_layer_changed:
            self.on_layer_changed()
    
    def _toggle_visibility(self, index: int, visible: bool):
        """Toggle layer visibility"""
        self.layer_manager.set_layer_visibility(index, visible)
        
        if self.on_layer_changed:
            self.on_layer_changed()
    
    def _set_layer_opacity(self, index: int, opacity: float):
        """Set layer opacity"""
        self.layer_manager.set_layer_opacity(index, opacity)
        
        if self.on_layer_changed:
            self.on_layer_changed()
    
    def _toggle_layer_lock(self, index: int, locked: bool):
        """Toggle layer lock state"""
        self.layer_manager.set_layer_locked(index, locked)
        self._update_display()
    
    def _start_rename(self, index: int):
        """Start renaming a layer"""
        layer = self.layer_manager.layers[index]
        
        # Create rename dialog
        dialog = ctk.CTkInputDialog(
            text=f"Enter new name for '{layer.name}':",
            title="Rename Layer"
        )
        new_name = dialog.get_input()
        
        if new_name and new_name.strip():
            self.layer_manager.set_layer_name(index, new_name.strip())
            self._update_display()
    
    def _on_drag_start(self, event, index: int):
        """Start dragging a layer"""
        self._drag_start_index = index
        # Store initial position to detect if it's a drag or just a click
        self._drag_start_y = event.y_root

    def _on_drag_motion(self, event, index: int):
        """Handle drag motion"""
        # Visual feedback could be added here
        pass

    def _on_drag_end(self, event, index: int):
        """End drag and reorder if needed"""
        if self._drag_start_index is None:
            return
        
        # Check if this was actually a drag (moved more than a few pixels)
        drag_threshold = 5
        if hasattr(self, '_drag_start_y'):
            if abs(event.y_root - self._drag_start_y) < drag_threshold:
                # It was just a click, select the layer
                self._select_layer(index)
                self._drag_start_index = None
                return
        
        # Calculate drop target based on y position
        widget = event.widget
        y = event.y_root
        
        # Find which layer row we're over
        target_index = None
        for idx, layer_row in self.layer_buttons.items():
            if layer_row and layer_row.winfo_exists():
                row_y = layer_row.winfo_rooty()
                row_height = layer_row.winfo_height()
                if row_y <= y <= row_y + row_height:
                    target_index = idx
                    break
        
        # Perform move if target is different
        if target_index is not None and target_index != self._drag_start_index:
            # Note: layer indices are reversed in display (top=highest index)
            if self.layer_manager.move_layer(self._drag_start_index, target_index):
                self._update_display()
                if self.on_layer_changed:
                    self.on_layer_changed()
        
        self._drag_start_index = None
    
    def _add_layer(self):
        """Add a new layer"""
        if self.layer_manager.add_layer():
            self._update_display()
            
            if self.on_layer_changed:
                self.on_layer_changed()
    
    def _delete_layer(self):
        """Delete the active layer"""
        active_index = self.layer_manager.active_layer_index
        if self.layer_manager.remove_layer(active_index):
            self._update_display()
            
            if self.on_layer_changed:
                self.on_layer_changed()
    
    def _duplicate_layer(self):
        """Duplicate the active layer"""
        active_index = self.layer_manager.active_layer_index
        if self.layer_manager.duplicate_layer(active_index):
            self._update_display()
            
            if self.on_layer_changed:
                self.on_layer_changed()
    
    def _merge_layer(self):
        """Merge active layer with layer below"""
        active_index = self.layer_manager.active_layer_index
        if active_index > 0:
            target_index = active_index - 1
            if self.layer_manager.merge_layers(target_index, active_index):
                self._update_display()
                
                if self.on_layer_changed:
                    self.on_layer_changed()
    
    def refresh(self):
        """Refresh the layer display"""
        self._update_display()
    
