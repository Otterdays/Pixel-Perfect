# Godot Engine Export Integration
**Feature Status**: 🔨 Phase 1 In Progress  
**Version Target**: v2.10.0  
**Date**: February 19, 2026

---

## Overview

Pixel Perfect exports pixel art assets optimized for the Godot Engine (4.x).  
The goal: **one click → drag into Godot → it just works.**

Currently, Pixel Perfect exports PNG, GIF, and sprite sheets with JSON metadata.
Godot needs specific formatting and can auto-import custom resource files (`.tres`)
that eliminate manual setup.

---

## What Godot Needs from Pixel Art

### Critical Import Settings
Godot will **blur pixel art** unless these are set correctly:

| Setting | Value | Why |
|---------|-------|-----|
| **Filter** | `Nearest` | Prevents bilinear interpolation blur |
| **Mipmaps** | `Off` | Mipmaps blend pixel edges at distance |
| **Repeat** | `Disabled` | Unless it's a tileset |
| **Compress Mode** | `Lossless` | Preserves exact pixel colors |

### Sprite Sheet Requirements
- **Zero spacing** between frames (Godot's frame grid assumes tightly packed)
- **Consistent frame size** (every cell same width × height)
- **Horizontal or grid layout** preferred (`AnimatedSprite2D` reads left-to-right, top-to-bottom)

### File Formats Godot Accepts
- `.png` — Standard sprite/texture (preferred)
- `.tres` — Godot text resource (SpriteFrames, AtlasTexture, etc.)
- `.tscn` — Godot scene file (ready-to-use nodes)
- `.obj` — 3D mesh (for token/coin 3D objects)
- `.import` — Godot's auto-import settings

---

## Export Modes

### 1. Single Sprite Export
**Use case**: A single item, icon, weapon, character pose, token, etc.

**Outputs**:
- `sprite_name.png` — The sprite at 1x (native resolution)
- `sprite_name.png.import` — Godot import preset (Nearest filter, lossless)

### 2. Animated Sprite Sheet Export
**Use case**: Character walk cycle, attack animation, idle loop, etc.

**Outputs**:
- `sprite_name_sheet.png` — All frames packed with zero spacing
- `sprite_name.tres` — Godot `SpriteFrames` resource with frame regions + FPS
- `sprite_name_scene.tscn` — Ready-to-use `AnimatedSprite2D` scene (optional)
- `sprite_name_sheet.png.import` — Import preset

**SpriteFrames .tres format** (Godot 4.x):
```
[gd_resource type="SpriteFrames" load_steps=N format=3]

[ext_resource type="Texture2D" path="res://path/sprite_name_sheet.png" id="1"]

[sub_resource type="AtlasTexture" id="atlas_0"]
atlas = ExtResource("1")
region = Rect2(0, 0, 32, 32)

[sub_resource type="AtlasTexture" id="atlas_1"]
atlas = ExtResource("1")
region = Rect2(32, 0, 32, 32)

[resource]
animations = [{
"frames": [{
"duration": 1.0,
"texture": SubResource("atlas_0")
}, {
"duration": 1.0,
"texture": SubResource("atlas_1")
}],
"loop": true,
"name": &"default",
"speed": 10.0
}]
```

### 3. Tileset Export
**Use case**: Terrain tiles, dungeon tiles, world-building blocks.

**Outputs**:
- `tileset_name.png` — Tightly packed grid
- Metadata with tile size for Godot TileMap setup

### 4. 3D Token Export (Future)
**Use case**: Coins, medallions, collectibles as 3D objects in Godot.

**Outputs**:
- `token_name.obj` + `token_name.mtl` — 3D mesh + material
- `token_name_diffuse.png` — Texture map for the mesh
- Or: `token_name_render.png` for use as `Sprite3D` billboard

---

## Godot Import Preset File (.import)

Godot auto-creates `.import` files when you drag assets into a project.
We can pre-generate these so Godot applies the correct pixel art settings:

```ini
[remap]
path="res://.godot/imported/sprite.png-<hash>.ctex"
type="CompressedTexture2D"

[deps]
source_file="res://sprites/sprite.png"
dest_files=["res://.godot/imported/sprite.png-<hash>.ctex"]

[params]
compress/mode=0
compress/high_quality=false
mipmaps/generate=false
roughness/mode=0
process/fix_alpha_border=true
process/premult_alpha=false
process/normal_map_invert_y=false
process/hdr_as_srgb=false
process/size_limit=0
detect_3d/compress_to=0
texture_format/bptc_lz4=false
```

> **Note**: In practice, it's simpler to provide a README with import instructions
> rather than generating `.import` files, since Godot regenerates them on import.

---

## Implementation Architecture

### New Module: `src/utils/godot_export.py`

```
GodotExporter
├── export_sprite()          → Single PNG + import instructions
├── export_sprite_sheet()    → Packed sheet + .tres SpriteFrames
├── export_scene()           → .tscn with AnimatedSprite2D node
├── _generate_tres()         → Build .tres text content
├── _generate_tscn()         → Build .tscn text content 
├── _generate_readme()       → Godot import instructions
└── _make_packed_sheet()     → Zero-spacing sprite sheet builder
```

### Integration Points
- **Export Dialog** — Add "Godot Export" tab/option alongside existing PNG/GIF/Sheet
- **3D Token Panel** — Add "Export for Godot" button 
- **Keyboard Shortcut** — Consider Ctrl+Shift+G or similar

### Dependencies
- **None new** — Uses Pillow (already installed) for image manipulation
- Godot `.tres` and `.tscn` are plain text formats we generate as strings

---

## Phase Plan

### Phase 1: Core Godot Export ← CURRENT
- [x] Feature specification document
- [x] `GodotExporter` module with sprite + sheet + .tres export
- [ ] Wire into export dialog / menu
- [ ] Test with Godot 4.x project

### Phase 2: Scene Files & Polish
- [ ] `.tscn` AnimatedSprite2D scene generation
- [ ] Tileset export mode
- [ ] Animation name support (walk, idle, attack, etc.)
- [ ] Multi-animation export (multiple animation rows)
- [ ] Power-of-2 padding option

### Phase 3: 3D Token Godot Integration
- [ ] OBJ mesh export of voxel coin
- [ ] Godot MeshInstance3D scene generation
- [ ] Sprite3D billboard export option

---

## Godot Quick-Start Guide (for Users)

### Importing a Single Sprite
1. Export from Pixel Perfect → "Export for Godot"
2. Copy the `.png` file into your Godot project's `res://` folder
3. In Godot, select the imported texture → Import tab → Preset: **2D Pixel**
4. Click **Reimport**
5. Create a `Sprite2D` node and assign the texture

### Importing an Animated Sprite Sheet
1. Export from Pixel Perfect → "Export Sprite Sheet for Godot"
2. Copy both the `.png` and `.tres` files into your Godot project
3. Create an `AnimatedSprite2D` node
4. Assign the `.tres` file as the `SpriteFrames` resource
5. Hit Play — animation should work immediately!

### Pixel Art Import Checklist
- [ ] Texture filter set to **Nearest**  
- [ ] Project Settings → Rendering → Textures → Default Texture Filter: **Nearest**
- [ ] Stretch Mode: `canvas_items` (for pixel-perfect rendering)
- [ ] Window size is a multiple of your game resolution

---

## Design Principles
1. **Zero config in Godot** — Exports should work without manual setup
2. **No new dependencies** — .tres and .tscn are plain text, PNG via Pillow
3. **Non-destructive** — Godot export doesn't modify the Pixel Perfect project
4. **Godot 4.x format** — Target format version 3 (Godot 4.0+)
5. **Pixel art first** — Always NEAREST filter, lossless compression
