from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from .user import PyObjectId, ObjectId


class ScoreBreakdown(BaseModel):
    security_score: float = 0.0
    architecture_score: float = 0.0
    performance_score: float = 0.0
    completeness_score: float = 0.0
    total_score: float = 0.0


class ValidationResult(BaseModel):
    rule_id: str
    rule_name: str
    severity: str  # error|warning|info
    message: str
    element_id: Optional[str] = None
    element_type: Optional[str] = None
    category: str  # security|architecture|performance|completeness


class FeedbackReport(BaseModel):
    summary: str
    strengths: List[str] = []
    weaknesses: List[str] = []
    recommendations: List[str] = []
    next_steps: List[str] = []


class ScoreCreate(BaseModel):
    scenario_id: str
    diagram_id: str
    scores: ScoreBreakdown
    time_spent: int  # in seconds
    validation_results: List[ValidationResult] = []
    feedback: Optional[FeedbackReport] = None


class ScoreResponse(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    scenario_id: str
    diagram_id: str
    scores: ScoreBreakdown
    time_spent: int
    submission_time: datetime
    validation_results: List[ValidationResult]
    feedback: Optional[FeedbackReport]

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class ScoreInDB(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    scenario_id: str
    diagram_id: str
    scores: ScoreBreakdown
    time_spent: int
    submission_time: datetime = Field(default_factory=datetime.utcnow)
    validation_results: List[ValidationResult] = []
    feedback: Optional[FeedbackReport] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class LeaderboardEntry(BaseModel):
    user_id: str
    user_name: str
    total_score: float
    scenarios_completed: int
    average_score: float
    rank: int


class UserStats(BaseModel):
    total_scenarios: int
    completed_scenarios: int
    average_score: float
    best_score: float
    total_time_spent: int
    current_streak: int
    badges_earned: List[str]