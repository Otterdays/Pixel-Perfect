#!/usr/bin/env python3
"""
Careful script to refactor theme methods from main_window.py
"""

def refactor_theme_methods():
    # Read the file
    with open('src/ui/main_window.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Original file: {len(lines)} lines")
    
    # Step 1: Add ThemeDialogManager import after UIBuilder import
    for i, line in enumerate(lines):
        if 'from ui.ui_builder import UIBuilder' in line:
            # Insert new import after this line
            lines.insert(i + 1, 'from ui.theme_dialog_manager import ThemeDialogManager\n')
            print(f"Added import at line {i+2}")
            break
    
    # Step 2: Find and mark methods to remove
    methods_to_remove = [
        '_create_settings_dialog',
        '_show_settings_dialog',
        '_hide_settings_dialog',
        '_apply_theme',
        '_apply_theme_to_children',
        '_update_theme_canvas_elements'
    ]
    
    method_ranges = []
    
    for method_name in methods_to_remove:
        # Find method start
        for i, line in enumerate(lines):
            if f'def {method_name}(' in line and line.startswith('    def '):
                start = i
                # Find method end (next method definition at same indentation level)
                end = None
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith('    def ') or lines[j].startswith('class ') or (lines[j].strip() and not lines[j].startswith(' ')):
                        end = j
                        break
                if end is None:
                    end = len(lines)
                method_ranges.append((start, end, method_name))
                print(f"Found {method_name}: lines {start+1} to {end}")
                break
    
    # Step 3: Remove methods in reverse order
    method_ranges.sort(reverse=True, key=lambda x: x[0])
    for start, end, name in method_ranges:
        print(f"Removing {name} from line {start+1} to {end}")
        del lines[start:end]
    
    # Step 4: Find theme_manager initialization and add theme_dialog_manager
    for i, line in enumerate(lines):
        if 'self.theme_manager = ThemeManager()' in line:
            # Find the callback line
            for j in range(i, min(i+5, len(lines))):
                if 'self.theme_manager.on_theme_changed' in line:
                    # Insert theme_dialog_manager initialization before theme_manager
                    lines.insert(i, '        # Initialize theme dialog manager\n')
                    lines.insert(i+1, '        self.theme_dialog_manager = ThemeDialogManager(self)\n')
                    lines.insert(i+2, '        \n')
                    # Update callback to use theme_dialog_manager
                    lines[j+3] = '        self.theme_manager.on_theme_changed = self.theme_dialog_manager.apply_theme\n'
                    print(f"Added theme_dialog_manager initialization at line {i+1}")
                    break
            break
    
    # Step 5: Find and update _apply_theme calls to use theme_dialog_manager
    for i, line in enumerate(lines):
        if 'self._apply_theme(' in line:
            lines[i] = line.replace('self._apply_theme(', 'self.theme_dialog_manager.apply_theme(')
            print(f"Updated _apply_theme call at line {i+1}")
    
    # Step 6: Find and update settings dialog callback
    for i, line in enumerate(lines):
        if "'show_settings_dialog': self._show_settings_dialog" in line:
            lines[i] = line.replace("'show_settings_dialog': self._show_settings_dialog", 
                                   "'show_settings_dialog': self.theme_dialog_manager.show_settings_dialog")
            print(f"Updated settings dialog callback at line {i+1}")
    
    # Step 7: Remove settings_dialog initialization call
    for i, line in enumerate(lines):
        if 'self._create_settings_dialog()' in line:
            del lines[i]
            print(f"Removed settings dialog initialization at line {i+1}")
            break
    
    # Write back to file
    with open('src/ui/main_window.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\nFinal file: {len(lines)} lines")
    print(f"Removed: {5127 - len(lines)} lines")
    print("Theme refactor complete!")

if __name__ == "__main__":
    refactor_theme_methods()

