@echo off
REM Run this on your Windows machine, inside the folder containing app.py

pip install -r requirements.txt

pyinstaller --noconfirm --onefile --windowed --name "YoutubePlaylistDownloader" app.py

echo.
echo Done. Your exe is in the "dist" folder: dist\YoutubePlaylistDownloader.exe
echo Copy your cookie file (www.youtube.com_cookies.txt) next to the .exe if you use one.
pause
