from dataclasses import dataclass
from datetime import datetime, date, time
from typing import Optional

# Belong_to
@dataclass
class BelongTo:
    song_id: int
    playlist_id: int
