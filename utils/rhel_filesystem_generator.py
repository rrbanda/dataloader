#!/usr/bin/env python3
"""
RHEL Filesystem Generator - Creates realistic RHEL system files for development
Simulates enterprise RHEL environments without needing SSH access to real systems
"""

import os
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path

class RHELFilesystemGenerator:
    """Generates realistic RHEL filesystem content for development/testing and Graph RAG agents"""
    
    def __init__(self, base_path: str = "simulated_rhel_systems", num_systems: int = 5):
        self.base_path = Path(base_path)
        self.num_systems = num_systems
        
        # Generate realistic enterprise system configurations
        if num_systems <= 10:
            # Use hardcoded systems for small deployments (existing behavior)
            self.systems = self._get_hardcoded_systems()
        else:
            # Generate large-scale enterprise systems programmatically
            self.systems = self._generate_enterprise_systems(num_systems)
        
        # Initialize packages and metadata
        self._initialize_packages()
    
    def _get_hardcoded_systems(self):
        """Original hardcoded systems for small deployments"""
        return {
            "web-prod-01": {
                "environment": "production",
                "rhel_version": "9.2",
                "kernel": "5.14.0-284.25.1.el9_2.x86_64",
                "services": ["httpd", "mysql", "redis", "chronyd", "sshd"],
                "criticality": "high",
                "datacenter": "DC-East-1",
                # Agent-compatible properties
                "prop_hostname": "web-prod-01.company.com",
                "prop_ip": "10.1.1.10", 
                "prop_cpu_cores": "8",
                "prop_memory_gb": "32", 
                "prop_disk_gb": "500",
                "prop_business_service": "Customer_Portal",
                "prop_team_owner": "Platform_Engineering",
                "prop_sla_availability": "99.95"
            },
            "web-prod-02": {
                "environment": "production", 
                "rhel_version": "9.1",
                "kernel": "5.14.0-162.23.1.el9_1.x86_64",
                "services": ["httpd", "postgresql", "nginx", "chronyd", "sshd"],
                "criticality": "high",
                "datacenter": "DC-West-1",
                # Agent-compatible properties
                "prop_hostname": "web-prod-02.company.com",
                "prop_ip": "10.1.1.11",
                "prop_cpu_cores": "8",
                "prop_memory_gb": "32",
                "prop_business_service": "Customer_Portal",
                "prop_team_owner": "Platform_Engineering"
            },
            "app-prod-01": {
                "environment": "production",
                "rhel_version": "9.2", 
                "kernel": "5.14.0-284.25.1.el9_2.x86_64",
                "services": ["tomcat", "elasticsearch", "docker", "chronyd", "sshd"],
                "criticality": "critical",
                "datacenter": "DC-Central-1",
                # Agent-compatible properties
                "prop_hostname": "app-prod-01.company.com",
                "prop_ip": "10.2.1.10",
                "prop_cpu_cores": "16",
                "prop_memory_gb": "64",
                "prop_business_service": "Core_Application",
                "prop_team_owner": "Application_Development"
            },
            "db-prod-01": {
                "environment": "production",
                "rhel_version": "8.8",
                "kernel": "4.18.0-477.27.1.el8_8.x86_64", 
                "services": ["mysql", "redis", "memcached", "chronyd", "sshd"],
                "criticality": "critical",
                "datacenter": "DC-East-1",
                # Agent-compatible properties
                "prop_hostname": "db-prod-01.company.com", 
                "prop_ip": "10.3.1.10",
                "prop_cpu_cores": "24",
                "prop_memory_gb": "128",
                "prop_business_service": "Database_Services", 
                "prop_team_owner": "Database_Administration"
            },
            "web-stage-01": {
                "environment": "staging",
                "rhel_version": "9.2",
                "kernel": "5.14.0-284.25.1.el9_2.x86_64",
                "services": ["httpd", "mysql", "chronyd", "sshd"],
                "criticality": "medium",
                "datacenter": "DC-Central-1",
                # Agent-compatible properties
                "prop_hostname": "web-stage-01.company.com",
                "prop_ip": "10.10.1.10",
                "prop_cpu_cores": "4",
                "prop_memory_gb": "16",
                "prop_business_service": "Testing_Environment"
            }
        }
    
    def _generate_enterprise_systems(self, num_systems: int):
        """Generate large-scale realistic enterprise systems (non-fake data)"""
        systems = {}
        
        # Real enterprise system types and configurations
        system_types = [
            {
                "prefix": "web",
                "services": ["httpd", "nginx", "haproxy", "chronyd", "sshd"],
                "cpu_range": (4, 16),
                "memory_range": (8, 64),
                "business_services": ["Customer_Portal", "Corporate_Website", "API_Gateway"],
                "teams": ["Platform_Engineering", "DevOps", "Frontend_Engineering"]
            },
            {
                "prefix": "app",
                "services": ["tomcat", "java", "docker", "chronyd", "sshd", "elasticsearch"],
                "cpu_range": (8, 32),
                "memory_range": (16, 128),
                "business_services": ["Core_Application", "Payment_Processing", "User_Management", "Inventory_System"],
                "teams": ["Application_Development", "Backend_Engineering", "API_Team"]
            },
            {
                "prefix": "db",
                "services": ["mysql", "postgresql", "redis", "memcached", "chronyd", "sshd"],
                "cpu_range": (16, 64),
                "memory_range": (32, 256),
                "business_services": ["Primary_Database", "Analytics_DB", "Cache_Layer", "Data_Warehouse"],
                "teams": ["Database_Administration", "Data_Engineering", "Backend_Engineering"]
            },
            {
                "prefix": "cache",
                "services": ["redis", "memcached", "nginx", "chronyd", "sshd"],
                "cpu_range": (4, 16),
                "memory_range": (16, 64),
                "business_services": ["Cache_Layer", "Session_Store", "Real_Time_Data"],
                "teams": ["Platform_Engineering", "Performance_Engineering"]
            },
            {
                "prefix": "api",
                "services": ["nginx", "docker", "kubernetes", "chronyd", "sshd"],
                "cpu_range": (8, 24),
                "memory_range": (16, 96),
                "business_services": ["API_Gateway", "Microservices", "Integration_Layer"],
                "teams": ["API_Team", "Microservices_Team", "Integration_Engineering"]
            },
            {
                "prefix": "analytics",
                "services": ["elasticsearch", "kibana", "logstash", "chronyd", "sshd"],
                "cpu_range": (12, 48),
                "memory_range": (32, 192),
                "business_services": ["Data_Analytics", "Log_Processing", "Search_Engine"],
                "teams": ["Data_Engineering", "Analytics_Team", "DevOps"]
            },
            {
                "prefix": "monitor",
                "services": ["prometheus", "grafana", "alertmanager", "chronyd", "sshd"],
                "cpu_range": (4, 16),
                "memory_range": (8, 32),
                "business_services": ["Monitoring", "Alerting", "Metrics_Collection"],
                "teams": ["SRE", "DevOps", "Platform_Engineering"]
            },
            {
                "prefix": "file",
                "services": ["nfs", "samba", "rsync", "chronyd", "sshd"],
                "cpu_range": (4, 16),
                "memory_range": (8, 64),
                "business_services": ["File_Storage", "Backup_System", "Shared_Storage"],
                "teams": ["Infrastructure", "Storage_Engineering", "IT_Operations"]
            }
        ]
        
        # Real enterprise environments and datacenters
        environments = ["production", "staging", "development", "testing", "dr"]
        env_weights = [0.4, 0.2, 0.2, 0.1, 0.1]  # More production systems
        
        datacenters = [
            "DC-East-1", "DC-East-2", "DC-West-1", "DC-West-2", 
            "DC-Central-1", "DC-Europe-1", "DC-Asia-1", "AWS-US-East-1",
            "Azure-West-2", "GCP-Central-1"
        ]
        
        # Real RHEL versions with realistic distribution
        rhel_versions = [
            ("9.3", "5.14.0-362.8.1.el9_3.x86_64", 0.3),
            ("9.2", "5.14.0-284.25.1.el9_2.x86_64", 0.25),
            ("9.1", "5.14.0-162.23.1.el9_1.x86_64", 0.15),
            ("8.9", "4.18.0-513.5.1.el8_9.x86_64", 0.2),
            ("8.8", "4.18.0-477.27.1.el8_8.x86_64", 0.1)
        ]
        
        # Generate systems
        system_counter = 1
        for i in range(num_systems):
            # Select system type
            system_type = random.choice(system_types)
            
            # Select environment (weighted towards production)
            environment = random.choices(environments, weights=env_weights)[0]
            
            # Generate system name
            if environment == "production":
                system_name = f"{system_type['prefix']}-prod-{system_counter:02d}"
            elif environment == "staging":
                system_name = f"{system_type['prefix']}-stage-{system_counter:02d}"
            elif environment == "development":
                system_name = f"{system_type['prefix']}-dev-{system_counter:02d}"
            elif environment == "testing":
                system_name = f"{system_type['prefix']}-test-{system_counter:02d}"
            else:  # dr
                system_name = f"{system_type['prefix']}-dr-{system_counter:02d}"
            
            # Select RHEL version (weighted)
            rhel_info = random.choices(rhel_versions, weights=[w[2] for w in rhel_versions])[0]
            
            # Generate realistic hardware specs
            cpu_cores = random.randint(*system_type["cpu_range"])
            memory_gb = random.choice([8, 16, 32, 64, 96, 128, 192, 256])
            disk_gb = random.choice([100, 200, 500, 1000, 2000, 4000])
            
            # Generate IP address based on datacenter and environment
            datacenter = random.choice(datacenters)
            if environment == "production":
                ip_base = "10.1"
            elif environment == "staging":
                ip_base = "10.2"
            elif environment == "development":
                ip_base = "192.168"
            else:
                ip_base = "172.16"
            
            subnet = random.randint(1, 254)
            host = random.randint(10, 250)
            ip_address = f"{ip_base}.{subnet}.{host}"
            
            # Select business service and team
            business_service = random.choice(system_type["business_services"])
            team_owner = random.choice(system_type["teams"])
            
            # Generate criticality based on environment and system type
            if environment == "production" and system_type["prefix"] in ["db", "app"]:
                criticality = "critical"
            elif environment == "production":
                criticality = "high"
            elif environment == "staging":
                criticality = "medium"
            else:
                criticality = "low"
            
            # Generate SLA based on criticality
            sla_map = {
                "critical": "99.99",
                "high": "99.95",
                "medium": "99.9",
                "low": "99.5"
            }
            
            systems[system_name] = {
                "environment": environment,
                "rhel_version": rhel_info[0],
                "kernel": rhel_info[1],
                "services": system_type["services"],
                "criticality": criticality,
                "datacenter": datacenter,
                # Agent-compatible properties
                "prop_hostname": f"{system_name}.{environment}.company.com",
                "prop_ip": ip_address,
                "prop_cpu_cores": str(cpu_cores),
                "prop_memory_gb": str(memory_gb),
                "prop_disk_gb": str(disk_gb),
                "prop_business_service": business_service,
                "prop_team_owner": team_owner,
                "prop_sla_availability": sla_map[criticality]
            }
            
            system_counter += 1
        
        return systems
    
    def _initialize_packages(self):
        """Initialize common RHEL packages with realistic versions"""
        self.packages = {
            "httpd": "2.4.53-11.el9_2.5",
            "httpd-tools": "2.4.53-11.el9_2.5", 
            "mysql-server": "8.0.32-1.el9_0",
            "mysql": "8.0.32-1.el9_0",
            "postgresql": "13.7-1.el9_0",
            "postgresql-server": "13.7-1.el9_0",
            "redis": "6.2.7-1.el9",
            "nginx": "1.20.1-13.el9",
            "tomcat": "9.0.62-5.el9_0.1",
            "elasticsearch": "7.17.7-1",
            "docker": "20.10.21-3.el9",
            "kernel": "5.14.0-284.25.1.el9_2",
            "glibc": "2.34-60.el9_2.7",
            "openssl": "3.0.7-16.el9_2",
            "systemd": "250-12.el9_2.6",
            "openssh": "8.7p1-24.el9_2",
            "chrony": "4.2-1.el9"
        }
        
        # Realistic patch/errata data
        self.patches = [
            {
                "id": "RHSA-2024-1234",
                "type": "Security",
                "severity": "Important", 
                "packages": ["httpd", "httpd-tools"],
                "cves": ["CVE-2024-12345", "CVE-2024-12346"],
                "description": "Important: httpd security update"
            },
            {
                "id": "RHSA-2024-1235", 
                "type": "Security",
                "severity": "Critical",
                "packages": ["mysql-server", "mysql"],
                "cves": ["CVE-2024-12347"],
                "description": "Critical: mysql security update"
            },
            {
                "id": "RHSA-2024-1236",
                "type": "Security", 
                "severity": "Important",
                "packages": ["kernel"],
                "cves": ["CVE-2024-12348", "CVE-2024-12349"],
                "description": "Important: kernel security update"
            },
            {
                "id": "RHSA-2024-0987",
                "type": "Bugfix",
                "severity": "Moderate",
                "packages": ["systemd"],
                "cves": [],
                "description": "systemd bug fix and enhancement update"
            }
        ]
        
        # Agent-compatible infrastructure for Graph RAG (NEW)
        self.agent_infrastructure = {
            "incidents": {
                "incident_001": {
                    "prop_incident_id": "INC-2024-001234",
                    "prop_severity": "P1_Critical",
                    "prop_status": "Resolved",
                    "prop_start_time": "2024-09-15T14:30:00Z",
                    "prop_end_time": "2024-09-15T16:45:00Z", 
                    "prop_duration_minutes": "135",
                    "prop_root_cause": "Memory_leak_in_Tomcat_application",
                    "prop_affected_users": "15000",
                    "description": "Critical production outage caused by memory leak in customer portal application"
                },
                "incident_002": {
                    "prop_incident_id": "INC-2024-001198", 
                    "prop_severity": "P2_High",
                    "prop_status": "Resolved",
                    "prop_start_time": "2024-09-10T09:15:00Z",
                    "prop_end_time": "2024-09-10T10:30:00Z",
                    "prop_root_cause": "Database_connection_pool_exhaustion",
                    "description": "Database connectivity issues causing slow response times in web portal"
                }
            },
            "security_events": {
                "security_001": {
                    "prop_event_id": "SEC-2024-000567",
                    "prop_event_type": "SQL_Injection_Attempt",
                    "prop_severity": "High", 
                    "prop_source_ip": "192.168.100.250",
                    "prop_target_system": "web-prod-01",
                    "prop_blocked": "true",
                    "description": "Blocked SQL injection attempt targeting user authentication endpoint"
                }
            },
            "applications": {
                "customer_portal": {
                    "prop_app_name": "CustomerPortal",
                    "prop_version": "v2.1.5", 
                    "prop_language": "Java_Spring_Boot",
                    "prop_database": "MySQL",
                    "prop_active_sessions": "5000",
                    "description": "Customer-facing web portal for account management and billing"
                }
            }
        }
        
        # Agent-compatible relationships for Cypher queries (NEW)
        self.agent_relationships = [
            # Server dependencies
            {"source": "web-prod-01", "target": "app-prod-01", "type": "DEPENDS_ON", "prop_connection_type": "HTTP"},
            {"source": "web-prod-02", "target": "app-prod-01", "type": "DEPENDS_ON", "prop_connection_type": "HTTP"},
            {"source": "app-prod-01", "target": "db-prod-01", "type": "DEPENDS_ON", "prop_connection_type": "TCP_3306"},
            
            # Incident relationships
            {"source": "incident_001", "target": "app-prod-01", "type": "AFFECTED", "prop_impact": "service_unavailable"},
            {"source": "incident_002", "target": "db-prod-01", "type": "AFFECTED", "prop_impact": "performance_degradation"},
            
            # Security relationships  
            {"source": "security_001", "target": "web-prod-01", "type": "TARGETED", "prop_endpoint": "/api/users"},
        ]
    
    def generate_all_systems(self):
        """Generate realistic files for all simulated systems (enhanced for Graph RAG agents)"""
        print(f"🏗️ Generating {len(self.systems)} realistic RHEL systems for Graph RAG agents...")
        
        # Progress tracking for large deployments
        total_systems = len(self.systems)
        for i, (system_id, config) in enumerate(self.systems.items(), 1):
            if total_systems > 10:
                print(f"   📁 Generating {system_id} ({config['environment']}) - {i}/{total_systems}")
            else:
                print(f"   📁 Generating {system_id} ({config['environment']})...")
            self.generate_system_files(system_id, config)
        
        # Generate agent-compatible metadata (NEW)
        self.generate_agent_metadata()
        
        print(" All simulated RHEL systems generated successfully!")
        print("🤖 Agent-compatible metadata generated for Graph RAG")
    
    def generate_system_files(self, system_id: str, config: Dict):
        """Generate all critical files for a single system"""
        system_path = self.base_path / system_id
        
        # Generate all critical file types
        self._generate_redhat_release(system_path, config)
        self._generate_yum_config(system_path, config)
        self._generate_yum_repos(system_path, config)
        self._generate_rhsm_config(system_path, config)
        self._generate_rpm_database(system_path, config)
        self._generate_yum_logs(system_path, config)
        self._generate_dnf_logs(system_path, config)
        self._generate_system_logs(system_path, config)
        self._generate_audit_logs(system_path, config)
        self._generate_yum_history(system_path, config)
        self._generate_systemd_services(system_path, config)
        self._generate_proc_files(system_path, config)
        self._generate_security_configs(system_path, config)
        
        # Generate agent-compatible operational data (NEW)
        self._generate_agent_operational_logs(system_path, config, system_id)
        self._generate_performance_metrics(system_path, config)
        self._generate_network_topology_files(system_path, config)
        
        # Generate authentic RHEL compliance data (NEW)
        self._generate_authentic_compliance_data(system_path, config)
        
        # Generate specialized agent data (NEW - for Graph RAG agents)
        self._generate_security_agent_data(system_path, config, system_id)
        self._generate_performance_agent_data(system_path, config)
        self._generate_compliance_agent_data(system_path, config)
        self._generate_approval_gate_data(system_path, config)
        
        # Clean up any fake directories and files that don't exist on real RHEL (AUTHENTICITY FIX)
        self._cleanup_fake_directories(system_path)
        self._cleanup_fake_files(system_path)
    
    def _generate_redhat_release(self, system_path: Path, config: Dict):
        """Generate /etc/redhat-release"""
        release_file = system_path / "etc" / "redhat-release"
        release_file.parent.mkdir(parents=True, exist_ok=True)
        
        content = f"Red Hat Enterprise Linux release {config['rhel_version']} (Plow)"
        release_file.write_text(content)
    
    def _generate_yum_config(self, system_path: Path, config: Dict):
        """Generate /etc/yum.conf"""
        yum_conf = system_path / "etc" / "yum.conf"
        
        # Realistic yum configuration
        content = f"""[main]
cachedir=/var/cache/yum/$basearch/$releasever
keepcache=0
debuglevel=2
logfile=/var/log/yum.log
exactarch=1
obsoletes=1
gpgcheck=1
plugins=1
installonly_limit=3
skip_broken=1

# Enterprise proxy configuration
proxy=http://proxy.company.com:8080
proxy_username=yum-service
proxy_password=***redacted***

# Security settings
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt

# Performance tuning
retries=10
timeout=30
bandwidth=1024

# Environment-specific settings
exclude=kernel* firefox* thunderbird*
{"installroot=/mnt/sysimage" if config.get("environment") == "staging" else ""}
"""
        yum_conf.write_text(content)
    
    def _generate_yum_repos(self, system_path: Path, config: Dict):
        """Generate /etc/yum.repos.d/*.repo files"""
        repos_dir = system_path / "etc" / "yum.repos.d"
        repos_dir.mkdir(parents=True, exist_ok=True)
        
        # Red Hat repositories
        rhel_repo = repos_dir / "redhat.repo"
        rhel_content = f"""[rhel-{config['rhel_version']}-for-x86_64-baseos-rpms]
name=Red Hat Enterprise Linux {config['rhel_version']} for x86_64 - BaseOS (RPMs)
baseurl=https://cdn.redhat.com/content/dist/rhel{config['rhel_version'].split('.')[0]}/
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
sslverify=1
sslcacert=/etc/rhsm/ca/redhat-uep.pem
sslclientkey=/etc/pki/entitlement/key.pem
sslclientcert=/etc/pki/entitlement/cert.pem
metadata_expire=86400
enabled_metadata=1

[rhel-{config['rhel_version']}-for-x86_64-appstream-rpms]
name=Red Hat Enterprise Linux {config['rhel_version']} for x86_64 - AppStream (RPMs)
baseurl=https://cdn.redhat.com/content/dist/rhel{config['rhel_version'].split('.')[0]}/
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
sslverify=1
metadata_expire=86400
"""
        rhel_repo.write_text(rhel_content)
        
        # EPEL repository (if applicable)
        if random.choice([True, False]):
            epel_repo = repos_dir / "epel.repo"
            epel_content = f"""[epel]
name=Extra Packages for Enterprise Linux {config['rhel_version'].split('.')[0]} - x86_64
baseurl=https://download.fedoraproject.org/pub/epel/{config['rhel_version'].split('.')[0]}/Everything/x86_64/
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-{config['rhel_version'].split('.')[0]}
"""
            epel_repo.write_text(epel_content)
    
    def _generate_rhsm_config(self, system_path: Path, config: Dict):
        """Generate /etc/rhsm/rhsm.conf"""
        rhsm_conf = system_path / "etc" / "rhsm" / "rhsm.conf"
        rhsm_conf.parent.mkdir(parents=True, exist_ok=True)
        
        content = f"""[server]
hostname=subscription.rhsm.redhat.com
port=443
prefix=/subscription
proxy_hostname=proxy.company.com
proxy_port=8080

[rhsm]
baseurl=https://cdn.redhat.com
ca_cert_dir=/etc/rhsm/ca/
repo_ca_cert=/etc/rhsm/ca/redhat-uep.pem
productCertDir=/etc/pki/product
entitlementCertDir=/etc/pki/entitlement
consumerCertDir=/etc/pki/consumer
manage_repos=1
full_refresh_on_yum=1

[logging]
default_log_level=INFO
"""
        rhsm_conf.write_text(content)
    
    def _generate_rpm_database(self, system_path: Path, config: Dict):
        """Generate RPM database info"""
        rpm_dir = system_path / "var" / "lib" / "rpm"
        rpm_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate a realistic package list
        packages_file = rpm_dir / "packages.txt"
        package_list = []
        
        # Include system packages based on services
        for service in config['services']:
            if service in self.packages:
                package_list.append(f"{service}-{self.packages[service]}")
        
        # Add common system packages
        for pkg in ["kernel", "glibc", "openssl", "systemd", "openssh"]:
            if pkg in self.packages:
                package_list.append(f"{pkg}-{self.packages[pkg]}")
        
        # Add random additional packages
        additional_packages = [
            "bash-5.1.8-4.el9", "coreutils-8.32-31.el9", "grep-3.6-5.el9",
            "sed-4.8-9.el9", "gawk-5.1.0-6.el9", "tar-1.34-3.el9",
            "vim-enhanced-8.2.2637-16.el9", "wget-1.21.1-7.el9"
        ]
        package_list.extend(random.sample(additional_packages, 5))
        
        packages_file.write_text("\n".join(sorted(package_list)))
    
    def _generate_yum_logs(self, system_path: Path, config: Dict):
        """Generate /var/log/yum.log"""
        log_file = system_path / "var" / "log" / "yum.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        log_entries = []
        
        # Generate realistic patch events over the last 90 days
        for i in range(20):
            days_ago = random.randint(1, 90)
            timestamp = datetime.now() - timedelta(days=days_ago)
            
            # Pick a random patch
            patch = random.choice(self.patches)
            packages = patch['packages']
            
            # Success/failure based on system and patch type
            success_rate = 0.9 if config['environment'] == 'staging' else 0.85
            if patch['id'] == 'RHSA-2024-1234':  # Known problematic patch
                success_rate = 0.7
            
            success = random.random() < success_rate
            
            for package in packages:
                if package in self.packages:
                    if success:
                        log_entries.append(
                            f"{timestamp.strftime('%b %d %H:%M:%S')} Updated: {package}-{self.packages[package]}"
                        )
                    else:
                        log_entries.append(
                            f"{timestamp.strftime('%b %d %H:%M:%S')} Failed: {package}-{self.packages[package]} - Transaction failed"
                        )
        
        log_file.write_text("\n".join(sorted(log_entries, reverse=True)))
    
    def _generate_dnf_logs(self, system_path: Path, config: Dict):
        """Generate /var/log/dnf.log for RHEL 8+"""
        if config['rhel_version'].startswith('8') or config['rhel_version'].startswith('9'):
            log_file = system_path / "var" / "log" / "dnf.log"
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Similar to yum.log but with DNF format
            log_entries = []
            for i in range(15):
                days_ago = random.randint(1, 60)
                timestamp = datetime.now() - timedelta(days=days_ago)
                
                patch = random.choice(self.patches)
                log_entries.append(
                    f"{timestamp.isoformat()} INFO dnf: {patch['id']} transaction started"
                )
                log_entries.append(
                    f"{timestamp.isoformat()} INFO dnf: {len(patch['packages'])} packages to update"
                )
            
            log_file.write_text("\n".join(sorted(log_entries, reverse=True)))
    
    def _generate_system_logs(self, system_path: Path, config: Dict):
        """Generate /var/log/messages"""
        log_file = system_path / "var" / "log" / "messages"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        log_entries = []
        
        # Generate system events related to patching
        for i in range(30):
            days_ago = random.randint(1, 30)
            timestamp = datetime.now() - timedelta(days=days_ago)
            
            events = [
                f"{timestamp.strftime('%b %d %H:%M:%S')} {config.get('hostname', 'localhost')} systemd[1]: Started dnf automatic.",
                f"{timestamp.strftime('%b %d %H:%M:%S')} {config.get('hostname', 'localhost')} kernel: SELinux: policy loaded",
                f"{timestamp.strftime('%b %d %H:%M:%S')} {config.get('hostname', 'localhost')} systemd[1]: Reloading.",
                f"{timestamp.strftime('%b %d %H:%M:%S')} {config.get('hostname', 'localhost')} yum[12345]: Updated: httpd-2.4.53-11.el9_2.5.x86_64"
            ]
            log_entries.extend(random.sample(events, 2))
        
        log_file.write_text("\n".join(sorted(log_entries, reverse=True)))
    
    def _generate_audit_logs(self, system_path: Path, config: Dict):
        """Generate /var/log/audit/audit.log"""
        audit_dir = system_path / "var" / "log" / "audit"
        audit_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = audit_dir / "audit.log"
        
        # Generate SELinux and security events
        log_entries = []
        for i in range(50):
            timestamp = int((datetime.now() - timedelta(days=random.randint(1, 7))).timestamp())
            
            events = [
                f"type=SOFTWARE_UPDATE msg=audit({timestamp}.123:456): pid=1234 uid=0 auid=0 ses=1 subj=system_u:system_r:rpm_t:s0 msg='software update: package=httpd version=2.4.53-11.el9_2.5 result=success'",
                f"type=SYSCALL msg=audit({timestamp}.456:789): arch=c000003e syscall=2 success=yes exit=3 a0=7fff12345678 a1=0 a2=1b6 a3=0 items=1 ppid=1 pid=1234 auid=0 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=pts0 ses=1 comm=yum exe=/usr/bin/python3.9",
                f"type=SERVICE_START msg=audit({timestamp}.789:012): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=httpd comm=systemd exe=/usr/lib/systemd/systemd hostname=? addr=? terminal=? res=success'"
            ]
            log_entries.append(random.choice(events))
        
        log_file.write_text("\n".join(sorted(log_entries, reverse=True)))
    
    def _generate_yum_history(self, system_path: Path, config: Dict):
        """Generate /var/lib/yum/history/ transaction data"""
        history_dir = system_path / "var" / "lib" / "yum" / "history"
        history_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate history database simulation
        history_file = history_dir / "history.txt"
        
        history_entries = []
        for i in range(1, 21):
            days_ago = random.randint(1, 180)
            timestamp = datetime.now() - timedelta(days=days_ago)
            
            patch = random.choice(self.patches)
            action = "Update" if random.random() > 0.1 else "Install"
            
            history_entries.append(
                f"    {i:2d} | {action:12s} | {timestamp.strftime('%Y-%m-%d %H:%M')} | {len(patch['packages']):3d} |  {random.randint(10, 500):3d} k"
            )
        
        header = "ID | Command Line                 | Date and time    | Action(s) | Altered\n"
        header += "------------------------------------------------------------------------------------\n"
        
        history_file.write_text(header + "\n".join(history_entries))
    
    def _generate_systemd_services(self, system_path: Path, config: Dict):
        """Generate systemd service files"""
        systemd_dir = system_path / "usr" / "lib" / "systemd" / "system"
        systemd_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate service files for each service in the config
        for service in config['services']:
            service_file = systemd_dir / f"{service}.service"
            
            service_content = f"""[Unit]
Description={service.upper()} Service
After=network.target
Wants=network.target

[Service]
Type=forking
ExecStart=/usr/sbin/{service}
ExecReload=/bin/kill -HUP $MAINPID
PIDFile=/var/run/{service}.pid
Restart=always

[Install]
WantedBy=multi-user.target
"""
            service_file.write_text(service_content)
    
    def _generate_proc_files(self, system_path: Path, config: Dict):
        """Generate /proc filesystem simulation"""
        proc_dir = system_path / "proc"
        proc_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate kernel version
        version_file = proc_dir / "version"
        version_file.write_text(
            f"Linux version {config['kernel']} (mockbuild@x86-64-01.build.example.com) "
            f"(gcc (GCC) 11.3.1 20220421 (Red Hat 11.3.1-2)) #1 SMP PREEMPT Wed Aug 17 15:54:38 EDT 2023"
        )
        
        # Generate uptime with agent-searchable content
        uptime_file = proc_dir / "uptime"
        uptime_days = random.randint(1, 365)
        uptime_seconds = uptime_days * 24 * 3600 + random.randint(0, 86400)
        uptime_file.write_text(f"{uptime_seconds}.12 {uptime_seconds//2}.34")
        
        # Generate additional proc files for agents
        meminfo_file = proc_dir / "meminfo"
        total_mem = int(config.get('prop_memory_gb', '32')) * 1024 * 1024  # KB
        used_mem = total_mem * random.randint(60, 85) // 100
        meminfo_content = f"""MemTotal:    {total_mem} kB
MemFree:     {total_mem - used_mem} kB
MemAvailable: {total_mem - used_mem + random.randint(1000, 5000)} kB
Buffers:     {random.randint(100000, 500000)} kB
Cached:      {random.randint(1000000, 3000000)} kB"""
        meminfo_file.write_text(meminfo_content)
        
        # Generate command line
        cmdline_file = proc_dir / "cmdline"
        cmdline_file.write_text(
            f"BOOT_IMAGE=(hd0,gpt2)/vmlinuz-{config['kernel']} root=UUID=12345678-1234-1234-1234-123456789012 ro rhgb quiet"
        )
    
    def _generate_security_configs(self, system_path: Path, config: Dict):
        """Generate security and compliance configuration files"""
        security_dir = system_path / "etc" / "security"
        security_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate security limits
        limits_file = security_dir / "limits.conf"
        limits_content = """# /etc/security/limits.conf
#
# Security limits for RHEL systems
root soft nofile 65536
root hard nofile 65536
* soft nofile 4096
* hard nofile 8192

# Memory limits
* soft memlock unlimited
* hard memlock unlimited
"""
        limits_file.write_text(limits_content)
        
        # Generate OVAL directory (security compliance)
        oval_dir = system_path / "etc" / "oval"
        oval_dir.mkdir(parents=True, exist_ok=True)
        
        oval_file = oval_dir / "rhel_definitions.xml"
        oval_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<oval_definitions>
    <generator>
        <product_name>Red Hat OVAL Content</product_name>
        <product_version>{config['rhel_version']}</product_version>
    </generator>
    <definitions>
        <!-- CVE-2024-12345: httpd vulnerability -->
        <definition class="vulnerability" id="oval:com.redhat.rhsa:def:20241234">
            <title>RHSA-2024:1234: httpd security update (Important)</title>
            <affected family="unix">
                <platform>Red Hat Enterprise Linux {config['rhel_version']}</platform>
            </affected>
        </definition>
    </definitions>
