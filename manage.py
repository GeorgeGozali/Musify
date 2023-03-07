from song import Song
from album import Album
from playlist import Playlist
from artist import Artist
from genre import Genre
from song import Song
import click
import os
from mutagen.easyid3 import EasyID3
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


@click.command()
@click.option('--dir', '-d', default='m/', required=True, help='/path/to/directory')
def scan(dir):
    """Scan directory"""
    click.echo(f"\nscaning... {dir}\n")
    music_list = Song.scan(dir)
    click.echo(f"There are {len(music_list)} music files in {dir}\n")
    for item in music_list:
        click.echo(item)


@click.command()
@click.option("--filename", required=1, type=str, help="/path/to/filename")
@click.option("--tags", type=str, help="/path/to/json_data")
@click.option("--title", "-t", type=str, help="Title of the song")
@click.option("--genre", "-g",  type=str, help="Genre of the song")
@click.option("--album", '-a', type=str, help="Album of the song")
@click.option("--artist",  type=str, help="Name of the singer")
@click.option("--fav", is_flag=True, help="add to favorites")
@click.option("--rmfav", '-rf', is_flag=True, help="remove from favorites")
def add(
    filename, fav, rmfav, **kwargs
):
    """This Method is to add a song in a library."""

    # Add Tags, if user inputs any of them
    if any(kwargs.values()):
        Song.add_tags(filename, kwargs)

    # Add Tags, if user adds json file of tags
    if kwargs['tags']:
        # TODO: add tags to the song and in the db
        Song.add_tags_from_json(
            json_file="/home/george/Music/tags/test.json", filename=filename)
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


@click.command()
@click.option("--name", "-n", required=0, help="playlist name")
@click.option("--fav", is_flag=True, help="see favorites")
@click.option("--create", '-c', is_flag=True, help="create new playlist")
def playlist(name, fav, create):
    """ create or show playlist by name"""
    if name and create:
        plist = Playlist.GET(
            table="playlist",
            col="name",
            row=name
        )
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
        click.echo("id | favorites | title")
        for track in playlist:
            print(track[0], track[3], track[1])
    elif fav:
        fav_list = Song.GET(
            table="music",
            col="favorites",
            row=1,
            many=True
        )
        print(fav_list)
        if fav_list:
            if len(fav_list) > 0:
                click.echo("Your favorite tracks, if you want to play, go <play --fav> method\n")
                for item in fav_list:
                    click.echo(item[0])
        else:
            click.echo(
                "You have no favorites,\
                    \nif you want to add go <add --fav> \
                        \nmethod with --filename")
    else:
        Playlist.see_playlist()


@click.command()
@click.option("--album", required=1, type=str, help="Album Title")
def search_album(album):
    """ This command finds album by title"""
    click.echo(Album.search(album))


@click.command()
@click.option(
    "--name", required=1,
    help="add dir path which contains music files")
@click.option("--playlist", "-p", help="playlist name")
@click.option("--delete", is_flag=True, help="delete directory with its music files")
def directory(name, playlist, delete):
    """ Add/remove dir to/from the playlist"""
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
            """)
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
                Song.DELETE(
                    f"DELETE FROM directory WHERE id = '{directory[0]}'")
                Song.DELETE(
                    f"DELETE FROM music WHERE directory_id = '{directory[0]}'")
                click.echo(f"{name} has been removed from playlist!")
                return True
            else:
                click.echo(f"{name} dir does not exists in a playlist")
                return False
        return False


@click.command()
@click.option("--playlist", '-p', help="Choose playlist you want to play")
@click.option("--title", help="play song by name")
@click.option("--id", help="play song by id")
@click.option("--dir", help="play directory by name")
@click.option("--fav", is_flag=True, help="play favorites")
def play(playlist, title, id, dir, fav):
    """Play music"""
    if playlist:
        playlist = Playlist.GET(
            table="playlist",
            col="name",
            row=playlist
        )
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        music_list = cur.execute(
            f"""SELECT music.filename, directory.path
            FROM music
            LEFT join directory ON music.directory_id=directory.id
            WHERE music.playlist_id ='{playlist.id}';
            """).fetchall()
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
            """).fetchone()
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
            """).fetchall()
        if music_list:
            play_list = [Song.path_plus_filename(item) for item in music_list]
            Song.play(play_list)
        else:
            click.echo("You do not have favorites")
    conn.close()


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
mycommands.add_command(create_db)
mycommands.add_command(search)
mycommands.add_command(search_album)
mycommands.add_command(directory)
mycommands.add_command(play)

if __name__ == '__main__':
    # create_db()
    mycommands()
