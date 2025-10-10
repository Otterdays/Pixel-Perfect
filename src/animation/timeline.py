"""
Animation timeline for Pixel Perfect
Frame-by-frame animation management
"""

import numpy as np
from typing import List, Optional, Callable
from dataclasses import dataclass
import customtkinter as ctk

@dataclass
class AnimationFrame:
    """Represents a single animation frame"""
    pixels: np.ndarray
    duration: int = 100  # Duration in milliseconds
    name: str = ""

class AnimationTimeline:
    """Manages animation timeline and frames"""
    
    def __init__(self, width: int, height: int, max_frames: int = 8):
        self.width = width
        self.height = height
        self.max_frames = max_frames
        self.frames: List[AnimationFrame] = []
        self.current_frame = 0
        self.is_playing = False
        self.fps = 12  # Default FPS for pixel art animation
        self.loop = True
        
        # Callbacks
        self.on_frame_changed: Optional[Callable] = None
        self.on_playback_changed: Optional[Callable] = None
        
        # Create initial frame
        self._create_initial_frame()
    
    def _create_initial_frame(self):
        """Create the first empty frame"""
        pixels = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        frame = AnimationFrame(pixels, name="Frame 1")
        self.frames.append(frame)
    
    def add_frame(self, after_frame: int = -1) -> bool:
        """Add a new frame after the specified frame"""
        if len(self.frames) >= self.max_frames:
            return False
        
        # Create new frame
        pixels = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        frame_name = f"Frame {len(self.frames) + 1}"
        new_frame = AnimationFrame(pixels, name=frame_name)
        
        # Insert after specified frame
        insert_index = after_frame + 1 if after_frame >= 0 else len(self.frames)
        self.frames.insert(insert_index, new_frame)
        
        # Update current frame if needed
        if after_frame < self.current_frame:
            self.current_frame += 1
        
        if self.on_frame_changed:
            self.on_frame_changed()
        
        return True
    
    def remove_frame(self, frame_index: int) -> bool:
        """Remove a frame at the given index"""
        if len(self.frames) <= 1 or frame_index < 0 or frame_index >= len(self.frames):
            return False
        
        self.frames.pop(frame_index)
        
        # Adjust current frame
        if self.current_frame >= len(self.frames):
            self.current_frame = len(self.frames) - 1
        elif self.current_frame > frame_index:
            self.current_frame -= 1
        
        if self.on_frame_changed:
            self.on_frame_changed()
        
        return True
    
    def clear_frames(self):
        """Clear all frames and add a default frame"""
        self.frames.clear()
        self.add_frame()
        self.current_frame_index = 0
    
    def duplicate_frame(self, frame_index: int) -> bool:
        """Duplicate a frame"""
        if len(self.frames) >= self.max_frames or frame_index < 0 or frame_index >= len(self.frames):
            return False
        
        original_frame = self.frames[frame_index]
        new_pixels = original_frame.pixels.copy()
        frame_name = f"{original_frame.name} Copy"
        new_frame = AnimationFrame(new_pixels, original_frame.duration, frame_name)
        
        # Insert after original frame
        self.frames.insert(frame_index + 1, new_frame)
        
        if self.on_frame_changed:
            self.on_frame_changed()
        
        return True
    
    def move_frame(self, from_index: int, to_index: int) -> bool:
        """Move frame from one position to another"""
        if (from_index < 0 or from_index >= len(self.frames) or 
            to_index < 0 or to_index >= len(self.frames) or 
            from_index == to_index):
            return False
        
        frame = self.frames.pop(from_index)
        self.frames.insert(to_index, frame)
        
        # Adjust current frame
        if self.current_frame == from_index:
            self.current_frame = to_index
        elif from_index < self.current_frame <= to_index:
            self.current_frame -= 1
        elif to_index <= self.current_frame < from_index:
            self.current_frame += 1
        
        if self.on_frame_changed:
            self.on_frame_changed()
        
        return True
    
    def set_current_frame(self, frame_index: int) -> bool:
        """Set the current frame"""
        if 0 <= frame_index < len(self.frames):
            self.current_frame = frame_index
            if self.on_frame_changed:
                self.on_frame_changed()
            return True
        return False
    
    def get_current_frame(self) -> Optional[AnimationFrame]:
        """Get the current frame"""
        if 0 <= self.current_frame < len(self.frames):
            return self.frames[self.current_frame]
        return None
    
    def get_frame(self, index: int) -> Optional[AnimationFrame]:
        """Get frame at given index"""
        if 0 <= index < len(self.frames):
            return self.frames[index]
        return None
    
    def next_frame(self):
        """Move to next frame"""
        if self.current_frame < len(self.frames) - 1:
            self.current_frame += 1
        elif self.loop:
            self.current_frame = 0
        
        if self.on_frame_changed:
            self.on_frame_changed()
    
    def previous_frame(self):
        """Move to previous frame"""
        if self.current_frame > 0:
            self.current_frame -= 1
        elif self.loop:
            self.current_frame = len(self.frames) - 1
        
        if self.on_frame_changed:
            self.on_frame_changed()
    
    def play(self):
        """Start animation playback"""
        self.is_playing = True
        if self.on_playback_changed:
            self.on_playback_changed()
    
    def pause(self):
        """Pause animation playback"""
        self.is_playing = False
        if self.on_playback_changed:
            self.on_playback_changed()
    
    def stop(self):
        """Stop animation playback and reset to first frame"""
        self.is_playing = False
        self.current_frame = 0
        if self.on_playback_changed:
            self.on_playback_changed()
        if self.on_frame_changed:
            self.on_frame_changed()
    
    def set_fps(self, fps: int):
        """Set animation FPS"""
        self.fps = max(1, min(60, fps))
    
    def set_frame_duration(self, frame_index: int, duration: int):
        """Set duration for a specific frame"""
        if 0 <= frame_index < len(self.frames):
            self.frames[frame_index].duration = max(10, duration)
    
    def resize_frames(self, new_width: int, new_height: int):
        """Resize all frames"""
        self.width = new_width
        self.height = new_height
        
        for frame in self.frames:
            new_pixels = np.zeros((new_height, new_width, 4), dtype=np.uint8)
            
            # Copy existing pixels (clipped to new size)
            copy_width = min(new_width, frame.pixels.shape[1])
            copy_height = min(new_height, frame.pixels.shape[0])
            new_pixels[:copy_height, :copy_width] = frame.pixels[:copy_height, :copy_width]
            
            frame.pixels = new_pixels
    
    def get_frame_count(self) -> int:
        """Get number of frames"""
        return len(self.frames)
    
    def get_total_duration(self) -> int:
        """Get total animation duration in milliseconds"""
        return sum(frame.duration for frame in self.frames)
    
    def get_playback_duration(self) -> float:
        """Get total playback duration in seconds"""
        return self.get_total_duration() / 1000.0
