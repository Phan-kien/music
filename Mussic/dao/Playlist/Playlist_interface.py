from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class PlaylistInput:
    user_id: int
    playlist_name: str
    artist_name: Optional[str]
    release_date: Optional[date]

@dataclass
class PlaylistOutput:
    id: int
    playlist_name: str
    artist_name: Optional[str]
    release_date: Optional[date]
