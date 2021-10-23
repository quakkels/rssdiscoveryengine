#!/bin/sh
export PYTHONUNBUFFERED=1
export FLASK_APP=rssdiscoveryengine_app

. .venv/bin/activate
python -m flask run