</oval_definitions>
"""
        oval_file.write_text(oval_content)
    
    def _generate_agent_operational_logs(self, system_path: Path, config: Dict, system_id: str):
        """Generate operational logs with agent-searchable incident and troubleshooting context (NEW)"""
        log_dir = system_path / "var" / "log"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Application logs with troubleshooting context for vector search
        if "app-prod-01" in system_id:
            app_log = log_dir / "application.log"
            app_logs = [
                "2024-09-15 14:30:15 ERROR [CustomerPortal] OutOfMemoryError: Java heap space at com.company.portal.UserService.loadUserData",
                "2024-09-15 14:30:20 ERROR [CustomerPortal] Connection pool exhausted, unable to serve requests", 
                "2024-09-15 14:35:10 WARN [CustomerPortal] High GC activity detected, memory usage at 98%",
                "2024-09-15 16:45:30 INFO [CustomerPortal] Service restored after memory leak fix deployment",
                "2024-09-10 09:15:45 ERROR [DatabasePool] Connection timeout to db-prod-01:3306 after 30 seconds",
                "2024-09-10 09:20:12 ERROR [DatabasePool] All 50 connections in pool exhausted, queuing requests",
                "2024-09-10 10:30:00 INFO [DatabasePool] Connection pool size increased to 100, service restored"
            ]
            app_log.write_text("\n".join(app_logs))
        
        # Generate REAL RHEL security logs (authentic /var/log/secure)
        self._generate_authentic_rhel_security_logs(log_dir, config, system_id)
        
        # Generate authentic SELinux denials
        self._generate_selinux_denials(log_dir, config)
        
        # Generate httpd security events (where WAF logs would actually be)
        self._generate_httpd_security_logs(log_dir, config, system_id)
        
        # Remove any fake security.log that shouldn't exist on RHEL
        fake_security_log = log_dir / "security.log"
        if fake_security_log.exists():
            fake_security_log.unlink()
        
        # Performance logs for agent analysis
        performance_log = log_dir / "performance.log"
        perf_logs = [
            f"2024-09-25 10:00:00 INFO [Metrics] CPU usage: {random.randint(15, 85)}%, Memory: {random.randint(60, 90)}%, Disk I/O: {random.randint(10, 50)} MB/s",
            f"2024-09-25 11:00:00 INFO [Metrics] Response time average: {random.randint(150, 500)}ms, Active connections: {random.randint(100, 1000)}",
            f"2024-09-25 12:00:00 WARN [Metrics] High memory usage detected: {random.randint(85, 95)}% on {config.get('prop_hostname', system_id)}"
        ]
        performance_log.write_text("\n".join(perf_logs))

    def _generate_performance_metrics(self, system_path: Path, config: Dict):
        """Generate performance metrics for agent analysis (NEW)"""
        metrics_dir = system_path / "var" / "metrics"
        metrics_dir.mkdir(parents=True, exist_ok=True)
        
        # System metrics in JSON format for agent queries
        system_metrics = {
            "hostname": config.get('prop_hostname', 'unknown'),
            "environment": config['environment'],
            "cpu_usage_percent": random.randint(15, 85),
            "memory_used_gb": int(config.get('prop_memory_gb', '32')) * random.randint(60, 90) // 100,
            "memory_total_gb": int(config.get('prop_memory_gb', '32')),
            "disk_used_percent": random.randint(45, 75),
            "load_average_1min": round(random.uniform(0.5, 4.0), 2),
            "network_throughput_mbps": random.randint(100, 1000),
            "active_connections": random.randint(50, 500),
            "last_updated": datetime.now().isoformat()
        }
        
        (metrics_dir / "system_metrics.json").write_text(json.dumps(system_metrics, indent=2))

    def _generate_network_topology_files(self, system_path: Path, config: Dict):
        """Generate network configuration with topology awareness for agent queries (NEW)"""
        network_dir = system_path / "etc" / "sysconfig" / "network-scripts"
        network_dir.mkdir(parents=True, exist_ok=True)
        
        # Enhanced network interface config
        ifcfg_eth0 = network_dir / "ifcfg-eth0"
        ifcfg_content = f"""DEVICE=eth0
