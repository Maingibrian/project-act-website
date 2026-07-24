@echo off
chcp 65001 >nul
echo Compressing hero video with ffmpeg...
echo.

if not exist "Images\Video 1.mp4" (
    echo ERROR: Images\Video 1.mp4 not found
    pause
    exit /b 1
)

ffmpeg -i "Images\Video 1.mp4" ^
    -vf "scale=-2:720" ^
    -c:v libx264 -preset slow -crf 23 ^
    -c:a aac -b:a 128k ^
    -movflags +faststart ^
    -y "Images\Video-720p.mp4"

if exist "Images\Video-720p.mp4" (
    echo.
    echo Compression complete.
    for %%I in ("Images\Video-720p.mp4") do echo Output size: %%~zI bytes (%%~zI / 1024 / 1024 MB)
) else (
    echo.
    echo ERROR: Compression failed. Ensure ffmpeg is installed and in PATH.
)

pause
