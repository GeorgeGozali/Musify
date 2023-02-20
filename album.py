import sqlite3
from music_item import MusicItem


class Album(MusicItem):
    def __init__(self, title, year):
        self.title = title
        self.year = year

    def __repr__(self):
        return f"Album('{self.title}', {self.year})"

    def __str__(self):
        return self.title

    @classmethod
    def search(cls, title):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        SEARCH_QUERY = f"""
            SELECT title FROM album WHERE title LIKE '{title}';
        """
        cursor.execute(SEARCH_QUERY)
        album = cursor.fetchone()
        conn.close()
        return album
