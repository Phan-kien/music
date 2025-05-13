from fastapi import APIRouter, HTTPException, Depends
from dao.daomanager import DAOManager
from dao.Playlist.Playlist_object import Playlist
from dao.Playlist.Playlist_interface import PlaylistInput
from typing import List

router = APIRouter()

@router.post("/", response_model=Playlist)
async def create_playlist(input_data: PlaylistInput, dao_manager: DAOManager = Depends(DAOManager)):
    playlist_dao = dao_manager.get_playlist_dao()
    playlist = playlist_dao.create_playlist(input_data)
    if not playlist:
        raise HTTPException(status_code=500, detail="Failed to create playlist")
    return playlist

@router.get("/{playlist_id}", response_model=Playlist)
async def get_playlist(playlist_id: int, dao_manager: DAOManager = Depends(DAOManager)):
    playlist_dao = dao_manager.get_playlist_dao()
    playlist = playlist_dao.get_playlist_by_id(playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist

@router.get("/user/{user_id}", response_model=List[Playlist])
async def get_all_playlists(user_id: int, dao_manager: DAOManager = Depends(DAOManager)):
    playlist_dao = dao_manager.get_playlist_dao()
    playlists = playlist_dao.get_all_playlists(user_id)
    return playlists

@router.put("/{playlist_id}", response_model=Playlist)
async def update_playlist(playlist_id: int, input_data: PlaylistInput, dao_manager: DAOManager = Depends(DAOManager)):
    playlist_dao = dao_manager.get_playlist_dao()
    playlist = playlist_dao.update_playlist(playlist_id, input_data)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found or update failed")
    return playlist

@router.delete("/{playlist_id}")
async def delete_playlist(playlist_id: int, dao_manager: DAOManager = Depends(DAOManager)):
    playlist_dao = dao_manager.get_playlist_dao()
    if not playlist_dao.delete_playlist(playlist_id):
        raise HTTPException(status_code=404, detail="Playlist not found or deletion failed")
    return {"message": "Playlist deleted"}