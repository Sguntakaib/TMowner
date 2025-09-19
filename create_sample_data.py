import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import hashlib
import uuid

# Mock data for testing
SAMPLE_SCENARIOS = [
    {
        "_id": "scenario_001",
        "title": "Web Application Security Assessment",
        "description": "Design a secure architecture for an e-commerce web application. You need to consider user authentication, payment processing, data protection, and protection against common web vulnerabilities like XSS, CSRF, and SQL injection.",
        "category": "web",
        "difficulty": "beginner",
        "tags": ["authentication", "web security", "e-commerce", "payment", "XSS", "CSRF"],
        "requirements": {
            "business_context": "A startup is launching an e-commerce platform that needs to handle user registrations, product catalog, shopping cart, and secure payment processing. The platform expects 10,000+ users in the first year.",
            "technical_constraints": [
                "Must support 1000+ concurrent users",
                "PCI DSS compliance for payment processing",
                "GDPR compliance for EU users",
                "Maximum 3-second page load time",
                "99.9% uptime requirement"
            ],
            "required_elements": [
                "Web Application Server",
                "Database Server", 
                "Payment Gateway",
                "Load Balancer",
                "Authentication Service",
                "Content Delivery Network"
            ]
        },
        "reference_architectures": [
            {
                "name": "Standard Web Application Architecture",
                "description": "A typical 3-tier web architecture with security controls",
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
        "time_limit": 60,
        "prerequisites": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "published": True
    },
    {
        "_id": "scenario_002",
        "title": "Cloud Infrastructure Security",
        "description": "Design a secure cloud infrastructure for a microservices architecture. Focus on container security, service mesh implementation, zero-trust networking, and proper identity and access management across multiple services.",
        "category": "cloud",
        "difficulty": "intermediate",
        "tags": ["cloud", "microservices", "containers", "service mesh", "zero-trust", "kubernetes"],
        "requirements": {
            "business_context": "A financial services company is migrating their monolithic application to a cloud-native microservices architecture. They need to maintain strict security and compliance requirements while improving scalability and deployment velocity.",
            "technical_constraints": [
                "Multi-region deployment for disaster recovery",
                "Zero-trust network architecture",
                "Container security scanning and runtime protection",
                "Centralized logging and monitoring",
                "Automated security policy enforcement"
            ],
            "required_elements": [
                "Container Registry",
                "Kubernetes Cluster",
                "Service Mesh (Istio/Linkerd)",
                "API Gateway",
                "Identity Provider",
                "Security Scanner",
                "Monitoring System",
                "Log Aggregation Service"
            ]
        },
        "reference_architectures": [
            {
                "name": "Cloud-Native Security Architecture",
                "description": "Secure microservices deployment with defense in depth",
                "score_weight": 1.0
            }
        ],
        "scoring_criteria": {
            "security_weight": 0.45,
            "architecture_weight": 0.35,
            "performance_weight": 0.15,
            "completeness_weight": 0.05
        },
        "max_points": 120,
        "time_limit": 90,
        "prerequisites": ["scenario_001"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "published": True
    },
    {
        "_id": "scenario_003",
        "title": "API Security and OAuth Implementation",
        "description": "Design a comprehensive API security architecture implementing OAuth 2.0, rate limiting, input validation, and protection against API-specific attacks like injection, broken authentication, and excessive data exposure.",
        "category": "api",
        "difficulty": "intermediate",
        "tags": ["API security", "OAuth 2.0", "rate limiting", "input validation", "JWT"],
        "requirements": {
            "business_context": "A SaaS company provides APIs for third-party integrations. They need to secure their APIs while maintaining ease of integration for partners and protecting against various API security threats.",
            "technical_constraints": [
                "Support for multiple OAuth 2.0 flows",
                "Rate limiting per client and endpoint",
                "Comprehensive request/response validation",
                "API versioning and backward compatibility",
                "Real-time threat detection and blocking"
            ],
            "required_elements": [
                "API Gateway",
                "OAuth Authorization Server",
                "Rate Limiting Service",
                "Input Validation Engine",
                "Web Application Firewall",
                "API Analytics Platform",
                "Token Management Service"
            ]
        },
        "reference_architectures": [
            {
                "name": "Enterprise API Security Architecture",
                "description": "Comprehensive API security with OAuth 2.0 and threat protection",
                "score_weight": 1.0
            }
        ],
        "scoring_criteria": {
            "security_weight": 0.5,
            "architecture_weight": 0.25,
            "performance_weight": 0.15,
            "completeness_weight": 0.1
        },
        "max_points": 110,
        "time_limit": 75,
        "prerequisites": ["scenario_001"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "published": True
    },
    {
        "_id": "scenario_004",
        "title": "Database Security and Encryption",
        "description": "Design a secure database architecture with encryption at rest and in transit, proper access controls, data masking, backup security, and protection against database-specific attacks.",
        "category": "database",
        "difficulty": "expert",
        "tags": ["database security", "encryption", "access control", "data masking", "backup"],
        "requirements": {
            "business_context": "A healthcare organization needs to secure patient data across multiple databases while ensuring HIPAA compliance, maintaining high availability, and enabling secure data analytics.",
            "technical_constraints": [
                "HIPAA compliance for patient data",
                "Encryption at rest and in transit",
                "Granular access control and audit logging",
                "Secure backup and disaster recovery",
                "Data masking for non-production environments"
            ],
            "required_elements": [
                "Primary Database Cluster",
                "Database Firewall",
                "Key Management Service",
                "Access Control Manager",
                "Audit Logging Service",
                "Backup and Recovery System",
                "Data Masking Engine"
            ]
        },
        "reference_architectures": [
            {
                "name": "Healthcare Database Security Architecture",
                "description": "HIPAA-compliant database security with comprehensive controls",
                "score_weight": 1.0
            }
        ],
        "scoring_criteria": {
            "security_weight": 0.6,
            "architecture_weight": 0.2,
            "performance_weight": 0.1,
            "completeness_weight": 0.1
        },
        "max_points": 130,
        "time_limit": 120,
        "prerequisites": ["scenario_001", "scenario_002"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "published": True
    },
    {
        "_id": "scenario_005",
        "title": "Mobile Application Security",
        "description": "Design security architecture for a mobile banking application including device security, secure communication, biometric authentication, and protection against mobile-specific threats.",
        "category": "mobile",
        "difficulty": "expert",
        "tags": ["mobile security", "banking", "biometrics", "device security", "SSL pinning"],
        "requirements": {
            "business_context": "A bank is developing a mobile application for customer banking services. The app needs to handle sensitive financial transactions while providing a seamless user experience and protecting against mobile threats.",
            "technical_constraints": [
                "Biometric authentication support",
                "Certificate pinning for API calls",
                "Root/jailbreak detection",
                "End-to-end encryption for transactions",
                "Offline capability with security"
            ],
            "required_elements": [
                "Mobile Application",
                "Mobile Device Management",
                "Biometric Authentication Service",
                "Certificate Authority",
                "Mobile Application Firewall",
                "Fraud Detection System",
                "Secure Element/Hardware Security Module"
            ]
        },
        "reference_architectures": [
            {
                "name": "Mobile Banking Security Architecture",
                "description": "Comprehensive mobile banking security with device and transaction protection",
                "score_weight": 1.0
            }
        ],
        "scoring_criteria": {
            "security_weight": 0.55,
            "architecture_weight": 0.25,
            "performance_weight": 0.1,
            "completeness_weight": 0.1
        },
        "max_points": 140,
        "time_limit": 150,
        "prerequisites": ["scenario_001", "scenario_003"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "published": True
    }
]

async def create_sample_data():
    """Create sample data for testing the threat modeling platform"""
    
    # Connect to MongoDB
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017/threat_modeling_platform")
    client = AsyncIOMotorClient(mongo_url)
    
    # Get database name from URL
    database_name = mongo_url.split('/')[-1] if '/' in mongo_url else "threat_modeling_platform"
    db = client[database_name]
    
    try:
        print("🚀 Creating sample data for Threat Modeling Platform...")
        
        # Create scenarios
        scenarios_collection = db.scenarios
        
        # Clear existing scenarios
        await scenarios_collection.delete_many({})
        
        # Insert sample scenarios
        result = await scenarios_collection.insert_many(SAMPLE_SCENARIOS)
        print(f"✅ Created {len(result.inserted_ids)} sample scenarios")
        
        # Create sample user
        users_collection = db.users
        
        # Clear existing test users
        await users_collection.delete_many({"email": {"$regex": "test"}})
        
        # Create admin user
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        admin_user = {
            "_id": str(uuid.uuid4()),
            "email": "admin@threatmodeling.com",
            "password_hash": pwd_context.hash("admin123"),
            "profile": {
                "first_name": "System",
                "last_name": "Administrator",
                "avatar_url": None,
                "bio": "Platform Administrator"
            },
            "role": "admin",
            "created_at": datetime.utcnow(),
            "last_login": None,
            "preferences": {
                "theme": "light",
                "notifications": True
            },
            "progress": {
                "level": 10,
                "experience_points": 5000,
                "completed_scenarios": ["scenario_001", "scenario_002", "scenario_003"],
                "badges": ["Security Expert", "Cloud Architect", "API Master"]
            }
        }
        
        student_user = {
            "_id": str(uuid.uuid4()),
            "email": "student@example.com", 
            "password_hash": pwd_context.hash("student123"),
            "profile": {
                "first_name": "Jane",
                "last_name": "Student",
                "avatar_url": None,
                "bio": "Learning threat modeling"
            },
            "role": "student",
            "created_at": datetime.utcnow(),
            "last_login": None,
            "preferences": {
                "theme": "light",
                "notifications": True
            },
            "progress": {
                "level": 2,
                "experience_points": 250,
                "completed_scenarios": ["scenario_001"],
                "badges": ["First Steps"]
            }
        }
        
        await users_collection.insert_many([admin_user, student_user])
        print("✅ Created sample users (admin@threatmodeling.com / admin123, student@example.com / student123)")
        
        # Create sample diagrams
        diagrams_collection = db.diagrams
        await diagrams_collection.delete_many({"title": {"$regex": "Sample"}})
        
        sample_diagram = {
            "_id": str(uuid.uuid4()),
            "user_id": student_user["_id"],
            "scenario_id": "scenario_001",
            "title": "Sample E-commerce Architecture",
            "diagram_data": {
                "nodes": [
                    {
                        "id": "user-1",
                        "type": "frontend",
                        "position": {"x": 100, "y": 100},
                        "data": {"label": "User Browser", "properties": {}}
                    },
                    {
                        "id": "lb-1", 
                        "type": "network",
                        "position": {"x": 300, "y": 100},
                        "data": {"label": "Load Balancer", "properties": {}}
                    },
                    {
                        "id": "web-1",
                        "type": "server",
                        "position": {"x": 500, "y": 100},
                        "data": {"label": "Web Server", "properties": {}}
                    },
                    {
                        "id": "db-1",
                        "type": "database",
                        "position": {"x": 500, "y": 300},
                        "data": {"label": "Database", "properties": {}}
                    }
                ],
                "edges": [
                    {
                        "id": "edge-1",
                        "source": "user-1",
                        "target": "lb-1",
                        "type": "default",
                        "data": {"protocol": "HTTPS", "encrypted": True}
                    },
                    {
                        "id": "edge-2", 
                        "source": "lb-1",
                        "target": "web-1",
                        "type": "default",
                        "data": {"protocol": "HTTP", "encrypted": False}
                    },
                    {
                        "id": "edge-3",
                        "source": "web-1", 
                        "target": "db-1",
                        "type": "default",
                        "data": {"protocol": "MySQL", "encrypted": True}
                    }
                ]
            },
            "metadata": {
                "trust_boundaries": [],
                "data_flows": [],
                "security_controls": []
            },
            "status": "draft",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "version": 1
        }
        
        await diagrams_collection.insert_one(sample_diagram)
        print("✅ Created sample diagram")
        
        # Create sample scores
        scores_collection = db.scores
        await scores_collection.delete_many({})
        
        sample_score = {
            "_id": str(uuid.uuid4()),
            "user_id": student_user["_id"],
            "scenario_id": "scenario_001",
            "diagram_id": sample_diagram["_id"],
            "scores": {
                "security_score": 75.5,
                "architecture_score": 85.0,
                "performance_score": 70.0,
                "completeness_score": 90.0,
                "total_score": 78.8
            },
            "time_spent": 3600,  # 1 hour
            "submission_time": datetime.utcnow(),
            "feedback": {
                "summary": "Good basic architecture with room for security improvements",
                "strengths": [
                    "Proper use of load balancer for high availability",
                    "Encrypted database connection",
                    "Clean separation of concerns"
                ],
                "weaknesses": [
                    "Missing Web Application Firewall",
                    "No authentication service shown",
                    "Internal communication not encrypted"
                ],
                "recommendations": [
                    "Add a Web Application Firewall before the load balancer",
                    "Implement proper authentication and session management",
                    "Use HTTPS for all internal communications",
                    "Add monitoring and logging components"
                ]
            },
            "validation_results": [
                {
                    "rule_id": "auth_required",
                    "severity": "warning",
                    "message": "No authentication service detected",
                    "element_id": "web-1"
                },
                {
                    "rule_id": "waf_missing",
                    "severity": "error", 
                    "message": "Web Application Firewall recommended for public-facing applications",
                    "element_id": "lb-1"
                }
            ]
        }
        
        await scores_collection.insert_one(sample_score)
        print("✅ Created sample score and feedback")
        
        print("\n🎉 Sample data creation completed!")
        print("\n📋 Test accounts:")
        print("   Admin: admin@threatmodeling.com / admin123")
        print("   Student: student@example.com / student123")
        print(f"\n📊 Created:")
        print(f"   - {len(SAMPLE_SCENARIOS)} scenarios")
        print(f"   - 2 users")
        print(f"   - 1 sample diagram")
        print(f"   - 1 sample score with feedback")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(create_sample_data())