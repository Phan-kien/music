from dataclasses import dataclass

@dataclass
class LikeInput:
    user_id: int
    song_id: int
