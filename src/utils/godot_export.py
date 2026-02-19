"""
Godot Engine Export Utilities for Pixel Perfect

Exports pixel art assets in Godot 4.x-ready formats:
- PNG sprites with correct import settings
- Sprite sheets (zero spacing, grid-aligned)
- .tres SpriteFrames resources (auto-configures animation in Godot)
- .tscn scene files (ready-to-use AnimatedSprite2D nodes)
- Import instructions README

Zero additional dependencies — generates plain text Godot resource files.

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import os
import json
import math
from typing import List, Optional
from PIL import Image
import numpy as np


class GodotExporter:
    """Exports Pixel Perfect assets in Godot Engine 4.x compatible formats."""

    def __init__(self):
        self.godot_res_path = "res://sprites"  # Default Godot resource path
        self.animation_fps = 10.0              # Default animation speed
        self.animation_name = "default"        # Default animation name
        self.loop = True                       # Loop animation by default

    # ------------------------------------------------------------------ #
    #  Single Sprite Export
    # ------------------------------------------------------------------ #
    def export_sprite(self, pixels: np.ndarray, filepath: str,
                      scale: int = 1, generate_readme: bool = True) -> bool:
        """Export a single sprite as a Godot-ready PNG.

        Args:
            pixels: RGBA numpy array (H, W, 4)
            filepath: Output .png path
            scale: Scale factor (NEAREST resampling)
            generate_readme: Whether to write import instructions

        Returns:
            True on success
        """
        try:
            img = Image.fromarray(pixels, "RGBA")

            if scale > 1:
                h, w = pixels.shape[:2]
                img = img.resize((w * scale, h * scale), Image.Resampling.NEAREST)

            img.save(filepath, "PNG")

            if generate_readme:
                readme_path = os.path.join(os.path.dirname(filepath), "GODOT_IMPORT_README.txt")
                if not os.path.exists(readme_path):
                    self._generate_readme(readme_path)

            return True
        except Exception as e:
            print(f"[GodotExporter] Sprite export error: {e}")
            return False

    # ------------------------------------------------------------------ #
    #  Sprite Sheet Export (with .tres)
    # ------------------------------------------------------------------ #
    def export_sprite_sheet(self, frames: List[np.ndarray], filepath: str,
                            scale: int = 1, columns: Optional[int] = None,
                            animation_name: str = "default",
                            fps: float = 10.0, loop: bool = True,
                            generate_tres: bool = True,
                            generate_tscn: bool = False,
                            generate_readme: bool = True) -> bool:
        """Export animation frames as a Godot-ready sprite sheet.

        Produces:
        - {name}_sheet.png  — Tightly packed sprite sheet (zero spacing)
        - {name}.tres       — Godot SpriteFrames resource
        - {name}_scene.tscn — Optional AnimatedSprite2D scene

        Args:
            frames: List of RGBA numpy arrays (all same size)
            filepath: Base output path (without suffix; we add _sheet.png etc.)
            scale: Scale factor for the sheet
            columns: Number of columns in the grid (auto-calculated if None)
            animation_name: Name for the animation in Godot
            fps: Animation playback speed (frames per second)
            loop: Whether the animation loops
            generate_tres: Generate .tres SpriteFrames resource
            generate_tscn: Generate .tscn scene file
            generate_readme: Write import instructions

        Returns:
            True on success
        """
        try:
            if not frames:
                return False

            frame_count = len(frames)
            fh, fw = frames[0].shape[:2]

            # Auto-calculate columns for a roughly square grid
            if columns is None:
                columns = min(frame_count, max(1, int(math.ceil(math.sqrt(frame_count)))))
            rows = int(math.ceil(frame_count / columns))

            # Build the sprite sheet image (zero spacing)
            sheet_w = fw * columns
            sheet_h = fh * rows
            sheet = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))

            for i, frame_pixels in enumerate(frames):
                col = i % columns
                row = i // columns
                frame_img = Image.fromarray(frame_pixels, "RGBA")
                sheet.paste(frame_img, (col * fw, row * fh), frame_img)

            # Scale if needed
            if scale > 1:
                sheet = sheet.resize(
                    (sheet_w * scale, sheet_h * scale),
                    Image.Resampling.NEAREST,
                )
                fw *= scale
                fh *= scale
                sheet_w *= scale
                sheet_h *= scale

            # Determine output paths
            base = filepath
            if base.lower().endswith(".png"):
                base = base[:-4]

            sheet_path = f"{base}_sheet.png"
            tres_path = f"{base}.tres"
            tscn_path = f"{base}_scene.tscn"

            # Save the sheet
            sheet.save(sheet_path, "PNG")

            # Determine the Godot resource path (relative)
            sheet_filename = os.path.basename(sheet_path)
            godot_texture_path = f"{self.godot_res_path}/{sheet_filename}"

            # Generate .tres SpriteFrames
            if generate_tres:
                tres_content = self._generate_tres(
                    texture_path=godot_texture_path,
                    frame_width=fw,
                    frame_height=fh,
                    frame_count=frame_count,
                    columns=columns,
                    animation_name=animation_name,
                    fps=fps,
                    loop=loop,
                )
                with open(tres_path, "w", encoding="utf-8") as f:
                    f.write(tres_content)

            # Generate .tscn scene
            if generate_tscn:
                tres_filename = os.path.basename(tres_path)
                godot_tres_path = f"{self.godot_res_path}/{tres_filename}"
                tscn_content = self._generate_tscn(
                    sprite_frames_path=godot_tres_path,
                    animation_name=animation_name,
                )
                with open(tscn_path, "w", encoding="utf-8") as f:
                    f.write(tscn_content)

            # Also export the JSON metadata (our existing format, for reference)
            meta_path = f"{base}_metadata.json"
            meta = {
                "exporter": "Pixel Perfect — Godot Export",
                "godot_version": "4.x",
                "animation_name": animation_name,
                "frame_count": frame_count,
                "frame_width": fw,
                "frame_height": fh,
                "columns": columns,
                "rows": rows,
                "fps": fps,
                "loop": loop,
                "scale": scale,
                "sheet_file": sheet_filename,
                "tres_file": os.path.basename(tres_path) if generate_tres else None,
            }
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)

            if generate_readme:
                readme_path = os.path.join(os.path.dirname(filepath), "GODOT_IMPORT_README.txt")
                if not os.path.exists(readme_path):
                    self._generate_readme(readme_path)

            return True
        except Exception as e:
            print(f"[GodotExporter] Sheet export error: {e}")
            return False

    # ------------------------------------------------------------------ #
    #  .tres SpriteFrames Generator
    # ------------------------------------------------------------------ #
    def _generate_tres(self, texture_path: str, frame_width: int,
                       frame_height: int, frame_count: int, columns: int,
                       animation_name: str = "default",
                       fps: float = 10.0, loop: bool = True) -> str:
        """Generate Godot 4.x SpriteFrames .tres resource content.

        This creates a text-based resource file that Godot can load directly.
        It defines AtlasTexture sub-resources for each frame region, then
        bundles them into a SpriteFrames animation.
        """
        lines = []

        # Header — load_steps = 1 (texture) + frame_count (atlas textures) + 1 (resource)
        load_steps = 1 + frame_count + 1
        lines.append(f'[gd_resource type="SpriteFrames" load_steps={load_steps} format=3]')
        lines.append("")

        # External resource: the sprite sheet texture
        lines.append(f'[ext_resource type="Texture2D" path="{texture_path}" id="1"]')
        lines.append("")

        # Sub-resources: one AtlasTexture per frame
        for i in range(frame_count):
            col = i % columns
            row = i // columns
            x = col * frame_width
            y = row * frame_height

            atlas_id = f"atlas_{i}"
            lines.append(f'[sub_resource type="AtlasTexture" id="{atlas_id}"]')
            lines.append('atlas = ExtResource("1")')
            lines.append(f"region = Rect2({x}, {y}, {frame_width}, {frame_height})")
            lines.append("")

        # Main resource: SpriteFrames with animation data
        lines.append("[resource]")

        # Build frame array entries
        frame_entries = []
        for i in range(frame_count):
            atlas_id = f"atlas_{i}"
            frame_entries.append(f'{{\n"duration": 1.0,\n"texture": SubResource("{atlas_id}")\n}}')

        frames_str = ", ".join(frame_entries)

        loop_str = "true" if loop else "false"
        lines.append(f'animations = [{{"frames": [{frames_str}], "loop": {loop_str}, "name": &"{animation_name}", "speed": {fps}}}]')
        lines.append("")

        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    #  .tscn Scene Generator
    # ------------------------------------------------------------------ #
    def _generate_tscn(self, sprite_frames_path: str,
                       animation_name: str = "default") -> str:
        """Generate a Godot 4.x .tscn file with an AnimatedSprite2D node.

        Drag this into your Godot scene tree and the sprite is ready to play.
        """
        lines = [
            '[gd_scene load_steps=2 format=3]',
            '',
            f'[ext_resource type="SpriteFrames" path="{sprite_frames_path}" id="1"]',
            '',
            '[node name="Sprite" type="AnimatedSprite2D"]',
            'sprite_frames = ExtResource("1")',
            f'animation = &"{animation_name}"',
            'texture_filter = 0',
            '',
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    #  README / Import Instructions
    # ------------------------------------------------------------------ #
    def _generate_readme(self, filepath: str):
        """Write Godot import instructions alongside exported files."""
        content = """==========================================================
  Pixel Perfect → Godot Import Guide
