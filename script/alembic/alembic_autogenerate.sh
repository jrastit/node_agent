#!/bin/bash
cd "$(dirname "$(dirname "$0")")"
echo ${PWD}
cd ..
export ENV_FOR_DYNACONF=alembic
alembic revision --autogenerate -m "init"

