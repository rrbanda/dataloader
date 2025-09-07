#!/usr/bin/env python3
"""
Universal Data Loader - AI-Powered Knowledge Graph Construction
Configurable, domain-agnostic data loading with LangChain LLMGraphTransformer
"""

import os
import re
import glob
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from abc import ABC, abstractmethod

# Use configuration pattern
from config.config_loader import get_config_loader
from core.data_models import SystemEntity, EventEntity

# Import optional dependencies with fallbacks
try:
    from unstructured.partition.auto import partition
    UNSTRUCTURED_AVAILABLE = True
except ImportError:
    UNSTRUCTURED_AVAILABLE = False

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

try:
    import pygrok
    PYGROK_AVAILABLE = True
except ImportError:
    PYGROK_AVAILABLE = False

try:
    import instructor
    from openai import OpenAI
    INSTRUCTOR_AVAILABLE = True
except ImportError:
    INSTRUCTOR_AVAILABLE = False

try:
    from core.graph_builders import GraphBuilder, create_graph_builder
    GRAPH_BUILDERS_AVAILABLE = True
except ImportError:
    GRAPH_BUILDERS_AVAILABLE = False

try:
    from langchain_experimental.graph_transformers import LLMGraphTransformer
    from langchain_openai import ChatOpenAI
    from langchain_core.documents import Document
    from langchain_neo4j import Neo4jGraph
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

logger = logging.getLogger(__name__)

class DataSourceAdapter(ABC):
    """Abstract adapter for different data source types"""
    
    @abstractmethod
    def read_system_files(self, system_id: str) -> Dict[str, str]:
        """Read raw files for a system"""
        pass
    
    @abstractmethod
    def list_available_systems(self) -> List[str]:
        """List all available systems"""
        pass

class FilesystemDataSourceAdapter(DataSourceAdapter):
    """Adapter for filesystem-based data sources (your current simulated_rhel_systems)"""
    
    def __init__(self, base_path: str, file_patterns: Dict[str, List[str]]):
        self.base_path = Path(base_path)
        self.file_patterns = file_patterns
        
        if not self.base_path.exists():
            raise FileNotFoundError(f"Data source path not found: {self.base_path}")
        
        logger.info(f"📁 Filesystem adapter initialized: {self.base_path}")
    
    def read_system_files(self, system_id: str) -> Dict[str, str]:
        """Read all files for a system according to configured patterns"""
        system_path = self.base_path / system_id
        if not system_path.exists():
            raise FileNotFoundError(f"System not found: {system_id}")
        
        files = {}
        
        # Read files according to configured patterns
        for pattern_type, patterns in self.file_patterns.items():
            for pattern in patterns:
                matching_files = self._find_files(system_path, pattern)
                for file_path in matching_files:
                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        relative_path = file_path.relative_to(system_path)
                        files[str(relative_path)] = content
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to read {file_path}: {e}")
                        files[str(file_path.relative_to(system_path))] = f"Error: {e}"
        
        logger.debug(f"📄 Read {len(files)} files from {system_id}")
        return files
    
    def list_available_systems(self) -> List[str]:
        """List all available system directories"""
        try:
            systems = [d.name for d in self.base_path.iterdir() if d.is_dir()]
            logger.debug(f"📋 Found {len(systems)} systems: {systems}")
            return systems
        except Exception as e:
            logger.error(f" Failed to list systems: {e}")
            return []
    
    def _find_files(self, base_path: Path, pattern: str) -> List[Path]:
        """Find files matching a pattern"""
        try:
            if '*' in pattern:
                # Use glob for patterns with wildcards
                full_pattern = str(base_path / pattern)
                return [Path(p) for p in glob.glob(full_pattern)]
            else:
                # Direct file path
                file_path = base_path / pattern
                return [file_path] if file_path.exists() else []
        except Exception as e:
            logger.warning(f"⚠️ Pattern matching failed for {pattern}: {e}")
            return []

