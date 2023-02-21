import sqlite3
MUS_FORMATS = ('.mp3', '.wav', '.acc', '.flac')


class MusicItem:

    # @staticmethod
    @classmethod
    def add_album_to_db(cls, album, year='Null'):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        INSERT_QUERY = f"""
            INSERT INTO album (title, year)
              VALUES('{album}', {year})
            """
        print(INSERT_QUERY)
        cursor.execute(INSERT_QUERY)
        conn.commit()
        conn.close()

    @staticmethod
    def add_dir_to_playlist(dir):
        #  TODO: add music files from directory to playlist
        #  TODO: use scan method
        #  TODO: add Dir column in playlist table
        pass




    def search(self):
        #  TODO: find album, artist, genre, music with one code
        pass
