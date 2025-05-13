from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# Song
@dataclass
class Song:
    song_id: int
    user_id: int
    song_name: Optional[str]
    artist_name: Optional[str]
    genre: Optional[str]
    release_year: Optional[int]
    album: Optional[str]
    upload_date: Optional[datetime]
    duration: Optional[str]
    bitrate: Optional[int]
    file_path: str
    