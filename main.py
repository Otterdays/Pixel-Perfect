#!/usr/bin/env python3
"""
Pixel Perfect - Retro Pixel Art Editor
Main application entry point
"""

import sys
import os
from src.ui.main_window import MainWindow

def main():
    """Main application entry point"""
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"Error starting Pixel Perfect: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
