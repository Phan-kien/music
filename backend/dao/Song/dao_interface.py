from abc import ABC, abstractmethod
from .Song_object import Song
from .Song_interface import SongInput, SongOutput

class SongDAOInterface(ABC):

    @abstractmethod
    def add_song(self, input_data: SongInput) -> Song:
        pass

    @abstractmethod
    def get_song_by_id(self, song_id: int) -> Song:
        pass

    @abstractmethod
    def get_all_songs(self) -> list[Song]:
        pass

    @abstractmethod
    def update_song(self, song_id: int, input_data: SongInput) -> Song:
        pass

    @abstractmethod
    def delete_song(self, song_id: int) -> bool:
        pass
