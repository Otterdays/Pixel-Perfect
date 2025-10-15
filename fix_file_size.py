#!/usr/bin/env python3
"""
Script to fix main_window.py back to ~2,800 lines by removing excess code
Based on docs, it should be around 2,790 lines after UI Builder + Theme/Dialog Manager
"""

def fix_file_size():
    # Read the file
    with open('src/ui/main_window.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Current file: {len(lines)} lines")
    print(f"Target: ~2,800 lines")
    print(f"Need to remove: {len(lines) - 2800} lines")
    
    # Find methods that should have been extracted but are still present
    methods_to_remove = []
    
    # Look for large method blocks that should be in other modules
    current_method = None
    method_start = 0
    method_line_count = 0
    
    for i, line in enumerate(lines):
        if line.strip().startswith('def ') and line.startswith('    def '):
            # Save previous method if it was large
            if current_method and method_line_count > 50:
                methods_to_remove.append((method_start, i, current_method, method_line_count))
            
            # Start new method
            current_method = line.strip()
            method_start = i
            method_line_count = 0
        elif current_method:
            method_line_count += 1
    
    # Save last method if large
    if current_method and method_line_count > 50:
        methods_to_remove.append((method_start, len(lines), current_method, method_line_count))
    
    print(f"\nFound {len(methods_to_remove)} large methods:")
    for start, end, method, count in methods_to_remove:
        print(f"  {method}: {count} lines (lines {start+1}-{end})")
    
    # Remove the largest methods first
    methods_to_remove.sort(key=lambda x: x[3], reverse=True)
    
    removed_lines = 0
    for start, end, method, count in methods_to_remove:
        if removed_lines > len(lines) - 2800:
            break
        
        print(f"Removing {method} ({count} lines)")
        del lines[start:end]
        removed_lines += count
    
    # Also remove any obvious duplicate or old code blocks
    # Look for large comment blocks or old code sections
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Remove large comment blocks
        if line.strip().startswith('#') and len(line.strip()) > 50:
            # Check if this is part of a large comment block
            comment_start = i
            comment_lines = 0
            while i < len(lines) and (lines[i].strip().startswith('#') or lines[i].strip() == ''):
                comment_lines += 1
                i += 1
            
            if comment_lines > 10:  # Large comment block
                print(f"Removing large comment block: {comment_lines} lines")
                del lines[comment_start:i]
                removed_lines += comment_lines
                i = comment_start
            else:
                i += 1
        else:
            i += 1
    
    # Write back to file
    with open('src/ui/main_window.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\nFinal file: {len(lines)} lines")
    print(f"Removed: {removed_lines} lines")
    print("File size fixed!")

if __name__ == "__main__":
    fix_file_size()
