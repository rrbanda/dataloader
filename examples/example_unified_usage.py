#!/usr/bin/env python3
"""
Example: Using the Unified RHEL Data Loader
Shows how to use the new configuration-driven data loader
"""

import os
from pathlib import Path

def example_basic_usage():
    """Basic usage example"""
    print("📊 EXAMPLE 1: Basic Data Loading")
    print("-" * 40)
    
    from core.unified_dataloader import get_unified_loader
    
    # Get loader for development environment
    loader = get_unified_loader('development')
    
    # List available systems
    systems = loader.list_available_systems()
    print(f"Available systems: {systems}")
    
    # Load data for one system
    if systems:
        system_id = systems[0]
        rhel_systems, patch_events = loader.load_system_data(system_id)
        print(f"Loaded: {len(rhel_systems)} systems, {len(patch_events)} events")
        
        # Show system details
        if rhel_systems:
            system = rhel_systems[0]
            print(f"System: {system.system_id}")
            print(f"RHEL Version: {system.rhel_version}")
            print(f"Environment: {system.environment}")
            print(f"Services: {system.services[:3]}...")  # First 3 services

def example_backward_compatibility():
    """Show backward compatibility with existing code"""
    print("\n🔄 EXAMPLE 2: Backward Compatibility")
    print("-" * 40)
    
    # This works exactly like your existing create_sample_data()
    from core.unified_dataloader import create_sample_data
    
    systems, events = create_sample_data()
    print(f"Backward compatible loading: {len(systems)} systems, {len(events)} events")

def example_configuration_usage():
    """Show how to use configuration"""
    print("\n⚙️ EXAMPLE 3: Configuration Usage")
    print("-" * 40)
    
    from config.config_loader import get_config_loader
    
    # Get configuration
    config = get_config_loader('development')
    
    # Check LLM configuration
    llm_config = config.get_llm_config()
    print(f"LLM Endpoint: {llm_config['base_url']}")
    print(f"Model: {llm_config['model']}")
    
    # Check data source configuration
    data_config = config.get_data_source_config()
    print(f"Data Source: {data_config['type']} at {data_config['base_path']}")
    
    # Check what phases are enabled
    ai_enabled = config.is_phase_enabled('ai_extraction')
    text_enabled = config.is_phase_enabled('text_processing')
    print(f"AI Extraction: {'✅ Enabled' if ai_enabled else '❌ Disabled'}")
    print(f"Text Processing: {'✅ Enabled' if text_enabled else '❌ Disabled'}")

def example_environment_switching():
    """Show how to switch between environments"""
    print("\n🌍 EXAMPLE 4: Environment Switching")
    print("-" * 40)
    
    from core.unified_dataloader import get_unified_loader
    
    # Different environments have different configurations
    environments = ['development', 'production', 'testing']
    
    for env in environments:
        try:
            loader = get_unified_loader(env)
            systems = loader.list_available_systems()
            print(f"{env.capitalize()}: {len(systems)} systems available")
        except Exception as e:
            print(f"{env.capitalize()}: Error - {e}")

def example_extensible_data_sources():
    """Show how the system is extensible for new data sources"""
    print("\n🔌 EXAMPLE 5: Extensible Design")
    print("-" * 40)
    
    print("Current data sources configured:")
    
    from config.config_loader import get_config_loader
    config = get_config_loader()
    
    # Load the full dataloader config to see all data sources
    dataloader_config = config._load_dataloader_config()
    data_sources = dataloader_config.get('data_sources', {})
    
    for source_name, source_config in data_sources.items():
        status = "✅ Enabled" if source_config.get('enabled', True) else "❌ Disabled"
        source_type = source_config.get('type', 'unknown')
        print(f"  {source_name}: {source_type} ({status})")
    
    print("\n💡 To add new data sources, edit config/data_loader_config.yaml")

def example_integration_with_existing_code():
    """Show how to integrate with your existing knowledge graph builders"""
    print("\n🔗 EXAMPLE 6: Integration with Knowledge Graph")
    print("-" * 40)
    
    try:
        # Load data using unified loader
        from core.unified_dataloader import get_unified_loader
        loader = get_unified_loader('development')
        systems, events = loader.load_all_systems()
        
        print(f"Loaded {len(systems)} systems and {len(events)} events")
        
        # This data can now be passed to any of your existing graph builders
        print("✅ Data ready for:")
        print("  - RHELKnowledgeGraphBuilder")
        print("  - DemoKnowledgeGraphBuilder") 
        print("  - EnterpriseKnowledgeGraphLoader")
        
        # Example: Use with your existing graph builder (commented out)
        # from core.knowledge_graph import RHELKnowledgeGraphBuilder
        # kg = RHELKnowledgeGraphBuilder()
        # kg.build_knowledge_graph(systems, events)
        
    except ImportError as e:
        print(f"⚠️ Some components not available: {e}")

def example_error_handling():
    """Show robust error handling"""
    print("\n🛡️ EXAMPLE 7: Error Handling & Fallbacks")
    print("-" * 40)
    
    from core.unified_dataloader import get_unified_loader
    
    try:
        # Try to load from non-existent system
        loader = get_unified_loader('development')
        systems, events = loader.load_system_data('non-existent-system')
        print(f"Non-existent system result: {len(systems)} systems, {len(events)} events")
        
    except Exception as e:
        print(f"Error handled gracefully: {e}")
    
    # Configuration automatically falls back to safe defaults
    print("✅ System continues working even with errors")

def main():
    """Run all examples"""
    print("🚀 UNIFIED RHEL DATA LOADER - USAGE EXAMPLES")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("simulated_rhel_systems").exists():
        print("❌ Please run this from the rhel-patch-intelligence directory")
        print("💡 cd to the directory containing simulated_rhel_systems/")
        return
    
    # Check environment variables
    if not os.getenv('OPENAI_BASE_URL'):
        print("⚠️ Environment variables not set")
        print("💡 Run 'source setup.sh' first")
        print()
    
    examples = [
        example_basic_usage,
        example_backward_compatibility,
        example_configuration_usage,
        example_environment_switching,
        example_extensible_data_sources,
        example_integration_with_existing_code,
        example_error_handling
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"❌ Example failed: {e}")
            print("💡 This might be expected if dependencies aren't installed")
    
    print("\n" + "=" * 60)
    print("🎯 KEY BENEFITS OF UNIFIED LOADER:")
    print("✅ Eliminates 4 duplicate data loaders")
    print("✅ Uses your existing configuration pattern")
    print("✅ Configurable for different environments")
    print("✅ Extensible for new data sources")
    print("✅ Backward compatible with existing code")
    print("✅ Works with your Red Hat AI endpoint")
    print("✅ Zero-cost open source stack")
    
    print("\n📖 Next Steps:")
    print("1. Run: python test_unified_loader.py")
    print("2. Review: DATALOADER_MIGRATION.md")
    print("3. Start migrating existing code step by step")

if __name__ == "__main__":
    main()
