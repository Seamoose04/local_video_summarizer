@echo off
setlocal

:: Stop on error (simulate with error checks)
set VERSION=0.29.1
set FILENAME=pocketbase_%VERSION%_windows_amd64.zip
set DOWNLOAD_URL=https://github.com/pocketbase/pocketbase/releases/download/v%VERSION%/%FILENAME%
set TARGET_DIR=pocketbase

echo Downloading PocketBase %VERSION%...
curl -L -o "%FILENAME%" "%DOWNLOAD_URL%"
if errorlevel 1 (
    echo ❌ Failed to download PocketBase.
    exit /b 1
)

echo Unzipping...
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"
powershell -Command "Expand-Archive -Path '%FILENAME%' -DestinationPath '%TARGET_DIR%' -Force"
if errorlevel 1 (
    echo ❌ Failed to unzip.
    exit /b 1
)

:: Clean up
del "%FILENAME%"

echo Installed PocketBase %VERSION% to .\%TARGET_DIR%\pocketbase.exe

endlocal