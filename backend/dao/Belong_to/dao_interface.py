from abc import ABC, abstractmethod
from .Belongto_object import BelongTo
from .dao_interface import BelongToInput

class BelongToDAOInterface(ABC):

    @abstractmethod
    def add_song_to_playlist(self, input_data: BelongToInput) -> bool:
        pass

    @abstractmethod
    def remove_song_from_playlist(self, song_id: int, playlist_id: int) -> bool:
        pass

    @abstractmethod
    def get_songs_in_playlist(self, playlist_id: int) -> list[BelongTo]:
        pass
