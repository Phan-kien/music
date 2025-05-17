from fastapi import APIRouter, HTTPException, Depends
from dao.daomanager import DAOManager
from dao.Belong_to.Belongto_object import BelongToInput
from dao.Belong_to.Belongto_interface import SongsInPlaylistResponse

router = APIRouter()

@router.post("/", response_model=dict)
async def add_song_to_playlist(input_data: BelongToInput, dao_manager: DAOManager = Depends(DAOManager)):
    belong_to_dao = dao_manager.get_belong_to_dao()
    if not belong_to_dao.add_song_to_playlist(input_data):
        raise HTTPException(status_code=500, detail="Failed to add song to playlist")
    return {"message": "Song added to playlist"}

@router.delete("/{song_id}/{playlist_id}", response_model=dict)
async def remove_song_from_playlist(song_id: int, playlist_id: int, dao_manager: DAOManager = Depends(DAOManager)):
    belong_to_dao = dao_manager.get_belong_to_dao()
    if not belong_to_dao.remove_song_from_playlist(song_id, playlist_id):
        raise HTTPException(status_code=404, detail="Song or playlist not found or removal failed")
    return {"message": "Song removed from playlist"}

@router.get("/{playlist_id}", response_model=SongsInPlaylistResponse)
async def get_songs_in_playlist(playlist_id: int, dao_manager: DAOManager = Depends(DAOManager)):
    belong_to_dao = dao_manager.get_belong_to_dao()
    songs = belong_to_dao.get_songs_in_playlist(playlist_id)
    return SongsInPlaylistResponse(playlist_id=playlist_id, songs=songs)