BOOTPROTO=static
IPADDR={config.get('prop_ip', '10.1.1.100')}
NETMASK=255.255.255.0
GATEWAY=10.{config.get('prop_ip', '10.1.1.100').split('.')[1]}.{config.get('prop_ip', '10.1.1.100').split('.')[2]}.1
DNS1=8.8.8.8
ONBOOT=yes
TYPE=Ethernet
# Network zone: {config.get('datacenter', 'Unknown')}
# Environment: {config['environment']}
# Business Service: {config.get('prop_business_service', 'Unknown')}
"""
        ifcfg_eth0.write_text(ifcfg_content)
        
        # Generate hosts file with all system relationships
        hosts_file = system_path / "etc" / "hosts"
        hosts_content = "127.0.0.1 localhost\n"
        
        # Add all systems for agent dependency queries
        for sys_id, sys_config in self.systems.items():
            if 'prop_ip' in sys_config:
                hosts_content += f"{sys_config['prop_ip']} {sys_config.get('prop_hostname', sys_id)}\n"
        
        hosts_file.write_text(hosts_content)

    def generate_agent_metadata(self):
        """Generate metadata files optimized for Graph RAG agents (NEW)"""
        metadata_dir = self.base_path / "_agent_metadata"
        metadata_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate all nodes for agent Neo4j queries
        all_nodes = []
        
        # Add server nodes with agent-compatible properties
        for system_id, config in self.systems.items():
            node = {
                "id": system_id,
                "labels": ["Server"],
                "properties": {k: v for k, v in config.items() if k.startswith('prop_') or k in ['environment', 'criticality', 'datacenter']},
                "description": f"{config['environment']} server {system_id} in {config['datacenter']} running {config.get('prop_business_service', 'system services')}"
            }
            all_nodes.append(node)
        
        # Add infrastructure nodes (incidents, security events, applications)
        for category, items in self.agent_infrastructure.items():
            for item_id, properties in items.items():
                node = {
                    "id": item_id,
                    "labels": [category.rstrip('s').title().replace('_', '')],  # incidents -> Incident
                    "properties": properties,
                    "description": properties.get('description', f"{category} {item_id}")
                }
                all_nodes.append(node)
        
        # Save agent-compatible data
        (metadata_dir / "nodes.json").write_text(json.dumps(all_nodes, indent=2))
        (metadata_dir / "relationships.json").write_text(json.dumps(self.agent_relationships, indent=2))
        
        # Generate agent query examples for testing
        query_examples = {
            "cypher_queries": [
                "MATCH (s:Server) WHERE s.environment = 'production' RETURN s.prop_hostname, s.prop_business_service",
                "MATCH (s:Server) WHERE s.criticality = 'critical' RETURN COUNT(s) as critical_servers",
                "MATCH (s1:Server)-[:DEPENDS_ON]->(s2:Server) RETURN s1.prop_hostname, s2.prop_hostname",
                "MATCH (i:Incident)-[:AFFECTED]->(s:Server) WHERE i.prop_severity = 'P1_Critical' RETURN i, s"
            ],
            "vector_search_examples": [
                "MySQL performance issues and database connectivity problems",
                "Memory leak causing application outages in production environment", 
                "SQL injection attacks and security incidents targeting web servers",
                "Java application server configuration and Tomcat optimization",
                "Network connectivity issues between web and application tiers",
                "Database connection pool exhaustion and timeout errors"
            ]
        }
        
        (metadata_dir / "agent_query_examples.json").write_text(json.dumps(query_examples, indent=2))
        
        print(f"🤖 Generated {len(all_nodes)} nodes and {len(self.agent_relationships)} relationships for Graph RAG agents")
        print(f"📊 Node types: Server, Incident, SecurityEvent, Application")

    def _generate_authentic_rhel_security_logs(self, log_dir: Path, config: Dict, system_id: str):
        """Generate authentic RHEL /var/log/secure with real authentication events (NEW)"""
        # THIS IS THE REAL RHEL AUTHENTICATION LOG FILE
        secure_log = log_dir / "secure"
        
        # Generate realistic authentication events from real RHEL systems
        auth_events = []
        for i in range(20):
            days_ago = random.randint(1, 30)
            timestamp = datetime.now() - timedelta(days=days_ago)
            hostname = config.get('prop_hostname', system_id)
            
            # Real RHEL authentication log formats
            events = [
                f"{timestamp.strftime('%b %d %H:%M:%S')} {hostname} sshd[{random.randint(1000, 9999)}]: Accepted publickey for root from 10.1.1.100 port {random.randint(40000, 60000)} ssh2: RSA SHA256:abc123def456",
                f"{timestamp.strftime('%b %d %H:%M:%S')} {hostname} sshd[{random.randint(1000, 9999)}]: Failed password for invalid user admin from 203.0.113.45 port {random.randint(40000, 60000)} ssh2",
                f"{timestamp.strftime('%b %d %H:%M:%S')} {hostname} sudo: root : TTY=pts/0 ; PWD=/root ; USER=root ; COMMAND=/bin/systemctl restart httpd",
                f"{timestamp.strftime('%b %d %H:%M:%S')} {hostname} sshd[{random.randint(1000, 9999)}]: pam_unix(sshd:session): session opened for user root by (uid=0)",
                f"{timestamp.strftime('%b %d %H:%M:%S')} {hostname} sshd[{random.randint(1000, 9999)}]: pam_unix(sshd:session): session closed for user root",
                f"{timestamp.strftime('%b %d %H:%M:%S')} {hostname} su: pam_unix(su-l:session): session opened for user apache by root(uid=0)",
                f"{timestamp.strftime('%b %d %H:%M:%S')} {hostname} systemd-logind[{random.randint(500, 999)}]: New session {random.randint(1, 100)} of user root.",
                f"{timestamp.strftime('%b %d %H:%M:%S')} {hostname} sshd[{random.randint(1000, 9999)}]: Invalid user oracle from 192.168.1.100 port {random.randint(40000, 60000)}"
            ]
            auth_events.append(random.choice(events))
        
        secure_log.write_text("\n".join(sorted(auth_events, reverse=True)))

    def _generate_selinux_denials(self, log_dir: Path, config: Dict):
        """Generate authentic SELinux denial logs in /var/log/messages (NEW)"""
        messages_file = log_dir / "messages"
        
        # Add realistic SELinux denials to existing messages
        if messages_file.exists():
            existing_content = messages_file.read_text()
        else:
            existing_content = ""
        
        selinux_denials = []
        for i in range(5):
            days_ago = random.randint(1, 15)
            timestamp = datetime.now() - timedelta(days=days_ago)
            hostname = config.get('prop_hostname', 'localhost')
            
            # Real SELinux denial formats from RHEL systems
            denials = [
                f"{timestamp.strftime('%b %d %H:%M:%S')} {hostname} kernel: audit: type=1400 audit(1693996800.123:456): avc: denied {{ read }} for pid={random.randint(1000, 9999)} comm=\"httpd\" name=\"index.html\" dev=\"dm-0\" ino={random.randint(100000, 999999)} scontext=system_u:system_r:httpd_t:s0 tcontext=unconfined_u:object_r:admin_home_t:s0 tclass=file permissive=0",
                f"{timestamp.strftime('%b %d %H:%M:%S')} {hostname} setroubleshoot: SELinux is preventing httpd from read access on the file index.html. For complete SELinux messages run: sealert -l {random.choice(['abc12345-def6-789a-bcde-f0123456789a', 'xyz98765-abc4-321z-yzab-c0987654321z'])}",
                f"{timestamp.strftime('%b %d %H:%M:%S')} {hostname} kernel: audit: type=1400 audit(1693996801.456:457): avc: denied {{ name_connect }} for pid={random.randint(1000, 9999)} comm=\"mysqld\" dest=3306 scontext=system_u:system_r:mysqld_t:s0 tcontext=system_u:object_r:mysqld_port_t:s0 tclass=tcp_socket permissive=0"
            ]
            selinux_denials.append(random.choice(denials))
        
        updated_content = existing_content + "\n" + "\n".join(selinux_denials)
        messages_file.write_text(updated_content)

    def _generate_httpd_security_logs(self, log_dir: Path, config: Dict, system_id: str):
        """Generate authentic Apache httpd security logs (where WAF events actually go) (NEW)"""
        if any(service in config.get('services', []) for service in ['httpd', 'nginx']):
            httpd_dir = log_dir / "httpd"
            httpd_dir.mkdir(parents=True, exist_ok=True)
            
            # Real Apache error log with security events
            error_log = httpd_dir / "error_log"
            security_events = []
            
            for i in range(10):
                days_ago = random.randint(1, 30)
                timestamp = datetime.now() - timedelta(days=days_ago)
                
                # Real Apache security log formats
                events = [
                    f"[{timestamp.strftime('%a %b %d %H:%M:%S.%f %Y')}] [security2:error] [pid {random.randint(1000, 9999)}] [client 192.168.100.250:54321] ModSecurity: Warning. Pattern match \"(?i:union.+select)\" at ARGS:search. [file \"/etc/httpd/modsecurity.d/activated_rules/modsecurity_crs_41_sql_injection_attacks.conf\"] [line \"37\"] [id \"981231\"] [msg \"SQL Injection Attack Detected via libinjection\"] [data \"union select\"] [severity \"CRITICAL\"] [hostname \"web-prod-01.company.com\"] [uri \"/api/users\"] [unique_id \"abc123def456\"]",
                    f"[{timestamp.strftime('%a %b %d %H:%M:%S.%f %Y')}] [core:error] [pid {random.randint(1000, 9999)}] [client 203.0.113.45:43210] AH00124: Request exceeded the limit of 10 internal redirects due to probable configuration error. Use 'LimitInternalRecursion' to increase the limit if necessary.",
                    f"[{timestamp.strftime('%a %b %d %H:%M:%S.%f %Y')}] [authz_core:error] [pid {random.randint(1000, 9999)}] [client 203.0.113.45:43211] AH01630: client denied by server configuration: /var/www/html/admin/",
                    f"[{timestamp.strftime('%a %b %d %H:%M:%S.%f %Y')}] [ssl:warn] [pid {random.randint(1000, 9999)}] AH01909: RSA certificate configured for www.company.com:443 does NOT include an ID which matches the server name"
                ]
                security_events.append(random.choice(events))
            
            error_log.write_text("\n".join(sorted(security_events, reverse=True)))

    def _generate_authentic_compliance_data(self, system_path: Path, config: Dict):
        """Generate authentic RHEL compliance and security configuration files (NEW)"""
        
        # Generate authentic PAM configuration
        pam_dir = system_path / "etc" / "pam.d"
        pam_dir.mkdir(parents=True, exist_ok=True)
        
        # Real PAM sshd configuration
        pam_sshd = pam_dir / "sshd"
        pam_sshd_content = """#%PAM-1.0
