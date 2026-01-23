"""
Animation timeline UI for Pixel Perfect
Frame management and playback controls
"""

import customtkinter as ctk
from typing import Optional, Callable
from animation.timeline import AnimationTimeline
from PIL import Image

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
        self._playback_timer_id = None  # Tkinter after() timer ID
        self._thumbnail_images = []  # Keep references to prevent garbage collection
        
        self._create_ui()
        self._update_display()
    
    def _create_ui(self):
        """Create the timeline panel UI"""
        # Use the parent frame directly, no container frame
        self.timeline_frame = self.parent_frame
        
        # Header
        header_frame = ctk.CTkFrame(self.timeline_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(15, 5))
        
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
        
        # Frame list (use regular frame - parent already scrollable)
        self.frame_list_frame = ctk.CTkFrame(self.timeline_frame, height=100)
        self.frame_list_frame.pack(fill="x", padx=10, pady=5)
        
        # Playback controls
        self.playback_controls = ctk.CTkFrame(self.timeline_frame, fg_color="transparent")
        self.playback_controls.pack(fill="x", padx=10, pady=(5, 15))
        
        # Control buttons
        button_frame = ctk.CTkFrame(self.playback_controls, fg_color="transparent")
        button_frame.pack(fill="x")
        
        self.prev_btn = ctk.CTkButton(
            button_frame,
            text="◀",
            width=28,
            height=28,
            font=ctk.CTkFont(size=12),
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            command=self._previous_frame
        )
        self.prev_btn.pack(side="left", padx=(0, 3))
        
        self.play_btn = ctk.CTkButton(
            button_frame,
            text="▶",
            width=28,
            height=28,
            font=ctk.CTkFont(size=12),
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            command=self._toggle_playback
        )
        self.play_btn.pack(side="left", padx=(0, 3))
        
        self.next_btn = ctk.CTkButton(
            button_frame,
            text="▶",
            width=28,
            height=28,
            font=ctk.CTkFont(size=12),
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            command=self._next_frame
        )
        self.next_btn.pack(side="left", padx=(0, 3))
        
        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="⏹",
            width=28,
            height=28,
            font=ctk.CTkFont(size=12),
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            command=self._stop_animation
        )
        self.stop_btn.pack(side="left")
        
        # Frame controls
        frame_control_frame = ctk.CTkFrame(self.playback_controls, fg_color="transparent")
        frame_control_frame.pack(fill="x", pady=(5, 0))
        
        self.add_frame_btn = ctk.CTkButton(
            frame_control_frame,
            text="Add Frame",
            width=75,
            height=28,
            font=ctk.CTkFont(size=12),
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            command=self._add_frame
        )
        self.add_frame_btn.pack(side="left", padx=(0, 3))
        
        self.duplicate_frame_btn = ctk.CTkButton(
            frame_control_frame,
            text="Duplicate",
            width=75,
            height=28,
            font=ctk.CTkFont(size=12),
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            command=self._duplicate_frame
        )
        self.duplicate_frame_btn.pack(side="left", padx=(0, 3))
        
        self.delete_frame_btn = ctk.CTkButton(
            frame_control_frame,
            text="Delete",
            width=65,
            height=28,
            font=ctk.CTkFont(size=12),
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            command=self._delete_frame
        )
        self.delete_frame_btn.pack(side="left")
        
        # Frame info
        self.frame_info_label = ctk.CTkLabel(
            self.timeline_frame,
            text=f"Frame 1 of {self.timeline.get_frame_count()}"
        )
        self.frame_info_label.pack(pady=5, padx=10)
        
        # Onion skinning controls
        onion_frame = ctk.CTkFrame(self.timeline_frame, fg_color="transparent")
        onion_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        # Onion skin toggle
        self.onion_skin_var = ctk.BooleanVar(value=self.timeline.onion_skin_enabled)
        onion_toggle = ctk.CTkCheckBox(
            onion_frame,
            text="Onion Skin",
            variable=self.onion_skin_var,
            command=self._toggle_onion_skin
        )
        onion_toggle.pack(side="left", padx=(0, 10))
        
        # Previous frame opacity
        prev_label = ctk.CTkLabel(onion_frame, text="Prev:")
        prev_label.pack(side="left", padx=(0, 5))
        self.prev_opacity_var = ctk.DoubleVar(value=self.timeline.onion_skin_prev_opacity)
        prev_slider = ctk.CTkSlider(
            onion_frame,
            from_=0.0,
            to=1.0,
            variable=self.prev_opacity_var,
            width=80,
            command=self._on_prev_opacity_change
        )
        prev_slider.pack(side="left", padx=(0, 10))
        
        # Next frame opacity
        next_label = ctk.CTkLabel(onion_frame, text="Next:")
        next_label.pack(side="left", padx=(0, 5))
        self.next_opacity_var = ctk.DoubleVar(value=self.timeline.onion_skin_next_opacity)
        next_slider = ctk.CTkSlider(
            onion_frame,
            from_=0.0,
            to=1.0,
            variable=self.next_opacity_var,
            width=80,
            command=self._on_next_opacity_change
        )
        next_slider.pack(side="left")
    
    def _toggle_onion_skin(self):
        """Toggle onion skinning on/off"""
        self.timeline.onion_skin_enabled = self.onion_skin_var.get()
        # Trigger canvas update to show/hide onion skin
        if self.on_frame_changed:
            self.on_frame_changed()
        # Also trigger pixel display update if available
        if hasattr(self, 'update_pixel_display_callback') and self.update_pixel_display_callback:
            self.update_pixel_display_callback()
    
    def _on_prev_opacity_change(self, value):
        """Handle previous frame opacity change"""
        self.timeline.onion_skin_prev_opacity = float(value)
        # Trigger canvas update to show updated opacity
        if hasattr(self, 'update_pixel_display_callback') and self.update_pixel_display_callback:
            self.update_pixel_display_callback()
    
    def _on_next_opacity_change(self, value):
        """Handle next frame opacity change"""
        self.timeline.onion_skin_next_opacity = float(value)
        # Trigger canvas update to show updated opacity
        if hasattr(self, 'update_pixel_display_callback') and self.update_pixel_display_callback:
            self.update_pixel_display_callback()
    
    def _update_display(self):
        """Update the timeline display"""
        # Clear thumbnail cache
        self._thumbnail_images.clear()  # Clear old thumbnails
        
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
        
        # Update onion skin controls
        if hasattr(self, 'onion_skin_var'):
            self.onion_skin_var.set(self.timeline.onion_skin_enabled)
        if hasattr(self, 'prev_opacity_var'):
            self.prev_opacity_var.set(self.timeline.onion_skin_prev_opacity)
        if hasattr(self, 'next_opacity_var'):
            self.next_opacity_var.set(self.timeline.onion_skin_next_opacity)
    
    def _create_frame_button(self, index: int, frame):
        """Create a button with thumbnail for a specific frame"""
        # Create container for thumbnail + label
        frame_container = ctk.CTkFrame(self.frame_list_frame, fg_color="transparent")
        frame_container.pack(side="left", padx=2)
        
        # Generate thumbnail (32x32 preview)
        thumb_size = 32
        try:
            # Convert numpy array to PIL Image
            img = Image.fromarray(frame.pixels, 'RGBA')
            img.thumbnail((thumb_size, thumb_size), Image.Resampling.NEAREST)
            
            # Create background for transparency
            bg = Image.new('RGBA', (thumb_size, thumb_size), (60, 60, 60, 255))
            # Center the thumbnail
            offset = ((thumb_size - img.width) // 2, (thumb_size - img.height) // 2)
            bg.paste(img, offset, img)
            
            # Use CTkImage for proper HighDPI support
            ctk_image = ctk.CTkImage(light_image=bg, dark_image=bg, size=(thumb_size, thumb_size))
            self._thumbnail_images.append(ctk_image)  # Keep reference
            
            thumb_label = ctk.CTkLabel(
                frame_container,
                image=ctk_image,
                text="",
                width=thumb_size,
                height=thumb_size
            )
            thumb_label.pack()
            thumb_label.bind("<Button-1>", lambda e, i=index: self._select_frame(i))
        except Exception:
            # Fallback to text if thumbnail fails
            pass
        
        # Frame number label
        is_current = index == self.timeline.current_frame
        frame_label = ctk.CTkLabel(
            frame_container,
            text=f"F{index + 1}",
            font=ctk.CTkFont(size=10, weight="bold" if is_current else "normal"),
            text_color="#4a9eff" if is_current else "#888888"
        )
        frame_label.pack()
        frame_label.bind("<Button-1>", lambda e, i=index: self._select_frame(i))
        
        # Highlight current frame
        if is_current:
            frame_container.configure(fg_color="#2a4a6a")
        
        # Store reference
        self.frame_buttons.append({
            'container': frame_container,
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
            # Cancel any pending timer
            if self._playback_timer_id:
                self.timeline_frame.after_cancel(self._playback_timer_id)
                self._playback_timer_id = None
        else:
            self.timeline.play()
            # Start playback loop
            self._advance_frame()
        
        self._update_display()
    
    def _advance_frame(self):
        """Advance to next frame during playback"""
        if not self.timeline.is_playing:
            self._playback_timer_id = None
            return
        
        # Advance frame
        self.timeline.next_frame()
        self._update_display()
        
        if self.on_frame_changed:
            self.on_frame_changed()
        
        # Schedule next frame based on FPS
        delay_ms = int(1000 / self.timeline.fps)
        self._playback_timer_id = self.timeline_frame.after(delay_ms, self._advance_frame)
    
    def _stop_animation(self):
        """Stop animation"""
        # Cancel any pending timer
        if self._playback_timer_id:
            self.timeline_frame.after_cancel(self._playback_timer_id)
            self._playback_timer_id = None
        
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
