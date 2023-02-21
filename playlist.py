import sqlite3
from music_item import MusicItem, MUS_FORMATS


class Playlist(MusicItem):
    def __init__(self, title, directory_id=None, artist_id=None,
                 genre_id=None, album_id=None):
        self.title = title
        self.directory_id = directory_id
        self.artist_id = artist_id
        self.genre_id = genre_id
        self.album_id = album_id

    @classmethod
    def create_playlist(self, title: str):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        INSERT_QUERY = f"""
            INSERT INTO playlist (title)
            VALUES('{title}')
        """
        cursor.execute(INSERT_QUERY)
        conn.commit()
        conn.close()

        Playlist(title)

    def __repr__(self):
        return f"""
            Playlist(
                '{self.title}',
                '{self.directory_id}',
                '{self.artist_id}',
                '{self.genre_id}',
                '{self.album_id}'
            )
        """
