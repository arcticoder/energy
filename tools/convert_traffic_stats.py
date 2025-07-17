#!/usr/bin/env python3
"""
Convert traffic_stats_history.json to NDJSON format and deduplicate entries.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def convert_json_to_ndjson_and_deduplicate():
    """Convert the massive JSON file to NDJSON and deduplicate."""
    json_file = Path("traffic_stats_history.json")
    ndjson_file = Path("traffic_stats_history.ndjson")
    
    if not json_file.exists():
        print(f"❌ {json_file} not found")
        return False
    
    print(f"🔄 Loading {json_file}...")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        print(f"📊 Loaded {len(history)} entries")
        
        # Deduplicate by date - keep only the latest entry for each date
        date_entries = {}
        
        for entry in history:
            date = entry.get('date')
            if date:
                # Keep the latest timestamp for each date
                if date not in date_entries or entry.get('timestamp', '') > date_entries[date].get('timestamp', ''):
                    date_entries[date] = entry
        
        # Sort by date
        sorted_entries = sorted(date_entries.values(), key=lambda x: x.get('date', ''))
        
        print(f"✅ Deduplicated to {len(sorted_entries)} unique dates")
        
        # Convert to NDJSON format
        print(f"💾 Writing NDJSON to {ndjson_file}...")
        
        with open(ndjson_file, 'w', encoding='utf-8') as f:
            for entry in sorted_entries:
                f.write(json.dumps(entry, separators=(',', ':')) + '\n')
        
        # Backup original file
        backup_file = json_file.with_suffix('.json.backup')
        print(f"💾 Creating backup: {backup_file}")
        json_file.rename(backup_file)
        
        print(f"✅ Conversion complete!")
        print(f"   Original: {len(history)} entries → {backup_file}")
        print(f"   New NDJSON: {len(sorted_entries)} entries → {ndjson_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def load_ndjson_history():
    """Load history from NDJSON file."""
    ndjson_file = Path("traffic_stats_history.ndjson")
    
    if not ndjson_file.exists():
        return []
    
    history = []
    with open(ndjson_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    history.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"⚠️  Skipping invalid JSON line: {e}")
    
    return history

def save_ndjson_history(history):
    """Save history to NDJSON file."""
    ndjson_file = Path("traffic_stats_history.ndjson")
    
    with open(ndjson_file, 'w', encoding='utf-8') as f:
        for entry in history:
            f.write(json.dumps(entry, separators=(',', ':')) + '\n')

if __name__ == "__main__":
    print("🔄 Traffic Stats JSON to NDJSON Converter")
    print("=" * 50)
    
    success = convert_json_to_ndjson_and_deduplicate()
    
    if success:
        print("\n✅ Conversion successful!")
        print("🔧 Next steps:")
        print("1. Update check_traffic_stats.py to use NDJSON format")
        print("2. Regenerate traffic_stats_chart.html")
        print("3. Commit and push changes")
    else:
        print("\n❌ Conversion failed!")
    
    sys.exit(0 if success else 1)
