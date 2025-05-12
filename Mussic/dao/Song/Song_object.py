from dataclasses import dataclass
from datetime import datetime, date, time
from typing import Optional


# dao/song/song_object.py
class Song:
    def __init__(self, song_id, user_id, song_name, artist_name, genre, release_year, album, upload_date, duration, bitrate, file_path):
        self.song_id = song_id
        self.user_id = user_id
        self.song_name = song_name
        self.artist_name = artist_name
        self.genre = genre
        self.release_year = release_year
        self.album = album
        self.upload_date = upload_date
        self.duration = duration
        self.bitrate = bitrate
        self.file_path = file_path

    @classmethod
    def from_dict(cls, data):
        return cls(
            song_id=data.get('Song_ID'),
            user_id=data.get('User_ID'),
            song_name=data.get('Song_Name'),
            artist_name=data.get('ArtistName'),
            genre=data.get('Genre'),
            release_year=data.get('ReleaseYear'),
            album=data.get('Album'),
            upload_date=data.get('Upload_Date'),
            duration=data.get('Duration'),
            bitrate=data.get('Bitrate'),
            file_path=data.get('File_Path')
        )