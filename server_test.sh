#!/bin/bash
set -e

source venv/bin/activate
export ENV_FOR_DYNACONF=test

uvicorn server:app --host 127.0.0.1 --port 8887 --reload
