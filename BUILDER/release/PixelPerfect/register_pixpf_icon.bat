@echo off
REM Register .pixpf file icon in Windows Registry

set ICON_PATH=%~dp0assets\icons\pixpf_icon.ico

if not exist "%ICON_PATH%" (
    echo ERROR: Icon file not found
    pause
    exit /b 1
)

echo Registering .pixpf file icon...

reg add "HKEY_CURRENT_USER\Software\Classes\.pixpf" /ve /d "PixelPerfect.Project" /f
reg add "HKEY_CURRENT_USER\Software\Classes\PixelPerfect.Project" /ve /d "Pixel Perfect Project" /f
reg add "HKEY_CURRENT_USER\Software\Classes\PixelPerfect.Project\DefaultIcon" /ve /d "%ICON_PATH%,0" /f

echo.
echo Done! Restart Explorer or reboot to see changes.
echo To clear icon cache: del %localappdata%\IconCache.db
pause

