"""
Enhanced Validation Service with Comprehensive Threat Modeling Rules
"""
from typing import List, Dict, Any, Optional
from models.diagram import DiagramResponse
from models.score import ValidationResult
import re


class ThreatModelingValidationService:
    """Advanced validation service for threat modeling scenarios"""
    
    def __init__(self):
        self.security_rules = self._initialize_security_rules()
        self.architecture_rules = self._initialize_architecture_rules()
        self.performance_rules = self._initialize_performance_rules()
        self.completeness_rules = self._initialize_completeness_rules()
    
    async def validate_comprehensive(self, diagram: DiagramResponse, scenario_context: Optional[Dict] = None) -> List[ValidationResult]:
        """Perform comprehensive threat modeling validation"""
        all_results = []
        
        # Security validations (most critical)
        security_results = await self._validate_security_comprehensive(diagram, scenario_context)
        all_results.extend(security_results)
        
        # Architecture validations
        architecture_results = await self._validate_architecture_comprehensive(diagram, scenario_context)
        all_results.extend(architecture_results)
        
        # Performance validations
        performance_results = await self._validate_performance_comprehensive(diagram, scenario_context)
        all_results.extend(performance_results)
        
        # Completeness validations
        completeness_results = await self._validate_completeness_comprehensive(diagram, scenario_context)
        all_results.extend(completeness_results)
        
        # OWASP Top 10 checks
        owasp_results = await self._validate_owasp_top10(diagram)
        all_results.extend(owasp_results)
        
        # STRIDE threat model checks
        stride_results = await self._validate_stride_threats(diagram)
        all_results.extend(stride_results)
        
        return all_results
    
    async def _validate_security_comprehensive(self, diagram: DiagramResponse, scenario_context: Optional[Dict] = None) -> List[ValidationResult]:
        """Comprehensive security validation"""
        results = []
        nodes = diagram.diagram_data.nodes
        edges = diagram.diagram_data.edges
        
        # 1. Authentication & Authorization
        auth_nodes = [n for n in nodes if any(keyword in n.type.lower() for keyword in ['auth', 'login', 'identity', 'oauth', 'sso'])]
        if not auth_nodes:
            results.append(ValidationResult(
                rule_id="SEC001",
                rule_name="Missing Authentication",
                severity="error",
                message="No authentication mechanism detected. All systems need user authentication.",
                category="security",
                element_type="system"
            ))
        
        # 2. Encryption in Transit
        unencrypted_connections = []
        for edge in edges:
            protocol = edge.data.get('protocol', '').lower()
            if protocol in ['http', 'ftp', 'telnet'] or (not protocol and not edge.data.get('encrypted', False)):
                unencrypted_connections.append(edge.id)
        
        if unencrypted_connections:
            results.append(ValidationResult(
                rule_id="SEC002",
                rule_name="Unencrypted Communication",
                severity="error" if len(unencrypted_connections) > len(edges) * 0.5 else "warning",
                message=f"Found {len(unencrypted_connections)} unencrypted connections. Use HTTPS/TLS for all communications.",
                category="security",
                element_type="connection"
            ))
        
        # 3. Database Security
        db_nodes = [n for n in nodes if 'database' in n.type.lower() or 'db' in n.type.lower()]
        for db_node in db_nodes:
            # Check if database has encryption at rest
            if not db_node.data.get('encrypted_at_rest', False):
                results.append(ValidationResult(
                    rule_id="SEC003",
                    rule_name="Database Encryption",
                    severity="warning",
                    message=f"Database '{db_node.data.get('label', db_node.id)}' should have encryption at rest enabled.",
                    category="security",
                    element_id=db_node.id,
                    element_type="database"
                ))
            
            # Check for direct database access from frontend
            direct_access = [e for e in edges if e.target == db_node.id and 
                           any(n.id == e.source and 'frontend' in n.type.lower() for n in nodes)]
            if direct_access:
                results.append(ValidationResult(
                    rule_id="SEC004",
                    rule_name="Direct Database Access",
                    severity="error",
                    message="Frontend components should not connect directly to databases. Use API layers.",
                    category="security",
                    element_id=db_node.id,
                    element_type="database"
                ))
        
        # 4. API Security
        api_nodes = [n for n in nodes if 'api' in n.type.lower() or 'service' in n.type.lower()]
        for api_node in api_nodes:
            # Check for API authentication
            if not api_node.data.get('requires_auth', False):
                results.append(ValidationResult(
                    rule_id="SEC005",
                    rule_name="API Authentication",
                    severity="error",
                    message=f"API '{api_node.data.get('label', api_node.id)}' should require authentication.",
                    category="security",
                    element_id=api_node.id,
                    element_type="api"
                ))
            
            # Check for rate limiting
            if not api_node.data.get('rate_limited', False):
                results.append(ValidationResult(
                    rule_id="SEC006",
                    rule_name="API Rate Limiting",
                    severity="warning",
                    message=f"API '{api_node.data.get('label', api_node.id)}' should implement rate limiting.",
                    category="security",
                    element_id=api_node.id,
                    element_type="api"
                ))
        
        # 5. Input Validation
        user_input_nodes = [n for n in nodes if any(keyword in n.type.lower() for keyword in ['frontend', 'form', 'input', 'ui'])]
        for input_node in user_input_nodes:
            if not input_node.data.get('input_validation', False):
                results.append(ValidationResult(
                    rule_id="SEC007",
                    rule_name="Input Validation",
                    severity="error",
                    message=f"Component '{input_node.data.get('label', input_node.id)}' should validate all user inputs.",
                    category="security",
                    element_id=input_node.id,
                    element_type="frontend"
                ))
        
        return results
    
    async def _validate_architecture_comprehensive(self, diagram: DiagramResponse, scenario_context: Optional[Dict] = None) -> List[ValidationResult]:
        """Comprehensive architecture validation"""
        results = []
        nodes = diagram.diagram_data.nodes
        edges = diagram.diagram_data.edges
        
        # 1. Layered Architecture
        layers = self._identify_architectural_layers(nodes)
        if len(layers.get('presentation', [])) > 0 and len(layers.get('business', [])) == 0:
            results.append(ValidationResult(
                rule_id="ARCH001",
                rule_name="Missing Business Layer",
                severity="warning",
                message="Consider adding a business/service layer between presentation and data layers.",
                category="architecture",
                element_type="system"
            ))
        
        # 2. Single Points of Failure
        critical_nodes = self._identify_critical_nodes(nodes, edges)
        for node_id in critical_nodes:
            node = next((n for n in nodes if n.id == node_id), None)
            if node and not node.data.get('redundancy', False):
                results.append(ValidationResult(
                    rule_id="ARCH002",
                    rule_name="Single Point of Failure",
                    severity="error",
                    message=f"Critical component '{node.data.get('label', node.id)}' lacks redundancy.",
                    category="architecture",
                    element_id=node.id,
                    element_type=node.type
                ))
        
        # 3. Circular Dependencies
        circular_deps = self._detect_circular_dependencies(nodes, edges)
        if circular_deps:
            results.append(ValidationResult(
                rule_id="ARCH003",
                rule_name="Circular Dependencies",
                severity="warning",
                message=f"Detected circular dependencies between: {', '.join(circular_deps)}",
                category="architecture",
                element_type="system"
            ))
        
        # 4. Microservices Best Practices (if applicable)
        service_nodes = [n for n in nodes if 'service' in n.type.lower() or 'microservice' in n.type.lower()]
        if len(service_nodes) > 3:  # Assuming microservices architecture
            # Check for service mesh/API gateway
            gateway_nodes = [n for n in nodes if any(keyword in n.type.lower() for keyword in ['gateway', 'proxy', 'mesh'])]
            if not gateway_nodes:
                results.append(ValidationResult(
                    rule_id="ARCH004",
                    rule_name="Missing API Gateway",
                    severity="warning",
                    message="Microservices architecture should include an API Gateway or service mesh.",
                    category="architecture",
                    element_type="system"
                ))
        
        return results
    
    async def _validate_performance_comprehensive(self, diagram: DiagramResponse, scenario_context: Optional[Dict] = None) -> List[ValidationResult]:
        """Comprehensive performance validation"""
        results = []
        nodes = diagram.diagram_data.nodes
        edges = diagram.diagram_data.edges
        
        # 1. Load Balancing
        if len(nodes) > 5:  # Complex system
            lb_nodes = [n for n in nodes if any(keyword in n.type.lower() for keyword in ['load', 'balancer', 'lb'])]
            if not lb_nodes:
                results.append(ValidationResult(
                    rule_id="PERF001",
                    rule_name="Missing Load Balancer",
                    severity="warning",
                    message="Complex systems should implement load balancing for scalability.",
                    category="performance",
                    element_type="system"
                ))
        
        # 2. Caching Strategy
        cache_nodes = [n for n in nodes if 'cache' in n.type.lower() or 'redis' in n.type.lower()]
        db_nodes = [n for n in nodes if 'database' in n.type.lower()]
        
        if len(db_nodes) > 0 and len(cache_nodes) == 0:
            results.append(ValidationResult(
                rule_id="PERF002",
                rule_name="Missing Caching Layer",
                severity="warning",
                message="Consider adding caching to improve database performance.",
                category="performance",
                element_type="system"
            ))
        
        # 3. CDN for Static Assets
        frontend_nodes = [n for n in nodes if 'frontend' in n.type.lower() or 'ui' in n.type.lower()]
        cdn_nodes = [n for n in nodes if 'cdn' in n.type.lower()]
        
        if len(frontend_nodes) > 0 and len(cdn_nodes) == 0:
            results.append(ValidationResult(
                rule_id="PERF003",
                rule_name="Missing CDN",
                severity="info",
                message="Consider using a CDN for static assets to improve loading times.",
                category="performance",
                element_type="system"
            ))
        
        # 4. Database Optimization
        for db_node in db_nodes:
            if not db_node.data.get('indexed', False):
                results.append(ValidationResult(
                    rule_id="PERF004",
                    rule_name="Database Indexing",
                    severity="warning",
                    message=f"Database '{db_node.data.get('label', db_node.id)}' should have proper indexing.",
                    category="performance",
                    element_id=db_node.id,
                    element_type="database"
                ))
        
        return results
    
    async def _validate_completeness_comprehensive(self, diagram: DiagramResponse, scenario_context: Optional[Dict] = None) -> List[ValidationResult]:
        """Comprehensive completeness validation"""
        results = []
        nodes = diagram.diagram_data.nodes
        edges = diagram.diagram_data.edges
        
        # 1. Minimum System Components
        if len(nodes) < 3:
            results.append(ValidationResult(
                rule_id="COMP001",
                rule_name="Insufficient Components",
                severity="error",
                message="A complete system design should have at least 3 components.",
                category="completeness",
                element_type="system"
            ))
        
        # 2. Essential Components for Web Applications
        if scenario_context and scenario_context.get('category') == 'web':
            required_components = ['frontend', 'api', 'database']
            missing_components = []
            
            for component in required_components:
                if not any(component in n.type.lower() for n in nodes):
                    missing_components.append(component)
            
            if missing_components:
                results.append(ValidationResult(
                    rule_id="COMP002",
                    rule_name="Missing Essential Components",
                    severity="error",
                    message=f"Web application missing: {', '.join(missing_components)}",
                    category="completeness",
                    element_type="system"
                ))
        
        # 3. Orphaned Components
        connected_nodes = set()
        for edge in edges:
            connected_nodes.add(edge.source)
            connected_nodes.add(edge.target)
        
        orphaned_nodes = [n for n in nodes if n.id not in connected_nodes]
        if orphaned_nodes:
            results.append(ValidationResult(
                rule_id="COMP003",
                rule_name="Orphaned Components",
                severity="warning",
                message=f"{len(orphaned_nodes)} components are not connected to the system.",
                category="completeness",
                element_type="system"
            ))
        
        # 4. Data Flow Completeness
        if not self._has_complete_data_flow(nodes, edges):
            results.append(ValidationResult(
                rule_id="COMP004",
                rule_name="Incomplete Data Flow",
                severity="warning",
                message="The system should show complete data flow from user input to data storage.",
                category="completeness",
                element_type="system"
            ))
        
        return results
    
    async def _validate_owasp_top10(self, diagram: DiagramResponse) -> List[ValidationResult]:
        """Validate against OWASP Top 10 vulnerabilities"""
        results = []
        nodes = diagram.diagram_data.nodes
        edges = diagram.diagram_data.edges
        
        # A01: Broken Access Control
        if not any('auth' in n.type.lower() or n.data.get('access_control', False) for n in nodes):
            results.append(ValidationResult(
                rule_id="OWASP001",
                rule_name="Broken Access Control (A01)",
                severity="error",
                message="System lacks proper access control mechanisms.",
                category="security",
                element_type="system"
            ))
        
        # A02: Cryptographic Failures
        sensitive_data_nodes = [n for n in nodes if n.data.get('stores_sensitive_data', False)]
        for node in sensitive_data_nodes:
            if not node.data.get('encrypted', False):
                results.append(ValidationResult(
                    rule_id="OWASP002", 
                    rule_name="Cryptographic Failures (A02)",
                    severity="error",
                    message=f"Sensitive data in '{node.data.get('label', node.id)}' should be encrypted.",
                    category="security",
                    element_id=node.id,
                    element_type=node.type
                ))
        
        # A03: Injection
        user_input_nodes = [n for n in nodes if 'frontend' in n.type.lower() or 'form' in n.type.lower()]
        for node in user_input_nodes:
            if not node.data.get('input_validation', False) and not node.data.get('prepared_statements', False):
                results.append(ValidationResult(
                    rule_id="OWASP003",
                    rule_name="Injection Vulnerabilities (A03)",
                    severity="error",
                    message=f"'{node.data.get('label', node.id)}' needs input validation and prepared statements.",
                    category="security",
                    element_id=node.id,
                    element_type=node.type
                ))
        
        return results
    
    async def _validate_stride_threats(self, diagram: DiagramResponse) -> List[ValidationResult]:
        """Validate using STRIDE threat modeling methodology"""
        results = []
        nodes = diagram.diagram_data.nodes
        edges = diagram.diagram_data.edges
        
        # Spoofing
        if not any(n.data.get('authentication', False) for n in nodes):
            results.append(ValidationResult(
                rule_id="STRIDE001",
                rule_name="Spoofing Threat",
                severity="error",
                message="System vulnerable to spoofing - implement strong authentication.",
                category="security",
                element_type="system"
            ))
        
        # Tampering
        unprotected_connections = [e for e in edges if not e.data.get('integrity_protection', False)]
        if len(unprotected_connections) > 0:
            results.append(ValidationResult(
                rule_id="STRIDE002",
                rule_name="Tampering Threat",
                severity="warning",
                message="Communications lack integrity protection - use digital signatures or HMAC.",
                category="security",
                element_type="connection"
            ))
        
        # Repudiation
        if not any(n.data.get('logging', False) or n.data.get('audit_trail', False) for n in nodes):
            results.append(ValidationResult(
                rule_id="STRIDE003",
                rule_name="Repudiation Threat",
                severity="warning",
                message="System lacks audit logging - implement comprehensive logging.",
                category="security",
                element_type="system"
            ))
        
        # Information Disclosure
        public_facing_nodes = [n for n in nodes if n.data.get('public_facing', False)]
        for node in public_facing_nodes:
            if not node.data.get('data_minimization', False):
                results.append(ValidationResult(
                    rule_id="STRIDE004",
                    rule_name="Information Disclosure Threat",
                    severity="warning",
                    message=f"Public component '{node.data.get('label', node.id)}' should minimize exposed data.",
                    category="security",
                    element_id=node.id,
                    element_type=node.type
                ))
        
        return results
    
    # Helper methods
    def _identify_architectural_layers(self, nodes: List) -> Dict[str, List]:
        """Identify architectural layers in the system"""
        layers = {
            'presentation': [],
            'business': [],
            'data': []
        }
        
        for node in nodes:
            node_type = node.type.lower()
            if any(keyword in node_type for keyword in ['frontend', 'ui', 'web', 'mobile']):
                layers['presentation'].append(node)
            elif any(keyword in node_type for keyword in ['api', 'service', 'business', 'logic']):
                layers['business'].append(node)
            elif any(keyword in node_type for keyword in ['database', 'storage', 'cache']):
                layers['data'].append(node)
        
        return layers
    
    def _identify_critical_nodes(self, nodes: List, edges: List) -> List[str]:
        """Identify nodes that are critical to system operation"""
        # Count connections for each node
        connection_count = {}
        for node in nodes:
            connection_count[node.id] = sum(1 for edge in edges if edge.source == node.id or edge.target == node.id)
        
        # Nodes with high connectivity are critical
        avg_connections = sum(connection_count.values()) / len(connection_count) if connection_count else 0
        critical_nodes = [node_id for node_id, count in connection_count.items() if count > avg_connections * 1.5]
        
        return critical_nodes
    
    def _detect_circular_dependencies(self, nodes: List, edges: List) -> List[str]:
        """Detect circular dependencies in the system"""
        # Simple cycle detection using DFS
        # This is a simplified version - a full implementation would use graph algorithms
        circular_deps = []
        
        # Build adjacency list
        adj_list = {node.id: [] for node in nodes}
        for edge in edges:
            adj_list[edge.source].append(edge.target)
        
        # Basic circular dependency detection (simplified)
        for node in nodes:
            for target in adj_list[node.id]:
                if node.id in adj_list.get(target, []):
                    circular_deps.append(f"{node.id} ↔ {target}")
        
        return circular_deps
    
    def _has_complete_data_flow(self, nodes: List, edges: List) -> bool:
        """Check if system has complete data flow"""
        # Check if there's a path from user input to data storage
        input_nodes = [n for n in nodes if any(keyword in n.type.lower() for keyword in ['frontend', 'input', 'ui'])]
        storage_nodes = [n for n in nodes if any(keyword in n.type.lower() for keyword in ['database', 'storage'])]
        
        if not input_nodes or not storage_nodes:
            return False
        
        # Simplified path checking - in a real implementation, use graph traversal
        return len(edges) >= len(nodes) - 1  # At least a connected graph
    
    def _initialize_security_rules(self) -> Dict[str, Dict]:
        """Initialize security validation rules"""
        return {
            "authentication": {"weight": 0.25, "critical": True},
            "encryption": {"weight": 0.20, "critical": True},
            "authorization": {"weight": 0.20, "critical": True},
            "input_validation": {"weight": 0.15, "critical": True},
            "session_management": {"weight": 0.10, "critical": False},
            "error_handling": {"weight": 0.10, "critical": False}
        }
    
    def _initialize_architecture_rules(self) -> Dict[str, Dict]:
        """Initialize architecture validation rules"""
        return {
            "separation_of_concerns": {"weight": 0.30, "critical": True},
            "scalability": {"weight": 0.25, "critical": False},
            "maintainability": {"weight": 0.20, "critical": False},
            "modularity": {"weight": 0.15, "critical": False},
            "coupling": {"weight": 0.10, "critical": False}
        }
    
    def _initialize_performance_rules(self) -> Dict[str, Dict]:
        """Initialize performance validation rules"""
        return {
            "load_balancing": {"weight": 0.30, "critical": False},
            "caching": {"weight": 0.25, "critical": False},
            "database_optimization": {"weight": 0.20, "critical": False},
            "cdn_usage": {"weight": 0.15, "critical": False},
            "compression": {"weight": 0.10, "critical": False}
        }
    
    def _initialize_completeness_rules(self) -> Dict[str, Dict]:
        """Initialize completeness validation rules"""
        return {
            "essential_components": {"weight": 0.40, "critical": True},
            "data_flow": {"weight": 0.25, "critical": True},
            "error_handling": {"weight": 0.20, "critical": False},
            "monitoring": {"weight": 0.15, "critical": False}
        }