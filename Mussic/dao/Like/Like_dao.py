from abc import ABC
from typing import List
from mysql.connector import MySQLConnection, Error
from .Like_interface import LikeDAOInterface
from .Like_object import Like
from ..Song.Song_object import Song

class LikeDAO(LikeDAOInterface):
    def __init__(self, db_connection: MySQLConnection):
        self.connection = db_connection

    def like_song(self, input_data: Like) -> bool:
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO LikedSongs (User_ID, Song_ID, Liked_At)
                VALUES (%s, %s, NOW())
            """
            cursor.execute(query, (input_data.user_id, input_data.song_id))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error liking song: {e}")
            return False
        finally:
            cursor.close()

    def unlike_song(self, user_id: int, song_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            query = """
                DELETE FROM LikedSongs
                WHERE User_ID = %s AND Song_ID = %s
            """
            cursor.execute(query, (user_id, song_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error unliking song: {e}")
            return False
        finally:
            cursor.close()

    def get_liked_songs_by_user(self, user_id: int) -> List[Song]:
        songs = []
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT s.Song_ID, s.User_ID, s.Song_Name, s.ArtistName, s.Genre, 
                       s.ReleaseYear, s.Album, s.Upload_Date, s.Duration, s.Bitrate, s.File_Path
                FROM Song s
                JOIN LikedSongs ls ON s.Song_ID = ls.Song_ID
                WHERE ls.User_ID = %s
            """
            cursor.execute(query, (user_id,))
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
            print(f"Error retrieving liked songs: {e}")
            return []
        finally:
            cursor.close()