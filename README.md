# 📦 Download .mp3 from playlist youtube

## 📚 Table of Contents

- [📦 Download .mp3 from playlist youtube](#-download-mp3-from-playlist-youtube)
  - [📚 Table of Contents](#-table-of-contents)
  - [📝 About](#-about)
  - [📁 Source](#-source)
  - [🚀 Getting Started](#-getting-started)
    - [💻 Technology](#-technology)
    - [🛠️ Build / Verification](#️-build--verification)
  - [🔗 Reference](#-reference)

## 📝 About

> Script to download YouTube videos and convert them to audio files (.mp3 files)

## 📁 Source

```
.
├── build/                              # PyInstaller build artifacts
├── dist/                               # Packaged application workspace
│   ├── playlist/                       # Downloaded .mp3 files
│   ├── downloaded.txt                  # Download history (prevents re-downloads)
│   ├── www.youtube.com_cookies.txt     # Your YouTube cookies
│   └── YoutubePlaylistDownloader.exe   # Application executable
├── app.py                              # Main source code
├── build.bat                           # Build script
├── playlist.txt                        # Playlist URL input
├── requirements.txt                    # Python dependencies
├── www.youtube.com_cookies.txt         # Your YouTube cookies
├── YoutubePlaylistDownloader.spec       # PyInstaller configuration
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### 💻 Technology

- python
- yt_dlp
- pyinstaller
- FFmpeg
- deno
- Make sure internet connection; youTube playlist must be PUBLIC

### 🛠️ Build / Verification

- Install packs manually
```powershell
pip install -U "yt-dlp[default]"
irm https://deno.land/install.ps1 | iex
```
- Install FFmpeg .zip, extract it, add path/to/bin to PATH of environment variables
- Export your youtube cookie
- Run build.bat (include install required packs)
- Run dist/YoutubePlaylistDownloader.exe
- Enter url of your playlist
- Audio files are saved in folder **dist/playlist** defaultly

## 🔗 Reference

- https://www.geeksforgeeks.org/installation-guide/how-to-install-ffmpeg-on-windows/
- https://github.com/BtbN/FFmpeg-Builds/releases
