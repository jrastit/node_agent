#!/bin/bash
set -e

source venv/bin/activate

export ENV_FOR_DYNACONF=server

python3.12 ./reset_database.py
