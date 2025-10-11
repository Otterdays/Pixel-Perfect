That's a really cool idea for giving your pixel art items a 3D appearance! So you want to create a coin/medallion-like effect where your pixel art gets depth - like it's embossed or stamped onto a coin. Let me break down what I understand and suggest some approaches:

## The Concept:
- **Front face**: Your original pixel art design
- **Edges/rim**: Extended pixels from the border of your design creating depth
- **Back face**: An inverted/mirrored version of your design

## Implementation Approaches:

### 1. **Simple Extrusion Method**
- Take your pixel art and extrude each pixel into a voxel (3D pixel)
- Edge pixels get extended backward to create the coin thickness
- The back face could be:
  - A negative/inverted color version
  - A mirrored flip of the design
  - A simplified silhouette

### 2. **Layered Depth Technique**
- Create multiple layers of your sprite with slight offsets
- Stack them to create a pseudo-3D effect
- Apply subtle shading to each layer to enhance depth perception

### 3. **Normal Mapping Style**
- Keep it 2D but use lighting/shading techniques
- Darker colors on edges to simulate depth
- Highlights on raised portions
- Could be automated based on pixel brightness/color

## For Your Pixel Art Editor:
You could add a "3D Preview" mode that:
1. Takes the current canvas
2. Generates a coin-like visualization in real-time
3. Shows rotation animations to display the depth effect


====================================================================================================================================================================================


# 2.5D Pixel Art Token/Coin Viewer - Technical Specification

## Overview
Create a desktop application module that transforms 2D pixel art into a 3D coin/medallion with depth, allowing rotation and real-time preview of the extruded design.

## Core Concept
Transform flat pixel art into a coin-like 3D object with:
- **Front Face**: Original pixel art design
- **Extruded Edges**: Depth created by extending border pixels
- **Back Face**: Mirrored or embossed reverse design
- **Interactive Rotation**: Real-time 3D viewing with mouse/touch controls

---

## Technical Architecture

### 1. Dependencies
```python
# requirements.txt
numpy>=1.24.0
moderngl>=5.8.0
Pillow>=10.0.0
PyQt6>=6.5.0  # or PyQt5, PySide6 - whatever your app uses
pyrr>=0.10.3  # for matrix transformations
glfw>=2.6.0  # optional: for standalone window, or use Qt's OpenGL widget
```

### 2. Data Structures

```python
from dataclasses import dataclass
from typing import Tuple, List
import numpy as np

@dataclass
class Pixel:
    """Represents a single pixel with position and color"""
    x: int
    y: int
    color: Tuple[int, int, int, int]  # RGBA
    
@dataclass
class Voxel:
    """3D pixel representation"""
    x: float
    y: float
    z: float
    color: Tuple[float, float, float, float]  # Normalized RGBA
    is_edge: bool = False
    is_back_face: bool = False

@dataclass
class CoinSettings:
    """Configuration for 3D coin generation"""
    thickness: float = 0.3  # Coin thickness in units
    bevel_size: float = 0.1  # Edge bevel radius
    edge_color_darken: float = 0.3  # How much to darken edge pixels
    back_face_mode: str = "mirrored"  # "mirrored", "inverted", "embossed"
    resolution_multiplier: int = 1  # For smoother voxels
```

---

## 3. Core Algorithm: Pixel Art to 3D Coin

### Step-by-Step Process

