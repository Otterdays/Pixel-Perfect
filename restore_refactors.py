#!/usr/bin/env python3
"""
Script to restore all completed refactors to main_window.py
Based on the refactor documentation, these should be present:
- Palette Views Refactor (Version 1.49) ✅
- Event Dispatcher Refactor (Version 1.50) ✅  
- Canvas Renderer Integration (Version 1.56) ✅
- UI Builder Refactor Progress (Version 1.58) ✅
- Theme/Dialog Manager (just completed) ✅
"""

def restore_refactors():
    # Read the file
    with open('src/ui/main_window.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Current file: {len(lines)} lines")
    
    # Step 1: Add missing imports
    missing_imports = [
        'from core.event_dispatcher import EventDispatcher',
        'from core.canvas_renderer import CanvasRenderer', 
        'from core.window_state_manager import WindowStateManager',
        'from ui.palette_views import GridView, PrimaryView, SavedView, ConstantsView'
    ]
    
    # Find where to insert imports (after existing imports)
    import_end = 0
    for i, line in enumerate(lines):
        if line.startswith('from ') or line.startswith('import '):
            import_end = i + 1
        elif line.strip() == '' and import_end > 0:
            break
    
    # Insert missing imports
    for import_line in missing_imports:
        if import_line not in ''.join(lines):
            lines.insert(import_end, import_line + '\n')
            import_end += 1
            print(f"Added import: {import_line}")
    
    # Step 2: Find __init__ method and add missing initializations
    init_start = -1
    for i, line in enumerate(lines):
        if 'def __init__(self):' in line:
            init_start = i
            break
    
    if init_start == -1:
        print("ERROR: Could not find __init__ method")
        return
    
    # Find where to insert initializations (after theme manager)
    init_insert_point = -1
    for i in range(init_start, min(init_start + 200, len(lines))):
        if 'self.theme_manager = ThemeManager()' in lines[i]:
            init_insert_point = i + 1
            break
    
    if init_insert_point == -1:
        print("ERROR: Could not find theme_manager initialization")
        return
    
    # Add missing initializations
    missing_inits = [
        '        # Initialize theme dialog manager',
        '        self.theme_dialog_manager = ThemeDialogManager(self)',
        '        ',
        '        # Initialize canvas renderer (before UI creation)',
        '        from src.core.canvas_renderer import CanvasRenderer',
        '        self.canvas_renderer = CanvasRenderer(self)',
        '        ',
        '        # Initialize event dispatcher',
        '        self.event_dispatcher = EventDispatcher(self)',
        '        self.event_dispatcher.bind_all_events()',
        '        ',
        '        # Initialize window state manager',
        '        self.window_state_manager = WindowStateManager(',
        '            root=self.root,',
        '            left_container=self.left_container,',
        '            right_container=self.right_container,',
        '            left_panel=self.left_panel,',
        '            right_panel=self.right_panel,',
        '            redraw_callback=self._redraw_canvas_after_resize',
        '        )',
        '        # Transfer panel width values to manager',
        '        self.window_state_manager.left_panel_width = self.left_panel_width',
        '        self.window_state_manager.right_panel_width = self.right_panel_width',
        '        ',
        '        # Try to restore saved window state (overrides calculated sizes if successful)',
        '        self._restore_window_state()',
        '        ',
        '        # Initialize palette views',
        '        self.grid_view = GridView(self.left_panel, self.palette, self._get_ui_callbacks())',
        '        self.primary_view = PrimaryView(self.left_panel, self.palette, self._get_ui_callbacks())',
        '        self.saved_view = SavedView(self.left_panel, self.saved_colors, self._get_ui_callbacks())',
        '        self.constants_view = ConstantsView(self.left_panel, self.palette, self._get_ui_callbacks())',
        '        ',
        '        # Initialize UI Builder',
        '        self.ui_builder = UIBuilder(self.main_frame, self._get_ui_callbacks(), self.theme_manager)',
        '        ',
        '        # Initialize tool buttons dictionary',
        '        self.tool_buttons = {}',
        '        ',
        '        # Initialize palette-related attributes',
        '        self.grid_view_frame = None',
        '        self.primary_view_frame = None',
        '        self.wheel_view_frame = None',
        '        self.constants_view_frame = None',
        '        self.saved_view_frame = None',
        '        self.color_frame = None',
        '        self.primary_frame = None',
        '        self.variations_frame = None',
        '        self.palette_frame = None',
        '        self.palette_var = None',
        '        self.palette_label = None',
        '        self.palette_menu = None',
        '        self.view_mode_var = None',
        '        self.color_wheel = None'
    ]
    
    # Insert missing initializations
    for init_line in missing_inits:
        lines.insert(init_insert_point, init_line + '\n')
        init_insert_point += 1
    
    print(f"Added {len(missing_inits)} initialization lines")
    
    # Step 3: Find and update method calls to use refactored modules
    updates_made = 0
    
    # Update theme manager callback
    for i, line in enumerate(lines):
        if 'self.theme_manager.on_theme_changed = self._apply_theme' in line:
            lines[i] = line.replace('self.theme_manager.on_theme_changed = self._apply_theme', 
                                   'self.theme_manager.on_theme_changed = self.theme_dialog_manager.apply_theme')
            updates_made += 1
            print(f"Updated theme callback at line {i+1}")
    
    # Update theme application calls
    for i, line in enumerate(lines):
        if 'self._apply_theme(' in line:
            lines[i] = line.replace('self._apply_theme(', 'self.theme_dialog_manager.apply_theme(')
            updates_made += 1
            print(f"Updated theme call at line {i+1}")
    
    # Update settings dialog calls
    for i, line in enumerate(lines):
        if "'show_settings_dialog': self._show_settings_dialog" in line:
            lines[i] = line.replace("'show_settings_dialog': self._show_settings_dialog", 
                                   "'show_settings_dialog': self.theme_dialog_manager.show_settings_dialog")
            updates_made += 1
            print(f"Updated settings dialog callback at line {i+1}")
    
    # Update canvas renderer calls
    for i, line in enumerate(lines):
        if 'self._draw_scale_handle(' in line:
            lines[i] = line.replace('self._draw_scale_handle(', 'self.canvas_renderer.draw_scale_handle(')
            updates_made += 1
            print(f"Updated canvas renderer call at line {i+1}")
    
    # Update event dispatcher calls
    for i, line in enumerate(lines):
        if 'self._on_tkinter_canvas_mouse_down' in line:
            lines[i] = line.replace('self._on_tkinter_canvas_mouse_down', 'self.event_dispatcher.on_tkinter_canvas_mouse_down')
            updates_made += 1
            print(f"Updated event dispatcher call at line {i+1}")
    
    print(f"Made {updates_made} method call updates")
    
    # Write back to file
    with open('src/ui/main_window.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\nFinal file: {len(lines)} lines")
    print("Refactors restored successfully!")

if __name__ == "__main__":
    restore_refactors()
