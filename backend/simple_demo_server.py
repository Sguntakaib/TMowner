from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
from datetime import datetime, timedelta
import random
import uvicorn

app = FastAPI(title="Threat Modeling Platform Demo API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Sample data for demo
sample_user = {
    "id": "demo_user_123",
    "email": "demo@example.com",
    "profile": {
        "first_name": "Demo",
        "last_name": "User"
    }
}

# Mock validation results
def generate_validation_results():
    results = []
    
    # Security issues
    results.append({
        "rule_id": "SEC001",
        "rule_name": "Missing Authentication",
        "severity": "error",
        "message": "No authentication mechanism detected. All systems need user authentication.",
        "category": "security",
        "element_type": "system"
    })
    
    results.append({
        "rule_id": "SEC002", 
        "rule_name": "Unencrypted Communication",
        "severity": "warning",
        "message": "Found unencrypted connections. Use HTTPS/TLS for all communications.",
        "category": "security",
        "element_type": "connection"
    })
    
    # Architecture issues
    results.append({
        "rule_id": "ARCH001",
        "rule_name": "Separation of Concerns",
        "severity": "error",
        "message": "Frontend should not connect directly to database",
        "category": "architecture",
        "element_type": "system"
    })
    
    # Performance suggestions
    results.append({
        "rule_id": "PERF001",
        "rule_name": "Missing Load Balancer",
        "severity": "info",
        "message": "Consider adding load balancing for scalability",
        "category": "performance",
        "element_type": "system"
    })
    
    return random.sample(results, random.randint(2, 4))

# Mock analytics data
def generate_analytics_data():
    return {
        "performance_overview": {
            "current_level": "Intermediate",
            "total_scenarios": 15,
            "average_score": 78.5,
            "best_score": 94.2,
            "improvement_rate": 12.3,
            "performance_trend": "improving"
        },
        "skill_radar": {
            "security": 82.0,
            "architecture": 76.5,
            "performance": 71.2,
            "completeness": 85.3,
            "overall": 78.8
        },
        "learning_velocity": {
            "scenarios_per_week": 3.2,
            "velocity_trend": "accelerating",
            "projection": {
                "next_week_scenarios": 4,
                "confidence": "high"
            }
        },
        "improvement_trends": {
            "security": {
                "early_average": 65.2,
                "recent_average": 82.0,
                "improvement": 16.8,
                "trend": "improving"
            },
            "architecture": {
                "early_average": 70.1,
                "recent_average": 76.5,
                "improvement": 6.4,
                "trend": "improving"
            }
        }
    }

# Mock achievements data
def generate_achievements_data():
    badges = [
        {
            "badge_id": "first_steps",
            "name": "First Steps",
            "description": "Complete your first threat modeling scenario",
            "icon": "🎯",
            "tier": "bronze",
            "earned": True,
            "earned_at": "2023-09-15T10:30:00Z"
        },
        {
            "badge_id": "high_scorer",
            "name": "High Scorer",
            "description": "Achieve a score of 90 or higher", 
            "icon": "🏆",
            "tier": "silver",
            "earned": True,
            "earned_at": "2023-09-18T14:22:00Z"
        },
        {
            "badge_id": "security_expert",
            "name": "Security Expert",
            "description": "Consistently high security scores",
            "icon": "🔒",
            "tier": "gold",
            "earned": False,
            "progress": {
                "current": 78.2,
                "target": 85.0,
                "percentage": 92.0
            }
        },
        {
            "badge_id": "perfectionist",
            "name": "Perfectionist",
            "description": "Achieve a perfect score of 100",
            "icon": "💯",
            "tier": "platinum",
            "earned": False,
            "progress": {
                "current": 94.2,
                "target": 100.0,
                "percentage": 94.2
            }
        }
    ]
    
    return {
        "earned_badges": 2,
        "total_badges": 4,
        "completion_percentage": 50.0,
        "badges": badges,
        "user_level": {
            "current_level": 3,
            "experience_points": 1250,
            "progress_percentage": 75.0
        },
        "experience_points": 1250
    }

# API Routes
@app.get("/")
async def root():
    return {"message": "Threat Modeling Platform Demo API", "status": "running"}

@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "threat-modeling-platform-demo"}

