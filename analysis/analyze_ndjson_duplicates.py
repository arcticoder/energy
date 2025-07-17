#!/usr/bin/env python3
"""
Analyze NDJSON file for repository duplicates within each date entry.
"""
import json
from pathlib import Path

def analyze_ndjson_duplicates():
    """Analyze the NDJSON file for repository duplicates within each date entry."""
    ndjson_file = Path("traffic_stats_history.ndjson")
    
    if not ndjson_file.exists():
        print("❌ NDJSON file not found")
        return
    
    print("🔍 Analyzing NDJSON for repository duplicates...")
    
    # Load all entries
    entries = []
    with open(ndjson_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    entry = json.loads(line)
                    entries.append((line_num, entry))
                except json.JSONDecodeError as e:
                    print(f"   ⚠️  Skipping invalid JSON on line {line_num}: {e}")
    
    print(f"✅ Loaded {len(entries)} entries")
    
    # Analyze each entry for duplicates
    total_duplicates = 0
    
    for line_num, entry in entries:
        date = entry.get('date', 'unknown')
        print(f"\n📊 Analyzing entry {line_num} (date: {date})...")
        
        if 'repositories' in entry:
            repos = entry['repositories']
            
            # Check for duplicates by counting repository names
            repo_counts = {}
            for repo_name in repos.keys():
                repo_counts[repo_name] = repo_counts.get(repo_name, 0) + 1
            
            # Find duplicates
            duplicates = {name: count for name, count in repo_counts.items() if count > 1}
            
            print(f"   📈 Total repositories: {len(repos)}")
            print(f"   🔍 Unique repository names: {len(repo_counts)}")
            
            if duplicates:
                print(f"   ⚠️  Found {len(duplicates)} duplicated repository names:")
                for repo_name, count in duplicates.items():
                    print(f"      - {repo_name}: appears {count} times")
                    total_duplicates += count - 1  # count extra occurrences
            else:
                print(f"   ✅ No duplicates found in this entry")
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total entries analyzed: {len(entries)}")
    print(f"   Total duplicate repository entries: {total_duplicates}")
    
    if total_duplicates > 0:
        print(f"   ❌ DUPLICATES DETECTED - Need to fix the data")
    else:
        print(f"   ✅ NO DUPLICATES FOUND - Data is clean")

if __name__ == "__main__":
    analyze_ndjson_duplicates()
