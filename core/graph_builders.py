#!/usr/bin/env python3
"""
Graph Builder Interfaces for Universal DataLoader
Extensible architecture for different knowledge graph creation strategies
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class GraphBuilder(ABC):
    """
    Abstract base class for knowledge graph builders
    
    Extensible interface that allows different strategies:
    - AI-powered graph creation (LangChain + LLM)
    - Rule-based graph creation (patterns + templates)
    - Hybrid approaches (AI + rules)
    - Domain-specific builders (security, networking, etc.)
    """
    
    @abstractmethod
    def create_knowledge_graph(self, system_id: str, processed_data: Dict[str, Any]) -> bool:
        """
        Create knowledge graph from processed data
        
        Args:
            system_id: Identifier for the data source
            processed_data: Pre-processed text data with structure:
                {
                    'file_path': {
                        'cleaned_content': str,
                        'structured_data': dict,
                        'metadata': dict
                    }
                }
        
        Returns:
            bool: True if knowledge graph created successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def get_supported_domains(self) -> List[str]:
        """
        Get list of domains this builder supports
        
        Returns:
            List of domain names (e.g., ['infrastructure', 'security', 'business'])
        """
        pass
    
    @abstractmethod
    def close(self):
        """Clean up resources (database connections, etc.)"""
        pass

class AIGraphBuilder(GraphBuilder):
    """
    AI-powered knowledge graph builder using LangChain LLMGraphTransformer
    
    Features:
    - Uses LLM to understand text semantically
    - Extracts entities and relationships automatically
    - Works with any domain (domain-agnostic)
    - Direct Neo4j integration via LangChain
    """
    
    def __init__(self, llm_config: Dict[str, Any], neo4j_config: Dict[str, Any]):
        """
        Initialize AI-powered graph builder
        
        Args:
            llm_config: LLM configuration (endpoint, model, API key)
            neo4j_config: Neo4j connection configuration
        """
        # Force reload environment variables to get working API key
        load_dotenv(override=True)
        
        self.llm_config = llm_config
        self.neo4j_config = neo4j_config
        self.llm = None
        self.graph_transformer = None
        self.neo4j_graph = None
        
        try:
            from langchain_experimental.graph_transformers import LLMGraphTransformer
            from langchain_openai import ChatOpenAI
            from langchain_core.documents import Document
            from langchain_neo4j import Neo4jGraph
            
            # Initialize LLM using config values
            self.llm = ChatOpenAI(
                base_url=llm_config['base_url'],
                api_key=llm_config['api_key'],
                model_name=llm_config['model'],
                temperature=0  # Deterministic for consistent results
            )
            
            # Initialize Neo4j connection
            self.neo4j_graph = Neo4jGraph(
                url=neo4j_config['uri'],
                username=neo4j_config['username'],
                password=neo4j_config['password'],
                database=neo4j_config['database'],
                refresh_schema=False
            )
            
            # Initialize LLM Graph Transformer with universal schema
            self.graph_transformer = LLMGraphTransformer(
                llm=self.llm,
                allowed_nodes=self._get_universal_node_types(),
                allowed_relationships=self._get_universal_relationships()
            )
            
            logger.info(f"AI Graph Builder initialized with {os.getenv('MODEL')}")
            
        except ImportError as e:
            logger.error(f"LangChain dependencies not available: {e}")
            raise RuntimeError("AI Graph Builder requires LangChain. Install with: pip install langchain langchain-experimental langchain-openai langchain-neo4j")
        except Exception as e:
            logger.error(f"Failed to initialize AI Graph Builder: {e}")
            raise RuntimeError(f"AI Graph Builder initialization failed: {e}")
    
    def _get_universal_node_types(self) -> List[str]:
        """Define universal node types that work across domains"""
        return [
            # Core Infrastructure
            "System", "Server", "Database", "Network", "Device",
            "Service", "Process", "Application", "Component",
            
            # Events & Operations  
            "Event", "Incident", "Alert", "Log", "Metric",
            "Change", "Deployment", "Backup", "Update",
            
            # Configuration & Code
            "Configuration", "Setting", "Parameter", "Variable",
            "Code", "Repository", "Package", "Library",
            
            # Business & Organization
            "Organization", "Team", "User", "Role", "Permission",
            "Project", "Environment", "Location", "Vendor",
            
            # Documents & Knowledge
            "Document", "Manual", "Policy", "Procedure", "Guide",
            "Report", "Dashboard", "Chart", "Analysis",
            
            # Security & Compliance
            "Vulnerability", "Threat", "Risk", "Control", "Audit",
            "Certificate", "Credential", "Token", "Key"
        ]
    
    def _get_universal_relationships(self) -> List[str]:
        """Define universal relationships that work across domains"""
        return [
            # Operational relationships
            "RUNS", "EXECUTES", "HOSTS", "CONTAINS", "INCLUDES",
            "DEPENDS_ON", "REQUIRES", "USES", "CONNECTS_TO",
            
            # Hierarchical relationships  
            "PARENT_OF", "CHILD_OF", "BELONGS_TO", "PART_OF",
            "MANAGES", "CONTROLS", "OWNS", "MAINTAINS",
            
            # Event relationships
            "GENERATES", "TRIGGERS", "CAUSES", "RESOLVES",
            "MONITORS", "ALERTS", "LOGS", "REPORTS",
            
            # Data relationships
            "READS", "WRITES", "ACCESSES", "STORES",
            "PROCESSES", "TRANSFORMS", "VALIDATES", "ENCRYPTS",
            
            # Business relationships
            "ASSIGNED_TO", "RESPONSIBLE_FOR", "APPROVES", "REVIEWS",
            "IMPLEMENTS", "DOCUMENTS", "SUPPORTS", "ESCALATES",
            
            # Security relationships
            "AUTHENTICATES", "AUTHORIZES", "PROTECTS", "THREATENS",
            "MITIGATES", "COMPLIES_WITH", "VIOLATES", "AUDITS"
        ]
    
    def create_knowledge_graph(self, system_id: str, processed_data: Dict[str, Any]) -> bool:
        """
        Create knowledge graph using AI analysis
        
        This method:
        1. Builds context from all processed files
        2. Uses LLM to extract entities and relationships
        3. Stores results directly in Neo4j
        4. Returns success/failure status
        """
        if not self.graph_transformer or not self.neo4j_graph:
            logger.error("AI Graph Builder not properly initialized")
            return False
        
        try:
            # Build comprehensive context for AI analysis
            context_text = self._build_analysis_context(system_id, processed_data)
            
            if not context_text.strip():
                logger.warning(f"No content available for {system_id}")
                return False
            
            # Create LangChain document for processing
            from langchain_core.documents import Document
            document = Document(
                page_content=context_text,
                metadata={
                    "source_id": system_id,
                    "timestamp": "2024-01-01T00:00:00Z",  # Will be dynamic in production
                    "builder_type": "ai_powered",
                    "domain": "universal"
                }
            )
            
            logger.info(f"Creating knowledge graph for {system_id} ({len(context_text)} chars)")
            
            # AI-powered graph creation
            graph_documents = self.graph_transformer.convert_to_graph_documents([document])
            
            if not graph_documents:
                logger.warning(f"No graph structure extracted from {system_id}")
                return False
            
            # Log what was extracted
            graph_doc = graph_documents[0]
            logger.info(f"AI extracted {len(graph_doc.nodes)} entities, {len(graph_doc.relationships)} relationships")
            
            # Store in Neo4j
            self.neo4j_graph.add_graph_documents(graph_documents)
            
            logger.info(f"Knowledge graph created successfully for {system_id}")
            return True
            
        except Exception as e:
            logger.error(f"Knowledge graph creation failed for {system_id}: {e}")
            return False
    
    def _build_analysis_context(self, system_id: str, processed_data: Dict[str, Any]) -> str:
        """Build comprehensive context for AI analysis"""
        context_parts = [f"SYSTEM ANALYSIS: {system_id}"]
        
        for file_path, file_data in processed_data.items():
            content = file_data.get('cleaned_content', '')
            if content.strip():
                context_parts.append(f"\n--- FILE: {file_path} ---")
                context_parts.append(content)
        
        # Add analysis instructions for better AI results
        context_parts.append(f"""

KNOWLEDGE GRAPH INSTRUCTIONS:
Analyze the system data above and create a comprehensive knowledge graph.

Focus on extracting:
1. SYSTEMS: servers, databases, applications with their properties
2. SERVICES: running processes, APIs, daemons with status/ports  
3. COMPONENTS: software packages, libraries, modules
4. EVENTS: incidents, changes, deployments, errors
5. CONFIGURATIONS: settings, parameters, environment variables
6. RELATIONSHIPS: how entities connect, depend on, or interact

System Context: {system_id}
Extract entities that represent real infrastructure, applications, and operational elements.
""")
        
        return '\n'.join(context_parts)
    
    def get_supported_domains(self) -> List[str]:
        """AI builder works with any domain"""
        return [
            "infrastructure", "applications", "security", "business",
            "documents", "operations", "networking", "databases",
            "monitoring", "compliance", "universal"
        ]
    
    def close(self):
        """Clean up AI graph builder resources"""
        if self.neo4j_graph:
            try:
                self.neo4j_graph.close()
                logger.info("AI Graph Builder connection closed")
            except:
                pass

