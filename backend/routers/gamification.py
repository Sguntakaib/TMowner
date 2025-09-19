"""
Gamification Router - Badges, Achievements, and Progress Tracking
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from typing import List, Optional
from database.connection import get_database
from models.user import UserResponse
from routers.auth import get_current_user
from services.gamification_service import GamificationService

router = APIRouter()


@router.get("/achievements")
async def get_user_achievements(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get user's achievements, badges, and progress"""
    db = await get_database()
    gamification_service = GamificationService(db)
    
    try:
        # Initialize badges system if needed
        await gamification_service.initialize_badges_system()
        
        achievements_data = await gamification_service.get_user_achievements(current_user.id)
        
        return {
            "user_id": current_user.id,
            "achievements": achievements_data,
            "last_updated": "datetime.utcnow().isoformat()"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve achievements"
        )


@router.post("/check-achievements")
async def check_new_achievements(
    background_tasks: BackgroundTasks,
    current_user: UserResponse = Depends(get_current_user)
):
    """Check for new achievements and award them"""
    db = await get_database()
    gamification_service = GamificationService(db)
    
    try:
        new_achievements = await gamification_service.check_and_award_achievements(current_user.id)
        
        return {
            "user_id": current_user.id,
            "new_achievements": new_achievements,
            "total_new": len(new_achievements),
            "checked_at": "datetime.utcnow().isoformat()"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check achievements"
        )


@router.get("/leaderboard")
async def get_achievements_leaderboard(
    category: Optional[str] = Query(None, description="Filter by scenario category"),
    timeframe: str = Query("all", regex="^(all|week|month|year)$", description="Timeframe for ranking"),
    limit: int = Query(20, ge=1, le=100, description="Number of users to return"),
    current_user: UserResponse = Depends(get_current_user)
):
    """Get leaderboard with achievement information"""
    db = await get_database()
    gamification_service = GamificationService(db)
    
    try:
        leaderboard_data = await gamification_service.get_leaderboard_with_achievements(
            category, timeframe, limit
        )
        
        return {
            "leaderboard": leaderboard_data,
            "filters": {
                "category": category,
                "timeframe": timeframe,
                "limit": limit
            },
            "generated_at": "datetime.utcnow().isoformat()"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate leaderboard"
        )


