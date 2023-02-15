from music_item import MusicItem
from album import Album
from artist import Artist
from song import Song
import click
import os


# TODO: this command should not run without this > --scan', '-s'
@click.command()
@click.option('--scan', '-s', default='music', help='/path/to/directory')
def scan(scan):
    formats = ['ogg', 'aac', 'mp3', 'wav', 'acc', 'flac', 'm4a', 'wma']
    dir_list = os.listdir(scan)
    print_list = [item for item in dir_list if item.split('.')[-1] in formats]
    for ix, item in enumerate(print_list, 1):
        print(ix, item)



if __name__ == '__main__':
    scan()


# TODO:
# python3 app.py add-song --tags /path/to/song/tag/json/data
# python3 app.py add-song --title Thriller --artist M. Jackson
# python3 app.py remove-directory /path/to/directory
# python3 app.py show-library
# python3 app.py search-album --album Dark Side of the Moon 