@echo off
title APK Runner - Installer
color 0A
setlocal enabledelayedexpansion

echo.
echo ╔══════════════════════════════════════════════╗
echo ║       📱 APK RUNNER - INSTALLER             ║
echo ║         Version 1.0                          ║
echo ╚══════════════════════════════════════════════╝
echo.

:: Set installation directory
set "INSTALL_DIR=%ProgramFiles%\APK Runner"
set "EXE_NAME=APKRunner.exe"

echo 📂 Installing to: %INSTALL_DIR%
echo.

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️  Administrator rights required!
    echo.
    echo Right-click this file and select "Run as Administrator"
    echo.
    pause
    exit /b 1
)

echo ✅ Admin rights confirmed
echo.

:: Create installation folder
echo 📁 Creating folder...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Find EXE
echo 🔍 Finding executable...

set "EXE_FOUND=0"

if exist "dist\%EXE_NAME%" (
    set "EXE_SOURCE=dist\%EXE_NAME%"
    set "EXE_FOUND=1"
    echo ✅ Found: dist\%EXE_NAME%
)

if exist "%EXE_NAME%" (
    set "EXE_SOURCE=%EXE_NAME%"
    set "EXE_FOUND=1"
    echo ✅ Found: %EXE_NAME%
)

if !EXE_FOUND!==0 (
    echo.
    echo ❌ APKRunner.exe not found!
    echo.
    echo Build it first:
    echo   python -m PyInstaller --onefile --windowed --name=APKRunner src\apk_runner.py
    echo.
    pause
    exit /b 1
)

:: Copy EXE
echo.
echo 📦 Installing...
copy /Y "!EXE_SOURCE!" "%INSTALL_DIR%\%EXE_NAME%" >nul
echo ✅ Application copied

:: Copy docs
if exist "README.md" copy /Y "README.md" "%INSTALL_DIR%\" >nul
if exist "LICENSE" copy /Y "LICENSE" "%INSTALL_DIR%\" >nul

:: Desktop shortcut
echo 🔗 Creating shortcuts...
powershell -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\APK Runner.lnk'); $SC.TargetPath = '%INSTALL_DIR%\%EXE_NAME%'; $SC.WorkingDirectory = '%INSTALL_DIR%'; $SC.Save()" 2>nul
echo ✅ Desktop shortcut

:: Start Menu
mkdir "%ProgramData%\Microsoft\Windows\Start Menu\Programs\APK Runner" 2>nul
powershell -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut([Environment]::GetFolderPath('CommonPrograms') + '\APK Runner\APK Runner.lnk'); $SC.TargetPath = '%INSTALL_DIR%\%EXE_NAME%'; $SC.WorkingDirectory = '%INSTALL_DIR%'; $SC.Save()" 2>nul
echo ✅ Start Menu

:: Uninstaller
echo 📝 Creating uninstaller...
(
echo @echo off
echo title Uninstall APK Runner
echo color 0C
echo.
echo ╔══════════════════════════════════════════════╗
echo ║     UNINSTALL APK RUNNER                    ║
echo ╚══════════════════════════════════════════════╝
echo.
echo This will remove APK Runner completely.
echo.
set /p confirm="Continue? (Y/N): "
if /i not "!confirm!"=="Y" exit
echo.
echo 🗑️  Uninstalling...
taskkill /f /im APKRunner.exe 2^>nul
del /Q "%%USERPROFILE%%\Desktop\APK Runner.lnk" 2^>nul
rmdir /S /Q "%%ProgramData%%\Microsoft\Windows\Start Menu\Programs\APK Runner" 2^>nul
rmdir /S /Q "%INSTALL_DIR%" 2^>nul
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\APK Runner" /f 2^>nul
echo.
echo ✅ Uninstall complete!
pause
) > "%INSTALL_DIR%\uninstall.bat"
echo ✅ Uninstaller

:: Registry
echo 📝 Registering...
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\APK Runner" /v "DisplayName" /d "APK Runner" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\APK Runner" /v "UninstallString" /d "\"%INSTALL_DIR%\uninstall.bat\"" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\APK Runner" /v "DisplayIcon" /d "\"%INSTALL_DIR%\%EXE_NAME%\"" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\APK Runner" /v "Publisher" /d "Neshley" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\APK Runner" /v "DisplayVersion" /d "1.0" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\APK Runner" /v "URLInfoAbout" /d "https://github.com/Neshley/apk-runner" /f >nul 2>&1

:: Done
echo.
echo ╔══════════════════════════════════════════════╗
echo ║     ✅ INSTALLATION COMPLETE!               ║
echo ╚══════════════════════════════════════════════╝
echo.
echo 📱 APK Runner v1.0 installed!
echo 📂 %INSTALL_DIR%
echo.
echo 🎯 Launch: Desktop shortcut or Start Menu
echo 🗑️  Uninstall: Control Panel ^> Programs
echo.
set /p launch="🚀 Launch now? (Y/N): "
if /i "%launch%"=="Y" start "" "%INSTALL_DIR%\%EXE_NAME%"
echo.
pause