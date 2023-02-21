# from music_item import MusicItem
# from album import Album
# from artist import Artist
from song import Song
from album import Album
from music_item import MusicItem
from playlist import Playlist
import click
import os
import mutagen
from mutagen.flac import FLAC
import sqlite3


@click.group()
def mycommands():
    pass


@click.command()
def create_db():
    """ This command creates database with its tables """
    if not os.path.exists("database.db"):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        CREATE_MUSIC = """
            CREATE TABLE music (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                directory_id INTEGER,
                artist_id INTEGER,
                genre_id INTEGER,
                album_id INTEGER,
                FOREIGN KEY (directory_id) REFERENCES directory (id),
                FOREIGN KEY (genre_id) REFERENCES genre (id),
                FOREIGN KEY(artist_id) REFERENCES artist(id),
                FOREIGN KEY(album_id) REFERENCES album(id)
            );
        """
        CREATE_PLAYLIST = """
            CREATE TABLE playlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT
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
            );
        """
        CREATE_DIRECTORY = """
            CREATE TABLE directory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT,
                playlist_id INTEGER,
                FOREIGN KEY(playlist_id) REFERENCES playlist(id)
            );
        """
        cursor.execute(CREATE_GENRE)
        cursor.execute(CREATE_DIRECTORY)
        cursor.execute(CREATE_ALBUM)
        cursor.execute(CREATE_ARTIST)
        cursor.execute(CREATE_PLAYLIST)
        cursor.execute(CREATE_MUSIC)
        conn.commit()
        conn.close()


# TODO: this command should not run without this > --scan', '-s'
@click.command()
@click.option('--scan', '-s', default='m/', required=True, help='/path/to/directory')
def scan(scan):
    """Scan directory"""
    Song.scan(scan)


@click.command()
@click.option("--filename", required=0, type=str, help="/path/to/filename")
@click.option("--tags", default="Unknown", type=str, help="/path/to/song/tag/json/data")
@click.option("--title", "-t", default="Unknown", type=str, help="Title of the song")
@click.option("--genre", "-g",  default="Unknown", type=str, help="Genre of the song")
@click.option("--album", '-a',  default="Unknown", type=str, help="Album of the song")
@click.option("--artist",  default="Unknown", type=str, help="Name of the singer")
def add_song(tags, title, artist, album, genre, filename):
    """This Method is to add a song in a library."""
    song = Song()
    if album:
        print(album)
        song.add_album_to_db(album)



@click.command()
def show_library():
    """Shows library"""
    pass


@click.command()
@click.option("--name", required=1, help="playlist name")
def create_playlist(name):
    """ create playlist by name """
    if name:
        Playlist.create_playlist(name)


@click.command()
@click.option("--album", required=1, type=str, help="Album Title")
def search_album(album):
    """ This command finds album by title"""
    print(Album.search(album))


@click.command()
@click.option("--dir", required=1, prompt="/path/to/directory",
              help="add dir which contains music files")
@click.option("--playlist", "-p", help="playlist name")
def directory(dir, playlist):
    """ Add dir to the playlist"""
    if playlist:
        plist = Playlist.get(playlist)
        if not plist:
            plist = Playlist(title=playlist)
            plist.create()
        plist.add_dir(dir)
        print(f"{dir} added to {playlist}")


mycommands.add_command(scan)
mycommands.add_command(add_song)
mycommands.add_command(show_library)
mycommands.add_command(create_db)
mycommands.add_command(search_album)
mycommands.add_command(create_playlist)
mycommands.add_command(directory)


if __name__ == '__main__':
    # create_db()
    mycommands()


# python3 app.py remove-directory /path/to/directory
# python3 app.py show-library
# python3 app.py search-album --album Dark Side of the Moon
