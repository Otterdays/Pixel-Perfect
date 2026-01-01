# Pixel Perfect - Known Issues

## Issue #1: Saved Colors Blank Space Bug
**Date**: December 2024  
**Status**: ✅ **RESOLVED**  
**Priority**: High  

### Problem Description
Large blank space appeared between the palette radio buttons (Grid/Primary/Wheel/Constants/Saved) and the "Saved Colors" section when the Saved view was active. The empty box was clearly visible and looked like a UI bug.

### Root Cause
`palette_content_frame` was packed and visible even when switching to the saved view, creating an empty box. This frame is only used by Grid, Primary, Wheel, and Constants views - NOT the Saved view. When clearing `palette_content_frame.winfo_children()`, the frame itself remained packed and visible, taking up vertical space.

### Resolution
✅ Fixed in Version 2.0.0:
- Added `self.palette_content_frame.pack_forget()` to hide the frame when clearing it
- Re-pack `palette_content_frame` only for views that need it (Grid, Primary, Wheel, Constants)
- Saved view does NOT pack `palette_content_frame`, eliminating the empty box

### Files Modified
- `src/ui/main_window.py` - Fixed `_show_view()` method
- `src/ui/ui_builder.py` - Reduced container padding
- `src/ui/palette_views/saved_view.py` - Reduced top padding

### Key Lesson
When debugging UI spacing issues, trace the EXACT frame hierarchy and packing order. Don't assume padding is the issue - sometimes entire frames are visible when they shouldn't be.

---

## Issue #2: Persistent Grey Boxes Around UI Sections
**Date**: October 14, 2025  
**Status**: 🔴 **OPEN** - Not Fixed  
**Priority**: High  

### Problem Description
Despite multiple attempts to fix the "ugly grey boxes" issue, the Tools, Selection, Palette, Layers, and Animation sections still have visible dark grey rounded containers around them. The sections do not blend seamlessly with the panel backgrounds.

### Visual Evidence
- Tools section has visible grey rounded box container
- Selection section has visible grey rounded box container  
- Palette section has visible grey rounded box container
- Layers section has visible grey rounded box container
- Animation section has visible grey rounded box container

### Attempted Fixes (All Failed)
1. **v1.52**: Set container frames to `fg_color="transparent"`
2. **v1.53**: Matched button colors to theme backgrounds
3. **v1.54**: Set scrollable panels to `fg_color="transparent"` then `fg_color=theme.bg_secondary`

### Root Cause Analysis Needed
The issue persists despite:
- Making all CTkFrame containers transparent
- Matching button colors to theme backgrounds
- Setting scrollable panel backgrounds to theme colors
- Removing hardcoded `fg_color="gray"` from buttons

### Next Investigation Steps
1. Check if CTkScrollableFrame internal canvas is overriding fg_color
2. Investigate if CustomTkinter theme system is forcing default colors
3. Consider using tk.Frame instead of CTkFrame for containers
4. Check if there are CSS-like style overrides in CustomTkinter

### User Impact
- UI appears cluttered with visible container boxes
- Buttons and sections don't "float" as intended
- Overall aesthetic is compromised

---

## Issue #3: Git Configuration Review Needed
**Date**: October 14, 2025  
**Status**: ✅ **RESOLVED**  
**Priority**: Medium  

### Problem Description
Need to verify .gitignore contains all necessary exclusions while preserving builder release and dist folders.

### Resolution
✅ Fixed .gitignore to properly exclude large build artifacts:
- BUILDER/release/ - excluded (too large for GitHub)
- BUILDER/dist/ - excluded (too large for GitHub)  
- All other standard exclusions verified (Python cache, IDE files, OS files, etc.)

### Items Checked
- [x] Python cache files (__pycache__, *.pyc)
- [x] IDE files (.vscode, .idea)
- [x] OS files (.DS_Store, Thumbs.db)
- [x] Build artifacts (excluding BUILDER/release/ and BUILDER/dist/)
- [x] Temporary files
- [x] Log files

---

## Issue #4: Move Tool Preview Visual Glitches
**Date**: January 1, 2026  
**Status**: 🟡 **OPEN** - Minor  
**Priority**: Low  

### Problem Description
When using the Selection tool to move pixels, there are minor visual glitches during the move preview:
1. Ghost pixels remain visible at the original position during the drag
2. Pixels underneath the selection box briefly disappear then reappear

### Visual Symptoms
- During drag: Old pixels stay visible at original position
- During drag: Pixels under the moving selection flicker

### Root Cause Analysis
These are visual preview timing issues related to how the move preview is rendered vs. when the layer data is updated. The move tool's preview system likely needs refactoring to:
1. Clear the original position in the preview layer
2. Properly composite the preview with existing pixels

### Workaround
The final result is correct - this is purely a visual preview issue during the move operation.

### User Impact
- Minor visual distraction during move operations
- Does not affect final result or data integrity
- Core functionality remains intact

---

*This document will be updated as issues are resolved.*
