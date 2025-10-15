"""
Animation timeline UI for Pixel Perfect
Frame management and playback controls
"""

import customtkinter as ctk
from typing import Optional, Callable
from animation.timeline import AnimationTimeline

class TimelinePanel:
    """Animation timeline UI panel"""
    
    def __init__(self, parent_frame: ctk.CTkFrame, timeline: AnimationTimeline):
        self.parent_frame = parent_frame
        self.timeline = timeline
        self.on_frame_changed: Optional[Callable] = None
        
        # UI components
        self.timeline_frame = None
        self.frame_buttons = []
        self.playback_controls = None
        
        self._create_ui()
        self._update_display()
    
    def _create_ui(self):
        """Create the timeline panel UI"""
        # Main timeline frame
        self.timeline_frame = ctk.CTkFrame(self.parent_frame)
        self.timeline_frame.pack(fill="x", padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(self.timeline_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Title
        title_label = ctk.CTkLabel(header_frame, text="Animation", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(side="left")
        
        # FPS control
        fps_label = ctk.CTkLabel(header_frame, text="FPS:")
        fps_label.pack(side="right", padx=(0, 5))
        
        self.fps_var = ctk.StringVar(value=str(self.timeline.fps))
        self.fps_entry = ctk.CTkEntry(header_frame, textvariable=self.fps_var, width=40)
        self.fps_entry.pack(side="right", padx=(0, 5))
        self.fps_entry.bind("<Return>", self._on_fps_change)
        
        # Frame list
        self.frame_list_frame = ctk.CTkScrollableFrame(self.timeline_frame, height=100)
        self.frame_list_frame.pack(fill="x", padx=10, pady=5)
        
        # Playback controls
        self.playback_controls = ctk.CTkFrame(self.timeline_frame)
        self.playback_controls.pack(fill="x", padx=10, pady=(5, 10))
        
        # Control buttons
        button_frame = ctk.CTkFrame(self.playback_controls)
        button_frame.pack(fill="x")
        
        self.prev_btn = ctk.CTkButton(
            button_frame,
            text="◀",
            width=28,
            height=28,
            font=ctk.CTkFont(size=12),
            command=self._previous_frame
        )
        self.prev_btn.pack(side="left", padx=(0, 3))
        
        self.play_btn = ctk.CTkButton(
            button_frame,
            text="▶",
            width=28,
            height=28,
            font=ctk.CTkFont(size=12),
            command=self._toggle_playback
        )
        self.play_btn.pack(side="left", padx=(0, 3))
        
        self.next_btn = ctk.CTkButton(
            button_frame,
            text="▶",
            width=28,
            height=28,
            font=ctk.CTkFont(size=12),
            command=self._next_frame
        )
        self.next_btn.pack(side="left", padx=(0, 3))
        
        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="⏹",
            width=28,
            height=28,
            font=ctk.CTkFont(size=12),
            command=self._stop_animation
        )
        self.stop_btn.pack(side="left")
        
        # Frame controls
        frame_control_frame = ctk.CTkFrame(self.playback_controls)
        frame_control_frame.pack(fill="x", pady=(5, 0))
        
        self.add_frame_btn = ctk.CTkButton(
            frame_control_frame,
            text="Add Frame",
            width=75,
            height=28,
            font=ctk.CTkFont(size=12),
            command=self._add_frame
        )
        self.add_frame_btn.pack(side="left", padx=(0, 3))
        
        self.duplicate_frame_btn = ctk.CTkButton(
            frame_control_frame,
            text="Duplicate",
            width=75,
            height=28,
            font=ctk.CTkFont(size=12),
            command=self._duplicate_frame
        )
        self.duplicate_frame_btn.pack(side="left", padx=(0, 3))
        
        self.delete_frame_btn = ctk.CTkButton(
            frame_control_frame,
            text="Delete",
            width=65,
            height=28,
            font=ctk.CTkFont(size=12),
            command=self._delete_frame
        )
        self.delete_frame_btn.pack(side="left")
        
        # Frame info
        self.frame_info_label = ctk.CTkLabel(
            self.timeline_frame,
            text=f"Frame 1 of {self.timeline.get_frame_count()}"
        )
        self.frame_info_label.pack(pady=5)
    
    def _update_display(self):
        """Update the timeline display"""
        # Clear existing frame buttons (optimized - only destroy if needed)
        for widget in self.frame_list_frame.winfo_children():
            widget.destroy()
        
        self.frame_buttons.clear()
        
        # Create frame buttons
        for i, frame in enumerate(self.timeline.frames):
            self._create_frame_button(i, frame)
        
        # Update button states
        self._update_button_states()
        
        # Update frame info
        self.frame_info_label.configure(
            text=f"Frame {self.timeline.current_frame + 1} of {self.timeline.get_frame_count()}"
        )
        
        # Update playback button
        if self.timeline.is_playing:
            self.play_btn.configure(text="⏸")
        else:
            self.play_btn.configure(text="▶")
    
    def _create_frame_button(self, index: int, frame):
        """Create a button for a specific frame"""
        frame_btn = ctk.CTkButton(
            self.frame_list_frame,
            text=f"F{index + 1}",
            width=50,
            height=30,
            command=lambda: self._select_frame(index)
        )
        frame_btn.pack(side="left", padx=2)
        
        # Highlight current frame
        if index == self.timeline.current_frame:
            frame_btn.configure(fg_color="blue")
        else:
            frame_btn.configure(fg_color="gray")
        
        # Store button reference
        self.frame_buttons.append({
            'button': frame_btn,
            'index': index
        })
    
    def _update_button_states(self):
        """Update the state of control buttons"""
        frame_count = self.timeline.get_frame_count()
        current_frame = self.timeline.current_frame
        
        # Enable/disable buttons based on current state
        self.add_frame_btn.configure(state="normal" if frame_count < 8 else "disabled")
        self.delete_frame_btn.configure(state="normal" if frame_count > 1 else "disabled")
        self.duplicate_frame_btn.configure(state="normal" if frame_count < 8 else "disabled")
        self.prev_btn.configure(state="normal")
        self.next_btn.configure(state="normal")
    
    def _select_frame(self, frame_index: int):
        """Select a frame"""
        self.timeline.set_current_frame(frame_index)
        self._update_display()
        
        if self.on_frame_changed:
            self.on_frame_changed()
    
    def _add_frame(self):
        """Add a new frame"""
        if self.timeline.add_frame(self.timeline.current_frame):
            self._update_display()
            
            if self.on_frame_changed:
                self.on_frame_changed()
    
    def _duplicate_frame(self):
        """Duplicate the current frame"""
        if self.timeline.duplicate_frame(self.timeline.current_frame):
            self._update_display()
            
            if self.on_frame_changed:
                self.on_frame_changed()
    
    def _delete_frame(self):
        """Delete the current frame"""
        if self.timeline.remove_frame(self.timeline.current_frame):
            self._update_display()
            
            if self.on_frame_changed:
                self.on_frame_changed()
    
    def _previous_frame(self):
        """Go to previous frame"""
        self.timeline.previous_frame()
        self._update_display()
        
        if self.on_frame_changed:
            self.on_frame_changed()
    
    def _next_frame(self):
        """Go to next frame"""
        self.timeline.next_frame()
        self._update_display()
        
        if self.on_frame_changed:
            self.on_frame_changed()
    
    def _toggle_playback(self):
        """Toggle animation playback"""
        if self.timeline.is_playing:
            self.timeline.pause()
        else:
            self.timeline.play()
        
        self._update_display()
    
    def _stop_animation(self):
        """Stop animation"""
        self.timeline.stop()
        self._update_display()
        
        if self.on_frame_changed:
            self.on_frame_changed()
    
    def _on_fps_change(self, event):
        """Handle FPS change"""
        try:
            fps = int(self.fps_var.get())
            self.timeline.set_fps(fps)
        except ValueError:
            self.fps_var.set(str(self.timeline.fps))
    
    def refresh(self):
        """Refresh the timeline display"""
        self._update_display()
