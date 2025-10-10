@echo off
echo ========================================
echo Pixel Perfect - Python 3.11 Installation
echo ========================================
echo.
echo According to your SBOM, Pixel Perfect requires Python 3.11+
echo You currently have Python 3.14, which is too new for pygame.
echo.
echo This script will help you install Python 3.11 alongside Python 3.14
echo.
echo STEP 1: Download Python 3.11.9
echo ========================================
echo.
echo Opening Python 3.11.9 download page...
start https://www.python.org/downloads/release/python-3119/
echo.
echo Please download: Windows installer (64-bit)
echo.
pause
echo.
echo STEP 2: Install Python 3.11.9
echo ========================================
echo.
echo When the installer opens:
echo 1. Check "Add Python to PATH"
echo 2. Check "Install for all users" (optional)
echo 3. Click "Install Now"
echo.
pause
echo.
echo STEP 3: Test Installation
echo ========================================
echo.
echo Testing Python 3.11 installation...
py -3.11 --version
if %errorlevel% equ 0 (
    echo ✅ Python 3.11 installed successfully!
    echo.
    echo Installing Pixel Perfect dependencies...
    py -3.11 -m pip install pygame Pillow customtkinter numpy
    echo.
    echo Testing Pixel Perfect with Python 3.11...
    py -3.11 main.py
) else (
    echo ❌ Python 3.11 not found. Please check installation.
    echo.
    echo Alternative: Use the full path to Python 3.11
    echo Example: "C:\Program Files\Python311\python.exe" main.py
)
echo.
pause
