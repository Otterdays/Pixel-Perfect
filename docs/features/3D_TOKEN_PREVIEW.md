# 3D Token Preview — Implementation Plan 🪙

## Status: PLANNED
**Priority**: High (User Requested)  
**Target Version**: v3.0  
**Last Updated**: February 19, 2026  
**Existing Spec**: `DOCS/technical/3D_TOKEN_DESIGN.md` (full algorithm + shader code)

---

## Goal

Add a "3D Token Preview" panel that transforms the current canvas pixel art into a spinning, interactive 3D coin/medallion directly inside Pixel Perfect. The artist sees their pixel art extruded into a voxel coin with real-time rotation, lighting, and material controls.

---

## Key Decision: Rendering Approach

The existing spec (`3D_TOKEN_DESIGN.md`) uses **ModernGL + PyQt6**. However, Pixel Perfect is a **CustomTkinter** app. We need a tkinter-compatible solution.

### Option A: Software Rasterizer (Pillow) ← **RECOMMENDED for v1**
- **Pros**: Zero new dependencies, uses Pillow (already installed), works everywhere
- **Cons**: Slower rendering, no GPU acceleration, simpler lighting
- **How**: Pre-render voxel cube faces with perspective projection, composite into a Pillow image, display as tkinter canvas image (same pattern as mini preview)
- **Performance**: For 16×16 sprite = ~768 visible voxel faces at coin thickness 3 → renders in <50ms on modern hardware
- **For 64×64**: ~12,288 faces → may need optimizations (batch sort, skip occluded faces)

### Option B: ModernGL Offscreen Rendering
- **Pros**: GPU-accelerated, full shader pipeline, production quality
- **Cons**: Adds `moderngl` + `pyrr` dependencies, GPU driver requirements
- **How**: Create a headless ModernGL context, render to framebuffer, read pixels, display as Pillow→tkinter image
- **Note**: This is what the existing spec describes; it works but adds complexity

### Option C: Embedded OpenGL Widget
- **Pros**: True real-time 3D with full interactivity
- **Cons**: Heavy dependency (PyOpenGL or moderngl-window), tkinter integration is fragile
- **How**: Embed an OpenGL context inside a tkinter frame
- **Not recommended**: Tkinter + OpenGL is notoriously fragile on Windows

### **Recommendation**: Start with **Option A** (software rasterizer). If performance is insufficient for larger canvases, upgrade to **Option B** (offscreen ModernGL). Skip Option C.

---

## Implementation Phases

### Phase 1: Core Voxel Engine (Software)

**File**: `src/core/voxel_renderer.py`

#### Step 1: Pixel Art → Voxel Data
```
Input:  numpy RGBA array (H × W × 4)
Output: List of visible cube faces + colors
```
- Convert each non-transparent pixel into a voxel (cube) at position (x, y, z=0)
- Detect edge pixels (adjacent to transparency) → extrude as coin rim
- Generate back face = mirrored/embossed version at z=-thickness
- **Cull hidden faces**: Only output faces that are visible (no face between two adjacent voxels)

#### Step 2: 3D Projection
```
Input:  Voxel faces + camera rotation angles
Output: Projected 2D polygons with depth
```
- Simple perspective projection matrix (no library needed, just 4x4 multiply)
- Painter's algorithm: sort faces by depth, draw back-to-front
- Apply rotation (X and Y axes) from mouse drag

#### Step 3: Rasterize to Pillow Image
```
Input:  Sorted 2D polygons + colors
Output: PIL.Image (RGBA)
```
- Use `ImageDraw.polygon()` for each face
- Apply simple directional lighting: `brightness = ambient + max(0, dot(normal, light_dir))`
- Face normals are trivial (±X, ±Y, ±Z for cube faces)

#### Step 4: Display in Tkinter Panel
- New class: `TokenPreviewPanel` (similar to `ReferencePanel`)
- Place in right sidebar or as floating window
- Convert PIL Image → `ImageTk.PhotoImage` → display on canvas
- Re-render on rotation change (mouse drag on preview panel)

### Phase 2: Interactive Controls

#### Mouse Controls (on the preview panel)
- **Left-drag**: Rotate coin (X/Y)
- **Scroll wheel**: Zoom in/out
- **Double-click**: Reset to default angle

#### Slider Controls
- **Thickness**: Coin depth (1-10 voxel layers)
- **Bevel**: Edge bevel amount (0-3)
- **Light Angle**: Horizontal light direction (0°-360°)

