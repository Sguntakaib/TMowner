from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from .user import PyObjectId, ObjectId


class DiagramNode(BaseModel):
    id: str
    type: str
    position: Dict[str, float]  # {"x": float, "y": float}
    data: Dict[str, Any] = {}


class DiagramEdge(BaseModel):
    id: str
    source: str
    target: str
    type: str = "default"
    data: Dict[str, Any] = {}


class DiagramData(BaseModel):
    nodes: List[DiagramNode] = []
    edges: List[DiagramEdge] = []


class TrustBoundary(BaseModel):
    id: str
    name: str
    description: str
    nodes: List[str] = []  # Node IDs within this boundary


class DataFlow(BaseModel):
    id: str
    name: str
    description: str
    source_node: str
    target_node: str
    data_type: str
    encryption: bool = False
    protocol: Optional[str] = None


class SecurityControl(BaseModel):
    id: str
    name: str
    type: str  # authentication, authorization, encryption, etc.
    description: str
    applied_to: List[str] = []  # Node or edge IDs


class DiagramMetadata(BaseModel):
    trust_boundaries: List[TrustBoundary] = []
    data_flows: List[DataFlow] = []
    security_controls: List[SecurityControl] = []


class DiagramCreate(BaseModel):
    title: str
    scenario_id: Optional[str] = None
    diagram_data: DiagramData = DiagramData()
    metadata: DiagramMetadata = DiagramMetadata()


class DiagramUpdate(BaseModel):
    title: Optional[str] = None
    diagram_data: Optional[DiagramData] = None
    metadata: Optional[DiagramMetadata] = None


class DiagramResponse(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    scenario_id: Optional[str]
    title: str
    diagram_data: DiagramData
    metadata: DiagramMetadata
    status: str  # draft|submitted|reviewed
    created_at: datetime
    updated_at: datetime
    version: int

    model_config = ConfigDict(populate_by_name=True)
        
    @classmethod
    def from_dict(cls, data):
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)


class DiagramInDB(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    scenario_id: Optional[str] = None
    title: str
    diagram_data: DiagramData = DiagramData()
    metadata: DiagramMetadata = DiagramMetadata()
    status: str = "draft"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    version: int = 1

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


class CollaborationSession(BaseModel):
    diagram_id: str
    participants: List[str] = []  # User IDs
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)