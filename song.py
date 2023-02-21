from music_item import MusicItem, MUS_FORMATS
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError, ID3, TPE1, TIT2, TALB
import os
import sqlite3


class Song(MusicItem):

    # TODO: make @classmethod to instantiate music items
    def add_song(self, tags, title, artist, album, genre, filename):
        if filename.endswith(MUS_FORMATS):
            try:
                audio_file = EasyID3(filename)
            except mutagen.id3.ID3NoHeaderError:
                audio_file = mutagen.File(filename)  # , easy=True)
                audio_file.add_tags()  # (ID3=EasyID3)

            try:
                audio_file['title'] = title
                audio_file['artist'] = artist
                audio_file['album'] = album
                audio_file['genre'] = genre
                audio_file.save(filename)
                # print(audio_file)
            except TypeError:
                pass
        # changed = EasyID3(filename)
        # for k, v in changed.items():
        #     print(f"{k}: {v}")
        # return audio_file
        # self.add_song_to_db(audio_file)

    def add_song_to_db(self, audio_file):
        ADD_TO_DB = """
            INSERT INTO playlist ( title ,begin_date,end_date)
              VALUES(?,?,?)
        """
        # print(audio_file)

    @staticmethod
    def scan(directory: str):
        formats = ('.mp3', '.wav', '.aac', '.flac')
        dir_list = os.listdir(directory)
        music_list = [item for item in dir_list if item.endswith(formats)]

        for item in music_list:
            filename = os.path.join(directory, item)
            try:
                audio_file = EasyID3(filename)
                if not audio_file.get("artist"):
                    audio_file['artist'] = u"Unknown artist"
                if not audio_file.get("title"):
                    audio_file['title'] = u"Unknown title"
                if not audio_file.get("album"):
                    audio_file['album'] = u"Unknown album"
                audio_file.save(filename)
            except ID3NoHeaderError:
                if filename.endswith((".wav", ".aac")):
                    audio_file = ID3()
                    audio_file.add(TPE1(encoding=3, text=u'Unknown artist'))
                    audio_file.add(TIT2(encoding=3, text=u'Unknown title'))
                    audio_file.add(TALB(encoding=3, text=u'Unknown album'))
                    audio_file.save(os.path.join(filename))
            print(item)
            for key, value in audio_file.items():
                print(f"{key}: {value}")
            print()

    def __repr__(self):
        return f"Song.add_song('{self.tags}', '{self.title}', '{self.artist}',\
            '{self.album}', '{self.genre}', '{self.filename}')"

    def add_to_favorites(self):
        #  TODO: add music file to favorites
        pass
