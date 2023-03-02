import sqlite3
from music_item import MusicItem


class Album(MusicItem):
    def __init__(self, id=None, title: str | None = None, year=None):
        self.title = title
        self.year = year
        self.id = id

    # def create(self):
    #     conn = sqlite3.connect("database.db")
    #     cursor = conn.cursor()
    #     INSERT_QUERY = f"""
    #         INSERT INTO album (title, year)
    #         VALUES('{self.title}', '{self.year}')
    #     """
    #     cursor.execute(INSERT_QUERY)
    #     self.id = cursor.lastrowid
    #     conn.commit()
    #     conn.close()

    # @classmethod
    # def get(cls, album):
    #     conn = sqlite3.connect("database.db")
    #     cursor = conn.cursor()
    #     SEARCH_QUERY = f"SELECT * FROM album WHERE  title LIKE '{album}'"
    #     result = cursor.execute(SEARCH_QUERY).fetchone()
    #     conn.close()
    #     if result:
    #         return Album(id=result[0], title=result[1])
    #     return None

    def __repr__(self):
        return f"Album('{self.title}', {self.year})"

    def __str__(self):
        return self.title

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
