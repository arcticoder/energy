#!/usr/bin/env python3
"""List Zotero personal and group collections and their items.
Reads ZOTERO_API_KEY from the repo .env file at the project root.
"""
from pathlib import Path
import os
import sys
import json
import re

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

try:
    import requests
except Exception as e:
    print("Missing dependency 'requests'. Run scripts/zotero/setup.sh or pip install -r scripts/zotero/requirements.txt", file=sys.stderr)
    raise

try:
    from pyzotero import zotero
except Exception:
    zotero = None

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"

if load_dotenv:
    load_dotenv(dotenv_path=str(ENV_PATH))
else:
    # fallback simple .env loader
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())

API_KEY = os.getenv('ZOTERO_API_KEY')
if not API_KEY:
    print(f"ERROR: ZOTERO_API_KEY not found in {ENV_PATH}", file=sys.stderr)
    sys.exit(1)

HEADERS = {'Zotero-API-Key': API_KEY, 'Accept': 'application/json'}


def get_key_info(api_key):
    url = f"https://api.zotero.org/keys/{api_key}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
    except Exception as e:
        print(f"Failed to reach Zotero API: {e}", file=sys.stderr)
        return None
    if r.status_code != 200:
        print(f"Key info endpoint returned {r.status_code}. Response: {r.text[:400]}")
        return None
    try:
        return r.json()
    except Exception:
        print(f"Non-JSON response from key info endpoint. Raw response (truncated):\n{r.text[:1000]}")
        return None


def get_userid_from_profile(username):
    url = f"https://www.zotero.org/{username}"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            return None
        # Try to find numeric user id occurrences
        m = re.search(r"/(users|people)/(\d+)", r.text)
        if m:
            return m.group(2)
        m2 = re.search(r"data-userid\s*=\s*\"(\d+)\"", r.text)
        if m2:
            return m2.group(1)
    except Exception:
        return None
    return None


def list_collections_for_library(lib_id, lib_type, api_key):
    print(f"\n--- {lib_type.upper()} library {lib_id} collections ---")
    if zotero is None:
        print("pyzotero not installed; falling back to raw API calls for collections/items")
        # Raw API: GET https://api.zotero.org/{lib_type}s/{library_id}/collections
        url = f"https://api.zotero.org/{lib_type}s/{lib_id}/collections"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print(f"Failed to fetch collections: {r.status_code} {r.text}")
            return
        try:
            coll = r.json()
        except Exception:
            print("Failed to parse collections response as JSON")
            return
        for c in coll:
            name = c.get('data', {}).get('name', '<no name>')
            key = c.get('data', {}).get('key')
            print(f"Collection: {name} (key={key})")
            # list items in collection
            items_url = f"https://api.zotero.org/{lib_type}s/{lib_id}/collections/{key}/items"
            ri = requests.get(items_url, headers=HEADERS)
            if ri.status_code != 200:
                print(f"  Failed to fetch items: {ri.status_code}")
                continue
            try:
                items = ri.json()
            except Exception:
                print(f"  Failed to parse items response")
                continue
            for it in items[:10]:
                title = it.get('data', {}).get('title') or it.get('data', {}).get('title', '<no title>')
                print(f"  - {title}")
    else:
        try:
            z = zotero.Zotero(lib_id, lib_type, api_key)
            collections = z.collections()
        except Exception as e:
            print(f"pyzotero failed for {lib_type} {lib_id}: {e}")
            return
        if not collections:
            print("No collections found.")
            return
        for c in collections:
            name = c.get('data', {}).get('name', '<no name>')
            key = c.get('data', {}).get('key')
            print(f"Collection: {name} (key={key})")
            try:
                items = z.collection_items(key, limit=50)
            except Exception as e:
                print(f"  Failed to fetch items via pyzotero: {e}")
                continue
            for it in items:
                title = it.get('data', {}).get('title') or '<no title>'
                print(f"  - {title}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='List Zotero user and group collections')
    parser.add_argument('--group', '-g', help='Group library ID to list (e.g. 6396936)', type=str)
    parser.add_argument('--username', '-u', help='Zotero username to try to resolve to a user id (default from ZOTERO_USERNAME or ryan.sherrington)', type=str)
    parser.add_argument('--limit', '-l', help='Limit items per collection (default 50)', type=int, default=50)

    args = parser.parse_args()

    print("Listing libraries accessible with the provided API key (no secrets will be printed).")
    key_info = get_key_info(API_KEY)
    user_id = None
    groups = []
    if key_info:
        # Try to extract user id and groups if present
        if isinstance(key_info, dict):
            user_id = key_info.get('userID') or key_info.get('userId') or key_info.get('user')
            # groups might be in key_info['groups'] or in other fields
            g = key_info.get('groups') or key_info.get('groupIDs') or key_info.get('groupsWithAccess')
            if isinstance(g, list):
                groups = g

    # If no user_id found, try to get it by scraping known username
    if not user_id:
        username = args.username or os.getenv('ZOTERO_USERNAME') or 'ryan.sherrington'
        userid_from_profile = get_userid_from_profile(username)
        if userid_from_profile:
            user_id = userid_from_profile

    # Report what we will list
    if user_id:
        print(f"Found user id: {user_id}")
        list_collections_for_library(user_id, 'user', API_KEY)
    else:
        print("No user id discovered for personal library; skipping personal library listing.")

    # explicit group from arg or env
    env_group = os.getenv('ZOTERO_GROUP_ID')
    if args.group:
        groups.append(args.group)
    elif env_group:
        groups.append(env_group)

    # If groups available via key_info or arguments, list them
    if groups:
        for g in groups:
            print(f"\nDiscovered group: {g}")
            list_collections_for_library(g, 'group', API_KEY)
    else:
        print('\nNo groups discovered via key info or arguments.\nIf you expect group access, set ZOTERO_GROUP_ID or pass --group <id> and try again.')

