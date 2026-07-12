@echo off
setlocal
set "USERPROFILE=%CD%"
set "HOME=%CD%"
set "HYPERFRAMES_BROWSER_PATH=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
set "HYPERFRAMES_FFMPEG_PATH=%CD%\node_modules\@ffmpeg-installer\win32-x64\ffmpeg.exe"
set "HYPERFRAMES_FFPROBE_PATH=%CD%\node_modules\@ffprobe-installer\win32-x64\ffprobe.exe"
call "C:\Users\97014\AppData\Local\npm-cache\_npx\702923228c2ce1e6\node_modules\.bin\hyperframes.cmd" render --output "..\..\xunfang-tutorial.mp4" --fps 30 --quality standard --workers 1 --no-browser-gpu --skill website-to-hyperframes
exit /b %ERRORLEVEL%
