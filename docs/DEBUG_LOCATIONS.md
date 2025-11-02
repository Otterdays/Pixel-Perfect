# Debug Locations & Tracking System

**Date**: October 18, 2025  
**Purpose**: Track all debug statements in the codebase for troubleshooting and development

## Debug Statement Format

All debug statements use the format: `print("🔍 DEBUG: [description]")`

## Current Debug Locations

### 1. Selection Manager (`src/ui/selection_manager.py`)

#### Mirror Selection Function
- **Line 68**: `mirror_selection() called` - Entry point tracking
- **Line 105**: `Got drawing layer, clearing original area...` - Layer access confirmation
- **Line 120**: `Cleared X non-transparent pixels from original area` - Pixel clearing count
- **Line 124**: `Mirrored pixels shape: (height, width, channels)` - Shape verification
- **Line 145**: `Wrote X non-transparent pixels, skipped Y transparent pixels` - Writing statistics
- **Line 150**: `Canvas callback updated` - Canvas update confirmation
- **Line 153**: `Display callback updated` - Display update confirmation
- **Line 155**: `No drawing layer found!` - Error condition

#### Rotate Selection Function
- **Line 159**: `rotate_selection() called` - Entry point tracking

#### Apply Rotation Function
- **Line 220**: `apply_rotation() called` - Entry point tracking
- **Line 223**: `Not in rotation mode` - Mode check
- **Line 239**: `Got drawing layer and rotated pixels preview` - Layer access confirmation
- **Line 243**: `Clearing original area: left=X, top=Y, width=W, height=H` - Clear area coordinates
- **Line 256**: `Cleared X non-transparent pixels from original rotation area` - Pixel clearing count
- **Line 262**: `Writing rotated pixels: new_width=X, new_height=Y` - New dimensions
- **Line 263**: `Writing at position: left=X, top=Y` - Write position
- **Line 280**: `Wrote X non-transparent rotated pixels, skipped Y transparent pixels` - Writing statistics
- **Line 288**: `Rotation canvas callback updated` - Canvas update confirmation
- **Line 291**: `Rotation display callback updated` - Display update confirmation
- **Line 293**: `No drawing layer or rotated pixels preview found!` - Error condition
- **Line 300**: `Exited rotation mode` - Mode exit confirmation

## Debug Categories

### 🔍 Pixel Operations
- Pixel clearing counts
- Pixel writing counts
- Transparent pixel skipping
- Shape verification

### 🔍 Layer Operations
- Drawing layer access
- Layer state verification
- Canvas updates

### 🔍 Coordinate Tracking
- Selection bounds
- Clear area coordinates
- Write positions
- Dimension changes

### 🔍 Mode Management
- Function entry/exit
- Mode state changes
- Callback confirmations

## Usage Instructions

1. **Enable Debug Mode**: Debug statements are always active
2. **Console Output**: Check console/terminal for debug messages
3. **Pattern Matching**: Look for specific debug patterns:
   - `mirror_selection()` for mirror operations
   - `apply_rotation()` for rotation operations
   - Pixel count mismatches indicate ghost pixel sources

## Troubleshooting Guide

### Ghost Pixels Issue
1. **Check Clearing Count**: Should match non-transparent pixels in original
2. **Check Writing Count**: Should match non-transparent pixels in transformed version
3. **Check Coordinates**: Verify clear and write positions are correct
4. **Check Layer Access**: Ensure drawing layer is available

### Common Debug Patterns
- **Cleared 0 pixels**: Original area had no non-transparent pixels
- **Wrote 0 pixels**: Transformed version had no non-transparent pixels
- **Shape mismatch**: Array dimensions don't match expectations
- **No drawing layer**: Layer system not initialized

## Adding New Debug Statements

When adding new debug statements:

1. Use the format: `print("🔍 DEBUG: [description]")`
2. Update this document with location and purpose
3. Include relevant data (counts, coordinates, shapes)
4. Group related debug statements logically

## Debug Statement Best Practices

- **Be Specific**: Include relevant data in debug messages
- **Use Consistent Format**: Always use 🔍 DEBUG: prefix
- **Include Context**: Mention function name and operation type
- **Count Operations**: Track pixel counts for verification
- **Verify Assumptions**: Check layer access, coordinates, shapes

## Future Debug Locations

Areas that may need debug statements:
- Canvas renderer operations
- Layer management
- Tool switching
- File operations
- Animation system
