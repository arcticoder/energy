## Zotero access — confirmed ✅

**What I did (quick):**
- Created scripts under **zotero**:
  - requirements.txt, `setup.sh`, `list_zotero.py`, README.md 🔧
- Installed dependencies: **pyzotero**, **python-dotenv**, **requests** (via `bash scripts/zotero/setup.sh`) ✅
- Ran the listing script and successfully accessed:
  - Personal library (user id **9318423**) — collections and items listed
  - Group library **6396936** (your Dawson group) — collections and items listed

> Important: the script reads your API key from .env (you already set `ZOTERO_API_KEY`). It does **not** print secrets.

---

## How to use it 💡
- Install deps:
  - `bash scripts/zotero/setup.sh`
- List your personal library:
  - `python3 scripts/zotero/list_zotero.py`
- List a group library:
  - `python3 list_zotero.py --group 6396936`
- Other options:
  - `--username <zotero_username>` or set `ZOTERO_USERNAME` in the environment
  - set `ZOTERO_GROUP_ID` env var to target a group persistently
  <!-- ------ -->