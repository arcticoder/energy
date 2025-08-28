#!/usr/bin/env python3
import json, sys, os
from datetime import datetime

repo = 'lqg-first-principles-fine-structure-constant'
path = 'README.md'
commit_id = '6c20f5e'

ROOT = '/home/echo_/Code/asciimath/energy'
NDJSON = os.path.join(ROOT, 'docs', 'HEDGING-TODO.ndjson')
COMPLETED = os.path.join(ROOT, 'docs', 'HEDGING-TODO-completed.ndjson')

# Read NDJSON
with open(NDJSON, 'r', encoding='utf-8') as f:
    lines = [l.rstrip('\n') for l in f if l.strip()]

objs = [json.loads(l) for l in lines]

found = False
updated_obj = None
for o in objs:
    if o.get('repo') == repo and o.get('path') == path and o.get('status') == 'todo':
        o['status'] = 'completed'
        o['completed_date'] = datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
        o['commit_id'] = commit_id
        o['notes'] = 'Hedged README: softened absolutist claims; added Scope/Validation & Limitations; added UQ/repro guidance.'
        o['actor'] = 'copilot'
        found = True
        updated_obj = o
        break

if not found:
    print('No matching todo entry found (repo/path/status). Aborting.', file=sys.stderr)
    sys.exit(1)

# Write back NDJSON (preserving order)
with open(NDJSON, 'w', encoding='utf-8') as f:
    for o in objs:
        f.write(json.dumps(o, ensure_ascii=False) + '\n')

# Append to completed log
with open(COMPLETED, 'a', encoding='utf-8') as f:
    f.write(json.dumps(updated_obj, ensure_ascii=False) + '\n')

print('NDJSON updated and appended to completed log.')

# Commit and push bookkeeping
os.chdir(ROOT)
import subprocess
try:
    subprocess.check_call(['git', 'add', 'docs/HEDGING-TODO.ndjson', 'docs/HEDGING-TODO-completed.ndjson'])
    subprocess.check_call(['git', 'commit', '-m', f'Bookkeeping: record completed hedging for {repo}/{path} ({commit_id})'])
    short = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
    print('Bookkeeping commit:', short)
    subprocess.check_call(['git', 'push', 'origin', 'main'])
    print('Pushed bookkeeping to origin/main')
except subprocess.CalledProcessError as e:
    print('Git command failed:', e, file=sys.stderr)
    sys.exit(1)
