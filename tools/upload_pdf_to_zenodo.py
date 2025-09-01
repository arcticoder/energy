#!/usr/bin/env python3
"""
Upload a single PDF to Zenodo using the existing upload utilities.
"""
import os
import json
from pathlib import Path
import requests
from datetime import datetime

# Load token from .env
env = Path(__file__).resolve().parents[2] / '.env'
if env.exists():
    with open(env) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ[k] = v

TOKEN = os.getenv('ZENODO_PAT_TOKEN')
if not TOKEN:
    raise SystemExit('ZENODO_PAT_TOKEN not found in environment')

PDF_PATH = Path('/home/username/Code/hts-coils/papers/rebco_hts_coil_optimization_fusion_antimatter.pdf')
if not PDF_PATH.exists():
    raise SystemExit(f'PDF not found: {PDF_PATH}')

BASE_URL = 'https://zenodo.org/api'
HEADERS = {'Authorization': f'Bearer {TOKEN}'}

# Create deposition
print('Creating Zenodo deposition...')
resp = requests.post(f'{BASE_URL}/deposit/depositions', headers=HEADERS, json={})
resp.raise_for_status()
dep = resp.json()
dep_id = dep['id']
bucket = dep['links']['bucket']
print('Deposition created:', dep_id)

# Upload file
print('Uploading PDF...')
with open(PDF_PATH, 'rb') as f:
    up = requests.put(f"{bucket}/{PDF_PATH.name}", data=f, headers=HEADERS)
up.raise_for_status()
print('Upload response OK')

# Update metadata
meta = {
    'metadata': {
        'title': 'REBCO HTS Coil Manuscript PDF',
        'upload_type': 'publication',
        'description': 'Manuscript PDF for the REBCO HTS coil optimization paper',
        'creators': [{'name': 'Your name', 'affiliation': 'Your affiliation'}]
    }
}
print('Updating metadata...')
rm = requests.put(f'{BASE_URL}/deposit/depositions/{dep_id}', headers=HEADERS, json=meta)
rm.raise_for_status()

# Publish
print('Publishing...')
pub = requests.post(f'{BASE_URL}/deposit/depositions/{dep_id}/actions/publish', headers=HEADERS)
pub.raise_for_status()
pubj = pub.json()
print('Published DOI:', pubj['doi'])

# Save result
result = {'doi': pubj['doi'], 'url': pubj['links']['record_html'], 'deposition_id': dep_id}
with open('zenodo_pdf_upload_result.json', 'w') as f:
    json.dump(result, f, indent=2)

print('Done')