@echo off
REM ===================================================
REM Pixel Perfect - Build Script
REM Creates standalone Windows executable
REM ===================================================

echo.
echo ====================================
echo    Pixel Perfect - Build Script
echo ====================================
echo.

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo [1/5] Cleaning previous build...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "PixelPerfect.spec" del /q "PixelPerfect.spec"

echo [2/5] Building executable with PyInstaller...
set ICON_PATH=%~dp0..\assets\icons\app_icon.ico
cd ..
python -m PyInstaller --name="PixelPerfect" --onefile --windowed --icon="%ICON_PATH%" --hidden-import=src.core.canvas --hidden-import=src.core.color_palette --hidden-import=src.core.custom_colors --hidden-import=src.core.layer_manager --hidden-import=src.core.project --hidden-import=src.core.undo_manager --hidden-import=src.tools.base_tool --hidden-import=src.tools.brush --hidden-import=src.tools.eraser --hidden-import=src.tools.eyedropper --hidden-import=src.tools.fill --hidden-import=src.tools.selection --hidden-import=src.tools.shapes --hidden-import=src.ui.layer_panel --hidden-import=src.ui.timeline_panel --hidden-import=src.ui.color_wheel --hidden-import=src.utils.export --hidden-import=src.utils.presets --hidden-import=src.animation.timeline --distpath="BUILDER\dist" --workpath="BUILDER\build" --specpath="BUILDER" main.py
if errorlevel 1 (
    echo ERROR: PyInstaller build failed!
    cd BUILDER
    pause
    exit /b 1
)
cd BUILDER

echo [3/5] Copying assets to distribution folder...
if not exist "dist\assets" mkdir "dist\assets"
xcopy /E /I /Y "..\assets" "dist\assets" >nul

if not exist "dist\docs" mkdir "dist\docs"
xcopy /E /I /Y "..\docs" "dist\docs" >nul

echo [4/5] Creating release package...
if not exist "release" mkdir "release"
xcopy /E /I /Y "dist\*" "release\PixelPerfect" >nul

echo [5/5] Cleaning up temporary files...
if exist "build" rmdir /s /q "build"
if exist "PixelPerfect.spec" del /q "PixelPerfect.spec"

echo.
echo ====================================
echo    BUILD COMPLETE!
echo ====================================
echo.
echo Executable location: dist\PixelPerfect.exe
echo Release package: release\PixelPerfect\
echo.
echo Temporary files cleaned up automatically.
echo You can now distribute the contents of release\PixelPerfect\
echo.

pause
