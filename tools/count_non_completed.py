#!/usr/bin/env python3
"""
Count non-COMPLETED tasks in TODO.ndjson robustly.
"""
import argparse
import json
from json import JSONDecoder
from pathlib import Path

parser = argparse.ArgumentParser(
    description='Count non-COMPLETED tasks in a NDJSON or concatenated JSON file.'
)
parser.add_argument('file', nargs='?', default='TODO.ndjson',
                    help='Path to TODO ndjson file (default: TODO.ndjson)')
parser.add_argument('-s', '--show', action='store_true',
                    help='Show non-COMPLETED task objects (pretty JSON)')
args = parser.parse_args()

p = Path(args.file)
if not p.exists():
    print(f'{p} not found')
    raise SystemExit(1)

s = p.read_text(encoding='utf-8')
# Attempt sequential decode to handle arrays or concatenated objects
dec = JSONDecoder()
idx = 0
L = len(s)
count_total = 0
count_non_completed = 0
non_completed_items = []
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
            # preserve original item for optional output
            non_completed_items.append(it)
    idx = end

print('Total tasks parsed:', count_total)
print('Non-COMPLETED tasks:', count_non_completed)

# If requested, show the non-COMPLETED tasks in pretty JSON form
if args.show:
    if count_non_completed == 0:
        print('\nNo non-COMPLETED tasks to show.')
    else:
        print(f"\nShowing {count_non_completed} non-COMPLETED task(s):\n")
        for i, itm in enumerate(non_completed_items, 1):
            try:
                print(f"--- Task {i} ---")
                print(json.dumps(itm, indent=2, ensure_ascii=False))
            except Exception:
                # fallback: print raw repr
                print(repr(itm))

# Exit codes: 0 if parsed and count found, 2 if non-zero non-completed
raise SystemExit(0 if count_non_completed==0 else 2)