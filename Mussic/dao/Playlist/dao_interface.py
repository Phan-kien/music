from abc import ABC, abstractmethod
from .Playlist_object import Playlist
from .Playlist_interface import PlaylistInput, PlaylistOutput

class PlaylistDAOInterface(ABC):

    @abstractmethod
    def create_playlist(self, input_data: PlaylistInput) -> Playlist:
        pass

    @abstractmethod
    def get_playlist_by_id(self, playlist_id: int) -> Playlist:
        pass

    @abstractmethod
    def get_all_playlists(self, user_id: int) -> list[Playlist]:
        pass

    @abstractmethod
    def update_playlist(self, playlist_id: int, input_data: PlaylistInput) -> Playlist:
        pass

    @abstractmethod
    def delete_playlist(self, playlist_id: int) -> bool:
        pass
