#!/usr/bin/env python3
import csv
import subprocess
import os
import bibtexparser
import re
import unicodedata

# Paths
bib_file = '/home/echo_/Code/asciimath/su2-3nj-series-paper/papers/paper/su2-3nj-unified-representations.bib'
tsv_file = '/home/echo_/Code/asciimath/energy/docs/downloaded_paper_locations.tsv'
work_dir = '/home/echo_/Code/asciimath/su2-3nj-series-paper/papers/related'

# Parse bib file
with open(bib_file, 'r') as f:
    bib_db = bibtexparser.load(f)

bib_entries = {}
for entry in bib_db.entries:
    key = entry['ID']
    title = unicodedata.normalize('NFKD', re.sub(r'[{}]', '', entry.get('title', ''))).lower()
    bib_entries[title] = key

# Parse TSV
tsv_entries = []
with open(tsv_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for i, row in enumerate(reader):
        if 26 <= i <= 40 and row['Manuscript'] == 'Unified Closed-Form Representations and Generating Functionals for SU(2) 3n-j Recoupling Coefficients':
            tsv_entries.append(row)

# Change to work directory
os.chdir(work_dir)

# Process each entry
for entry in tsv_entries:
    title = unicodedata.normalize('NFKD', entry['Name']).lower()
    if title in bib_entries:
        key = bib_entries[title]
        if os.path.exists(key):
            print(f"Skipping already converted: {key}")
        else:
            pdf_path = os.path.join(entry['Ubuntu Path'], entry['Filename'])
            if os.path.exists(pdf_path):
                cmd = ['mineru', '-p', pdf_path, '-o', key, '-m', 'auto', '-d', 'cuda', '-l', 'en']
                print(f"Running: {' '.join(cmd)}")
                subprocess.run(cmd)
            else:
                print(f"PDF not found: {pdf_path}")
    else:
        print(f"No bib match for title: {entry['Name']}")