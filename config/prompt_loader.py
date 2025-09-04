#!/usr/bin/env python3
"""
Safe Prompt Configuration Loader for PatchOps Intelligence
Production-grade YAML configuration management with safety features
"""

import os
import yaml
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import hashlib
from functools import lru_cache

logger = logging.getLogger(__name__)

class PromptConfigurationError(Exception):
    """Custom exception for prompt configuration issues"""
    pass

class SafePromptLoader:
    """
    Production-grade prompt configuration loader with safety features:
    - YAML validation and schema checking
    - Fallback to hardcoded prompts on failure
    - Environment-specific overrides
    - Caching for performance
    - Configuration validation
    """
    
    def __init__(self, config_path: Optional[str] = None, environment: str = "production"):
        """
        Initialize the prompt loader
        
        Args:
            config_path: Path to YAML config file (defaults to config/agent_prompts.yaml)
            environment: Environment name for env-specific overrides
        """
        self.config_path = config_path or self._get_default_config_path()
        self.environment = environment
        self._config_cache = {}
        self._config_hash = None
        
        logger.info(f"🔧 SafePromptLoader initialized for environment: {environment}")
    
    def _get_default_config_path(self) -> str:
        """Get default config path relative to current file"""
        current_dir = Path(__file__).parent
        return str(current_dir / "agent_prompts.yaml")
    
    @lru_cache(maxsize=1)
    def _load_config_file(self) -> Dict[str, Any]:
        """
        Load and cache YAML configuration with safety checks
        
        Returns:
            Parsed configuration dictionary
            
        Raises:
            PromptConfigurationError: If config loading/validation fails
        """
        try:
            # Check if config file exists
            if not os.path.exists(self.config_path):
                raise PromptConfigurationError(f"Config file not found: {self.config_path}")
            
            # Read and hash config for cache invalidation
            with open(self.config_path, 'r', encoding='utf-8') as f:
                content = f.read()
                config_hash = hashlib.md5(content.encode()).hexdigest()
            
            # Load YAML safely
            config = yaml.safe_load(content)
            
            # Validate configuration structure
            self._validate_config(config)
            
            # Cache the configuration
            self._config_hash = config_hash
            logger.info(f" Configuration loaded successfully from {self.config_path}")
            
            return config
            
        except yaml.YAMLError as e:
            raise PromptConfigurationError(f"YAML parsing error: {str(e)}")
        except Exception as e:
            raise PromptConfigurationError(f"Configuration loading error: {str(e)}")
    
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate configuration structure and required fields
        
        Args:
            config: Configuration dictionary to validate
            
        Raises:
            PromptConfigurationError: If validation fails
        """
        required_sections = ['agent_prompts']
        for section in required_sections:
            if section not in config:
                raise PromptConfigurationError(f"Missing required section: {section}")
        
        # Validate agent configurations
        required_agents = ['planner_agent', 'data_collection_agent', 'risk_analysis_agent', 'recommendation_agent']
        agent_prompts = config['agent_prompts']
        
        for agent in required_agents:
            if agent not in agent_prompts:
                raise PromptConfigurationError(f"Missing agent configuration: {agent}")
            
            agent_config = agent_prompts[agent]
            required_fields = ['name', 'system_prompt']
            
            for field in required_fields:
                if field not in agent_config:
                    raise PromptConfigurationError(f"Missing field '{field}' in agent '{agent}'")
        
        logger.debug(" Configuration validation passed")
    
    def _get_fallback_prompts(self) -> Dict[str, str]:
        """
        Provide hardcoded fallback prompts for safety
        
        Returns:
            Dictionary of fallback prompts for each agent
        """
        logger.warning("🔄 Using fallback hardcoded prompts")
        
        return {
            'planner_agent': """You are an intelligent PatchOps Analysis Planner. 

Your expertise:
- Strategic thinking about patch deployment risks
- Understanding complex enterprise RHEL environments  
- Creating optimal analysis workflows based on available data
- Identifying critical data gaps and analysis priorities

Your responsibilities:
1. Analyze the patch intelligence request comprehensively
2. Use available tools to understand what data exists
3. Create an intelligent analysis strategy based on findings
4. Identify potential risks and areas requiring deeper investigation
5. Plan the optimal sequence of analysis activities

Always use tools first to gather intelligence, then apply strategic reasoning
to create the most effective analysis approach for the specific situation.""",

            'data_collection_agent': """You are a PatchOps Data Collection Specialist.

Your expertise:
- Systematic intelligence gathering from Neo4j knowledge graphs
- Understanding relationships between patches, systems, and failures
- Comprehensive data collection strategies
- Quality assessment of gathered intelligence

