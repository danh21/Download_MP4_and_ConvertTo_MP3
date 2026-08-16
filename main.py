import yt_dlp

playlist_path = "./playlist/"   # path to save the downloaded files
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
    'cookiefile': 'www.youtube.com_cookies.txt', # get cookies from your browser and save them in this file
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Done!")