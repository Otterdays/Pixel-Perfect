@echo off
REM ===================================================
REM Pixel Perfect - Build Script (OPTIMIZED)
REM Creates standalone Windows executable
REM Optimizations: bytecode optimization, 17+ module exclusions
REM Target: ~24-25 MB (from 29 MB baseline, 330 MB original)
REM Build Time: ~45-48 seconds
REM ===================================================

echo.
echo ====================================
echo  Pixel Perfect - Build Script
echo  MAXIMUM OPTIMIZATION MODE
echo ====================================
echo.

REM Start timer
set START_TIME=%time%
echo Build started at: %START_TIME%
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
python -m PyInstaller --name="PixelPerfect" --onefile --windowed --optimize=2 --icon="%ICON_PATH%" --add-data="%LOGO_PATH%;." --exclude-module=pygame --exclude-module=scipy --exclude-module=tkinter.test --exclude-module=unittest --exclude-module=test --exclude-module=xml.etree --exclude-module=xml.dom --exclude-module=doctest --exclude-module=pdb --exclude-module=email --exclude-module=http --exclude-module=urllib --exclude-module=xmlrpc --exclude-module=pydoc --exclude-module=bz2 --exclude-module=lzma --exclude-module=_ssl --exclude-module=ssl --exclude-module=charset_normalizer --exclude-module=pycparser --hidden-import=src.core.canvas --hidden-import=src.core.color_palette --hidden-import=src.core.custom_colors --hidden-import=src.core.layer_manager --hidden-import=src.core.project --hidden-import=src.core.undo_manager --hidden-import=src.core.saved_colors --hidden-import=src.tools.base_tool --hidden-import=src.tools.brush --hidden-import=src.tools.eraser --hidden-import=src.tools.eyedropper --hidden-import=src.tools.fill --hidden-import=src.tools.selection --hidden-import=src.tools.shapes --hidden-import=src.tools.pan --hidden-import=src.ui.main_window --hidden-import=src.ui.layer_panel --hidden-import=src.ui.timeline_panel --hidden-import=src.ui.color_wheel --hidden-import=src.ui.theme_manager --hidden-import=src.ui.tooltip --hidden-import=src.utils.export --hidden-import=src.utils.import_png --hidden-import=src.utils.presets --hidden-import=src.utils.file_association --hidden-import=src.animation.timeline --distpath="BUILDER\dist" --workpath="BUILDER\build" --specpath="BUILDER" main.py
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

REM Calculate build time
set END_TIME=%time%
call :GetSeconds %START_TIME% START_SECONDS
call :GetSeconds %END_TIME% END_SECONDS
set /a ELAPSED_SECONDS=END_SECONDS-START_SECONDS
if %ELAPSED_SECONDS% lss 0 set /a ELAPSED_SECONDS+=86400

REM Convert to minutes and seconds
set /a ELAPSED_MINUTES=ELAPSED_SECONDS/60
set /a ELAPSED_SECS=ELAPSED_SECONDS%%60

echo.
echo ====================================
echo    BUILD COMPLETE (OPTIMIZED)!
echo ====================================
echo.
echo Executable location: dist\PixelPerfect.exe
echo Optimized Size: %EXE_SIZE_MB% MB
echo Release package: release\PixelPerfect\
echo.
echo Build Duration: %ELAPSED_MINUTES%m %ELAPSED_SECS%s
echo Started: %START_TIME%
echo Finished: %END_TIME%
echo.
echo Optimizations Applied:
echo  - Bytecode optimization (--optimize=2)
echo  - Excluded 17+ unused modules (stdlib + charset_normalizer + pycparser)
echo  - Removed pygame and scipy dependencies
echo.
echo Temporary files cleaned up automatically.
echo You can now distribute the contents of release\PixelPerfect\
echo.

pause
exit /b 0

:GetSeconds
REM Convert time to seconds
set TIME_STR=%1
set TIME_STR=%TIME_STR::=,%
set TIME_STR=%TIME_STR:.=,%
for /f "tokens=1-4 delims=," %%a in ("%TIME_STR%") do (
    set /a HH=%%a
    set /a MM=%%b
    set /a SS=%%c
)
set /a %2=HH*3600 + MM*60 + SS
exit /b
