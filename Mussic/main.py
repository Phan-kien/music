
from fastapi import FastAPI, Depends
from config.db import Database
from dao.daomanager import DAOManager
from api import user, song_api, playlist_api, belong_to_api, like_api

app = FastAPI(title="Music Management API")

# Dependency để inject DAOManager
def get_dao_manager():
    db = Database()
    dao_manager = DAOManager(db)
    dao_manager.connect()
    try:
        yield dao_manager
    finally:
        dao_manager.disconnect()

# Đăng ký các router
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(song_api.router, prefix="/songs", tags=["Songs"])
app.include_router(playlist_api.router, prefix="/playlists", tags=["Playlists"])
app.include_router(belong_to_api.router, prefix="/belong-to", tags=["Belong To"])
app.include_router(like_api.router, prefix="/likes", tags=["Likes"])

@app.get("/")
async def root():
    return {"message": "Welcome to Music Management API"}