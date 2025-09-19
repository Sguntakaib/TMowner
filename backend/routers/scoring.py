from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from database.connection import get_database
from models.score import ScoreResponse, LeaderboardEntry, UserStats
from models.user import UserResponse
from routers.auth import get_current_user
from services.scoring_service import ScoringService

router = APIRouter()


@router.post("/validate")
async def validate_diagram(
    diagram_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Real-time diagram validation"""
    db = await get_database()
    scoring_service = ScoringService(db)
    
    try:
        validation_results = await scoring_service.validate_diagram(diagram_id, current_user.id)
        return {
            "diagram_id": diagram_id,
            "validation_results": validation_results,
            "timestamp": "datetime.utcnow().isoformat()"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Validation failed"
        )


@router.post("/score", response_model=ScoreResponse)
async def score_diagram(
    diagram_id: str,
    time_spent: int = Query(..., description="Time spent in seconds"),
    current_user: UserResponse = Depends(get_current_user)
):
    """Calculate final score for diagram"""
    db = await get_database()
    scoring_service = ScoringService(db)
    
    try:
        score = await scoring_service.score_diagram(diagram_id, current_user.id, time_spent)
        if not score:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unable to score diagram"
            )
        return score
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Scoring failed"
        )


@router.get("/history", response_model=List[ScoreResponse])
async def get_score_history(
    scenario_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=50),
    current_user: UserResponse = Depends(get_current_user)
):
    """Get user's scoring history"""
    db = await get_database()
    scoring_service = ScoringService(db)
    
    scores = await scoring_service.get_user_scores(
        current_user.id, scenario_id, skip, limit
    )
    return scores


@router.get("/feedback/{score_id}")
async def get_detailed_feedback(
    score_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get detailed feedback for a score"""
    db = await get_database()
    scoring_service = ScoringService(db)
    
    feedback = await scoring_service.get_detailed_feedback(score_id, current_user.id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    return feedback


@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    timeframe: str = Query("all", regex="^(all|week|month|year)$"),
    limit: int = Query(10, le=50),
    current_user: UserResponse = Depends(get_current_user)
):
    """Get leaderboard"""
    db = await get_database()
    scoring_service = ScoringService(db)
    
    leaderboard = await scoring_service.get_leaderboard(
        category, difficulty, timeframe, limit
    )
    return leaderboard


@router.get("/stats", response_model=UserStats)
async def get_user_stats(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get user statistics"""
    db = await get_database()
    scoring_service = ScoringService(db)
    
    stats = await scoring_service.get_user_stats(current_user.id)
    return stats


@router.get("/analytics")
async def get_user_analytics(
    days: int = Query(30, ge=1, le=365),
    current_user: UserResponse = Depends(get_current_user)
):
    """Get user performance analytics"""
    db = await get_database()
    scoring_service = ScoringService(db)
    
    analytics = await scoring_service.get_user_analytics(current_user.id, days)
    return analytics