#!/usr/bin/env python3
import json
from pathlib import Path

todo_path=Path("/home/echo_/Code/asciimath/energy/docs/HEDGING-TODO.ndjson")
completed_path=Path("/home/echo_/Code/asciimath/energy/docs/HEDGING-TODO-completed.ndjson")
completed=set()
if completed_path.exists():
    for l in completed_path.read_text().splitlines():
        try:
            j=json.loads(l)
            key=(j.get('repo'),j.get('path'))
            completed.add(key)
        except Exception:
            pass

for l in todo_path.read_text().splitlines():
    try:
        j=json.loads(l)
    except Exception:
        continue
    if j.get('status')!='todo':
        continue
    key=(j.get('repo'),j.get('path'))
    if key in completed:
        continue
    fp=Path('/home/echo_/Code/asciimath')/j.get('repo')/j.get('path')
    exists=fp.exists()
    print(json.dumps({'repo':j.get('repo'),'path':j.get('path'),'exists':exists}))
    if exists:
        break