```python
class PixelTo3DConverter:
    """
    Converts 2D pixel art into 3D voxel-based coin/medallion
    """
    
    def __init__(self, settings: CoinSettings = None):
        self.settings = settings or CoinSettings()
        
    def convert_image_to_voxels(self, image_array: np.ndarray) -> List[Voxel]:
        """
        Main conversion function
        
        Args:
            image_array: RGBA numpy array (height, width, 4)
            
        Returns:
            List of Voxel objects representing the 3D coin
        """
        height, width = image_array.shape[:2]
        voxels = []
        
        # Step 1: Create front face voxels
        front_voxels = self._create_front_face(image_array)
        voxels.extend(front_voxels)
        
        # Step 2: Detect edges and create extrusion
        edge_map = self._detect_edges(image_array)
        edge_voxels = self._create_extruded_edges(
            image_array, edge_map, self.settings.thickness
        )
        voxels.extend(edge_voxels)
        
        # Step 3: Create back face
        back_voxels = self._create_back_face(
            image_array, self.settings.thickness
        )
        voxels.extend(back_voxels)
        
        # Step 4: Optional - add beveled edges
        if self.settings.bevel_size > 0:
            bevel_voxels = self._create_beveled_rim(
                image_array, edge_map
            )
            voxels.extend(bevel_voxels)
            
        return voxels
    
    def _create_front_face(self, image_array: np.ndarray) -> List[Voxel]:
        """
        Create voxels for the front face at z=0
        Only includes non-transparent pixels
        """
        height, width = image_array.shape[:2]
        voxels = []
        
        for y in range(height):
            for x in range(width):
                pixel = image_array[y, x]
                alpha = pixel[3]
                
                # Skip transparent pixels
                if alpha < 10:
                    continue
                
                # Normalize color to 0-1 range
                color = tuple(pixel / 255.0)
                
                voxels.append(Voxel(
                    x=float(x),
                    y=float(y),
                    z=0.0,
                    color=color,
                    is_edge=False
                ))
                
        return voxels
    
    def _detect_edges(self, image_array: np.ndarray) -> np.ndarray:
        """
        Detect edge pixels (pixels adjacent to transparent areas)
        
        Returns:
            Boolean array where True = edge pixel
        """
        height, width = image_array.shape[:2]
        alpha_channel = image_array[:, :, 3]
        edge_map = np.zeros((height, width), dtype=bool)
        
        # A pixel is an edge if it's opaque and has at least one transparent neighbor
        for y in range(height):
            for x in range(width):
                if alpha_channel[y, x] < 10:  # Transparent
                    continue
                
                # Check 8 neighbors
                is_edge = False
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dy == 0 and dx == 0:
                            continue
                        
                        ny, nx = y + dy, x + dx
                        
                        # Out of bounds = edge
                        if ny < 0 or ny >= height or nx < 0 or nx >= width:
                            is_edge = True
                            break
                        
                        # Transparent neighbor = edge
                        if alpha_channel[ny, nx] < 10:
                            is_edge = True
                            break
                    
                    if is_edge:
                        break
                
                edge_map[y, x] = is_edge
        
        return edge_map
    
    def _create_extruded_edges(
        self, 
        image_array: np.ndarray, 
        edge_map: np.ndarray,
        thickness: float
    ) -> List[Voxel]:
        """
        Create voxels that form the sides of the coin
        These connect the front face to the back face
        """
        height, width = image_array.shape[:2]
        voxels = []
        
        # Number of layers for smooth extrusion
        num_layers = max(3, int(thickness * 10))
        
        for y in range(height):
            for x in range(width):
                if not edge_map[y, x]:
                    continue
                
                pixel = image_array[y, x]
                if pixel[3] < 10:  # Skip transparent
                    continue
                
                # Darken edge color for depth effect
                base_color = pixel / 255.0
                edge_color = base_color.copy()
                edge_color[:3] *= (1.0 - self.settings.edge_color_darken)
                
                # Create layers from z=0 to z=-thickness
                for i in range(1, num_layers):
                    z = -thickness * (i / num_layers)
                    
                    voxels.append(Voxel(
                        x=float(x),
                        y=float(y),
                        z=z,
                        color=tuple(edge_color),
                        is_edge=True
                    ))
        
        return voxels
    
    def _create_back_face(
        self, 
        image_array: np.ndarray, 
        thickness: float
    ) -> List[Voxel]:
        """
        Create the back face of the coin
        """
        height, width = image_array.shape[:2]
        voxels = []
        
        for y in range(height):
            for x in range(width):
                pixel = image_array[y, x]
                if pixel[3] < 10:  # Skip transparent
                    continue
                
                # Choose back face appearance based on mode
                if self.settings.back_face_mode == "mirrored":
                    # Flip horizontally
                    back_x = width - 1 - x
                    back_color = image_array[y, back_x] / 255.0
                    
                elif self.settings.back_face_mode == "inverted":
                    # Invert colors
                    back_color = pixel / 255.0
                    back_color[:3] = 1.0 - back_color[:3]
                    
                elif self.settings.back_face_mode == "embossed":
                    # Grayscale embossed look
                    gray = np.mean(pixel[:3])
                    back_color = np.array([gray, gray, gray, pixel[3]]) / 255.0
                else:
                    back_color = pixel / 255.0
                
                # Slightly darken back face
                back_color[:3] *= 0.8
                
                voxels.append(Voxel(
                    x=float(x),
                    y=float(y),
                    z=-thickness,
                    color=tuple(back_color),
                    is_back_face=True
                ))
        
        return voxels
    
    def _create_beveled_rim(
        self, 
        image_array: np.ndarray, 
        edge_map: np.ndarray
    ) -> List[Voxel]:
        """
        Create smooth beveled edges around the coin rim
        """
        # Simplified version - can be expanded with proper beveling
        voxels = []
        
        height, width = image_array.shape[:2]
        bevel_steps = 3
        
        for y in range(height):
            for x in range(width):
                if not edge_map[y, x]:
                    continue
                
                pixel = image_array[y, x]
                if pixel[3] < 10:
                    continue
                
                base_color = pixel / 255.0
                
                # Create beveled transition
                for i in range(bevel_steps):
                    offset = self.settings.bevel_size * (i / bevel_steps)
                    z_offset = -self.settings.bevel_size * (i / bevel_steps)
                    
                    # Gradually darken
                    bevel_color = base_color.copy()
                    bevel_color[:3] *= (1.0 - 0.2 * (i / bevel_steps))
                    
                    # Add slight outward offset for bevel effect
                    # (This is simplified - proper beveling would calculate normals)
                    voxels.append(Voxel(
                        x=float(x),
                        y=float(y),
                        z=z_offset,
                        color=tuple(bevel_color),
                        is_edge=True
                    ))
        
        return voxels
```

