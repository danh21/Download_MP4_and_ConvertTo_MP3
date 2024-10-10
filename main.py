from pytubefix import Playlist


# Config
playlist_url = "https://www.youtube.com/playlist?list=PLnLNse3s5NSur0jeszOqIVMZkxC3kr_QA"
playlist_path = "./playlist/"


playlist = Playlist(playlist_url)

for video in playlist.videos:
    print("Downloading " + video.title + " ...")
    audio_stream = video.streams.get_audio_only()
    audio_stream.download(output_path=playlist_path, mp3=True)

print("Handle all audios successfully!")
