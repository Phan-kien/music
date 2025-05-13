from pydantic import BaseModel
from datetime import date
from typing import Optional

class PlaylistInput(BaseModel):
    user_id: int
    playlist_name: str
    artist_name: Optional[str] = None
    release_date: Optional[date] = None

class Playlist(BaseModel):
    playlist_id: int
    user_id: int
    playlist_name: str
    artist_name: Optional[str] = None
    release_date: Optional[date] = None