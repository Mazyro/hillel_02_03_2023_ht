import sqlite3

import os


class DB:

    def __init__(self):
        self.db = self.cursor = None

    def __enter__(self):
        self.db = sqlite3.connect(os.path.join(os.getcwd(), 'chinook.db'))
        return self.db.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.commit()
        self.db.close()


if __name__ == '__main__':
    with DB() as cursor:
        res = cursor.execute("select * "
                             "from tracks t "
                             "left join genres g on t.GenreId = g.GenreId "
                             "LEFT JOIN media_types mt ON t.MediaTypeId = mt.MediaTypeId "
                             "WHERE SUBSTRING(UPPER( g.Name), 1, 1) = 'R' and mt.Name = 'AAC audio file'")

        print(res.fetchall())

    with DB() as cursor:
        res = cursor.execute("select t.Name as name, t.Bytes as bytes, t.Milliseconds "
                             "FROM (select t.Name, t.Bytes, t.Milliseconds FROM tracks t "
                             "WHERE t.Milliseconds  > 200) t	ORDER BY t.Bytes DESC 	LIMIT 1")

        print(res.fetchall())

    with DB() as cursor:
        res = cursor.execute("select t.Name , a.Title\
	                            FROM tracks t\
	                            left join albums a on a.AlbumId = t.AlbumId\
	                            left JOIN playlist_track pt ON pt.TrackId  = t.TrackId\
	                            LEFT JOIN playlists p ON pt.PlaylistId = p.PlaylistId\
	                            WHERE p.Name = 'TV Shows'")

        print(res.fetchall())

