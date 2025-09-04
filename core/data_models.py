#!/usr/bin/env python3
"""
Generic Data Models for Universal DataLoader
Replaces domain-specific models with flexible, configurable alternatives
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class SystemEntity:
    """
    Generic system entity - can represent any type of system/server/device
    
    Replaces RHELSystem with a flexible, domain-agnostic model
    """
    system_id: str
    name: str = ""
    system_type: str = "unknown"  # e.g., "server", "device", "application"
    version: str = "unknown"
    environment: str = "unknown"  # e.g., "production", "staging", "development"
    location: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)
    services: List[str] = field(default_factory=list)
    components: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Set default name if not provided"""
        if not self.name:
            self.name = self.system_id

@dataclass 
class EventEntity:
    """
    Generic event entity - can represent any type of event/incident/change
    
    Replaces PatchEvent with a flexible, domain-agnostic model
    """
    event_id: str
    system_id: str = ""
    event_type: str = "unknown"  # e.g., "patch", "incident", "change", "alert"
    timestamp: Optional[datetime] = None
    severity: str = "info"  # e.g., "critical", "high", "medium", "low", "info"
    status: str = "unknown"  # e.g., "open", "in_progress", "resolved", "closed"
    title: str = ""
    description: str = ""
    source: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Set default timestamp and title if not provided"""
        if not self.timestamp:
            self.timestamp = datetime.now()
        if not self.title:
            self.title = f"{self.event_type.title()} Event {self.event_id}"

@dataclass
class DocumentEntity:
    """
    Generic document entity - represents processed documents/files
    """
    document_id: str
    source_path: str = ""
    document_type: str = "unknown"  # e.g., "log", "config", "report", "manual"
    content: str = ""
    processed_content: str = ""
    entities_found: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        """Set default timestamp"""
        if not self.timestamp:
            self.timestamp = datetime.now()

# Type aliases for backward compatibility and flexibility
System = SystemEntity
Event = EventEntity 
Document = DocumentEntity

# Factory functions for easy creation
def create_system(system_id: str, **kwargs) -> SystemEntity:
    """Create a system entity with flexible parameters"""
    return SystemEntity(system_id=system_id, **kwargs)

def create_event(event_id: str, **kwargs) -> EventEntity:
    """Create an event entity with flexible parameters"""
    return EventEntity(event_id=event_id, **kwargs)

def create_document(document_id: str, **kwargs) -> DocumentEntity:
    """Create a document entity with flexible parameters"""
    return DocumentEntity(document_id=document_id, **kwargs)

# Example usage for different domains:
"""
# For RHEL/Linux systems:
rhel_server = create_system(
    system_id="web-prod-01", 
    system_type="linux_server",
    version="RHEL 9.2",
    environment="production",
    services=["httpd", "mariadb"],
    properties={"cpu_cores": 8, "memory_gb": 32}
)

# For network devices:
network_switch = create_system(
    system_id="switch-core-01",
    system_type="network_switch", 
    version="Cisco IOS 15.2",
    location="datacenter-1",
    properties={"ports": 48, "mgmt_ip": "192.168.1.10"}
)

# For applications:
web_app = create_system(
    system_id="ecommerce-api",
    system_type="application",
    version="v2.1.3",
    environment="production",
    components=["authentication", "catalog", "payments"]
)

# For security events:
security_event = create_event(
    event_id="SEC-2024-001",
    event_type="security_incident",
    severity="high",
    title="Unauthorized Access Attempt",
    system_id="web-prod-01"
)

# For maintenance events:
maintenance_event = create_event(
    event_id="MAINT-2024-001", 
    event_type="maintenance",
    severity="low",
    title="Scheduled System Update",
    system_id="web-prod-01"
)
"""
