from music_item import MusicItem, MUS_FORMATS
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError, ID3, TPE1, TIT2, TALB
# from playsound import playsound
import os
from pydub import AudioSegment
from pydub.playback import play
import json


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

    @staticmethod
    def add_tags(
        filename,
        args_dict: dict
    ):

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
            except TypeError:
                pass

    def add_song_to_db(self, audio_file):
        ADD_TO_DB = """
            INSERT INTO playlist ( title ,begin_date,end_date)
              VALUES(?,?,?)
        """
        # print(audio_file)

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
                audio_file.save(filename)
            except ID3NoHeaderError:
                if filename.endswith((".wav", ".aac")):
                    audio_file = ID3()
                    audio_file.add(TPE1(encoding=3, text=u'Unknown artist'))
                    audio_file.add(TIT2(encoding=3, text=u'Unknown title'))
                    audio_file.add(TALB(encoding=3, text=u'Unknown album'))
                    audio_file.save(os.path.join(filename))
        return music_list

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

    def add_to_favorites(self):
        #  TODO: add music file to favorites
        pass

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
