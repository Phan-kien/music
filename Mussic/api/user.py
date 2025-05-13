from fastapi import APIRouter, HTTPException, Depends
from dao.daomanager import DAOManager
from dao.User.User_object import User
from dao.User.User_interface import RegisterInput, LoginInput
from typing import Optional

router = APIRouter()

@router.post("/register", response_model=User)
async def register_user(input_data: RegisterInput, dao_manager: DAOManager = Depends(DAOManager)):
    user_dao = dao_manager.get_user_dao()
    if user_dao.get_user_by_username(input_data.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    user = user_dao.create_user(input_data)
    if not user:
        raise HTTPException(status_code=500, detail="Failed to create user")
    return user

@router.post("/login", response_model=User)
async def login_user(input_data: LoginInput, dao_manager: DAOManager = Depends(DAOManager)):
    user_dao = dao_manager.get_user_dao()
    user = user_dao.get_user_by_username(input_data.username)
    if not user or not verify_password(input_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@router.get("/{username}", response_model=User)
async def get_user(username: str, dao_manager: DAOManager = Depends(DAOManager)):
    user_dao = dao_manager.get_user_dao()
    user = user_dao.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user