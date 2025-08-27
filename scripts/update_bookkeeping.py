#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

repo="enhanced-simulation-hardware-abstraction-framework"
path_entry="README.md"
commit='6cd7177'

todo=Path('/home/echo_/Code/asciimath/energy/docs/HEDGING-TODO.ndjson')
completed=Path('/home/echo_/Code/asciimath/energy/docs/HEDGING-TODO-completed.ndjson')
lines=todo.read_text().splitlines()
newlines=[]
changed=False
for l in lines:
    try:
        j=json.loads(l)
    except Exception:
        newlines.append(l)
        continue
    if j.get('status')=='todo' and j.get('repo')==repo and j.get('path')==path_entry:
        j['status']='completed'
        j['completed_date']=datetime.utcnow().strftime('%Y-%m-%d')
        j['commit_id']=commit
        newlines.append(json.dumps(j))
        audit={
            'event':'hedge_file',
            'date':datetime.utcnow().strftime('%Y-%m-%d'),
            'repo':repo,
            'path':path_entry,
            'task':'Hedge the file/text: soften absolutist language, add qualifiers and evidence links where available.',
            'status':'completed',
            'completed_date':datetime.utcnow().strftime('%Y-%m-%d'),
            'notes':'Hedged README to soften absolutist claims and add Scope/Validation guidance.',
            'actor':'assistant',
            'commit_id':commit
        }
        completed.write_text(completed.read_text().rstrip('\n')+"\n"+json.dumps(audit)+"\n")
        changed=True
    else:
        newlines.append(l)
if changed:
    todo.write_text('\n'.join(newlines)+"\n")
    print('Updated HEDGING-TODO.ndjson and appended audit (commit='+commit+')')
else:
    print('No matching todo entry updated; maybe it was already completed.')
