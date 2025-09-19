"""
Advanced Analytics Service for Learning Progress and Performance Visualization
"""
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from bson import ObjectId
import statistics
from collections import defaultdict, Counter


class AnalyticsService:
    """Advanced analytics service for comprehensive learning insights"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.scores_collection = db.scores
        self.users_collection = db.users
        self.scenarios_collection = db.scenarios
        self.diagrams_collection = db.diagrams
    
    async def get_user_comprehensive_analytics(self, user_id: str, days: int = 90) -> Dict[str, Any]:
        """Get comprehensive user analytics dashboard data"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get user scores
        user_scores = await self.scores_collection.find({
            "user_id": user_id,
            "submission_time": {"$gte": cutoff_date}
        }).sort("submission_time", 1).to_list(length=None)
        
        # Get all user scores for trends
        all_user_scores = await self.scores_collection.find({
            "user_id": user_id
        }).sort("submission_time", 1).to_list(length=None)
        
        return {
            "performance_overview": await self._get_performance_overview(user_scores, all_user_scores),
            "skill_radar": await self._get_skill_radar_data(user_scores),
            "learning_velocity": await self._get_learning_velocity(all_user_scores),
            "improvement_trends": await self._get_improvement_trends(all_user_scores),
            "category_performance": await self._get_category_performance(user_id, user_scores),
            "time_analytics": await self._get_time_analytics(user_scores),
            "consistency_metrics": await self._get_consistency_metrics(all_user_scores),
            "predictive_insights": await self._get_predictive_insights(user_id, all_user_scores),
            "comparison_metrics": await self._get_peer_comparison(user_id, user_scores),
            "goal_tracking": await self._get_goal_tracking(user_id, all_user_scores)
        }
    
    async def get_progress_visualization_data(self, user_id: str) -> Dict[str, Any]:
        """Get data optimized for progress visualization components"""
        all_scores = await self.scores_collection.find({
            "user_id": user_id
        }).sort("submission_time", 1).to_list(length=None)
        
        if not all_scores:
            return self._get_empty_progress_data()
        
        return {
            "score_timeline": await self._build_score_timeline(all_scores),
            "skill_progression": await self._build_skill_progression(all_scores),
            "milestone_achievements": await self._build_milestone_data(user_id, all_scores),
            "competency_matrix": await self._build_competency_matrix(all_scores),
            "learning_path_progress": await self._get_learning_path_visualization(user_id),
            "performance_heatmap": await self._build_performance_heatmap(all_scores),
            "efficiency_metrics": await self._build_efficiency_metrics(all_scores)
        }
    
    async def get_skill_assessment_data(self, user_id: str) -> Dict[str, Any]:
        """Get detailed skill assessment and recommendations"""
        user_scores = await self.scores_collection.find({
            "user_id": user_id
        }).to_list(length=None)
        
        if not user_scores:
            return {"message": "No assessment data available"}
        
        return {
            "current_skill_levels": await self._assess_current_skills(user_scores),
            "skill_gaps": await self._identify_skill_gaps(user_scores),
            "improvement_recommendations": await self._generate_skill_recommendations(user_id, user_scores),
            "next_challenges": await self._recommend_next_challenges(user_id, user_scores),
            "mastery_tracking": await self._track_skill_mastery(user_scores),
            "benchmark_comparison": await self._compare_to_benchmarks(user_scores)
        }
    
    async def get_engagement_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get user engagement and activity analytics"""
        # Get user activity over time
        activity_data = await self._get_user_activity_patterns(user_id)
        
        return {
            "activity_patterns": activity_data,
            "engagement_score": await self._calculate_engagement_score(user_id, activity_data),
            "session_analytics": await self._get_session_analytics(user_id),
            "retention_metrics": await self._get_retention_metrics(user_id),
            "motivation_indicators": await self._get_motivation_indicators(user_id)
        }
    
    # Private helper methods for performance overview
    async def _get_performance_overview(self, recent_scores: List[Dict], all_scores: List[Dict]) -> Dict[str, Any]:
        """Generate performance overview metrics"""
        if not recent_scores:
            return {
                "current_level": "Beginner",
                "total_scenarios": 0,
                "average_score": 0,
                "best_score": 0,
                "improvement_rate": 0,
                "performance_trend": "stable"
            }
        
        total_scenarios = len(all_scores)
        recent_avg = statistics.mean([s["scores"]["total_score"] for s in recent_scores])
        best_score = max([s["scores"]["total_score"] for s in all_scores])
        
        # Calculate improvement rate
        if len(all_scores) >= 5:
            early_scores = [s["scores"]["total_score"] for s in all_scores[:5]]
            recent_5_scores = [s["scores"]["total_score"] for s in all_scores[-5:]]
            improvement_rate = (statistics.mean(recent_5_scores) - statistics.mean(early_scores))
        else:
            improvement_rate = 0
        
        # Determine performance trend
        if len(recent_scores) >= 3:
            trend_scores = [s["scores"]["total_score"] for s in recent_scores[-3:]]
            if trend_scores[2] > trend_scores[0]:
                trend = "improving"
            elif trend_scores[2] < trend_scores[0]:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        # Determine current level
        if recent_avg >= 90:
            level = "Expert"
        elif recent_avg >= 75:
            level = "Advanced"
        elif recent_avg >= 60:
            level = "Intermediate"
        else:
            level = "Beginner"
        
        return {
            "current_level": level,
            "total_scenarios": total_scenarios,
            "average_score": round(recent_avg, 1),
            "best_score": round(best_score, 1),
            "improvement_rate": round(improvement_rate, 1),
            "performance_trend": trend
        }
    
    async def _get_skill_radar_data(self, scores: List[Dict]) -> Dict[str, Any]:
        """Generate skill radar chart data"""
        if not scores:
            return {
                "security": 0, "architecture": 0, "performance": 0, 
                "completeness": 0, "overall": 0
            }
        
        skill_averages = {
            "security": statistics.mean([s["scores"]["security_score"] for s in scores]),
            "architecture": statistics.mean([s["scores"]["architecture_score"] for s in scores]),
            "performance": statistics.mean([s["scores"]["performance_score"] for s in scores]),
            "completeness": statistics.mean([s["scores"]["completeness_score"] for s in scores]),
            "overall": statistics.mean([s["scores"]["total_score"] for s in scores])
        }
        
        return {k: round(v, 1) for k, v in skill_averages.items()}
    
    async def _get_learning_velocity(self, all_scores: List[Dict]) -> Dict[str, Any]:
        """Calculate learning velocity metrics"""
        if len(all_scores) < 2:
            return {"scenarios_per_week": 0, "velocity_trend": "stable", "projection": {}}
        
        # Group by week
        weekly_counts = defaultdict(int)
        for score in all_scores:
            week_key = score["submission_time"].strftime("%Y-W%U")
            weekly_counts[week_key] += 1
        
        if len(weekly_counts) < 2:
            return {"scenarios_per_week": len(all_scores), "velocity_trend": "stable", "projection": {}}
        
        weeks = sorted(weekly_counts.keys())
        recent_weeks = list(weekly_counts.values())[-4:]  # Last 4 weeks
        avg_velocity = statistics.mean(recent_weeks) if recent_weeks else 0
        
        # Calculate trend
        if len(recent_weeks) >= 2:
            if recent_weeks[-1] > recent_weeks[0]:
                trend = "accelerating"
            elif recent_weeks[-1] < recent_weeks[0]:
                trend = "decelerating"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        # Project next week
        projection = {
            "next_week_scenarios": max(1, round(avg_velocity)),
            "confidence": "high" if len(recent_weeks) >= 3 else "medium"
        }
        
        return {
            "scenarios_per_week": round(avg_velocity, 1),
            "velocity_trend": trend,
            "projection": projection,
            "weekly_data": dict(weekly_counts)
        }
    
    async def _get_improvement_trends(self, all_scores: List[Dict]) -> Dict[str, Any]:
        """Analyze improvement trends across different skill areas"""
        if len(all_scores) < 5:
            return {"insufficient_data": True}
        
        # Split scores into early and recent periods
        mid_point = len(all_scores) // 2
        early_scores = all_scores[:mid_point]
        recent_scores = all_scores[mid_point:]
        
        trends = {}
        skill_areas = ["security_score", "architecture_score", "performance_score", "completeness_score", "total_score"]
        
        for skill in skill_areas:
            early_avg = statistics.mean([s["scores"][skill] for s in early_scores])
            recent_avg = statistics.mean([s["scores"][skill] for s in recent_scores])
            
            improvement = recent_avg - early_avg
            improvement_rate = (improvement / early_avg) * 100 if early_avg > 0 else 0
            
            trends[skill.replace("_score", "")] = {
                "early_average": round(early_avg, 1),
                "recent_average": round(recent_avg, 1),
                "improvement": round(improvement, 1),
                "improvement_rate": round(improvement_rate, 1),
                "trend": "improving" if improvement > 2 else "declining" if improvement < -2 else "stable"
            }
        
        return trends
    
    async def _get_category_performance(self, user_id: str, scores: List[Dict]) -> Dict[str, Any]:
        """Analyze performance by scenario category"""
        category_data = defaultdict(list)
        
        for score in scores:
            if score.get("scenario_id"):
                scenario = await self.scenarios_collection.find_one({"_id": ObjectId(score["scenario_id"])})
                if scenario:
                    category = scenario.get("category", "uncategorized")
                    category_data[category].append(score["scores"]["total_score"])
        
        category_analysis = {}
        for category, scores_list in category_data.items():
            category_analysis[category] = {
                "average_score": round(statistics.mean(scores_list), 1),
                "best_score": round(max(scores_list), 1),
                "attempts": len(scores_list),
                "consistency": round(100 - (statistics.stdev(scores_list) if len(scores_list) > 1 else 0), 1)
            }
        
        return category_analysis
    
    async def _get_time_analytics(self, scores: List[Dict]) -> Dict[str, Any]:
        """Analyze time-based performance metrics"""
        if not scores:
            return {"average_time": 0, "efficiency_trend": "stable"}
        
        times = [s["time_spent"] for s in scores]
        scores_list = [s["scores"]["total_score"] for s in scores]
        
        return {
            "average_time_minutes": round(statistics.mean(times) / 60, 1),
            "fastest_completion": round(min(times) / 60, 1),
            "efficiency_score": await self._calculate_efficiency_score(times, scores_list),
            "time_trend": await self._analyze_time_trend(scores)
        }
    
    async def _get_consistency_metrics(self, all_scores: List[Dict]) -> Dict[str, Any]:
        """Calculate consistency and reliability metrics"""
        if len(all_scores) < 3:
            return {"consistency_score": 0, "reliability": "insufficient_data"}
        
        total_scores = [s["scores"]["total_score"] for s in all_scores]
        
        # Calculate consistency score (inverse of coefficient of variation)
        mean_score = statistics.mean(total_scores)
        std_dev = statistics.stdev(total_scores)
        consistency_score = max(0, 100 - ((std_dev / mean_score) * 100)) if mean_score > 0 else 0
        
        # Determine reliability level
        if consistency_score >= 80:
            reliability = "highly_consistent"
        elif consistency_score >= 60:
            reliability = "moderately_consistent"
        else:
            reliability = "inconsistent"
        
        return {
            "consistency_score": round(consistency_score, 1),
            "reliability": reliability,
            "score_variance": round(std_dev, 1),
            "performance_range": {
                "min": round(min(total_scores), 1),
                "max": round(max(total_scores), 1)
            }
        }
    
    async def _build_score_timeline(self, scores: List[Dict]) -> List[Dict[str, Any]]:
        """Build timeline data for score progression visualization"""
        timeline = []
        
        for i, score in enumerate(scores):
            timeline.append({
                "attempt": i + 1,
                "date": score["submission_time"].isoformat(),
                "total_score": score["scores"]["total_score"],
                "security_score": score["scores"]["security_score"],
                "architecture_score": score["scores"]["architecture_score"],
                "performance_score": score["scores"]["performance_score"],
                "completeness_score": score["scores"]["completeness_score"],
                "time_spent_minutes": round(score["time_spent"] / 60, 1),
                "scenario_id": score.get("scenario_id", ""),
                "moving_average": await self._calculate_moving_average(scores, i, window=5)
            })
        
        return timeline
    
    async def _build_skill_progression(self, scores: List[Dict]) -> Dict[str, List[float]]:
        """Build skill progression data for each competency area"""
        progression = {
            "security": [],
            "architecture": [],
            "performance": [],
            "completeness": []
        }
        
        window_size = 3  # Moving average window
        
        for i in range(len(scores)):
            start_idx = max(0, i - window_size + 1)
            window_scores = scores[start_idx:i+1]
            
            progression["security"].append(
                round(statistics.mean([s["scores"]["security_score"] for s in window_scores]), 1)
            )
            progression["architecture"].append(
                round(statistics.mean([s["scores"]["architecture_score"] for s in window_scores]), 1)
            )
            progression["performance"].append(
                round(statistics.mean([s["scores"]["performance_score"] for s in window_scores]), 1)
            )
            progression["completeness"].append(
                round(statistics.mean([s["scores"]["completeness_score"] for s in window_scores]), 1)
            )
        
        return progression
    
    async def _build_competency_matrix(self, scores: List[Dict]) -> Dict[str, Any]:
        """Build competency matrix showing mastery levels"""
        if not scores:
            return {}
        
        # Recent performance (last 10 scores or all if less)
        recent_scores = scores[-10:] if len(scores) > 10 else scores
        
        competencies = {
            "Security": {
                "current_level": await self._determine_competency_level(
                    [s["scores"]["security_score"] for s in recent_scores]
                ),
                "trend": await self._calculate_skill_trend(scores, "security_score"),
                "mastery_percentage": await self._calculate_mastery_percentage(
                    [s["scores"]["security_score"] for s in recent_scores]
                )
            },
            "Architecture": {
                "current_level": await self._determine_competency_level(
                    [s["scores"]["architecture_score"] for s in recent_scores]
                ),
                "trend": await self._calculate_skill_trend(scores, "architecture_score"),
                "mastery_percentage": await self._calculate_mastery_percentage(
                    [s["scores"]["architecture_score"] for s in recent_scores]
                )
            },
            "Performance": {
                "current_level": await self._determine_competency_level(
                    [s["scores"]["performance_score"] for s in recent_scores]
                ),
                "trend": await self._calculate_skill_trend(scores, "performance_score"),
                "mastery_percentage": await self._calculate_mastery_percentage(
                    [s["scores"]["performance_score"] for s in recent_scores]
                )
            },
            "Completeness": {
                "current_level": await self._determine_competency_level(
                    [s["scores"]["completeness_score"] for s in recent_scores]
                ),
                "trend": await self._calculate_skill_trend(scores, "completeness_score"),
                "mastery_percentage": await self._calculate_mastery_percentage(
                    [s["scores"]["completeness_score"] for s in recent_scores]
                )
            }
        }
        
        return competencies
    
    # Additional helper methods
    async def _calculate_moving_average(self, scores: List[Dict], current_index: int, window: int = 5) -> float:
        """Calculate moving average for smoothed trend lines"""
        start_idx = max(0, current_index - window + 1)
        window_scores = scores[start_idx:current_index + 1]
        return round(statistics.mean([s["scores"]["total_score"] for s in window_scores]), 1)
    
    async def _determine_competency_level(self, scores: List[float]) -> str:
        """Determine competency level based on score distribution"""
        if not scores:
            return "Novice"
        
        avg_score = statistics.mean(scores)
        if avg_score >= 90:
            return "Expert"
        elif avg_score >= 75:
            return "Proficient"
        elif avg_score >= 60:
            return "Competent"
        elif avg_score >= 45:
            return "Developing"
        else:
            return "Novice"
    
    async def _calculate_skill_trend(self, all_scores: List[Dict], skill_field: str) -> str:
        """Calculate trend for a specific skill over time"""
        if len(all_scores) < 3:
            return "stable"
        
        skill_scores = [s["scores"][skill_field] for s in all_scores]
        
        # Compare first third vs last third
        third = len(skill_scores) // 3
        if third == 0:
            return "stable"
        
        early_avg = statistics.mean(skill_scores[:third])
        recent_avg = statistics.mean(skill_scores[-third:])
        
        improvement = recent_avg - early_avg
        
        if improvement > 5:
            return "improving"
        elif improvement < -5:
            return "declining"
        else:
            return "stable"
    
    async def _calculate_mastery_percentage(self, scores: List[float]) -> float:
        """Calculate mastery percentage based on consistency and performance"""
        if not scores:
            return 0.0
        
        avg_score = statistics.mean(scores)
        consistency = 100 - (statistics.stdev(scores) if len(scores) > 1 else 0)
        
        # Mastery is combination of high performance and consistency
        mastery = (avg_score * 0.7) + (consistency * 0.3)
        return round(min(100, mastery), 1)
    
    async def _get_empty_progress_data(self) -> Dict[str, Any]:
        """Return empty progress data structure"""
        return {
            "score_timeline": [],
            "skill_progression": {"security": [], "architecture": [], "performance": [], "completeness": []},
            "milestone_achievements": [],
            "competency_matrix": {},
            "learning_path_progress": {},
            "performance_heatmap": {},
            "efficiency_metrics": {}
        }
    
    # Additional methods for predictive insights, peer comparison, etc.
    async def _get_predictive_insights(self, user_id: str, scores: List[Dict]) -> Dict[str, Any]:
        """Generate predictive insights about user's learning trajectory"""
        # This is a simplified version - real implementation would use ML models
        if len(scores) < 5:
            return {"message": "Need more data for predictions"}
        
        recent_trend = await self._calculate_overall_trend(scores[-10:])
        
        return {
            "projected_next_score": await self._project_next_score(scores),
            "time_to_mastery": await self._estimate_mastery_time(scores),
            "recommended_focus_areas": await self._recommend_focus_areas(scores),
            "success_probability": await self._calculate_success_probability(scores)
        }
    
    async def _get_peer_comparison(self, user_id: str, user_scores: List[Dict]) -> Dict[str, Any]:
        """Compare user performance with peers"""
        if not user_scores:
            return {"message": "No comparison data available"}
        
        user_avg = statistics.mean([s["scores"]["total_score"] for s in user_scores])
        
        # Get aggregate peer data (simplified)
        peer_stats = await self.scores_collection.aggregate([
            {"$group": {
                "_id": None,
                "avg_score": {"$avg": "$scores.total_score"},
                "percentiles": {"$push": "$scores.total_score"}
            }}
        ]).to_list(length=1)
        
        if not peer_stats:
            return {"message": "No peer data available"}
        
        peer_avg = peer_stats[0]["avg_score"]
        
        return {
            "user_average": round(user_avg, 1),
            "peer_average": round(peer_avg, 1),
            "percentile_rank": await self._calculate_percentile_rank(user_avg, peer_stats[0]["percentiles"]),
            "performance_vs_peers": "above_average" if user_avg > peer_avg else "below_average" if user_avg < peer_avg else "average"
        }
    
    async def _calculate_percentile_rank(self, user_score: float, all_scores: List[float]) -> int:
        """Calculate user's percentile rank"""
        if not all_scores:
            return 50
        
        below_user = len([s for s in all_scores if s < user_score])
        percentile = (below_user / len(all_scores)) * 100
        return round(percentile)
    
    # Placeholder methods for additional functionality
    async def _calculate_efficiency_score(self, times: List[int], scores: List[float]) -> float:
        """Calculate efficiency score based on time vs performance"""
        # Implementation would analyze time-to-score ratio
        return 75.0  # Placeholder
    
    async def _analyze_time_trend(self, scores: List[Dict]) -> str:
        """Analyze if user is getting faster over time"""
        if len(scores) < 3:
            return "stable"
        
        times = [s["time_spent"] for s in scores]
        early_avg = statistics.mean(times[:len(times)//2])
        recent_avg = statistics.mean(times[len(times)//2:])
        
        if recent_avg < early_avg * 0.9:
            return "improving"
        elif recent_avg > early_avg * 1.1:
            return "slowing"
        else:
            return "stable"
    
    async def _calculate_overall_trend(self, scores: List[Dict]) -> str:
        """Calculate overall performance trend"""
        if len(scores) < 3:
            return "stable"
        
        total_scores = [s["scores"]["total_score"] for s in scores]
        
        # Simple linear trend
        x = list(range(len(total_scores)))
        n = len(x)
        
        # Calculate slope using least squares
        sum_x = sum(x)
        sum_y = sum(total_scores)
        sum_xy = sum(xi * yi for xi, yi in zip(x, total_scores))
        sum_x_sq = sum(xi * xi for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x_sq - sum_x * sum_x)
        
        if slope > 1:
            return "improving"
        elif slope < -1:
            return "declining"
        else:
            return "stable"
    
    async def _project_next_score(self, scores: List[Dict]) -> float:
        """Project user's next likely score"""
        if len(scores) < 3:
            return statistics.mean([s["scores"]["total_score"] for s in scores])
        
        recent_scores = [s["scores"]["total_score"] for s in scores[-5:]]
        return round(statistics.mean(recent_scores), 1)
    
    async def _estimate_mastery_time(self, scores: List[Dict]) -> str:
        """Estimate time to reach mastery level"""
        # Simplified estimation
        current_avg = statistics.mean([s["scores"]["total_score"] for s in scores[-5:]])
        
        if current_avg >= 85:
            return "Already achieved"
        elif current_avg >= 70:
            return "2-4 weeks"
        elif current_avg >= 55:
            return "1-2 months"
        else:
            return "2-3 months"
    
    async def _recommend_focus_areas(self, scores: List[Dict]) -> List[str]:
        """Recommend areas for improvement"""
        skill_avgs = {
            "Security": statistics.mean([s["scores"]["security_score"] for s in scores[-5:]]),
            "Architecture": statistics.mean([s["scores"]["architecture_score"] for s in scores[-5:]]),
            "Performance": statistics.mean([s["scores"]["performance_score"] for s in scores[-5:]]),
            "Completeness": statistics.mean([s["scores"]["completeness_score"] for s in scores[-5:]])
        }
        
        # Return lowest performing areas
        sorted_skills = sorted(skill_avgs.items(), key=lambda x: x[1])
        return [skill[0] for skill in sorted_skills[:2]]
    
    async def _calculate_success_probability(self, scores: List[Dict]) -> float:
        """Calculate probability of success on next attempt"""
        if len(scores) < 3:
            return 0.7
        
        recent_scores = [s["scores"]["total_score"] for s in scores[-3:]]
        success_count = len([s for s in recent_scores if s >= 70])
        
        return round(success_count / len(recent_scores), 2)