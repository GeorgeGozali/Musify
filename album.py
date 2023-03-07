from music_item import MusicItem


class Album(MusicItem):
    def __init__(
            self, id=None,
            title: str | None = "Unknown Album", year=None
            ):
        self.title = title
        self.year = year
        self.id = id

    def __repr__(self):
        return f"""Album(
            '{self.title}',
            {self.year}
            )"""

    def __str__(self):
        return self.title
