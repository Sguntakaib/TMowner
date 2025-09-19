"""
Analytics Router - Advanced Learning Analytics and Progress Visualization
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from database.connection import get_database
from models.user import UserResponse
from routers.auth import get_current_user
from services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/dashboard")
async def get_analytics_dashboard(
    days: int = Query(90, ge=1, le=365, description="Number of days to analyze"),
    current_user: UserResponse = Depends(get_current_user)
):
    """Get comprehensive analytics dashboard data"""
    db = await get_database()
    analytics_service = AnalyticsService(db)
    
    try:
        analytics_data = await analytics_service.get_user_comprehensive_analytics(
            current_user.id, days
        )
        return {
            "user_id": current_user.id,
            "analysis_period_days": days,
            "analytics": analytics_data,
            "generated_at": "datetime.utcnow().isoformat()"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate analytics dashboard"
        )


@router.get("/progress-visualization")
async def get_progress_visualization(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get data optimized for progress visualization components"""
    db = await get_database()
    analytics_service = AnalyticsService(db)
    
    try:
        visualization_data = await analytics_service.get_progress_visualization_data(current_user.id)
        return {
            "user_id": current_user.id,
            "visualization_data": visualization_data,
            "last_updated": "datetime.utcnow().isoformat()"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate progress visualization data"
        )


