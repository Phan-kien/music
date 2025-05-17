from fastapi import APIRouter, HTTPException, Depends
from dao.daomanager import DAOManager
from dao.Song.Song_object import Song
from dao.Song.Song_interface import SongInput
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Song])
async def get_all_songs(dao_manager: DAOManager = Depends(DAOManager)):
    try:
        song_dao = dao_manager.get_song_dao()
        songs = song_dao.get_all_songs()
        return songs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{song_id}", response_model=Song)
async def get_song(song_id: int, dao_manager: DAOManager = Depends(DAOManager)):
    song_dao = dao_manager.get_song_dao()
    song = song_dao.get_song_by_id(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@router.post("/", response_model=Song)
async def add_song(input_data: SongInput, dao_manager: DAOManager = Depends(DAOManager)):
    song_dao = dao_manager.get_song_dao()
    song = song_dao.add_song(input_data)
    if not song:
        raise HTTPException(status_code=500, detail="Failed to add song")
    return song

@router.put("/{song_id}", response_model=Song)
async def update_song(song_id: int, input_data: SongInput, dao_manager: DAOManager = Depends(DAOManager)):
    song_dao = dao_manager.get_song_dao()
    song = song_dao.update_song(song_id, input_data)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found or update failed")
    return song

@router.delete("/{song_id}")
async def delete_song(song_id: int, dao_manager: DAOManager = Depends(DAOManager)):
    song_dao = dao_manager.get_song_dao()
    if not song_dao.delete_song(song_id):
        raise HTTPException(status_code=404, detail="Song not found or deletion failed")
    return {"message": "Song deleted"}