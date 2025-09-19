from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from database.connection import get_database
from models.user import UserResponse
from routers.auth import get_current_user
from services.learning_service import LearningService

router = APIRouter()


@router.get("/paths")
async def get_learning_paths(
    category: Optional[str] = Query(None),
    current_user: UserResponse = Depends(get_current_user)
):
    """Get available learning paths"""
    db = await get_database()
    learning_service = LearningService(db)
    
    paths = await learning_service.get_learning_paths(category)
    return {"learning_paths": paths}


@router.get("/paths/{path_id}")
async def get_learning_path(
    path_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get learning path details"""
    db = await get_database()
    learning_service = LearningService(db)
    
    path = await learning_service.get_learning_path_by_id(path_id)
    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )
    
    return path


@router.post("/paths/{path_id}/enroll")
async def enroll_in_path(
    path_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Enroll in a learning path"""
    db = await get_database()
    learning_service = LearningService(db)
    
    success = await learning_service.enroll_user_in_path(current_user.id, path_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to enroll in learning path"
        )
    
    return {"message": "Successfully enrolled in learning path"}


@router.get("/progress")
async def get_learning_progress(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get user's learning progress"""
    db = await get_database()
    learning_service = LearningService(db)
    
    progress = await learning_service.get_user_progress(current_user.id)
    return progress


@router.get("/recommendations")
async def get_recommendations(
    limit: int = Query(5, le=20),
    current_user: UserResponse = Depends(get_current_user)
):
    """Get personalized learning recommendations"""
    db = await get_database()
    learning_service = LearningService(db)
    
    recommendations = await learning_service.get_personalized_recommendations(
        current_user.id, limit
    )
    return {"recommendations": recommendations}


@router.get("/achievements")
async def get_achievements(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get user achievements and badges"""
    db = await get_database()
    learning_service = LearningService(db)
    
    achievements = await learning_service.get_user_achievements(current_user.id)
    return achievements


@router.post("/achievements/check")
async def check_achievements(
    current_user: UserResponse = Depends(get_current_user)
):
    """Check for new achievements"""
    db = await get_database()
    learning_service = LearningService(db)
    
    new_achievements = await learning_service.check_and_award_achievements(current_user.id)
    return {
        "new_achievements": new_achievements,
        "message": f"Awarded {len(new_achievements)} new achievements"
    }