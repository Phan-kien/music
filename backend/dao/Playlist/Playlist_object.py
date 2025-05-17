from dataclasses import dataclass
from datetime import date
from typing import Optional

# Playlist
@dataclass
class Playlist:
    playlist_id: int
    user_id: int
    playlist_name: str
    artist_name: Optional[str]
    release_date: Optional[date]
    