#!/bin/bash
set -e

source venv/bin/activate

export ENV_FOR_DYNACONF=test

python3.11 ./reset_database.py


# pytest --cov --cov-branch --cov-report term-missing -s  -W ignore::DeprecationWarning tests
pytest -k test_server_info_status -s  -W ignore::DeprecationWarning tests
