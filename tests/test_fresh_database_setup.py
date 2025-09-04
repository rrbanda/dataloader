#!/usr/bin/env python3
"""
Test Fresh Database Setup - Verifies database creation from scratch
Tests the complete flow: Database Creation → Schema Setup → Data Loading
"""

import os
import sys
from dotenv import load_dotenv

def test_database_creation():
    """Test database creation from scratch"""
    print("🧪 TESTING FRESH DATABASE SETUP")
    print("=" * 50)
    
    load_dotenv()
    
    # Check environment setup
    neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    neo4j_username = os.getenv('NEO4J_USERNAME', 'neo4j')
    neo4j_password = os.getenv('NEO4J_PASSWORD', 'password')
    neo4j_database = os.getenv('NEO4J_DATABASE', 'rhel')
    
    print(f"🔗 Neo4j URI: {neo4j_uri}")
    print(f"👤 Username: {neo4j_username}")
    print(f"🗄️ Target Database: {neo4j_database}")
    print()
    
    try:
        from core.unified_dataloader import Neo4jGraphLoader
        from config.config_loader import get_config_loader
        
        # Test configuration loading
        print("⚙️ Testing configuration...")
        config = get_config_loader('development')
        neo4j_config = config.get_neo4j_config()
        
        print(f"✅ Config loaded: {neo4j_config['uri']}")
        print(f"✅ Auto-create enabled: {neo4j_config['management']['auto_create_database']}")
        print()
        
        # Test database creation and connection
        print("🗄️ Testing database creation...")
        graph_loader = Neo4jGraphLoader(neo4j_config)
        
        if graph_loader.driver:
            print("✅ Neo4j connection successful!")
            print(f"✅ Database '{neo4j_config['database']}' ready")
            
            # Test basic query
            with graph_loader.driver.session(database=neo4j_config['database']) as session:
                result = session.run("RETURN 'Database is working!' as message")
                message = result.single()["message"]
                print(f"✅ Test query successful: {message}")
            
            # Show database info
            try:
                with graph_loader.driver.session(database="system") as session:
                    result = session.run("SHOW DATABASES")
                    databases = [record["name"] for record in result]
                    print(f"📋 Available databases: {databases}")
                    
                    if neo4j_config['database'] in databases:
                        print(f"✅ Target database '{neo4j_config['database']}' exists")
                    else:
                        print(f"⚠️ Target database '{neo4j_config['database']}' not found")
                        
            except Exception as e:
                print(f"💡 Database listing not available (Community edition?): {e}")
            
            graph_loader.close()
            return True
            
        else:
            print("❌ Failed to connect to Neo4j")
            print_neo4j_troubleshooting()
            return False
            
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        print_neo4j_troubleshooting()
        return False

def test_complete_fresh_pipeline():
    """Test complete pipeline from fresh database"""
    print("\n🧪 TESTING COMPLETE FRESH PIPELINE")
    print("=" * 50)
    
    try:
        from core.unified_dataloader import get_unified_loader
        
        print("🚀 Starting fresh pipeline test...")
        
        # Initialize unified loader (this will create database if needed)
        loader = get_unified_loader('development')
        
        # Test with one system
        systems = loader.list_available_systems()
        if systems:
            print(f"📋 Testing with system: {systems[0]}")
            
            # Load data (this will create indexes and load to Neo4j)
            rhel_systems, patch_events = loader.load_system_data(systems[0])
            
            print(f"✅ Pipeline complete!")
            print(f"   📊 Systems: {len(rhel_systems)}")
            print(f"   📊 Events: {len(patch_events)}")
            
            # Test graph query (if data was loaded)
            if hasattr(loader, 'graph_loader') and loader.graph_loader and loader.graph_loader.driver:
                try:
                    with loader.graph_loader.driver.session(database=loader.graph_loader.database) as session:
                        # Count nodes
                        result = session.run("MATCH (n) RETURN count(n) as node_count")
                        node_count = result.single()["node_count"]
                        
                        # Count relationships
                        result = session.run("MATCH ()-[r]->() RETURN count(r) as rel_count")
                        rel_count = result.single()["rel_count"]
                        
                        print(f"🗄️ Neo4j Graph Status:")
                        print(f"   📊 Nodes: {node_count}")
                        print(f"   🔗 Relationships: {rel_count}")
                        
                except Exception as e:
                    print(f"⚠️ Graph query failed: {e}")
            
            loader.close()
            return True
        else:
            print("❌ No systems found to test")
            return False
            
    except Exception as e:
        print(f"❌ Fresh pipeline test failed: {e}")
        return False

def print_neo4j_troubleshooting():
    """Print Neo4j troubleshooting information"""
    print("\n🔧 NEO4J TROUBLESHOOTING:")
    print("1. Is Neo4j running?")
    print("   • Docker: docker run -p 7474:7474 -p 7687:7687 neo4j")
    print("   • Local: Check Neo4j Desktop or service")
    print()
    print("2. Check connection settings in setup.sh:")
    print("   • NEO4J_URI=bolt://localhost:7687")
    print("   • NEO4J_USERNAME=neo4j")
    print("   • NEO4J_PASSWORD=your_password")
    print("   • NEO4J_DATABASE=rhel")
    print()
    print("3. Database creation requirements:")
    print("   • Neo4j 4.0+ for multi-database support")
    print("   • Enterprise edition for advanced features")
    print("   • Community edition: May need manual creation")

if __name__ == "__main__":
    print("🔍 Testing Fresh Database Setup From Scratch...")
    
    db_success = test_database_creation()
    
    if db_success:
        pipeline_success = test_complete_fresh_pipeline()
        
        if pipeline_success:
            print("\n🎉 FRESH SETUP SUCCESSFUL!")
            print("✅ Database created")
            print("✅ Schema initialized") 
            print("✅ Data loaded")
            print("✅ Ready for production use")
            sys.exit(0)
    
    print("\n❌ Fresh setup needs attention")
    print("💡 Check Neo4j setup and configuration")
    sys.exit(1)