Your responsibilities:
1. Execute the data collection strategy from the planner
2. Use tools systematically to gather comprehensive patch intelligence
3. Collect system profiles, patch histories, and failure patterns
4. Identify similar systems and cross-reference patterns
5. Ensure data quality and completeness for analysis

Be thorough and methodical. Missing data leads to poor risk assessments.
Always validate data quality and identify any gaps in the intelligence.""",

            'risk_analysis_agent': """You are a PatchOps Risk Analysis Expert.

Your expertise:
- Advanced risk calculation using historical patterns
- Evidence-based reasoning about patch deployment risks
- Statistical analysis of success/failure patterns
- Enterprise environment risk assessment

Your responsibilities:
1. Analyze all collected intelligence using advanced reasoning
2. Calculate risk probabilities based on historical evidence
3. Identify specific risk factors and their impact levels
4. Assess confidence levels in risk calculations
5. Provide detailed reasoning for all risk assessments

Use data-driven analysis. Every risk assessment must be backed by concrete
evidence from the knowledge graph. Distinguish between high-confidence
and low-confidence assessments based on available data quality.""",

            'recommendation_agent': """You are a PatchOps Implementation Strategist.

Your expertise:
- Enterprise patch deployment best practices
- Risk mitigation strategies for different environments
- Operational procedures for safe patch deployment
- Incident response and rollback planning

Your responsibilities:
1. Create specific, actionable deployment recommendations
2. Design risk mitigation strategies based on assessed risk levels
3. Plan pre-deployment preparations and safety measures
4. Create monitoring and validation procedures
5. Design comprehensive rollback and recovery plans

Recommendations must be practical, specific, and tailored to the assessed
risk level. High-risk deployments need comprehensive safety measures.
Low-risk deployments need basic but effective safety procedures."""
        }
    
    def get_agent_prompt(self, agent_name: str) -> str:
        """
        Get system prompt for a specific agent with safety fallbacks
        
        Args:
            agent_name: Name of the agent (e.g., 'planner_agent')
            
        Returns:
            System prompt string for the agent
        """
        try:
            # Load configuration
            config = self._load_config_file()
            
            # Get agent configuration
            agent_config = config['agent_prompts'][agent_name]
            
            # Format prompt with template variables
            prompt = agent_config['system_prompt'].format(
                name=agent_config.get('name', 'AI Agent'),
                expertise=self._format_list(agent_config.get('expertise', [])),
                responsibilities=self._format_list(agent_config.get('responsibilities', [])),
                instructions=agent_config.get('instructions', '')
            )
            
            # Apply environment-specific suffix if available
            if 'environments' in config and self.environment in config['environments']:
                env_config = config['environments'][self.environment]
                if 'global_suffix' in env_config:
                    prompt += env_config['global_suffix']
            
            logger.debug(f" Loaded prompt for {agent_name} from configuration")
            return prompt
            
        except Exception as e:
            logger.error(f"❌ Failed to load prompt for {agent_name}: {str(e)}")
            logger.info("🔄 Falling back to hardcoded prompt")
            
            # Fallback to hardcoded prompts
            fallback_prompts = self._get_fallback_prompts()
            return fallback_prompts.get(agent_name, "You are a helpful AI assistant.")
    
    def _format_list(self, items: list) -> str:
        """Format a list of items as a bullet-pointed string"""
        if not items:
            return ""
        return "\n".join(f"- {item}" for item in items)
    
    def get_request_template(self, template_name: str = "standard_request", **kwargs) -> str:
        """
        Get request template for formatting agent requests
        
        Args:
            template_name: Name of template to retrieve
            **kwargs: Variables to substitute in the template
            
        Returns:
            Formatted template string
        """
        try:
            config = self._load_config_file()
            templates = config.get('templates', {})
            template = templates.get(template_name, "")
            
            # Format template with provided variables
            if template and kwargs:
                return template.format(**kwargs)
            return template
            
        except Exception as e:
            logger.error(f"❌ Failed to load template {template_name}: {str(e)}")
            return ""
    
    def get_node_system_message(self, node_name: str) -> str:
        """
        Get system message for a specific workflow node
        
        Args:
            node_name: Name of the workflow node
            
        Returns:
            System message string
        """
        try:
            config = self._load_config_file()
            node_messages = config.get('node_system_messages', {})
            return node_messages.get(node_name, "")
        except Exception as e:
            logger.error(f"❌ Failed to load node system message {node_name}: {str(e)}")
            return "You are a helpful AI assistant."
    
    def reload_config(self) -> bool:
        """
        Force reload configuration (useful for development/testing)
        
        Returns:
            True if reload successful, False otherwise
        """
        try:
            # Clear cache
            self._load_config_file.cache_clear()
            self._config_cache.clear()
            
            # Reload
            self._load_config_file()
            logger.info("🔄 Configuration reloaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Configuration reload failed: {str(e)}")
            return False
