#!/bin/bash
# Environment Setup for Universal DataLoader
# Run: source setup_environment.sh

echo "🚀 Setting up Universal DataLoader environment..."

# Check if user has set their API key
if [ "${OPENAI_API_KEY}" = "your-api-key-here" ] || [ -z "${OPENAI_API_KEY}" ]; then
    echo ""
    echo "⚠️  API KEY REQUIRED"
    echo "🔑 Please set your Red Hat AI API key:"
    echo "   export OPENAI_API_KEY=\"your-actual-api-key\""
    echo ""
    echo "💡 Or copy env.example to .env and fill in your credentials"
    echo ""
fi

# LLM Configuration - Red Hat AI endpoint
export OPENAI_BASE_URL="https://llama-4-scout-17b-16e-w4a16-maas-apicast-production.apps.prod.rhoai.rh-aiservices-bu.com:443/v1"
export OPENAI_API_KEY="${OPENAI_API_KEY:-your-api-key-here}"
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

echo "✅ Environment variables set!"
echo "📊 Sample data ready (15 systems, 120 events)"
echo ""
echo "🔧 To test the dataloader:"
echo "   python test_setup.py"
echo ""
echo "💡 To use with actual AI/Neo4j:"
echo "   1. Start Neo4j Desktop and create a database"
echo "   2. Start Ollama: ollama serve (optional - for local LLM)"
echo "   3. Pull model: ollama pull llama2 (optional)"
echo "   4. Run loader: python test_setup.py"
