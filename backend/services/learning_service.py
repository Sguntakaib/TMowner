from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from bson import ObjectId


class LearningService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.learning_paths_collection = db.learning_paths
        self.user_progress_collection = db.user_learning_progress
        self.achievements_collection = db.achievements

    async def get_learning_paths(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get available learning paths"""
        query = {"active": True}
        if category:
            query["category"] = category
        
        paths = await self.learning_paths_collection.find(query).to_list(length=None)
        
        # Default learning paths if none exist
        if not paths:
            return await self._create_default_learning_paths()
        
        return paths

    async def get_learning_path_by_id(self, path_id: str) -> Optional[Dict[str, Any]]:
        """Get learning path details"""
        try:
            path = await self.learning_paths_collection.find_one({"_id": ObjectId(path_id)})
            return path
        except Exception:
            return None

    async def enroll_user_in_path(self, user_id: str, path_id: str) -> bool:
        """Enroll user in a learning path"""
        try:
            # Check if already enrolled
            existing = await self.user_progress_collection.find_one({
                "user_id": user_id,
                "path_id": path_id
            })
            
            if existing:
                return True  # Already enrolled
            
            # Create progress record
            progress_doc = {
                "user_id": user_id,
                "path_id": path_id,
                "enrolled_at": datetime.utcnow(),
                "current_module": 0,
                "completed_modules": [],
                "completion_percentage": 0.0,
                "last_activity": datetime.utcnow()
            }
            
            await self.user_progress_collection.insert_one(progress_doc)
            return True
        except Exception:
            return False

    async def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        """Get user's learning progress"""
        # Get all enrolled paths
        enrolled_paths = await self.user_progress_collection.find({
            "user_id": user_id
        }).to_list(length=None)
        
        progress_data = {
            "enrolled_paths": len(enrolled_paths),
            "active_paths": [],
            "completed_paths": [],
            "overall_progress": 0.0
        }
        
        total_progress = 0.0
        for path_progress in enrolled_paths:
            path = await self.learning_paths_collection.find_one({
                "_id": ObjectId(path_progress["path_id"])
            })
            
            if path:
                path_data = {
                    "path_id": path_progress["path_id"],
                    "path_name": path["name"],
                    "completion_percentage": path_progress["completion_percentage"],
                    "current_module": path_progress["current_module"],
                    "last_activity": path_progress["last_activity"]
                }
                
                if path_progress["completion_percentage"] >= 100:
                    progress_data["completed_paths"].append(path_data)
                else:
                    progress_data["active_paths"].append(path_data)
                
                total_progress += path_progress["completion_percentage"]
        
        if enrolled_paths:
            progress_data["overall_progress"] = total_progress / len(enrolled_paths)
        
        return progress_data

    async def get_personalized_recommendations(self, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get personalized learning recommendations"""
        # Get user's score history to identify weak areas
        user_scores = await self.db.scores.find({"user_id": user_id}).to_list(length=None)
        
        recommendations = []
        
        if not user_scores:
            # New user recommendations
            recommendations = [
                {
                    "type": "scenario",
                    "title": "Start with Web Security Fundamentals",
                    "description": "Learn basic web security concepts",
                    "category": "web",
                    "difficulty": "beginner",
                    "reason": "Perfect starting point for beginners"
                },
                {
                    "type": "learning_path",
                    "title": "Security Fundamentals Path",
                    "description": "Comprehensive introduction to security concepts",
                    "category": "security",
                    "reason": "Structured learning approach"
                }
            ]
        else:
            # Analyze performance to recommend improvements
            weak_areas = await self._identify_user_weak_areas(user_scores)
            
            for area in weak_areas[:limit]:
                recommendations.append({
                    "type": "scenario",
                    "title": f"Improve {area} Skills",
                    "description": f"Practice scenarios focused on {area.lower()}",
                    "category": area.lower(),
                    "difficulty": "intermediate",
                    "reason": f"Your {area.lower()} scores could be improved"
                })
        
        return recommendations

    async def get_user_achievements(self, user_id: str) -> Dict[str, Any]:
        """Get user achievements and badges"""
        # Get user's achievements
        user_achievements = await self.achievements_collection.find({
            "user_id": user_id
        }).to_list(length=None)
        
        # Get available achievements
        available_achievements = await self._get_available_achievements()
        
        earned_badges = [ach["badge_id"] for ach in user_achievements]
        
        return {
            "earned_badges": earned_badges,
            "total_earned": len(earned_badges),
            "available_achievements": available_achievements,
            "recent_achievements": sorted(user_achievements, key=lambda x: x["earned_at"], reverse=True)[:5],
            "progress_to_next": await self._calculate_progress_to_next_badge(user_id, earned_badges)
        }

    async def check_and_award_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        """Check for new achievements and award them"""
        # Get user stats
        user_scores = await self.db.scores.find({"user_id": user_id}).to_list(length=None)
        existing_achievements = await self.achievements_collection.find({
            "user_id": user_id
        }).to_list(length=None)
        
        existing_badge_ids = {ach["badge_id"] for ach in existing_achievements}
        new_achievements = []
        
        # Check various achievement criteria
        
        # First Score Achievement
        if len(user_scores) >= 1 and "first_score" not in existing_badge_ids:
            await self._award_achievement(user_id, "first_score", "First Steps", "Completed your first scenario")
            new_achievements.append({"badge_id": "first_score", "name": "First Steps"})
        
        # High Score Achievement
        high_scores = [s for s in user_scores if s["scores"]["total_score"] >= 90]
        if len(high_scores) >= 1 and "high_scorer" not in existing_badge_ids:
            await self._award_achievement(user_id, "high_scorer", "High Scorer", "Achieved a score of 90 or higher")
            new_achievements.append({"badge_id": "high_scorer", "name": "High Scorer"})
        
        # Consistent Performer
        if len(user_scores) >= 5:
            recent_scores = [s["scores"]["total_score"] for s in user_scores[-5:]]
            if all(score >= 70 for score in recent_scores) and "consistent_performer" not in existing_badge_ids:
                await self._award_achievement(user_id, "consistent_performer", "Consistent Performer", "Maintained good scores across 5 scenarios")
                new_achievements.append({"badge_id": "consistent_performer", "name": "Consistent Performer"})
        
        # Security Expert
        security_scores = [s["scores"]["security_score"] for s in user_scores if s["scores"]["security_score"] >= 85]
        if len(security_scores) >= 3 and "security_expert" not in existing_badge_ids:
            await self._award_achievement(user_id, "security_expert", "Security Expert", "Consistently high security scores")
            new_achievements.append({"badge_id": "security_expert", "name": "Security Expert"})
        
        return new_achievements

    # Private helper methods
    async def _create_default_learning_paths(self) -> List[Dict[str, Any]]:
        """Create default learning paths"""
        default_paths = [
            {
                "name": "Security Fundamentals",
                "description": "Learn the basics of cybersecurity and threat modeling",
                "category": "security",
                "difficulty": "beginner",
                "modules": [
                    {"name": "Introduction to Security", "scenarios": ["basic_web_security"]},
                    {"name": "Authentication & Authorization", "scenarios": ["auth_design"]},
                    {"name": "Data Protection", "scenarios": ["data_encryption"]}
                ],
                "estimated_hours": 10,
                "active": True,
                "created_at": datetime.utcnow()
            },
            {
                "name": "Web Application Security",
                "description": "Deep dive into web application security patterns",
                "category": "web",
                "difficulty": "intermediate",
                "modules": [
                    {"name": "Frontend Security", "scenarios": ["spa_security"]},
                    {"name": "API Security", "scenarios": ["rest_api_security"]},
                    {"name": "Database Security", "scenarios": ["database_protection"]}
                ],
                "estimated_hours": 15,
                "active": True,
                "created_at": datetime.utcnow()
            },
            {
                "name": "Cloud Security Architecture",
                "description": "Master cloud security and architecture patterns",
                "category": "cloud",
                "difficulty": "expert",
                "modules": [
                    {"name": "Cloud Fundamentals", "scenarios": ["cloud_basics"]},
                    {"name": "Microservices Security", "scenarios": ["microservices_arch"]},
                    {"name": "DevSecOps", "scenarios": ["devsecops_pipeline"]}
                ],
                "estimated_hours": 20,
                "active": True,
                "created_at": datetime.utcnow()
            }
        ]
        
        # Insert default paths
        for path in default_paths:
            await self.learning_paths_collection.insert_one(path)
        
        return default_paths

    async def _identify_user_weak_areas(self, user_scores: List[Dict[str, Any]]) -> List[str]:
        """Identify areas where user needs improvement"""
        if not user_scores:
            return []
        
        # Calculate average scores by category
        security_avg = sum(s["scores"]["security_score"] for s in user_scores) / len(user_scores)
        architecture_avg = sum(s["scores"]["architecture_score"] for s in user_scores) / len(user_scores)
        performance_avg = sum(s["scores"]["performance_score"] for s in user_scores) / len(user_scores)
        completeness_avg = sum(s["scores"]["completeness_score"] for s in user_scores) / len(user_scores)
        
        weak_areas = []
        threshold = 70  # Consider below 70 as weak
        
        if security_avg < threshold:
            weak_areas.append("Security")
        if architecture_avg < threshold:
            weak_areas.append("Architecture")
        if performance_avg < threshold:
            weak_areas.append("Performance")
        if completeness_avg < threshold:
            weak_areas.append("Completeness")
        
        return weak_areas

    async def _get_available_achievements(self) -> List[Dict[str, Any]]:
        """Get all available achievements"""
        return [
            {"badge_id": "first_score", "name": "First Steps", "description": "Complete your first scenario", "icon": "🎯"},
            {"badge_id": "high_scorer", "name": "High Scorer", "description": "Achieve a score of 90 or higher", "icon": "🏆"},
            {"badge_id": "consistent_performer", "name": "Consistent Performer", "description": "Maintain good scores across 5 scenarios", "icon": "📈"},
            {"badge_id": "security_expert", "name": "Security Expert", "description": "Consistently high security scores", "icon": "🔒"},
            {"badge_id": "architecture_master", "name": "Architecture Master", "description": "Excel at system architecture", "icon": "🏗️"},
            {"badge_id": "speed_demon", "name": "Speed Demon", "description": "Complete scenarios quickly", "icon": "⚡"},
            {"badge_id": "perfectionist", "name": "Perfectionist", "description": "Achieve perfect scores", "icon": "💯"}
        ]

    async def _calculate_progress_to_next_badge(self, user_id: str, earned_badges: List[str]) -> Dict[str, Any]:
        """Calculate progress towards next achievement"""
        user_scores = await self.db.scores.find({"user_id": user_id}).to_list(length=None)
        
        if not user_scores:
            return {
                "next_badge": "first_score",
                "progress": 0,
                "target": 1,
                "description": "Complete your first scenario"
            }
        
        # Check progress towards high scorer
        if "high_scorer" not in earned_badges:
            high_scores = [s for s in user_scores if s["scores"]["total_score"] >= 90]
            if not high_scores:
                best_score = max(s["scores"]["total_score"] for s in user_scores)
                return {
                    "next_badge": "high_scorer",
                    "progress": best_score,
                    "target": 90,
                    "description": "Achieve a score of 90 or higher"
                }
        
        # Check progress towards consistent performer
        if "consistent_performer" not in earned_badges and len(user_scores) < 5:
            return {
                "next_badge": "consistent_performer",
                "progress": len(user_scores),
                "target": 5,
                "description": "Complete 5 scenarios with good scores"
            }
        
        return {
            "next_badge": None,
            "progress": 100,
            "target": 100,
            "description": "All achievements unlocked!"
        }

    async def _award_achievement(self, user_id: str, badge_id: str, name: str, description: str):
        """Award an achievement to a user"""
        achievement_doc = {
            "user_id": user_id,
            "badge_id": badge_id,
            "name": name,
            "description": description,
            "earned_at": datetime.utcnow()
        }
        
        await self.achievements_collection.insert_one(achievement_doc)
        
        # Also update user progress in users collection
        await self.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$addToSet": {"progress.badges": badge_id}}
        )