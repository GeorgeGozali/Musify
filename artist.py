from music_item import MusicItem


class Artist(MusicItem):
    def __init__(self, id=None, full_name='Unknown Artist'):
        self.id = id
        self.full_name = full_name

    def __repr__(self):
        return f"""
            Artist(
                '{self.id}',
                '{self.full_name}'
            )
        """

    def __str__(self):
        return self.full_name
