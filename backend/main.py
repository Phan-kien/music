from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from config.db import Database
from dao.daomanager import DAOManager
from api import user, song, playlist, belong_to, like


app = FastAPI(title="Music Management API")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Bao gồm OPTIONS
    allow_headers=["*"],
)

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
app.include_router(song.router, prefix="/songs", tags=["Songs"])
app.include_router(playlist.router, prefix="/playlists", tags=["Playlists"])
app.include_router(belong_to.router, prefix="/belong-to", tags=["Belong To"])
app.include_router(like.router, prefix="/likes", tags=["Likes"])

@app.get("/")
async def root():
    return {"message": "Welcome to Music Management API"}
