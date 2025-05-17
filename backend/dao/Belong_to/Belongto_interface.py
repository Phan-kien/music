from pydantic import BaseModel
from typing import List
from dao.Song.Song_interface import Song

class BelongToInput(BaseModel):
    song_id: int
    playlist_id: int

class BelongTo(BelongToInput):
    pass

class SongsInPlaylistResponse(BaseModel):
    playlist_id: int
    songs: List[Song]