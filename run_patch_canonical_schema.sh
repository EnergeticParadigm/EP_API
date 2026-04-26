#!/bin/zsh
set -euo pipefail

cd "/Users/wesleyshu/Library/CloudStorage/OneDrive-Personal/Energetic Paradigm/EP Model/Building EP on GPT/EPRA_API_Wrapper_v2"

python3 tools/patch_canonical_schema.py
python3 -m py_compile app/services/epra.py
grep -n "canonical_setup" -A12 -B4 app/services/epra.py
