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
    def add_tags_db(QUERY):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        print(QUERY)
        conn.commit()
        conn.close()
        return cursor.lastrowid

    @staticmethod
    def add_dir(dir):
        #  TODO: add music files from directory to playlist
        #  TODO: use scan method
        #  TODO: add Dir column in playlist table
        pass

    @classmethod
    def search(cls, search_word: str, table: str, col: str):
        #  TODO: find album, artist, genre, music with one code
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        GET_QUERY = f"""
            SELECT * FROM {table};
        """
        print(GET_QUERY)
        result = cursor.execute(GET_QUERY).fetchall()
        print(result)
        conn.commit()
        conn.close()
        # print(result)
        if result:
            for r in result:
                print(r)
        # self.__class__.__name__

    @staticmethod
    def DELETE(QUERY: str):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        print(QUERY)
        cursor.execute(QUERY)
        conn.commit()
        conn.close()

    # @staticmethod
    # def GET(query: str, many=False):
    #     print(query)
    #     conn = sqlite3.connect("database.db")
    #     cursor = conn.cursor()
    #     if many:
    #         result = cursor.execute(query).fetchall()
    #     else:
    #         result = cursor.execute(query).fetchone()
    #     conn.commit()
    #     conn.close()
    #     if result:
    #         return result
    #     return None
    @classmethod
    def GET(cls, table: str, col: str, row: str):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        GET_QUERY = f"""
            SELECT id, {col} FROM '{table}'
            WHERE {col} LIKE '{row}';
        """
        result = cursor.execute(GET_QUERY).fetchone()
        conn.close()
        if result:
            return cls(*result)
        return False

    def CREATE(self, QUERY: str):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        print(QUERY)
        cursor.execute(QUERY)
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return cursor.lastrowid

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