---

## 4. 3D Rendering System

### OpenGL-based Renderer

```python
import moderngl
from pyrr import Matrix44, Vector3
import numpy as np

class CoinRenderer:
    """
    Renders voxels as 3D cubes with instancing for performance
    """
    
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        
        # Initialize ModernGL context (can be Qt OpenGL widget)
        self.ctx = moderngl.create_standalone_context()
        
        # Camera parameters
        self.rotation_x = 30.0  # degrees
        self.rotation_y = 45.0
        self.zoom = 2.0
        
        # Setup shader program
        self.prog = self._create_shader_program()
        
        # Create cube mesh for instanced rendering
        self.vbo_cube, self.ibo_cube = self._create_cube_mesh()
        
        # Voxel instance data (position + color)
        self.vbo_instances = None
        self.vao = None
        
    def _create_shader_program(self):
        """
        Create vertex and fragment shaders for voxel rendering
        """
        vertex_shader = """
        #version 330
        
        // Per-vertex attributes (cube mesh)
        in vec3 in_position;
        in vec3 in_normal;
        
        // Per-instance attributes (voxel data)
        in vec3 in_instance_position;
        in vec4 in_instance_color;
        
        // Uniforms
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;
        
        // Outputs to fragment shader
        out vec4 v_color;
        out vec3 v_normal;
        out vec3 v_frag_pos;
        
        void main() {
            // Scale cube to voxel size (0.95 to create small gaps)
            vec3 scaled_pos = in_position * 0.95;
            
            // Translate to instance position
            vec3 world_pos = scaled_pos + in_instance_position;
            
            // Transform to clip space
            gl_Position = projection * view * model * vec4(world_pos, 1.0);
            
            // Pass data to fragment shader
            v_color = in_instance_color;
            v_normal = mat3(model) * in_normal;
            v_frag_pos = vec3(model * vec4(world_pos, 1.0));
        }
        """
        
        fragment_shader = """
        #version 330
        
        in vec4 v_color;
        in vec3 v_normal;
        in vec3 v_frag_pos;
        
        out vec4 fragColor;
        
        uniform vec3 light_pos;
        uniform vec3 view_pos;
        
        void main() {
            // Simple Blinn-Phong lighting
            vec3 normal = normalize(v_normal);
            vec3 light_dir = normalize(light_pos - v_frag_pos);
            vec3 view_dir = normalize(view_pos - v_frag_pos);
            vec3 halfway_dir = normalize(light_dir + view_dir);
            
            // Ambient
            float ambient = 0.3;
            
            // Diffuse
            float diff = max(dot(normal, light_dir), 0.0);
            
            // Specular
            float spec = pow(max(dot(normal, halfway_dir), 0.0), 32.0);
            
            // Combine
            vec3 result = v_color.rgb * (ambient + diff * 0.6 + spec * 0.3);
            fragColor = vec4(result, v_color.a);
        }
        """
        
        return self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )
    
    def _create_cube_mesh(self):
        """
        Create a unit cube mesh (will be instanced for each voxel)
        """
        # Cube vertices (position + normal)
        vertices = np.array([
            # Front face
            [-0.5, -0.5,  0.5,  0.0,  0.0,  1.0],
            [ 0.5, -0.5,  0.5,  0.0,  0.0,  1.0],
            [ 0.5,  0.5,  0.5,  0.0,  0.0,  1.0],
            [-0.5,  0.5,  0.5,  0.0,  0.0,  1.0],
            # Back face
            [-0.5, -0.5, -0.5,  0.0,  0.0, -1.0],
            [ 0.5, -0.5, -0.5,  0.0,  0.0, -1.0],
            [ 0.5,  0.5, -0.5,  0.0,  0.0, -1.0],
            [-0.5,  0.5, -0.5,  0.0,  0.0, -1.0],
            # Top face
            [-0.5,  0.5, -0.5,  0.0,  1.0,  0.0],
            [ 0.5,  0.5, -0.5,  0.0,  1.0,  0.0],
            [ 0.5,  0.5,  0.5,  0.0,  1.0,  0.0],
            [-0.5,  0.5,  0.5,  0.0,  1.0,  0.0],
            # Bottom face
            [-0.5, -0.5, -0.5,  0.0, -1.0,  0.0],
            [ 0.5, -0.5, -0.5,  0.0, -1.0,  0.0],
            [ 0.5, -0.5,  0.5,  0.0, -1.0,  0.0],
            [-0.5, -0.5,  0.5,  0.0, -1.0,  0.0],
            # Right face
            [ 0.5, -0.5, -0.5,  1.0,  0.0,  0.0],
            [ 0.5,  0.5, -0.5,  1.0,  0.0,  0.0],
            [ 0.5,  0.5,  0.5,  1.0,  0.0,  0.0],
            [ 0.5, -0.5,  0.5,  1.0,  0.0,  0.0],
            # Left face
            [-0.5, -0.5, -0.5, -1.0,  0.0,  0.0],
            [-0.5,  0.5, -0.5, -1.0,  0.0,  0.0],
            [-0.5,  0.5,  0.5, -1.0,  0.0,  0.0],
            [-0.5, -0.5,  0.5, -1.0,  0.0,  0.0],
        ], dtype='f4')
        
        # Cube indices
        indices = np.array([
            0, 1, 2, 2, 3, 0,      # Front
            4, 7, 6, 6, 5, 4,      # Back
            8, 9, 10, 10, 11, 8,   # Top
            12, 15, 14, 14, 13, 12, # Bottom
            16, 17, 18, 18, 19, 16, # Right
            20, 23, 22, 22, 21, 20, # Left
        ], dtype='i4')
        
        vbo = self.ctx.buffer(vertices.tobytes())
        ibo = self.ctx.buffer(indices.tobytes())
        
        return vbo, ibo
    
    def load_voxels(self, voxels: List[Voxel]):
        """
        Load voxel data into GPU buffer for instanced rendering
        """
        # Convert voxels to instance data array
        instance_data = []
        for voxel in voxels:
            # Position (xyz) + Color (rgba)
            instance_data.extend([
                voxel.x, voxel.y, voxel.z,  # position
                voxel.color[0], voxel.color[1], 
                voxel.color[2], voxel.color[3]  # color
            ])
        
        instance_array = np.array(instance_data, dtype='f4')
        
        # Create or update instance buffer
        if self.vbo_instances:
            self.vbo_instances.release()
        
        self.vbo_instances = self.ctx.buffer(instance_array.tobytes())
        
        # Create VAO
        if self.vao:
            self.vao.release()
        
        self.vao = self.ctx.vertex_array(
            self.prog,
            [
                (self.vbo_cube, '3f 3f', 'in_position', 'in_normal'),
                (self.vbo_instances, '3f 4f /i', 
                 'in_instance_position', 'in_instance_color'),
            ],
            self.ibo_cube
        )
        
        self.num_instances = len(voxels)
    
    def render(self) -> np.ndarray:
        """
        Render the coin and return as numpy image array
        """
        # Setup framebuffer
        fbo = self.ctx.framebuffer(
            color_attachments=[
                self.ctx.texture((self.width, self.height), 4)
            ],
            depth_attachment=self.ctx.depth_texture((self.width, self.height))
        )
        
        fbo.use()
        self.ctx.clear(0.1, 0.1, 0.1, 1.0)
        self.ctx.enable(moderngl.DEPTH_TEST)
        
        # Calculate matrices
        model = Matrix44.identity()
        model = Matrix44.from_x_rotation(np.radians(self.rotation_x)) @ model
        model = Matrix44.from_y_rotation(np.radians(self.rotation_y)) @ model
        
        # Center the model
        view = Matrix44.look_at(
            (0.0, 0.0, self.zoom),
            (0.0, 0.0, 0.0),
            (0.0, 1.0, 0.0)
        )
        
        projection = Matrix44.perspective_projection(
            45.0, self.width / self.height, 0.1, 100.0
        )
        
        # Set uniforms
        self.prog['model'].write(model.astype('f4').tobytes())
        self.prog['view'].write(view.astype('f4').tobytes())
        self.prog['projection'].write(projection.astype('f4').tobytes())
        self.prog['light_pos'].value = (5.0, 5.0, 5.0)
        self.prog['view_pos'].value = (0.0, 0.0, self.zoom)
        
        # Render instances
        self.vao.render(instances=self.num_instances)
        
        # Read pixels
        image_data = fbo.read(components=4)
        image = np.frombuffer(image_data, dtype='u1').reshape(
            (self.height, self.width, 4)
        )
        
        # Flip vertically (OpenGL origin is bottom-left)
        image = np.flipud(image)
        
        fbo.release()
        
        return image
    
    def set_rotation(self, x: float, y: float):
        """Set camera rotation angles in degrees"""
        self.rotation_x = x
        self.rotation_y = y
    
    def set_zoom(self, zoom: float):
        """Set camera zoom distance"""
        self.zoom = max(1.0, min(10.0, zoom))
```

