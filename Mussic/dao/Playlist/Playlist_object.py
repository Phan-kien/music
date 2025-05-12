from dataclasses import dataclass
from datetime import datetime, date, time
from typing import Optional

# Playlist
@dataclass
class Playlist:
    id: int
    user_id: int
    name: str
    artist_name: Optional[str]
    release_date: Optional[date]

