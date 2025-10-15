#!/usr/bin/env python3
"""
Pixel Perfect - Retro Pixel Art Editor
Main application entry point

Copyright © 2024-2025 Diamond Clad Studios
All Rights Reserved - Proprietary Software
"""

import sys
import os
from src.ui.main_window import MainWindow

def main():
    """Main application entry point"""
    # Register .pixpf file icon on first launch (Windows only)
    if os.name == 'nt':
        try:
            from src.utils.file_association import prompt_and_register
            prompt_and_register()
        except Exception as e:
            print(f"Note: Could not register file icon: {e}")
    
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        import traceback
        print(f"Error starting Pixel Perfect: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
