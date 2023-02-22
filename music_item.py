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
        cursor.execute(INSERT_QUERY)
        conn.commit()
        conn.close()

    @staticmethod
    def add_dir(dir):
        #  TODO: add music files from directory to playlist
        #  TODO: use scan method
        #  TODO: add Dir column in playlist table
        pass

    @staticmethod
    def play(playlist=None, filename=None):
        # TODO: play playlist
        # TODO: play single music file
        pass

    def search(self):
        #  TODO: find album, artist, genre, music with one code
        pass

    def POST(query):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()

    def GET(query, many=False):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        if many:
            result = cursor.execute(query).fetchall()
        else:
            result = cursor.execute(query).fetchone()
        conn.commit()
        conn.close()
        if result:
            return result
        return None

    def CREATE(self, QUERY):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(QUERY)
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()