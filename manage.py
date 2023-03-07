import click
import os
from prettytable import PrettyTable
import sqlite3

from album import Album
from artist import Artist
from genre import Genre
from song import Song
from playlist import Playlist


@click.group()
def mycommands():
    pass


# This Command creates database and its tables
@click.command()
def init_db():
    """This command creates database with its tables"""
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
                name TEXT
            );"""
        CREATE_GENRE = """
            CREATE TABLE genre (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
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


# This Command lists music files in directory, add ID3 tags
# python3 manage.py scan --dir /home/george/Music/
@click.command()
@click.option("--dir", "-d", default="m/", required=True, help="/path/to/directory")
def scan(dir):
    """Scan directory"""
    if not os.path.exists(dir):
        click.echo("Enter directory with valid path")
        return False
    click.echo(f"\nscaning... {dir}\n")
    music_list = Song.scan(dir)
    click.echo(f"There are {len(music_list)} music files in {dir}\n")
    myTable = PrettyTable(["Num", "Filename"])
    for idx, item in enumerate(music_list, 1):
        myTable.add_row([idx, item])
    click.echo(myTable)


# This Command add tags with json
# User can add each tag
# User can add track in favorites and remove, by dir/filename
"""
    python3 manage.py add-song --filename /home/george/Music/Led-Zeppelin-
    Stairway-To-Heaven.mp3 -t Stairway To Heaven -g Rock
"""
"""
    python3 manage.py add-song --filename /home/george/Music/Led-Zeppelin-
    Stairway-To-Heaven.mp3 --tags /home/george/Music/data/test/json
"""
"""
    python3 manage.py add --filename /home/george/Music/Led-Zeppelin-Stairway
    -To-Heaven.mp3  --fav
"""


@click.command()
@click.option("--filename", required=1, type=str, help="/path/to/filename")
@click.option("--tags", type=str, help="/path/to/json_data")
@click.option("--title", "-t", type=str, help="Title of the song")
@click.option("--genre", "-g", type=str, help="Genre of the song")
@click.option("--album", "-a", type=str, help="Album of the song")
@click.option("--artist", type=str, help="Name of the singer")
@click.option("--fav", is_flag=True, help="add to favorites")
@click.option("--rmfav", "-rf", is_flag=True, help="remove from favorites")
def add(filename, fav, rmfav, **kwargs):
    """This Method is to add a song in a library."""

    # Add Tags, if user inputs any of them
    if any(kwargs.values()):
        Song.add_tags(filename, kwargs)

    # Add Tags, if user adds json file of tags
    if kwargs["tags"]:
        Song.add_tags_from_json(
            json_file="/home/george/Music/tags/test.json", filename=filename
        )
    if fav:
        if Song.is_favorite(filename):
            click.echo("\nThis song is already in favorites")
            click.echo("if you want to remove, go with <--rmfav> or <-rf>")
        else:
            Song.favorites(filename=filename, arg=fav)
            click.echo("\nThat song added to favorites")
    elif rmfav:
        if not Song.is_favorite(filename):
            click.echo("\nThis song is not in favorites, do you want to add?")
        else:
            Song.favorites(filename=filename, arg=fav)
            click.echo("\nThat song removed from favorites")


# With this command is possible to see or create new playlist
# See favorites
@click.command()
@click.option("--name", "-n", required=0, help="playlist name")
@click.option("--fav", is_flag=True, help="see favorites")
@click.option("--create", "-c", is_flag=True, help="create new playlist")
def playlist(name, fav, create):
    """create or show playlist by name"""
    if name and create:
        plist = Playlist.GET(table="playlist", col="name", row=name)
        if not plist:
            plist = Playlist(title=name)
            plist.CREATE(
                f"""
                    INSERT INTO playlist (title)
                    VALUES('{name}');
                """
            )
            click.echo(f"playlit: {name} has created!")
        else:
            click.echo(f"{name} already exists")
    elif name:
        playlist = Playlist.see_playlist(name)
        click.echo(playlist)
    elif fav:
        fav_list = Song.GET(table="music", col="favorites", row=1, many=True)
        if fav_list:
            if len(fav_list) > 0:
                click.echo(
                    "Your favorite tracks, if you want to play, go <play --fav> method\n"
                )
                for item in fav_list:
                    click.echo(item[0])
        else:
            click.echo(
                "You have no favorites,\
                    \nif you want to add go <add --fav> \
                        \nmethod with --filename"
            )
    else:
        result = Playlist.see_playlist()
        click.echo(result)


# With this command is possible to add or delete directory from playlist
# tracks located in directory will add or remove from playlist
# python3 manage.py directory --name "/home/george/Music" --playlist name
@click.command()
@click.option("--name", required=1, help="add dir path which contains music files")
@click.option("--playlist", "-p", help="playlist name")
@click.option("--delete", is_flag=True, help="delete directory with its music files")
def directory(name, playlist, delete):
    """Add/remove dir to/from the playlist"""
    if not os.path.exists(name):
        click.echo("Enter directory with valid path")
        return False

    elif playlist and not delete:
        plist = Playlist.GET(table="playlist", col="name", row=playlist)
        if not plist:
            plist = Playlist(title=playlist)
            plist.CREATE(
                f"""
                INSERT INTO playlist (name)
                VALUES('{playlist}')
            """
            )
        if not plist.have_dir(name):
            new_dir = plist.add_dir(name)
            click.echo(f"{dir} added to {playlist}\n")
            click.echo("Scanning directory...\n")
            click.echo("Adding songs to the library...\n")
            songs_list = Song.scan(name)
            for song in songs_list:
                song = Song(filename=song)
                song.write_track_with_tags(
                    dir_name=name, dir_id=new_dir, playlist_id=plist.id
                )
            return True
        else:
            click.echo(f"{name} is already added to {playlist}.")
            return False

    elif delete:
        confirm = input(f"Do you realy want to delete {name}? (yes/no) ")
        if confirm.lower() in ("yes", "y"):
            directory = Playlist.get_dir(dir_path=name)
            if directory:
                Song.DELETE(f"DELETE FROM directory WHERE id = '{directory[0]}'")
                Song.DELETE(f"DELETE FROM music WHERE directory_id = '{directory[0]}'")
                click.echo(f"{name} has been removed from playlist!")
                return True
            else:
                click.echo(f"{name} dir does not exists in a playlist")
                return False
        return False


# with this command is possible to play playlist
# or play directory, or play favorites, or play by id
# python3 manage.py play --playlist test
# python3 manage.py play --id 3
@click.command()
@click.option("--playlist", "-p", help="Choose playlist you want to play")
@click.option("--title", help="play song by name")
@click.option("--id", help="play song by id")
@click.option("--dir", help="play directory by name")
@click.option("--fav", is_flag=True, help="play favorites")
def play(playlist, title, id, dir, fav):
    """Play music"""
    if playlist:
        playlist = Playlist.GET(table="playlist", col="name", row=playlist)
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        music_list = cur.execute(
            f"""SELECT music.filename, directory.path
            FROM music
            LEFT join directory ON music.directory_id=directory.id
            WHERE music.playlist_id ='{playlist.id}';
            """
        ).fetchall()
        play_list = [Song.path_plus_filename(item) for item in music_list]
        Song.play(play_list)
    elif title:
        pass
    elif id:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        music_file = cur.execute(
            f"""SELECT music.filename, directory.path
            FROM music
            LEFT join directory ON music.directory_id=directory.id
            WHERE music.id ='{id}';
            """
        ).fetchone()
        song_filename = Song.path_plus_filename(music_file)
        Song.play(song_filename)
    elif dir:
        music_list = Song.scan(dir)
        play_list = [Song.path_plus_filename((item, dir)) for item in music_list]
        Song.play(play_list)
    elif fav:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        music_list = cur.execute(
            """SELECT music.filename, directory.path
            FROM music
            LEFT join directory ON music.directory_id=directory.id
            WHERE music.favorites =1;
            """
        ).fetchall()
        if music_list:
            play_list = [Song.path_plus_filename(item) for item in music_list]
            Song.play(play_list)
        else:
            click.echo("You do not have favorites")
    conn.close()


# With this command is possible to find anything by keyword
# python3 manage.py search -k "Led Zep"
@click.command()
@click.option("--keyword", "-k", required=1, help="Find Anything by keyword")
def search(keyword):
    """Find Anything by keyword"""
    tracks = Song.search(keyword, table="music", col="title")
    albums = Album.search(keyword, table="album", col="title")
    artists = Artist.search(keyword, table="artist", col="full_name")
    genres = Genre.search(keyword, table="genre", col="name")
    print(f"Here is the result with this search keyword <{keyword}>:\n")
    if tracks:
        print("Tracks")
        for single_track in tracks:
            print("\t", single_track[1])
    if albums:
        print("\nAlbums")
        for single_album in albums:
            print("\t", single_album[1])
    if artists:
        print("\nArtists")
        for single_artist in artists:
            print("\t", single_artist[1])
    if genres:
        print("\nGenres")
        for single_genre in genres:
            print("\t", single_genre[1])


mycommands.add_command(scan)
mycommands.add_command(add)
mycommands.add_command(playlist)
mycommands.add_command(init_db)
mycommands.add_command(search)
mycommands.add_command(directory)
mycommands.add_command(play)

if __name__ == "__main__":
    mycommands()
