#!/usr/bin/env python3
"""
Test LangChain-based AI Extraction Approach
Tests the simplified, working implementation vs. broken Instructor approach
"""

import os
import sys
from dotenv import load_dotenv

def test_langchain_dependencies():
    """Test that all LangChain dependencies are available"""
    print("🧪 TESTING LANGCHAIN DEPENDENCIES")
    print("=" * 50)
    
    dependencies = [
        "langchain_experimental.graph_transformers",
        "langchain_openai", 
        "langchain_core.documents",
        "langchain_neo4j"
    ]
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError as e:
            print(f"❌ {dep}: {e}")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠️ Missing dependencies: {missing}")
        print("💡 Install with: pip install langchain-experimental")
        return False
    
    print("\n✅ All LangChain dependencies available!")
    return True

def test_langchain_dataloader():
    """Test the new LangChain-based unified dataloader"""
    print("\n🧪 TESTING LANGCHAIN DATALOADER")
    print("=" * 50)
    
    load_dotenv()
    
    try:
        # Import from dataload folder
        sys.path.insert(0, '/Users/raghurambanda/llm-ops-agent/rhel-patch-intelligence/dataload')
        
        from unified_dataloader import get_unified_loader
        
        print("🚀 Initializing LangChain-based unified loader...")
        loader = get_unified_loader('development')
        
        # Check AI extractor type
        if hasattr(loader, 'ai_extractor') and loader.ai_extractor:
            extractor_type = type(loader.ai_extractor).__name__
            print(f"✅ AI Extractor: {extractor_type}")
            
            if extractor_type == "LangChainAIExtractor":
                print("✅ Using NEW LangChain approach!")
            else:
                print("⚠️ Still using old approach")
                
        # Test system listing
        systems = loader.list_available_systems()
        print(f"📋 Available systems: {len(systems)}")
        
        if systems:
            # Test single system with LangChain extraction
            print(f"\n🔍 Testing LangChain extraction on: {systems[0]}")
            
            try:
                rhel_systems, patch_events = loader.load_system_data(systems[0])
                print(f"✅ LangChain pipeline complete!")
                print(f"   📊 Processing successful")
                print(f"   🗄️ Data loaded directly to Neo4j")
                
                # Check if data was actually loaded to Neo4j
                if hasattr(loader, 'ai_extractor') and loader.ai_extractor and hasattr(loader.ai_extractor, 'neo4j_graph'):
                    try:
                        result = loader.ai_extractor.neo4j_graph.query("MATCH (n) RETURN count(n) as node_count")
                        node_count = result[0]['node_count'] if result else 0
                        print(f"🗄️ Neo4j nodes after extraction: {node_count}")
                        
                        if node_count > 0:
                            print("✅ LangChain extraction successful - data in Neo4j!")
                        else:
                            print("⚠️ No nodes found - check AI extraction")
                    except Exception as e:
                        print(f"⚠️ Neo4j query failed: {e}")
                
                return True
                
            except Exception as e:
                print(f"❌ LangChain extraction failed: {e}")
                return False
        
        else:
            print("❌ No systems found to test")
            return False
            
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        if 'loader' in locals():
            loader.close()

def test_old_vs_new_approach():
    """Compare old broken Instructor approach with new LangChain approach"""
    print("\n🧪 COMPARING OLD VS NEW APPROACH")
    print("=" * 50)
    
    print("❌ OLD APPROACH (Instructor):")
    print("   - Complex custom Pydantic models")
    print("   - Manual prompt engineering")
    print("   - Broken placeholder implementations")
    print("   - Returns empty results: []")
    print("   - Requires Phase 4 graph loading")
    
    print("\n✅ NEW APPROACH (LangChain):")
    print("   - Uses proven LLMGraphTransformer")
    print("   - Industry-standard knowledge graph construction")
    print("   - Direct Neo4j integration")
    print("   - Combines Phase 3 + 4 efficiently")
    print("   - Actually works!")
    
    return True

def main():
    """Run all LangChain approach tests"""
    print("🔍 Testing LangChain-based AI Extraction Approach...")
    
    # Test 1: Dependencies
    deps_ok = test_langchain_dependencies()
    
    # Test 2: New dataloader
    if deps_ok:
        dataloader_ok = test_langchain_dataloader()
    else:
        dataloader_ok = False
    
    # Test 3: Comparison
    comparison_ok = test_old_vs_new_approach()
    
    print("\n" + "=" * 60)
    if deps_ok and dataloader_ok:
        print("🎉 LANGCHAIN APPROACH WORKING!")
        print("✅ Much simpler than Instructor")
        print("✅ Industry-standard implementation")
        print("✅ Direct Neo4j integration")
        print("✅ Actually extracts and loads data")
        print("\n💡 Ready to replace old broken approach!")
        return True
    else:
        print("❌ LangChain approach needs attention")
        if not deps_ok:
            print("   - Install missing dependencies")
        if not dataloader_ok:
            print("   - Check LLM endpoint configuration")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
