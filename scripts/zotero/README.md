Zotero helper scripts

Usage:

1. Ensure your API key is stored in the scripts/zotero/.env file as `ZOTERO_API_KEY=<your_key>` and `GROUP_ID=<your_group_id>` (copy from .env.example and fill in your values).
2. Install dependencies (user scope):
   ```bash
   bash scripts/zotero/setup.sh
   ```
3. Run the listing script:
   ```bash
   python3 scripts/zotero/list_zotero.py
   ```
4. Run the annotation conversion script:
   ```bash
   python3 scripts/zotero/convert_annotations.py
   ```
   This script converts Markdown annotations from `coherence_gravity_coupling-bib-annotations.md` into Zotero HTML notes with proper math rendering. It generates and executes curl commands to update existing Zotero notes via the API.

   Prerequisites:
   - The source file must be at `/home/echo_/Code/asciimath/coherence-gravity-coupling/papers/coherence_gravity_coupling-bib-annotations.md`
   - Existing Zotero notes attached to the mapped items (currently jacobson1995 and birrell2012)
   - API key with write access to the group

Notes:
- The script tries to use `pyzotero` if installed, and falls back to raw API calls using `requests` if not.
- If your API key has access to specific groups, the key info endpoint should reveal them. If not, set `ZOTERO_GROUP_ID` or `ZOTERO_USERNAME` in the environment for fallback detection.
- The script avoids printing secret values; only collection names and item titles are shown.
- The conversion script uses hardcoded paths and mappings; edit the script for new annotations or paths.
