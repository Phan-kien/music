from mysql.connector import MySQLConnection, connect, Error
from dao.User.User_dao import UserDAO
from dao.Song.song_dao import SongDAO
from dao.Playlist.playlist_dao import PlaylistDAO
from dao.Belong_to.Belong_to_dao import BelongToDAO
from dao.Like.Like_dao import LikeDAO

class DAOManager:
    def __init__(self, db_config: dict):
        self.connection = None
        self.db_config = db_config
        self.user_dao = None
        self.song_dao = None
        self.playlist_dao = None
        self.belong_to_dao = None
        self.like_dao = None

    def connect(self) -> bool:
        try:
            self.connection = connect(**self.db_config)
            if self.connection.is_connected():
                self.user_dao = UserDAO(self.connection)
                self.song_dao = SongDAO(self.connection)
                self.playlist_dao = PlaylistDAO(self.connection)
                self.belong_to_dao = BelongToDAO(self.connection)
                self.like_dao = LikeDAO(self.connection)
                return True
        except Error as e:
            print(f"Error connecting to database: {e}")
            return False

    def disconnect(self) -> bool:
        try:
            if self.connection and self.connection.is_connected():
                self.connection.close()
                self.user_dao = None
                self.song_dao = None
                self.playlist_dao = None
                self.belong_to_dao = None
                self.like_dao = None
                return True
        except Error as e:
            print(f"Error disconnecting from database: {e}")
            return False
        return True

    def get_user_dao(self) -> UserDAO:
        return self.user_dao

    def get_song_dao(self) -> SongDAO:
        return self.song_dao

    def get_playlist_dao(self) -> PlaylistDAO:
        return self.playlist_dao

    def get_belong_to_dao(self) -> BelongToDAO:
        return self.belong_to_dao

    def get_like_dao(self) -> LikeDAO:
        return self.like_dao
