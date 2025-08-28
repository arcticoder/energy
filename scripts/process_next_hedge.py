#!/usr/bin/env python3
"""Find the next todo in HEDGING-TODO.ndjson whose path exists locally,
apply conservative hedging edits to the target file, commit & push the repo,
then update HEDGING-TODO.ndjson and append to HEDGING-TODO-completed.ndjson
and commit/push the bookkeeping repo.
"""
import os,sys,json,re,subprocess
from datetime import datetime
ROOT_WS='/home/echo_/Code/asciimath'
BOOK_ROOT=os.path.join(ROOT_WS,'energy')
NDJSON=os.path.join(BOOK_ROOT,'docs','HEDGING-TODO.ndjson')
COMPLETED=os.path.join(BOOK_ROOT,'docs','HEDGING-TODO-completed.ndjson')

with open(NDJSON,'r',encoding='utf-8') as f:
    lines=[l.rstrip('\n') for l in f if l.strip()]
objs=[json.loads(l) for l in lines]

# find next todo with file exists
sel=None
for o in objs:
    if o.get('status')=='todo':
        repo=o['repo']
        path=o['path']
        # skip Github About entries
        if path.strip().startswith('('):
            continue
        p=os.path.join(ROOT_WS,repo,path)
        if os.path.exists(p):
            sel={'obj':o,'repo':repo,'path':path,'abs_path':p}
            break

if not sel:
    print('No actionable todo with existing file found. Exiting.')
    sys.exit(0)

print('Selected:', sel['repo'], sel['path'])

# Read file
p=sel['abs_path']
with open(p,'r',encoding='utf-8') as f:
    content=f.read()

orig=content
# Conservative replacement rules (case-insensitive)
replacements = [
    (r"\bbreakthrough\b", "reported improvement (see methods and evidence)"),
    (r"\brevolutionary\b", "proposed"),
    (r"\bproduction[- ]?ready\b", "not production-ready / research-stage"),
    (r"\bexact\b", "approximate"),
    (r"\bdefinitive\b", "preliminary"),
    (r"\bwe proved\b", "we provide evidence consistent with"),
    (r"\bunprecedented\b", "noted in these example runs"),
    (r"\bgame-changer\b", "notable in these runs (requires replication)"),
]
for pat,repl in replacements:
    content=re.sub(pat,repl,content,flags=re.IGNORECASE)

# Ensure Scope, Validation & Limitations exists
if 'Scope, Validation & Limitations' not in content and 'Scope, Validation and Limitations' not in content:
    append_section='''\n## Scope, Validation & Limitations\n\n- Scope: The materials and numeric outputs in this repository are research-stage examples and depend on implementation choices, parameter settings, and numerical tolerances.\n- Validation: Reproducibility artifacts (scripts, raw outputs, seeds, and environment details) are provided in `docs/` or `examples/` where available; reproduce analyses with parameter sweeps and independent environments to assess robustness.\n- Limitations: Results are sensitive to modeling choices and discretization. Independent verification, sensitivity analyses, and peer review are recommended before using these results for engineering or policy decisions.\n'''
    content = content.rstrip() + '\n\n' + append_section

# If no change, report and exit
if content.strip() == orig.strip():
    print('No textual changes applied (content already hedged). Still adding Scope section if missing.')

# Write atomically
bak = p + '.bak'
with open(bak,'w',encoding='utf-8') as f:
    f.write(orig)
with open(p + '.tmp','w',encoding='utf-8') as f:
    f.write(content)
os.replace(p + '.tmp', p)
print('Wrote hedged content to', p)

# Commit & push target repo
repo_dir=os.path.join(ROOT_WS,sel['repo'])
commit_msg=f"Hedge {sel['path']}: soften absolute claims; add Scope/Validation & Limitations; add UQ/repro guidance"
try:
    subprocess.check_call(['git','add',sel['path']], cwd=repo_dir)
    subprocess.check_call(['git','commit','-m',commit_msg], cwd=repo_dir)
except subprocess.CalledProcessError:
    print('Git commit may have failed or nothing to commit in target repo (it may already be clean).')

# Get short commit id
try:
    rev = subprocess.check_output(['git','rev-parse','--short','HEAD'], cwd=repo_dir).decode().strip()
except Exception:
    rev = None
print('Target repo HEAD:', rev)
# push
try:
    subprocess.check_call(['git','push','origin','main'], cwd=repo_dir)
    print('Pushed target repo')
except subprocess.CalledProcessError:
    print('Failed to push target repo; continuing to bookkeeping update')

# Re-read NDJSON fresh and update the first matching todo entry
with open(NDJSON,'r',encoding='utf-8') as f:
    lines=[l.rstrip('\n') for l in f if l.strip()]
objs=[json.loads(l) for l in lines]
updated=None
for o in objs:
    if o.get('status')=='todo' and o.get('repo')==sel['repo'] and o.get('path')==sel['path']:
        o['status']='completed'
        o['completed_date']=datetime.utcnow().replace(microsecond=0).isoformat()+'Z'
        o['commit_id']=rev
        o['notes']='Hedged README: softened absolutist claims; added Scope/Validation & Limitations and UQ/repro guidance.'
        o['actor']='copilot'
        updated=o
        break

if not updated:
    print('Could not find matching todo entry to update; aborting NDJSON update')
    sys.exit(1)

# Write back NDJSON and append to completed
with open(NDJSON,'w',encoding='utf-8') as f:
    for o in objs:
        f.write(json.dumps(o,ensure_ascii=False)+'\n')
with open(COMPLETED,'a',encoding='utf-8') as f:
    f.write(json.dumps(updated,ensure_ascii=False)+'\n')
print('Bookkeeping NDJSON updated and appended to completed log')

# Commit and push bookkeeping
try:
    subprocess.check_call(['git','add','docs/HEDGING-TODO.ndjson','docs/HEDGING-TODO-completed.ndjson'], cwd=BOOK_ROOT)
    subprocess.check_call(['git','commit','-m',f'Bookkeeping: record completed hedging for {sel["repo"]}/{sel["path"]} ({rev})'], cwd=BOOK_ROOT)
    short = subprocess.check_output(['git','rev-parse','--short','HEAD'], cwd=BOOK_ROOT).decode().strip()
    print('Bookkeeping commit:', short)
    subprocess.check_call(['git','push','origin','main'], cwd=BOOK_ROOT)
    print('Pushed bookkeeping to origin/main')
except subprocess.CalledProcessError as e:
    print('Bookkeeping git commands failed:', e)

print('All done for this item.')
