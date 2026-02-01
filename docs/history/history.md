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
  ---
  I have successfully completed the requested changes:

### Changes Made:

1. **Moved .env file**: Relocated `/home/echo_/Code/asciimath/energy/.env` to .env.

2. **Created .env.example**: Added a new file .env.example with placeholder values:
   ```
   ZOTERO_API_KEY=your_api_key_here
   GROUP_ID=your_group_id_here
   ```

3. **Updated convert_annotations.py**: Modified the script to load configuration from the .env file using `python-dotenv`:
   - Added imports for `os` and `dotenv.load_dotenv()`.
   - Changed hardcoded values to `os.getenv("ZOTERO_API_KEY")` and `os.getenv("GROUP_ID")`.

4. **Updated README.md**: Revised the usage instructions to reflect the new .env file location and requirements.

The script now securely loads sensitive configuration from the local .env file instead of having it hardcoded. Make sure to copy `.env.example` to .env and fill in your actual Zotero API key and group ID before running the script. If `python-dotenv` is not installed, you may need to add it to the dependencies in setup.sh.
<!-- ------ -->
---
The script has been moved to process_papers.py, and the necessary setup has been completed:

- **requirements.txt**: Created with `bibtexparser` (already installed in the energy venv).
- **run_process_papers.sh**: Executable bash script to activate the venv and run the Python script.
- **README.md**: Updated to document the new script.

To run the script, use:

```bash
cd ~/Code/asciimath/energy/scripts
./run_process_papers.sh
```

Or manually:

```bash
cd ~/Code/asciimath/energy
source .venv/bin/activate
python scripts/process_papers.py
```

The script will now work without the `ModuleNotFoundError` since `bibtexparser` is installed in the venv. MinerU is assumed to be available system-wide as before.
<!-- ------ -->
---