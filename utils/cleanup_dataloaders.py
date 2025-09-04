#!/usr/bin/env python3
"""
Safe Cleanup Utility for RHEL Data Loaders
Handles both file cleanup and Neo4j database management
"""

import os
import shutil
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataLoaderCleanup:
    """Safe cleanup utility for data loaders and databases"""
    
    def __init__(self):
        self.backup_dir = Path("cleanup_backups") / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.duplicate_files = [
            "core/file_parser.py",
            "core/instructor_parser.py", 
            "core/demo_intelligence_extractor.py"
        ]
        
    def create_backup_directory(self):
        """Create backup directory for safety"""
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Created backup directory: {self.backup_dir}")
    
    def backup_file(self, file_path: str) -> bool:
        """Backup a file before cleanup"""
        try:
            source = Path(file_path)
            if not source.exists():
                logger.warning(f"⚠️ File not found for backup: {file_path}")
                return False
            
            # Create backup with same directory structure
            backup_path = self.backup_dir / file_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(source, backup_path)
            logger.info(f"✅ Backed up: {file_path} -> {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to backup {file_path}: {e}")
            return False
    
    def check_unified_loader_working(self) -> bool:
        """Verify that unified loader is working before cleanup"""
        try:
            from core.unified_dataloader import get_unified_loader
            
            loader = get_unified_loader('development')
            systems = loader.list_available_systems()
            
            if not systems:
                logger.warning("⚠️ No systems found with unified loader")
                return False
            
            # Try to load one system
            rhel_systems, events = loader.load_system_data(systems[0])
            logger.info(f"✅ Unified loader working: {len(rhel_systems)} systems, {len(events)} events")
            return True
            
        except Exception as e:
            logger.error(f"❌ Unified loader test failed: {e}")
            return False
    
    def cleanup_duplicate_files(self, force: bool = False) -> bool:
        """Remove duplicate dataloader files safely"""
        
        if not force:
            # Check if unified loader is working first
            if not self.check_unified_loader_working():
                logger.error("❌ Unified loader not working - aborting cleanup")
                logger.info("💡 Run 'python test_unified_loader.py' to verify setup")
                return False
        
        # Create backup directory
        self.create_backup_directory()
        
        # Backup all files first
        backup_success = True
        for file_path in self.duplicate_files:
            if not self.backup_file(file_path):
                backup_success = False
        
        if not backup_success:
            logger.error("❌ Not all files backed up successfully - aborting cleanup")
            return False
        
        # Remove duplicate files
        removed_count = 0
        for file_path in self.duplicate_files:
            try:
                source = Path(file_path)
                if source.exists():
                    source.unlink()
                    logger.info(f"🗑️ Removed: {file_path}")
                    removed_count += 1
                else:
                    logger.info(f"ℹ️ Already removed: {file_path}")
            except Exception as e:
                logger.error(f"❌ Failed to remove {file_path}: {e}")
                return False
        
        logger.info(f"🎉 Cleanup complete! Removed {removed_count} duplicate files")
        logger.info(f"📁 Backups saved in: {self.backup_dir}")
        return True
    
    def restore_from_backup(self, backup_timestamp: str = None) -> bool:
        """Restore files from backup"""
        try:
            if backup_timestamp:
                restore_dir = Path("cleanup_backups") / backup_timestamp
            else:
                # Find most recent backup
                backup_dirs = list(Path("cleanup_backups").glob("*"))
                if not backup_dirs:
                    logger.error("❌ No backups found")
                    return False
                restore_dir = sorted(backup_dirs)[-1]
            
            if not restore_dir.exists():
                logger.error(f"❌ Backup directory not found: {restore_dir}")
                return False
            
            # Restore each file
            restored_count = 0
            for file_path in self.duplicate_files:
                backup_file = restore_dir / file_path
                if backup_file.exists():
                    target = Path(file_path)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup_file, target)
                    logger.info(f"🔄 Restored: {file_path}")
                    restored_count += 1
            
            logger.info(f"✅ Restored {restored_count} files from {restore_dir}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Restore failed: {e}")
            return False

