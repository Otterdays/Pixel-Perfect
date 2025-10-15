"""
Project save/load system for Pixel Perfect
Custom project format with auto-save functionality
"""

import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import numpy as np
from core.layer_manager import LayerManager
from core.color_palette import ColorPalette
from animation.timeline import AnimationTimeline

class ProjectManager:
    """Manages project save/load operations"""
    
    def __init__(self):
        self.current_project_path: Optional[str] = None
        self.auto_save_enabled = True
        self.auto_save_interval = 300  # 5 minutes
        self.recent_files: List[str] = []
        self.max_recent_files = 10
    
    def save_project(self, filename: str, canvas, palette: ColorPalette, 
                    layer_manager: LayerManager, timeline: AnimationTimeline,
                    metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Save project to file"""
        try:
            # Prepare project data
            project_data = {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat(),
                "canvas": {
                    "width": canvas.width,
                    "height": canvas.height,
                    "zoom": canvas.zoom,
                    "show_grid": canvas.show_grid,
                    "checkerboard": canvas.checkerboard
                },
                "palette": {
                    "name": palette.palette_name,
                    "type": palette.palette_type.value,
                    "colors": palette.colors,
                    "primary_color": palette.primary_color,
                    "secondary_color": palette.secondary_color
                },
                "layers": self._serialize_layers(layer_manager),
                "animation": self._serialize_animation(timeline),
                "metadata": metadata or {}
            }
            
            # Save to file
            with open(filename, 'w') as f:
                json.dump(project_data, f, indent=2, default=self._json_serializer)
            
            self.current_project_path = filename
            self._add_to_recent_files(filename)
            
            return True
            
        except Exception as e:
            print(f"Error saving project: {e}")
            return False
    
    def load_project(self, filename: str, canvas, palette: ColorPalette,
                    layer_manager: LayerManager, timeline: AnimationTimeline) -> bool:
        """Load project from file"""
        try:
            with open(filename, 'r') as f:
                project_data = json.load(f)
            
            # Load canvas settings
            canvas_config = project_data.get("canvas", {})
            new_width = canvas_config.get("width", 32)
            new_height = canvas_config.get("height", 32)
            canvas.zoom = canvas_config.get("zoom", 8)
            canvas.show_grid = canvas_config.get("show_grid", True)
            canvas.checkerboard = canvas_config.get("checkerboard", True)
            
            # Resize canvas to new dimensions
            canvas.resize(new_width, new_height)
            
            # Update layer manager dimensions to match canvas
            layer_manager.width = new_width
            layer_manager.height = new_height
            
            # Load palette
            palette_config = project_data.get("palette", {})
            palette.palette_name = palette_config.get("name", "Default")
            palette.colors = [tuple(color) for color in palette_config.get("colors", [])]
            palette.primary_color = palette_config.get("primary_color", 0)
            palette.secondary_color = palette_config.get("secondary_color", 1)
            
            # Set palette type
            palette_type_str = palette_config.get("type", "custom")
            try:
                from core.color_palette import PaletteType
                palette.palette_type = PaletteType(palette_type_str)
            except ValueError:
                palette.palette_type = PaletteType.CUSTOM
            
            # Load layers
            self._deserialize_layers(layer_manager, project_data.get("layers", []))
            
            # Load animation
            self._deserialize_animation(timeline, project_data.get("animation", {}))
            
            self.current_project_path = filename
            self._add_to_recent_files(filename)
            
            return True
            
        except Exception as e:
            print(f"Error loading project: {e}")
            return False
    
    def _serialize_layers(self, layer_manager: LayerManager) -> List[Dict[str, Any]]:
        """Serialize layer data"""
        layers_data = []
        
        for i, layer in enumerate(layer_manager.layers):
            layer_data = {
                "index": i,
                "name": layer.name,
                "visible": layer.visible,
                "opacity": layer.opacity,
                "locked": layer.locked,
                "pixels": layer.pixels.tolist()  # Convert numpy array to list
            }
            layers_data.append(layer_data)
        
        return layers_data
    
    def _deserialize_layers(self, layer_manager: LayerManager, layers_data: List[Dict[str, Any]]):
        """Deserialize layer data"""
        # Clear existing layers
        layer_manager.layers.clear()
        
        # Recreate layers
        for layer_data in layers_data:
            pixels = np.array(layer_data.get("pixels", []), dtype=np.uint8)
            name = layer_data.get("name", "Layer")
            visible = layer_data.get("visible", True)
            opacity = layer_data.get("opacity", 1.0)
            locked = layer_data.get("locked", False)
            
            from core.layer_manager import Layer
            layer = Layer(name, pixels, visible, opacity, locked)
            layer_manager.layers.append(layer)
        
        # Set active layer
        layer_manager.active_layer_index = 0
    
    def _serialize_animation(self, timeline: AnimationTimeline) -> Dict[str, Any]:
        """Serialize animation data"""
        frames_data = []
        
        for i, frame in enumerate(timeline.frames):
            frame_data = {
                "index": i,
                "name": frame.name,
                "duration": frame.duration,
                "pixels": frame.pixels.tolist()
            }
            frames_data.append(frame_data)
        
        return {
            "current_frame": timeline.current_frame,
            "fps": timeline.fps,
            "loop": timeline.loop,
            "frames": frames_data
        }
    
    def _deserialize_animation(self, timeline: AnimationTimeline, animation_data: Dict[str, Any]):
        """Deserialize animation data"""
        # Clear existing frames
        timeline.frames.clear()
        
        # Recreate frames
        frames_data = animation_data.get("frames", [])
        for frame_data in frames_data:
            pixels = np.array(frame_data.get("pixels", []), dtype=np.uint8)
            name = frame_data.get("name", "Frame")
            duration = frame_data.get("duration", 100)
            
            from animation.timeline import AnimationFrame
            frame = AnimationFrame(pixels, duration, name)
            timeline.frames.append(frame)
        
        # Set animation properties
        timeline.current_frame = animation_data.get("current_frame", 0)
        timeline.fps = animation_data.get("fps", 12)
        timeline.loop = animation_data.get("loop", True)
    
    def _json_serializer(self, obj):
        """Custom JSON serializer for numpy arrays"""
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    def _add_to_recent_files(self, filename: str):
        """Add file to recent files list"""
        if filename in self.recent_files:
            self.recent_files.remove(filename)
        
        self.recent_files.insert(0, filename)
        
        # Limit recent files
        if len(self.recent_files) > self.max_recent_files:
            self.recent_files = self.recent_files[:self.max_recent_files]
    
    def get_recent_files(self) -> List[str]:
        """Get list of recent files"""
        # Filter out files that no longer exist
        existing_files = []
        for filename in self.recent_files:
            if os.path.exists(filename):
                existing_files.append(filename)
        
        self.recent_files = existing_files
        return self.recent_files.copy()
    
    def clear_recent_files(self):
        """Clear recent files list"""
        self.recent_files.clear()
    
    def get_project_info(self, filename: str) -> Optional[Dict[str, Any]]:
        """Get basic project information without loading"""
        try:
            with open(filename, 'r') as f:
                project_data = json.load(f)
            
            return {
                "version": project_data.get("version", "Unknown"),
                "created": project_data.get("created", "Unknown"),
                "modified": project_data.get("modified", "Unknown"),
                "canvas_size": f"{project_data.get('canvas', {}).get('width', 0)}x{project_data.get('canvas', {}).get('height', 0)}",
                "palette": project_data.get("palette", {}).get("name", "Unknown"),
                "layer_count": len(project_data.get("layers", [])),
                "frame_count": len(project_data.get("animation", {}).get("frames", []))
            }
            
        except Exception as e:
            print(f"Error reading project info: {e}")
            return None
    
    def export_png(self, filename: str, canvas, scale: int = 1) -> bool:
        """Export current canvas as PNG"""
        try:
            from PIL import Image
            
            # Convert canvas pixels to PIL Image
            pixels = canvas.pixels
            image = Image.fromarray(pixels, 'RGBA')
            
            # Scale if needed
            if scale > 1:
                new_size = (canvas.width * scale, canvas.height * scale)
                image = image.resize(new_size, Image.NEAREST)
            
            # Save image
            image.save(filename, 'PNG')
            return True
            
        except Exception as e:
            print(f"Error exporting PNG: {e}")
            return False
    
    def export_gif(self, filename: str, timeline: AnimationTimeline, scale: int = 1) -> bool:
        """Export animation as GIF"""
        try:
            from PIL import Image
            
            if not timeline.frames:
                return False
            
            # Convert frames to PIL Images
            pil_frames = []
            for frame in timeline.frames:
                image = Image.fromarray(frame.pixels, 'RGBA')
                
                # Scale if needed
                if scale > 1:
                    new_size = (timeline.width * scale, timeline.height * scale)
                    image = image.resize(new_size, Image.NEAREST)
                
                pil_frames.append(image)
            
            # Save as GIF
            if len(pil_frames) == 1:
                pil_frames[0].save(filename, 'GIF')
            else:
                pil_frames[0].save(
                    filename,
                    'GIF',
                    save_all=True,
                    append_images=pil_frames[1:],
                    duration=timeline.frames[0].duration,
                    loop=0
                )
            
            return True
            
        except Exception as e:
            print(f"Error exporting GIF: {e}")
            return False
