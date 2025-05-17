from dataclasses import dataclass
from pydantic import BaseModel

# Belong_to
@dataclass
class BelongTo:
    song_id: int
    playlist_id: int

class BelongToInput(BaseModel):
    song_id: int
    playlist_id: int

class BelongTo(BelongToInput):
    pass