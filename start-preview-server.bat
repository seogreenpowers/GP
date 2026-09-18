@echo off
echo Starting Green Powers preview server...
echo Open Chrome and go to: http://localhost:8080
echo Press Ctrl+C to stop the server.
cd /d "%~dp0"
py -m http.server 8080
pause
