#!/usr/bin/env python3
"""
Setup Test Script for Universal DataLoader
Tests basic functionality and validates setup
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test that all required imports work"""
    print("🔍 Testing imports...")
    try:
        from core.unified_dataloader import get_universal_loader
        print("✅ Core dataloader imports working")
        
        from neo4j import GraphDatabase
        print("✅ Neo4j driver available")
        
        import langchain
        print("✅ LangChain available")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n⚙️ Testing configuration...")
    try:
        from config.config_loader import get_config_loader
        
        config = get_config_loader('development')
        llm_config = config.get_llm_config()
        neo4j_config = config.get_neo4j_config()
        
        print(f"✅ LLM endpoint: {llm_config.get('base_url', 'NOT SET')}")
        print(f"✅ Neo4j URI: {neo4j_config.get('uri', 'NOT SET')}")
        print(f"✅ Environment: {config.environment}")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_data_availability():
    """Test if sample data exists"""
    print("\n📁 Testing data availability...")
    
    data_paths = [
        "simulated_rhel_systems",
        "demo_data/security_incidents", 
        "demo_data/knowledge_base",
        "demo_data/app_data"
    ]
    
    available_sources = 0
    for path in data_paths:
        if Path(path).exists():
            print(f"✅ {path}: Available")
            available_sources += 1
        else:
            print(f"⚠️ {path}: Not found")
    
    print(f"📊 {available_sources}/{len(data_paths)} data sources available")
    return available_sources > 0

def test_neo4j_connection():
    """Test Neo4j connection"""
    print("\n🗄️ Testing Neo4j connection...")
    try:
        from neo4j import GraphDatabase
        
        neo4j_uri = os.getenv('NEO4J_URI', 'neo4j://127.0.0.1:7687')
        neo4j_user = os.getenv('NEO4J_USERNAME', 'neo4j')
        neo4j_pass = os.getenv('NEO4J_PASSWORD', 'password')
        
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass))
        
        with driver.session() as session:
            result = session.run('RETURN 1 as test')
            record = result.single()
            print(f"✅ Neo4j connected: {neo4j_uri}")
            
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ Neo4j connection failed: {e}")
        print("💡 Make sure Neo4j Desktop is running")
        return False

def test_basic_dataloader():
    """Test basic dataloader functionality"""
    print("\n🚀 Testing basic dataloader...")
    try:
        from core.unified_dataloader import get_universal_loader
        
        loader = get_universal_loader('development')
        systems = loader.list_available_systems()
        
        print(f"✅ Found {len(systems)} systems: {systems[:3]}{'...' if len(systems) > 3 else ''}")
        
        if systems:
            # Test loading one system
            system_id = systems[0]
            print(f"📋 Testing with system: {system_id}")
            
            rhel_systems, patch_events = loader.load_system_data(system_id)
            print(f"✅ Loaded: {len(rhel_systems)} systems, {len(patch_events)} events")
            
        loader.close()
        return True
        
    except Exception as e:
        print(f"❌ Dataloader test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 UNIVERSAL DATALOADER - SETUP TEST")
    print("=" * 50)
    
    # Check environment
    env_vars = ['OPENAI_BASE_URL', 'OPENAI_API_KEY', 'NEO4J_URI']
    print(f"🌍 Environment: {os.getenv('ENVIRONMENT', 'not set')}")
    for var in env_vars:
        value = os.getenv(var, 'NOT SET')
        if 'KEY' in var and value != 'NOT SET':
            value = '***'  # Mask sensitive values
        print(f"   {var}: {value}")
    
    print()
    
    # Run tests
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Data Sources", test_data_availability),
        ("Neo4j Connection", test_neo4j_connection),
        ("Basic Dataloader", test_basic_dataloader)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test_name} crashed: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY:")
    passed = sum(results)
    total = len(results)
    print(f"✅ Passed: {passed}/{total} tests")
    
    if passed == total:
        print("🎉 All tests passed! Your dataloader is ready.")
        print("\n🚀 Ready to run:")
        print("   python -c 'from core.unified_dataloader import get_universal_loader; loader = get_universal_loader(); systems, events = loader.load_all_systems(); loader.close(); print(f\"Loaded {len(systems)} systems!\")'")
    else:
        print("⚠️ Some tests failed. Check the output above.")
        
    print("\n💡 Next steps:")
    print("   1. Fix any failed tests")
    print("   2. Run your dataloader code")
    print("   3. View results in Neo4j Desktop")

if __name__ == "__main__":
    main()