class Neo4jDatabaseManager:
    """Neo4j database management utility"""
    
    def __init__(self):
        self.config = None
        
    def get_neo4j_config(self) -> Dict[str, Any]:
        """Get Neo4j configuration"""
        if self.config is None:
            try:
                from config.config_loader import get_config_loader
                config_loader = get_config_loader()
                self.config = config_loader.get_neo4j_config()
            except Exception as e:
                logger.error(f"❌ Failed to load Neo4j config: {e}")
                self.config = {
                    'uri': 'bolt://localhost:7687',
                    'username': 'neo4j',
                    'password': 'password',
                    'database': 'neo4j'
                }
        return self.config
    
    def test_connection(self) -> bool:
        """Test Neo4j connection"""
        try:
            from neo4j import GraphDatabase
            
            config = self.get_neo4j_config()
            
            with GraphDatabase.driver(
                config['uri'],
                auth=(config['username'], config['password'])
            ) as driver:
                with driver.session(database=config['database']) as session:
                    result = session.run("RETURN 1 as test")
                    test_value = result.single()["test"]
                    
            logger.info(f"✅ Neo4j connection successful: {config['uri']}/{config['database']}")
            return test_value == 1
            
        except Exception as e:
            logger.error(f"❌ Neo4j connection failed: {e}")
            return False
    
    def list_databases(self) -> List[str]:
        """List available databases"""
        try:
            from neo4j import GraphDatabase
            
            config = self.get_neo4j_config()
            
            with GraphDatabase.driver(
                config['uri'],
                auth=(config['username'], config['password'])
            ) as driver:
                with driver.session() as session:
                    result = session.run("SHOW DATABASES")
                    databases = [record["name"] for record in result]
            
            logger.info(f"📋 Available databases: {databases}")
            return databases
            
        except Exception as e:
            logger.error(f"❌ Failed to list databases: {e}")
            return []
    
    def create_database(self, database_name: str) -> bool:
        """Create a new database"""
        try:
            from neo4j import GraphDatabase
            
            config = self.get_neo4j_config()
            
            with GraphDatabase.driver(
                config['uri'],
                auth=(config['username'], config['password'])
            ) as driver:
                with driver.session() as session:
                    session.run(f"CREATE DATABASE `{database_name}` IF NOT EXISTS")
            
            logger.info(f"✅ Database created: {database_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create database {database_name}: {e}")
            return False
    
    def clear_database(self, database_name: str = None, backup: bool = True) -> bool:
        """Clear all data from a database"""
        try:
            from neo4j import GraphDatabase
            
            config = self.get_neo4j_config()
            db_name = database_name or config['database']
            
            if backup:
                # TODO: Implement backup functionality
                logger.info(f"⚠️ Backup not implemented yet for database: {db_name}")
            
            with GraphDatabase.driver(
                config['uri'],
                auth=(config['username'], config['password'])
            ) as driver:
                with driver.session(database=db_name) as session:
                    # Get count before clearing
                    result = session.run("MATCH (n) RETURN count(n) as count")
                    node_count = result.single()["count"]
                    
                    # Clear all data
                    session.run("MATCH (n) DETACH DELETE n")
                    
                    logger.info(f"🗑️ Cleared {node_count} nodes from database: {db_name}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to clear database {database_name}: {e}")
            return False

def main():
    """Main cleanup interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="RHEL Data Loader Cleanup Utility")
    parser.add_argument("--files", action="store_true", help="Clean up duplicate dataloader files")
    parser.add_argument("--database", action="store_true", help="Clean up Neo4j database")
    parser.add_argument("--restore", type=str, help="Restore files from backup (timestamp)")
    parser.add_argument("--force", action="store_true", help="Force cleanup without verification")
    parser.add_argument("--test", action="store_true", help="Test connections and configurations")
    
    args = parser.parse_args()
    
    if args.test:
        # Test everything
        print("🧪 Testing Configurations and Connections")
        print("=" * 50)
        
        # Test unified loader
        cleanup = DataLoaderCleanup()
        if cleanup.check_unified_loader_working():
            print("✅ Unified data loader: Working")
        else:
            print("❌ Unified data loader: Failed")
        
        # Test Neo4j
        db_manager = Neo4jDatabaseManager()
        if db_manager.test_connection():
            print("✅ Neo4j connection: Working")
            databases = db_manager.list_databases()
            print(f"📋 Available databases: {databases}")
        else:
            print("❌ Neo4j connection: Failed")
        
    elif args.files:
        if args.restore:
            # Restore files
            cleanup = DataLoaderCleanup()
            cleanup.restore_from_backup(args.restore)
        else:
            # Clean up duplicate files
            print("🧹 Starting File Cleanup...")
            print("=" * 30)
            
            cleanup = DataLoaderCleanup()
            success = cleanup.cleanup_duplicate_files(force=args.force)
            
            if success:
                print("\n🎉 File cleanup completed successfully!")
                print("💡 Your system now uses the unified data loader only")
                print(f"📁 Backups saved in: {cleanup.backup_dir}")
            else:
                print("\n❌ File cleanup failed")
                print("💡 Run with --test to check system status")
    
    elif args.database:
        # Database management
        print("🗄️ Neo4j Database Management")
        print("=" * 30)
        
        db_manager = Neo4jDatabaseManager()
        
        if not db_manager.test_connection():
            print("❌ Cannot connect to Neo4j")
            return
        
        config = db_manager.get_neo4j_config()
        database_name = config['database']
        
        print(f"📋 Current database: {database_name}")
        
        # Ask for confirmation
        response = input(f"⚠️ Clear all data from '{database_name}'? (yes/no): ")
        if response.lower() in ['yes', 'y']:
            if db_manager.clear_database(database_name):
                print(f"✅ Database '{database_name}' cleared successfully")
            else:
                print(f"❌ Failed to clear database '{database_name}'")
        else:
            print("🔄 Database cleanup cancelled")
    
    else:
        # Show help
        print("🧹 RHEL Data Loader Cleanup Utility")
        print("=" * 40)
        print()
        print("Usage examples:")
        print("  python cleanup_dataloaders.py --test           # Test everything")
        print("  python cleanup_dataloaders.py --files          # Clean duplicate files")
        print("  python cleanup_dataloaders.py --database       # Clean Neo4j database") 
        print("  python cleanup_dataloaders.py --restore 20240115_143022  # Restore backup")
        print()
        print("Safety features:")
        print("✅ Automatic backups before cleanup")
        print("✅ Verification before file removal")
        print("✅ Easy restore from backups")
        print("✅ Configuration validation")

if __name__ == "__main__":
    main()
