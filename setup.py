#!/usr/bin/env python3
"""
Energy Framework - Dynamic Backreaction Factor Framework
Revolutionary intelligent adaptive energy field enhancement technology
"""

from setuptools import setup, find_packages
import os

# Read version from VERSION file
def get_version():
    """Read version from VERSION file"""
    version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
    if os.path.exists(version_file):
        with open(version_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return '2.0.0'

# Read long description from README
def get_long_description():
    """Read long description from README.md"""
    readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_file):
        with open(readme_file, 'r', encoding='utf-8') as f:
            return f.read()
    return "Revolutionary Dynamic Backreaction Factor Framework for intelligent adaptive energy field enhancement"

setup(
    name="energy-framework",
    version=get_version(),
    author="Energy Framework Team",
    author_email="team@energy-framework.org",
    description="Revolutionary Dynamic Backreaction Factor Framework - World's First Intelligent Adaptive Energy Field Enhancement Technology",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/energy-framework/energy",
    project_urls={
        "Documentation": "https://github.com/energy-framework/energy/docs",
        "Bug Reports": "https://github.com/energy-framework/energy/issues",
        "Source": "https://github.com/energy-framework/energy",
        "Changelog": "https://github.com/energy-framework/energy/CHANGELOG.md",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Scientific/Engineering",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "sympy>=1.8",
        "pydantic>=1.8.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.910",
            "pre-commit>=2.15",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
            "myst-parser>=0.15",
        ],
        "test": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "pytest-benchmark>=3.4",
            "hypothesis>=6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "energy-framework=src.core.cli:main",
            "dynamic-backreaction=src.core.dynamic_backreaction:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yaml", "*.yml", "*.json"],
    },
    zip_safe=False,
    keywords=[
        "quantum-gravity",
        "energy-enhancement",
        "dynamic-backreaction",
        "adaptive-systems",
        "field-manipulation",
        "spacetime-geometry",
        "intelligent-optimization",
        "physics-simulation",
        "gravitational-fields",
        "revolutionary-technology",
    ],
    platforms=["any"],
    license="MIT",
)
