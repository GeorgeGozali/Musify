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

    @staticmethod
    def DELETE(QUERY: str):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        print(QUERY)
        cursor.execute(QUERY)
        conn.commit()
        conn.close()

    @staticmethod
    def GET(query: str, many=False):
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

    def CREATE(self, QUERY: str):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(QUERY)
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def plus_one(filename: str):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        GET_QUERY = f"SELECT played FROM music WHERE filename ='{filename}'"
        played_num = int(cursor.execute(GET_QUERY).fetchone()[0])
        POST_QUERY = f"""
            UPDATE music SET played = {played_num + 1}
            WHERE filename = '{filename}';
        """
        cursor.execute(POST_QUERY)
        conn.commit()
        conn.close()

    @staticmethod
    def UPDATE(filename: str, table: str, col: str, arg):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        UPDATE_QUERY = f"""
            UPDATE {table} SET {col} = {arg}
            WHERE filename = '{filename}';
        """
        cursor.execute(UPDATE_QUERY)
        conn.commit()
        conn.close()
