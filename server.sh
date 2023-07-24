#!/bin/bash
set -e

source venv/bin/activate
source private_env.sh
gunicorn --bind 0.0.0.0:9432 server:app
