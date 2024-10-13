# Include
import sys
from pytubefix import Playlist


# Config
playlist_path = "./playlist/"


# Main
if sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print("""
    How to run:
        python main.py <url-of-your-playlist>
    """)
else:
    playlist = Playlist(sys.argv[1])

    for video in playlist.videos:
        print("Downloading " + video.title + " ...")
        audio_stream = video.streams.get_audio_only()
        audio_stream.download(output_path=playlist_path, mp3=True)

    print("\nHandle all audios successfully!")
