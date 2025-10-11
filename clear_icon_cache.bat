@echo off
echo ========================================
echo   Windows Icon Cache Clearer
echo ========================================
echo.
echo This will clear Windows icon cache and restart Explorer.
echo Press any key to continue...
pause >nul

echo.
echo [1/4] Stopping Windows Explorer...
taskkill /f /im explorer.exe

echo [2/4] Clearing icon cache...
cd /d %userprofile%\AppData\Local
attrib -h IconCache.db
del IconCache.db /a
del /f /s /q /a IconCache.db
rmdir /s /q Microsoft\Windows\Explorer\IconCache*

echo [3/4] Clearing thumbnail cache...
del /f /s /q /a thumbcache_*.db

echo [4/4] Restarting Windows Explorer...
start explorer.exe

echo.
echo ========================================
echo   Icon Cache Cleared!
echo ========================================
echo.
echo Now try running: BUILDER\release\PixelPerfect\PixelPerfect.exe
echo.
pause

