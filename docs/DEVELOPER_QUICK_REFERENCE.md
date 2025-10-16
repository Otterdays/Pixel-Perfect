# Developer Quick Reference

**For Pixel Perfect Development**

## 🚨 CRITICAL: Adding New Modules

**Every time you create a new Python module, you MUST update the build script:**

### 1. Create your module
```python
# src/ui/my_new_feature_manager.py
class MyNewFeatureManager:
    pass
```

### 2. Update build script
**File:** `BUILDER/build.bat`  
**Add:** `--hidden-import=src.ui.my_new_feature_manager`

**Example fix (Background Mode Toggle):**
```batch
--hidden-import=src.ui.grid_control_manager --hidden-import=src.ui.background_control_manager --hidden-import=src.ui.notes_panel
```

### 3. Test build
```batch
cd BUILDER
build.bat
```

### 4. Test executable
```batch
BUILDER\dist\PixelPerfect.exe
```

---

## Common Commands

```batch
# Test Python version
python main.py

# Build executable
cd BUILDER && build.bat

# Clean build
cd BUILDER
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
```

---

## File Locations

| File | Purpose |
|------|---------|
| `BUILDER/build.bat` | **Main build script** (edit this for new modules) |
| `docs/BUILD_SYSTEM.md` | Complete build documentation |
| `BUILDER/dist/PixelPerfect.exe` | Built executable |
| `BUILDER/release/PixelPerfect/` | Distribution package |

---

## Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'ui.some_module'` | New module not in build script | Add `--hidden-import=src.path.to.module` |
| Build fails with import errors | Excluded module still imported | Remove from `--exclude-module` or remove imports |
| EXE runs but features missing | Module excluded but needed | Add to `--hidden-import` list |

---

## Current Hidden Imports

Keep this list updated in `build.bat`:

```batch
--hidden-import=src.core.canvas
--hidden-import=src.core.canvas_renderer
--hidden-import=src.core.color_palette
--hidden-import=src.core.custom_colors
--hidden-import=src.core.event_dispatcher
--hidden-import=src.core.layer_manager
--hidden-import=src.core.project
--hidden-import=src.core.undo_manager
--hidden-import=src.core.saved_colors
--hidden-import=src.core.window_state_manager
--hidden-import=src.tools.base_tool
--hidden-import=src.tools.brush
--hidden-import=src.tools.eraser
--hidden-import=src.tools.eyedropper
--hidden-import=src.tools.fill
--hidden-import=src.tools.selection
--hidden-import=src.tools.shapes
--hidden-import=src.tools.pan
--hidden-import=src.tools.texture
--hidden-import=src.ui.main_window
--hidden-import=src.ui.dialog_manager
--hidden-import=src.ui.file_operations_manager
--hidden-import=src.ui.selection_manager
--hidden-import=src.ui.tool_size_manager
--hidden-import=src.ui.canvas_zoom_manager
--hidden-import=src.ui.grid_control_manager
--hidden-import=src.ui.background_control_manager
--hidden-import=src.ui.notes_panel
--hidden-import=src.ui.theme_dialog_manager
--hidden-import=src.ui.ui_builder
--hidden-import=src.ui.layer_panel
--hidden-import=src.ui.timeline_panel
--hidden-import=src.ui.color_wheel
--hidden-import=src.ui.theme_manager
--hidden-import=src.ui.tooltip
--hidden-import=src.ui.import_png_dialog
--hidden-import=src.ui.canvas_operations_manager
--hidden-import=src.ui.layer_animation_manager
--hidden-import=src.ui.color_view_manager
--hidden-import=src.ui.loading_screen
--hidden-import=src.ui.palette_views
--hidden-import=src.ui.palette_views.grid_view
--hidden-import=src.ui.palette_views.primary_view
--hidden-import=src.ui.palette_views.constants_view
--hidden-import=src.ui.palette_views.saved_view
--hidden-import=src.utils.export
--hidden-import=src.utils.import_png
--hidden-import=src.utils.presets
--hidden-import=src.utils.file_association
--hidden-import=src.animation.timeline
```

---

**📖 For detailed information, see [BUILD_SYSTEM.md](BUILD_SYSTEM.md)**
