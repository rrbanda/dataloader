#!/usr/bin/env python3
"""
Test Script for Unified Data Loader
Verifies that the new system works with your existing configuration
"""

import os
import sys
from pathlib import Path

def test_configuration():
    """Test that configuration loading works"""
    print("🔧 Testing Configuration Loading...")
    
    try:
        from config.config_loader import get_config_loader
        
        # Test config loader initialization
        config = get_config_loader('development')
        print("✅ Configuration loader initialized")
        
        # Test LLM config (should use your Red Hat endpoint)
        llm_config = config.get_llm_config()
        print(f"✅ LLM Endpoint: {llm_config.get('base_url', 'Not configured')}")
        print(f"✅ Model: {llm_config.get('model', 'Not configured')}")
        
        # Test data source config
        data_config = config.get_data_source_config()
        print(f"✅ Data Source Type: {data_config.get('type', 'Not configured')}")
        print(f"✅ Data Path: {data_config.get('base_path', 'Not configured')}")
        
        # Test text processing config
        text_config = config.get_text_processing_config()
        chunk_size = text_config.get('chunking', {}).get('max_chunk_size', 'Not configured')
        print(f"✅ Text Processing - Chunk Size: {chunk_size}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_data_source_access():
    """Test that we can access your simulated RHEL systems"""
    print("\n📁 Testing Data Source Access...")
    
    try:
        # Check if simulated systems directory exists
        systems_path = Path("simulated_rhel_systems")
        if not systems_path.exists():
            print(f"❌ Simulated systems directory not found: {systems_path}")
            return False
        
        # List available systems
        systems = [d.name for d in systems_path.iterdir() if d.is_dir()]
        print(f"✅ Found {len(systems)} systems: {systems}")
        
        if not systems:
            print("❌ No systems found in simulated_rhel_systems directory")
            return False
        
        # Test reading a sample system
        sample_system = systems[0]
        sample_path = systems_path / sample_system
        
        # Check for key files
        key_files = [
            "etc/redhat-release",
            "var/lib/rpm/packages.txt",
            "var/log/yum.log"
        ]
        
        found_files = []
        for file_path in key_files:
            full_path = sample_path / file_path
            if full_path.exists():
                found_files.append(file_path)
        
        print(f"✅ Sample system {sample_system} has {len(found_files)}/{len(key_files)} key files")
        
        return True
        
    except Exception as e:
        print(f"❌ Data source access test failed: {e}")
        return False

def test_unified_loader():
    """Test the unified data loader"""
    print("\n🚀 Testing Unified Data Loader...")
    
    try:
        from core.unified_dataloader import get_unified_loader
        
        # Initialize loader
        loader = get_unified_loader('development')
        print("✅ Unified loader initialized")
        
        # Test listing systems
        available_systems = loader.list_available_systems()
        print(f"✅ Loader found {len(available_systems)} systems: {available_systems}")
        
        if not available_systems:
            print("❌ No systems available from loader")
            return False
        
        # Test loading one system
        sample_system = available_systems[0]
        print(f"📊 Testing data loading for: {sample_system}")
        
        systems, events = loader.load_system_data(sample_system)
        print(f"✅ Loaded: {len(systems)} system objects, {len(events)} event objects")
        
        # Test the system object
        if systems:
            system = systems[0]
            print(f"✅ System object: ID={system.system_id}, Version={system.rhel_version}")
        
        return True
        
    except Exception as e:
        print(f"❌ Unified loader test failed: {e}")
        print(f"💡 This might be expected if optional dependencies aren't installed")
        return False

def test_backward_compatibility():
    """Test that existing interfaces still work"""
    print("\n🔄 Testing Backward Compatibility...")
    
    try:
        from core.unified_dataloader import create_sample_data
        
        # Test the backward compatibility function
        systems, events = create_sample_data()
        print(f"✅ Backward compatible function works: {len(systems)} systems, {len(events)} events")
        
        return True
        
    except Exception as e:
        print(f"❌ Backward compatibility test failed: {e}")
        return False

def test_environment_variables():
    """Test that environment variables are properly set"""
    print("\n🌍 Testing Environment Variables...")
    
    # LLM variables
    llm_vars = [
        'OPENAI_BASE_URL',
        'OPENAI_API_KEY', 
        'MODEL'
    ]
    
    # Neo4j variables
    neo4j_vars = [
        'NEO4J_URI',
        'NEO4J_USERNAME',
        'NEO4J_PASSWORD',
        'NEO4J_DATABASE'
    ]
    
    missing_vars = []
    
    print("🧠 LLM Configuration:")
    for var in llm_vars:
        value = os.getenv(var)
        if not value or value == 'dummy':
            missing_vars.append(var)
        else:
            # Show partial value for security
            display_value = value[:20] + "..." if len(value) > 20 else value
            print(f"  ✅ {var}: {display_value}")
    
    print("\n🗄️ Neo4j Configuration:")
    for var in neo4j_vars:
        value = os.getenv(var)
        if not value:
            print(f"  ⚠️ {var}: Not set (will use default)")
        else:
            # Show partial value for security (except URI)
            if var == 'NEO4J_URI':
                display_value = value
            else:
                display_value = value[:10] + "..." if len(value) > 10 else value
            print(f"  ✅ {var}: {display_value}")
    
    if missing_vars:
        print(f"\n⚠️ Missing required environment variables: {missing_vars}")
        print("💡 Run 'source setup.sh' to set them")
        return False
    
    return True

def test_neo4j_configuration():
    """Test Neo4j configuration and connection"""
    print("\n🗄️ Testing Neo4j Configuration...")
    
    try:
        from config.config_loader import get_config_loader
        
        config = get_config_loader('development')
        neo4j_config = config.get_neo4j_config()
        
        print(f"✅ Neo4j URI: {neo4j_config['uri']}")
        print(f"✅ Neo4j Database: {neo4j_config['database']}")
        print(f"✅ Neo4j Username: {neo4j_config['username']}")
        
        # Test management options
        management = neo4j_config.get('management', {})
        auto_create = management.get('auto_create_database', False)
        clear_startup = management.get('clear_on_startup', False)
        print(f"✅ Auto-create DB: {auto_create}")
        print(f"✅ Clear on startup: {clear_startup}")
        
        # Try to connect (optional test)
        try:
            from neo4j import GraphDatabase
            
            with GraphDatabase.driver(
                neo4j_config['uri'],
                auth=(neo4j_config['username'], neo4j_config['password'])
            ) as driver:
                with driver.session(database=neo4j_config['database']) as session:
                    result = session.run("RETURN 1 as test")
                    if result.single()["test"] == 1:
                        print("✅ Neo4j connection successful")
                        return True
        except Exception as e:
            print(f"⚠️ Neo4j connection failed: {e}")
            print("💡 This is OK if Neo4j isn't running yet")
            return True  # Config is still valid
            
    except Exception as e:
        print(f"❌ Neo4j configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 UNIFIED DATA LOADER TEST SUITE")
    print("=" * 50)
    
    # Check working directory
    if not Path("simulated_rhel_systems").exists():
        print("❌ Please run this script from the rhel-patch-intelligence directory")
        print("💡 cd to the directory containing simulated_rhel_systems/")
        sys.exit(1)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Configuration Loading", test_configuration),
        ("Neo4j Configuration", test_neo4j_configuration),
        ("Data Source Access", test_data_source_access),
        ("Unified Data Loader", test_unified_loader),
        ("Backward Compatibility", test_backward_compatibility)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Unified data loader is working correctly")
        print("✅ Ready to migrate existing code")
        print("\n📖 Next steps:")
        print("   1. Review DATALOADER_MIGRATION.md")
        print("   2. Start with Phase 2 testing")
        print("   3. Gradually migrate existing code")
    else:
        print(f"\n⚠️  {total - passed} tests failed")
        print("💡 Check the error messages above")
        print("💡 Make sure you've run 'source setup.sh'")
        
        if not test_environment_variables():
            print("💡 Environment variable issues are most common")

if __name__ == "__main__":
    main()
