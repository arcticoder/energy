#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limited test version to identify which repository is causing the hang
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        if sys.stdout.encoding != 'utf-8':
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, OSError):
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach(), errors='replace')

def safe_print(text):
    """Safely print text with Unicode characters."""
    try:
        print(text)
    except UnicodeEncodeError:
        ascii_text = text.replace("🚀", "[ROCKET]").replace("✅", "[OK]").replace("❌", "[ERROR]")
        print(ascii_text)

# Test with just the first few repositories
TEST_REPOS = [
    "energy", 
    "artificial-gravity-field-generator", 
    "casimir-anti-stiction-metasurface-coatings",
    "casimir-environmental-enclosure-platform",
    "casimir-nanopositioning-platform"
]

def run_gh_command_with_timeout(args, timeout_seconds=15):
    """Run GitHub CLI command with timeout."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=timeout_seconds,
            check=False
        )
        
        if result.returncode != 0:
            return None
            
        if not result.stdout or not result.stdout.strip():
            return None
            
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        safe_print(f"   ❌ Command timed out after {timeout_seconds} seconds")
        return None
    except Exception as e:
        safe_print(f"   ❌ Error: {e}")
        return None

def test_repository(repo):
    """Test processing a single repository with detailed logging."""
    safe_print(f"🚀 Testing repository: {repo}")
    
    # Test 1: Basic repo info
    safe_print("   Step 1: Getting repository info...")
    repo_info = run_gh_command_with_timeout(["api", f"repos/arcticoder/{repo}"])
    if repo_info:
        safe_print(f"   ✅ Repo info: {repo_info.get('stargazers_count', 0)} stars")
    else:
        safe_print("   ❌ Failed to get repo info")
        return False
    
    # Test 2: Traffic views
    safe_print("   Step 2: Getting traffic views...")
    views_data = run_gh_command_with_timeout(["api", f"repos/arcticoder/{repo}/traffic/views"])
    if views_data:
        safe_print(f"   ✅ Views data: {views_data.get('count', 0)} total views")
    else:
        safe_print("   ❌ Failed to get views data (may be normal for some repos)")
    
    # Test 3: Traffic clones
    safe_print("   Step 3: Getting traffic clones...")
    clones_data = run_gh_command_with_timeout(["api", f"repos/arcticoder/{repo}/traffic/clones"])
    if clones_data:
        safe_print(f"   ✅ Clones data: {clones_data.get('count', 0)} total clones")
    else:
        safe_print("   ❌ Failed to get clones data (may be normal for some repos)")
    
    # Test 4: Forks
    safe_print("   Step 4: Getting forks...")
    forks_data = run_gh_command_with_timeout(["api", f"repos/arcticoder/{repo}/forks"])
    if forks_data:
        safe_print(f"   ✅ Forks data: {len(forks_data)} forks")
    else:
        safe_print("   ❌ Failed to get forks data")
    
    safe_print(f"✅ Repository {repo} processed successfully")
    print("-" * 60)
    return True

def main():
    """Main test function."""
    safe_print("🚀 Repository-by-Repository Testing Tool")
    print("=" * 60)
    
    successful = 0
    failed = 0
    
    for repo in TEST_REPOS:
        try:
            if test_repository(repo):
                successful += 1
            else:
                failed += 1
        except KeyboardInterrupt:
            safe_print(f"❌ Interrupted while processing {repo}")
            break
        except Exception as e:
            safe_print(f"❌ Unexpected error processing {repo}: {e}")
            failed += 1
    
    print("=" * 60)
    safe_print(f"Summary: {successful} successful, {failed} failed")
    
    if failed == 0:
        safe_print("✅ All test repositories processed successfully")
        safe_print("The issue may be with repositories later in the list or processing volume")
    else:
        safe_print("❌ Some repositories failed - this may indicate the source of the hanging issue")

if __name__ == "__main__":
    main()
