@echo off
echo Installing Python 3.11 for Pixel Perfect...
echo.

REM Download Python 3.11.9 (latest 3.11 version)
echo Downloading Python 3.11.9...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python-3.11.9-amd64.exe'"

if exist python-3.11.9-amd64.exe (
    echo.
    echo Installing Python 3.11.9...
    echo IMPORTANT: Make sure to check "Add Python to PATH" during installation!
    echo.
    python-3.11.9-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    echo.
    echo Installation complete!
    echo.
    echo Testing Python 3.11...
    py -3.11 --version
    
    echo.
    echo Installing Pixel Perfect dependencies...
    py -3.11 -m pip install pygame Pillow customtkinter numpy
    
    echo.
    echo Testing Pixel Perfect...
    py -3.11 main.py
    
    echo.
    echo Cleaning up...
    del python-3.11.9-amd64.exe
    
) else (
    echo Failed to download Python 3.11.9
    echo Please download manually from: https://python.org/downloads/release/python-3119/
)

pause
