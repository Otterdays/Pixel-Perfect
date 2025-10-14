@echo off
REM ===================================================
REM Pixel Perfect - Build Script (OPTIMIZED)
REM Creates standalone Windows executable
REM Optimizations: bytecode, stripping, stdlib exclusions
REM Target: <25 MB (from 29 MB baseline)
REM ===================================================

echo.
echo ====================================
echo  Pixel Perfect - Build Script
echo  MAXIMUM OPTIMIZATION MODE
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

echo [2/6] Building executable with PyInstaller (MAXIMUM OPTIMIZATION)...
set ICON_PATH=%~dp0..\assets\icons\app_icon.ico
set LOGO_PATH=%~dp0..\dcs.png
cd ..
python -m PyInstaller --name="PixelPerfect" --onefile --windowed --optimize=2 --strip --icon="%ICON_PATH%" --add-data="%LOGO_PATH%;." --exclude-module=pygame --exclude-module=scipy --exclude-module=tkinter.test --exclude-module=unittest --exclude-module=test --exclude-module=xml.etree --exclude-module=xml.dom --exclude-module=doctest --exclude-module=pdb --exclude-module=email --exclude-module=http --exclude-module=urllib --exclude-module=xmlrpc --exclude-module=pydoc --exclude-module=bz2 --exclude-module=lzma --exclude-module=_ssl --exclude-module=ssl --hidden-import=src.core.canvas --hidden-import=src.core.color_palette --hidden-import=src.core.custom_colors --hidden-import=src.core.layer_manager --hidden-import=src.core.project --hidden-import=src.core.undo_manager --hidden-import=src.core.saved_colors --hidden-import=src.tools.base_tool --hidden-import=src.tools.brush --hidden-import=src.tools.eraser --hidden-import=src.tools.eyedropper --hidden-import=src.tools.fill --hidden-import=src.tools.selection --hidden-import=src.tools.shapes --hidden-import=src.tools.pan --hidden-import=src.ui.main_window --hidden-import=src.ui.layer_panel --hidden-import=src.ui.timeline_panel --hidden-import=src.ui.color_wheel --hidden-import=src.ui.theme_manager --hidden-import=src.ui.tooltip --hidden-import=src.utils.export --hidden-import=src.utils.import_png --hidden-import=src.utils.presets --hidden-import=src.utils.file_association --hidden-import=src.animation.timeline --distpath="BUILDER\dist" --workpath="BUILDER\build" --specpath="BUILDER" main.py
if errorlevel 1 (
    echo ERROR: PyInstaller build failed!
    cd BUILDER
    pause
    exit /b 1
)
cd BUILDER

echo [3/6] Checking EXE size...
for %%A in (dist\PixelPerfect.exe) do set EXE_SIZE=%%~zA
set /a EXE_SIZE_MB=EXE_SIZE/1048576
echo Optimized EXE Size: %EXE_SIZE_MB% MB

echo [4/6] Copying assets to distribution folder...
if not exist "dist\assets" mkdir "dist\assets"
xcopy /E /I /Y "..\assets" "dist\assets" >nul

if not exist "dist\docs" mkdir "dist\docs"
xcopy /E /I /Y "..\docs" "dist\docs" >nul

copy /Y "..\register_pixpf_icon.bat" "dist\register_pixpf_icon.bat" >nul

echo [5/6] Creating release package...
if not exist "release" mkdir "release"
xcopy /E /I /Y "dist\*" "release\PixelPerfect" >nul
copy /Y "..\register_pixpf_icon.bat" "release\PixelPerfect\register_pixpf_icon.bat" >nul

echo [6/6] Cleaning up temporary files...
if exist "build" rmdir /s /q "build"
if exist "PixelPerfect.spec" del /q "PixelPerfect.spec"

echo.
echo ====================================
echo    BUILD COMPLETE (OPTIMIZED)!
echo ====================================
echo.
echo Executable location: dist\PixelPerfect.exe
echo Optimized Size: %EXE_SIZE_MB% MB
echo Release package: release\PixelPerfect\
echo.
echo Optimizations Applied:
echo  - Bytecode optimization (--optimize=2)
echo  - Debug symbol stripping (--strip)
echo  - Excluded 15+ unused stdlib modules
echo.
echo Temporary files cleaned up automatically.
echo You can now distribute the contents of release\PixelPerfect\
echo.

pause
