from motor.motor_asyncio import AsyncIOMotorDatabase
from models.user import UserCreate, UserInDB, UserLogin, UserResponse
from utils.security import get_password_hash, verify_password, create_access_token
from typing import Optional
from datetime import datetime
import uuid


class AuthService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.users

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user"""
        # Check if user already exists
        existing_user = await self.collection.find_one({"email": user_data.email})
        if existing_user:
            raise ValueError("User with this email already exists")

        # Create user document
        user_dict = user_data.dict()
        user_dict["password_hash"] = get_password_hash(user_dict.pop("password"))
        
        # Set profile data
        profile_data = {}
        if user_data.first_name:
            profile_data["first_name"] = user_data.first_name
        if user_data.last_name:
            profile_data["last_name"] = user_data.last_name
        
        user_in_db = UserInDB(**user_dict)
        if profile_data:
            user_in_db.profile = user_in_db.profile.copy(update=profile_data)

        # Insert user
        result = await self.collection.insert_one(user_in_db.dict(by_alias=True))
        
        # Return user response
        created_user = await self.collection.find_one({"_id": result.inserted_id})
        return UserResponse.from_dict(created_user)

    async def authenticate_user(self, login_data: UserLogin) -> Optional[UserResponse]:
        """Authenticate user and return user data if valid"""
        user = await self.collection.find_one({"email": login_data.email})
        if not user:
            return None
        
        if not verify_password(login_data.password, user["password_hash"]):
            return None
        
        # Update last login
        await self.collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        return UserResponse.from_dict(user)

    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Get user by ID"""
        try:
            # Try with string UUID first (new format)
            user = await self.collection.find_one({"_id": user_id})
            if user:
                return UserResponse.from_dict(user)
                
            # Fallback to ObjectId for backward compatibility
            from bson import ObjectId
            user = await self.collection.find_one({"_id": ObjectId(user_id)})
            if user:
                return UserResponse.from_dict(user)
        except Exception:
            pass
        return None

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get user by email"""
        user = await self.collection.find_one({"email": email})
        if user:
            return UserResponse.from_dict(user)
        return None

    async def update_user_profile(self, user_id: str, profile_data: dict) -> Optional[UserResponse]:
        """Update user profile"""
        try:
            # Update user profile
            update_data = {}
            for key, value in profile_data.items():
                if key in ["first_name", "last_name", "avatar_url", "bio"]:
                    update_data[f"profile.{key}"] = value
                elif key in ["theme", "notifications"]:
                    update_data[f"preferences.{key}"] = value
            
            if update_data:
                # Try with string UUID first
                result = await self.collection.update_one(
                    {"_id": user_id},
                    {"$set": update_data}
                )
                
                # If no document updated, try with ObjectId
                if result.modified_count == 0:
                    from bson import ObjectId
                    await self.collection.update_one(
                        {"_id": ObjectId(user_id)},
                        {"$set": update_data}
                    )
            
            # Return updated user
            return await self.get_user_by_id(user_id)
        except Exception:
            return None

    async def create_access_token_for_user(self, user: UserResponse) -> str:
        """Create access token for user"""
        token_data = {
            "sub": user.email,
            "user_id": user.id,
            "role": user.role
        }
        return create_access_token(token_data)