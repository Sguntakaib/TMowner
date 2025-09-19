from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Threat Modeling Platform API - Test",
    description="Test server to verify basic functionality",
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
    return {"message": "Test Threat Modeling Platform API", "status": "running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "threat-modeling-platform-test"}

if __name__ == "__main__":
    uvicorn.run(
        "test_server:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )