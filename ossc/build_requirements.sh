#!/bin/bash

# Script to approximate venv on RA for SICSS. Run on the snellius login node.
# assume we don't need beautifulsoup4, QtPy, fastapi


declare OSSC_requirements="ossc/requirements_ossc.txt"
declare RA_requirements="ossc/environment0000.txt"

echo "loading modules" 
source ossc/modules.sh

echo "installing from pip"
python -m venv .venv 
source .venv/bin/activate
pip install -r ossc/pip_requirements.txt

pip freeze > "$OSSC_requirements" 

python ossc/translate.py --from "$OSSC_requirements" --to "$RA_requirements" 
python ossc/compare_requirements.py --ossc_src "$OSSC_requirements"

deactivate 
rm -rf .venv