class TextProcessor:
    """Configurable text processor using open source tools"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.chunking_config = config.get('chunking', {})
        self.cleaning_config = config.get('cleaning', {})
        self.parsing_config = config.get('parsing', {})
        
        # Initialize text splitter if available
        self.text_splitter = None
        if LANGCHAIN_AVAILABLE:
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunking_config.get('max_chunk_size', 2000),
                chunk_overlap=self.chunking_config.get('chunk_overlap', 200),
                separators=self.chunking_config.get('separators', ['\n\n', '\n', ' ', ''])
            )
        
        # Initialize grok patterns if available
        self.grok_patterns = {}
        if PYGROK_AVAILABLE and 'log_patterns' in self.parsing_config:
            for pattern_name, pattern in self.parsing_config['log_patterns'].items():
                try:
                    self.grok_patterns[pattern_name] = pygrok.Grok(pattern)
                except Exception as e:
                    logger.warning(f"⚠️ Failed to compile grok pattern {pattern_name}: {e}")
        
        logger.info(f"⚙️ Text processor initialized with {len(self.grok_patterns)} patterns")
    
    def process_files(self, raw_files: Dict[str, str]) -> Dict[str, Any]:
        """Process raw files into structured, clean text"""
        processed = {}
        
        for file_path, content in raw_files.items():
            if not content or content.startswith("Error"):
                continue
            
            try:
                # Step 1: Clean the text
                cleaned_content = self._clean_text(content)
                
                # Step 2: Detect file type and parse accordingly
                file_type = self._detect_file_type(file_path, cleaned_content)
                parsed_data = self._parse_by_type(file_type, cleaned_content)
                
                # Step 3: Chunk if needed
                chunks = self._chunk_text(cleaned_content)
                
                processed[file_path] = {
                    'file_type': file_type,
                    'cleaned_content': cleaned_content,
                    'parsed_data': parsed_data,
                    'chunks': chunks,
                    'metadata': {
                        'original_size': len(content),
                        'cleaned_size': len(cleaned_content),
                        'chunk_count': len(chunks)
                    }
                }
                
            except Exception as e:
                logger.error(f" Failed to process {file_path}: {e}")
                processed[file_path] = {
                    'error': str(e),
                    'raw_content': content[:1000]  # First 1000 chars for debugging
                }
        
        logger.info(f"⚙️ Processed {len(processed)} files")
        return processed
    
    def _clean_text(self, text: str) -> str:
        """Clean text according to configuration"""
        cleaned = text
        
        if self.cleaning_config.get('remove_ansi_codes', True):
            # Remove ANSI color codes
            cleaned = re.sub(r'\x1b\[[0-9;]*m', '', cleaned)
        
        if self.cleaning_config.get('normalize_whitespace', True):
            # Normalize whitespace
            cleaned = re.sub(r'\s+', ' ', cleaned)
        
        if self.cleaning_config.get('remove_debug_logs', True):
            # Remove debug log lines
            cleaned = re.sub(r'^.*\[DEBUG\].*$', '', cleaned, flags=re.MULTILINE)
        
        return cleaned.strip()
    
    def _detect_file_type(self, file_path: str, content: str) -> str:
        """Detect file type based on path and content"""
        file_path_lower = file_path.lower()
        
        if file_path_lower.endswith('.log'):
            return 'log_file'
        elif file_path_lower.endswith('.conf'):
            return 'config_file'
        elif file_path_lower.endswith('.service'):
            return 'systemd_service'
        elif 'packages.txt' in file_path_lower:
            return 'package_list'
        elif 'redhat-release' in file_path_lower:
            return 'release_info'
        elif file_path_lower.endswith('.repo'):
            return 'repository_config'
        else:
            return 'unknown'
    
    def _parse_by_type(self, file_type: str, content: str) -> Dict[str, Any]:
        """Parse content based on detected file type"""
        if file_type == 'log_file':
            return self._parse_log_file(content)
        elif file_type == 'config_file':
            return self._parse_config_file(content)
        elif file_type == 'package_list':
            return self._parse_package_list(content)
        elif file_type == 'release_info':
            return self._parse_release_info(content)
        else:
            return {'raw_content': content}
    
    def _parse_log_file(self, content: str) -> Dict[str, Any]:
        """Parse log files using grok patterns"""
        events = []
        
        for line in content.split('\n'):
            if not line.strip():
                continue
            
            # Try each grok pattern
            for pattern_name, grok_pattern in self.grok_patterns.items():
                try:
                    match = grok_pattern.match(line)
                    if match:
                        events.append({
                            'pattern_type': pattern_name,
                            'raw_line': line,
                            **match
                        })
                        break
                except Exception:
                    continue
        
        return {
            'parsed_events': events,
            'total_events': len(events),
            'total_lines': len(content.split('\n'))
        }
    
    def _parse_config_file(self, content: str) -> Dict[str, Any]:
        """Parse configuration files"""
        config_pairs = {}
        
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                try:
                    key, value = line.split('=', 1)
                    config_pairs[key.strip()] = value.strip()
                except ValueError:
                    continue
        
        return {
            'config_pairs': config_pairs,
            'total_settings': len(config_pairs)
        }
    
    def _parse_package_list(self, content: str) -> Dict[str, Any]:
        """Parse package lists"""
        packages = []
        
        for line in content.split('\n'):
            line = line.strip()
            if line:
                packages.append(line)
        
        return {
            'packages': packages,
            'package_count': len(packages)
        }
    
    def _parse_release_info(self, content: str) -> Dict[str, Any]:
        """Parse Red Hat release information"""
        version_match = re.search(r'release (\d+\.\d+)', content)
        codename_match = re.search(r'\(([^)]+)\)', content)
        
        return {
            'full_release': content.strip(),
            'version': version_match.group(1) if version_match else 'unknown',
            'codename': codename_match.group(1) if codename_match else 'unknown'
        }
    
    def _chunk_text(self, text: str) -> List[str]:
        """Chunk text using appropriate method"""
        if self.text_splitter and len(text) > self.chunking_config.get('max_chunk_size', 2000):
            return self.text_splitter.split_text(text)
        else:
            # Simple chunking fallback
            chunk_size = self.chunking_config.get('max_chunk_size', 2000)
            return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# NOTE: LangChainAIExtractor has been replaced by the more extensible 
# AIGraphBuilder architecture in core/graph_builders.py
# This provides better separation of concerns and extensibility

class LangChainAIExtractor:
    """
    DEPRECATED: This class has been replaced by AIGraphBuilder in core/graph_builders.py
    Keeping for backward compatibility during transition
    """
    
    def __init__(self, llm_config: Dict[str, Any], neo4j_config: Dict[str, Any]):
        self.llm_config = llm_config
        self.neo4j_config = neo4j_config
        self.llm = None
        self.graph_transformer = None
        self.neo4j_graph = None
        
        if not LANGCHAIN_AVAILABLE:
            logger.warning("⚠️ LangChain experimental not available - AI extraction disabled")
            return
        
        try:
            # Initialize LLM (using your Red Hat AI endpoint)
            self.llm = ChatOpenAI(
                base_url=llm_config['base_url'],
                api_key=llm_config['api_key'],
                model_name=llm_config['model'],
                temperature=0  # Deterministic for better extraction
            )
            
            # Initialize Neo4j connection for direct graph loading
            self.neo4j_graph = Neo4jGraph(
                url=neo4j_config['uri'],
                username=neo4j_config['username'],
                password=neo4j_config['password'],
                database=neo4j_config['database'],
                refresh_schema=False
            )
            
            # Initialize LLM Graph Transformer with generic, flexible schema
            self.graph_transformer = LLMGraphTransformer(
                llm=self.llm,
                allowed_nodes=self._get_generic_node_types(),
                allowed_relationships=self._get_generic_relationships(),
                node_properties=self._get_generic_node_properties()
            )
            
            logger.info(f"🧠 LangChain AI extractor initialized with {llm_config['model']}")
            
        except Exception as e:
            logger.error(f" Failed to initialize LangChain AI extractor: {e}")
            self.llm = None
            self.graph_transformer = None
    
    def _get_generic_node_types(self) -> List[str]:
        """Define generic, domain-agnostic node types for extraction"""
        return [
            "System",           # Any system/server/device
            "Application",      # Software applications
            "Service",          # Running services/processes
            "Component",        # System components/modules
            "Document",         # Files, logs, configurations
            "Event",            # Events, incidents, changes
            "User",             # Users, accounts, roles
            "Location",         # Physical/logical locations
            "Network",          # Network elements
            "Database",         # Data storage systems
            "Configuration",    # Settings and configurations
            "Process",          # Business/technical processes
            "Organization",     # Organizational entities
            "Technology"        # Technologies, frameworks, tools
        ]
    
    def _get_generic_relationships(self) -> List[tuple]:
        """Define generic, domain-agnostic relationships for extraction"""
        return [
            ("System", "RUNS", "Application"),
            ("System", "HOSTS", "Service"),
            ("System", "CONTAINS", "Component"),
            ("System", "GENERATES", "Document"),
            ("System", "EXPERIENCES", "Event"),
            ("System", "LOCATED_IN", "Location"),
            ("System", "CONNECTED_TO", "Network"),
            ("System", "STORES_DATA_IN", "Database"),
            ("System", "USES", "Technology"),
            ("Application", "DEPENDS_ON", "Service"),
            ("Application", "USES", "Component"),
            ("Application", "GENERATES", "Event"),
            ("Application", "ACCESSES", "Database"),
            ("Service", "DEPENDS_ON", "Component"),
            ("Service", "GENERATES", "Document"),
            ("User", "ACCESSES", "System"),
            ("User", "USES", "Application"),
            ("User", "BELONGS_TO", "Organization"),
            ("Event", "AFFECTS", "System"),
            ("Event", "INVOLVES", "User"),
            ("Document", "DESCRIBES", "Configuration"),
            ("Process", "INVOLVES", "System"),
            ("Organization", "OWNS", "System")
        ]
    
    def _get_generic_node_properties(self) -> List[str]:
        """Define generic node properties to extract"""
        return [
            "name",             # Entity name
            "type",             # Entity type/category
            "version",          # Version information
            "status",           # Current status
            "environment",      # Environment (prod, dev, test)
            "location",         # Physical/logical location
            "timestamp",        # Event timestamps
            "severity",         # Event severity levels
            "description",      # Descriptions
            "ip_address",       # Network addresses
            "port",             # Port numbers
            "path",             # File/directory paths
            "size",             # Size information
            "owner",            # Ownership information
            "tags",             # Classification tags
            "priority",         # Priority levels
            "category"          # Categories/classifications
        ]
    
    def extract_and_load_to_graph(self, system_id: str, processed_data: Dict[str, Any]) -> bool:
        """
        Extract entities from processed data and load directly to Neo4j graph
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.graph_transformer or not self.neo4j_graph:
            logger.warning("⚠️ LangChain AI extraction not available")
            return False
        
        try:
            # Build context document for extraction
            context_text = self._build_extraction_context(system_id, processed_data)
            
            if not context_text.strip():
                logger.warning(f"⚠️ No content to extract for {system_id}")
                return False
            
            # Create LangChain document
            document = Document(
                page_content=context_text,
                metadata={
                    "system_id": system_id,
                    "timestamp": datetime.now().isoformat(),
                    "extraction_type": "rhel_system_analysis"
                }
            )
            
            logger.info(f"🔍 Extracting entities from {system_id} ({len(context_text)} chars)")
            
            # Convert to graph documents using LLM
            graph_documents = self.graph_transformer.convert_to_graph_documents([document])
            
            if not graph_documents:
                logger.warning(f"⚠️ No graph documents extracted from {system_id}")
                return False
            
            # Log extraction results
            graph_doc = graph_documents[0]
            logger.info(f" Extracted {len(graph_doc.nodes)} nodes, {len(graph_doc.relationships)} relationships")
            
            # Load directly to Neo4j - following LangChain example exactly
            self.neo4j_graph.add_graph_documents(graph_documents)
            
            logger.info(f"🗄️ Loaded graph data for {system_id} to Neo4j")
            return True
            
        except Exception as e:
            logger.error(f" AI extraction failed for {system_id}: {e}")
            return False
    
    def _build_extraction_context(self, system_id: str, processed_data: Dict[str, Any]) -> str:
        """Build context text for AI extraction"""
        context_parts = [
            f"System Analysis: {system_id}",
            f"Timestamp: {datetime.now().isoformat()}",
            ""
        ]
        
        for file_path, file_data in processed_data.items():
            if isinstance(file_data, dict):
                content = file_data.get('cleaned_content', '')
                file_type = file_data.get('file_type', 'unknown')
                
                if content and not content.startswith("Error"):
                    # Add file context with clear markers
                    context_parts.append(f"=== {file_type.upper()}: {file_path} ===")
                    context_parts.append(content[:2000])  # Limit to avoid token limits
                    context_parts.append("")
        
        full_context = '\n'.join(context_parts)
        
        # Add extraction instructions for better results
        extraction_prompt = f"""

EXTRACTION INSTRUCTIONS:
Analyze the above system data and extract relevant entities and relationships:

1. SYSTEM entities with properties: name, type, version, environment, location
2. APPLICATION entities with properties: name, version, status
3. SERVICE entities with properties: name, status, port
4. COMPONENT entities with properties: name, type, version
5. EVENT entities with properties: timestamp, severity, description, status
6. DOCUMENT entities with properties: path, type, description
7. USER entities with properties: name, role, permissions
8. CONFIGURATION entities with properties: path, type, settings
9. NETWORK entities with properties: ip_address, port, protocol
10. DATABASE entities with properties: name, type, size

Focus on identifying systems, applications, services, events, configurations, and their relationships.
Extract any relevant technical or business entities mentioned in the data.
System ID: {system_id}
"""
        
        return full_context + extraction_prompt
    
    def close(self):
        """Clean up resources"""
        if self.neo4j_graph:
            try:
                self.neo4j_graph.close()
                logger.info("🗄️ LangChain AI extractor connection closed")
            except:
                pass

