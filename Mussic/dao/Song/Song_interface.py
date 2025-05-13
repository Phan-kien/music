from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SongInput(BaseModel):
    user_id: int
    song_name: Optional[str] = None
    artist_name: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None
    album: Optional[str] = None
    duration: Optional[str] = None  # TIME in MySQL, stored as string (e.g., "00:03:30")
    bitrate: Optional[int] = None
    file_path: str

class Song(BaseModel):
    song_id: int
    user_id: int
    song_name: Optional[str] = None
    artist_name: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None
    album: Optional[str] = None
    upload_date: Optional[datetime] = None
    duration: Optional[str] = None
    bitrate: Optional[int] = None
    file_path: str
    