#!/bin/bash
set -e

source venv/bin/activate

export ENV_FOR_DYNACONF=test

./reset_test_database.sh


# pytest --cov --cov-branch --cov-report term-missing -s  -W ignore::DeprecationWarning tests
pytest -s  -W ignore::DeprecationWarning tests
