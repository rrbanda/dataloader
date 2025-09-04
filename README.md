# 🚀 Universal DataLoader

**AI-Powered Knowledge Graph Construction for Any Domain**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-green.svg)](https://python.langchain.com/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.0+-red.svg)](https://neo4j.com/)

Transform unstructured data from **any domain** into rich knowledge graphs using **LangChain** and **Neo4j**. Works with servers, applications, documents, network devices, security data, and more!

## 🎯 What This DataLoader Actually Does (Start to End)

**Input:** Raw text files (logs, configs, documents) from any domain  
**Output:** Sophisticated knowledge graph in Neo4j with AI-extracted entities and relationships

### The Complete Pipeline (Real Implementation):

1. **📁 File Discovery**: Scans `simulated_rhel_systems/` directory for system files (.log, .txt, .conf files)

2. **📖 Text Processing**: 
   - Reads and cleans file content (removes ANSI codes, normalizes whitespace)
   - Applies Grok patterns to extract structured data from logs
   - Chunks large files for optimal AI processing

3. **🧠 AI Knowledge Graph Creation** (The Core Magic):
   - Uses **LangChain LLMGraphTransformer** with **Red Hat AI endpoint**
   - **Automatically builds visual graph**: Systems, Services, Applications, Components, Events, Configurations
   - **Creates smart connections**: RUNS, DEPENDS_ON, CONTAINS, HOSTS
   - **No manual rules** - pure AI understanding creates the knowledge graph

4. **🗄️ Neo4j Loading**:
   - Connects to your Neo4j Desktop instance  
   - Uses APOC procedures for efficient bulk loading
   - Creates searchable, visual knowledge graph

### Real Results (Tested & Verified):
- **Input**: 5 simulated RHEL systems with configs and logs
- **AI Processing**: LangChain + Red Hat AI model analyzes text
- **Output**: 39 nodes + 16 relationships in Neo4j  
- **Entity Types**: System, Service, Application, Component, Event, Configuration
- **Time**: ~30 seconds for complete pipeline

## 🚀 Ready for Graph RAG & LangGraph Integration

This dataloader creates the **foundation knowledge graph** needed for advanced RAG applications:

### ✅ **What's Ready Now:**
- **Rich Knowledge Graph**: AI-extracted entities with semantic relationships
- **Neo4j Integration**: Production-ready graph database with APOC support
- **LangChain Compatible**: Direct integration with LangChain ecosystem
- **Configurable Pipeline**: Easy to extend for new data sources and domains

### 🔮 **Perfect for Building:**
- **Graph RAG Systems**: Query the knowledge graph for contextual information
- **LangGraph Agents**: Multi-step reasoning over your knowledge graph
- **Semantic Search**: Vector embeddings + graph traversal for enhanced retrieval
- **Domain-Specific AI**: Train models on your graph-structured data

### 🎯 **Next Steps for Graph RAG:**
1. **Add vector embeddings** for semantic similarity search
2. **Implement graph traversal algorithms** for context expansion
3. **Create LangGraph workflows** for intelligent query processing
4. **Build RAG chains** that combine vector search + graph relationships

The hard part (knowledge graph creation) is **done** ✅ — now you can focus on the AI applications!

## ✨ Universal & Domain-Agnostic

Works with **any data domain**:
- 🖥️ **IT Infrastructure** (servers, networks, applications)
- 📊 **Business Systems** (processes, organizations, users)  
- 📚 **Document Analysis** (manuals, reports, logs)
- 🔒 **Security Data** (incidents, vulnerabilities, compliance)
- 🏭 **Industrial Systems** (IoT, manufacturing, monitoring)
- 🏥 **Healthcare** (systems, processes, documentation)
- 💰 **Financial** (transactions, systems, compliance)

## ⭐ Key Features

- 🤖 **LangChain-Powered AI**: Uses `LLMGraphTransformer` for reliable entity extraction
- 🗄️ **Direct Neo4j Integration**: Automatic schema creation and data loading
- 🔧 **Configuration-Driven**: YAML-based configuration for easy customization
- 🌍 **Domain-Agnostic**: Works with any data type - not limited to specific domains
- 📁 **Flexible Data Sources**: Filesystem, APIs, databases (easily extensible)
- 🏗️ **4-Phase Pipeline**: Raw ingestion → Text processing → AI extraction → Graph loading
- 🔒 **Production-Ready**: Environment-aware configuration and error handling
- 🚀 **Easy Integration**: Simple Python API with minimal setup

## 🎯 Perfect For

- **DevOps & Infrastructure**: Server configs, logs, monitoring data
- **Security Analysis**: Incident reports, vulnerability scans, compliance data  
- **Business Intelligence**: Process documentation, organizational data
- **Document Analysis**: Technical manuals, reports, knowledge bases
- **Application Monitoring**: Service dependencies, performance metrics
- **Research & Analysis**: Any unstructured text data requiring graph representation

## 🏗️ 4-Phase AI Pipeline

### How It Works: From Raw Data to Knowledge Graph

**Phase 1: Raw Data Ingestion**
- Reads files from filesystem (logs, configs, documents)
- Supports multiple file formats (.log, .txt, .yaml, .json, .conf, etc.)
- No AI required - pure file system operations

**Phase 2: Text Processing** 
- Cleans ANSI codes, normalizes whitespace
- Applies Grok patterns for structured log parsing
- Chunks large files for AI processing
- Uses LangChain's RecursiveCharacterTextSplitter

**Phase 3: AI Knowledge Graph Creation** (The Magic ✨)
- **Reads your files with AI** using LangChain LLMGraphTransformer + Red Hat AI
- **Finds entities**: `System`, `Service`, `Application`, `Component`, `Event`, `Configuration`
- **Creates connections**: `RUNS`, `DEPENDS_ON`, `CONTAINS`, `HOSTS`
- **Builds visual graph**: Interactive knowledge graph in Neo4j
- **Works with any domain**: Not limited to IT - handles business docs, security data, etc.

**Phase 4: Graph Storage & Visualization**
- **Stores in Neo4j**: Direct integration via LangChain Neo4jGraph
- **Creates database structure**: Automatic schema and indexes
- **Ready for exploration**: Query and visualize in Neo4j Desktop
- **Graph RAG ready**: Perfect foundation for intelligent retrieval

## 📂 Directory Structure (Clean & Focused)

```
dataloader/
├── 📁 core/                    # Core functionality  
│   ├── unified_dataloader.py   # AI-powered dataloader (LangChain + Red Hat AI)
│   └── data_models.py          # Generic data models for any domain
├── 📁 config/                  # Configuration management
│   ├── config_loader.py        # Configuration loader with environment support
│   ├── data_loader_config.yaml # Main config (Red Hat AI + Neo4j Desktop)
│   └── universal_dataloader_config.yaml  # Alternative config template
├── 📁 tests/                   # Comprehensive test suite
│   ├── test_unified_loader.py  # Core dataloader tests
│   ├── test_langchain_approach.py  # AI extraction tests
│   └── test_*.py               # Additional test cases
├── 📁 utils/                   # Essential utilities
│   └── rhel_filesystem_generator.py  # Generate realistic RHEL test data
├── 📁 simulated_rhel_systems/  # Generated test data (5 RHEL systems)
│   ├── app-prod-01/            # Production app server
│   ├── db-prod-01/             # Production database server  
│   ├── web-prod-01/            # Production web server
│   ├── web-prod-02/            # Production web server 2
│   └── web-stage-01/           # Staging web server
├── 📊 test_setup.py           # Main test runner
├── ⚙️ setup_environment.sh    # Environment variable setup
├── 🚀 setup_local_dev.sh     # Quick development setup script
├── 📦 requirements.txt        # Python dependencies
├── 📚 README.md               # Complete documentation (this file)
└── 📄 LICENSE                 # Apache 2.0 license
```

## 🚀 Quick Start

**Complete setup in 15 minutes - Follow these steps in order:**

### 1. Prerequisites (Install These First)

**Required Software:**
- ✅ **Python 3.9+** - [Download here](https://www.python.org/downloads/)
- ✅ **Git** - [Download here](https://git-scm.com/downloads) 
- ✅ **Neo4j Desktop** - [Download here](https://neo4j.com/download/) **(REQUIRED - Must install before proceeding)**

### 2. Setup Neo4j Desktop (Do This First!)

**🚨 IMPORTANT: Complete Neo4j setup before cloning the repository!**

1. **Install Neo4j Desktop** from [neo4j.com/download](https://neo4j.com/download/)
2. **Open Neo4j Desktop** → Create account (free) → Sign in
3. **Create New Project**:
   - Click "New" → "Create Project" 
   - Name it "dataloader-project"
4. **Add Database**:
   - Click "Add" → "Local DBMS"
   - Name: `dataloader-db`
   - Password: `password` (exactly this - needed for config)
   - Version: Latest (5.x recommended)
   - Click "Create"
5. **Install APOC Plugin** (CRITICAL for AI extraction):
   - Select your `dataloader-db` → Click "Plugins" tab
   - Find "APOC" → Click "Install" 
   - Wait for installation to complete
6. **Start Your Database**:
   - Click the ▶️ "Start" button
   - Wait for "Running" status (green dot)
   - Connection URI will be: `neo4j://127.0.0.1:7687`

**✅ Verify Neo4j Setup:**
- Database shows "Running" with green dot
- APOC plugin shows "Installed" 
- You can click "Open" to see Neo4j Browser

### 3. Clone & Setup Python Environment

```bash
# Clone the repository
git clone https://github.com/rrbanda/dataloader.git
cd dataloader

# Setup Python environment and dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Generate sample data
python utils/rhel_filesystem_generator.py
```

### 4. Configure Environment Variables

```bash
# Setup all environment variables (LLM + Neo4j)
source setup_environment.sh
```

**This configures:**
- ✅ **Red Hat AI endpoint** (pre-configured and working)
- ✅ **Neo4j connection** (matches your Desktop setup)
- ✅ **All required variables** for the dataloader

### 5. Run the AI-Powered DataLoader

```bash
# Test basic setup first
python test_setup.py

# Run the AI-powered knowledge graph creation
python -c "
from core.unified_dataloader import get_universal_loader

print('🚀 Starting AI-powered knowledge graph creation...')
loader = get_universal_loader('development')
systems, events = loader.load_all_systems()
loader.close()
print(f'✅ SUCCESS! Loaded {len(systems)} systems, {len(events)} events to Neo4j!')
"
```

**What This Does:**
1. **Reads** 5 simulated RHEL systems from `simulated_rhel_systems/`
2. **Processes** logs, configs, and system files using LangChain
3. **Creates visual knowledge graph** using Red Hat AI + LLMGraphTransformer
4. **Stores interactive graph** in your Neo4j Desktop database

### 6. View Your AI-Generated Knowledge Graph

1. **Open Neo4j Desktop** → Select your `dataloader-db` 
2. **Click "Open"** to launch Neo4j Browser
3. **Run this query** to see your knowledge graph:
   ```cypher
   MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 25
   ```

**🎉 Expected Results (Verified Working):**
- ✅ **~39 sophisticated nodes** extracted by Red Hat AI
- ✅ **~16 meaningful relationships** between entities  
- ✅ **Entity types**: `System`, `Service`, `Application`, `Component`, `Event`, `Configuration`
- ✅ **Relationship types**: `RUNS`, `DEPENDS_ON`, `CONTAINS`, `HOSTS`
- ✅ **Visual, interactive graph** you can explore and query

### 7. Troubleshooting

**If you get connection errors:**
```bash
# Check if Neo4j is running
# In Neo4j Desktop: database should show green "Running" status

# Verify environment variables
echo $NEO4J_URI        # Should be: neo4j://127.0.0.1:7687
echo $NEO4J_PASSWORD   # Should be: password
```

**If AI extraction fails:**
```bash
# Check Red Hat AI connection
echo $OPENAI_BASE_URL  # Should show Red Hat AI endpoint
python -c "from langchain_openai import ChatOpenAI; print('✅ LangChain working')"
```

**Common Issues:**
- ❌ **"APOC not found"** → Install APOC plugin in Neo4j Desktop
- ❌ **"Connection refused"** → Start your Neo4j database  
- ❌ **"Database not found"** → Use database name `neo4j` (default)
- ❌ **"Authentication failed"** → Check password is exactly `password`

### 8. Explore Your AI-Generated Knowledge Graph

**View all entity types and their counts:**
```cypher
CALL db.labels() YIELD label
CALL apoc.cypher.run('MATCH (n:`' + label + '`) RETURN COUNT(n) as count', {}) YIELD value
RETURN label, value.count as count
```

**Explore relationships between entities:**
```cypher
// See what systems contain
MATCH (s:System)-[r:CONTAINS]->(c) RETURN s.name, type(r), c.name LIMIT 10

// Find service dependencies  
MATCH (s:Service)-[r:DEPENDS_ON]->(d) RETURN s.name, r, d.name

// See what applications are hosted
MATCH (app:Application)<-[r:HOSTS]-(host) RETURN app.name, host.name
```

**Find specific patterns:**
```cypher  
// All components of a specific system
MATCH (s:System {name: "app-prod-01"})-[:CONTAINS*]->(component) 
RETURN s, component

// Services and their dependencies
MATCH path = (s:Service)-[:DEPENDS_ON*]->(dep:Service)
RETURN path LIMIT 5
```

## 🔧 Configuration

### Environment Variables (Configured via `setup_environment.sh`)
```bash
# LLM Configuration (Red Hat AI - Pre-configured)
OPENAI_BASE_URL=https://llama-4-scout-17b-16e-w4a16-maas-apicast-production.apps.prod.rhoai.rh-aiservices-bu.com:443/v1
OPENAI_API_KEY=your-red-hat-ai-api-key-here
MODEL=llama-4-scout-17b-16e-w4a16

# Neo4j Configuration (Neo4j Desktop)
NEO4J_URI=neo4j://127.0.0.1:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password              # Set to your Neo4j Desktop password
NEO4J_DATABASE=neo4j                 # Default database name
```

### Main Configuration (`config/data_loader_config.yaml`)

The actual configuration used by the working dataloader:

```yaml
# Data Sources (Points to generated RHEL system data)
data_sources:
  primary_data:
    type: "filesystem" 
    base_path: "simulated_rhel_systems"
    file_patterns:
      system_info: ["**/system_info.txt"]
      logs: ["**/*.log"]
      configs: ["**/*.conf", "**/*.yaml"]

# LLM Configuration (Red Hat AI endpoint)
llm_config:
  base_url: "${OPENAI_BASE_URL}"
  api_key: "${OPENAI_API_KEY}" 
  model: "${MODEL}"
  fallback_config:
    base_url: "https://llama-4-scout-17b-16e-w4a16-maas-apicast-production.apps.prod.rhoai.rh-aiservices-bu.com:443/v1"
    api_key: "your-red-hat-ai-api-key-here"
    model: "llama-4-scout-17b-16e-w4a16"

# Neo4j Configuration
neo4j_config:
  uri: "${NEO4J_URI}"
  username: "${NEO4J_USERNAME}"
  password: "${NEO4J_PASSWORD}"
  database: "${NEO4J_DATABASE}"

# AI Entity Extraction (LangChain automatically discovers these)
# The AI extracts: System, Service, Application, Component, Event, Configuration
# With relationships: RUNS, DEPENDS_ON, CONTAINS, HOSTS
```

## 💼 Real-World Examples

### Example 1: IT Infrastructure Analysis
```python
# Point to your server configs and logs
config = {
    "data_sources": {
        "servers": {
            "base_path": "/var/log/servers",
            "file_patterns": {
                "configs": ["**/*.conf", "**/*.yaml"],
                "logs": ["**/*.log"]
            }
        }
    }
}

loader = get_universal_loader('production')
# Extracts: Server nodes, Service relationships, Configuration entities
```

### Example 2: Security Incident Analysis  
```python
# Point to security logs and incident reports
config = {
    "data_sources": {
        "security": {
            "base_path": "/security/incidents",
            "file_patterns": {
                "incidents": ["**/*incident*.txt", "**/*alert*.log"],
                "reports": ["**/*.pdf", "**/*.md"]
            }
        }
    }
}

# Extracts: Incident events, Affected systems, User entities, Security relationships
```

### Example 3: Business Process Documentation
```python
# Point to business documents and process files  
config = {
    "data_sources": {
        "business": {
            "base_path": "/business/processes",
            "file_patterns": {
                "processes": ["**/*process*.md", "**/*workflow*.yaml"],
                "documents": ["**/*.pdf", "**/*.docx"]
            }
        }
    }
}

# Extracts: Process entities, Role relationships, Document references
```

## 🛠️ Development & Extension

### Adding Custom Entity Types
```python
# In your configuration
entity_extraction:
  target_entities:
    - "CustomEntity"     # Your specific entity type
    - "DomainSpecific"   # Another custom entity
    
  target_relationships:
    - ("CustomEntity", "RELATES_TO", "System")
    - ("DomainSpecific", "CONTAINS", "CustomEntity")
```

### Creating New Data Source Adapters
```python
class CustomDataSourceAdapter(DataSourceAdapter):
    def list_available_systems(self) -> List[str]:
        # Your custom logic to discover data sources
        pass
        
    def load_system_files(self, system_id: str) -> Dict[str, str]:
        # Your custom logic to load data
        pass
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Test specific components
python tests/test_universal_loader.py
python tests/test_langchain_approach.py
```

## 🚀 Production Deployment

### Docker Deployment
```bash
# Build the image
docker build -t universal-dataloader .

# Run with environment variables
docker run -e OPENAI_API_KEY=your-key \
           -e NEO4J_URI=bolt://neo4j:7687 \
           -v /your/data:/app/data \
           universal-dataloader
```

### Environment-Specific Configuration
```yaml
# Development environment
environments:
  development:
    neo4j_config:
      management:
        clear_on_startup: true    # Clean slate for development
        
# Production environment
environments:
  production:
    neo4j_config:
      management:
        clear_on_startup: false   # Preserve data in production
        backup_before_clear: true
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Areas for Contribution
- 🔌 **New Data Source Adapters** (APIs, databases, cloud storage)
- 🎯 **Domain-Specific Entity Templates** (healthcare, finance, manufacturing)
- 🧪 **Testing & Validation** (more test cases, data validation)
- 📚 **Documentation** (tutorials, examples, best practices)
- ⚡ **Performance Optimizations** (parallel processing, caching)

## 📚 Documentation

- 📖 **[Configuration Guide](config/universal_dataloader_config.yaml)** - Complete configuration reference
- 🚀 **[Examples](examples/)** - Real-world usage patterns
- 🧪 **[Testing](tests/)** - Comprehensive test suite
- 🔧 **[Setup Guide](.env.example)** - Environment configuration

## 🆘 Support & Community

- 🐛 **[Issues](https://github.com/rrbanda/dataloader/issues)** - Bug reports and feature requests
- 💬 **[Discussions](https://github.com/rrbanda/dataloader/discussions)** - Community support and ideas
- 📧 **Contact** - your.email@example.com for direct support

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with these amazing open-source projects:
- **[LangChain](https://python.langchain.com/)** - LLM application framework
- **[Neo4j](https://neo4j.com/)** - Graph database platform  
- **[OpenAI](https://openai.com/)** - AI models and APIs

---

**🌟 Star this project if it helps you build better knowledge graphs! 🌟**