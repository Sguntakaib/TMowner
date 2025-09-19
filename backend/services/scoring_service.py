from motor.motor_asyncio import AsyncIOMotorDatabase
from models.score import (
    ScoreResponse, ScoreInDB, ScoreBreakdown, ValidationResult, 
    FeedbackReport, LeaderboardEntry, UserStats
)
from models.diagram import DiagramResponse
from services.diagram_service import DiagramService
from services.scenario_service import ScenarioService
from services.validation_service import ThreatModelingValidationService
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from bson import ObjectId


class ScoringService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.scores
        self.diagram_service = DiagramService(db)
        self.scenario_service = ScenarioService(db)
        self.validation_service = ThreatModelingValidationService()

    async def validate_diagram(self, diagram_id: str, user_id: str) -> List[ValidationResult]:
        """Real-time diagram validation"""
        diagram = await self.diagram_service.get_diagram_by_id(diagram_id)
        if not diagram or diagram.user_id != user_id:
            raise ValueError("Diagram not found or access denied")
        
        validation_results = []
        
        # Security validations
        security_results = await self._validate_security(diagram)
        validation_results.extend(security_results)
        
        # Architecture validations  
        architecture_results = await self._validate_architecture(diagram)
        validation_results.extend(architecture_results)
        
        # Performance validations
        performance_results = await self._validate_performance(diagram)
        validation_results.extend(performance_results)
        
        # Completeness validations
        completeness_results = await self._validate_completeness(diagram)
        validation_results.extend(completeness_results)
        
        return validation_results

    async def score_diagram(self, diagram_id: str, user_id: str, time_spent: int) -> Optional[ScoreResponse]:
        """Calculate final score for diagram"""
        diagram = await self.diagram_service.get_diagram_by_id(diagram_id)
        if not diagram or diagram.user_id != user_id:
            raise ValueError("Diagram not found or access denied")
        
        # Get scenario for scoring criteria
        scenario = None
        if diagram.scenario_id:
            scenario = await self.scenario_service.get_scenario_by_id(diagram.scenario_id)
        
        # Run validation
        validation_results = await self.validate_diagram(diagram_id, user_id)
        
        # Calculate scores
        scores = await self._calculate_scores(diagram, validation_results, scenario, time_spent)
        
        # Generate feedback
        feedback = await self._generate_feedback(diagram, validation_results, scores)
        
        # Save score
        score_data = ScoreInDB(
            user_id=user_id,
            scenario_id=diagram.scenario_id or "",
            diagram_id=diagram_id,
            scores=scores,
            time_spent=time_spent,
            validation_results=validation_results,
            feedback=feedback
        )
        
        result = await self.collection.insert_one(score_data.dict(by_alias=True))
        created_score = await self.collection.find_one({"_id": result.inserted_id})
        
        return ScoreResponse(**created_score)

    async def get_user_scores(self, user_id: str, scenario_id: Optional[str] = None, 
                             skip: int = 0, limit: int = 20) -> List[ScoreResponse]:
        """Get user's scoring history"""
        query = {"user_id": user_id}
        
        if scenario_id:
            query["scenario_id"] = scenario_id
        
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("submission_time", -1)
        scores = await cursor.to_list(length=limit)
        
        return [ScoreResponse(**score) for score in scores]

    async def get_detailed_feedback(self, score_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed feedback for a score"""
        try:
            score = await self.collection.find_one({
                "_id": ObjectId(score_id),
                "user_id": user_id
            })
            
            if score:
                return {
                    "score": ScoreResponse(**score),
                    "detailed_analysis": await self._get_detailed_analysis(score),
                    "improvement_suggestions": await self._get_improvement_suggestions(score)
                }
        except Exception:
            pass
        return None

    async def get_leaderboard(self, category: Optional[str] = None, difficulty: Optional[str] = None,
                             timeframe: str = "all", limit: int = 10) -> List[LeaderboardEntry]:
        """Get leaderboard"""
        pipeline = []
        
        # Match criteria
        match_criteria = {}
        if timeframe != "all":
            days_ago = {"week": 7, "month": 30, "year": 365}[timeframe]
            cutoff_date = datetime.utcnow() - timedelta(days=days_ago)
            match_criteria["submission_time"] = {"$gte": cutoff_date}
        
        if category or difficulty:
            # Join with scenarios to filter by category/difficulty
            pipeline.append({
                "$lookup": {
                    "from": "scenarios",
                    "localField": "scenario_id",
                    "foreignField": "_id",
                    "as": "scenario"
                }
            })
            
            if category:
                match_criteria["scenario.category"] = category
            if difficulty:
                match_criteria["scenario.difficulty"] = difficulty
        
        if match_criteria:
            pipeline.append({"$match": match_criteria})
        
        # Group by user and calculate stats
        pipeline.extend([
            {
                "$group": {
                    "_id": "$user_id",
                    "total_score": {"$sum": "$scores.total_score"},
                    "scenarios_completed": {"$sum": 1},
                    "average_score": {"$avg": "$scores.total_score"},
                    "best_score": {"$max": "$scores.total_score"}
                }
            },
            {"$sort": {"average_score": -1}},
            {"$limit": limit}
        ])
        
        results = await self.collection.aggregate(pipeline).to_list(length=limit)
        
        leaderboard = []
        for rank, result in enumerate(results, 1):
            # Get user name
            user = await self.db.users.find_one({"_id": ObjectId(result["_id"])})
            user_name = f"{user.get('profile', {}).get('first_name', '')} {user.get('profile', {}).get('last_name', '')}".strip()
            if not user_name:
                user_name = user.get('email', 'Anonymous').split('@')[0]
            
            leaderboard.append(LeaderboardEntry(
                user_id=result["_id"],
                user_name=user_name,
                total_score=result["total_score"],
                scenarios_completed=result["scenarios_completed"],
                average_score=result["average_score"],
                rank=rank
            ))
        
        return leaderboard

    async def get_user_stats(self, user_id: str) -> UserStats:
        """Get user statistics"""
        # Get user's scores
        user_scores = await self.collection.find({"user_id": user_id}).to_list(length=None)
        
        # Calculate stats
        total_scenarios = len(user_scores)
        completed_scenarios = len([s for s in user_scores if s["scores"]["total_score"] >= 70])
        
        if user_scores:
            average_score = sum(s["scores"]["total_score"] for s in user_scores) / len(user_scores)
            best_score = max(s["scores"]["total_score"] for s in user_scores)
            total_time_spent = sum(s["time_spent"] for s in user_scores)
        else:
            average_score = 0
            best_score = 0
            total_time_spent = 0
        
        # Calculate current streak (consecutive days with activity)
        current_streak = await self._calculate_streak(user_id)
        
        # Get badges
        user = await self.db.users.find_one({"_id": ObjectId(user_id)})
        badges_earned = user.get("progress", {}).get("badges", []) if user else []
        
        return UserStats(
            total_scenarios=total_scenarios,
            completed_scenarios=completed_scenarios,
            average_score=average_score,
            best_score=best_score,
            total_time_spent=total_time_spent,
            current_streak=current_streak,
            badges_earned=badges_earned
        )

    async def get_user_analytics(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get user performance analytics"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        user_scores = await self.collection.find({
            "user_id": user_id,
            "submission_time": {"$gte": cutoff_date}
        }).sort("submission_time", 1).to_list(length=None)
        
        # Prepare analytics data
        daily_scores = {}
        category_performance = {}
        
        for score in user_scores:
            date_key = score["submission_time"].strftime("%Y-%m-%d")
            if date_key not in daily_scores:
                daily_scores[date_key] = []
            daily_scores[date_key].append(score["scores"]["total_score"])
            
            # Category performance (if scenario data available)
            if score.get("scenario_id"):
                scenario = await self.scenario_service.get_scenario_by_id(score["scenario_id"])
                if scenario:
                    category = scenario.category
                    if category not in category_performance:
                        category_performance[category] = []
                    category_performance[category].append(score["scores"]["total_score"])
        
        return {
            "daily_scores": {date: sum(scores)/len(scores) for date, scores in daily_scores.items()},
            "category_performance": {cat: sum(scores)/len(scores) for cat, scores in category_performance.items()},
            "improvement_trend": await self._calculate_improvement_trend(user_scores),
            "weak_areas": await self._identify_weak_areas(user_scores)
        }

    # Private helper methods
    async def _validate_security(self, diagram: DiagramResponse) -> List[ValidationResult]:
        """Validate security aspects of the diagram"""
        results = []
        
        # Check for authentication elements
        auth_nodes = [node for node in diagram.diagram_data.nodes if 'auth' in node.type.lower()]
        if not auth_nodes:
            results.append(ValidationResult(
                rule_id="SEC001",
                rule_name="Authentication Required",
                severity="error",
                message="No authentication mechanism found in the design",
                category="security"
            ))
        
        # Check for HTTPS/TLS
        secure_connections = [edge for edge in diagram.diagram_data.edges 
                            if edge.data.get('protocol', '').lower() in ['https', 'tls']]
        
        if len(secure_connections) < len(diagram.diagram_data.edges) * 0.8:
            results.append(ValidationResult(
                rule_id="SEC002", 
                rule_name="Secure Communication",
                severity="warning",
                message="Many connections are not using secure protocols (HTTPS/TLS)",
                category="security"
            ))
        
        return results

    async def _validate_architecture(self, diagram: DiagramResponse) -> List[ValidationResult]:
        """Validate architecture aspects"""
        results = []
        
        # Check for proper separation of concerns
        if len(diagram.diagram_data.nodes) > 1:
            # Look for database nodes connected directly to frontend
            frontend_nodes = [n for n in diagram.diagram_data.nodes if 'frontend' in n.type.lower()]
            database_nodes = [n for n in diagram.diagram_data.nodes if 'database' in n.type.lower()]
            
            direct_connections = [
                edge for edge in diagram.diagram_data.edges
                if any(edge.source == fn.id for fn in frontend_nodes) and 
                   any(edge.target == db.id for db in database_nodes)
            ]
            
            if direct_connections:
                results.append(ValidationResult(
                    rule_id="ARCH001",
                    rule_name="Separation of Concerns",
                    severity="error", 
                    message="Frontend should not connect directly to database",
                    category="architecture"
                ))
        
        return results

    async def _validate_performance(self, diagram: DiagramResponse) -> List[ValidationResult]:
        """Validate performance aspects"""
        results = []
        
        # Check for load balancers in high-traffic scenarios
        if len(diagram.diagram_data.nodes) > 5:  # Assume complex system
            lb_nodes = [n for n in diagram.diagram_data.nodes if 'load' in n.type.lower() or 'balancer' in n.type.lower()]
            if not lb_nodes:
                results.append(ValidationResult(
                    rule_id="PERF001",
                    rule_name="Load Balancing",
                    severity="warning",
                    message="Consider adding load balancing for scalability",
                    category="performance"
                ))
        
        return results

    async def _validate_completeness(self, diagram: DiagramResponse) -> List[ValidationResult]:
        """Validate completeness of the design"""
        results = []
        
        # Check minimum required elements
        if len(diagram.diagram_data.nodes) < 3:
            results.append(ValidationResult(
                rule_id="COMP001",
                rule_name="Design Completeness",
                severity="error",
                message="Design appears incomplete - minimum 3 components expected",
                category="completeness"
            ))
        
        # Check for unconnected nodes
        connected_nodes = set()
        for edge in diagram.diagram_data.edges:
            connected_nodes.add(edge.source)
            connected_nodes.add(edge.target)
        
        unconnected = [n for n in diagram.diagram_data.nodes if n.id not in connected_nodes]
        if unconnected:
            results.append(ValidationResult(
                rule_id="COMP002",
                rule_name="Isolated Components",
                severity="warning",
                message=f"{len(unconnected)} components are not connected to the system",
                category="completeness"
            ))
        
        return results

    async def _calculate_scores(self, diagram: DiagramResponse, validation_results: List[ValidationResult],
                               scenario: Optional[Any], time_spent: int) -> ScoreBreakdown:
        """Calculate individual and total scores"""
        # Get scoring weights
        if scenario:
            security_weight = scenario.scoring_criteria.security_weight
            architecture_weight = scenario.scoring_criteria.architecture_weight  
            performance_weight = scenario.scoring_criteria.performance_weight
            completeness_weight = scenario.scoring_criteria.completeness_weight
        else:
            security_weight = architecture_weight = performance_weight = completeness_weight = 0.25
        
        # Base scores (start at 100, deduct for violations)
        security_score = 100.0
        architecture_score = 100.0
        performance_score = 100.0
        completeness_score = 100.0
        
        # Deduct points for violations
        for result in validation_results:
            deduction = 20 if result.severity == "error" else 10 if result.severity == "warning" else 5
            
            if result.category == "security":
                security_score = max(0, security_score - deduction)
            elif result.category == "architecture":
                architecture_score = max(0, architecture_score - deduction)
            elif result.category == "performance":
                performance_score = max(0, performance_score - deduction)
            elif result.category == "completeness":
                completeness_score = max(0, completeness_score - deduction)
        
        # Calculate weighted total
        total_score = (
            security_score * security_weight +
            architecture_score * architecture_weight +
            performance_score * performance_weight +
            completeness_score * completeness_weight
        )
        
        # Time bonus/penalty (optional)
        if scenario and scenario.time_limit:
            if time_spent < scenario.time_limit * 60 * 0.8:  # Finished in less than 80% of time limit
                total_score *= 1.1  # 10% bonus
            elif time_spent > scenario.time_limit * 60:  # Exceeded time limit
                total_score *= 0.9  # 10% penalty
        
        return ScoreBreakdown(
            security_score=security_score,
            architecture_score=architecture_score,
            performance_score=performance_score,
            completeness_score=completeness_score,
            total_score=min(100, total_score)  # Cap at 100
        )

    async def _generate_feedback(self, diagram: DiagramResponse, validation_results: List[ValidationResult],
                               scores: ScoreBreakdown) -> FeedbackReport:
        """Generate detailed feedback"""
        strengths = []
        weaknesses = []
        recommendations = []
        
        # Analyze scores for strengths and weaknesses
        if scores.security_score >= 80:
            strengths.append("Strong security implementation")
        else:
            weaknesses.append("Security implementation needs improvement")
            recommendations.append("Review authentication and encryption mechanisms")
        
        if scores.architecture_score >= 80:
            strengths.append("Well-structured architecture")
        else:
            weaknesses.append("Architecture could be better organized")
            recommendations.append("Consider separation of concerns and layered architecture")
        
        # Add specific recommendations based on validation results
        error_count = len([r for r in validation_results if r.severity == "error"])
        warning_count = len([r for r in validation_results if r.severity == "warning"])
        
        if error_count == 0:
            strengths.append("No critical security or architectural errors")
        
        if warning_count > 0:
            recommendations.append(f"Address {warning_count} improvement opportunities")
        
        # Generate summary
        score_level = "Excellent" if scores.total_score >= 90 else \
                     "Good" if scores.total_score >= 70 else \
                     "Needs Improvement" if scores.total_score >= 50 else "Poor"
        
        summary = f"{score_level} design with a score of {scores.total_score:.1f}/100. " + \
                 f"Found {error_count} errors and {warning_count} warnings."
        
        return FeedbackReport(
            summary=summary,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            next_steps=[
                "Review the validation results",
                "Implement suggested improvements", 
                "Test your updated design",
                "Try more advanced scenarios"
            ]
        )

    async def _calculate_streak(self, user_id: str) -> int:
        """Calculate user's current streak of consecutive active days"""
        # Get user's recent scores grouped by date
        recent_scores = await self.collection.find({
            "user_id": user_id,
            "submission_time": {"$gte": datetime.utcnow() - timedelta(days=30)}
        }).sort("submission_time", -1).to_list(length=None)
        
        if not recent_scores:
            return 0
        
        # Group by date
        activity_dates = set()
        for score in recent_scores:
            date_key = score["submission_time"].strftime("%Y-%m-%d")
            activity_dates.add(date_key)
        
        # Calculate streak from today backwards
        streak = 0
        current_date = datetime.utcnow().date()
        
        while current_date.strftime("%Y-%m-%d") in activity_dates:
            streak += 1
            current_date -= timedelta(days=1)
        
        return streak

    async def _get_detailed_analysis(self, score: dict) -> Dict[str, Any]:
        """Get detailed analysis of the score"""
        return {
            "score_breakdown": score["scores"],
            "validation_summary": {
                "total_issues": len(score["validation_results"]),
                "errors": len([r for r in score["validation_results"] if r["severity"] == "error"]),
                "warnings": len([r for r in score["validation_results"] if r["severity"] == "warning"]),
                "info": len([r for r in score["validation_results"] if r["severity"] == "info"])
            },
            "performance_metrics": {
                "time_spent_minutes": score["time_spent"] // 60,
                "efficiency_rating": "Good" if score["time_spent"] < 1800 else "Average"
            }
        }

    async def _get_improvement_suggestions(self, score: dict) -> List[str]:
        """Get specific improvement suggestions"""
        suggestions = []
        
        scores = score["scores"]
        
        if scores["security_score"] < 70:
            suggestions.append("Focus on implementing proper authentication and authorization")
            suggestions.append("Ensure all communications use secure protocols (HTTPS/TLS)")
        
        if scores["architecture_score"] < 70:
            suggestions.append("Review architectural patterns and separation of concerns")
            suggestions.append("Consider implementing proper layered architecture")
        
        if scores["performance_score"] < 70:
            suggestions.append("Add load balancing and caching mechanisms")
            suggestions.append("Review database design and query optimization")
        
        if scores["completeness_score"] < 70:
            suggestions.append("Ensure all required components are included")
            suggestions.append("Review system integration and data flows")
        
        return suggestions

    async def _calculate_improvement_trend(self, user_scores: List[dict]) -> str:
        """Calculate if user is improving over time"""
        if len(user_scores) < 2:
            return "Not enough data"
        
        # Compare recent vs older scores
        recent_scores = [s["scores"]["total_score"] for s in user_scores[-5:]]
        older_scores = [s["scores"]["total_score"] for s in user_scores[:-5]] if len(user_scores) > 5 else []
        
        if not older_scores:
            return "Improving" if len(recent_scores) > 1 and recent_scores[-1] > recent_scores[0] else "Stable"
        
        recent_avg = sum(recent_scores) / len(recent_scores)
        older_avg = sum(older_scores) / len(older_scores)
        
        if recent_avg > older_avg + 5:
            return "Improving"
        elif recent_avg < older_avg - 5:
            return "Declining"
        else:
            return "Stable"

    async def _identify_weak_areas(self, user_scores: List[dict]) -> List[str]:
        """Identify areas where user consistently scores low"""
        weak_areas = []
        
        if not user_scores:
            return weak_areas
        
        # Calculate average scores by category
        security_scores = [s["scores"]["security_score"] for s in user_scores]
        architecture_scores = [s["scores"]["architecture_score"] for s in user_scores]
        performance_scores = [s["scores"]["performance_score"] for s in user_scores]
        completeness_scores = [s["scores"]["completeness_score"] for s in user_scores]
        
        if sum(security_scores) / len(security_scores) < 70:
            weak_areas.append("Security")
        
        if sum(architecture_scores) / len(architecture_scores) < 70:
            weak_areas.append("Architecture")
        
        if sum(performance_scores) / len(performance_scores) < 70:
            weak_areas.append("Performance")
        
        if sum(completeness_scores) / len(completeness_scores) < 70:
            weak_areas.append("Completeness")
        
        return weak_areas