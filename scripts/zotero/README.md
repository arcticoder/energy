Zotero helper scripts

Usage:

1. Ensure your API key is stored in the project .env file as `ZOTERO_API_KEY=<your_key>` (already done).
2. Install dependencies (user scope):
   ```bash
   bash scripts/zotero/setup.sh
   ```
3. Run the listing script:
   ```bash
   python3 scripts/zotero/list_zotero.py
   ```

Notes:
- The script tries to use `pyzotero` if installed, and falls back to raw API calls using `requests` if not.
- If your API key has access to specific groups, the key info endpoint should reveal them. If not, set `ZOTERO_GROUP_ID` or `ZOTERO_USERNAME` in the environment for fallback detection.
- The script avoids printing secret values; only collection names and item titles are shown.
