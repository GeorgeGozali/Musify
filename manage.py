# from music_item import MusicItem
# from album import Album
# from artist import Artist
from song import Song
import click
import os
import mutagen
from mutagen.flac import FLAC
import sqlite3


@click.group()
def mycommands():
    pass


def create_db():
    if not os.path.exists("database.db"):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        CREATE_PLAYLIST = """
            CREATE TABLE playlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                artist_id INTEGER,
                genre_id INTEGER,
                album_id INTEGER,
                FOREIGN KEY (genre_id) REFERENCES genre (id),
                FOREIGN KEY(artist_id) REFERENCES artist(id),
                FOREIGN KEY(album_id) REFERENCES album(id)
            );"""
        CREATE_GENRE = """
            CREATE TABLE genre (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre TEXT
            );"""
        CREATE_ALBUM = """
            CREATE TABLE album (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                year INTEGER
            );"""
        CREATE_ARTIST = """
            CREATE TABLE artist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT
            )
        """
        cursor.execute(CREATE_GENRE)
        cursor.execute(CREATE_ALBUM)
        cursor.execute(CREATE_ARTIST)
        cursor.execute(CREATE_PLAYLIST)
        conn.commit()
        conn.close()



# TODO: this command should not run without this > --scan', '-s'
@click.command()
@click.option('--scan', '-s', default='m/', required=True, help='/path/to/directory')
def scan(scan):
    """Scan directory"""
    formats = ('.aac', '.mp3', '.wav', '.acc', '.flac')
    dir_list = os.listdir(scan)
    print_list = [item for item in dir_list if item.endswith(formats)]
    for ix, item in enumerate(print_list, 1):
        print(ix, item)
    # f = FLAC("m/" + print_list[1])
    # f['title'] = u"Come Together"
    # print(f)
    # f.save()
    # print(dir(f.info))
    # print(f.info.length)


@click.command()
@click.option("--filename", required=1, type=str, help="/path/to/filename")
@click.option("--tags", default="Unknown", type=str, help="/path/to/song/tag/json/data")
@click.option("--title", "-t", default="Unknown", type=str, help="Title of the song")
@click.option("--genre", "-g",  default="Unknown", type=str, help="Genre of the song")
@click.option("--album", '-a',  default="Unknown", type=str, help="Album of the song")
@click.option("--artist",  default="Unknown", type=str, help="Name of the singer")
def add_song(tags, title, artist, album, genre, filename):
    """This Method is to add a song in a library."""
    song = Song()
    data = song.add_song(tags, title, artist, album, genre, filename)
    song.add_song_to_json(data)
    # print(type(s))
    # for k, v in s.items():
    #     print(k, v[0])



@click.command()
def show_library():
    """Shows library"""
    pass


mycommands.add_command(scan)
mycommands.add_command(add_song)
mycommands.add_command(show_library)


if __name__ == '__main__':
    create_db()
    mycommands()


# python3 app.py remove-directory /path/to/directory
# python3 app.py show-library
# python3 app.py search-album --album Dark Side of the Moon
