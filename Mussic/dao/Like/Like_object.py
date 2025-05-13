from dataclasses import dataclass
from datetime import datetime

# Like
@dataclass
class Like:
    user_id: int
    song_id: int
    liked_at: datetime
    