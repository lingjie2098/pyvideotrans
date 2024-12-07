#!/bin/bash

# see https://pyvideotrans.com/mac.html and https://github.com/jianchang512/pyvideotrans

# Preparatory work
# Install Homebrew

brew install python@3.10
brew install libsndfile
brew install ffmpeg

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
echo "=============$CURRENT_DIR============="
cd "$CURRENT_DIR"

python3.10 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com