# Auth endpoints
@app.post("/api/auth/login")
async def login(credentials: dict):
    return {
        "message": "Login successful",
        "user": sample_user,
        "access_token": "demo_token_123",
        "token_type": "bearer"
    }

@app.get("/api/auth/profile")
async def get_profile():
    return sample_user

# Scoring endpoints
@app.post("/api/scoring/validate")
async def validate_diagram(request: dict):
    diagram_id = request.get("diagram_id", "demo_diagram")
    return {
        "diagram_id": diagram_id,
        "validation_results": generate_validation_results(),
        "timestamp": datetime.utcnow().isoformat()
    }

# Analytics endpoints
@app.get("/api/analytics/dashboard")
async def get_analytics_dashboard():
    return {
        "user_id": sample_user["id"],
        "analysis_period_days": 90,
        "analytics": generate_analytics_data(),
        "generated_at": datetime.utcnow().isoformat()
    }

@app.get("/api/analytics/skill-radar-data")
async def get_skill_radar():
    analytics = generate_analytics_data()
    return {
        "radar_data": analytics["skill_radar"],
        "data_points": 15,
        "period": "recent"
    }

@app.get("/api/analytics/learning-insights")
async def get_learning_insights():
    return {
        "insights": [
            "📈 Your performance is improving consistently!",
            "💪 Your strongest area is Completeness (85.3%)",
            "🎯 Focus on improving Performance (71.2%)",
            "⚡ You're completing scenarios efficiently!"
        ],
        "recommendations": [
            "Practice scenarios that emphasize performance skills",
            "Try scenarios in your focus areas",
            "Review feedback from previous attempts"
        ],
        "focus_areas": ["Performance"],
        "next_steps": [
            "Try scenarios in your focus areas",
            "Review feedback from previous attempts", 
            "Challenge yourself with harder scenarios"
        ],
        "performance_summary": {
            "total_attempts": 15,
            "average_score": 78.5,
            "skill_breakdown": {
                "Security": 82.0,
                "Architecture": 76.5,
                "Performance": 71.2,
                "Completeness": 85.3
            }
        }
    }

@app.get("/api/analytics/performance-timeline")
async def get_performance_timeline():
    timeline = []
    base_date = datetime.utcnow() - timedelta(days=30)
    
    for i in range(15):
        date = base_date + timedelta(days=i*2)
        timeline.append({
            "date": date.isoformat(),
            "total_score": random.randint(60, 95),
            "security_score": random.randint(70, 90),
            "architecture_score": random.randint(65, 85),
            "performance_score": random.randint(60, 80),
            "completeness_score": random.randint(75, 95),
            "attempt_number": i + 1,
            "time_spent_minutes": random.randint(15, 45)
        })
    
    return {
        "user_id": sample_user["id"],
        "timeline": timeline,
        "total_attempts": len(timeline)
    }

# Gamification endpoints
@app.get("/api/gamification/achievements")
async def get_achievements():
    return {
        "user_id": sample_user["id"],
        "achievements": generate_achievements_data(),
        "last_updated": datetime.utcnow().isoformat()
    }

@app.post("/api/gamification/check-achievements")
async def check_achievements():
    # Sometimes return new achievements
    new_achievements = []
    if random.random() > 0.7:  # 30% chance of new achievement
        new_achievements.append({
            "badge_id": "consistent_performer",
            "name": "Consistent Performer"
        })
    
    return {
        "user_id": sample_user["id"],
        "new_achievements": new_achievements,
        "total_new": len(new_achievements),
        "checked_at": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")