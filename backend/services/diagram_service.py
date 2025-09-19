from motor.motor_asyncio import AsyncIOMotorDatabase
from models.diagram import DiagramCreate, DiagramUpdate, DiagramResponse, DiagramInDB
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from utils.database import convert_doc_to_dict, convert_docs_to_list


class DiagramService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.diagrams

    async def create_diagram(self, user_id: str, diagram_data: DiagramCreate) -> DiagramResponse:
        """Create a new diagram"""
        diagram_dict = diagram_data.dict()
        diagram_dict["user_id"] = user_id
        
        diagram_in_db = DiagramInDB(**diagram_dict)
        
        result = await self.collection.insert_one(diagram_in_db.dict(by_alias=True))
        created_diagram = await self.collection.find_one({"_id": result.inserted_id})
        
        # Convert ObjectId to string before creating response
        created_diagram = convert_doc_to_dict(created_diagram)
        return DiagramResponse(**created_diagram)

    async def get_user_diagrams(self, user_id: str, scenario_id: Optional[str] = None, 
                               skip: int = 0, limit: int = 20) -> List[DiagramResponse]:
        """Get user's diagrams"""
        query = {"user_id": user_id}
        
        if scenario_id:
            query["scenario_id"] = scenario_id
        
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("updated_at", -1)
        diagrams = await cursor.to_list(length=limit)
        
        # Convert ObjectIds to strings
        diagrams = convert_docs_to_list(diagrams)
        return [DiagramResponse(**diagram) for diagram in diagrams]

    async def get_diagram_by_id(self, diagram_id: str) -> Optional[DiagramResponse]:
        """Get diagram by ID"""
        try:
            diagram = await self.collection.find_one({"_id": ObjectId(diagram_id)})
            if diagram:
                diagram = convert_doc_to_dict(diagram)
                return DiagramResponse(**diagram)
        except Exception:
            pass
        return None

    async def update_diagram(self, diagram_id: str, diagram_data: DiagramUpdate) -> Optional[DiagramResponse]:
        """Update diagram"""
        try:
            update_data = {}
            
            # Only update provided fields
            if diagram_data.title is not None:
                update_data["title"] = diagram_data.title
            
            if diagram_data.diagram_data is not None:
                update_data["diagram_data"] = diagram_data.diagram_data.dict()
            
            if diagram_data.metadata is not None:
                update_data["metadata"] = diagram_data.metadata.dict()
            
            update_data["updated_at"] = datetime.utcnow()
            update_data["version"] = {"$inc": 1}  # Increment version
            
            if update_data:
                result = await self.collection.update_one(
                    {"_id": ObjectId(diagram_id)},
                    {"$set": update_data, "$inc": {"version": 1}}
                )
                
                if result.modified_count:
                    updated_diagram = await self.collection.find_one({"_id": ObjectId(diagram_id)})
                    return DiagramResponse(**updated_diagram)
        except Exception:
            pass
        return None

    async def delete_diagram(self, diagram_id: str) -> bool:
        """Delete diagram"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(diagram_id)})
            return result.deleted_count > 0
        except Exception:
            return False

    async def submit_diagram(self, diagram_id: str) -> Optional[DiagramResponse]:
        """Submit diagram for scoring"""
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(diagram_id)},
                {"$set": {"status": "submitted", "updated_at": datetime.utcnow()}}
            )
            
            if result.modified_count:
                submitted_diagram = await self.collection.find_one({"_id": ObjectId(diagram_id)})
                return DiagramResponse(**submitted_diagram)
        except Exception:
            pass
        return None

    async def duplicate_diagram(self, diagram_id: str, new_user_id: str) -> Optional[DiagramResponse]:
        """Duplicate an existing diagram"""
        try:
            original_diagram = await self.collection.find_one({"_id": ObjectId(diagram_id)})
            if not original_diagram:
                return None
            
            # Create new diagram data
            new_diagram = DiagramInDB(
                user_id=new_user_id,
                scenario_id=original_diagram.get("scenario_id"),
                title=f"{original_diagram['title']} (Copy)",
                diagram_data=original_diagram["diagram_data"],
                metadata=original_diagram["metadata"],
                status="draft"
            )
            
            result = await self.collection.insert_one(new_diagram.dict(by_alias=True))
            duplicated_diagram = await self.collection.find_one({"_id": result.inserted_id})
            
            return DiagramResponse(**duplicated_diagram)
        except Exception:
            pass
        return None

    async def get_diagram_collaborators(self, diagram_id: str) -> List[str]:
        """Get list of users collaborating on a diagram"""
        # This would integrate with WebSocket sessions
        # For now, return empty list
        return []

    async def save_diagram_version(self, diagram_id: str, version_data: dict) -> bool:
        """Save a version of the diagram for history"""
        try:
            versions_collection = self.db.diagram_versions
            
            diagram = await self.collection.find_one({"_id": ObjectId(diagram_id)})
            if not diagram:
                return False
            
            version_doc = {
                "diagram_id": diagram_id,
                "version": diagram["version"],
                "diagram_data": diagram["diagram_data"],
                "metadata": diagram["metadata"],
                "created_at": datetime.utcnow(),
                "created_by": diagram["user_id"]
            }
            
            await versions_collection.insert_one(version_doc)
            return True
        except Exception:
            return False