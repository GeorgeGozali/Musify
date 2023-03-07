import sqlite3
from music_item import MusicItem


class Playlist(MusicItem):
    def __init__(self, id=None, title: str | None = "Unknown Playlist"):
        self.id = id
        self.title = title

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

    @staticmethod
    def get_dir(dir_path):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        GET_QUERY = f"""
            SELECT id FROM directory WHERE path='{dir_path}';
            """
        print(GET_QUERY)
        result = cursor.execute(GET_QUERY).fetchone()
        conn.close()
        if result:
            return result
        return False

    def add_song(self, filename):
        # TODO: add single song to the playlist
        pass

    # @classmethod
    # def GET(cls, name: str):
    #     conn = sqlite3.connect("database.db")
    #     cursor = conn.cursor()
    #     GET_QUERY = f"""
    #         SELECT name, id FROM playlist
    #         WHERE name LIKE '{name}';
    #     """
    #     print(GET_QUERY)
    #     try:
    #         result = cursor.execute(GET_QUERY).fetchone()
    #         conn.close()
    #         return cls(*result)
    #     except sqlite3.OperationalError:
    #         conn.close()
    #         return False
    #     except TypeError:
    #         return False

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
            try:
                for item in result:
                    print(f"{item[0]}:  {item[1]}")
            except TypeError:
                return f"playlist: {playlist} doesn`t contans any songs!"
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
