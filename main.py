# Include
from pytubefix import Playlist

# Config
playlist_path = "./playlist/"

# Main
url = input("Enter url here >")
playlist = Playlist(url)
for video in playlist.videos:
    print("Downloading " + video.title + " ...")
    audio_stream = video.streams.get_audio_only()
    audio_stream.download(output_path=playlist_path)
print("\Downloaded all audios successfully!")