---

## 5. Integration Example: Qt Widget

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PIL import Image
import numpy as np

class CoinPreviewWidget(QWidget):
    """
    Qt widget that shows interactive 3D coin preview
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.converter = PixelTo3DConverter()
        self.renderer = CoinRenderer(800, 600)
        self.voxels = []
        
        self.setup_ui()
        
        # Auto-rotate timer
        self.auto_rotate = False
        self.rotate_timer = QTimer()
        self.rotate_timer.timeout.connect(self._auto_rotate_step)
        self.rotate_speed = 1.0
        
    def setup_ui(self):
        """Create UI elements"""
        layout = QVBoxLayout()
        
        # Preview label
        self.preview_label = QLabel()
        self.preview_label.setMinimumSize(800, 600)
        self.preview_label.setStyleSheet("background-color: #1a1a1a;")
        layout.addWidget(self.preview_label)
        
        # Rotation X slider
        self.slider_x = QSlider(Qt.Orientation.Horizontal)
        self.slider_x.setRange(-180, 180)
        self.slider_x.setValue(30)
        self.slider_x.valueChanged.connect(self._on_rotation_change)
        layout.addWidget(QLabel("Rotation X:"))
        layout.addWidget(self.slider_x)
        
        # Rotation Y slider
        self.slider_y = QSlider(Qt.Orientation.Horizontal)
        self.slider_y.setRange(-180, 180)
        self.slider_y.setValue(45)
        self.slider_y.valueChanged.connect(self._on_rotation_change)
        layout.addWidget(QLabel("Rotation Y:"))
        layout.addWidget(self.slider_y)
        
        # Thickness slider
        self.slider_thickness = QSlider(Qt.Orientation.Horizontal)
        self.slider_thickness.setRange(1, 20)
        self.slider_thickness.setValue(3)
        self.slider_thickness.valueChanged.connect(self._on_settings_change)
        layout.addWidget(QLabel("Coin Thickness:"))
        layout.addWidget(self.slider_thickness)
        
        self.setLayout(layout)
    
    def load_pixel_art(self, image_path_or_array):
        """
        Load pixel art and generate 3D coin
        
        Args:
            image_path_or_array: Either file path string or numpy array
        """
        # Load image
        if isinstance(image_path_or_array, str):
            img = Image.open(image_path_or_array).convert('RGBA')
            image_array = np.array(img)
        else:
            image_array = image_path_or_array
        
        # Update thickness setting
        thickness = self.slider_thickness.value() / 10.0
        self.converter.settings.thickness = thickness
        
        # Convert to voxels
        self.voxels = self.converter.convert_image_to_voxels(image_array)
        
        # Load into renderer
        self.renderer.load_voxels(self.voxels)
        
        # Update preview
        self.update_preview()
    
    def _on_rotation_change(self):
        """Handle rotation slider changes"""
        self.renderer.set_rotation(
            self.slider_x.value(),
            self.slider_y.value()
        )
        self.update_preview()
    
    def _on_settings_change(self):
        """Handle settings changes - requires regeneration"""
        if hasattr(self, 'last_image_array'):
            self.load_pixel_art(self.last_image_array)
    
    def update_preview(self):
        """Render and display the 3D coin"""
        if not self.voxels:
            return
        
        # Render to numpy array
        image_array = self.renderer.render()
        
        # Convert to QPixmap
        height, width = image_array.shape[:2]
        bytes_per_line = 4 * width
        
        q_image = QImage(
            image_array.data,
            width, height,
            bytes_per_line,
            QImage.Format.Format_RGBA8888
        )
        
        pixmap = QPixmap.fromImage(q_image)
        self.preview_label.setPixmap(pixmap)
    
    def toggle_auto_rotate(self, enabled: bool):
        """Enable/disable automatic rotation"""
        self.auto_rotate = enabled
        if enabled:
            self.rotate_timer.start(16)  # ~60 FPS
        else:
            self.rotate_timer.stop()
    
    def _auto_rotate_step(self):
        """Step function for auto-rotation"""
        current_y = self.slider_y.value()
        new_y = (current_y + self.rotate_speed) % 360
        self.slider_y.setValue(int(new_y))
```

---

## 6. Usage Example

```python
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    
    # Create coin preview widget
    preview = CoinPreviewWidget()
    preview.setWindowTitle("2.5D Pixel Art Coin Viewer")
    preview.show()
    
    # Load example pixel art
    preview.load_pixel_art("path/to/your/pixel_art.png")
    
    # Enable auto-rotation
    preview.toggle_auto_rotate(True)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

---

## 7. Advanced Features to Add

### A. Export Options
```python
def export_as_obj(voxels: List[Voxel], filepath: str):
    """Export coin as OBJ file for 3D printing"""
    # Generate mesh from voxels
    # Write OBJ format
    pass

def export_animation(renderer: CoinRenderer, 
                     output_path: str, 
                     num_frames: int = 60):
    """Export rotating coin as GIF/video"""
    from PIL import Image
    
    frames = []
    for i in range(num_frames):
        angle = (i / num_frames) * 360
        renderer.set_rotation(30, angle)
        frame = renderer.render()
        frames.append(Image.fromarray(frame))
    
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=33,  # ~30 FPS
        loop=0
    )
```

### B. Lighting Control
```python
class LightingSettings:
    ambient_strength: float = 0.3
    diffuse_strength: float = 0.6
    specular_strength: float = 0.3
    light_position: Tuple[float, float, float] = (5.0, 5.0, 5.0)
```

### C. Material Presets
```python
MATERIAL_PRESETS = {
    "gold": {
        "metallic": 0.9,
        "roughness": 0.3,
        "color_tint": (1.0, 0.843, 0.0)
    },
    "silver": {
        "metallic": 0.95,
        "roughness": 0.2,
        "color_tint": (0.972, 0.960, 0.915)
    },
    "bronze": {
        "metallic": 0.8,
        "roughness": 0.4,
        "color_tint": (0.804, 0.498, 0.196)
    }
}
```

---

## Summary

This specification provides:

1. **Complete algorithm** for converting 2D pixel art to 3D voxel coins
2. **Production-ready renderer** using ModernGL with instanced rendering
3. **Qt integration** for desktop application
4. **Configurable parameters**: thickness, beveling