@router.get("/skill-assessment")
async def get_skill_assessment(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get detailed skill assessment and improvement recommendations"""
    db = await get_database()
    analytics_service = AnalyticsService(db)
    
    try:
        assessment_data = await analytics_service.get_skill_assessment_data(current_user.id)
        return {
            "user_id": current_user.id,
            "skill_assessment": assessment_data,
            "assessment_date": "datetime.utcnow().isoformat()"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate skill assessment"
        )


@router.get("/engagement-metrics")
async def get_engagement_analytics(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get user engagement and activity analytics"""
    db = await get_database()
    analytics_service = AnalyticsService(db)
    
    try:
        engagement_data = await analytics_service.get_engagement_analytics(current_user.id)
        return {
            "user_id": current_user.id,
            "engagement_analytics": engagement_data,
            "analyzed_at": "datetime.utcnow().isoformat()"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate engagement analytics"
        )


@router.get("/performance-timeline")
async def get_performance_timeline(
    limit: int = Query(50, ge=1, le=200, description="Maximum number of data points"),
    current_user: UserResponse = Depends(get_current_user)
):
    """Get performance timeline data for charts"""
    db = await get_database()
    analytics_service = AnalyticsService(db)
    
    try:
        # Get recent scores for timeline
        scores = await db.scores.find({
            "user_id": current_user.id
        }).sort("submission_time", 1).limit(limit).to_list(length=limit)
        
        timeline_data = []
        for i, score in enumerate(scores):
            timeline_data.append({
                "date": score["submission_time"].isoformat(),
                "total_score": score["scores"]["total_score"],
                "security_score": score["scores"]["security_score"],
                "architecture_score": score["scores"]["architecture_score"],
                "performance_score": score["scores"]["performance_score"],
                "completeness_score": score["scores"]["completeness_score"],
                "attempt_number": i + 1,
                "time_spent_minutes": round(score["time_spent"] / 60, 1)
            })
        
        return {
            "user_id": current_user.id,
            "timeline": timeline_data,
            "total_attempts": len(timeline_data)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate performance timeline"
        )


@router.get("/skill-radar-data")
async def get_skill_radar_data(
    period: str = Query("recent", regex="^(recent|all|last_month)$", description="Analysis period"),
    current_user: UserResponse = Depends(get_current_user)
):
    """Get skill radar chart data for visualization"""
    db = await get_database()
    
    try:
        query = {"user_id": current_user.id}
        
        if period == "recent":
            # Last 10 attempts
            scores = await db.scores.find(query).sort("submission_time", -1).limit(10).to_list(length=10)
        elif period == "last_month":
            # Last 30 days
            from datetime import datetime, timedelta
            cutoff = datetime.utcnow() - timedelta(days=30)
            query["submission_time"] = {"$gte": cutoff}
            scores = await db.scores.find(query).to_list(length=None)
        else:
            # All scores
            scores = await db.scores.find(query).to_list(length=None)
        
        if not scores:
            return {
                "radar_data": {
                    "Security": 0,
                    "Architecture": 0,
                    "Performance": 0,
                    "Completeness": 0,
                    "Overall": 0
                },
                "data_points": 0
            }
        
        # Calculate averages
        import statistics
        radar_data = {
            "Security": round(statistics.mean([s["scores"]["security_score"] for s in scores]), 1),
            "Architecture": round(statistics.mean([s["scores"]["architecture_score"] for s in scores]), 1),
            "Performance": round(statistics.mean([s["scores"]["performance_score"] for s in scores]), 1),
            "Completeness": round(statistics.mean([s["scores"]["completeness_score"] for s in scores]), 1),
            "Overall": round(statistics.mean([s["scores"]["total_score"] for s in scores]), 1)
        }
        
        return {
            "radar_data": radar_data,
            "data_points": len(scores),
            "period": period
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate skill radar data"
        )


@router.get("/learning-insights")
async def get_learning_insights(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get personalized learning insights and recommendations"""
    db = await get_database()
    analytics_service = AnalyticsService(db)
    
    try:
        # Get user's recent performance
        recent_scores = await db.scores.find({
            "user_id": current_user.id
        }).sort("submission_time", -1).limit(20).to_list(length=20)
        
        if not recent_scores:
            return {
                "insights": [],
                "recommendations": ["Start with your first threat modeling scenario!"],
                "focus_areas": [],
                "next_steps": ["Browse available scenarios", "Try a beginner-level challenge"]
            }
        
        import statistics
        
        # Calculate insights
        insights = []
        recommendations = []
        focus_areas = []
        
        # Performance trend
        if len(recent_scores) >= 5:
            early_avg = statistics.mean([s["scores"]["total_score"] for s in recent_scores[-5:]])
            recent_avg = statistics.mean([s["scores"]["total_score"] for s in recent_scores[:5]])
            
            if recent_avg > early_avg + 5:
                insights.append("📈 Your performance is improving consistently!")
            elif recent_avg < early_avg - 5:
                insights.append("📉 Consider reviewing fundamentals to get back on track")
            else:
                insights.append("📊 Your performance is stable")
        
        # Skill analysis
        skill_averages = {
            "Security": statistics.mean([s["scores"]["security_score"] for s in recent_scores]),
            "Architecture": statistics.mean([s["scores"]["architecture_score"] for s in recent_scores]),
            "Performance": statistics.mean([s["scores"]["performance_score"] for s in recent_scores]),
            "Completeness": statistics.mean([s["scores"]["completeness_score"] for s in recent_scores])
        }
        
        # Find strongest and weakest areas
        strongest = max(skill_averages.items(), key=lambda x: x[1])
        weakest = min(skill_averages.items(), key=lambda x: x[1])
        
        insights.append(f"💪 Your strongest area is {strongest[0]} ({strongest[1]:.1f}%)")
        
        if weakest[1] < 70:
            insights.append(f"🎯 Focus on improving {weakest[0]} ({weakest[1]:.1f}%)")
            focus_areas.append(weakest[0])
            recommendations.append(f"Practice scenarios that emphasize {weakest[0].lower()} skills")
        
        # Time efficiency
        avg_time = statistics.mean([s["time_spent"] for s in recent_scores]) / 60
        if avg_time < 20:
            insights.append("⚡ You're completing scenarios efficiently!")
        elif avg_time > 45:
            recommendations.append("Take your time to thoroughly analyze each scenario")
        
        # Consistency check
        score_variance = statistics.stdev([s["scores"]["total_score"] for s in recent_scores])
        if score_variance < 10:
            insights.append("🎯 Your performance is very consistent!")
        elif score_variance > 20:
            recommendations.append("Work on consistency - review your approach for each scenario")
        
        return {
            "insights": insights,
            "recommendations": recommendations,
            "focus_areas": focus_areas,
            "next_steps": [
                "Try scenarios in your focus areas",
                "Review feedback from previous attempts",
                "Challenge yourself with harder scenarios"
            ],
            "performance_summary": {
                "total_attempts": len(recent_scores),
                "average_score": round(statistics.mean([s["scores"]["total_score"] for s in recent_scores]), 1),
                "skill_breakdown": {k: round(v, 1) for k, v in skill_averages.items()}
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate learning insights"
        )