#!/usr/bin/env python3
"""
Demo Data Generator - Creates realistic RHEL patch data for demonstration
Generates comprehensive fake data that looks like real enterprise RHEL environment
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class DemoRHELSystem:
    """Demo RHEL system with realistic properties"""
    system_id: str
    hostname: str
    ip_address: str
    rhel_version: str
    kernel_version: str
    environment: str
    datacenter: str
    services: List[str]
    installed_packages: Dict[str, str]
    cpu_cores: int
    memory_gb: int
    disk_gb: int
    last_reboot: str
    uptime_days: int

@dataclass
class DemoPatchEvent:
    """Demo patch event with realistic details"""
    patch_id: str
    system_id: str
    timestamp: str
    success: bool
    packages_updated: List[str]
    services_affected: List[str]
    downtime_minutes: int
    error_message: str = None
    resolution_steps: List[str] = None
    applied_by: str = "automation"
    pre_patch_backup: bool = True

class DemoDataGenerator:
    """Generates realistic demo data for RHEL patch intelligence"""
    
    def __init__(self):
        # Realistic base data
        self.rhel_versions = ["8.6", "8.8", "9.1", "9.2", "9.3"]
        self.environments = ["production", "staging", "development", "testing"]
        self.datacenters = ["DC-East-1", "DC-West-1", "DC-Central-1", "AWS-us-east-1"]
        
        # Common RHEL services
        self.common_services = [
            "httpd", "apache2", "nginx", "mysql", "mariadb", "postgresql", 
            "redis", "memcached", "elasticsearch", "tomcat", "nodejs",
            "docker", "kubelet", "sshd", "systemd", "NetworkManager",
            "firewalld", "chronyd", "rsyslog", "postfix"
        ]
        
        # Common packages with versions
        self.common_packages = {
            "httpd": ["2.4.51-7.el9", "2.4.53-11.el9", "2.4.55-1.el9"],
            "httpd-tools": ["2.4.51-7.el9", "2.4.53-11.el9", "2.4.55-1.el9"],
            "mysql-server": ["8.0.32-1.el9", "8.0.34-1.el9", "8.0.35-1.el9"],
            "postgresql": ["13.7-1.el9", "13.8-1.el9", "14.5-1.el9"],
            "kernel": ["5.14.0-162.el9", "5.14.0-284.el9", "5.14.0-325.el9"],
            "glibc": ["2.34-28.el9", "2.34-40.el9", "2.34-60.el9"],
            "openssl": ["3.0.1-41.el9", "3.0.7-16.el9", "3.0.8-1.el9"],
            "systemd": ["250-12.el9", "250-18.el9", "252-13.el9"]
        }
        
        # Realistic error patterns
        self.error_patterns = [
            "Apache failed to restart - MaxRequestWorkers configuration conflict",
            "Service dependency failure - MySQL not responding",
            "Package conflict: httpd-2.4.53 conflicts with custom-apache-2.4.51",
            "Kernel module incompatibility after update",
            "SELinux policy violation preventing service startup",
            "Configuration file syntax error in /etc/httpd/conf/httpd.conf",
            "SSL certificate validation failed after OpenSSL update",
            "Memory allocation error during package installation",
            "Disk space insufficient for package cache",
            "Network timeout during package download"
        ]
        
        # Resolution steps
        self.resolution_patterns = [
            ["Updated MaxRequestWorkers in httpd.conf", "Restarted Apache service"],
            ["Increased MySQL timeout settings", "Restarted MySQL service"],
            ["Removed conflicting package", "Re-applied patch"],
            ["Updated kernel module parameters", "Rebooted system"],
            ["Updated SELinux policy", "Restarted affected service"],
            ["Fixed configuration syntax", "Validated with httpd -t", "Restarted service"],
            ["Updated SSL certificate paths", "Reloaded SSL configuration"],
            ["Increased memory limits", "Retried installation"],
            ["Cleaned package cache", "Freed disk space", "Retried installation"],
            ["Configured proxy settings", "Retried download"]
        ]
    
    def generate_systems(self, count: int = 15) -> List[DemoRHELSystem]:
        """Generate realistic RHEL systems"""
        
        systems = []
        
        # System type patterns
        system_types = [
            {"prefix": "web-prod", "env": "production", "services": ["httpd", "mysql", "redis"]},
            {"prefix": "web-stage", "env": "staging", "services": ["httpd", "mysql"]},
            {"prefix": "app-prod", "env": "production", "services": ["tomcat", "postgresql", "elasticsearch"]},
            {"prefix": "app-stage", "env": "staging", "services": ["tomcat", "postgresql"]},
            {"prefix": "db-prod", "env": "production", "services": ["mysql", "redis", "memcached"]},
            {"prefix": "api-prod", "env": "production", "services": ["nginx", "nodejs", "redis"]},
            {"prefix": "worker-prod", "env": "production", "services": ["docker", "kubelet"]},
            {"prefix": "lb-prod", "env": "production", "services": ["nginx", "haproxy"]},
            {"prefix": "dev", "env": "development", "services": ["httpd", "mysql", "docker"]},
            {"prefix": "test", "env": "testing", "services": ["httpd", "postgresql"]}
        ]
        
        for i in range(count):
            sys_type = random.choice(system_types)
            system_num = (i % 5) + 1
            
            # Generate system properties
            system_id = f"{sys_type['prefix']}-{system_num:02d}"
            hostname = f"{system_id}.company.com"
            
            # Realistic IP address
            ip_base = "10.1" if sys_type['env'] == "production" else "10.2"
            ip_address = f"{ip_base}.{random.randint(1, 254)}.{random.randint(1, 254)}"
            
            # Version distribution (newer versions more likely)
            rhel_version = random.choices(
                self.rhel_versions, 
                weights=[10, 15, 20, 30, 25]  # Favor newer versions
            )[0]
            
            kernel_version = f"5.14.0-{random.randint(150, 400)}.el9.x86_64"
            
            # Generate services (base + some random)
            services = sys_type['services'].copy()
            additional_services = random.sample(
                [s for s in self.common_services if s not in services], 
                random.randint(2, 5)
            )
            services.extend(additional_services)
            
            # Generate installed packages
            packages = {}
            for pkg, versions in self.common_packages.items():
                if random.random() > 0.3:  # 70% chance package is installed
                    packages[pkg] = random.choice(versions)
            
            # Hardware specs based on environment
            if sys_type['env'] == "production":
                cpu_cores = random.choice([8, 16, 24, 32])
                memory_gb = random.choice([32, 64, 128])
                disk_gb = random.choice([500, 1000, 2000])
            else:
                cpu_cores = random.choice([4, 8, 16])
                memory_gb = random.choice([16, 32, 64])
                disk_gb = random.choice([250, 500, 1000])
            
            # Uptime (production systems have higher uptime)
            if sys_type['env'] == "production":
                uptime_days = random.randint(30, 365)
            else:
                uptime_days = random.randint(1, 90)
            
            last_reboot = (datetime.now() - timedelta(days=uptime_days)).isoformat()
            
            system = DemoRHELSystem(
                system_id=system_id,
                hostname=hostname,
                ip_address=ip_address,
                rhel_version=rhel_version,
                kernel_version=kernel_version,
                environment=sys_type['env'],
                datacenter=random.choice(self.datacenters),
                services=services,
                installed_packages=packages,
                cpu_cores=cpu_cores,
                memory_gb=memory_gb,
                disk_gb=disk_gb,
                last_reboot=last_reboot,
                uptime_days=uptime_days
            )
            
            systems.append(system)
        
        return systems
    
    def generate_patch_events(self, systems: List[DemoRHELSystem], events_per_system: int = 8) -> List[DemoPatchEvent]:
        """Generate realistic patch events"""
        
        events = []
        
        # Common RHEL patches
        patches = [
            "RHSA-2024-1234",  # Apache security update
            "RHSA-2024-1235",  # MySQL security update  
            "RHSA-2024-1236",  # Kernel security update
            "RHSA-2024-1237",  # OpenSSL security update
            "RHSA-2024-1238",  # SystemD update
            "RHSA-2024-0987",  # Kernel update
            "RHSA-2024-0988",  # PostgreSQL update
            "RHSA-2024-0989",  # Nginx update
            "RHSA-2023-8876",  # Older Apache update
            "RHSA-2023-8877"   # Older kernel update
        ]
        
        for system in systems:
            for _ in range(events_per_system):
                patch_id = random.choice(patches)
                
                # Generate timestamp (last 6 months)
                days_ago = random.randint(1, 180)
                timestamp = (datetime.now() - timedelta(days=days_ago)).isoformat()
                
                # Success rate depends on environment and patch type
                if system.environment == "production":
                    success_rate = 0.85  # Production is more stable
                elif patch_id.endswith("1234"):  # Apache patch has known issues
                    success_rate = 0.70
                else:
                    success_rate = 0.90
                
                success = random.random() < success_rate
                
                # Packages affected based on patch
                if "1234" in patch_id:  # Apache patch
                    packages = ["httpd", "httpd-tools"]
                    services = ["httpd"] if "httpd" in system.services else ["apache2"]
                elif "1235" in patch_id:  # MySQL patch
                    packages = ["mysql-server", "mysql"]
                    services = ["mysql"] if "mysql" in system.services else ["mariadb"]
                elif "1236" in patch_id or "0987" in patch_id:  # Kernel patch
                    packages = ["kernel", "kernel-tools"]
                    services = ["all"]  # Requires reboot
                else:
                    packages = random.sample(list(system.installed_packages.keys()), random.randint(1, 3))
                    services = random.sample(system.services, random.randint(1, 2))
                
                # Downtime calculation
                if services == ["all"]:  # Reboot required
                    downtime = random.randint(5, 15)
                elif not success:
                    downtime = random.randint(10, 60)
                else:
                    downtime = random.randint(1, 5)
                
                # Error details for failures
                error_message = None
                resolution_steps = None
                if not success:
                    error_message = random.choice(self.error_patterns)
                    resolution_steps = random.choice(self.resolution_patterns)
                
                # Applied by
                applied_by = random.choices(
                    ["automation", "admin-john", "admin-sarah", "patch-team"],
                    weights=[60, 15, 15, 10]
                )[0]
                
                event = DemoPatchEvent(
                    patch_id=patch_id,
                    system_id=system.system_id,
                    timestamp=timestamp,
                    success=success,
                    packages_updated=packages,
                    services_affected=services,
                    downtime_minutes=downtime,
                    error_message=error_message,
                    resolution_steps=resolution_steps,
                    applied_by=applied_by,
                    pre_patch_backup=random.random() > 0.1  # 90% have backups
                )
                
                events.append(event)
        
        return events
    
    def generate_demo_dataset(self) -> Dict:
        """Generate complete demo dataset"""
        
        print("🎭 Generating realistic demo data...")
        
        # Generate systems
        systems = self.generate_systems(15)
        print(f"   📊 Generated {len(systems)} RHEL systems")
        
        # Generate patch events
        events = self.generate_patch_events(systems, 8)
        print(f"   📅 Generated {len(events)} patch events")
        
        # Calculate statistics
        total_events = len(events)
        successful_events = len([e for e in events if e.success])
        failed_events = total_events - successful_events
        
        production_systems = len([s for s in systems if s.environment == "production"])
        
        stats = {
            "total_systems": len(systems),
            "production_systems": production_systems,
            "total_events": total_events,
            "successful_events": successful_events,
            "failed_events": failed_events,
            "overall_success_rate": successful_events / total_events if total_events > 0 else 0,
            "environments": list(set(s.environment for s in systems)),
            "rhel_versions": list(set(s.rhel_version for s in systems)),
            "unique_patches": list(set(e.patch_id for e in events))
        }
        
        print(f"   📈 Success rate: {stats['overall_success_rate']:.1%}")
        print(f"   🏭 Production systems: {production_systems}")
        print(f"   🔧 RHEL versions: {', '.join(sorted(stats['rhel_versions']))}")
        
        return {
            "systems": systems,
            "events": events,
            "statistics": stats
        }

def print_demo_summary(dataset: Dict):
    """Print a summary of the generated demo data"""
    
    systems = dataset["systems"]
    events = dataset["events"]
    stats = dataset["statistics"]
    
    print("\n" + "="*60)
    print("📊 DEMO DATASET SUMMARY")
    print("="*60)
    
    print(f"\n🖥️  SYSTEMS ({len(systems)} total):")
    env_counts = {}
    for system in systems:
        env_counts[system.environment] = env_counts.get(system.environment, 0) + 1
    
    for env, count in sorted(env_counts.items()):
        print(f"   {env}: {count} systems")
    
    print(f"\n📦 PATCHES ({len(stats['unique_patches'])} unique):")
    for patch in sorted(stats['unique_patches']):
        patch_events = [e for e in events if e.patch_id == patch]
        success_rate = len([e for e in patch_events if e.success]) / len(patch_events)
        print(f"   {patch}: {len(patch_events)} applications, {success_rate:.1%} success")
    
    print(f"\n⚠️  NOTABLE FAILURE PATTERNS:")
    failures = [e for e in events if not e.success]
    error_counts = {}
    for failure in failures:
        if failure.error_message:
            error_counts[failure.error_message] = error_counts.get(failure.error_message, 0) + 1
    
    for error, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
        print(f"   {count}x: {error[:60]}...")
    
    print(f"\n🎯 KEY STATISTICS:")
    print(f"   Overall success rate: {stats['overall_success_rate']:.1%}")
    print(f"   Production systems: {stats['production_systems']}/{stats['total_systems']}")
    print(f"   Total patch applications: {stats['total_events']}")
    print(f"   Failed applications: {stats['failed_events']}")

if __name__ == "__main__":
    generator = DemoDataGenerator()
    dataset = generator.generate_demo_dataset()
    print_demo_summary(dataset)
    
    print(f"\n Demo data ready for loading into Neo4j!")