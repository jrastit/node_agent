#!/bin/bash
set -e

source venv/bin/activate
export ENV_FOR_DYNACONF=test

export FLASK_APP=server:app
export FLASK_DEBUG=1
flask run
