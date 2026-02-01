#!/usr/bin/env python3
import csv
import subprocess
import os
import bibtexparser
import re
import unicodedata
import sys

# Paths
bib_file = '/home/echo_/Code/asciimath/su2-3nj-series-paper/papers/paper/su2-3nj-unified-representations.bib'
tsv_file = '/home/echo_/Code/asciimath/energy/docs/downloaded_paper_locations.tsv'
work_dir = '/home/echo_/Code/asciimath/su2-3nj-series-paper/papers/related'

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
        if 26 <= i <= 40 and row['Manuscript'] == 'Unified Closed-Form Representations and Generating Functionals for SU(2) 3n-j Recoupling Coefficients':
            tsv_entries.append(row)

# Change to work directory
os.chdir(work_dir)

mineru_device = os.environ.get('MINERU_DEVICE', 'cuda')

# Process each entry
for entry in tsv_entries:
    title = normalize_title(entry['Name'])
    if title in bib_entries:
        key = bib_entries[title]
        if os.path.exists(key):
            print(f"Skipping already converted: {key}")
        else:
            pdf_path = os.path.join(entry['Ubuntu Path'], entry['Filename'])
            if os.path.exists(pdf_path):
                cmd = ['mineru', '-p', pdf_path, '-o', key, '-m', 'auto', '-d', mineru_device, '-l', 'en']
                print(f"Running: {' '.join(cmd)}")
                if not dry_run:
                    result = subprocess.run(cmd)
                    if result.returncode != 0 and mineru_device == 'cuda':
                        cmd_cpu = ['mineru', '-p', pdf_path, '-o', key, '-m', 'auto', '-d', 'cpu', '-l', 'en']
                        print("Retrying on CPU due to CUDA failure")
                        subprocess.run(cmd_cpu)
            else:
                print(f"PDF not found: {pdf_path}")
    else:
        print(f"No bib match for title: {entry['Name']}")