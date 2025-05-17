from abc import ABC, abstractmethod
from .Like_object import Like
from .Like_interface import LikeInput

class LikeDAOInterface(ABC):

    @abstractmethod
    def like_song(self, input_data: LikeInput) -> bool:
        pass

    @abstractmethod
    def unlike_song(self, user_id: int, song_id: int) -> bool:
        pass

    @abstractmethod
    def get_liked_songs_by_user(self, user_id: int) -> list[Like]:
        pass
