"""
File association utilities for .pixpf files
Registers custom icon on Windows
"""

import os
import sys
import winreg
import ctypes

def is_pixpf_registered():
    """Check if .pixpf file association is already registered"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.pixpf", 0, winreg.KEY_READ)
        winreg.CloseKey(key)
        return True
    except WindowsError:
        return False

def is_admin():
    """Check if running with admin rights"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def register_pixpf_icon():
    """Register .pixpf file icon in Windows registry"""
    try:
        # Get icon path
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.join(os.path.dirname(__file__), "..", "..")
        
        icon_path = os.path.abspath(os.path.join(base_path, "assets", "icons", "pixpf_icon.ico"))
        
        if not os.path.exists(icon_path):
            print(f"⚠ Icon not found: {icon_path}")
            return False
        
        # Register file association
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.pixpf")
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.pixpf", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "PixelPerfect.Project")
        winreg.CloseKey(key)
        
        # Set description
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\PixelPerfect.Project")
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\PixelPerfect.Project", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Pixel Perfect Project")
        winreg.CloseKey(key)
        
        # Set icon
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\PixelPerfect.Project\DefaultIcon")
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\PixelPerfect.Project\DefaultIcon", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f"{icon_path},0")
        winreg.CloseKey(key)
        
        print("✓ Registered .pixpf file icon")
        return True
        
    except Exception as e:
        print(f"✗ Failed to register icon: {e}")
        return False

def prompt_and_register():
    """Prompt user and register file association on first launch"""
    if is_pixpf_registered():
        return True
    
    print("\n" + "="*50)
    print("  First Launch: Register .pixpf File Icon")
    print("="*50)
    print("\nThis will set a custom icon for Pixel Perfect project files.")
    print("Registering file association...")
    
    if register_pixpf_icon():
        print("\n✓ Success! .pixpf files will now show the custom icon.")
        print("  (You may need to restart Explorer to see changes)")
        return True
    else:
        print("\n⚠ Could not auto-register.")
        print("  To manually register, run: register_pixpf_icon.bat")
        return False

