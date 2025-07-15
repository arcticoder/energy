#!/usr/bin/env python3
import json

with open('traffic_stats_history.ndjson', 'r') as f:
    lines = f.readlines()
    
total_warp_field_coils = 0
for i, line in enumerate(lines, 1):
    data = json.loads(line.strip())
    if 'warp-field-coils' in data.get('repositories', {}):
        total_warp_field_coils += 1
        print(f'Line {i} ({data["date"]}): warp-field-coils found')

print(f'Total occurrences of warp-field-coils: {total_warp_field_coils}')
