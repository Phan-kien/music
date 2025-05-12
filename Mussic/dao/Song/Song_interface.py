from dataclasses import dataclass
from typing import Optional

@dataclass
class SongInput:
    user_id: int
    song_name: Optional[str]
    artist_name: Optional[str]
    genre: Optional[str]
    release_year: Optional[int]
    album: Optional[str]
    duration: Optional[str]
    bitrate: Optional[int]
    file_path: str

@dataclass
class SongOutput:
    id: int
    song_name: Optional[str]
    artist_name: Optional[str]
    genre: Optional[str]
    release_year: Optional[int]
    album: Optional[str]
    upload_date: Optional[str]
    duration: Optional[str]
    bitrate: Optional[int]
    file_path: str
