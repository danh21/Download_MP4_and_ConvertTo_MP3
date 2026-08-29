@echo off
REM Run this on your Windows machine, inside the folder containing app.py

pip install -r requirements.txt

pyinstaller --noconfirm --onedir --windowed --name "YoutubePlaylistDownloader" app.py

REM Add template placeholder files into the built app folder
echo # Netscape HTTP Cookie File > "dist\YoutubePlaylistDownloader\www.youtube.com_cookies.txt"
echo # Replace this file with your real exported cookies (see README) >> "dist\YoutubePlaylistDownloader\www.youtube.com_cookies.txt"
type nul > "dist\YoutubePlaylistDownloader\downloaded.txt"

echo.
echo Done. Your app folder is in: dist\YoutubePlaylistDownloader\
echo Run YoutubePlaylistDownloader.exe INSIDE that folder (do not move the exe out alone).
echo Replace www.youtube.com_cookies.txt inside that folder with your real exported cookies.
pause
