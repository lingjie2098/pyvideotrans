#!/bin/bash

# see https://pyvideotrans.com/mac.html and https://github.com/jianchang512/pyvideotrans
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
echo "=============$CURRENT_DIR============="
cd "$CURRENT_DIR"

source ./venv/bin/activate
python3.10 sp.py