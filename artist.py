from music_item import MusicItem


class Artist(MusicItem):
    def __init__(self, full_name='Unknown Artist'):
        self.full_name = full_name
