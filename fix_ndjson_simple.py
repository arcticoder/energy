#!/usr/bin/env python3
"""
Fix NDJSON by keeping only the most recent entry
"""

import json

def fix_ndjson_keep_latest():
    """Keep only the most recent entry in NDJSON file"""
    
    entries = []
    with open('traffic_stats_history.ndjson', 'r') as f:
        for line in f:
            if line.strip():
                entry = json.loads(line.strip())
                entries.append(entry)
    
    print(f"Found {len(entries)} entries")
    
    if len(entries) <= 1:
        print("Already has 1 or fewer entries")
        return
    
    # Keep only the last (most recent) entry
    latest_entry = entries[-1]
    
    # Write only the latest entry back
    with open('traffic_stats_history.ndjson', 'w') as f:
        f.write(json.dumps(latest_entry) + '\n')
    
    print(f"✅ Reduced from {len(entries)} entries to 1 entry")
    print(f"✅ Kept latest entry with timestamp: {latest_entry.get('timestamp', 'unknown')}")
    print(f"✅ Contains {len(latest_entry.get('repositories', []))} repositories")

if __name__ == "__main__":
    fix_ndjson_keep_latest()
