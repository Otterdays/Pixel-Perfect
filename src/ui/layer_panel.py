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
        self.layer_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self.layer_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header with controls
        header_frame = ctk.CTkFrame(self.layer_frame, fg_color="transparent")
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
        
        # Layer list frame (regular frame since parent is already scrollable)
        self.list_frame = ctk.CTkFrame(self.layer_frame, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Layer controls frame
        controls_frame = ctk.CTkFrame(self.layer_frame, fg_color="transparent")
        controls_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        # Layer control buttons
        button_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        
        self.duplicate_btn = ctk.CTkButton(
            button_frame,
            text="Duplicate",
            width=80,
            height=28,
            font=ctk.CTkFont(size=12),
            command=self._duplicate_layer
        )
        self.duplicate_btn.pack(side="left", padx=(0, 3))
        
        self.delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete",
            width=70,
            height=28,
            font=ctk.CTkFont(size=12),
            command=self._delete_layer
        )
        self.delete_btn.pack(side="left", padx=(0, 3))
        
        self.merge_btn = ctk.CTkButton(
            button_frame,
            text="Merge Down",
            width=85,
            height=28,
            font=ctk.CTkFont(size=12),
            command=self._merge_layer
        )
        self.merge_btn.pack(side="left")
        
    
    def _update_display(self):
        """Update the layer display"""
        # Clear existing layer buttons (optimized - only destroy if needed)
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
        def on_visibility_change():
            """Handle visibility checkbox change"""
            self._toggle_visibility(index, visibility_var.get())
        
        visibility_cb = ctk.CTkCheckBox(
            layer_btn_frame,
            text="",
            width=18,
            height=18,
            variable=visibility_var,
            command=on_visibility_change
        )
        visibility_cb.pack(side="left", padx=(5, 0))
        
        # Layer name (clickable)
        layer_btn = ctk.CTkButton(
            layer_btn_frame,
            text=layer.name,
            height=28,
            anchor="w",
            font=ctk.CTkFont(size=12),
            command=lambda: self._select_layer(index)
        )
        layer_btn.pack(side="left", fill="x", expand=True, padx=(5, 5))
        
        # Active indicator
        if index == self.layer_manager.active_layer_index:
            layer_btn.configure(fg_color="blue")
        elif self.layer_manager.active_layer_index == -1:
            # No layer selected (show all) - make all layers slightly highlighted
            layer_btn.configure(fg_color="darkblue")
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
        """Select a layer (or deselect if clicking on active layer)"""
        # If clicking on the active layer, deselect it (show all layers)
        if index == self.layer_manager.active_layer_index:
            self.layer_manager.active_layer_index = -1  # -1 means no layer selected (show all)
        else:
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
    
