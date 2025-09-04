#!/usr/bin/env python3
"""
Examples: Extending Universal DataLoader for Different Domains
Shows how to customize the AI graph builder for specific use cases
"""

from typing import Dict, Any, List
from core.graph_builders import GraphBuilder, create_graph_builder

# Example 1: Security Domain Extension
def create_security_graph_builder(llm_config: Dict[str, Any], neo4j_config: Dict[str, Any]) -> GraphBuilder:
    """
    Create a graph builder optimized for security data
    
    This example shows how to customize the AI for security incident analysis
    """
    # Create AI graph builder with security-specific configuration
    builder = create_graph_builder('ai', llm_config=llm_config, neo4j_config=neo4j_config)
    
    # Security-specific node types (extends the universal set)
    security_nodes = [
        "Incident", "Vulnerability", "Threat", "Attack", "Malware",
        "Firewall", "IDS", "SIEM", "SOC", "Analyst",
        "IOC", "TTP", "MITRE_ATT&CK", "CVE", "Evidence"
    ]
    
    # Security-specific relationships
    security_relationships = [
        "EXPLOITS", "MITIGATES", "DETECTS", "BLOCKS", "ESCALATES",
        "INVESTIGATES", "RESPONDS_TO", "CORRELATES_WITH", "INDICATES",
        "ATTRIBUTED_TO", "TARGETS", "COMPROMISES", "EXFILTRATES"
    ]
    
    # You could extend the builder's allowed nodes/relationships here
    # This demonstrates the extensibility pattern
    
    return builder

# Example 2: Business Process Extension  
def create_business_process_builder(llm_config: Dict[str, Any], neo4j_config: Dict[str, Any]) -> GraphBuilder:
    """
    Create a graph builder optimized for business process documentation
    """
    builder = create_graph_builder('ai', llm_config=llm_config, neo4j_config=neo4j_config)
    
    # Business-specific nodes
    business_nodes = [
        "Process", "Workflow", "Task", "Decision", "Gateway",
        "Actor", "Role", "Department", "System", "Document",
        "KPI", "Metric", "SLA", "Compliance", "Risk"
    ]
    
    # Business-specific relationships
    business_relationships = [
        "PERFORMS", "APPROVES", "REVIEWS", "ESCALATES_TO", "REPORTS_TO",
        "DEPENDS_ON", "TRIGGERS", "COMPLETES", "VALIDATES", "MEASURES"
    ]
    
    return builder

# Example 3: IoT/Industrial Extension
def create_iot_industrial_builder(llm_config: Dict[str, Any], neo4j_config: Dict[str, Any]) -> GraphBuilder:
    """
    Create a graph builder optimized for IoT and industrial systems
    """
    builder = create_graph_builder('ai', llm_config=llm_config, neo4j_config=neo4j_config)
    
    # IoT/Industrial nodes
    iot_nodes = [
        "Sensor", "Actuator", "Gateway", "Controller", "HMI",
        "SCADA", "PLC", "Machine", "Production_Line", "Factory",
        "Reading", "Alert", "Maintenance", "Calibration", "Recipe"
    ]
    
    # IoT/Industrial relationships
    iot_relationships = [
        "MONITORS", "CONTROLS", "CALIBRATES", "MAINTAINS", "PRODUCES",
        "TRANSMITS_TO", "RECEIVES_FROM", "TRIGGERS_ALARM", "SCHEDULES"
    ]
    
    return builder

# Example 4: Multi-Domain Usage
def demo_multi_domain_usage():
    """
    Demonstrate how to use different builders for different data types
    """
    
    # Mock configurations (in real usage, these come from your config files)
    llm_config = {
        'base_url': 'https://your-llm-endpoint.com/v1',
        'api_key': 'your-api-key',
        'model': 'your-model'
    }
    
    neo4j_config = {
        'uri': 'neo4j://127.0.0.1:7687',
        'username': 'neo4j',
        'password': 'password',
        'database': 'neo4j'
    }
    
    # Example data for different domains
    security_data = {
        'incident_report.txt': {
            'cleaned_content': 'Security incident detected: SQL injection attempt from IP 192.168.1.100 targeting user database. Firewall blocked 95% of requests.'
        }
    }
    
    business_data = {
        'process_doc.md': {
            'cleaned_content': 'Purchase Order Process: 1. Requester submits PO 2. Manager approves 3. Finance validates budget 4. Procurement processes order'
        }
    }
    
    iot_data = {
        'sensor_logs.txt': {
            'cleaned_content': 'Temperature sensor T-001 reading 85°C. Threshold exceeded. Cooling system activated. Production line paused.'
        }
    }
    
    # Create domain-specific builders
    security_builder = create_security_graph_builder(llm_config, neo4j_config)
    business_builder = create_business_process_builder(llm_config, neo4j_config)
    iot_builder = create_iot_industrial_builder(llm_config, neo4j_config)
    
    # Process each domain with its specialized builder
    print("🔒 Processing security data...")
    security_builder.create_knowledge_graph('security_incident_001', security_data)
    
    print("💼 Processing business data...")  
    business_builder.create_knowledge_graph('purchase_process', business_data)
    
    print("🏭 Processing IoT data...")
    iot_builder.create_knowledge_graph('factory_floor_01', iot_data)
    
    # Clean up
    security_builder.close()
    business_builder.close()
    iot_builder.close()
    
    print("✅ Multi-domain knowledge graphs created!")

