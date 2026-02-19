"""
voxel_renderer.py

Software-based 3D voxel renderer for the Token Preview feature.
Converts 2D pixel art into a 3D coin/medallion visualization using
Pillow for rasterization — zero additional dependencies beyond numpy + Pillow.
"""

import numpy as np
import math
from PIL import Image, ImageDraw


class VoxelRenderer:
    """Renders pixel art as a 3D coin/token using software rasterization.
    
    Pipeline:
        1. Build visible surface faces from pixel data (cached)
        2. Rotate all vertices/normals via numpy batch multiply
        3. Back-face cull (normal.z <= 0)
        4. Compute per-face lighting (Blinn-Phong)
        5. Depth-sort (painter's algorithm)
        6. Rasterize with Pillow ImageDraw.polygon
    """

    # Material tint presets (RGB 0-1)
    MATERIALS = {
        'flat': None,
        'gold': (1.0, 0.843, 0.0),
        'silver': (0.87, 0.86, 0.82),
        'bronze': (0.804, 0.498, 0.196),
    }

    def __init__(self):
        # Camera
        self.rotation_x = 25.0    # vertical tilt (degrees)
        self.rotation_y = -35.0   # horizontal spin (degrees)
        self.zoom = 1.0

        # Coin geometry
        self.thickness = 3        # depth in voxel layers
        self.back_face_mode = 'mirrored'  # 'mirrored','embossed','same','blank'

        # Lighting
        self.light_yaw = 135.0    # horizontal angle (degrees)
        self.ambient = 0.35
        self.diffuse = 0.55
        self.specular = 0.10

        # Material
        self.material = 'flat'

        # Face cache (rebuilt when canvas/settings change)
        self._verts = None    # (N, 4, 3)
        self._normals = None  # (N, 3)
        self._colors = None   # (N, 4) in 0-255
        self._cache_key = None

    # ------------------------------------------------------------------ #
    #  Rotation matrix
    # ------------------------------------------------------------------ #
    def _rotation_matrix(self):
        """Combined Y-then-X rotation matrix."""
        rx = math.radians(self.rotation_x)
        ry = math.radians(self.rotation_y)
        cx, sx = math.cos(rx), math.sin(rx)
        cy, sy = math.cos(ry), math.sin(ry)
        return np.array([
            [cy,   sy * sx,   sy * cx],
            [0,    cx,        -sx],
            [-sy,  cy * sx,   cy * cx],
        ], dtype=np.float64)

    # ------------------------------------------------------------------ #
    #  Face generation (cached)
    # ------------------------------------------------------------------ #
    def _build_faces(self, pixels):
        """Generate visible surface quads from pixel data.

        Each non-transparent pixel is extruded by `thickness` layers.
        Only faces on the surface (adjacent to air) are emitted.
        Returns (verts, normals, colors) as numpy arrays.
        """
        h, w = pixels.shape[:2]
        t = self.thickness
        opaque = pixels[:, :, 3] > 10  # (h, w) bool

        # Back-face pixel colors
        if self.back_face_mode == 'mirrored':
            bpx = np.flip(pixels, axis=1)
        elif self.back_face_mode == 'embossed':
            g = np.mean(pixels[:, :, :3], axis=2, keepdims=True).astype(np.uint8)
            bpx = np.concatenate([g, g, g, pixels[:, :, 3:4]], axis=2)
        elif self.back_face_mode == 'blank':
            bpx = np.full_like(pixels, 60)
            bpx[:, :, 3] = pixels[:, :, 3]
        else:
            bpx = pixels

        cx, cy, cz = w / 2.0, h / 2.0, t / 2.0

        # Six canonical normals
        N_F = np.array([0, 0, 1], dtype=np.float64)
        N_B = np.array([0, 0, -1], dtype=np.float64)
        N_R = np.array([1, 0, 0], dtype=np.float64)
        N_L = np.array([-1, 0, 0], dtype=np.float64)
        N_U = np.array([0, 1, 0], dtype=np.float64)
        N_D = np.array([0, -1, 0], dtype=np.float64)

        v_list, n_list, c_list = [], [], []

        for row in range(h):
            for col in range(w):
                if not opaque[row, col]:
                    continue

                x = col - cx
                y = cy - row  # flip Y

                fc = pixels[row, col].astype(np.float64)
                bc = bpx[row, col].astype(np.float64)
                ec = fc.copy()
                ec[:3] *= 0.75  # darken edges

                # --- Front face (z = cz) ---
                v_list.append(np.array([
                    [x, y - 1, cz], [x + 1, y - 1, cz],
                    [x + 1, y, cz], [x, y, cz]
                ], dtype=np.float64))
                n_list.append(N_F)
                c_list.append(fc)

                # --- Back face (z = cz - t) ---
                zb = cz - t
                v_list.append(np.array([
                    [x, y, zb], [x + 1, y, zb],
                    [x + 1, y - 1, zb], [x, y - 1, zb]
                ], dtype=np.float64))
                n_list.append(N_B)
                c_list.append(bc)

                # --- Side faces (per z-layer, only at edges) ---
                nr = col + 1 >= w or not opaque[row, col + 1]
                nl = col - 1 < 0  or not opaque[row, col - 1]
                nu = row - 1 < 0  or not opaque[row - 1, col]
                nd = row + 1 >= h or not opaque[row + 1, col]

                for zi in range(t):
                    zt = cz - zi
                    zbot = zt - 1

                    if nr:
                        v_list.append(np.array([
                            [x+1, y-1, zt], [x+1, y-1, zbot],
                            [x+1, y, zbot], [x+1, y, zt]
                        ], dtype=np.float64))
                        n_list.append(N_R); c_list.append(ec)

                    if nl:
                        v_list.append(np.array([
                            [x, y, zt], [x, y, zbot],
                            [x, y-1, zbot], [x, y-1, zt]
                        ], dtype=np.float64))
                        n_list.append(N_L); c_list.append(ec)

                    if nu:
                        v_list.append(np.array([
                            [x, y, zt], [x+1, y, zt],
                            [x+1, y, zbot], [x, y, zbot]
                        ], dtype=np.float64))
                        n_list.append(N_U); c_list.append(ec)

                    if nd:
                        v_list.append(np.array([
                            [x, y-1, zbot], [x+1, y-1, zbot],
                            [x+1, y-1, zt], [x, y-1, zt]
                        ], dtype=np.float64))
                        n_list.append(N_D); c_list.append(ec)

        if not v_list:
            return np.empty((0, 4, 3)), np.empty((0, 3)), np.empty((0, 4))

        return (
            np.array(v_list, dtype=np.float64),
            np.array(n_list, dtype=np.float64),
            np.array(c_list, dtype=np.float64),
        )

    # ------------------------------------------------------------------ #
    #  Main render
    # ------------------------------------------------------------------ #
    def render(self, pixels, render_size=200):
        """Render pixel art as a 3D coin.

        Args:
            pixels: numpy RGBA array (H, W, 4)
            render_size: output image dimension in px

        Returns:
            PIL.Image RGBA
        """
        empty = Image.new("RGBA", (render_size, render_size), (0, 0, 0, 0))
        if pixels is None or pixels.size == 0:
            return empty

        h, w = pixels.shape[:2]

        # Downsample large canvases for performance
        cap = 48
        if w > cap or h > cap:
            from PIL import Image as _Img
            ratio = cap / max(w, h)
            nw, nh = max(1, int(w * ratio)), max(1, int(h * ratio))
            pixels = np.array(
                _Img.fromarray(pixels, "RGBA").resize((nw, nh), _Img.Resampling.NEAREST)
            )

        # Rebuild face cache if needed
        key = (pixels.tobytes(), self.thickness, self.back_face_mode)
        if self._cache_key != key:
            self._verts, self._normals, self._colors = self._build_faces(pixels)
            self._cache_key = key

        N = self._verts.shape[0]
        if N == 0:
            return empty

        R = self._rotation_matrix()

        # --- Batch rotate normals & cull ---
        rn = self._normals @ R.T          # (N, 3)
        vis = rn[:, 2] > 0
        idx = np.where(vis)[0]
        if idx.size == 0:
            return empty

        vis_n = rn[idx]
        vis_c = self._colors[idx]
        M = idx.size

        # --- Batch rotate vertices ---
        rv = self._verts[idx].reshape(-1, 3) @ R.T   # (M*4, 3)
        rv = rv.reshape(M, 4, 3)

        # --- Lighting (Blinn-Phong) ---
        ly = math.radians(self.light_yaw)
        ld = np.array([math.cos(ly), 0.5, math.sin(ly)], dtype=np.float64)
        ld /= np.linalg.norm(ld)

        diff = np.maximum(0.0, vis_n @ ld)

        vd = np.array([0, 0, 1], dtype=np.float64)
        hv = ld + vd
        hv /= np.linalg.norm(hv)
        spec = np.maximum(0.0, vis_n @ hv) ** 16

        bright = self.ambient + self.diffuse * diff + self.specular * spec

        # --- Depth sort (painter's) ---
        avg_z = rv[:, :, 2].mean(axis=1)
        order = np.argsort(avg_z)

        # --- Auto-scale ---
        xy = rv[:, :, :2].reshape(-1, 2)
        lo, hi = xy.min(0), xy.max(0)
        span = max(hi[0] - lo[0], hi[1] - lo[1], 0.001)
        pad = render_size * 0.08
        sc = (render_size - 2 * pad) / span * self.zoom
        ctr = (lo + hi) / 2
        half = render_size / 2

        # --- Rasterize ---
        img = Image.new("RGBA", (render_size, render_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        tint = self.MATERIALS.get(self.material)

        for i in order:
            fv = rv[i]           # (4, 3)
            cr, cg, cb, ca = vis_c[i]
            br = bright[i]

            # Normalize color
            r, g, b = cr / 255.0, cg / 255.0, cb / 255.0

            # Material tint
            if tint is not None:
                if self.material == 'silver':
                    gray = 0.299 * r + 0.587 * g + 0.114 * b
                    r = gray * 0.5 + tint[0] * 0.5
                    g = gray * 0.5 + tint[1] * 0.5
                    b = gray * 0.5 + tint[2] * 0.5
                else:
                    r = r * 0.4 + tint[0] * 0.6
                    g = g * 0.4 + tint[1] * 0.6
                    b = b * 0.4 + tint[2] * 0.6

            r = min(255, int(min(1.0, r * br) * 255))
            g = min(255, int(min(1.0, g * br) * 255))
            b = min(255, int(min(1.0, b * br) * 255))

            pts = []
            for vx, vy in fv[:, :2]:
                sx = half + (vx - ctr[0]) * sc
                sy = half - (vy - ctr[1]) * sc
                pts.append((sx, sy))

            draw.polygon(pts, fill=(r, g, b, int(ca)))

        return img

    def invalidate_cache(self):
        """Force rebuild on next render."""
        self._cache_key = None