@router.get("/badge-progress")
async def get_badge_progress(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get detailed progress towards unearned badges"""
    db = await get_database()
    gamification_service = GamificationService(db)
    
    try:
        achievements_data = await gamification_service.get_user_achievements(current_user.id)
        
        # Filter to show only unearned badges with progress
        unearned_badges = [
            badge for badge in achievements_data["badges"] 
            if not badge["earned"] and badge.get("progress")
        ]
        
        # Sort by progress percentage (closest to completion first)
        unearned_badges.sort(key=lambda x: x["progress"].get("percentage", 0), reverse=True)
        
        return {
            "user_id": current_user.id,
            "unearned_badges": unearned_badges[:10],  # Top 10 closest to earning
            "total_unearned": len(unearned_badges),
            "next_milestone": achievements_data.get("next_milestone"),
            "current_level": achievements_data.get("user_level")
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get badge progress"
        )


@router.get("/achievement-stats")
async def get_achievement_statistics(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get global achievement statistics and badge rarity"""
    db = await get_database()
    gamification_service = GamificationService(db)
    
    try:
        stats_data = await gamification_service.get_achievement_statistics()
        
        return {
            "global_statistics": stats_data,
            "generated_at": "datetime.utcnow().isoformat()"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get achievement statistics"
        )


@router.get("/user-level")
async def get_user_level_info(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get detailed user level and experience information"""
    db = await get_database()
    
    try:
        # Get user scores for experience calculation
        user_scores = await db.scores.find({"user_id": current_user.id}).to_list(length=None)
        
        total_experience = sum(score["scores"]["total_score"] for score in user_scores)
        
        # Calculate level (using square root progression)
        import math
        level = math.floor(math.sqrt(total_experience / 100)) + 1
        
        # Experience for current and next level
        current_level_threshold = ((level - 1) ** 2) * 100
        next_level_threshold = (level ** 2) * 100
        
        experience_in_level = total_experience - current_level_threshold
        experience_needed = next_level_threshold - current_level_threshold
        
        # Level titles
        level_titles = {
            1: "Novice",
            2: "Apprentice", 
            3: "Practitioner",
            5: "Specialist",
            8: "Expert",
            12: "Master",
            18: "Grandmaster",
            25: "Legend"
        }
        
        # Find appropriate title
        title = "Novice"
        for threshold, level_title in sorted(level_titles.items(), reverse=True):
            if level >= threshold:
                title = level_title
                break
        
        return {
            "user_id": current_user.id,
            "level": level,
            "title": title,
            "total_experience": total_experience,
            "experience_in_level": experience_in_level,
            "experience_needed_for_next": experience_needed - experience_in_level,
            "progress_percentage": round((experience_in_level / experience_needed) * 100, 1),
            "total_scenarios_completed": len(user_scores),
            "level_progression": {
                "current_threshold": current_level_threshold,
                "next_threshold": next_level_threshold,
                "next_title": level_titles.get(level + 1, "Ultimate Master")
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user level information"
        )


@router.get("/recent-achievements")
async def get_recent_achievements(
    limit: int = Query(10, ge=1, le=50, description="Number of recent achievements to return"),
    global_view: bool = Query(False, description="Show global recent achievements instead of user's"),
    current_user: UserResponse = Depends(get_current_user)
):
    """Get recent achievements (user's or global)"""
    db = await get_database()
    
    try:
        if global_view:
            # Get recent achievements from all users
            recent_achievements = await db.user_achievements.find({}).sort("earned_at", -1).limit(limit).to_list(length=limit)
            
            # Enhance with user information
            enhanced_achievements = []
            for achievement in recent_achievements:
                user = await db.users.find_one({"_id": ObjectId(achievement["user_id"])})
                user_name = "Anonymous"
                if user:
                    profile = user.get("profile", {})
                    user_name = f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip()
                    if not user_name:
                        user_name = user.get("email", "Anonymous").split("@")[0]
                
                enhanced_achievements.append({
                    **achievement,
                    "user_name": user_name,
                    "time_ago": "datetime.utcnow() - achievement['earned_at']"  # This would be calculated properly
                })
            
            return {
                "recent_achievements": enhanced_achievements,
                "is_global": True,
                "total_shown": len(enhanced_achievements)
            }
        else:
            # Get user's recent achievements
            user_achievements = await db.user_achievements.find({
                "user_id": current_user.id
            }).sort("earned_at", -1).limit(limit).to_list(length=limit)
            
            return {
                "user_id": current_user.id,
                "recent_achievements": user_achievements,
                "is_global": False,
                "total_shown": len(user_achievements)
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get recent achievements"
        )


@router.get("/motivation-dashboard")
async def get_motivation_dashboard(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get motivational dashboard with streaks, goals, and encouragement"""
    db = await get_database()
    
    try:
        # Get user activity for streak calculation
        from datetime import datetime, timedelta
        recent_scores = await db.scores.find({
            "user_id": current_user.id,
            "submission_time": {"$gte": datetime.utcnow() - timedelta(days=30)}
        }).sort("submission_time", -1).to_list(length=None)
        
        # Calculate current streak
        activity_dates = set()
        for score in recent_scores:
            date_key = score["submission_time"].strftime("%Y-%m-%d")
            activity_dates.add(date_key)
        
        current_streak = 0
        current_date = datetime.utcnow().date()
        
        while current_date.strftime("%Y-%m-%d") in activity_dates:
            current_streak += 1
            current_date -= timedelta(days=1)
        
        # Get achievements for motivation
        user_achievements = await db.user_achievements.find({
            "user_id": current_user.id
        }).to_list(length=None)
        
        # Calculate weekly goal progress
        week_start = datetime.utcnow() - timedelta(days=7)
        this_week_scores = [s for s in recent_scores if s["submission_time"] >= week_start]
        
        # Motivational messages based on activity
        motivation_messages = []
        if current_streak >= 7:
            motivation_messages.append("🔥 Amazing! You're on a hot streak!")
        elif current_streak >= 3:
            motivation_messages.append("🚀 Great momentum! Keep it going!")
        elif len(this_week_scores) >= 3:
            motivation_messages.append("💪 Strong week! You're making great progress!")
        else:
            motivation_messages.append("🎯 Ready to tackle some new challenges?")
        
        if len(user_achievements) >= 5:
            motivation_messages.append("🏆 Badge collector! You're doing fantastic!")
        
        return {
            "user_id": current_user.id,
            "current_streak": current_streak,
            "this_week_attempts": len(this_week_scores),
            "weekly_goal": 5,  # Default weekly goal
            "weekly_progress": min(100, (len(this_week_scores) / 5) * 100),
            "total_badges": len(user_achievements),
            "motivation_messages": motivation_messages,
            "suggested_actions": [
                "Try a new scenario category",
                "Improve your weakest skill area", 
                "Challenge yourself with a harder difficulty",
                "Review your previous feedback"
            ],
            "streak_milestone": {
                "next_milestone": 7 if current_streak < 7 else 14 if current_streak < 14 else 30,
                "days_to_go": max(0, (7 if current_streak < 7 else 14 if current_streak < 14 else 30) - current_streak)
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate motivation dashboard"
        )


from bson import ObjectId  # Add this import at the top