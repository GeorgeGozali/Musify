from music_item import MusicItem, MUS_FORMATS
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError, ID3, TPE1, TIT2, TALB, TCON
# from playsound import playsound
import os
from pydub import AudioSegment
from pydub.playback import play
import json
import sqlite3
from artist import Artist
from genre import Genre
from album import Album


class Song(MusicItem):
    def __init__(
            self, filename, title=None, id=None, favorites=False, directory_id=None,
            artist_id=None, genre_id=None, album_id=None, playlist_id=None):
        self.id = id
        self.filename = filename
        self.title = title
        self.favorites = favorites
        self.directory_id = directory_id
        self.artist_id = artist_id
        self.genre_id = genre_id
        self.album_id = album_id
        self.playlist_id = playlist_id

    def write_track_with_tags(
            self, dir_name: str, dir_id: int, playlist_id: int):
        # print(dir_name)
        # print(dir_id)
        # print(playlist_id)
        print()
        filename = os.path.join(dir_name, self.filename)
        audio_file = EasyID3(filename)
        title = audio_file.get('title')[0]

        try:
            artist = Song.GET(f"""
                SELECT id FROM artist
                WHERE full_name = '''{audio_file.get("artist")[0]}''';
            """)
            artist = Artist(*artist)
        except TypeError:
            artist = Artist(full_name=audio_file.get("artist")[0])
            artist.CREATE(QUERY=f"""
                INSERT INTO artist (full_name)
                VALUES('''{artist.full_name}''')
            """)
        try:
            genre = Song.GET(f"""
                SELECT * FROM genre
                WHERE genre = '''{audio_file.get("genre")[0]}''';
                """)
            genre = Genre(*genre)
        except TypeError:
            genre = Genre(genre=audio_file.get("genre")[0])
            genre.CREATE(f"""
                INSERT INTO genre (genre)
                VALUES('''{genre.genre}''')
            """)
        try:
            album = Song.GET(f"""
                SELECT * FROM album
                WHERE title = '''{audio_file.get("album")[0]}''';
            """)
            print(album)
            album = Album(*album)
        except TypeError:
            album = Album(title=audio_file.get("album")[0])
            album.CREATE(f"""
                INSERT INTO album (title)
                VALUES('''{album.title}''');
            """)
        self.CREATE(
            f"""
            INSERT INTO music (
                title, filename, directory_id,
                artist_id, album_id, genre_id, playlist_id
                )
            VALUES(
                '''{title}''', '''{filename}''', {dir_id},
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
                    audio_file['artist'] = u"Unknown artist"
                if not audio_file.get("title"):
                    audio_file['title'] = u"Unknown title"
                if not audio_file.get("album"):
                    audio_file['album'] = u"Unknown album"
                if not audio_file.get("genre"):
                    audio_file["genre"] = u"Unknown genre"
                audio_file.save(filename)
            except ID3NoHeaderError:
                if filename.endswith((".wav", ".aac")):
                    audio_file = ID3()
                    audio_file.add(TPE1(encoding=3, text=u'Unknown artist'))
                    audio_file.add(TIT2(encoding=3, text=u'Unknown title'))
                    audio_file.add(TALB(encoding=3, text=u'Unknown album'))
                    audio_file.add(TCON(encoding=3, text=u"Unknown genre"))
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
        print(UPDATE_QUERY)
        cursor.execute(UPDATE_QUERY)
        conn.commit()
        conn.close()

    @staticmethod
    def play(music: list[str] | str) -> None:
        if isinstance(music, str):
            music = [music]
        for item in music:
            if item.endswith(MUS_FORMATS):
                name = item.split('/')[-1]
                format = name.split(".")[-1]
            try:
                Song.plus_one(name)
                song = AudioSegment.from_file(item, format)

                print(f"\nplaying: {name}\n")
                play(song)

            except Exception:
                print(f"\ncan`t play {name}\n")

    @staticmethod
    def path_plus_filename(item: tuple[str]):
        if len(item) == 2:
            return os.path.join(item[1], item[0])
        return False

    def __repr__(self):
        return f"""Song.add_song(
            '{self.title}',
            '{self.favorites}',
            '{self.directory_id}',
            '{self.artist_id}',
            '{self.genre_id}',
            '{self.album_id},
            '{self.playlist_id}')"""

    @staticmethod
    def add_tags_from_json(json_file: str, filename: str):
        with open(json_file) as f:
            data = json.load(f)
            Song.add_tags(
                title=data['title'],
                artist=data['artist'],
                album=data['album'],
                genre=data['genre'],
                filename=filename)

    @staticmethod
    def is_favorite(filename):
        result = Song.GET(
            f"""
                SELECT favorites FROM music
                WHERE filename = '{filename.split("/")[-1]}'
            """)[0]
        return result

    @classmethod
    def favorites(cls, filename: str, arg: int):
        Song.UPDATE(
            filename=filename.split("/")[-1],
            table="music",
            col="favorites",
            arg=arg
        )
