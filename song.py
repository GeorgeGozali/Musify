from music_item import MusicItem


class Song(MusicItem):
    def __init__(self, name, year, album, artist):
        self.name = name
        self.year = year
        self.album = album
        self.artist = artist
        
