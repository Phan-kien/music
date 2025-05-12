from dataclasses import dataclass
from datetime import datetime, date, time
from typing import Optional

# LikedSongs
@dataclass
class LikedSong:
    user_id: int
    song_id: int
    liked_at: datetime
