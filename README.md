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
├── playlist/                       # output
├── main.py                         # main app
├── www.youtube.com_cookies.txt     # your youtube cookie
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### 💻 Technology

- python
- yt_dlp
- FFmpeg
- deno
- Make sure internet connection; youTube playlist must be PUBLIC

### 🛠️ Build / Verification

- Install packs
```powershell
pip install -U "yt-dlp[default]"
irm https://deno.land/install.ps1 | iex
```
- Install FFmpeg .zip, extract it, add path/to/bin to PATH of environment variables
- Export your youtube cookie
- Run main.py script, enter url of your playlist
- Audio files are saved in folder **playlist** defaultly (configured in **main.py**)

## 🔗 Reference

- https://www.geeksforgeeks.org/installation-guide/how-to-install-ffmpeg-on-windows/
- https://github.com/BtbN/FFmpeg-Builds/releases