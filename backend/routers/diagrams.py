from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from database.connection import get_database
from models.diagram import DiagramCreate, DiagramUpdate, DiagramResponse
from models.user import UserResponse
from routers.auth import get_current_user
from services.diagram_service import DiagramService

router = APIRouter()


@router.get("/", response_model=List[DiagramResponse])
async def get_diagrams(
    scenario_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=50),
    current_user: UserResponse = Depends(get_current_user)
):
    """Get user's diagrams"""
    db = await get_database()
    diagram_service = DiagramService(db)
    
    diagrams = await diagram_service.get_user_diagrams(
        current_user.id, scenario_id, skip, limit
    )
    return diagrams


@router.get("/{diagram_id}", response_model=DiagramResponse)
async def get_diagram(
    diagram_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get diagram by ID"""
    db = await get_database()
    diagram_service = DiagramService(db)
    
    diagram = await diagram_service.get_diagram_by_id(diagram_id)
    if not diagram:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagram not found"
        )
    
    # Check if user owns the diagram or has permission
    if diagram.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return diagram


@router.post("/", response_model=DiagramResponse)
async def create_diagram(
    diagram_data: DiagramCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Create a new diagram"""
    db = await get_database()
    diagram_service = DiagramService(db)
    
    try:
        diagram = await diagram_service.create_diagram(current_user.id, diagram_data)
        return diagram
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create diagram"
        )


@router.put("/{diagram_id}", response_model=DiagramResponse)
async def update_diagram(
    diagram_id: str,
    diagram_data: DiagramUpdate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Update diagram"""
    db = await get_database()
    diagram_service = DiagramService(db)
    
    # Check ownership
    existing_diagram = await diagram_service.get_diagram_by_id(diagram_id)
    if not existing_diagram:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagram not found"
        )
    
    if existing_diagram.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    diagram = await diagram_service.update_diagram(diagram_id, diagram_data)
    if not diagram:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update diagram"
        )
    
    return diagram


@router.delete("/{diagram_id}")
async def delete_diagram(
    diagram_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Delete diagram"""
    db = await get_database()
    diagram_service = DiagramService(db)
    
    # Check ownership
    existing_diagram = await diagram_service.get_diagram_by_id(diagram_id)
    if not existing_diagram:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagram not found"
        )
    
    if existing_diagram.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    success = await diagram_service.delete_diagram(diagram_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete diagram"
        )
    
    return {"message": "Diagram deleted successfully"}


@router.post("/{diagram_id}/submit")
async def submit_diagram(
    diagram_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Submit diagram for scoring"""
    db = await get_database()
    diagram_service = DiagramService(db)
    
    # Check ownership
    diagram = await diagram_service.get_diagram_by_id(diagram_id)
    if not diagram:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagram not found"
        )
    
    if diagram.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update status to submitted
    updated_diagram = await diagram_service.submit_diagram(diagram_id)
    if not updated_diagram:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit diagram"
        )
    
    return {
        "message": "Diagram submitted successfully",
        "diagram": updated_diagram
    }


@router.post("/{diagram_id}/duplicate", response_model=DiagramResponse)
async def duplicate_diagram(
    diagram_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Duplicate an existing diagram"""
    db = await get_database()
    diagram_service = DiagramService(db)
    
    diagram = await diagram_service.get_diagram_by_id(diagram_id)
    if not diagram:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagram not found"
        )
    
    # Check if user has access (own diagram or public)
    if diagram.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    duplicated_diagram = await diagram_service.duplicate_diagram(diagram_id, current_user.id)
    if not duplicated_diagram:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to duplicate diagram"
        )
    
    return duplicated_diagram