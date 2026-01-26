# Pixel Perfect - Polish & Enhancement Checklist

**Last Updated**: January 25, 2026
**Status**: Active Development Roadmap
**Target**: Rival Top-Tier Image Creation Software (Aseprite, Photoshop, Procreate)

---

## 🎨 Visual & Theme Enhancements

- [x] **1. Theme Customization Panel** ✅ COMPLETE (v2.7.6)
  - [x] Let users tweak theme colors (backgrounds, accents, text)
  - [x] Save custom themes
  - [x] Export/import theme files
  - [x] Preview before applying

- [ ] **2. UI Scale/DPI Controls**
  - [ ] Slider for UI scale (100%, 125%, 150%, 200%)
  - [ ] Separate font size control
  - [ ] Useful for high-DPI displays

- [ ] **3. More Theme Variants**
  - [ ] Retro CRT (green/amber monochrome)
  - [ ] High Contrast (accessibility)
  - [ ] Midnight Blue (dark blue variant)
  - [ ] Sepia (warm brown tones)
  - [ ] **Cyberpunk Neon** (Deep purples, glowing cyan/pink accents)
  - [ ] **Gameboy Classic** (4-color green palette UI)
  - [ ] **Nord/Dracula** (Popular developer themes)
  - [ ] **Paper Sketch** (High brightness, low contrast, pencil aesthetic)

- [ ] **4. Canvas Rotation/Flip View (Non-Destructive)**
  - [ ] Rotate/flip view only (not the canvas)
  - [ ] Helps with perspective checks
  - [ ] Keyboard shortcuts: `[` / `]` or `Ctrl+R`

- [ ] **26. UI Animations & Feedback**
  - [ ] Micro-animations on button hover/click (scale/brightness)
  - [ ] Smooth transitions for panel collapse/expand
  - [ ] "Juicy" UI feedback (particles/flash on critical actions)
  - [ ] Toast notifications for save/export/errors (non-intrusive)

- [ ] **27. Cursor Customization**
  - [ ] Crosshair, Brush Outline, Icon, or "Pro" dot cursor
  - [ ] High-visibility cursor mode (inverted colors)
  - [ ] Brush size outline constantly visible (optional)

- [ ] **28. Zen Mode**
  - [ ] Single hotkey (`Tab` or `F`) to hide ALL UI interactions
  - [ ] Only canvas visible, centered on dark background
  - [ ] Floating minimal toolbar on hover

---

## 🖌️ Next-Gen Drawing Engine

- [ ] **29. Pixel-Perfect Line Algorithm**
  - [ ] Auto-remove "L-shapes" (corner cleaning) for crisp pixel lines
  - [ ] Toggleable per brush

- [ ] **30. Symmetry Painting System**
  - [ ] X-axis, Y-axis, active mirrors
  - [ ] Radial/Mandala symmetry (3 to 12 points)
  - [ ] Adjustable center point for symmetry

- [ ] **31. Jitter & Dynamics**
  - [ ] Position/Scatter jitter
  - [ ] Color jitter (Hue/Sat/Val per pixel)
  - [ ] Opacity jitter (Pressure simulation for mouse users)

- [ ] **32. Shading Brush ("Shading Mode")**
  - [ ] Lighten/Darken based on current palette index
  - [ ] "Lock Alpha" mode for shading inside existing pixels only
  - [ ] Dither brush mode (auto-checkerboard)

- [ ] **33. Gradient Tool 2.0**
  - [ ] Linear, Radial, and Angle gradients
  - [ ] Dithering support for gradients (Bayer, Floyd-Steinberg)
  - [ ] Palette-constraint (gradient snaps to palette colors only)

- [ ] **34. Contour / Filled Stroke**
  - [ ] Tool to draw filled shapes directly (lasso fill)
  - [ ] "Closing" functionality for unclosed lines

- [ ] **35. "Sticky" Tool Keys (Spring-loaded)**
  - [ ] Hold key to switch tool, release to switch back
  - [ ] Example: Hold `E` to erase, release to return to Brush

- [ ] **36. Tile Mode Painting (Wraparound)**
  - [ ] Painting on the edge appears on the opposite side
  - [ ] Visual preview of adjacent tiles (already in v2.7.5, but implement *painting* logic)

---

## ⚡ Quality of Life Improvements

- [ ] **5. Copy/Paste Keyboard Shortcuts**
  - [ ] `Ctrl+C` / `Ctrl+V` for selection
  - [ ] `Ctrl+Shift+C` / `Ctrl+Shift+V` for copy/paste between projects
  - [ ] Visual paste preview before placing

- [x] **6. Middle Mouse Button Pan**
  - [ ] Middle-click + drag to pan
  - [ ] Common in art apps
  - [ ] Alternative to pan tool

- [ ] **7. Spacebar Temporary Pan**
  - [ ] Hold Space + drag = temporary pan
  - [ ] Release Space = return to previous tool
  - [ ] Faster than switching tools

