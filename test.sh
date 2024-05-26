#!/bin/bash
set -e

source venv/bin/activate

export ENV_FOR_DYNACONF=test
export SETTINGS_FILE_FOR_DYNACONF="settings/settings.yaml"

python3.11 ./reset_database.py


# pytest --cov --cov-branch --cov-report term-missing -s  -W ignore::DeprecationWarning tests
pytest -s  -W ignore::DeprecationWarning tests
