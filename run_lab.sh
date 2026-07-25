#!/usr/bin/env bash
# run_lab.sh — python-itertools-label-grouping-lab
set -euo pipefail
cd "$(dirname "$0")"

# Find a usable Python (prefer python3, fall back to python)
if command -v python3 >/dev/null 2>&1; then
    PY=python3
elif command -v python >/dev/null 2>&1; then
    PY=python
else
    echo "Error: python3 / python not found in PATH" >&2
    exit 1
fi

echo "Using: $("$PY" --version 2>&1)"
echo
echo "=== run_lab.py ==="
"$PY" run_lab.py
echo
echo "=== unittest test_lab ==="
"$PY" -m unittest test_lab -v
