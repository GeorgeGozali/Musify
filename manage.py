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
                filename TEXT,
                favorites INTEGER DEFAULT 0,
                played INTEGER DEFAULT 0,
                directory_id INTEGER,
                artist_id INTEGER,
                genre_id INTEGER,
                album_id INTEGER,
                playlist_id INTEGER,
                FOREIGN KEY (directory_id) REFERENCES directory (id),
                FOREIGN KEY (genre_id) REFERENCES genre (id),
                FOREIGN KEY(artist_id) REFERENCES artist(id),
                FOREIGN KEY(album_id) REFERENCES album(id),
                FOREIGN KEY(playlist_id) REFERENCES playlist(id)
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
@click.option("--playlist", help="name of the playlist")
@click.option("--fav", default=True, help="add to favorite")
def add_song(tags, title, artist, album, genre, filename, playlist, fav):
    """This Method is to add a song in a library."""
    # song = Song()
    if tags:
        # TODO: add tags to the song and in the db
        pass
    if title:
        # TODO: add title tag to the song
        pass
    if genre:
        # TODO: add genre tag to the song
        pass
    if album:
        # TODO: add album tag to the song
        # TODO: add song to album
        pass
    if artist:
        # TODO: add artist to the song
        pass
    if playlist:
        # TODO: add song to playlist
        pass
    if fav:
        # TODO: add song to favorites
        # TODO: remove song from favorites
        pass


@click.command()
@click.option("--playlist", help="playlist name")
def show_library(playlist):
    """Shows library"""
    if playlist:
        Playlist.see_playlist(playlist)
    else:
        Playlist.see_playlist()


@click.command()
@click.option("--name", required=1, help="playlist name")
def create_playlist(name):
    """ create playlist by name """
    if name:
        plist = Playlist.GET(
            f"""
                SELECT * FROM playlist WHERE title LIKE '{name}';
            """
        )
        if not plist:
            plist = Playlist(title=name)
            plist.CREATE(
                f"""
                    INSERT INTO playlist (title) 
                    VALUES('{name}');
                """
            )


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
    if not os.path.exists(dir):
        print("Enter directory with valid path")
        return False
    if playlist:
        plist = Playlist.GET(
            f"SELECT * FROM playlist WHERE  title LIKE '{playlist}'"
            )
        if plist:
            plist = Playlist(*plist[::-1])
        else:
            plist = Playlist(title=playlist)
            plist.CREATE(
                f"""
                INSERT INTO playlist (title)
                VALUES('{playlist}')
            """)
        if not plist.have_dir(dir):
            new_dir = plist.add_dir(dir)
            print(f"{dir} added to {playlist}\n")
            print("Scanning directory...\n")
            print("Adding songs to the library...\n")
            songs_list = Song.scan(dir)
            for song in songs_list:
                song = Song(filename=song)
                song.CREATE(
                    f"""
                    INSERT INTO music (filename, directory_id, playlist_id)
                    VALUES('{song.filename}', {new_dir}, {plist.id})
                """
                )
            return True
        else:
            print(f"{dir} is already added to {playlist}.")
            return False
        

@click.command()
@click.option("--dir", prompt="dir name",
              help="remove dir from playlist with its files")
def delete(dir):
    """Delete directory and its content by name"""
    if dir:
        directory = Song.GET(
            f"SELECT id FROM directory WHERE  path LIKE '%{dir}'"
        )
        if directory:
            Song.DELETE(f"DELETE FROM directory WHERE id = '{directory[0]}'")
            Song.DELETE(f"DELETE FROM music WHERE directory_id = '{directory[0]}'")
            print(f"{dir} has been removed from playlist!")
            return True
        else:
            print(f"{dir} dir does not exists in a playlist")
            return False
    return False


@click.command()
@click.option("--playlist", '-p', help="Choose playlist you want to play")
@click.option("--song", help="play song by name")
@click.option("-id", help="play song by id")
@click.option("--dir", help="play directory by name")
def play(playlist, song, id, dir):
    """Play music"""
    if playlist:
        id = Playlist.GET(f"SELECT id FROM playlist WHERE title='{playlist}'")[0]
        music_list = Playlist.GET(
            f"""SELECT music.filename, directory.path
            FROM music
            LEFT join directory ON music.directory_id=directory.id
            WHERE music.playlist_id ='{id}';
            """, many=True)
        play_list = [os.path.join(item[1], item[0]) for item in music_list]
        Song.play(play_list)
    elif song:
        pass


mycommands.add_command(scan)
mycommands.add_command(add_song)
mycommands.add_command(show_library)
mycommands.add_command(create_db)
mycommands.add_command(search_album)
mycommands.add_command(create_playlist)
mycommands.add_command(directory)
mycommands.add_command(delete)
mycommands.add_command(play)


if __name__ == '__main__':
    # create_db()
    mycommands()


# python3 app.py remove-directory /path/to/directory
# python3 app.py show-library
# python3 app.py search-album --album Dark Side of the Moon
