# from music_item import MusicItem
# from album import Album
# from artist import Artist
from song import Song
from album import Album
from playlist import Playlist
import click
import os
import mutagen
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
    click.echo(fav)
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
@click.option("--playlist", help="playlist name")
@click.option("--fav", is_flag=True, help="see favorites")
def show(playlist, fav):
    """Shows library"""
    if playlist:
        click.echo(Playlist.see_playlist(playlist))
    elif fav:
        fav_list = Song.GET("""
            SELECT music.filename, directory.path
            FROM music
            LEFT join directory ON music.directory_id=directory.id
            WHERE music.favorites =1;
            """, many=True)
        if len(fav_list) > 0:
            click.echo("Your favorite tracks, if you want to play, go <play --fav> method\n")
            for item in fav_list:
                click.echo(item[0])
        else:
            click.echo(
                "You have no favorites,\
                    if you want to add go <add --fav> \
                        \nmethod with --filename")
    else:
        Playlist.see_playlist()


@click.command()
@click.option("--name", required=1, help="playlist name")
def playlist(name):
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
    click.echo(Album.search(album))


@click.command()
@click.option(
    "--dir", required=1,
    help="add dir path which contains music files")
@click.option("--playlist", "-p", help="playlist name")
@click.option("--delete", is_flag=True, help="delete directory with its music files")
def directory(dir, playlist, delete):
    """ Add/remove dir to/from the playlist"""
    if not os.path.exists(dir):
        click.echo("Enter directory with valid path")
        return False

    elif playlist and not delete:
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
            click.echo(f"{dir} added to {playlist}\n")
            click.echo("Scanning directory...\n")
            click.echo("Adding songs to the library...\n")
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
            click.echo(f"{dir} is already added to {playlist}.")
            return False
    elif delete:
        confirm = input(f"Do you realy want to delete {dir}? (yes/no) ")
        if confirm.lower() in ("yes", "y"):
            directory = Song.GET(
                f"SELECT id FROM directory WHERE  path LIKE '%{dir}'"
            )
            if directory:
                Song.DELETE(f"DELETE FROM directory WHERE id = '{directory[0]}'")
                Song.DELETE(f"DELETE FROM music WHERE directory_id = '{directory[0]}'")
                click.echo(f"{dir} has been removed from playlist!")
                return True
            else:
                click.echo(f"{dir} dir does not exists in a playlist")
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
        playlist_id = Playlist.GET(f"SELECT id FROM playlist WHERE title='{playlist}'")[0]
        music_list = Playlist.GET(
            f"""SELECT music.filename, directory.path
            FROM music
            LEFT join directory ON music.directory_id=directory.id
            WHERE music.playlist_id ='{playlist_id}';
            """, many=True)
        play_list = [Song.path_plus_filename(item) for item in music_list]
        Song.play(play_list)
    elif title:
        pass
    elif id:
        music_file = Playlist.GET(
            f"""SELECT music.filename, directory.path
            FROM music
            LEFT join directory ON music.directory_id=directory.id
            WHERE music.id ='{id}';
            """)
        song_filename = Song.path_plus_filename(music_file)
        Song.play(song_filename)
    elif dir:
        music_list = Song.scan(dir)
        play_list = [Song.path_plus_filename((item, dir)) for item in music_list]
        Song.play(play_list)
    elif fav:
        music_list = Playlist.GET(
            """SELECT music.filename, directory.path
            FROM music
            LEFT join directory ON music.directory_id=directory.id
            WHERE music.favorites =1;
            """, many=True)
        play_list = [Song.path_plus_filename(item) for item in music_list]
        Song.play(play_list)


mycommands.add_command(scan)
mycommands.add_command(add)
mycommands.add_command(show)
mycommands.add_command(create_db)
mycommands.add_command(search_album)
mycommands.add_command(playlist)
mycommands.add_command(directory)
mycommands.add_command(play)


if __name__ == '__main__':
    # create_db()
    mycommands()
