#!/bin/bash
source "venv/bin/activate"
echo "Virtual environment started"
python flask_mongo_script/load_mongo.py
echo "Running flask server"
python wsgi.py