#!/usr/bin/env python3
"""
Unified Configuration Loader for RHEL Intelligence System
Extends SafePromptLoader pattern to handle all configuration needs
"""

import os
import yaml
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from functools import lru_cache

from .prompt_loader import SafePromptLoader, PromptConfigurationError

logger = logging.getLogger(__name__)

class UnifiedConfigLoader(SafePromptLoader):
    """
    Unified configuration loader that extends SafePromptLoader
    Handles both agent prompts and data loader configuration
    """
    
    def __init__(self, environment: str = "production"):
        """
        Initialize unified config loader
        
        Args:
            environment: Environment name for env-specific overrides
        """
        # Initialize parent class for prompt loading
        super().__init__(environment=environment)
        
        # Add dataloader config path
        self.dataloader_config_path = self._get_dataloader_config_path()
        self._dataloader_config_cache = {}
        
        logger.info(f"🔧 UnifiedConfigLoader initialized for environment: {environment}")
    
    def _get_dataloader_config_path(self) -> str:
        """Get dataloader config path relative to current file"""
        current_dir = Path(__file__).parent
        return str(current_dir / "data_loader_config.yaml")
    
    @lru_cache(maxsize=1)
    def _load_dataloader_config(self) -> Dict[str, Any]:
        """
        Load and cache dataloader configuration with safety checks
        
        Returns:
            Parsed dataloader configuration dictionary
            
        Raises:
            PromptConfigurationError: If config loading/validation fails
        """
        try:
            # Check if config file exists
            if not os.path.exists(self.dataloader_config_path):
                logger.warning(f"Dataloader config not found: {self.dataloader_config_path}")
                return self._get_fallback_dataloader_config()
            
            # Read and load YAML safely
            with open(self.dataloader_config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            config = yaml.safe_load(content)
            
            # Validate configuration structure
            self._validate_dataloader_config(config)
            
            logger.info(f"✅ Dataloader configuration loaded from {self.dataloader_config_path}")
            return config
            
        except yaml.YAMLError as e:
            logger.error(f"❌ Dataloader YAML parsing error: {str(e)}")
            return self._get_fallback_dataloader_config()
        except Exception as e:
            logger.error(f"❌ Dataloader config loading error: {str(e)}")
            return self._get_fallback_dataloader_config()
    
    def _validate_dataloader_config(self, config: Dict[str, Any]) -> None:
        """
        Validate dataloader configuration structure
        
        Args:
            config: Configuration dictionary to validate
        """
        required_sections = ['llm_config', 'data_sources', 'text_processing']
        for section in required_sections:
            if section not in config:
                logger.warning(f"Missing dataloader config section: {section}")
        
        logger.debug("✅ Dataloader configuration validation passed")
    
    def _get_fallback_dataloader_config(self) -> Dict[str, Any]:
        """
        Provide hardcoded fallback dataloader config for safety
        
        Returns:
            Dictionary of fallback dataloader configuration
        """
        logger.warning("🔄 Using fallback hardcoded dataloader config")
        
        return {
            'llm_config': {
                'base_url_env': 'OPENAI_BASE_URL',
                'api_key_env': 'OPENAI_API_KEY',
                'model_env': 'MODEL',
                'timeout_env': 'HTTP_TIMEOUT',
                'fallback_config': {
                    'base_url': 'https://llama-4-scout-17b-16e-w4a16-maas-apicast-production.apps.prod.rhoai.rh-aiservices-bu.com:443/v1',
                    'model': 'llama-4-scout-17b-16e-w4a16',
                    'timeout': 180
                }
            },
            'data_sources': {
                'rhel_systems': {
                    'type': 'filesystem',
                    'base_path': 'simulated_rhel_systems',
                    'file_patterns': {
                        'config_files': ['etc/redhat-release', 'etc/yum.conf'],
                        'log_files': ['var/log/yum.log', 'var/log/messages'],
                        'system_files': ['var/lib/rpm/packages.txt', 'usr/lib/systemd/system/*.service']
                    }
                }
            },
            'text_processing': {
                'chunking': {
                    'max_chunk_size': 2000,
                    'chunk_overlap': 200,
                    'separators': ['\n\n', '\n', ' ', '']
                },
                'cleaning': {
                    'remove_ansi_codes': True,
                    'normalize_whitespace': True
                }
            },
            'pipeline': {
                'phases': {
                    'ai_extraction': {
                        'enabled': True,
                        'max_retries': 3
                    }
                }
            }
        }
    
    def get_llm_config(self) -> Dict[str, Any]:
        """
        Get LLM configuration with environment variable resolution
        
        Returns:
            LLM configuration dictionary with resolved values
        """
        try:
            config = self._load_dataloader_config()
            llm_config = config.get('llm_config', {})
            
            # Resolve environment variables
            resolved_config = {}
            
            # Get base URL
            base_url_env = llm_config.get('base_url_env', 'OPENAI_BASE_URL')
            resolved_config['base_url'] = os.getenv(
                base_url_env, 
                llm_config.get('fallback_config', {}).get('base_url', '')
            )
            
            # Get API key
            api_key_env = llm_config.get('api_key_env', 'OPENAI_API_KEY')
            resolved_config['api_key'] = os.getenv(
                api_key_env,
                llm_config.get('fallback_config', {}).get('api_key', '')
            )
            
            # Get model
            model_env = llm_config.get('model_env', 'MODEL')
            resolved_config['model'] = os.getenv(
                model_env,
                llm_config.get('fallback_config', {}).get('model', 'llama-4-scout-17b-16e-w4a16')
            )
            
            # Get timeout
            timeout_env = llm_config.get('timeout_env', 'HTTP_TIMEOUT')
            resolved_config['timeout'] = int(os.getenv(
                timeout_env,
                str(llm_config.get('fallback_config', {}).get('timeout', 180))
            ))
            
            logger.debug(f"✅ LLM config resolved: {resolved_config['base_url']}")
            return resolved_config
            
        except Exception as e:
            logger.error(f"❌ Failed to get LLM config: {str(e)}")
            return self._get_fallback_dataloader_config()['llm_config']['fallback_config']
    
    def get_data_source_config(self, source_name: str = 'rhel_systems') -> Dict[str, Any]:
        """
        Get configuration for a specific data source
        
        Args:
            source_name: Name of the data source
            
        Returns:
            Data source configuration dictionary
        """
        try:
            config = self._load_dataloader_config()
            data_sources = config.get('data_sources', {})
            
            source_config = data_sources.get(source_name, {})
            
            # Apply environment-specific overrides
            if 'environments' in config and self.environment in config['environments']:
                env_config = config['environments'][self.environment]
                if 'data_sources' in env_config and source_name in env_config['data_sources']:
                    env_overrides = env_config['data_sources'][source_name]
                    source_config.update(env_overrides)
            
            logger.debug(f"✅ Data source config retrieved: {source_name}")
            return source_config
            
        except Exception as e:
            logger.error(f"❌ Failed to get data source config for {source_name}: {str(e)}")
            return self._get_fallback_dataloader_config()['data_sources'].get(source_name, {})
    
    def get_text_processing_config(self) -> Dict[str, Any]:
        """
        Get text processing configuration
        
        Returns:
            Text processing configuration dictionary
        """
        try:
            config = self._load_dataloader_config()
            text_config = config.get('text_processing', {})
            
            # Apply environment-specific overrides
            if 'environments' in config and self.environment in config['environments']:
                env_config = config['environments'][self.environment]
                if 'text_processing' in env_config:
                    env_overrides = env_config['text_processing']
                    # Deep merge configuration
                    for key, value in env_overrides.items():
                        if isinstance(value, dict) and key in text_config:
                            text_config[key].update(value)
                        else:
                            text_config[key] = value
            
            logger.debug("✅ Text processing config retrieved")
            return text_config
            
        except Exception as e:
            logger.error(f"❌ Failed to get text processing config: {str(e)}")
            return self._get_fallback_dataloader_config()['text_processing']
    
    def get_pipeline_config(self) -> Dict[str, Any]:
        """
        Get pipeline configuration
        
        Returns:
            Pipeline configuration dictionary
        """
        try:
            config = self._load_dataloader_config()
            pipeline_config = config.get('pipeline', {})
            
            # Apply environment-specific overrides
            if 'environments' in config and self.environment in config['environments']:
                env_config = config['environments'][self.environment]
                if 'pipeline' in env_config:
                    env_overrides = env_config['pipeline']
                    # Deep merge configuration
                    self._deep_merge(pipeline_config, env_overrides)
            
            logger.debug("✅ Pipeline config retrieved")
            return pipeline_config
            
        except Exception as e:
            logger.error(f"❌ Failed to get pipeline config: {str(e)}")
            return self._get_fallback_dataloader_config()['pipeline']
    
    def _deep_merge(self, base_dict: Dict, override_dict: Dict) -> None:
        """
        Deep merge override dictionary into base dictionary
        
        Args:
            base_dict: Base dictionary to merge into
            override_dict: Override dictionary to merge from
        """
        for key, value in override_dict.items():
            if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
                self._deep_merge(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def is_phase_enabled(self, phase_name: str) -> bool:
        """
        Check if a pipeline phase is enabled
        
        Args:
            phase_name: Name of the pipeline phase
            
        Returns:
            True if phase is enabled, False otherwise
        """
        try:
            pipeline_config = self.get_pipeline_config()
            phases = pipeline_config.get('phases', {})
            phase_config = phases.get(phase_name, {})
            return phase_config.get('enabled', True)
        except Exception:
            return True  # Default to enabled
    
    def get_entity_extraction_config(self) -> Dict[str, Any]:
        """
        Get entity extraction configuration
        
        Returns:
            Entity extraction configuration dictionary
        """
        try:
            config = self._load_dataloader_config()
            return config.get('entity_extraction', {})
        except Exception as e:
            logger.error(f"❌ Failed to get entity extraction config: {str(e)}")
            return {}
    
    def get_neo4j_config(self) -> Dict[str, Any]:
        """
        Get Neo4j configuration with environment variable resolution
        
        Returns:
            Neo4j configuration dictionary with resolved values
        """
        try:
            config = self._load_dataloader_config()
            neo4j_config = config.get('neo4j_config', {})
            
            # Resolve environment variables
            resolved_config = {}
            
            # Get URI
            uri_env = neo4j_config.get('uri_env', 'NEO4J_URI')
            resolved_config['uri'] = os.getenv(
                uri_env, 
                neo4j_config.get('fallback_config', {}).get('uri', 'bolt://localhost:7687')
            )
            
            # Get username
            username_env = neo4j_config.get('username_env', 'NEO4J_USERNAME')
            resolved_config['username'] = os.getenv(
                username_env,
                neo4j_config.get('fallback_config', {}).get('username', 'neo4j')
            )
            
            # Get password
            password_env = neo4j_config.get('password_env', 'NEO4J_PASSWORD')
            resolved_config['password'] = os.getenv(
                password_env,
                neo4j_config.get('fallback_config', {}).get('password', 'password')
            )
            
            # Get database name (optional)
            database_env = neo4j_config.get('database_env', 'NEO4J_DATABASE')
            resolved_config['database'] = os.getenv(
                database_env,
                neo4j_config.get('fallback_config', {}).get('database', 'neo4j')
            )
            
            # Get management options
            management = neo4j_config.get('management', {})
            resolved_config['management'] = management
            
            logger.debug(f"✅ Neo4j config resolved: {resolved_config['uri']}/{resolved_config['database']}")
            return resolved_config
            
        except Exception as e:
            logger.error(f"❌ Failed to get Neo4j config: {str(e)}")
            # Return safe fallback
            return {
                'uri': 'bolt://localhost:7687',
                'username': 'neo4j', 
                'password': 'password',
                'database': 'neo4j',
                'management': {
                    'auto_create_database': False,
                    'clear_on_startup': False,
                    'backup_before_clear': True,
                    'max_connections': 50
                }
            }
    
    def get_cleanup_config(self) -> Dict[str, Any]:
        """
        Get data cleanup configuration
        
        Returns:
            Data cleanup configuration dictionary
        """
        try:
            config = self._load_dataloader_config()
            return config.get('data_cleanup', {
                'auto_cleanup_on_load': False,
                'backup_old_data': True,
                'cleanup_strategies': ['clear_existing_nodes']
            })
        except Exception as e:
            logger.error(f"❌ Failed to get cleanup config: {str(e)}")
            return {
                'auto_cleanup_on_load': False,
                'backup_old_data': True, 
                'cleanup_strategies': ['clear_existing_nodes']
            }
    
    def reload_all_configs(self) -> bool:
        """
        Force reload all configurations (useful for development/testing)
        
        Returns:
            True if reload successful, False otherwise
        """
        try:
            # Clear parent class cache
            success = super().reload_config()
            
            # Clear dataloader config cache
            self._load_dataloader_config.cache_clear()
            self._dataloader_config_cache.clear()
            
            # Reload dataloader config
            self._load_dataloader_config()
            
            logger.info("🔄 All configurations reloaded successfully")
            return success
            
        except Exception as e:
            logger.error(f"❌ Configuration reload failed: {str(e)}")
            return False

# Create global instance following your pattern
_config_loader = None

def get_config_loader(environment: str = None) -> UnifiedConfigLoader:
    """
    Get global configuration loader instance (singleton pattern)
    
    Args:
        environment: Environment name (defaults to current environment)
        
    Returns:
        UnifiedConfigLoader instance
    """
    global _config_loader
    
    if _config_loader is None or (environment and environment != _config_loader.environment):
        env = environment or os.getenv('ENVIRONMENT', 'production')
        _config_loader = UnifiedConfigLoader(environment=env)
    
    return _config_loader