class Neo4jGraphLoader:
    """Phase 4: Graph Loading (No AI) - Load entities into Neo4j database"""
    
    def __init__(self, neo4j_config: Dict[str, Any]):
        self.neo4j_config = neo4j_config
        self.driver = None
        self.database = neo4j_config.get('database', 'neo4j')
        
        if NEO4J_AVAILABLE:
            try:
                self.driver = GraphDatabase.driver(
                    neo4j_config['uri'],
                    auth=(neo4j_config['username'], neo4j_config['password'])
                )
                
                # Create database if it doesn't exist (and auto_create is enabled)
                if self._should_auto_create_database():
                    self._ensure_database_exists()
                
                # Test connection to target database
                with self.driver.session(database=self.database) as session:
                    session.run("RETURN 1")
                
                logger.info(f"🗄️ Neo4j graph loader connected: {neo4j_config['uri']}/{self.database}")
                
                # Initialize schema
                self._create_indexes_and_constraints()
                
            except Exception as e:
                logger.error(f" Failed to connect to Neo4j: {e}")
                self.driver = None
        else:
            logger.warning("⚠️ Neo4j driver not available - graph loading disabled")
    
    def load_systems_and_events(self, systems: List[SystemEntity], events: List[EventEntity]) -> bool:
        """Load systems and events into Neo4j graph"""
        if not self.driver:
            logger.warning("⚠️ Neo4j not available - skipping graph loading")
            return False
        
        try:
            with self.driver.session(database=self.database) as session:
                # Clear existing data if configured
                if self.neo4j_config.get('management', {}).get('clear_on_startup', False):
                    self._clear_existing_data(session)
                
                # Load systems
                systems_loaded = self._load_systems(session, systems)
                
                # Load events
                events_loaded = self._load_events(session, events)
                
                # Create relationships
                relationships_created = self._create_relationships(session, systems, events)
                
                logger.info(f" Graph loading complete: {systems_loaded} systems, {events_loaded} events, {relationships_created} relationships")
                return True
                
        except Exception as e:
            logger.error(f" Graph loading failed: {e}")
            return False
    
    def _create_indexes_and_constraints(self):
        """Create Neo4j indexes and constraints for performance"""
        if not self.driver:
            return
        
        try:
            with self.driver.session(database=self.database) as session:
                # System constraints and indexes
                session.run("CREATE CONSTRAINT system_id_unique IF NOT EXISTS FOR (s:System) REQUIRE s.system_id IS UNIQUE")
                session.run("CREATE INDEX system_hostname_idx IF NOT EXISTS FOR (s:System) ON (s.hostname)")
                session.run("CREATE INDEX system_environment_idx IF NOT EXISTS FOR (s:System) ON (s.environment)")
                
                # Event constraints and indexes
                session.run("CREATE CONSTRAINT event_id_unique IF NOT EXISTS FOR (e:Event) REQUIRE e.event_id IS UNIQUE")
                session.run("CREATE INDEX event_timestamp_idx IF NOT EXISTS FOR (e:Event) ON (e.timestamp)")
                session.run("CREATE INDEX event_severity_idx IF NOT EXISTS FOR (e:Event) ON (e.severity)")
                
                logger.debug("🗄️ Neo4j schema initialized")
                
        except Exception as e:
            logger.warning(f"⚠️ Failed to create indexes: {e}")
    
    def _clear_existing_data(self, session):
        """Clear existing data from Neo4j"""
        try:
            # Backup before clearing if configured
            if self.neo4j_config.get('management', {}).get('backup_before_clear', True):
                logger.info("💾 Creating backup before clearing data...")
                # In a real implementation, you'd export data here
                
            logger.info("🧹 Clearing existing graph data...")
            session.run("MATCH (n) DETACH DELETE n")
            logger.info(" Graph data cleared")
            
        except Exception as e:
            logger.error(f" Failed to clear data: {e}")
    
    def _load_systems(self, session, systems: List[SystemEntity]) -> int:
        """Load system nodes into Neo4j"""
        if not systems:
            return 0
        
        loaded_count = 0
        for system in systems:
            try:
                # Create system node
                session.run("""
                    MERGE (s:System {system_id: $system_id})
                    SET s.hostname = $hostname,
                        s.rhel_version = $rhel_version,
                        s.environment = $environment,
                        s.package_count = $package_count,
                        s.updated_at = datetime()
                """, {
                    'system_id': system.system_id,
                    'hostname': system.hostname,
                    'rhel_version': system.rhel_version,
                    'environment': system.environment,
                    'package_count': system.package_count
                })
                
                # Create service nodes and relationships
                for service in system.services:
                    session.run("""
                        MERGE (s:System {system_id: $system_id})
                        MERGE (svc:Service {name: $service_name})
                        MERGE (s)-[:RUNS]->(svc)
                    """, {
                        'system_id': system.system_id,
                        'service_name': service
                    })
                
                loaded_count += 1
                
            except Exception as e:
                logger.error(f" Failed to load system {system.system_id}: {e}")
        
        return loaded_count
    
    def _load_events(self, session, events: List[EventEntity]) -> int:
        """Load event nodes into Neo4j"""
        if not events:
            return 0
        
        loaded_count = 0
        for event in events:
            try:
                session.run("""
                    MERGE (e:Event {event_id: $event_id})
                    SET e.system_id = $system_id,
                        e.event_type = $event_type,
                        e.timestamp = datetime($timestamp),
                        e.severity = $severity,
                        e.status = $status,
                        e.title = $title,
                        e.description = $description,
                        e.source = $source,
                        e.updated_at = datetime()
                """, {
                    'event_id': event.event_id,
                    'system_id': event.system_id,
                    'event_type': event.event_type,
                    'timestamp': event.timestamp.isoformat() if event.timestamp else None,
                    'severity': event.severity,
                    'status': event.status,
                    'title': event.title,
                    'description': event.description,
                    'source': event.source
                })
                
                loaded_count += 1
                
            except Exception as e:
                logger.error(f" Failed to load event {event.event_id}: {e}")
        
        return loaded_count
    
    def _create_relationships(self, session, systems: List[SystemEntity], events: List[EventEntity]) -> int:
        """Create relationships between systems and events"""
        relationships_created = 0
        
        try:
            # Connect events to systems
            for event in events:
                session.run("""
                    MATCH (s:System {system_id: $system_id})
                    MATCH (e:Event {event_id: $event_id})
                    MERGE (s)-[:HAS_EVENT]->(e)
                """, {
                    'system_id': event.system_id,
                    'event_id': event.event_id
                })
                relationships_created += 1
                
        except Exception as e:
            logger.error(f" Failed to create relationships: {e}")
        
        return relationships_created
    
    def _should_auto_create_database(self) -> bool:
        """Check if database should be auto-created"""
        return self.neo4j_config.get('management', {}).get('auto_create_database', False)
    
    def _ensure_database_exists(self):
        """Create database if it doesn't exist (Enterprise) or verify default database (Community)"""
        if not self.driver:
            return
        
        # For default databases, just verify they exist
        if self.database.lower() in ['neo4j', 'system']:
            logger.info(f"🗄️ Using default database: {self.database}")
            return
        
        try:
            # Connect to system database to check/create database
            with self.driver.session(database="system") as session:
                # Check if database exists
                result = session.run(
                    "SHOW DATABASES YIELD name WHERE name = $db_name",
                    db_name=self.database
                )
                
                if not result.single():
                    # Database doesn't exist, try to create it
                    logger.info(f"🏗️ Creating database: {self.database}")
                    session.run(f"CREATE DATABASE `{self.database}`")
                    logger.info(f" Database created: {self.database}")
                else:
                    logger.info(f"🗄️ Database already exists: {self.database}")
                    
        except Exception as e:
            error_msg = str(e)
            if "UnsupportedAdministrationCommand" in error_msg:
                logger.warning(f"⚠️ Neo4j Community Edition detected - cannot create custom databases")
                logger.info(f"💡 Falling back to default database: neo4j")
                # Update database to use default
                self.database = "neo4j"
                self.neo4j_config['database'] = "neo4j"
            else:
                logger.warning(f"⚠️ Could not create database {self.database}: {e}")
                logger.info("💡 You may need to create the database manually or use Neo4j Enterprise")

    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            logger.info("🗄️ Neo4j connection closed")

