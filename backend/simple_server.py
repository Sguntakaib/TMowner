from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI(
    title="Threat Modeling Platform API",
    description="Interactive SaaS learning platform for threat modeling",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Threat Modeling Platform API", "status": "running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "threat-modeling-platform"}

# Basic auth endpoints for frontend
@app.post("/api/auth/login")
async def login():
    # Mock response for now
    return {
        "user": {
            "id": "test123",
            "email": "test@example.com",
            "profile": {
                "first_name": "Test",
                "last_name": "User",
                "avatar_url": None,
                "bio": None
            },
            "role": "student",
            "progress": {
                "level": 1,
                "experience_points": 0,
                "completed_scenarios": [],
                "badges": []
            },
            "preferences": {
                "theme": "light",
                "notifications": True
            }
        },
        "access_token": "mock_token_12345",
        "token_type": "bearer"
    }

@app.post("/api/auth/register")
async def register():
    # Mock response for now
    return {
        "user": {
            "id": "test123",
            "email": "test@example.com",
            "profile": {
                "first_name": "Test",
                "last_name": "User",
                "avatar_url": None,
                "bio": None
            },
            "role": "student",
            "progress": {
                "level": 1,
                "experience_points": 0,
                "completed_scenarios": [],
                "badges": []
            },
            "preferences": {
                "theme": "light",
                "notifications": True
            }
        },
        "access_token": "mock_token_12345",
        "token_type": "bearer"
    }

@app.get("/api/auth/verify")
async def verify():
    # Mock response for now
    return {
        "user": {
            "id": "test123",
            "email": "test@example.com",
            "profile": {
                "first_name": "Test",
                "last_name": "User",
                "avatar_url": None,
                "bio": None
            },
            "role": "student",
            "progress": {
                "level": 1,
                "experience_points": 0,
                "completed_scenarios": [],
                "badges": []
            },
            "preferences": {
                "theme": "light",
                "notifications": True
            }
        }
    }

@app.get("/api/scenarios/")
async def get_scenarios():
    # Mock scenarios data
    return [
        {
            "id": "scenario1",
            "title": "Web Application Security Assessment",
            "description": "Design a secure architecture for a web application with user authentication, data storage, and API endpoints.",
            "category": "web",
            "difficulty": "beginner",
            "tags": ["authentication", "web security", "API"],
            "requirements": {
                "business_context": "A startup needs a secure web application for user management",
                "technical_constraints": ["Must support 1000+ concurrent users", "GDPR compliance required"],
                "required_elements": ["Web Server", "Database", "Load Balancer", "Authentication Service"]
            },
            "scoring_criteria": {
                "security_weight": 0.4,
                "architecture_weight": 0.3,
                "performance_weight": 0.2,
                "completeness_weight": 0.1
            },
            "max_points": 100,
            "time_limit": 60,
            "prerequisites": [],
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "published": True,
            "reference_architectures": []
        },
        {
            "id": "scenario2", 
            "title": "Cloud Infrastructure Security",
            "description": "Design a secure cloud infrastructure for a microservices architecture with proper network segmentation.",
            "category": "cloud",
            "difficulty": "intermediate",
            "tags": ["cloud", "microservices", "network security"],
            "requirements": {
                "business_context": "Enterprise migration to cloud with multiple services",
                "technical_constraints": ["Multi-region deployment", "Zero-trust network"],
                "required_elements": ["API Gateway", "Service Mesh", "Container Registry", "Identity Provider"]
            },
            "scoring_criteria": {
                "security_weight": 0.4,
                "architecture_weight": 0.3,
                "performance_weight": 0.2,
                "completeness_weight": 0.1
            },
            "max_points": 100,
            "time_limit": 90,
            "prerequisites": [],
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "published": True,
            "reference_architectures": []
        }
    ]

@app.get("/api/scoring/stats")
async def get_stats():
    return {
        "completed_scenarios": 0,
        "average_score": 0.0,
        "badges_earned": [],
        "current_streak": 0
    }

@app.get("/api/scoring/history")
async def get_score_history():
    return []

@app.get("/api/learning/recommendations")
async def get_recommendations():
    return {
        "recommendations": [
            {
                "title": "Start with Web Security Basics",
                "description": "Learn fundamental web application security concepts"
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "simple_server:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )