#!/usr/bin/env python3
"""
Script to remove window state methods that should be in Window State Manager
"""

def remove_window_state_methods():
    # Read the file
    with open('src/ui/main_window.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Current file: {len(lines)} lines")
    
    # Window state methods that should be in Window State Manager
    window_methods = [
        '_toggle_left_panel',
        '_toggle_right_panel',
        '_redraw_canvas_after_resize',
        '_show_panel_loading_indicator',
        '_finish_panel_toggle'
    ]
    
    # Find method boundaries
    method_ranges = []
    
    for method_name in window_methods:
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
    
    # Remove methods in reverse order
    method_ranges.sort(reverse=True, key=lambda x: x[0])
    total_removed = 0
    
    for start, end, name in method_ranges:
        removed_lines = end - start
        print(f"Removing {name}: {removed_lines} lines")
        del lines[start:end]
        total_removed += removed_lines
    
    print(f"\nRemoved {total_removed} lines total")
    
    # Write back to file
    with open('src/ui/main_window.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"Final file: {len(lines)} lines")
    print("Window state methods removed!")

if __name__ == "__main__":
    remove_window_state_methods()