auth       required     pam_sepermit.so
auth       substack     password-auth
auth       include      postlogin
# Used with polkit to reauthorize users in remote sessions
-auth      optional     pam_reauthorize.so prepare
account    required     pam_nologin.so
account    include      password-auth
password   include      password-auth
# pam_selinux.so close should be the first session rule
session    required     pam_selinux.so close
session    required     pam_loginuid.so
# pam_selinux.so open should only be followed by sessions to be executed in the user context
session    required     pam_selinux.so open env_params
session    required     pam_namespace.so
session    optional     pam_keyinit.so force revoke
session    include      password-auth
session    include      postlogin
# Used with polkit to reauthorize users in remote sessions
-session   optional     pam_reauthorize.so prepare"""
        pam_sshd.write_text(pam_sshd_content)
        
        # Generate real CIS benchmark results (in admin's home where they'd actually be)
        admin_home = system_path / "root"
        admin_home.mkdir(parents=True, exist_ok=True)
        
        cis_results = admin_home / "cis-scan-report-$(date +%Y%m%d).html"
        # Generate authentic CIS HTML report (how CIS-CAT actually outputs)
        cis_html = f"""<!DOCTYPE html>
<html>
<head><title>CIS-CAT Pro Assessment Report</title></head>
<body>
<h1>CIS Red Hat Enterprise Linux 9 Benchmark v1.0.0</h1>
<h2>Assessment Results for {config.get('prop_hostname', 'localhost')}</h2>
<p>Assessment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<p>Overall Score: {random.randint(75, 95)}%</p>

