#!/usr/bin/env python3
"""
Count non-COMPLETED tasks in TODO.ndjson robustly.
"""
import json
from json import JSONDecoder
from pathlib import Path

p = Path('TODO.ndjson')
if not p.exists():
    print('TODO.ndjson not found')
    raise SystemExit(1)

s = p.read_text(encoding='utf-8')
# Attempt sequential decode to handle arrays or concatenated objects
dec = JSONDecoder()
idx = 0
L = len(s)
count_total = 0
count_non_completed = 0
while idx < L:
    # skip whitespace
    while idx < L and s[idx].isspace():
        idx += 1
    if idx >= L:
        break
    try:
        obj, end = dec.raw_decode(s, idx)
    except json.JSONDecodeError as e:
        # can't decode further
        print('JSON decode error at pos', idx, e)
        break
    # handle lists
    items = obj if isinstance(obj, list) else [obj]
    for it in items:
        count_total += 1
        status = str(it.get('status','')).upper() if isinstance(it, dict) else ''
        if status != 'COMPLETED':
            count_non_completed += 1
    idx = end

print('Total tasks parsed:', count_total)
print('Non-COMPLETED tasks:', count_non_completed)

# Exit codes: 0 if parsed and count found, 2 if non-zero non-completed
raise SystemExit(0 if count_non_completed==0 else 2)