- [ ] **8. Number Keys for Quick Tool Selection**
  - [ ] `1` = Brush, `2` = Eraser, `3` = Fill, `4` = Eyedropper, etc.
  - [ ] Tools mapping customizable

- [x] **9. Tab Key Panel Toggle**
  - [ ] `Tab` = hide/show all panels (maximize canvas)
  - [ ] `Shift+Tab` = hide/show left panel only

- [ ] **10. Right-Click Context Menu on Canvas**
  - [ ] Context menu with common actions
  - [ ] Copy, Paste, Fill, Eyedropper
  - [ ] "Select All Color"

- [ ] **37. Auto-Save & Crash Recovery**
  - [ ] Background save every X minutes
  - [ ] Recovery dialog on startup if standard exit wasn't detected
  - [ ] Snapshot folder maintenance

- [ ] **38. Background Checker Customization**
  - [ ] Change colors of the transparency checkerboard (currently grey/white)
  - [ ] Change size of checker squares

- [ ] **39. Mouse Wheel Customization**
  - [ ] Option: Wheel = Zoom, Ctrl+Wheel = Scroll OR Vice Versa
  - [ ] Shift+Wheel = Horizontal Scroll
  - [ ] Alt+Wheel = Change Color or Brush Size

- [ ] **40. Command Palette**
  - [ ] `Ctrl+Shift+P` (VS Code style) to search any command/tool
  - [ ] Fuzzy search for "Export", "Grid", "Resize", etc.

---

## 🎨 Advanced Color Mastery

- [ ] **13. Color History Navigation**
  - [ ] `Alt+Left/Right` to cycle through recent colors
  - [ ] Visual indicator of current color in history

- [ ] **18. Color Picker from Screen**
  - [ ] Eyedropper can sample from outside the app
  - [ ] `Alt+Click` to sample from screen

- [ ] **41. Palette Analysis & Sorting**
  - [ ] Sort palette by Hue, Saturation, Brightness
  - [ ] Remove duplicates
  - [ ] "Count used colors" report

- [ ] **42. Gamut Masks**
  - [ ] Overlay on color wheel to limit choices to specific harmonies
  - [ ] Locking mechanism to prevent picking outside gamut

- [ ] **43. Palette Ramp Generator**
  - [ ] Select two colors -> generate X intermediate steps
  - [ ] Auto-add to palette

- [ ] **44. Color Replacement Tool**
  - [ ] Swap Color A for Color B globally
  - [ ] Swap only within selection
  - [ ] Tolerance slider for similar colors

- [ ] **45. Colorblind Simulation Views**
  - [ ] Toggle to view canvas as Deuteranopia/Protanopia/Grayscale
  - [ ] Real-time check helps accessibility

- [ ] **46. Select by Color (Magic Wand for Colors)**
  - [ ] Select all pixels of current color
  - [ ] Contiguous vs Global toggle

---

## 🪄 Selection & Transform Magic

- [ ] **20. Multi-Select Layers**
  - [ ] `Ctrl+Click` to select multiple layers
  - [ ] Bulk move/delete

- [ ] **47. Advanced Magic Wand**
  - [ ] Tolerance setting (0-255) for non-pixel-perfect images
  - [ ] "Dithered Selection" handling

- [ ] **48. Free Transform Tool**
  - [ ] Rotation handles enabled on selection
  - [ ] Scaling handles without menu interaction
  - [ ] Shearing/skewing ability

- [ ] **49. Mesh Warp / Deformation**
  - [ ] 3x3 or 4x4 grid to warp pixel selections
  - [ ] Essential for organic animation (breathing, squashing)

- [ ] **50. "Floating" Selection**
  - [ ] Move selection contents without cutting immediately
  - [ ] Commit on click-off or Enter

- [ ] **51. Border/Outline Selection**
  - [ ] Create selection border around current selection (e.g., 1px outline)
  - [ ] Great for quickly outlining characters

- [ ] **52. Auto-Crop to Content**
  - [ ] Trim transparent edges automatically
  - [ ] "Trim" command

---

## 🎭 Animation Features

- [ ] **21. Animation Onion Skin Improvements**
  - [ ] Adjustable opacity slider
  - [ ] Color-coded frames (Previous=Red, Next=Blue)
  - [ ] "Jump" frames (see every Nth frame)

- [ ] **24. Status Bar Enhancements**
  - [ ] Show FPS, Frame Number/Total

- [ ] **53. Frame Tagging System**
  - [ ] Label frames "Idle", "Run", "Jump"
  - [ ] Loop sections based on tags

- [ ] **54. Variable Frame Duration**
  - [ ] Set specific duration (ms) for individual frames
  - [ ] Essential for "pauses" without duplicating frames

- [ ] **55. Linked Cels**
  - [ ] Edit one frame, update linked frames automatically
  - [ ] Perfect for static background layers in animation

