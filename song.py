from music_item import MusicItem, MUS_FORMATS
import mutagen
from mutagen.easyid3 import EasyID3


class Song(MusicItem):

    def add_song(tags, title, artist, album, genre, filename):
        print("title", title)
        print("artist", artist)
        print("genre", genre)
        if filename.endswith(MUS_FORMATS):
            try:
                audio_file = EasyID3(filename)
            except mutagen.id3.ID3NoHeaderError:
                audio_file = mutagen.File(filename)  # , easy=True)
                audio_file.add_tags()#(ID3=EasyID3)

            try:
                audio_file['title'] = title
                audio_file['artist'] = artist
                audio_file['album'] = album
                audio_file['genre'] = genre
                audio_file.save(filename)
                print(audio_file)
            except TypeError:
                pass
        changed = EasyID3(filename)
        for k, v in changed.items():
            print(f"{k}: {v}")
