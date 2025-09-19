from motor.motor_asyncio import AsyncIOMotorDatabase
from models.scenario import ScenarioCreate, ScenarioResponse, ScenarioInDB, ScenarioFilter
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


class ScenarioService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.scenarios

    async def create_scenario(self, scenario_data: ScenarioCreate) -> ScenarioResponse:
        """Create a new scenario"""
        scenario_dict = scenario_data.dict()
        scenario_in_db = ScenarioInDB(**scenario_dict)
        
        result = await self.collection.insert_one(scenario_in_db.dict(by_alias=True))
        created_scenario = await self.collection.find_one({"_id": result.inserted_id})
        
        return ScenarioResponse.from_dict(created_scenario)

    async def get_scenarios(self, filters: ScenarioFilter, skip: int = 0, limit: int = 50) -> List[ScenarioResponse]:
        """Get scenarios with filtering"""
        query = {"published": True}
        
        # Apply filters
        if filters.category:
            query["category"] = filters.category
        
        if filters.difficulty:
            query["difficulty"] = filters.difficulty
        
        if filters.tags:
            query["tags"] = {"$in": filters.tags}
        
        if filters.search:
            query["$or"] = [
                {"title": {"$regex": filters.search, "$options": "i"}},
                {"description": {"$regex": filters.search, "$options": "i"}},
                {"tags": {"$in": [filters.search]}}
            ]
        
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
        scenarios = await cursor.to_list(length=limit)
        
        return [ScenarioResponse.from_dict(scenario) for scenario in scenarios]

    async def get_scenario_by_id(self, scenario_id: str) -> Optional[ScenarioResponse]:
        """Get scenario by ID"""
        try:
            scenario = await self.collection.find_one({"_id": ObjectId(scenario_id)})
            if scenario:
                return ScenarioResponse.from_dict(scenario)
        except Exception:
            pass
        return None

    async def update_scenario(self, scenario_id: str, scenario_data: ScenarioCreate) -> Optional[ScenarioResponse]:
        """Update scenario"""
        try:
            update_data = scenario_data.dict()
            update_data["updated_at"] = datetime.utcnow()
            
            result = await self.collection.update_one(
                {"_id": ObjectId(scenario_id)},
                {"$set": update_data}
            )
            
            if result.modified_count:
                updated_scenario = await self.collection.find_one({"_id": ObjectId(scenario_id)})
                return ScenarioResponse.from_dict(updated_scenario)
        except Exception:
            pass
        return None

    async def delete_scenario(self, scenario_id: str) -> bool:
        """Delete scenario"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(scenario_id)})
            return result.deleted_count > 0
        except Exception:
            return False

    async def get_user_scenario_progress(self, user_id: str, scenario_id: str) -> dict:
        """Get user's progress on a specific scenario"""
        # Get user's attempts and scores for this scenario
        scores_collection = self.db.scores
        diagrams_collection = self.db.diagrams
        
        # Get all attempts
        attempts = await scores_collection.find({
            "user_id": user_id,
            "scenario_id": scenario_id
        }).sort("submission_time", -1).to_list(length=None)
        
        # Get saved diagrams
        saved_diagrams = await diagrams_collection.find({
            "user_id": user_id,
            "scenario_id": scenario_id
        }).to_list(length=None)
        
        best_score = 0
        if attempts:
            best_score = max(attempt["scores"]["total_score"] for attempt in attempts)
        
        return {
            "scenario_id": scenario_id,
            "attempts": len(attempts),
            "best_score": best_score,
            "saved_diagrams": len(saved_diagrams),
            "completed": best_score > 70,  # Consider 70+ as completed
            "last_attempt": attempts[0]["submission_time"] if attempts else None
        }