<h3>Rule Results</h3>
<table border="1">
<tr><th>Rule</th><th>Title</th><th>Result</th></tr>
<tr><td>1.1.1.1</td><td>Ensure mounting of cramfs filesystems is disabled</td><td>Pass</td></tr>
<tr><td>1.4.1</td><td>Ensure permissions on bootloader config are configured</td><td>Pass</td></tr>
<tr><td>5.2.1</td><td>Ensure permissions on /etc/ssh/sshd_config are configured</td><td>Fail</td></tr>
<tr><td>5.2.4</td><td>Ensure SSH Protocol is set to 2</td><td>Pass</td></tr>
</table>

<p>Generated by CIS-CAT Pro Assessor v4.0</p>
</body>
</html>"""
        cis_results.write_text(cis_html)
        
        # Generate STIG findings (in realistic location - admin's home)
        stig_results = admin_home / "STIG_RHEL9_Checklist.ckl"
        # Real STIG Viewer checklist format (XML-based .ckl format)
        stig_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<CHECKLIST>
    <ASSET>
        <ROLE>None</ROLE>
        <ASSET_TYPE>Computing</ASSET_TYPE>
        <HOST_NAME>{config.get('prop_hostname', 'localhost')}</HOST_NAME>
        <HOST_IP>{config.get('prop_ip', '10.1.1.100')}</HOST_IP>
        <HOST_MAC></HOST_MAC>
        <HOST_GUID></HOST_GUID>
        <HOST_FQDN>{config.get('prop_hostname', 'localhost')}</HOST_FQDN>
        <TECH_AREA></TECH_AREA>
        <TARGET_KEY>2777</TARGET_KEY>
        <WEB_OR_DATABASE>false</WEB_OR_DATABASE>
        <WEB_DB_SITE></WEB_DB_SITE>
        <WEB_DB_INSTANCE></WEB_DB_INSTANCE>
    </ASSET>
    <STIGS>
        <iSTIG>
            <STIG_INFO>
                <SI_DATA>
                    <SID_NAME>title</SID_NAME>
                    <SID_DATA>Red Hat Enterprise Linux 9 Security Technical Implementation Guide</SID_DATA>
                </SI_DATA>
                <SI_DATA>
                    <SID_NAME>version</SID_NAME>
                    <SID_DATA>1</SID_DATA>
                </SI_DATA>
                <SI_DATA>
                    <SID_NAME>releaseinfo</SID_NAME>
                    <SID_DATA>Release: 1 Benchmark Date: 23 Jan 2024</SID_DATA>
                </SI_DATA>
            </STIG_INFO>
            <VULN>
                <STIG_DATA>
                    <VULN_ATTRIBUTE>Vuln_Num</VULN_ATTRIBUTE>
                    <ATTRIBUTE_DATA>V-258000</ATTRIBUTE_DATA>
                </STIG_DATA>
                <STIG_DATA>
                    <VULN_ATTRIBUTE>Severity</VULN_ATTRIBUTE>
                    <ATTRIBUTE_DATA>medium</ATTRIBUTE_DATA>
                </STIG_DATA>
                <STIG_DATA>
                    <VULN_ATTRIBUTE>Rule_Title</VULN_ATTRIBUTE>
                    <ATTRIBUTE_DATA>RHEL-09-211010: The operating system must implement DoD-approved encryption</ATTRIBUTE_DATA>
                </STIG_DATA>
                <STATUS>Open</STATUS>
                <FINDING_DETAILS>System does not implement FIPS 140-2 encryption modules</FINDING_DETAILS>
                <COMMENTS></COMMENTS>
                <SEVERITY_OVERRIDE></SEVERITY_OVERRIDE>
                <SEVERITY_JUSTIFICATION></SEVERITY_JUSTIFICATION>
            </VULN>
        </iSTIG>
    </STIGS>
</CHECKLIST>"""
        stig_results.write_text(stig_content)
        
        # Generate authentic sudoers configuration
        sudoers_dir = system_path / "etc" / "sudoers.d"
        sudoers_dir.mkdir(parents=True, exist_ok=True)
        
        sudoers_app = sudoers_dir / "application_users"
        sudoers_content = """# Application service accounts
apache ALL=(ALL) NOPASSWD: /bin/systemctl restart httpd, /bin/systemctl reload httpd
mysql ALL=(ALL) NOPASSWD: /bin/systemctl restart mysql, /bin/systemctl stop mysql
# Emergency access for platform team
%platform_engineering ALL=(ALL) ALL
# Monitoring user
monitoring ALL=(ALL) NOPASSWD: /bin/ps, /bin/netstat, /bin/ss, /usr/bin/top
"""
        sudoers_app.write_text(sudoers_content)

    def _generate_security_agent_data(self, system_path: Path, config: Dict, system_id: str):
        """Generate security data in REAL RHEL locations (FIXED for authenticity)"""
        # Use real Red Hat Insights directory structure
        insights_dir = system_path / "var" / "lib" / "insights"
        insights_dir.mkdir(parents=True, exist_ok=True)
        
        # Real Red Hat Insights data (AUTHENTIC file structure)
        client_results_dir = insights_dir / "client-results"
        client_results_dir.mkdir(parents=True, exist_ok=True)
        
        # Real Insights data file (authentic name format)
        vuln_scan = client_results_dir / "insights-archive-2024-09-07.tar.gz.json"
        vulnerabilities = {
            "scan_date": datetime.now().isoformat(),
            "scanner": "Red Hat Insights Security",
            "target": config.get('prop_hostname', system_id),
            "vulnerabilities": [
                {
                    "cve_id": "CVE-2024-3094",
                    "severity": "CRITICAL",
                    "cvss_score": 9.8,
                    "package": "xz-utils-5.2.5-4.el9",
                    "description": "Backdoor in xz compression library",
                    "remediation": "Update to xz-utils-5.2.6-1.el9_4",
                    "risk_level": "HIGH",
                    "exploitable": True,
                    "patch_available": True
                },
                {
                    "cve_id": "CVE-2024-1086", 
                    "severity": "HIGH",
                    "cvss_score": 7.8,
                    "package": "kernel-5.14.0-284.25.1.el9_2",
                    "description": "Use-after-free vulnerability in netfilter",
                    "remediation": "Update to kernel-5.14.0-362.8.1.el9_3",
                    "risk_level": "MEDIUM",
                    "exploitable": False,
                    "patch_available": True
                },
                {
                    "cve_id": "CVE-2024-0727",
                    "severity": "MEDIUM", 
                    "cvss_score": 5.5,
                    "package": "openssl-3.0.7-16.el9_2",
                    "description": "Denial of service in OpenSSL certificate verification",
                    "remediation": "Update to openssl-3.0.7-25.el9_3",
                    "risk_level": "LOW",
                    "exploitable": False,
                    "patch_available": True
                }
            ],
            "summary": {
                "total_vulnerabilities": 3,
                "critical": 1,
                "high": 1, 
                "medium": 1,
                "low": 0,
                "patched": 0,
                "unpatched": 3
            }
        }
        vuln_scan.write_text(json.dumps(vulnerabilities, indent=2))
        
        # Real firewalld status (authentic RHEL location)  
        firewalld_dir = system_path / "etc" / "firewalld"
        firewalld_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate authentic firewalld zone configuration
        public_zone = firewalld_dir / "zones" / "public.xml"
        public_zone.parent.mkdir(parents=True, exist_ok=True)
        zone_content = """<?xml version="1.0" encoding="utf-8"?>
<zone>
  <short>Public</short>
  <description>For use in public areas</description>
  <service name="ssh"/>
  <service name="http"/>
  <service name="https"/>
  <port port="8080" protocol="tcp"/>
  <rule family="ipv4">
    <source address="192.168.100.0/24"/>
    <drop/>
  </rule>
</zone>"""
        public_zone.write_text(zone_content)
        
        # Network scan results - put in admin's home directory (realistic location)
        admin_home = system_path / "root"
        admin_home.mkdir(parents=True, exist_ok=True)
        network_scan = admin_home / "nmap_scan_$(date +%Y%m%d).log"
        network_data = {
            "scan_date": datetime.now().isoformat(),
            "target": config.get('prop_ip', '10.1.1.100'),
            "hostname": config.get('prop_hostname', system_id),
            "open_ports": [
                {"port": 22, "service": "ssh", "version": "OpenSSH 8.7", "risk": "LOW", "justified": True},
                {"port": 80, "service": "http", "version": "Apache 2.4.53", "risk": "LOW", "justified": True},
                {"port": 443, "service": "https", "version": "Apache 2.4.53", "risk": "LOW", "justified": True}
            ],
            "closed_ports": [21, 23, 25, 53, 110, 143, 993, 995],
            "filtered_ports": [135, 139, 445],
            "firewall_status": "active",
            "security_findings": [
                {
                    "finding_id": "SEC-001",
                    "title": "SSH root login enabled",
                    "risk_level": "MEDIUM", 
                    "description": "Direct root SSH access increases attack surface",
                    "remediation": "Disable PermitRootLogin in /etc/ssh/sshd_config",
                    "requires_approval": True
                },
                {
                    "finding_id": "SEC-002", 
                    "title": "Weak SSL cipher suites enabled",
                    "risk_level": "LOW",
                    "description": "Legacy cipher suites detected in Apache configuration",
                    "remediation": "Update SSLCipherSuite directive",
                    "requires_approval": False
                }
            ]
        }
        # Generate authentic nmap-style output instead of JSON
        nmap_output = f"""Starting Nmap scan on {config.get('prop_hostname', system_id)} ({config.get('prop_ip', '10.1.1.100')})
Nmap scan report for {config.get('prop_hostname', system_id)} ({config.get('prop_ip', '10.1.1.100')})
Host is up (0.0012s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.7 (protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.53 ((Red Hat Enterprise Linux))
443/tcp  open  https   Apache httpd 2.4.53 ((Red Hat Enterprise Linux))
3306/tcp closed mysql

Nmap done: 1 IP address (1 host up) scanned in 2.45 seconds"""
        network_scan.write_text(nmap_output)
        
        # Real user and group files (authentic RHEL location)
        passwd_file = system_path / "etc" / "passwd"
        passwd_file.parent.mkdir(parents=True, exist_ok=True)
        # Generate authentic /etc/passwd content
        passwd_content = """root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
operator:x:11:0:operator:/root:/sbin/nologin
games:x:12:100:games:/usr/games:/sbin/nologin
ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin
nobody:x:65534:65534:Kernel Overflow User:/:/sbin/nologin
dbus:x:81:81:System message bus:/:/sbin/nologin
systemd-coredump:x:999:997:systemd Core Dumper:/:/sbin/nologin
systemd-resolve:x:193:193:systemd Resolver:/:/sbin/nologin
tss:x:59:59:Account used for TPM access:/dev/null:/sbin/nologin
polkitd:x:998:996:User for polkitd:/:/sbin/nologin
libstoragemgmt:x:997:995:daemon account for libstoragemgmt:/var/run/lsm:/sbin/nologin
cockpit-ws:x:996:994:User for cockpit web service:/nonexisting:/sbin/nologin
cockpit-wsinstance:x:995:993:User for cockpit-ws instances:/nonexisting:/sbin/nologin
sssd:x:994:992:User for sssd:/:/sbin/nologin
sshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologin
chrony:x:993:991::/var/lib/chrony:/sbin/nologin
apache:x:48:48:Apache:/usr/share/httpd:/sbin/nologin
mysql:x:27:27:MySQL Server:/var/lib/mysql:/sbin/nologin
monitoring:x:1001:1001:Monitoring User:/home/monitoring:/bin/bash"""
        passwd_file.write_text(passwd_content)

    def _generate_performance_agent_data(self, system_path: Path, config: Dict):
        """Generate performance data in REAL RHEL locations (FIXED for authenticity)"""
        # Use real SAR data location
        sar_dir = system_path / "var" / "log" / "sa"
        sar_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate authentic SAR data file (real RHEL performance tool)
        today = datetime.now().strftime('%d')
        sar_file = sar_dir / f"sa{today}"
        
        # Also generate readable sar report
        perf_history = sar_dir / f"sar{today}.txt"
        # Generate authentic SAR output format (real RHEL performance data)
        sar_output = f"""Linux {config.get('prop_hostname', 'localhost')} ({config['kernel']}) \t{datetime.now().strftime('%m/%d/%Y')} \t_x86_64_\t({config.get('prop_cpu_cores', '8')} CPU)

12:00:01 AM     CPU     %user     %nice   %system   %iowait    %steal     %idle
12:10:01 AM     all      {random.randint(10, 30)}.{random.randint(10, 99)}      0.00      {random.randint(5, 15)}.{random.randint(10, 99)}      {random.randint(1, 5)}.{random.randint(10, 99)}      0.00     {random.randint(60, 80)}.{random.randint(10, 99)}
12:20:01 AM     all      {random.randint(15, 35)}.{random.randint(10, 99)}      0.00      {random.randint(8, 18)}.{random.randint(10, 99)}      {random.randint(2, 6)}.{random.randint(10, 99)}      0.00     {random.randint(55, 75)}.{random.randint(10, 99)}
12:30:01 AM     all      {random.randint(20, 40)}.{random.randint(10, 99)}      0.00     {random.randint(10, 20)}.{random.randint(10, 99)}      {random.randint(1, 4)}.{random.randint(10, 99)}      0.00     {random.randint(50, 70)}.{random.randint(10, 99)}

Average:        all      {random.randint(18, 32)}.{random.randint(10, 99)}      0.00     {random.randint(8, 16)}.{random.randint(10, 99)}      {random.randint(1, 5)}.{random.randint(10, 99)}      0.00     {random.randint(55, 75)}.{random.randint(10, 99)}

12:00:01 AM kbmemfree kbmemused  %memused kbbuffers  kbcached  kbcommit   %commit  kbactive   kbinact   kbdirty
12:10:01 AM   {random.randint(5000000, 8000000)}  {random.randint(25000000, 30000000)}     {random.randint(70, 85)}.{random.randint(10, 99)}    {random.randint(200000, 400000)}  {random.randint(8000000, 12000000)}  {random.randint(15000000, 20000000)}     {random.randint(45, 65)}.{random.randint(10, 99)} {random.randint(12000000, 16000000)}  {random.randint(4000000, 6000000)}      {random.randint(100, 500)}
12:20:01 AM   {random.randint(4500000, 7500000)}  {random.randint(26000000, 31000000)}     {random.randint(72, 87)}.{random.randint(10, 99)}    {random.randint(250000, 450000)}  {random.randint(8500000, 12500000)}  {random.randint(16000000, 21000000)}     {random.randint(48, 68)}.{random.randint(10, 99)} {random.randint(13000000, 17000000)}  {random.randint(4200000, 6200000)}      {random.randint(150, 600)}

Average:      {random.randint(5000000, 7000000)}  {random.randint(25000000, 29000000)}     {random.randint(72, 85)}.{random.randint(10, 99)}    {random.randint(220000, 420000)}  {random.randint(8200000, 12200000)}  {random.randint(15500000, 20500000)}     {random.randint(47, 67)}.{random.randint(10, 99)} {random.randint(12500000, 16500000)}  {random.randint(4100000, 6100000)}      {random.randint(125, 550)}"""
        
        perf_history.write_text(sar_output)
        
        # Generate /proc/loadavg (real RHEL location)
        proc_dir = system_path / "proc"
        proc_dir.mkdir(parents=True, exist_ok=True)
        loadavg_file = proc_dir / "loadavg"
        loadavg_content = f"{random.uniform(0.5, 4.0):.2f} {random.uniform(0.8, 3.5):.2f} {random.uniform(1.0, 3.0):.2f} {random.randint(1, 5)}/{random.randint(150, 300)} {random.randint(1000, 9999)}"
        loadavg_file.write_text(loadavg_content)

    def _generate_compliance_agent_data(self, system_path: Path, config: Dict):
        """Generate compliance data in REAL RHEL locations (FIXED for authenticity)"""
        # Use real OpenSCAP directory structure
        openscap_dir = system_path / "var" / "lib" / "openscap"
        openscap_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate authentic OpenSCAP result file (real RHEL compliance tool)
        compliance_report = openscap_dir / "ssg-rhel9-xccdf-result.xml"
        # Generate authentic OpenSCAP XML format instead of JSON
        openscap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<TestResult xmlns="http://checklists.nist.gov/xccdf/1.2" id="xccdf_org.ssgproject.content_testresult_default-profile" start-time="{datetime.now().isoformat()}" end-time="{datetime.now().isoformat()}" test-system="{config.get('prop_hostname', 'localhost')}" version="0.1.66">
  <benchmark href="/usr/share/xml/scap/ssg/content/ssg-rhel9-xccdf.xml" id="xccdf_org.ssgproject.content_benchmark_RHEL-9"/>
  <title>OSCAP Scan Result</title>
  <identity authenticated="true" privileged="true">root</identity>
  <profile idref="xccdf_org.ssgproject.content_profile_cis"/>
  <target>{config.get('prop_hostname', 'localhost')}</target>
  <target-address>{config.get('prop_ip', '10.1.1.100')}</target-address>
  
  <rule-result idref="xccdf_org.ssgproject.content_rule_accounts_password_minlen_login_defs" severity="medium" time="{datetime.now().isoformat()}">
    <result>pass</result>
  </rule-result>
  
  <rule-result idref="xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny" severity="medium" time="{datetime.now().isoformat()}">
    <result>fail</result>
    <message>Account lockout policy not configured</message>
  </rule-result>
  
  <rule-result idref="xccdf_org.ssgproject.content_rule_service_sshd_enabled" severity="high" time="{datetime.now().isoformat()}">
    <result>pass</result>
  </rule-result>
  
  <score system="urn:xccdf:scoring:absolute" maximum="100">{random.randint(75, 95)}</score>
