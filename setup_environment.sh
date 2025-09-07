#!/bin/bash
# Environment Setup for Universal DataLoader
# Run: source setup_environment.sh

echo "🚀 Setting up Universal DataLoader environment..."

# Check if user has set their API key
if [ -z "${OPENAI_API_KEY}" ]; then
    echo ""
    echo "⚠️  API KEY REQUIRED"
    echo "🔑 Please set your Red Hat AI API key first:"
    echo "   export OPENAI_API_KEY=\"your-actual-api-key\""
    echo "   source setup_environment.sh"
    echo ""
    exit 1
fi

# LLM Configuration - Red Hat AI endpoint
export OPENAI_BASE_URL="https://llama-4-scout-17b-16e-w4a16-maas-apicast-production.apps.prod.rhoai.rh-aiservices-bu.com:443/v1"
export OPENAI_API_KEY="${OPENAI_API_KEY}"
export MODEL="llama-4-scout-17b-16e-w4a16"

# Alternative: Local Ollama (if available)
# export OPENAI_BASE_URL="http://localhost:11434/v1"
# export OPENAI_API_KEY="dummy-key-for-local-llm"
# export MODEL="llama2"

# Neo4j Configuration  
export NEO4J_URI="neo4j://127.0.0.1:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="password"
export NEO4J_DATABASE="neo4j"

# Optional settings
export HTTP_TIMEOUT="180"
export ENVIRONMENT="development"

echo " Environment variables set!"
echo ""
echo "🔧 Next steps:"
echo "   1. Generate sample data: python utils/rhel_filesystem_generator.py"
echo "   2. Test setup: python test_setup.py"
echo "   3. Run dataloader: python -c 'from core.unified_dataloader import get_universal_loader; loader = get_universal_loader(); systems, events = loader.load_all_systems(); loader.close()'"
echo ""
echo "💡 Prerequisites:"
echo "   - Neo4j Desktop running with APOC plugin installed"
echo "   - Valid Red Hat AI API key set"
