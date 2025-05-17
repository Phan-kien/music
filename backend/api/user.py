import logging
from fastapi import APIRouter, HTTPException, Depends
from dao.daomanager import DAOManager
from dao.User.User_object import User
from dao.User.User_interface import RegisterInput, LoginInput
from typing import Optional
import bcrypt
import jwt
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

SECRET_KEY = "your-secret-key"  # Thay đổi thành một key bảo mật
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=User)
async def register_user(input_data: RegisterInput, dao_manager: DAOManager = Depends(DAOManager)):
    logger.info(f"Received register request: {input_data}")
    user_dao = dao_manager.get_user_dao()
    existing_user = user_dao.get_user_by_username(input_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Hash password
    hashed_password = bcrypt.hashpw(input_data.password.encode(), bcrypt.gensalt())
    input_data.password = hashed_password.decode()
    
    user = user_dao.create_user(input_data)
    if not user:
        logger.error("Failed to create user")
        raise HTTPException(status_code=500, detail="Failed to create user")
    logger.info(f"Created user: {user}")
    return User(
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        registration_date=user.registration_date
    )

@router.post("/login")
async def login_user(input_data: LoginInput, dao_manager: DAOManager = Depends(DAOManager)):
    user_dao = dao_manager.get_user_dao()
    user = user_dao.get_user_by_username(input_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not bcrypt.checkpw(input_data.password.encode(), user.password.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.user_id}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.user_id,
            "username": user.username,
            "email": user.email
        }
    }

@router.get("/{username}", response_model=User)
async def get_user(username: str, dao_manager: DAOManager = Depends(DAOManager)):
    user_dao = dao_manager.get_user_dao()
    user = user_dao.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