</TestResult>"""
        compliance_report.write_text(openscap_xml)

    def _generate_approval_gate_data(self, system_path: Path, config: Dict):
        """Generate risk data in REAL RHEL locations (FIXED for authenticity)"""
        # Use real Red Hat Insights directory for findings
        insights_dir = system_path / "var" / "lib" / "insights"
        insights_dir.mkdir(parents=True, exist_ok=True)
        
        client_results_dir = insights_dir / "client-results"
        client_results_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate Red Hat Insights findings (real RHEL location)
        approval_queue = client_results_dir / "advisor-recommendations.json"
        approval_data = {
            "system": config.get('prop_hostname', 'unknown'),
            "last_updated": datetime.now().isoformat(),
            "pending_approvals": [
                {
                    "finding_id": "SEC-HIGH-001",
                    "finding": "Critical vulnerability CVE-2024-3094 detected in xz-utils package",
                    "risk_level": "CRITICAL",
                    "impact_analysis": {
                        "confidentiality": "HIGH",
                        "integrity": "HIGH", 
                        "availability": "HIGH",
                        "business_impact": "Service disruption possible",
                        "affected_users": "All system users",
                        "financial_impact": "$50,000 potential loss"
                    },
                    "recommended_action": "Immediate patching required",
                    "urgency": "24_hours",
                    "approver_required": "CISO",
                    "analysis_depth": "detailed_investigation"
                },
                {
                    "finding_id": "SEC-MED-002",
                    "finding": "SSH root login enabled on production system",
                    "risk_level": "MEDIUM",
                    "impact_analysis": {
                        "confidentiality": "MEDIUM",
                        "integrity": "MEDIUM",
                        "availability": "LOW",
                        "business_impact": "Increased attack surface",
                        "affected_users": "Administrative users",
                        "financial_impact": "$10,000 potential loss"
                    },
                    "recommended_action": "Disable root SSH and implement key-based access",
                    "urgency": "7_days",
                    "approver_required": "Security_Team",
                    "analysis_depth": "standard_review"
                },
                {
                    "finding_id": "SEC-LOW-003",
                    "finding": "Legacy SSL cipher suites detected in web server configuration",
                    "risk_level": "LOW",
                    "impact_analysis": {
                        "confidentiality": "LOW",
                        "integrity": "LOW",
                        "availability": "NONE",
                        "business_impact": "Minimal security exposure",
                        "affected_users": "Web application users",
                        "financial_impact": "$1,000 potential loss"
                    },
                    "recommended_action": "Update SSL configuration to modern cipher suites",
                    "urgency": "30_days",
                    "approver_required": "Platform_Team",
                    "analysis_depth": "basic_review"
                }
            ],
            "approval_workflow": {
                "CRITICAL": {"approver": "CISO", "timeline": "4_hours", "escalation": "CEO"},
                "HIGH": {"approver": "Security_Manager", "timeline": "24_hours", "escalation": "CISO"},
                "MEDIUM": {"approver": "Security_Team", "timeline": "7_days", "escalation": "Security_Manager"},
                "LOW": {"approver": "Platform_Team", "timeline": "30_days", "escalation": "Security_Team"}
            }
        }
        approval_queue.write_text(json.dumps(approval_data, indent=2))

    def _cleanup_fake_directories(self, system_path: Path):
        """Remove fake directories that don't exist on real RHEL systems (AUTHENTICITY FIX)"""
        fake_dirs = [
            system_path / "var" / "security",      #  Not real RHEL
            system_path / "var" / "performance",   #  Not real RHEL
            system_path / "var" / "approvals",     #  Not real RHEL
            system_path / "var" / "metrics",       #  Not real RHEL
            system_path / "var" / "compliance",    #  Not real RHEL 
            system_path / "var" / "log" / "compliance",  #  Not real RHEL
            system_path / "var" / "log" / "security"     #  Not real RHEL
        ]
        
        import shutil
        for fake_dir in fake_dirs:
            if fake_dir.exists():
                shutil.rmtree(fake_dir)
                print(f"   🧹 Removed fake directory: {fake_dir.name}")

    def _cleanup_fake_files(self, system_path: Path):
        """Remove fake files that don't exist on real RHEL systems (AUTHENTICITY FIX)"""
        fake_files = [
            system_path / "var" / "lib" / "insights" / "insights_findings.json",  #  Not real filename
            system_path / "var" / "lib" / "insights" / "vulnerabilities.json",   #  Not real filename
            system_path / "var" / "log" / "performance.log",                     #  Not real RHEL log
        ]
        
        for fake_file in fake_files:
            if fake_file.exists():
                fake_file.unlink()
                print(f"   🧹 Removed fake file: {fake_file.name}")

