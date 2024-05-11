#!/bin/sh
set -eux
rm -rf .venv
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements_dev.txt
