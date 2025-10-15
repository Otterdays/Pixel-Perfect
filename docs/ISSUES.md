# Pixel Perfect - Known Issues

## Issue #1: Persistent Grey Boxes Around UI Sections
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

## Issue #2: Git Configuration Review Needed
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

*This document will be updated as issues are resolved.*
