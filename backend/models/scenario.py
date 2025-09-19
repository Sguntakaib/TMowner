from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ReferenceArchitecture(BaseModel):
    name: str
    diagram_data: Dict[str, Any]
    score_weight: float = 1.0


class ScenarioRequirements(BaseModel):
    business_context: str
    technical_constraints: List[str] = []
    required_elements: List[str] = []


class ScoringCriteria(BaseModel):
    security_weight: float = 0.3
    architecture_weight: float = 0.3
    performance_weight: float = 0.2
    completeness_weight: float = 0.2


class ScenarioCreate(BaseModel):
    title: str
    description: str
    category: str  # web|api|database|cloud|mobile
    difficulty: str  # beginner|intermediate|expert
    tags: List[str] = []
    requirements: ScenarioRequirements
    reference_architectures: List[ReferenceArchitecture] = []
    scoring_criteria: ScoringCriteria = ScoringCriteria()
    max_points: int = 100
    time_limit: Optional[int] = None  # in minutes
    prerequisites: List[str] = []


class ScenarioResponse(BaseModel):
    id: str = Field(alias="_id")
    title: str
    description: str
    category: str
    difficulty: str
    tags: List[str]
    requirements: ScenarioRequirements
    reference_architectures: List[ReferenceArchitecture]
    scoring_criteria: ScoringCriteria
    max_points: int
    time_limit: Optional[int]
    prerequisites: List[str]
    created_at: datetime
    updated_at: datetime
    published: bool
        
    @classmethod
    def from_dict(cls, data):
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)


class ScenarioInDB(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    description: str
    category: str
    difficulty: str
    tags: List[str] = []
    requirements: ScenarioRequirements
    reference_architectures: List[ReferenceArchitecture] = []
    scoring_criteria: ScoringCriteria = ScoringCriteria()
    max_points: int = 100
    time_limit: Optional[int] = None
    prerequisites: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    published: bool = False


class ScenarioFilter(BaseModel):
    category: Optional[str] = None
    difficulty: Optional[str] = None
    tags: Optional[List[str]] = None
    search: Optional[str] = None