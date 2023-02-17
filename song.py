from music_item import MusicItem, MUS_FORMATS
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.aac import AAC
# import json
import os
import sqlite3


class Song(MusicItem):

    def connect_db(self, db_name="database.db"):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        return cursor

    def save(self):
        self.conn.commit()
        self.conn.close()

    def add_song(self, tags, title, artist, album, genre, filename):
        # print("title", title)
        # print("artist", artist)
        # print("genre", genre)
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
        self.add_song_to_db(audio_file)

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
            except mutagen.id3.ID3NoHeaderError as e:
                # audio_file = mutagen.File(filename, easy=True)
                # audio_file.add_tags()  # (ID3=EasyID3)
                # print(e)
                pass
            # except mutagen.id3._util.ID3NoHeaderError as e:
            #     print(e)
            #     if item.endswith(".aac"):
            #         audio_file = AAC(filename, easy=True)
            #         audio_file.add_tags()
            except TypeError:
                pass
            try:
                audio_file['artist'] = audio_file.get("artist", "Unknown artist")
                audio_file['genre'] = audio_file.get("genre", "Unknown genre")
                audio_file['album'] = audio_file.get("album", "Unknown album")
                audio_file['title'] = audio_file.get("title", "Unknown title")
                audio_file = audio_file.save()
            except Exception as e:
                # print(e)
                pass