if __name__ == "__main__":
    import sys
    
    # Support command line argument for number of systems
    num_systems = 5  # Default
    if len(sys.argv) > 1:
        try:
            num_systems = int(sys.argv[1])
            if num_systems < 1 or num_systems > 10000:
                print(" Number of systems must be between 1 and 10,000")
                sys.exit(1)
        except ValueError:
            print(" Invalid number of systems. Usage: python rhel_filesystem_generator.py [num_systems]")
            sys.exit(1)
    
    print(f"🚀 Creating {num_systems} enterprise RHEL systems...")
    
    generator = RHELFilesystemGenerator(num_systems=num_systems)
    generator.generate_all_systems()
    
    print(f"\n🎯 {len(generator.systems)} RHEL systems ready for Graph RAG agents!")
    print("   📁 Traditional RHEL files: Maintained compatibility")  
    print("   🤖 Agent metadata: /simulated_rhel_systems/_agent_metadata/")
    print("   🔍 Ready for neo4j_query_tool and vector_search_tool")
    print("   📊 Supports Cypher queries and semantic vector search")
    
    # Show enterprise statistics
    envs = {}
    types = {}
    for system_id, config in generator.systems.items():
        env = config['environment']
        sys_type = system_id.split('-')[0]
        envs[env] = envs.get(env, 0) + 1
        types[sys_type] = types.get(sys_type, 0) + 1
    
    print(f"\n📊 Enterprise Distribution:")
    print(f"   Environments: {dict(sorted(envs.items()))}")
    print(f"   System Types: {dict(sorted(types.items()))}")
    print(f"   💾 Estimated Storage: ~{len(generator.systems) * 0.05:.1f} MB")
