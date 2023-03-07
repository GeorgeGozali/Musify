import sqlite3
from music_item import MusicItem


class Album(MusicItem):
    def __init__(
            self, id=None,
            title: str | None = "Unknown Album", year=None
            ):
        self.title = title
        self.year = year
        self.id = id

    @classmethod
    def search(cls, title: str):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        SEARCH_QUERY = f"""
            SELECT title FROM album WHERE title LIKE '{title}';
        """
        cursor.execute(SEARCH_QUERY)
        album = cursor.fetchone()
        conn.close()
        return album

    def __repr__(self):
        return f"""Album(
            '{self.title}',
            {self.year}
            )"""

    def __str__(self):
        return self.title
