import sqlite3

from prettytable import PrettyTable

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

    @classmethod
    def see_playlist(cls, playlist_name=None):
        if playlist_name:
            playlist = cls.GET(table="playlist", col="name", row=playlist_name)
            if not playlist:
                return f"{playlist_name} doesn`t exists"
            result = cls.GET(
                table="music", col="playlist_id", row=playlist.id, many=True
            )
            if result:
                myTable = PrettyTable(["id", "title", "played"])
                for item in result:
                    myTable.add_row([item[0], item[1], item[4]])
                return myTable
            else:
                return f"playlist: {playlist} doesn`t contans any songs!"
        else:
            QUERY = """
                SELECT playlist.name, COUNT(music.playlist_id) as C
                FROM playlist
                LEFT JOIN music ON playlist.id=music.playlist_id;
            """
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            result = cur.execute(QUERY)
            myTable = PrettyTable(["Directory", "Number of tracks"])
            for item in result:
                myTable.add_row([item[0], item[1]])
            return myTable

    def __repr__(self):
        return f"""
            Playlist(
                '{self.id}',
                '{self.title}'
            )
        """

    def __str__(self):
        return f"{self.title}"