==========================================================

HOW TO USE THESE FILES IN GODOT
-------------------------------

1. COPY all exported files into your Godot project folder
   (e.g., res://sprites/ or res://assets/)

2. SWITCH to Godot — it will auto-detect the new files

3. SELECT the .png file in the FileSystem dock

4. In the IMPORT tab (top of the Inspector):
   - Click "Preset" dropdown → choose "2D Pixel"
   - Or manually set:
       • Filter: Nearest
       • Mipmaps: Off  
       • Compress Mode: Lossless
   - Click "Reimport"

5. For ANIMATED SPRITES:
   - If a .tres file was generated:
     → Create an AnimatedSprite2D node
     → Drag the .tres file onto the "Sprite Frames" property
     → Done! Press Play to see the animation
   
   - If a .tscn file was generated:
     → Just drag it into your scene tree — ready to go!

GODOT PROJECT SETTINGS (one-time setup)
---------------------------------------
For pixel-perfect rendering in your entire project:

  Project → Project Settings → Rendering → Textures:
    • Default Texture Filter: Nearest

  Project → Project Settings → Display → Window:
    • Stretch Mode: canvas_items
    • Stretch Aspect: keep

  This prevents ALL textures from being blurred.

NOTES
-----
• Sprite sheets use ZERO spacing between frames
  (Godot's AnimatedSprite2D expects tightly packed grids)

• All exports use NEAREST neighbor scaling to preserve
  crisp pixel art edges

• The _metadata.json file contains frame layout info
  for custom import scripts

==========================================================
  Exported by Pixel Perfect — Diamond Clad Studios
==========================================================
"""
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            print(f"[GodotExporter] README write error: {e}")
