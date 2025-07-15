#!/usr/bin/env python3
"""
Fix NDJSON duplicates by properly parsing and deduplicating repository data.
The issue is that repository data within each date entry contains duplicates.
"""
import json
from pathlib import Path

def fix_ndjson_duplicates():
    """Fix the NDJSON file by removing repository duplicates within each date entry."""
    ndjson_file = Path("traffic_stats_history.ndjson")
    
    if not ndjson_file.exists():
        print("❌ NDJSON file not found")
        return
    
    print("🔄 Loading and fixing NDJSON data...")
    
    # Load all entries
    entries = []
    with open(ndjson_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    entry = json.loads(line)
                    entries.append(entry)
                    print(f"   📊 Loaded entry {line_num}: {entry.get('date', 'unknown')}")
                except json.JSONDecodeError as e:
                    print(f"   ⚠️  Skipping invalid JSON on line {line_num}: {e}")
    
    print(f"✅ Loaded {len(entries)} entries")
    
    # Fix duplicates in each entry
    fixed_entries = []
    for entry in entries:
        date = entry.get('date', 'unknown')
        print(f"\n🔧 Fixing entry for {date}...")
        
        if 'repositories' in entry:
            repos = entry['repositories']
            
            # Count unique repository names vs total entries
            unique_repos = set()
            total_repo_entries = 0
            
            # Collect all unique repository data
            repo_data = {}
            for repo_name, repo_info in repos.items():
                if repo_name not in repo_data:
                    repo_data[repo_name] = repo_info
                    unique_repos.add(repo_name)
                total_repo_entries += 1
            
            print(f"   📊 Found {total_repo_entries} repository entries, {len(unique_repos)} unique repositories")
            
            if total_repo_entries > len(unique_repos):
                print(f"   🔧 Removing {total_repo_entries - len(unique_repos)} duplicate repository entries")
                
                # Replace with deduplicated data
                entry['repositories'] = repo_data
                
                # Recalculate totals
                totals = {
                    "views": 0,
                    "unique_views": 0, 
                    "clones": 0,
                    "unique_clones": 0,
                    "stars": 0,
                    "watchers": 0,
                    "forks": 0,
                    "active_forks": 0,
                    "recent_forks": 0,
                    "repositories_count": len(repo_data)
                }
                
                for repo_info in repo_data.values():
                    totals["views"] += repo_info.get("views_total", 0)
                    totals["unique_views"] += repo_info.get("views_unique", 0)
                    totals["clones"] += repo_info.get("clones_total", 0)
                    totals["unique_clones"] += repo_info.get("clones_unique", 0)
                    totals["stars"] += repo_info.get("stars", 0)
                    totals["watchers"] += repo_info.get("watchers", 0)
                    totals["forks"] += repo_info.get("forks", 0)
                    totals["active_forks"] += repo_info.get("active_forks", 0)
                    totals["recent_forks"] += repo_info.get("recent_forks", 0)
                
                entry["totals"] = totals
                print(f"   ✅ Fixed totals: {totals['repositories_count']} repos, {totals['clones']} clones")
        
        fixed_entries.append(entry)
    
    # Save fixed data
    print(f"\n💾 Saving {len(fixed_entries)} fixed entries...")
    with open(ndjson_file, 'w', encoding='utf-8') as f:
        for entry in fixed_entries:
            f.write(json.dumps(entry, separators=(',', ':')) + '\n')
    
    print("✅ NDJSON duplicates fixed successfully!")

if __name__ == "__main__":
    fix_ndjson_duplicates()
