from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from database.connection import get_database
from models.scenario import ScenarioCreate, ScenarioResponse, ScenarioFilter
from models.user import UserResponse
from routers.auth import get_current_user
from services.scenario_service import ScenarioService

router = APIRouter()


@router.get("/", response_model=List[ScenarioResponse])
async def get_scenarios(
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),  # Comma-separated tags
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100),
    current_user: UserResponse = Depends(get_current_user)
):
    """Get scenarios with filtering"""
    db = await get_database()
    scenario_service = ScenarioService(db)
    
    # Parse tags if provided
    tag_list = tags.split(",") if tags else None
    
    filter_params = ScenarioFilter(
        category=category,
        difficulty=difficulty,
        tags=tag_list,
        search=search
    )
    
    scenarios = await scenario_service.get_scenarios(filter_params, skip, limit)
    return scenarios


@router.get("/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(
    scenario_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get scenario by ID"""
    db = await get_database()
    scenario_service = ScenarioService(db)
    
    scenario = await scenario_service.get_scenario_by_id(scenario_id)
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    return scenario


@router.post("/", response_model=ScenarioResponse)
async def create_scenario(
    scenario_data: ScenarioCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Create a new scenario (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can create scenarios"
        )
    
    db = await get_database()
    scenario_service = ScenarioService(db)
    
    try:
        scenario = await scenario_service.create_scenario(scenario_data)
        return scenario
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create scenario"
        )


@router.put("/{scenario_id}", response_model=ScenarioResponse)
async def update_scenario(
    scenario_id: str,
    scenario_data: ScenarioCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Update scenario (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can update scenarios"
        )
    
    db = await get_database()
    scenario_service = ScenarioService(db)
    
    scenario = await scenario_service.update_scenario(scenario_id, scenario_data)
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    return scenario


@router.delete("/{scenario_id}")
async def delete_scenario(
    scenario_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Delete scenario (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can delete scenarios"
        )
    
    db = await get_database()
    scenario_service = ScenarioService(db)
    
    success = await scenario_service.delete_scenario(scenario_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    return {"message": "Scenario deleted successfully"}


@router.get("/categories/list")
async def get_categories(current_user: UserResponse = Depends(get_current_user)):
    """Get available scenario categories"""
    return {
        "categories": ["web", "api", "database", "cloud", "mobile", "network", "iot"]
    }


@router.get("/difficulties/list")
async def get_difficulties(current_user: UserResponse = Depends(get_current_user)):
    """Get available difficulty levels"""
    return {
        "difficulties": ["beginner", "intermediate", "expert"]
    }


@router.get("/{scenario_id}/progress")
async def get_scenario_progress(
    scenario_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get user's progress on a specific scenario"""
    db = await get_database()
    scenario_service = ScenarioService(db)
    
    progress = await scenario_service.get_user_scenario_progress(current_user.id, scenario_id)
    return progress