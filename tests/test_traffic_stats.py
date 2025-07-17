#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simplified test version of traffic stats script to identify hanging issues
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding for Unicode characters
if sys.platform == "win32":
    try:
        import locale
        if sys.stdout.encoding != 'utf-8':
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, OSError):
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach(), errors='replace')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach(), errors='replace')

def safe_print(text):
    """Safely print text with Unicode characters, falling back to ASCII if needed."""
    try:
        print(text)
    except UnicodeEncodeError:
        ascii_text = text.replace("🚀", "[ROCKET]").replace("✅", "[OK]").replace("❌", "[ERROR]")
        print(ascii_text)

def test_gh_command():
    """Test basic GitHub CLI functionality."""
    safe_print("🚀 Testing GitHub CLI...")
    
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True,
            timeout=10  # 10 second timeout
        )
        
        if result.returncode == 0:
            safe_print("✅ GitHub CLI is working")
            return True
        else:
            safe_print("❌ GitHub CLI auth issue")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        safe_print("❌ GitHub CLI command timed out")
        return False
    except Exception as e:
        safe_print(f"❌ Error testing GitHub CLI: {e}")
        return False

def test_simple_repo_query():
    """Test querying a single repository."""
    safe_print("🚀 Testing simple repository query...")
    
    try:
        result = subprocess.run(
            ["gh", "api", "repos/arcticoder/energy"],
            capture_output=True,
            text=True,
            timeout=15  # 15 second timeout
        )
        
        if result.returncode == 0:
            safe_print("✅ Repository query successful")
            data = json.loads(result.stdout)
            safe_print(f"   Repository: {data.get('name', 'unknown')}")
            safe_print(f"   Stars: {data.get('stargazers_count', 0)}")
            return True
        else:
            safe_print("❌ Repository query failed")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        safe_print("❌ Repository query timed out")
        return False
    except Exception as e:
        safe_print(f"❌ Error querying repository: {e}")
        return False

def test_imports():
    """Test importing potentially problematic modules."""
    safe_print("🚀 Testing module imports...")
    
    try:
        safe_print("   Testing numpy...")
        import numpy as np
        safe_print("   ✅ numpy imported successfully")
        
        safe_print("   Testing scipy...")
        from scipy import stats
        safe_print("   ✅ scipy imported successfully")
        
        return True
    except Exception as e:
        safe_print(f"   ❌ Import error: {e}")
        return False

def main():
    """Main test function."""
    safe_print("🚀 Traffic Stats Troubleshooting Tool")
    print("=" * 50)
    
    # Test 1: Module imports
    if not test_imports():
        safe_print("❌ Module import test failed")
        return
    
    # Test 2: GitHub CLI basic functionality
    if not test_gh_command():
        safe_print("❌ GitHub CLI test failed")
        return
    
    # Test 3: Simple repository query
    if not test_simple_repo_query():
        safe_print("❌ Repository query test failed")
        return
    
    safe_print("✅ All tests passed - basic functionality is working")
    safe_print("The issue may be with the full repository list or processing logic")

if __name__ == "__main__":
    main()