- [ ] **56. Ping-Pong Playback**
  - [ ] Forward -> Reverse loop mode

- [ ] **57. Sub-Pixel Animation Helper**
  - [ ] Visual guide for sub-pixel movement references

---

## 🔧 Workflow & Tools

- [ ] **11. Ruler/Guides System**
  - [ ] Toggleable rulers, Drag guides
  - [ ] Snap to guides

- [ ] **12. Snap to Grid Toggle**
  - [ ] Visual snap indicator

- [ ] **16. Canvas Presets Quick Access**
  - [ ] Common sizes (Icon, 1080p, Gameboy)

- [ ] **17. Layer Blend Modes**
  - [ ] Multiply, Screen, Overlay, Soft Light

- [ ] **19. Undo History Visualizer**
  - [ ] List/Timeline of actions

- [ ] **58. Reference Images**
  - [ ] Load reference image as non-editable overlay
  - [ ] Floating reference window
  - [ ] Opacity control for tracing

- [ ] **59. Navigator Window**
  - [ ] Mini-map view of canvas
  - [ ] Click to jump viewport
  - [ ] Zoom slider in navigator

- [ ] **60. Multiple Viewports**
  - [ ] Open second window of SAME file (e.g., one at 100%, one zoomed in)
  - [ ] Changes reflect instantly in both

- [ ] **61. Pixel Grid**
  - [ ] Show visual gaps between pixels at high zoom (>800%)
  - [ ] Toggleable

- [ ] **62. Scripting/Plugin API (Basic)**
  - [ ] Load external Python scripts as tools
  - [ ] "Plugins" folder support

- [ ] **63. Macro/Action Recorder**
  - [ ] Record sequence of actions
  - [ ] Replay on current layer/frame

---

## 📤 Export, Fx & Integration

- [ ] **22. Export Preview Window**
  - [ ] Scale options, transparent check

- [ ] **23. Canvas Grid Customization**
  - [ ] Grid colors, spacing

- [ ] **64. Sprite Sheet Packer**
  - [ ] Export all frames as single sheet
  - [ ] Configure columns/rows/padding

- [ ] **65. GIF Optimization**
  - [ ] Color table generation options
  - [ ] "Save for Web" equivalents

- [ ] **66. Social Media Export Mode**
  - [ ] Auto-scale to 400% or 1000%
  - [ ] Auto-center on solid background
  - [ ] Perfect for Twitter/Instagram posting

- [ ] **67. Slice Tool / Export Regions**
  - [ ] Define named regions to export separately
  - [ ] Useful for UI sheets or tilemaps

- [ ] **68. Outline FX**
  - [ ] Filter to automatically draw outline around sprite
  - [ ] Color/Thickness choice

- [ ] **69. CRT/Scanline Filter Export**
  - [ ] Apply "Retra" look to exported image
  - [ ] Curvature, Scanlines, Bloom

- [ ] **70. Metdata/Game Engine Export**
  - [ ] Export with .meta file (Unity/Godot optimized)
  - [ ] JSON export of tags and frame data

---

## 💡 Experimental & Future

- [ ] **71. 9-Slice Scaling Helper**
  - [ ] Visual guides for 9-slice UI assets
- [ ] **72. Isometric Grid Support**
  - [ ] 2:1 Isometric grid overlay
  - [ ] Isometric shape tools
- [ ] **73. Text Tool with Bitmap Fonts**
  - [ ] Type text using custom .png fonts (not just system fonts)
- [ ] **74. "Pixel Logic" Analysis**
  - [ ] Find "orphaned" pixels (singles)
  - [ ] Find doubles (jaggies) and auto-fix
- [ ] **75. Collaborative Mode (Couch CO-OP)**
  - [ ] Two mouse support? (Experimental)
  - [ ] Networked session?

---

## Priority Recommendations

### High Impact, Medium Effort
- [ ] Copy/Paste shortcuts (#5)
- [ ] Middle mouse pan (#6)
- [ ] Spacebar pan (#7)
- [ ] Number keys for tools (#8)
- [ ] Tab panel toggle (#9)
- [ ] Pixel-Perfect Line Algorithm (#29)
- [ ] Auto-Save (#37)

### High Impact, Higher Effort
- [x] Theme customization (#1) ✅ COMPLETE
- [ ] Right-click context menu (#10)
- [ ] Layer blend modes (#17)
- [ ] Symmetry Painting (#30)
- [ ] Reference Images (#58)
- [ ] Sprite Sheet Packer (#64)

### Polish & Polish
- [ ] Ruler/guides (#11)
- [ ] Snap to grid (#12)
- [ ] Color history navigation (#13)
- [ ] Micro-animations (#26)

---

## Notes

These features focus on speed, visual feedback, and workflow efficiency. Check off items as they're completed and update this file accordingly.
