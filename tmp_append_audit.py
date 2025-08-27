from pathlib import Path
p=Path('docs/HEDGING-TODO-completed.ndjson')
line='{"event":"hedge_file","date":"2025-08-26","repo":"casimir-nanopositioning-platform","path":"README.md","task":"Hedge the file/text: soften absolutist language, add qualifiers and evidence links where available.","status":"completed","completed_date":"2025-08-26","notes":"Softened production-grade claims and added Scope/Validation & Limitations; pointed to docs/ for provenance and UQ.","actor":"assistant","commit_id":"dd5aad5"}\n'
with p.open('a') as f:
    f.write(line)
print('appended to', p)