# Example 5: Custom Configuration Integration
def integrate_with_dataloader_config():
    """
    Show how to integrate domain-specific builders with the main dataloader
    """
    
    # Example: Extend the main configuration to support domain-specific builders
    domain_configs = {
        'security': {
            'builder_type': 'ai',
            'specialized_nodes': ['Incident', 'Vulnerability', 'Threat'],
            'specialized_relationships': ['EXPLOITS', 'MITIGATES', 'DETECTS']
        },
        'business': {
            'builder_type': 'ai', 
            'specialized_nodes': ['Process', 'Workflow', 'Task'],
            'specialized_relationships': ['PERFORMS', 'APPROVES', 'TRIGGERS']
        }
    }
    
    print("🔧 Domain-specific configurations:")
    for domain, config in domain_configs.items():
        print(f"   {domain}: {config['builder_type']} with {len(config['specialized_nodes'])} custom nodes")

# Example 6: Factory Pattern for Builder Selection
def create_domain_aware_builder(domain: str, llm_config: Dict[str, Any], neo4j_config: Dict[str, Any]) -> GraphBuilder:
    """
    Factory function that creates the right builder based on data domain
    
    This shows how you could automatically select builders based on content analysis
    """
    
    domain_builders = {
        'security': create_security_graph_builder,
        'business': create_business_process_builder,
        'iot': create_iot_industrial_builder,
        'infrastructure': lambda llm, neo4j: create_graph_builder('ai', llm_config=llm, neo4j_config=neo4j),  # Default
        'universal': lambda llm, neo4j: create_graph_builder('ai', llm_config=llm, neo4j_config=neo4j)  # Default
    }
    
    builder_factory = domain_builders.get(domain, domain_builders['universal'])
    return builder_factory(llm_config, neo4j_config)

def main():
    """
    Run extension examples
    """
    print("🚀 DOMAIN EXTENSION EXAMPLES")
    print("=" * 50)
    
    print("\n1. 🔒 Security Domain Builder")
    print("   - Specialized for incident analysis")
    print("   - Custom entities: Incident, Vulnerability, Threat")
    print("   - Custom relationships: EXPLOITS, MITIGATES, DETECTS")
    
    print("\n2. 💼 Business Process Builder") 
    print("   - Specialized for workflow documentation")
    print("   - Custom entities: Process, Workflow, Task")
    print("   - Custom relationships: PERFORMS, APPROVES, TRIGGERS")
    
    print("\n3. 🏭 IoT/Industrial Builder")
    print("   - Specialized for manufacturing systems")
    print("   - Custom entities: Sensor, Actuator, Machine")
    print("   - Custom relationships: MONITORS, CONTROLS, PRODUCES")
    
    print("\n4. 🎯 Multi-Domain Usage")
    print("   - Different builders for different data types")
    print("   - Automatic domain detection and builder selection")
    print("   - Unified knowledge graph with domain-specific optimization")
    
    print("\n💡 Key Benefits:")
    print("   ✅ Extensible architecture")
    print("   ✅ Domain-specific optimization")
    print("   ✅ Maintains universal compatibility")
    print("   ✅ Easy to add new domains")
    
    print("\n🔧 To extend for your domain:")
    print("   1. Create your custom builder function")
    print("   2. Define domain-specific nodes and relationships")
    print("   3. Use create_graph_builder() with your config")
    print("   4. Add to domain_builders factory dict")
    
    # Uncomment to run actual demo (requires valid LLM/Neo4j config)
    # integrate_with_dataloader_config()

if __name__ == "__main__":
    main()
