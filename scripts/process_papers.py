#!/usr/bin/env python3
import csv
import subprocess
import os
import shutil
import bibtexparser
import re
import unicodedata
import sys

# Paths
bib_file = '/home/echo_/Code/asciimath/energy-tensor-cone/papers/aqei-cone-formalization.bib'
tsv_file = '/home/echo_/Code/asciimath/energy/docs/downloaded_paper_locations.tsv'
work_dir = '/home/echo_/Code/asciimath/energy-tensor-cone/papers/related' 

dry_run = '--dry-run' in sys.argv

# Parse bib file
def normalize_title(text):
    normalized = unicodedata.normalize('NFKD', text)
    normalized = re.sub(r'[{}]', '', normalized)
    normalized = normalized.replace('\u2019', "'").replace('\u2018', "'")
    normalized = re.sub(r'[\u2010-\u2015\u2212]', '-', normalized)
    normalized = re.sub(r'\s+', ' ', normalized)
    return normalized.strip().lower()

with open(bib_file, 'r') as f:
    bib_db = bibtexparser.load(f)

bib_entries = {}
for entry in bib_db.entries:
    key = entry['ID']
    title = normalize_title(entry.get('title', ''))
    bib_entries[title] = key

# Parse TSV
tsv_entries = []
with open(tsv_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for i, row in enumerate(reader):
        if not row:
            continue
        # select rows that look like PDFs awaiting conversion (handles single-entry TSVs)
        row_text = ' '.join([(v or '') for v in row.values()])
        if 'awaiting' in row_text.lower() or any((v or '').lower().endswith('.pdf') for v in row.values()):
            tsv_entries.append(row)

# Change to work directory
os.chdir(work_dir)

print(f"TSV entries to process: {len(tsv_entries)}")
for r in tsv_entries:
    print(" -", r.get('Manuscript') or r.get('Name'))

mineru_device = os.environ.get('MINERU_DEVICE', 'cuda')
mineru_path = shutil.which('mineru')

def _find_pdf_path(row):
    # prefer Ubuntu Path + Path/Filename
    up = (row.get('Ubuntu Path') or '').strip()
    path_name = (row.get('Path') or row.get('Filename') or row.get('Name') or '').strip()
    if up and path_name:
        candidate = os.path.join(up, os.path.basename(path_name))
        if os.path.exists(candidate):
            return candidate
    # absolute pdf path in any column
    for v in row.values():
        if isinstance(v, str):
            s = v.strip()
            if s.startswith('/') and s.lower().endswith('.pdf') and os.path.exists(s):
                return s
    # convert UNC WSL path if present
    name = (row.get('Name') or '')
    if isinstance(name, str) and name.startswith('\\\\wsl.localhost\\Ubuntu\\'):
        p = name.replace('\\\\wsl.localhost\\Ubuntu\\', '/').replace('\\', '/')
        if os.path.exists(p):
            return p
    # fallback to any value that looks like a pdf path-like string
    for k in ('Filename', 'Path', 'Name'):
        v = (row.get(k) or '').strip()
        if v.lower().endswith('.pdf'):
            return v
    return None

# Process each entry
for entry in tsv_entries:
    title = normalize_title(entry.get('Manuscript', entry.get('Name', '')))
    if title in bib_entries:
        key = bib_entries[title]
        md_path = os.path.join(work_dir, f"{key}.md")
        if os.path.exists(key) or os.path.exists(md_path):
            print(f"Skipping already converted: {key}")
        else:
            pdf_path = _find_pdf_path(entry)
            if pdf_path and os.path.exists(pdf_path):
                print(f"Found PDF for '{entry.get('Manuscript', entry.get('Name',''))}': {pdf_path}")
                if mineru_path:
                    cmd = [mineru_path, '-p', pdf_path, '-o', key, '-m', 'auto', '-d', mineru_device, '-l', 'en']
                    print(f"Running: {' '.join(cmd)}")
                    if not dry_run:
                        result = subprocess.run(cmd)
                        if result.returncode != 0 and mineru_device == 'cuda':
                            cmd_cpu = [mineru_path, '-p', pdf_path, '-o', key, '-m', 'auto', '-d', 'cpu', '-l', 'en']
                            print("Retrying on CPU due to CUDA failure")
                            subprocess.run(cmd_cpu)
                else:
                    # create placeholder markdown so the output is findable even if mineru isn't installed
                    with open(md_path, 'w', encoding='utf-8') as m:
                        m.write(f"# {entry.get('Manuscript', entry.get('Name',''))}\n\n")
                        m.write("> Placeholder: `mineru` not available; created markdown instead of running conversion.\n\n")
                        m.write(f"- Source PDF: {pdf_path}\n")
                        m.write(f"- BibTeX key: {key}\n")
                        m.write("\n---\n\n")
                    print(f"Created placeholder markdown: {md_path}")
            else:
                print(f"PDF not found (tried multiple columns): {entry}")
    else:
        # No BibTeX match — create a placeholder markdown so you can find and review this item
        manuscript = entry.get('Manuscript', entry.get('Name', 'untitled'))
        slug = re.sub(r'[^a-z0-9]+', '-', normalize_title(manuscript)).strip('-')[:80] or 'untitled'
        md_path = os.path.join(work_dir, f"{slug}.md")
        pdf_path = _find_pdf_path(entry)
        with open(md_path, 'w', encoding='utf-8') as m:
            m.write(f"# {manuscript}\n\n")
            m.write("> Placeholder: no BibTeX match found for this manuscript.\n\n")
            if pdf_path:
                m.write(f"- Source PDF: {pdf_path}\n")
            # include TSV row for reference
            m.write("\n---\n\n")
            m.write("## TSV row\n\n```")
            for k, v in entry.items():
                m.write(f"\n{k}: {v}")
            m.write("\n```\n")
        print(f"Created placeholder markdown for unmatched entry: {md_path}")