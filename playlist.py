import sqlite3
from music_item import MusicItem, MUS_FORMATS


class Playlist(MusicItem):
    def __init__(self, title, id=None):
        self.id = id
        self.title = title
    """
        # def create(self):
        #     conn = sqlite3.connect("database.db")
        #     cursor = conn.cursor()
        #     INSERT_QUERY = f
        #         INSERT INTO playlist (title)
        #         VALUES('{self.title}')
        #     
        #     cursor.execute(INSERT_QUERY)

        #     self.id = cursor.lastrowid

        #     conn.commit()
        #     conn.close()


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

            # @classmethod
        # def get(cls, playlist):
        #     conn = sqlite3.connect("database.db")
        #     cursor = conn.cursor()
        #     SEARCH_QUERY = f"SELECT * FROM playlist WHERE  title LIKE '{playlist}'"
        #     result = cursor.execute(SEARCH_QUERY).fetchone()
        #     conn.close()
        #     if result:
        #         return Playlist(id=result[0], title=result[1])  # {"id": result[0], "title": result[1]}
        #         # print(result[1])
        #     return None
    """

    def add_dir(self, directory: str):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        INSERT_QUERY = f"""
            INSERT INTO directory (path, playlist_id)
              VALUES('{directory}', '{self.id}');
            """
        cursor.execute(INSERT_QUERY)
        conn.commit()
        conn.close()
        return cursor.lastrowid

    def have_dir(self, directory: str):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        INSERT_QUERY = f"""
            SELECT path  FROM directory WHERE playlist_id={self.id};
            """
        result = cursor.execute(INSERT_QUERY).fetchone()
        conn.close()
        if result:
            return True
        return False


    def add_song(self, filename):
        # TODO: add single song to the playlist
        pass

    @classmethod
    def see_playlist(cls, playlist=None):
        if playlist:
            QUERY = f"""
                SELECT id FROM playlist WHERE title LIKE '{playlist}';
            """
            try:
                playlist_id = cls.GET(QUERY)[0]
            except TypeError:
                return f"{playlist} doesn`t exists"
            GET_SONGS = f"""
                SELECT id, filename FROM music
                WHERE playlist_id = '{playlist_id}';
            """
            result = cls.GET(GET_SONGS, many=True)
            for item in result:
                print(f"{item[0]}:  {item[1]}")
        else:
            QUERY = """
                SELECT playlist.title, COUNT(music.playlist_id) as C
                FROM playlist
                LEFT JOIN music ON playlist.id=music.playlist_id;
            """
            result = cls.GET(QUERY, many=True)
            print("[ dir | num ]")
            for item in result:
                print(item[0], "|", item[1])


        # TODO: if many True see playlists names and len items
        # TODO: else see len items and items
        pass

    def __repr__(self):
        return f"""
            Playlist(
                '{self.id}',
                '{self.title}'
            )
        """

    def __str__(self):
        return f"{self.title}"
