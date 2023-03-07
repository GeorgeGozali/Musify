import json

import os
import sqlite3

import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TALB, TCON, TIT2, TPE1, ID3NoHeaderError
from pydub import AudioSegment
from pydub.playback import play

from album import Album
from artist import Artist
from genre import Genre
from music_item import MUS_FORMATS, MusicItem


class Song(MusicItem):
    def __init__(
        self,
        filename,
        title=None,
        id=None,
        favorite=False,
        directory_id=None,
        artist_id=None,
        genre_id=None,
        album_id=None,
        playlist_id=None,
    ):
        self.id = id
        self.filename = filename
        self.title = title
        self.favorite = favorite
        self.directory_id = directory_id
        self.artist_id = artist_id
        self.genre_id = genre_id
        self.album_id = album_id
        self.playlist_id = playlist_id

    def write_track_with_tags(self, dir_name: str, dir_id: int, playlist_id: int):
        filename = os.path.join(dir_name, self.filename)
        audio_file = EasyID3(filename)
        title = audio_file.get("title")[0]
        artist = Artist.GET(
            table="artist", col="full_name", row=audio_file.get("artist")[0]
        )
        if not artist:
            artist = Artist(full_name=audio_file.get("artist")[0])
            artist.CREATE(
                QUERY=f"""
                INSERT INTO artist (full_name)
                VALUES('{artist.full_name}')
            """
            )
        genre = Genre.GET(table="genre", col="name", row=audio_file.get("genre")[0])
        if not genre:
            genre = Genre(genre=audio_file.get("genre")[0])
            genre.CREATE(
                f"""
                INSERT INTO genre (name)
                VALUES('{genre.genre}')
            """
            )

        album = Album.GET(table="album", col="title", row=audio_file.get("album")[0])
        if not album:
            album = Album(title=audio_file.get("album")[0])
            album.CREATE(
                f"""
                INSERT INTO album (title)
                VALUES('{album.title}');
            """
            )
        self.CREATE(
            f"""
            INSERT INTO music (
                title, filename, directory_id,
                artist_id, album_id, genre_id, playlist_id
                )
            VALUES(
                '{title}', '{filename}', {dir_id},
                {artist.id}, {album.id},{genre.id},{playlist_id}
                );
        """
        )

    @staticmethod
    def scan(directory: str):
        dir_list = os.listdir(directory)
        music_list = [item for item in dir_list if item.endswith(MUS_FORMATS)]

        for item in music_list:
            filename = os.path.join(directory, item)
            try:
                audio_file = EasyID3(filename)
                if not audio_file.get("artist"):
                    audio_file["artist"] = "Unknown artist"
                if not audio_file.get("title"):
                    audio_file["title"] = "Unknown title"
                if not audio_file.get("album"):
                    audio_file["album"] = "Unknown album"
                if not audio_file.get("genre"):
                    audio_file["genre"] = "Unknown genre"
                audio_file.save(filename)
            except ID3NoHeaderError:
                if filename.endswith((".wav", ".aac")):
                    audio_file = ID3()
                    audio_file.add(TPE1(encoding=3, text="Unknown artist"))
                    audio_file.add(TIT2(encoding=3, text="Unknown title"))
                    audio_file.add(TALB(encoding=3, text="Unknown album"))
                    audio_file.add(TCON(encoding=3, text="Unknown genre"))
                    audio_file.save(os.path.join(filename))
        return music_list

    def get_tags(self, dir_name: str):
        filename = os.path.join(dir_name, self.filename)
        audio_file = EasyID3(filename)
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        UPDATE_QUERY = f"""
            UPDATE music SET (author = '{audio_file["author"]}', title = '{audio_file["title"]}')
            WHERE filename = '{filename}';
        """
        # print(UPDATE_QUERY)
        cursor.execute(UPDATE_QUERY)
        conn.commit()
        conn.close()

    @staticmethod
    def play(music: list[str] | str) -> None:
        if isinstance(music, str):
            music = [music]
        for item in music:
            # print(item)
            if item.endswith(MUS_FORMATS):
                name = item.split("/")[-1]
                format = name.split(".")[-1]
            try:
                Song.plus_one(item)
                song = AudioSegment.from_file(item, format)
                print(f"\nplaying: {name}\n")
                play(song)
            except Exception:
                print(f"\ncan`t play <{name}>\n")
            break

    @staticmethod
    def path_plus_filename(item: tuple[str]):
        if len(item) == 2:
            return os.path.join(item[1], item[0])
        return False

    def add_tags(filename, args_dict: dict):
        if filename and filename.endswith(MUS_FORMATS):
            try:
                audio_file = EasyID3(filename)
            except mutagen.id3.ID3NoHeaderError:
                audio_file = mutagen.File(filename)  # , easy=True)
                audio_file.add_tags()  # (ID3=EasyID3)

            try:
                for key, value in args_dict.items():
                    if value is not None:
                        audio_file[key] = value
                        audio_file.save(filename)
            except Exception:
                return False

    @staticmethod
    def add_tags_from_json(json_file: str, filename: str):
        with open(json_file) as f:
            data = json.load(f)
            print(data)
            Song.add_tags(filename=filename, args_dict=data)

    @staticmethod
    def is_favorite(filename):
        result = Song.GET(
            f"""
                SELECT favorite FROM music
                WHERE filename = '{filename.split("/")[-1]}'
            """
        )[0]
        return result

    @classmethod
    def favorites(cls, filename: str, arg: int):
        Song.UPDATE(
            filename=filename.split("/")[-1], table="music", col="favorite", arg=arg
        )

    def __repr__(self):
        return f"""Song.add_song(
            '{self.title}',
            '{self.favorites}',
            '{self.directory_id}',
            '{self.artist_id}',
            '{self.genre_id}',
            '{self.album_id},
            '{self.playlist_id}')"""

    def __str__(self):
        return self.filename
