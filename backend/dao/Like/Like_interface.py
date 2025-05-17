from pydantic import BaseModel
from typing import List
from dao.Song.Song_interface import Song

class LikeInput(BaseModel):
    user_id: int
    song_id: int

class Like(LikeInput):
    liked_at: str  # DATETIME stored as string

class LikedSongsResponse(BaseModel):
    user_id: int
    songs: List[Song]