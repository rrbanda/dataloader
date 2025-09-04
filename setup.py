#!/usr/bin/env python3
"""
Universal DataLoader - AI-Powered Knowledge Graph Construction
Domain-agnostic data loading for any use case
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Universal DataLoader - AI-Powered Knowledge Graph Construction"

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    requirements = []
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
    return requirements

setup(
    name="universal-dataloader",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Universal DataLoader - AI-Powered Knowledge Graph Construction",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/rrbanda/dataloader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Data Engineers", 
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Database",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.991",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "full": [
            "unstructured>=0.10.0",
            "pygrok>=1.0.0",
            "pypdf>=3.0.0",
            "beautifulsoup4>=4.11.0",
            "markdown>=3.4.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "universal-dataloader=core.unified_dataloader:main",
        ],
    },
    include_package_data=True,
    package_data={
        "config": ["*.yaml", "*.yml"],
        "examples": ["*.py"],
        "tests": ["*.py"],
    },
    keywords=[
        "data-loading",
        "knowledge-graph", 
        "neo4j",
        "langchain",
        "ai",
        "nlp",
        "data-extraction",
        "graph-database",
        "llm",
        "rag",
        "data-pipeline"
    ],
    project_urls={
        "Bug Reports": "https://github.com/rrbanda/dataloader/issues",
        "Source": "https://github.com/rrbanda/dataloader",
        "Documentation": "https://github.com/rrbanda/dataloader/blob/main/README.md",
    },
)
