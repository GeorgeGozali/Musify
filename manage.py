# from music_item import MusicItem
# from album import Album
# from artist import Artist
# from song import Song
import click
import os
import mutagen
from mutagen.flac import FLAC


@click.group
def mycommands():
    pass


# TODO: this command should not run without this > --scan', '-s'
@click.command()
@click.option('--scan', '-s', default='m/', required=True, help='/path/to/directory')
def scan(scan):
    """Scan directory"""
    formats = ['ogg', 'aac', 'mp3', 'wav', 'acc', 'flac', 'm4a', 'wma']
    dir_list = os.listdir(scan)
    print_list = [item for item in dir_list if item.split('.')[-1] in formats]
    for ix, item in enumerate(print_list, 1):
        print(ix, item)
    f = FLAC("m/" + print_list[1])
    f['title'] = u"Come Together"
    print(f)
    f.save()
    # print(dir(f.info))
    # print(f.info.length)


@click.command()
@click.option("--filename", required=1, help="/path/to/filename")
@click.option("--tags", help="/path/to/song/tag/json/data")
@click.option("--title", "-t", help="Title of the song")
@click.option("--artist", help="Name of the singer")
def add_song(tags, title, artist, filename):
    """This Method is to add a song in a library."""
    pass


@click.command()
def show_library():
    """Shows library"""
    pass


mycommands.add_command(scan)
mycommands.add_command(add_song)
mycommands.add_command(show_library)


if __name__ == '__main__':
    mycommands()


# python3 app.py remove-directory /path/to/directory
# python3 app.py show-library
# python3 app.py search-album --album Dark Side of the Moon
