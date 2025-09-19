#!/usr/bin/env python3
"""
Script to create sample data for the threat modeling platform
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os

# MongoDB connection
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/threat_modeling_platform")

sample_scenarios = [
    {
        "title": "E-commerce Web Application",
        "description": "Design a secure e-commerce platform with user authentication, product catalog, shopping cart, and payment processing. Consider data protection, secure transactions, and scalability.",
        "category": "web",
        "difficulty": "beginner",
        "tags": ["authentication", "payment", "data-protection", "web-security"],
        "requirements": {
            "business_context": "You are designing an online store that sells consumer electronics. The system needs to handle user registration, product browsing, shopping cart functionality, and secure payment processing. The expected user base is 10,000 monthly active users.",
            "technical_constraints": [
                "Must comply with PCI DSS for payment processing",
                "User data must be encrypted at rest and in transit",
                "System must handle 1000 concurrent users",
                "Must integrate with external payment gateway"
            ],
            "required_elements": [
                "Web frontend (React/Angular)",
                "API gateway",
                "Authentication service",
                "Product database",
                "Payment processing service",
                "Load balancer"
            ]
        },
        "reference_architectures": [
            {
                "name": "Secure E-commerce Architecture",
                "diagram_data": {
                    "nodes": [
                        {"id": "frontend", "type": "frontend", "position": {"x": 100, "y": 100}},
                        {"id": "api", "type": "api", "position": {"x": 300, "y": 100}},
                        {"id": "auth", "type": "security", "position": {"x": 500, "y": 50}},
                        {"id": "db", "type": "database", "position": {"x": 500, "y": 150}}
                    ],
                    "edges": [
                        {"id": "e1", "source": "frontend", "target": "api"},
                        {"id": "e2", "source": "api", "target": "auth"},
                        {"id": "e3", "source": "api", "target": "db"}
                    ]
                },
                "score_weight": 1.0
            }
        ],
        "scoring_criteria": {
            "security_weight": 0.4,
            "architecture_weight": 0.3,
            "performance_weight": 0.2,
            "completeness_weight": 0.1
        },
        "max_points": 100,
        "time_limit": 45,
        "prerequisites": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "published": True
    },
    {
        "title": "Microservices API Architecture",
        "description": "Design a microservices-based API system with service discovery, load balancing, and inter-service communication. Focus on security between services and data consistency.",
        "category": "api",
        "difficulty": "intermediate",
        "tags": ["microservices", "api-security", "service-mesh", "scalability"],
        "requirements": {
            "business_context": "Design a backend system for a social media platform with user management, content posting, notifications, and messaging services. The system should be highly scalable and maintainable.",
            "technical_constraints": [
                "Services must communicate securely",
                "Must implement circuit breaker pattern",
                "API rate limiting required",
                "Distributed tracing for monitoring"
            ],
            "required_elements": [
                "API Gateway",
                "User Service",
                "Content Service", 
                "Notification Service",
                "Message Queue",
                "Service Discovery",
                "Load Balancer"
            ]
        },
        "reference_architectures": [],
        "scoring_criteria": {
            "security_weight": 0.35,
            "architecture_weight": 0.4,
            "performance_weight": 0.15,
            "completeness_weight": 0.1
        },
        "max_points": 120,
        "time_limit": 60,
        "prerequisites": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "published": True
    },
    {
        "title": "Cloud Infrastructure Security",
        "description": "Design a secure cloud infrastructure with proper network segmentation, identity management, and data protection. Consider multi-region deployment and disaster recovery.",
        "category": "cloud",
        "difficulty": "expert",
        "tags": ["cloud-security", "network-segmentation", "identity-management", "disaster-recovery"],
        "requirements": {
            "business_context": "Design cloud infrastructure for a financial services company that needs to comply with regulatory requirements while maintaining high availability and performance.",
            "technical_constraints": [
                "Must comply with SOC 2 and PCI DSS",
                "Multi-region deployment required",
                "Zero-trust network architecture",
                "Automated backup and disaster recovery"
            ],
            "required_elements": [
                "Virtual Private Cloud (VPC)",
                "Identity and Access Management (IAM)",
                "Network Security Groups",
                "Load Balancers",
                "Database clusters",
                "Monitoring and logging",
                "Backup systems"
            ]
        },
        "reference_architectures": [],
        "scoring_criteria": {
            "security_weight": 0.5,
            "architecture_weight": 0.25,
            "performance_weight": 0.15,
            "completeness_weight": 0.1
        },
        "max_points": 150,
        "time_limit": 90,
        "prerequisites": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "published": True
    }
]

async def create_sample_data():
    """Create sample scenarios in the database"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.threat_modeling_platform
    
    try:
        # Clear existing scenarios
        await db.scenarios.delete_many({})
        print("Cleared existing scenarios")
        
        # Insert sample scenarios
        result = await db.scenarios.insert_many(sample_scenarios)
        print(f"Created {len(result.inserted_ids)} sample scenarios")
        
        # Print scenario IDs for reference
        for i, scenario_id in enumerate(result.inserted_ids):
            print(f"  - {sample_scenarios[i]['title']}: {scenario_id}")
            
    except Exception as e:
        print(f"Error creating sample data: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(create_sample_data())