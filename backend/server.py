from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
import os
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

from routers import auth, scenarios, diagrams, scoring, learning, analytics, gamification
from database.connection import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


app = FastAPI(
    title="Threat Modeling Platform API",
    description="Interactive SaaS learning platform for threat modeling",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(scenarios.router, prefix="/api/scenarios", tags=["scenarios"])  
app.include_router(diagrams.router, prefix="/api/diagrams", tags=["diagrams"])
app.include_router(scoring.router, prefix="/api/scoring", tags=["scoring"])
app.include_router(learning.router, prefix="/api/learning", tags=["learning"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(gamification.router, prefix="/api/gamification", tags=["gamification"])

@app.get("/")
async def root():
    return {"message": "Threat Modeling Platform API", "status": "running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "threat-modeling-platform"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )