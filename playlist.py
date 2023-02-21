import sqlite3
from music_item import MusicItem, MUS_FORMATS


class Playlist(MusicItem):
    def __init__(self, title, id=None, directory_id=None, artist_id=None,
                 genre_id=None, album_id=None):
        self.title = title
        self.directory_id = directory_id
        self.artist_id = artist_id
        self.genre_id = genre_id
        self.album_id = album_id

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        INSERT_QUERY = f"""
            INSERT INTO playlist (title)
            VALUES('{title}')
        """
        cursor.execute(INSERT_QUERY)

        self.id = cursor.lastrowid

        conn.commit()
        conn.close()


    # @classmethod
    # def exists(cls, title):
    #     conn = sqlite3.connect("database.db")
    #     cursor = conn.cursor()
    #     SEARCH_QUERY = f"SELECT * FROM playlist WHERE  title LIKE '{title}'"
    #     result = cursor.execute(SEARCH_QUERY).fetchone()
    #     conn.close()
    #     if result:
    #         return True
    #     return False

    # @classmethod
    # def update(cls, **kwargs):
    #     conn = sqlite3.connect("database.db")
    #     cursor = conn.cursor()
    #     print(kwargs)
    #     INSERT_QUERY = f"""
    #         INSERT INTO album (title, year)
    #           VALUES('{album}', {year})
    #         """
    #     print()
    #     print(INSERT_QUERY)
    #     # cursor.execute(INSERT_QUERY)
    #     conn.commit()
    #     conn.close()
    def add_dir(self, id, directory):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        INSERT_QUERY = f"""
            INSERT INTO directory (path, album_id)
              VALUES('{directory}', '{id}')
            """
        print()
        print(INSERT_QUERY)      

    @classmethod
    def get(cls, playlist):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        SEARCH_QUERY = f"SELECT * FROM playlist WHERE  title LIKE '{playlist}'"
        result = cursor.execute(SEARCH_QUERY).fetchone()
        conn.close()
        if result:
            return {"id": result[0], "title": result[1]}
        return None

    def __repr__(self):
        return f"""
            Playlist(
                '{self.id}',
                '{self.title}',
                '{self.directory_id}',
                '{self.artist_id}',
                '{self.genre_id}',
                '{self.album_id}'
            )
        """

    # def __str__(self):
    #     return f'({self.id}, {self.title})'
