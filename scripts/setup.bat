@echo off
setlocal EnableDelayedExpansion

REM Define the path to your .env.local file
set "ENV_FILE=.env"

REM Check if the .env file exists
if not exist "%ENV_FILE%" (
    echo Error: %ENV_FILE% not found.
    goto :eof
)

REM Loop through each line in the .env file
for /f "usebackq tokens=1,* delims==" %%i in ("%ENV_FILE%") do (
    set "key=%%i"
    set "val=%%j"
    if not "!key!"=="" (
        if not "!key:~0,1!"=="#" (
            set "!key!=!val!"
            echo Set environment variable: !key!
        )
    )
)

:: Create superuser
services\pocketbase\pocketbase.exe superuser upsert %PB_ADMIN_EMAIL% %PB_ADMIN_PASSWORD%
echo superuser created.

services\pocketbase\pocketbase.exe migrate up
echo setup complete!