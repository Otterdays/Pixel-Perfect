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
        self.layer_buttons = []
        
        self._create_ui()
        self._update_display()
    
    def _create_ui(self):
        """Create the layer panel UI"""
        # Main layer frame
        self.layer_frame = ctk.CTkFrame(self.parent_frame)
        self.layer_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header with controls
        header_frame = ctk.CTkFrame(self.layer_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Title
        title_label = ctk.CTkLabel(header_frame, text="Layers", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(side="left")
        
        # Add layer button
        self.add_layer_btn = ctk.CTkButton(
            header_frame, 
            text="+", 
            width=30, 
            height=30,
            command=self._add_layer
        )
        self.add_layer_btn.pack(side="right", padx=(5, 0))
        
        # Layer list frame
        self.list_frame = ctk.CTkScrollableFrame(self.layer_frame)
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Layer controls frame
        controls_frame = ctk.CTkFrame(self.layer_frame)
        controls_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        # Layer control buttons
        button_frame = ctk.CTkFrame(controls_frame)
        button_frame.pack(fill="x")
        
        self.duplicate_btn = ctk.CTkButton(
            button_frame,
            text="Duplicate",
            width=80,
            command=self._duplicate_layer
        )
        self.duplicate_btn.pack(side="left", padx=(0, 5))
        
        self.delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete",
            width=80,
            command=self._delete_layer
        )
        self.delete_btn.pack(side="left", padx=(0, 5))
        
        self.merge_btn = ctk.CTkButton(
            button_frame,
            text="Merge Down",
            width=80,
            command=self._merge_layer
        )
        self.merge_btn.pack(side="left")
    
    def _update_display(self):
        """Update the layer display"""
        # Clear existing layer buttons
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
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
        layer_btn_frame = ctk.CTkFrame(self.list_frame)
        layer_btn_frame.pack(fill="x", pady=1)
        
        # Visibility toggle
        visibility_var = ctk.BooleanVar(value=layer.visible)
        visibility_cb = ctk.CTkCheckBox(
            layer_btn_frame,
            text="",
            width=20,
            variable=visibility_var,
            command=lambda: self._toggle_visibility(index, visibility_var.get())
        )
        visibility_cb.pack(side="left", padx=(5, 0))
        
        # Layer name (clickable)
        layer_btn = ctk.CTkButton(
            layer_btn_frame,
            text=layer.name,
            height=30,
            anchor="w",
            command=lambda: self._select_layer(index)
        )
        layer_btn.pack(side="left", fill="x", expand=True, padx=(5, 5))
        
        # Active indicator
        if index == self.layer_manager.active_layer_index:
            layer_btn.configure(fg_color="blue")
        else:
            layer_btn.configure(fg_color="gray")
        
        # Lock indicator
        if layer.locked:
            lock_label = ctk.CTkLabel(layer_btn_frame, text="🔒", width=20)
            lock_label.pack(side="right", padx=(0, 5))
        
        # Store button reference
        self.layer_buttons.append({
            'frame': layer_btn_frame,
            'button': layer_btn,
            'visibility': visibility_cb,
            'index': index
        })
    
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
        self.layer_manager.set_active_layer(index)
        self._update_display()
        
        if self.on_layer_changed:
            self.on_layer_changed()
    
    def _toggle_visibility(self, index: int, visible: bool):
        """Toggle layer visibility"""
        self.layer_manager.set_layer_visibility(index, visible)
        
        if self.on_layer_changed:
            self.on_layer_changed()
    
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
