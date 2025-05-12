from abc import ABC
from typing import List, Optional
from mysql.connector import MySQLConnection, Error
from .Song_interface import SongDAOInterface, SongInput
from .Song_object import Song

class SongDAO(SongDAOInterface):
    def __init__(self, db_connection: MySQLConnection):
        self.connection = db_connection

    def add_song(self, input_data: 'SongInput') -> Optional[Song]:
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO Song (User_ID, Song_Name, ArtistName, Genre, ReleaseYear, Album, 
                                Upload_Date, Duration, Bitrate, File_Path)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s)
            """
            cursor.execute(query, (
                input_data.user_id, input_data.song_name, input_data.artist_name, 
                input_data.genre, input_data.release_year, input_data.album,
                input_data.duration, input_data.bitrate, input_data.file_path
            ))
            self.connection.commit()
            song_id = cursor.lastrowid
            return Song(
                song_id=song_id,
                user_id=input_data.user_id,
                song_name=input_data.song_name,
                artist_name=input_data.artist_name,
                genre=input_data.genre,
                release_year=input_data.release_year,
                album=input_data.album,
                upload_date=None,
                duration=input_data.duration,
                bitrate=input_data.bitrate,
                file_path=input_data.file_path
            )
        except Error as e:
            print(f"Error adding song: {e}")
            return None
        finally:
            cursor.close()

    def get_song_by_id(self, song_id: int) -> Optional[Song]:
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT Song_ID, User_ID, Song_Name, ArtistName, Genre, ReleaseYear, 
                       Album, Upload_Date, Duration, Bitrate, File_Path
                FROM Song
                WHERE Song_ID = %s
            """
            cursor.execute(query, (song_id,))
            row = cursor.fetchone()
            if row:
                return Song(
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
            return None
        except Error as e:
            print(f"Error retrieving song by ID: {e}")
            return None
        finally:
            cursor.close()

    def get_all_songs(self) -> List[Song]:
        songs = []
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT Song_ID, User_ID, Song_Name, ArtistName, Genre, ReleaseYear, 
                       Album, Upload_Date, Duration, Bitrate, File_Path
                FROM Song
            """
            cursor.execute(query)
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
            print(f"Error retrieving all songs: {e}")
            return []
        finally:
            cursor.close()

    def update_song(self, song_id: int, input_data: 'SongInput') -> Optional[Song]:
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE Song
                SET Song_Name = %s, ArtistName = %s, Genre = %s, ReleaseYear = %s, 
                    Album = %s, Duration = %s, Bitrate = %s, File_Path = %s
                WHERE Song_ID = %s
            """
            cursor.execute(query, (
                input_data.song_name, input_data.artist_name, input_data.genre, 
                input_data.release_year, input_data.album, input_data.duration, 
                input_data.bitrate, input_data.file_path, song_id
            ))
            self.connection.commit()
            if cursor.rowcount > 0:
                return self.get_song_by_id(song_id)
            return None
        except Error as e:
            print(f"Error updating song: {e}")
            return None
        finally:
            cursor.close()

    def delete_song(self, song_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            query = """
                DELETE FROM Song
                WHERE Song_ID = %s
            """
            cursor.execute(query, (song_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting song: {e}")
            return False
        finally:
            cursor.close()