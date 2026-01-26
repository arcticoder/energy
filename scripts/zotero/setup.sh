#!/usr/bin/env bash
set -euo pipefail
REQ_FILE="$(dirname "$0")/requirements.txt"
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found" >&2
  exit 1
fi
python3 -m pip install --user -r "$REQ_FILE"
echo "Installed Python packages from $REQ_FILE (user scope)."
