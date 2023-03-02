from music_item import MusicItem


class Genre(MusicItem):
    def __init__(self, id=None, genre: str | None = "Unknown genre"):
        self.id = id
        self.genre = genre

    def __repr__(self):
        return f"""
            Genre(
                '{self.id}',
                '{self.genre}'
            )
        """