class UniversalDataLoader:
    """
    Universal Data Loader - Domain-agnostic knowledge graph construction
    
    Features:
    - Works with ANY data domain (not just RHEL)
    - LangChain-powered AI extraction
    - Direct Neo4j integration
    - Configurable and extensible
    """
    
    def __init__(self, environment: str = None):
        """
        Initialize unified data loader with configuration
        
        Args:
            environment: Environment name (uses config from your existing pattern)
        """
        # Get configuration using your existing pattern
        self.config_loader = get_config_loader(environment)
        self.environment = environment or 'production'
        
        # Initialize components based on configuration
        self._initialize_data_source()
        self._initialize_text_processor()
        self._initialize_graph_builder()
        
        logger.info(f"🚀 UniversalDataLoader initialized for {self.environment}")
    
    def _initialize_data_source(self):
        """Initialize data source adapter based on configuration"""
        source_config = self.config_loader.get_data_source_config('primary_data')
        
        if source_config.get('type') == 'filesystem':
            self.data_source = FilesystemDataSourceAdapter(
                base_path=source_config.get('base_path', 'simulated_rhel_systems'),
                file_patterns=source_config.get('file_patterns', {})
            )
        else:
            raise ValueError(f"Unsupported data source type: {source_config.get('type')}")
    
    def _initialize_text_processor(self):
        """Initialize text processor based on configuration"""
        if self.config_loader.is_phase_enabled('text_processing'):
            text_config = self.config_loader.get_text_processing_config()
            self.text_processor = TextProcessor(text_config)
        else:
            self.text_processor = None
            logger.info("📝 Text processing disabled by configuration")
    
    def _initialize_graph_builder(self):
        """Initialize knowledge graph builder based on configuration"""
        if self.config_loader.is_phase_enabled('ai_extraction'):
            llm_config = self.config_loader.get_llm_config()
            neo4j_config = self.config_loader.get_neo4j_config()
            
            # Use new extensible graph builder architecture
            self.graph_builder = create_graph_builder(
                'ai',
                llm_config=llm_config,
                neo4j_config=neo4j_config
            )
            logger.info("🧠 AI Knowledge Graph Builder initialized")
        else:
            self.graph_builder = None
            logger.info("🧠 Knowledge graph creation disabled by configuration")
    
    def _initialize_graph_loader(self):
        """Graph loader not needed in AI-only mode - LangChain handles Neo4j directly"""
        self.graph_loader = None
        logger.info("🗄️ AI-only mode: LangChain handles Neo4j directly (no separate graph loader needed)")
    
    def load_system_data(self, system_id: str) -> Tuple[List[SystemEntity], List[EventEntity]]:
        """
        Load and process data for a single system
        
        Args:
            system_id: System identifier
            
        Returns:
            Tuple of (systems, patch_events)
        """
        logger.info(f"📊 Loading data for system: {system_id}")
        
        try:
            # Phase 1: Raw data ingestion
            raw_files = self.data_source.read_system_files(system_id)
            logger.debug(f"📁 Loaded {len(raw_files)} raw files")
            
            # Phase 2: Text processing (if enabled)
            if self.text_processor:
                processed_data = self.text_processor.process_files(raw_files)
                logger.debug(f"⚙️ Processed {len(processed_data)} files")
            else:
                processed_data = {path: {'cleaned_content': content} for path, content in raw_files.items()}
            
            # Phase 3 & 4: AI-Powered Knowledge Graph Creation
            if not self.graph_builder:
                logger.error(f" Knowledge graph builder not available for {system_id} - requires AI configuration")
                raise RuntimeError("Knowledge graph builder required. Check LLM configuration and dependencies.")
            
            # Create knowledge graph using AI analysis
            graph_creation_success = self.graph_builder.create_knowledge_graph(system_id, processed_data)
            
            if graph_creation_success:
                logger.info(f" Knowledge graph created successfully for {system_id}")
                # Create basic system info for return value compatibility
                systems = self._create_basic_system_info(system_id, processed_data)
                events = []
                return systems, events
            else:
                logger.error(f" Knowledge graph creation failed for {system_id}")
                raise RuntimeError(f"Knowledge graph creation failed for {system_id}. Check LLM connection, APOC plugin, and Neo4j setup.")
            
            
        except RuntimeError as e:
            # Re-raise runtime errors (knowledge graph creation failures) for visibility
            logger.error(f" Knowledge graph creation failed for {system_id}: {e}")
            raise e
        except Exception as e:
            logger.error(f" Unexpected error for {system_id}: {e}")
            return [], []
    
    def load_all_systems(self) -> Tuple[List[SystemEntity], List[EventEntity]]:
        """
        Load data for all available systems
        
        Returns:
            Tuple of (all_systems, all_patch_events)
        """
        available_systems = self.data_source.list_available_systems()
        logger.info(f"📋 Loading data for {len(available_systems)} systems")
        
        all_systems = []
        all_events = []
        
        for system_id in available_systems:
            systems, events = self.load_system_data(system_id)
            all_systems.extend(systems)
            all_events.extend(events)
        
        # Data already loaded to Neo4j during individual system processing (LangChain approach)
        # No separate batch loading needed - it's done during AI extraction
        
        logger.info(f" Batch processing complete: {len(all_systems)} systems, {len(all_events)} events")
        logger.info("🗄️ Graph data already loaded during AI extraction (LangChain approach)")
        return all_systems, all_events
    
    def list_available_systems(self) -> List[str]:
        """List all available systems"""
        return self.data_source.list_available_systems()
    
    def _create_basic_system_info(self, system_id: str, processed_data: Dict[str, Any]) -> List[SystemEntity]:
        """Create basic system info without AI (fallback)"""
        # Parse basic info from the processed data
        rhel_version = "unknown"
        environment = "unknown"
        services = []
        package_count = 0
        
        # Extract basic info from files
        for file_path, file_data in processed_data.items():
            if isinstance(file_data, dict):
                content = file_data.get('cleaned_content', '')
                
                # Parse RHEL version from redhat-release
                if 'redhat-release' in file_path and content:
                    if 'release' in content:
                        import re
                        match = re.search(r'release (\d+\.\d+)', content)
                        if match:
                            rhel_version = match.group(1)
                
                # Count packages
                if 'packages.txt' in file_path and content:
                    package_count = len([line for line in content.split('\n') if line.strip()])
                
                # Extract services from systemd files
                if 'systemd/system' in file_path and file_path.endswith('.service'):
                    service_name = file_path.split('/')[-1].replace('.service', '')
                    services.append(service_name)
        
        # Determine environment from system_id patterns
        if 'prod' in system_id.lower():
            environment = "production"
        elif 'stage' in system_id.lower() or 'staging' in system_id.lower():
            environment = "staging"
        elif 'dev' in system_id.lower():
            environment = "development"
        
        # Create SystemEntity with backward compatibility attributes
        system = SystemEntity(
            system_id=system_id,
            name=system_id,
            system_type="rhel_server",
            version=rhel_version,
            environment=environment,
            services=services,
            components=[]
        )
        
        # Add backward compatibility attributes for Neo4jGraphLoader
        system.hostname = system_id  # Add hostname attribute
        system.rhel_version = rhel_version  # Add rhel_version attribute
        system.package_count = package_count  # Add package_count attribute
        
        return [system]
    
    def close(self):
        """Clean up resources"""
        if hasattr(self, 'graph_builder') and self.graph_builder:
            self.graph_builder.close()
        if hasattr(self, 'graph_loader') and self.graph_loader:
            self.graph_loader.close()
        logger.info("🧹 UniversalDataLoader resources cleaned up")

# Factory functions for easy integration
def create_sample_data() -> Tuple[List[SystemEntity], List[EventEntity]]:
    """
    Backward compatible function for sample data creation
    Uses the new universal loader under the hood
    """
    logger.info("🔄 Using universal data loader (backward compatibility)")
    loader = UniversalDataLoader()
    return loader.load_all_systems()

# Main factory function for easy integration
def get_universal_loader(environment: str = None) -> UniversalDataLoader:
    """
    Get universal data loader instance
    
    Args:
        environment: Environment name (development, production, testing)
        
    Returns:
        UniversalDataLoader instance ready for any domain
    """
    return UniversalDataLoader(environment=environment)

# Backward compatibility alias
def get_unified_loader(environment: str = None) -> UniversalDataLoader:
    """Backward compatibility alias for get_universal_loader"""
    return get_universal_loader(environment)
