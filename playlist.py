import sqlite3
from music_item import MusicItem, MUS_FORMATS


class Playlist(MusicItem):
    def __init__(self, title, id=None):
        self.id = id
        self.title = title

    def create(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        INSERT_QUERY = f"""
            INSERT INTO playlist (title)
            VALUES('{self.title}')
        """
        cursor.execute(INSERT_QUERY)

        self.id = cursor.lastrowid

        conn.commit()
        conn.close()

    """
            # @classmethod
            # def update(cls, **kwargs):
            #     conn = sqlite3.connect("database.db")
            #     cursor = conn.cursor()
            #     print(kwargs)
            #     INSERT_QUERY = f
            #         INSERT INTO album (title, year)
            #           VALUES('{album}', {year})
            #         
            #     print()
            #     print(INSERT_QUERY)
            #     # cursor.execute(INSERT_QUERY)
            #     conn.commit()
            #     conn.close()
    """

    def add_dir(self, directory):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        INSERT_QUERY = f"""
            INSERT INTO directory (path, playlist_id)
              VALUES('{directory}', '{self.id}');
            """
        cursor.execute(INSERT_QUERY)
        print(INSERT_QUERY)
        conn.commit()
        conn.close()

    @classmethod
    def get(cls, playlist):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        SEARCH_QUERY = f"SELECT * FROM playlist WHERE  title LIKE '{playlist}'"
        result = cursor.execute(SEARCH_QUERY).fetchone()
        conn.close()
        if result:
            return Playlist(id=result[0], title=result[1])  # {"id": result[0], "title": result[1]}
            # print(result[1])
        return None

    def __repr__(self):
        return f"""
            Playlist(
                '{self.id}',
                '{self.title}'
            )
        """

    def __str__(self):
        return self.title
