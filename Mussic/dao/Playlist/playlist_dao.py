from abc import ABC
from typing import List, Optional
from mysql.connector import MySQLConnection, Error
from .Playlist_interface import PlaylistDAOInterface, PlaylistInput
from .Playlist_object import Playlist

class PlaylistDAO(PlaylistDAOInterface):
    def __init__(self, db_connection: MySQLConnection):
        self.connection = db_connection

    def create_playlist(self, input_data: 'PlaylistInput') -> Optional[Playlist]:
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO Playlist (User_ID, Playlist_Name, ArtistName, ReleaseDate)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (
                input_data.user_id,
                input_data.playlist_name,
                input_data.artist_name,
                input_data.release_date
            ))
            self.connection.commit()
            playlist_id = cursor.lastrowid
            return Playlist(
                playlist_id=playlist_id,
                user_id=input_data.user_id,
                playlist_name=input_data.playlist_name,
                artist_name=input_data.artist_name,
                release_date=input_data.release_date
            )
        except Error as e:
            print(f"Error creating playlist: {e}")
            return None
        finally:
            cursor.close()

    def get_playlist_by_id(self, playlist_id: int) -> Optional[Playlist]:
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT Playlist_ID, User_ID, Playlist_Name, ArtistName, ReleaseDate
                FROM Playlist
                WHERE Playlist_ID = %s
            """
            cursor.execute(query, (playlist_id,))
            row = cursor.fetchone()
            if row:
                return Playlist(
                    playlist_id=row[0],
                    user_id=row[1],
                    playlist_name=row[2],
                    artist_name=row[3],
                    release_date=row[4]
                )
            return None
        except Error as e:
            print(f"Error retrieving playlist by ID: {e}")
            return None
        finally:
            cursor.close()

    def get_all_playlists(self, user_id: int) -> List[Playlist]:
        playlists = []
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT Playlist_ID, User_ID, Playlist_Name, ArtistName, ReleaseDate
                FROM Playlist
                WHERE User_ID = %s
            """
            cursor.execute(query, (user_id,))
            for row in cursor.fetchall():
                playlist = Playlist(
                    playlist_id=row[0],
                    user_id=row[1],
                    playlist_name=row[2],
                    artist_name=row[3],
                    release_date=row[4]
                )
                playlists.append(playlist)
            return playlists
        except Error as e:
            print(f"Error retrieving all playlists: {e}")
            return []
        finally:
            cursor.close()

    def update_playlist(self, playlist_id: int, input_data: 'PlaylistInput') -> Optional[Playlist]:
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE Playlist
                SET Playlist_Name = %s, ArtistName = %s, ReleaseDate = %s
                WHERE Playlist_ID = %s
            """
            cursor.execute(query, (
                input_data.playlist_name,
                input_data.artist_name,
                input_data.release_date,
                playlist_id
            ))
            self.connection.commit()
            if cursor.rowcount > 0:
                return self.get_playlist_by_id(playlist_id)
            return None
        except Error as e:
            print(f"Error updating playlist: {e}")
            return None
        finally:
            cursor.close()

    def delete_playlist(self, playlist_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            query = """
                DELETE FROM Playlist
                WHERE Playlist_ID = %s
            """
            cursor.execute(query, (playlist_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting playlist: {e}")
            return False
        finally:
            cursor.close()