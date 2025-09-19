from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

__all__ = ['UserProfile', 'UserPreferences', 'UserProgress', 'UserCreate', 'UserLogin', 'UserResponse', 'UserInDB', 'Token', 'TokenData']


class UserProfile(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None


class UserPreferences(BaseModel):
    theme: str = "light"
    notifications: bool = True


class UserProgress(BaseModel):
    level: int = 1
    experience_points: int = 0
    completed_scenarios: List[str] = []
    badges: List[str] = []


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    email: EmailStr
    profile: UserProfile
    role: str
    created_at: datetime
    last_login: Optional[datetime] = None
    preferences: UserPreferences
    progress: UserProgress
        
    @classmethod
    def from_dict(cls, data):
        # Convert ObjectId to string
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)


class UserInDB(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    email: EmailStr
    password_hash: str
    profile: UserProfile = UserProfile()
    role: str = "student"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    preferences: UserPreferences = UserPreferences()
    progress: UserProgress = UserProgress()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[str] = None