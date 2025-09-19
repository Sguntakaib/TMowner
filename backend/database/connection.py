from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from decouple import config

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def get_database():
    return db.db

async def connect_to_mongo():
    """Create database connection"""
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017/threat_modeling_platform")
    
    try:
        db.client = AsyncIOMotorClient(
            mongo_url,
            server_api=ServerApi('1'),
            maxPoolSize=10,
            minPoolSize=5,
            maxIdleTimeMS=45000,
            socketTimeoutMS=20000,
            connectTimeoutMS=20000,
        )
        
        # Get database name from URL or use default
        database_name = mongo_url.split('/')[-1] if '/' in mongo_url else "threat_modeling_platform"
        db.db = db.client[database_name]
        
        # Test the connection
        await db.client.admin.command('ping')
        print(f"✅ Connected to MongoDB: {database_name}")
        
    except Exception as e:
        print(f"❌ Could not connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("🔌 Disconnected from MongoDB")