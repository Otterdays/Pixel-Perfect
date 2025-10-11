@echo off
echo Starting Pixel Perfect with Python 3.13.6...

REM Try Python 3.13.6 first (recommended)
py -3.13 main.py
if %errorlevel% equ 0 goto :success

REM Try regular python command
python main.py
if %errorlevel% equ 0 goto :success

echo.
echo Python command failed. Trying alternative methods...
echo.

REM Try to find Python executable
for /f "tokens=*" %%i in ('where python 2^>nul') do (
    echo Found Python at: %%i
    "%%i" main.py
    if %errorlevel% equ 0 goto :success
)

echo.
echo Python not found in PATH!
echo Please add Python to your system PATH environment variable.
echo.
echo To fix this:
echo 1. Press Windows + R, type "sysdm.cpl", press Enter
echo 2. Click "Environment Variables"
echo 3. Under "System Variables", find and select "Path"
echo 4. Click "Edit"
echo 5. Click "New" and add your Python installation path
echo 6. Click "OK" on all dialogs
echo 7. Restart your computer
echo.
pause
exit /b 1

:success
echo.
echo ========================================
echo  Pixel Perfect closed successfully!
echo ========================================
echo.
echo Window will auto-close in 2 seconds...
timeout /t 2 /nobreak >nul
exit /b 0
