# 🚀 Universal DataLoader

**AI-Powered Knowledge Graph Construction for Any Domain**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-green.svg)](https://python.langchain.com/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.0+-red.svg)](https://neo4j.com/)

Transform unstructured data from **any domain** into rich knowledge graphs using **LangChain** and **Neo4j**. Works with servers, applications, documents, network devices, security data, and more!

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

1. **📁 Phase 1: Raw Data Ingestion** (No AI)
2. **⚙️ Phase 2: Text Processing** (Minimal AI) 
3. **🧠 Phase 3: AI Entity Extraction** (LangChain LLMGraphTransformer)
4. **🗄️ Phase 4: Graph Loading** (Direct Neo4j integration)

## 📂 Directory Structure

```
universal-dataloader/
├── core/                   # 🎯 Core functionality
│   ├── unified_dataloader.py    # Universal dataloader (LangChain-based)
│   ├── data_models.py           # Generic data models for any domain
│   └── __init__.py
├── config/                 # ⚙️ Configuration management  
│   ├── config_loader.py         # Configuration loader
│   ├── universal_dataloader_config.yaml  # Main configuration file
│   └── __init__.py
├── tests/                  # ✅ Comprehensive test suite
│   ├── test_universal_loader.py
│   ├── test_langchain_approach.py
│   └── test_*.py
├── examples/               # 📖 Usage examples
│   └── example_usage.py
├── utils/                  # 🛠️ Utilities
│   └── cleanup_*.py
├── sample_data/            # 📁 Sample data for testing
│   └── example_system/
├── requirements.txt        # 📦 Dependencies
├── setup.py               # 📦 Package setup
├── .env.example           # ⚙️ Environment template
└── README.md              # 📚 This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/rrbanda/dataloader.git
cd dataloader

# Install dependencies
pip install -r requirements.txt

# For full features (optional)
pip install -r requirements.txt[full]
```

### 2. Configuration

```bash
# Copy and configure environment variables
cp .env.example .env
# Edit .env with your LLM API key and Neo4j credentials

# The default configuration works out of the box with sample data
# Customize config/universal_dataloader_config.yaml as needed
```

### 3. Run with Sample Data

```python
from core.unified_dataloader import get_universal_loader

# Initialize and run with sample data
loader = get_universal_loader('development')
systems, events = loader.load_all_systems()
loader.close()

print(f"Loaded {len(systems)} systems and {len(events)} events into Neo4j!")
```

## 🔧 Configuration

### Environment Variables (`.env`)
```bash
# LLM Configuration
OPENAI_BASE_URL=https://your-llm-endpoint.com/v1
OPENAI_API_KEY=your-api-key
MODEL=gpt-3.5-turbo

# Neo4j Configuration  
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password
NEO4J_DATABASE=knowledge_graph
```

### Main Configuration (`config/universal_dataloader_config.yaml`)

The configuration is structured for maximum flexibility:

```yaml
# Data Sources - easily point to your data
data_sources:
  primary_data:
    type: "filesystem"
    base_path: "your_data_directory"
    file_patterns:
      logs: ["**/*.log", "**/*.txt"]
      configs: ["**/*.yaml", "**/*.json", "**/*.conf"]
      documents: ["**/*.md", "**/*.pdf"]

# Entity Extraction - customize for your domain
entity_extraction:
  target_entities:
    - "System"      # Servers, applications, devices
    - "Service"     # Running processes, APIs  
    - "Event"       # Incidents, changes, alerts
    - "Document"    # Files, logs, reports
    # Add your domain-specific entities
    
  target_relationships:
    - "RUNS"        # System RUNS Service
    - "GENERATES"   # System GENERATES Event
    - "CONTAINS"    # System CONTAINS Component
    # Add your domain-specific relationships
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