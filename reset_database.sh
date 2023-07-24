#!/bin/bash
set -e

source venv/bin/activate
source private_env.sh

echo RESET database

export SQLALCHEMY_SILENCE_UBER_WARNING=1
python3 reset_database.py
