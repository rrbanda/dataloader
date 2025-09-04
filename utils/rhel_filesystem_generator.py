#!/usr/bin/env python3
"""
RHEL Filesystem Generator - Creates realistic RHEL system files for development
Simulates enterprise RHEL environments without needing SSH access to real systems
"""

import os
import random
from datetime import datetime, timedelta
from typing import Dict, List
from pathlib import Path

class RHELFilesystemGenerator:
    """Generates realistic RHEL filesystem content for development/testing"""
    
    def __init__(self, base_path: str = "simulated_rhel_systems"):
        self.base_path = Path(base_path)
        
        # Realistic enterprise system configurations
        self.systems = {
            "web-prod-01": {
                "environment": "production",
                "rhel_version": "9.2",
                "kernel": "5.14.0-284.25.1.el9_2.x86_64",
                "services": ["httpd", "mysql", "redis", "chronyd", "sshd"],
                "criticality": "high",
                "datacenter": "DC-East-1"
            },
            "web-prod-02": {
                "environment": "production", 
                "rhel_version": "9.1",
                "kernel": "5.14.0-162.23.1.el9_1.x86_64",
                "services": ["httpd", "postgresql", "nginx", "chronyd", "sshd"],
                "criticality": "high",
                "datacenter": "DC-West-1"
            },
            "app-prod-01": {
                "environment": "production",
                "rhel_version": "9.2", 
                "kernel": "5.14.0-284.25.1.el9_2.x86_64",
                "services": ["tomcat", "elasticsearch", "docker", "chronyd", "sshd"],
                "criticality": "critical",
                "datacenter": "DC-Central-1"
            },
            "db-prod-01": {
                "environment": "production",
                "rhel_version": "8.8",
                "kernel": "4.18.0-477.27.1.el8_8.x86_64", 
                "services": ["mysql", "redis", "memcached", "chronyd", "sshd"],
                "criticality": "critical",
                "datacenter": "DC-East-1"
            },
            "web-stage-01": {
                "environment": "staging",
                "rhel_version": "9.2",
                "kernel": "5.14.0-284.25.1.el9_2.x86_64",
                "services": ["httpd", "mysql", "chronyd", "sshd"],
                "criticality": "medium",
                "datacenter": "DC-Central-1"
            }
        }
        
        # Common RHEL packages with realistic versions
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
    
    def generate_all_systems(self):
        """Generate realistic files for all simulated systems"""
        print("🏗️ Generating realistic RHEL filesystem content...")
        
        for system_id, config in self.systems.items():
            print(f"   📁 Generating {system_id} ({config['environment']})...")
            self.generate_system_files(system_id, config)
        
        print(" All simulated RHEL systems generated successfully!")
    
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
        
        # Generate uptime
        uptime_file = proc_dir / "uptime"
        uptime_days = random.randint(1, 365)
        uptime_seconds = uptime_days * 24 * 3600 + random.randint(0, 86400)
        uptime_file.write_text(f"{uptime_seconds}.12 {uptime_seconds//2}.34")
        
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

if __name__ == "__main__":
    generator = RHELFilesystemGenerator()
    generator.generate_all_systems()
    
    print("\n🎯 Simulated RHEL systems ready for testing!")
    print("   Use LocalRHELDataCollector to read from these files")
    print("   Compatible with future Satellite/Insights integration")
