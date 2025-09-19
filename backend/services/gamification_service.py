"""
Enhanced Gamification Service for Achievement and Badge Management
"""
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from bson import ObjectId
import math


class GamificationService:
    """Advanced gamification system with badges, achievements, and progress tracking"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.achievements_collection = db.achievements
        self.user_achievements_collection = db.user_achievements
        self.badges_collection = db.badges
        self.streaks_collection = db.user_streaks
        
    async def initialize_badges_system(self):
        """Initialize the badge system with predefined badges"""
        badges = await self._get_default_badges()
        
        # Insert badges if they don't exist
        for badge in badges:
            existing = await self.badges_collection.find_one({"badge_id": badge["badge_id"]})
            if not existing:
                await self.badges_collection.insert_one(badge)
    
    async def get_user_achievements(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user achievement data"""
        # Get user achievements
        user_achievements = await self.user_achievements_collection.find({
            "user_id": user_id
        }).to_list(length=None)
        
        # Get all available badges
        all_badges = await self.badges_collection.find({}).to_list(length=None)
        
        # Get user stats for progress calculation
        user_stats = await self._get_user_stats(user_id)
        
        # Calculate achievement progress
        achievement_progress = await self._calculate_achievement_progress(user_id, user_stats)
        
        earned_badges = {ach["badge_id"]: ach for ach in user_achievements}
        
        return {
            "total_badges": len(all_badges),
            "earned_badges": len(user_achievements),
            "completion_percentage": (len(user_achievements) / len(all_badges)) * 100 if all_badges else 0,
            "recent_achievements": sorted(user_achievements, key=lambda x: x["earned_at"], reverse=True)[:5],
            "badges": [
                {
                    **badge,
                    "earned": badge["badge_id"] in earned_badges,
                    "earned_at": earned_badges.get(badge["badge_id"], {}).get("earned_at"),
                    "progress": achievement_progress.get(badge["badge_id"], {})
                }
                for badge in all_badges
            ],
            "next_milestone": await self._get_next_milestone(user_id, earned_badges, achievement_progress),
            "user_level": await self._calculate_user_level(user_stats),
            "experience_points": user_stats.get("total_score", 0)
        }
    
    async def check_and_award_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        """Check for new achievements and award them"""
        user_stats = await self._get_user_stats(user_id)
        existing_achievements = await self.user_achievements_collection.find({
            "user_id": user_id
        }).to_list(length=None)
        
        existing_badge_ids = {ach["badge_id"] for ach in existing_achievements}
        new_achievements = []
        
        # Check all achievement criteria
        achievement_checks = [
            self._check_first_steps(user_id, user_stats, existing_badge_ids),
            self._check_score_achievements(user_id, user_stats, existing_badge_ids),
            self._check_consistency_achievements(user_id, user_stats, existing_badge_ids),
            self._check_expertise_achievements(user_id, user_stats, existing_badge_ids),
            self._check_speed_achievements(user_id, user_stats, existing_badge_ids),
            self._check_streak_achievements(user_id, user_stats, existing_badge_ids),
            self._check_completion_achievements(user_id, user_stats, existing_badge_ids),
            self._check_special_achievements(user_id, user_stats, existing_badge_ids)
        ]
        
        for check_results in await asyncio.gather(*achievement_checks):
            new_achievements.extend(check_results)
        
        return new_achievements
    
    async def get_leaderboard_with_achievements(self, category: Optional[str] = None, 
                                              timeframe: str = "all", limit: int = 20) -> List[Dict[str, Any]]:
        """Get leaderboard enhanced with achievement information"""
        # Get basic leaderboard from scoring service
        from services.scoring_service import ScoringService
        scoring_service = ScoringService(self.db)
        basic_leaderboard = await scoring_service.get_leaderboard(category, None, timeframe, limit)
        
        # Enhance with achievement data
        enhanced_leaderboard = []
        for entry in basic_leaderboard:
            user_achievements = await self.user_achievements_collection.find({
                "user_id": entry.user_id
            }).to_list(length=None)
            
            # Get featured badges (highest tier achievements)
            featured_badges = [ach for ach in user_achievements if 
                             await self._is_featured_badge(ach["badge_id"])]
            
            enhanced_entry = {
                **entry.dict(),
                "badge_count": len(user_achievements),
                "featured_badges": featured_badges[:3],  # Top 3 featured badges
                "achievement_score": await self._calculate_achievement_score(user_achievements)
            }
            enhanced_leaderboard.append(enhanced_entry)
        
        return enhanced_leaderboard
    
    async def get_achievement_statistics(self) -> Dict[str, Any]:
        """Get global achievement statistics"""
        all_badges = await self.badges_collection.find({}).to_list(length=None)
        all_user_achievements = await self.user_achievements_collection.find({}).to_list(length=None)
        
        # Calculate badge rarity
        badge_stats = {}
        total_users = await self.db.users.count_documents({})
        
        for badge in all_badges:
            earned_count = len([ach for ach in all_user_achievements if ach["badge_id"] == badge["badge_id"]])
            rarity_percentage = (earned_count / total_users) * 100 if total_users > 0 else 0
            
            badge_stats[badge["badge_id"]] = {
                "name": badge["name"],
                "earned_count": earned_count,
                "rarity_percentage": rarity_percentage,
                "tier": badge.get("tier", "common")
            }
        
        # Most recent achievements
        recent_achievements = await self.user_achievements_collection.find({}).sort("earned_at", -1).limit(10).to_list(length=10)
        
        return {
            "total_badges": len(all_badges),
            "total_achievements_earned": len(all_user_achievements),
            "average_badges_per_user": len(all_user_achievements) / total_users if total_users > 0 else 0,
            "badge_statistics": badge_stats,
            "recent_achievements": recent_achievements,
            "rarest_badges": sorted(badge_stats.items(), key=lambda x: x[1]["rarity_percentage"])[:5]
        }
    
    # Private helper methods
    async def _get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user statistics"""
        user_scores = await self.db.scores.find({"user_id": user_id}).to_list(length=None)
        
        if not user_scores:
            return {
                "total_scenarios": 0,
                "total_score": 0,
                "average_score": 0,
                "best_score": 0,
                "perfect_scores": 0,
                "high_scores": 0,
                "security_avg": 0,
                "architecture_avg": 0,
                "performance_avg": 0,
                "completeness_avg": 0,
                "total_time": 0,
                "streak_data": {"current": 0, "longest": 0}
            }
        
        total_score = sum(s["scores"]["total_score"] for s in user_scores)
        perfect_scores = len([s for s in user_scores if s["scores"]["total_score"] >= 100])
        high_scores = len([s for s in user_scores if s["scores"]["total_score"] >= 90])
        
        return {
            "total_scenarios": len(user_scores),
            "total_score": total_score,
            "average_score": total_score / len(user_scores),
            "best_score": max(s["scores"]["total_score"] for s in user_scores),
            "perfect_scores": perfect_scores,
            "high_scores": high_scores,
            "security_avg": sum(s["scores"]["security_score"] for s in user_scores) / len(user_scores),
            "architecture_avg": sum(s["scores"]["architecture_score"] for s in user_scores) / len(user_scores),
            "performance_avg": sum(s["scores"]["performance_score"] for s in user_scores) / len(user_scores),
            "completeness_avg": sum(s["scores"]["completeness_score"] for s in user_scores) / len(user_scores),
            "total_time": sum(s["time_spent"] for s in user_scores),
            "streak_data": await self._get_streak_data(user_id)
        }
    
    async def _calculate_achievement_progress(self, user_id: str, user_stats: Dict[str, Any]) -> Dict[str, Dict]:
        """Calculate progress towards each achievement"""
        progress = {}
        
        # Progress towards score-based achievements
        progress["high_scorer"] = {
            "current": user_stats["best_score"],
            "target": 90,
            "percentage": min(100, (user_stats["best_score"] / 90) * 100)
        }
        
        progress["perfectionist"] = {
            "current": user_stats["perfect_scores"],
            "target": 1,
            "percentage": min(100, user_stats["perfect_scores"] * 100)
        }
        
        # Progress towards consistency achievements
        progress["consistent_performer"] = {
            "current": user_stats["total_scenarios"],
            "target": 5,
            "percentage": min(100, (user_stats["total_scenarios"] / 5) * 100)
        }
        
        # Progress towards expertise achievements
        progress["security_expert"] = {
            "current": user_stats["security_avg"],
            "target": 85,
            "percentage": min(100, (user_stats["security_avg"] / 85) * 100)
        }
        
        # Progress towards marathon achievements
        progress["marathon_runner"] = {
            "current": user_stats["total_scenarios"],
            "target": 50,
            "percentage": min(100, (user_stats["total_scenarios"] / 50) * 100)
        }
        
        return progress
    
    async def _get_next_milestone(self, user_id: str, earned_badges: Dict, progress: Dict) -> Dict[str, Any]:
        """Get the next achievable milestone"""
        # Find the closest unearned achievement
        closest_achievement = None
        min_distance = float('inf')
        
        for badge_id, prog_data in progress.items():
            if badge_id not in earned_badges and prog_data["percentage"] < 100:
                distance = 100 - prog_data["percentage"]
                if distance < min_distance:
                    min_distance = distance
                    closest_achievement = {
                        "badge_id": badge_id,
                        "progress_percentage": prog_data["percentage"],
                        "remaining": prog_data["target"] - prog_data["current"]
                    }
        
        return closest_achievement
    
    async def _calculate_user_level(self, user_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate user level based on experience points"""
        total_score = user_stats.get("total_score", 0)
        
        # Level calculation: Level = floor(sqrt(total_score / 100))
        level = math.floor(math.sqrt(total_score / 100)) + 1
        
        # Experience needed for next level
        next_level_threshold = ((level) ** 2) * 100
        current_level_threshold = ((level - 1) ** 2) * 100
        
        progress_in_level = total_score - current_level_threshold
        progress_needed = next_level_threshold - current_level_threshold
        
        return {
            "current_level": level,
            "experience_points": total_score,
            "progress_in_level": progress_in_level,
            "progress_needed": progress_needed,
            "progress_percentage": (progress_in_level / progress_needed) * 100 if progress_needed > 0 else 100
        }
    
    async def _get_streak_data(self, user_id: str) -> Dict[str, int]:
        """Get user's streak information"""
        # Get user's recent activity
        recent_scores = await self.db.scores.find({
            "user_id": user_id,
            "submission_time": {"$gte": datetime.utcnow() - timedelta(days=90)}
        }).sort("submission_time", -1).to_list(length=None)
        
        if not recent_scores:
            return {"current": 0, "longest": 0}
        
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
        
        # Calculate longest streak (simplified - in production, store this)
        longest_streak = current_streak  # Simplified for this example
        
        return {"current": current_streak, "longest": longest_streak}
    
    # Achievement check methods
    async def _check_first_steps(self, user_id: str, stats: Dict, existing: set) -> List[Dict]:
        achievements = []
        if stats["total_scenarios"] >= 1 and "first_steps" not in existing:
            await self._award_achievement(user_id, "first_steps", "First Steps", 
                                        "Completed your first threat modeling scenario")
            achievements.append({"badge_id": "first_steps", "name": "First Steps"})
        return achievements
    
    async def _check_score_achievements(self, user_id: str, stats: Dict, existing: set) -> List[Dict]:
        achievements = []
        
        if stats["best_score"] >= 90 and "high_scorer" not in existing:
            await self._award_achievement(user_id, "high_scorer", "High Scorer", 
                                        "Achieved a score of 90 or higher")
            achievements.append({"badge_id": "high_scorer", "name": "High Scorer"})
        
        if stats["perfect_scores"] >= 1 and "perfectionist" not in existing:
            await self._award_achievement(user_id, "perfectionist", "Perfectionist", 
                                        "Achieved a perfect score of 100")
            achievements.append({"badge_id": "perfectionist", "name": "Perfectionist"})
        
        if stats["perfect_scores"] >= 5 and "master_perfectionist" not in existing:
            await self._award_achievement(user_id, "master_perfectionist", "Master Perfectionist", 
                                        "Achieved 5 perfect scores")
            achievements.append({"badge_id": "master_perfectionist", "name": "Master Perfectionist"})
            
        return achievements
    
    async def _check_consistency_achievements(self, user_id: str, stats: Dict, existing: set) -> List[Dict]:
        achievements = []
        
        if stats["total_scenarios"] >= 5 and stats["average_score"] >= 70 and "consistent_performer" not in existing:
            await self._award_achievement(user_id, "consistent_performer", "Consistent Performer", 
                                        "Maintained good scores across 5 scenarios")
            achievements.append({"badge_id": "consistent_performer", "name": "Consistent Performer"})
        
        if stats["total_scenarios"] >= 20 and "dedicated_learner" not in existing:
            await self._award_achievement(user_id, "dedicated_learner", "Dedicated Learner", 
                                        "Completed 20 threat modeling scenarios")
            achievements.append({"badge_id": "dedicated_learner", "name": "Dedicated Learner"})
            
        return achievements
    
    async def _check_expertise_achievements(self, user_id: str, stats: Dict, existing: set) -> List[Dict]:
        achievements = []
        
        if stats["security_avg"] >= 85 and "security_expert" not in existing:
            await self._award_achievement(user_id, "security_expert", "Security Expert", 
                                        "Consistently high security scores")
            achievements.append({"badge_id": "security_expert", "name": "Security Expert"})
        
        if stats["architecture_avg"] >= 85 and "architecture_master" not in existing:
            await self._award_achievement(user_id, "architecture_master", "Architecture Master", 
                                        "Mastered system architecture design")
            achievements.append({"badge_id": "architecture_master", "name": "Architecture Master"})
            
        return achievements
    
    async def _check_speed_achievements(self, user_id: str, stats: Dict, existing: set) -> List[Dict]:
        achievements = []
        
        # Check recent scores for speed (simplified)
        recent_scores = await self.db.scores.find({
            "user_id": user_id
        }).sort("submission_time", -1).limit(5).to_list(length=5)
        
        fast_completions = [s for s in recent_scores if s["time_spent"] < 900]  # Under 15 minutes
        
        if len(fast_completions) >= 3 and "speed_demon" not in existing:
            await self._award_achievement(user_id, "speed_demon", "Speed Demon", 
                                        "Completed multiple scenarios quickly")
            achievements.append({"badge_id": "speed_demon", "name": "Speed Demon"})
            
        return achievements
    
    async def _check_streak_achievements(self, user_id: str, stats: Dict, existing: set) -> List[Dict]:
        achievements = []
        streak_data = stats.get("streak_data", {})
        
        if streak_data.get("current", 0) >= 7 and "week_warrior" not in existing:
            await self._award_achievement(user_id, "week_warrior", "Week Warrior", 
                                        "Maintained a 7-day learning streak")
            achievements.append({"badge_id": "week_warrior", "name": "Week Warrior"})
            
        return achievements
    
    async def _check_completion_achievements(self, user_id: str, stats: Dict, existing: set) -> List[Dict]:
        achievements = []
        
        if stats["total_scenarios"] >= 50 and "marathon_runner" not in existing:
            await self._award_achievement(user_id, "marathon_runner", "Marathon Runner", 
                                        "Completed 50 threat modeling scenarios")
            achievements.append({"badge_id": "marathon_runner", "name": "Marathon Runner"})
            
        return achievements
    
    async def _check_special_achievements(self, user_id: str, stats: Dict, existing: set) -> List[Dict]:
        achievements = []
        
        # Check for balanced skills (all categories above 80)
        if (stats["security_avg"] >= 80 and stats["architecture_avg"] >= 80 and 
            stats["performance_avg"] >= 80 and stats["completeness_avg"] >= 80 and 
            "well_rounded" not in existing):
            await self._award_achievement(user_id, "well_rounded", "Well Rounded", 
                                        "Excellent performance across all skill areas")
            achievements.append({"badge_id": "well_rounded", "name": "Well Rounded"})
            
        return achievements
    
    async def _award_achievement(self, user_id: str, badge_id: str, name: str, description: str):
        """Award an achievement to a user"""
        achievement_doc = {
            "user_id": user_id,
            "badge_id": badge_id,
            "name": name,
            "description": description,
            "earned_at": datetime.utcnow(),
            "points_awarded": await self._get_badge_points(badge_id)
        }
        
        await self.user_achievements_collection.insert_one(achievement_doc)
        
        # Update user progress
        await self.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$addToSet": {"progress.badges": badge_id},
                "$inc": {"progress.experience_points": achievement_doc["points_awarded"]}
            }
        )
    
    async def _get_badge_points(self, badge_id: str) -> int:
        """Get points awarded for a specific badge"""
        badge_points = {
            "first_steps": 10,
            "high_scorer": 25,
            "perfectionist": 50,
            "master_perfectionist": 100,
            "consistent_performer": 30,
            "dedicated_learner": 75,
            "security_expert": 40,
            "architecture_master": 40,
            "speed_demon": 35,
            "week_warrior": 25,
            "marathon_runner": 150,
            "well_rounded": 100
        }
        return badge_points.get(badge_id, 10)
    
    async def _is_featured_badge(self, badge_id: str) -> bool:
        """Check if badge is featured (high-tier achievement)"""
        featured_badges = [
            "perfectionist", "master_perfectionist", "security_expert", 
            "architecture_master", "marathon_runner", "well_rounded"
        ]
        return badge_id in featured_badges
    
    async def _calculate_achievement_score(self, achievements: List[Dict]) -> int:
        """Calculate total achievement score"""
        return sum(ach.get("points_awarded", 10) for ach in achievements)
    
    async def _get_default_badges(self) -> List[Dict[str, Any]]:
        """Get default badge definitions"""
        return [
            {
                "badge_id": "first_steps",
                "name": "First Steps",
                "description": "Complete your first threat modeling scenario",
                "icon": "🎯",
                "tier": "bronze",
                "category": "milestone",
                "points": 10
            },
            {
                "badge_id": "high_scorer",
                "name": "High Scorer", 
                "description": "Achieve a score of 90 or higher",
                "icon": "🏆",
                "tier": "silver",
                "category": "performance",
                "points": 25
            },
            {
                "badge_id": "perfectionist",
                "name": "Perfectionist",
                "description": "Achieve a perfect score of 100",
                "icon": "💯",
                "tier": "gold",
                "category": "performance",
                "points": 50
            },
            {
                "badge_id": "master_perfectionist",
                "name": "Master Perfectionist",
                "description": "Achieve 5 perfect scores",
                "icon": "🌟",
                "tier": "platinum",
                "category": "performance",
                "points": 100
            },
            {
                "badge_id": "consistent_performer",
                "name": "Consistent Performer",
                "description": "Maintain good scores across 5 scenarios",
                "icon": "📈",
                "tier": "silver",
                "category": "consistency",
                "points": 30
            },
            {
                "badge_id": "dedicated_learner",
                "name": "Dedicated Learner",
                "description": "Complete 20 threat modeling scenarios",
                "icon": "📚",
                "tier": "gold",
                "category": "dedication",
                "points": 75
            },
            {
                "badge_id": "security_expert",
                "name": "Security Expert",
                "description": "Consistently high security scores",
                "icon": "🔒",
                "tier": "gold",
                "category": "expertise",
                "points": 40
            },
            {
                "badge_id": "architecture_master",
                "name": "Architecture Master",
                "description": "Master system architecture design",
                "icon": "🏗️",
                "tier": "gold", 
                "category": "expertise",
                "points": 40
            },
            {
                "badge_id": "speed_demon",
                "name": "Speed Demon",
                "description": "Complete scenarios quickly with good scores",
                "icon": "⚡",
                "tier": "silver",
                "category": "efficiency",
                "points": 35
            },
            {
                "badge_id": "week_warrior",
                "name": "Week Warrior",
                "description": "Maintain a 7-day learning streak",
                "icon": "🔥",
                "tier": "silver",
                "category": "consistency",
                "points": 25
            },
            {
                "badge_id": "marathon_runner",
                "name": "Marathon Runner",
                "description": "Complete 50 threat modeling scenarios",
                "icon": "🏃‍♂️",
                "tier": "platinum",
                "category": "dedication",
                "points": 150
            },
            {
                "badge_id": "well_rounded",
                "name": "Well Rounded",
                "description": "Excel across all skill areas",
                "icon": "⭐",
                "tier": "platinum",
                "category": "mastery",
                "points": 100
            }
        ]


import asyncio  # Add this import at the top