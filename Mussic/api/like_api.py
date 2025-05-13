from fastapi import APIRouter, HTTPException, Depends
from dao.daomanager import DAOManager
from dao.Like.Like_object import Like
from dao.Like.Like_interface import LikeInput, LikedSongsResponse

router = APIRouter()

@router.post("/", response_model=dict)
async def like_song(input_data: LikeInput, dao_manager: DAOManager = Depends(DAOManager)):
    like_dao = dao_manager.get_like_dao()
    if not like_dao.like_song(input_data):
        raise HTTPException(status_code=500, detail="Failed to like song")
    return {"message": "Song liked"}

@router.delete("/{user_id}/{song_id}", response_model=dict)
async def unlike_song(user_id: int, song_id: int, dao_manager: DAOManager = Depends(DAOManager)):
    like_dao = dao_manager.get_like_dao()
    if not like_dao.unlike_song(user_id, song_id):
        raise HTTPException(status_code=404, detail="Like not found or unliking failed")
    return {"message": "Song unliked"}

@router.get("/{user_id}", response_model=LikedSongsResponse)
async def get_liked_songs(user_id: int, dao_manager: DAOManager = Depends(DAOManager)):
    like_dao = dao_manager.get_like_dao()
    songs = like_dao.get_liked_songs_by_user(user_id)
    return LikedSongsResponse(user_id=user_id, songs=songs)