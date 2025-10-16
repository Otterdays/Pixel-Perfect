# Import PNG Dialog Scale Calculation Fix

**Version**: 2.3.0  
**Date**: January 2025  
**Status**: ✅ Complete

## Problem

The Import PNG dialog had two critical issues:

1. **GUI Scale Calculation Bug**: Scale calculations used raw PNG file dimensions instead of validated base dimensions
2. **Import Logic Bug**: Actual import process used wrong dimensions, causing 8x8 images to import as 64x64

**Symptoms:**
- Dialog showed "Original: 8x8 pixels" ✅
- But scale calculations were wrong: 1x scale showed "Import as: 64x64" ❌
- Switching scales corrupted the GUI state
- Actual import created 64x64 canvas instead of 8x8 ❌

## Root Cause Analysis

### Issue 1: GUI Scale Calculation
The `_set_scale()` method used `self.preview_image.size` (raw file dimensions) instead of validated base dimensions:

```python
# BEFORE (Broken)
def _set_scale(self, scale: int):
    # ...
    if self.preview_image:
        w, h = self.preview_image.size  # 64x64 (raw file size) ❌
        self._update_result_label(w, h)
```

### Issue 2: Import Logic Priority
The `import_png_to_pixpf()` method had the same priority bug as the validation method - it checked direct sizes before scaled exports:

```python
# BEFORE (Broken Priority)
if width not in self.VALID_SIZES or height not in self.VALID_SIZES:
    # Check scaled exports SECOND (never reached for 64x64)
```

## Solution

### Files Modified

1. **`src/ui/import_png_dialog.py`**
   - Added `base_width` and `base_height` properties to store validated dimensions
   - Modified `_load_preview()` to store validated base dimensions
   - Fixed `_set_scale()` to use stored base dimensions instead of raw file dimensions

2. **`src/utils/import_png.py`**
   - Fixed `import_png_to_pixpf()` method to prioritize scaled export detection
   - Applied same priority logic as validation method

### Technical Changes

**GUI Scale Calculation Fix:**
```python
# BEFORE (Broken)
def _set_scale(self, scale: int):
    if self.preview_image:
        w, h = self.preview_image.size  # Raw file dimensions
        self._update_result_label(w, h)

# AFTER (Fixed)
def _set_scale(self, scale: int):
    if self.base_width is not None and self.base_height is not None:
        self._update_result_label(self.base_width, self.base_height)  # Validated base dimensions
```

**Import Logic Priority Fix:**
```python
# BEFORE (Broken Priority)
if width not in self.VALID_SIZES or height not in self.VALID_SIZES:
    # Check scaled exports SECOND

# AFTER (Fixed Priority)
# PRIORITY: Check scaled exports FIRST
for scale in reversed(self.SCALE_FACTORS):
    # ... scaled detection logic
# SECONDARY: Check direct sizes only if no scaled export detected
```

## Complete Fix Flow

### Your 8x8 Image Scenario (Fixed)
1. **64x64 PNG file** (8x8 exported at 8x scale)
2. **Validation**: Detects as 8x8 scaled export ✅
3. **GUI**: Shows "Original: 8x8 pixels" ✅
4. **Scale Calculation**: Uses base dimensions (8x8) ✅
5. **1x Scale**: Shows "Import as: 8x8 (no scaling)" ✅
6. **2x Scale**: Shows "Import as: 16x16 (2x scaled from 8x8)" ✅
7. **Actual Import**: Creates 8x8 canvas ✅

## Testing

✅ **GUI Scale Display**: All scales show correct dimensions  
✅ **Scale Switching**: No GUI state corruption when switching scales  
✅ **1x Scale Import**: 8x8 images import as 8x8 canvas  
✅ **2x Scale Import**: 8x8 images import as 16x16 canvas  
✅ **4x Scale Import**: 8x8 images import as 32x32 canvas  
✅ **8x Scale Import**: 8x8 images import as 64x64 canvas  
✅ **Direct PNG Files**: Still work correctly (8x8, 16x16, 32x32, 64x64)  
✅ **Scaled Exports**: All scales detected correctly  

## Impact

- **GUI Accuracy**: Scale calculations now use correct base dimensions
- **Import Accuracy**: Actual imports match displayed dimensions
- **User Experience**: No confusion between displayed and actual import sizes
- **Consistency**: GUI and import logic use same validation system

## Edge Cases Handled

- **Scale Switching**: GUI state remains consistent
- **Multiple Valid Scales**: Prioritizes highest scale detection
- **Direct vs Scaled**: Handles both scenarios correctly
- **Error Cases**: Proper fallback to raw dimensions if validation fails

## Future Considerations

- Monitor for any edge cases with unusual scaling factors
- Ensure consistency between validation and import logic
- Consider adding visual indicators for scaled vs direct imports

---

**Implementation Status**: ✅ Complete and tested  
**User Impact**: High - fixes critical GUI and import accuracy  
**Technical Complexity**: Medium - fixed both GUI state and import logic
