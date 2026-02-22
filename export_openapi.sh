#!/bin/bash
set -e

source venv/bin/activate
python3 ./export_openapi.py "$@"
