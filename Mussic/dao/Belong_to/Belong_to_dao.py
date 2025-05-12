from abc import ABC
from typing import List
from mysql.connector import MySQLConnection, Error
from .Belongto_interface import BelongToDAOInterface
from .Belongto_object import BelongTo
from ..Song.Song_object import Song

class BelongToDAO(BelongToDAOInterface):
    def __init__(self, db_connection: MySQLConnection):
        self.connection = db_connection

    def add_song_to_playlist(self, input_data: BelongTo) -> bool:
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO Belong_to (Song_ID, Playlist_ID)
                VALUES (%s, %s)
            """
            cursor.execute(query, (input_data.song_id, input_data.playlist_id))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error adding song to playlist: {e}")
            return False
        finally:
            cursor.close()

    def remove_song_from_playlist(self, song_id: int, playlist_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            query = """
                DELETE FROM Belong_to
                WHERE Song_ID = %s AND Playlist_ID = %s
            """
            cursor.execute(query, (song_id, playlist_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error removing song from playlist: {e}")
            return False
        finally:
            cursor.close()

    def get_songs_in_playlist(self, playlist_id: int) -> List[Song]:
        songs = []
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT s.Song_ID, s.User_ID, s.Song_Name, s.ArtistName, s.Genre, 
                       s.ReleaseYear, s.Album, s.Upload_Date, s.Duration, s.Bitrate, s.File_Path
                FROM Song s
                JOIN Belong_to bt ON s.Song_ID = bt.Song_ID
                WHERE bt.Playlist_ID = %s
            """
            cursor.execute(query, (playlist_id,))
            for row in cursor.fetchall():
                song = Song(
                    song_id=row[0],
                    user_id=row[1],
                    song_name=row[2],
                    artist_name=row[3],
                    genre=row[4],
                    release_year=row[5],
                    album=row[6],
                    upload_date=row[7],
                    duration=row[8],
                    bitrate=row[9],
                    file_path=row[10]
                )
                songs.append(song)
            return songs
        except Error as e:
            print(f"Error retrieving songs in playlist: {e}")
            return []
        finally:
            cursor.close()