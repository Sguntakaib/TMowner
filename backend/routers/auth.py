from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database.connection import get_database
from services.auth_service import AuthService
from models.user import UserCreate, UserLogin, UserResponse, Token
from utils.security import verify_token
from typing import Optional

router = APIRouter()
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserResponse:
    """Get current authenticated user"""
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email: str = payload.get("sub")
    user_id: str = payload.get("user_id")
    
    if email is None or user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    db = await get_database()
    auth_service = AuthService(db)
    user = await auth_service.get_user_by_id(user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


@router.post("/register", response_model=dict)
async def register(user_data: UserCreate):
    """Register a new user"""
    db = await get_database()
    auth_service = AuthService(db)
    
    try:
        user = await auth_service.create_user(user_data)
        token = await auth_service.create_access_token_for_user(user)
        
        return {
            "message": "User created successfully",
            "user": user,
            "access_token": token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/login", response_model=dict)
async def login(login_data: UserLogin):
    """User login"""
    db = await get_database()
    auth_service = AuthService(db)
    
    user = await auth_service.authenticate_user(login_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = await auth_service.create_access_token_for_user(user)
    
    return {
        "message": "Login successful",
        "user": user,
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: UserResponse = Depends(get_current_user)):
    """Get current user profile"""
    return current_user


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    profile_data: dict,
    current_user: UserResponse = Depends(get_current_user)
):
    """Update user profile"""
    db = await get_database()
    auth_service = AuthService(db)
    
    updated_user = await auth_service.update_user_profile(current_user.id, profile_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update profile"
        )
    
    return updated_user


@router.post("/logout")
async def logout():
    """User logout (client should remove token)"""
    return {"message": "Logout successful"}


@router.get("/verify")
async def verify_token_endpoint(current_user: UserResponse = Depends(get_current_user)):
    """Verify token validity"""
    return {
        "valid": True,
        "user": current_user
    }