#### Material Presets
- **Flat**: Direct pixel colors (default)
- **Gold**: Warm metallic tint + specular highlights
- **Silver**: Cool metallic tint + specular highlights
- **Bronze**: Warm deep metallic tint
- **Custom**: User picks a tint color

### Phase 3: Export & Advanced

#### Export Options
- **Export as PNG**: Rendered 3D preview at chosen size (256, 512, 1024px)
- **Export as GIF**: 360° auto-rotation animation (30-60 frames)
- **Export as OBJ**: Wavefront OBJ file for 3D printing / modeling software
- **Export as STL**: For direct 3D printing

#### Auto-Rotate
- Toggle button to spin the coin continuously
- Speed slider

#### Back Face Modes
- **Mirrored**: Horizontal flip of front
- **Embossed**: Grayscale relief version
- **Inverted**: Color-inverted version
- **Blank**: Flat coin back with rim only
- **Custom**: Different pixel art (from another layer or imported image)

---

## File Structure (Planned)

```
src/
├── core/
│   └── voxel_renderer.py     ← NEW: Voxel generation + software rasterizer
├── ui/
│   └── token_preview_panel.py ← NEW: UI panel with controls
```

---

## Dependency Analysis

### Option A (Software — Recommended)
| Dependency | Status | Purpose |
|-----------|--------|---------|
| numpy | ✅ Already installed | Voxel data, matrix math |
| Pillow | ✅ Already installed | Rasterization + display |
| **Total new deps** | **0** | |

### Option B (ModernGL — Future upgrade)
| Dependency | Status | Purpose |
|-----------|--------|---------|
| moderngl | ❌ New | GPU rendering context |
| pyrr | ❌ New | Matrix/vector math |
| **Total new deps** | **2** | |

---

## Performance Estimates (Software Rasterizer)

| Canvas Size | Voxels (approx) | Visible Faces | Est. Render Time |
|-------------|-----------------|---------------|-----------------|
| 8×8 | ~200 | ~600 | <5ms |
| 16×16 | ~768 | ~2,300 | <20ms |
| 32×32 | ~3,072 | ~9,200 | <80ms |
| 64×64 | ~12,288 | ~37,000 | ~300ms |
| 128×128 | ~49,152 | ~147,000 | ~2-3s (needs GPU) |

**Verdict**: Software rasterizer is viable up to 64×64. For 128+ canvases, should switch to Option B or limit token preview to a downsampled version.

---

## UI Integration Plan

### Where to Place It
1. **Right Sidebar Panel** (like Reference Panel) — collapsible, starts collapsed
2. **Toggle Shortcut**: `Shift+T` (T for Token)
3. **Menu Entry**: View → 3D Token Preview

### Panel Layout
```
┌──────────────────────────┐
│ 🪙 3D Token Preview  [×] │
├──────────────────────────┤
│                          │
│    [3D Coin Render]      │
│    (drag to rotate)      │
│                          │
├──────────────────────────┤
│ Thickness: [====●====]   │
│ Bevel:     [==●========] │
│ Light:     [======●====] │
├──────────────────────────┤
│ Material: [Gold      ▾]  │
│ Back Face: [Mirrored ▾]  │
├──────────────────────────┤
│ [🔄 Auto-Rotate]  [📤 Export] │
└──────────────────────────┘
```

---

## Step-by-Step Build Order

1. **`voxel_renderer.py`** — Core engine
   - `pixels_to_voxels(pixels, thickness, bevel)` → voxel list
   - `project_voxels(voxels, rot_x, rot_y, zoom)` → sorted screen faces
   - `render_to_image(faces, width, height, light_dir, material)` → PIL.Image

2. **`token_preview_panel.py`** — UI shell
   - Panel with canvas + sliders
   - Mouse drag rotation
   - Call `voxel_renderer` on every interaction
   - Display result as `ImageTk.PhotoImage`

3. **Integration** — Wire into main app
   - Import panel in `main_window.py`
   - Add to right sidebar
   - Add `Shift+T` shortcut in `event_dispatcher.py`
   - Auto-update when canvas changes (debounced, ~500ms delay)

4. **Export** — File output
   - PNG snapshot
   - GIF rotation animation
   - OBJ mesh export (future)

---

## References

- **Existing Spec**: `DOCS/technical/3D_TOKEN_DESIGN.md` — Full algorithm with ModernGL shaders
- **Suggestion Origin**: `DOCS/SUGGESTIONS.md` line 8: "2.5d-3d tokens"
- **Similar Feature**: Import PNG Dialog already has a spinning 3D preview concept
- **Pixel Art 3D Examples**: Aseprite voxel plugins, MagicaVoxel, Goxel