class RuleBasedGraphBuilder(GraphBuilder):
    """
    Rule-based knowledge graph builder using patterns and templates
    
    Features:
    - Uses predefined patterns to extract entities
    - Fast and deterministic
    - Good for structured data with known formats
    - Extensible via configuration files
    """
    
    def __init__(self, rules_config: Dict[str, Any], neo4j_config: Dict[str, Any]):
        """Initialize rule-based graph builder"""
        self.rules_config = rules_config
        self.neo4j_config = neo4j_config
        # Implementation would go here
        logger.info("Rule-based Graph Builder initialized")
    
    def create_knowledge_graph(self, system_id: str, processed_data: Dict[str, Any]) -> bool:
        """Create graph using predefined rules and patterns"""
        # Implementation would extract entities using regex patterns,
        # configuration templates, etc.
        logger.info(f"Creating rule-based knowledge graph for {system_id}")
        return True
    
    def get_supported_domains(self) -> List[str]:
        """Rule-based builder supports specific configured domains"""
        return ["infrastructure", "logs", "configurations"]
    
    def close(self):
        """Clean up rule-based builder resources"""
        pass

# Factory function for creating graph builders
def create_graph_builder(builder_type: str, **config) -> GraphBuilder:
    """
    Factory function to create graph builders
    
    Args:
        builder_type: Type of builder ('ai', 'rules', 'hybrid')
        **config: Configuration parameters for the builder
    
    Returns:
        GraphBuilder instance
    
    Example:
        builder = create_graph_builder(
            'ai',
            llm_config=llm_config,
            neo4j_config=neo4j_config
        )
    """
    if builder_type.lower() == 'ai':
        return AIGraphBuilder(
            llm_config=config['llm_config'],
            neo4j_config=config['neo4j_config']
        )
    elif builder_type.lower() == 'rules':
        return RuleBasedGraphBuilder(
            rules_config=config.get('rules_config', {}),
            neo4j_config=config['neo4j_config']
        )
    else:
        raise ValueError(f"Unknown graph builder type: {builder_type}")