import yt_dlp

# path to save the downloaded files
playlist_path = "./playlist/"

url = input("Enter url of playlist: ")

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': playlist_path + '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'ignoreerrors': True,
    # get cookies from your browser and save them in this file
    'cookiefile': 'www.youtube.com_cookies.txt',
    # write cache of downloaded files to this file to avoid re-downloading
    'download_archive': 'downloaded.txt',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Done!")