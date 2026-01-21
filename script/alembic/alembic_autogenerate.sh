#!/bin/bash
cd "$(dirname "$(dirname "$0")")"
echo ${PWD}
cd ..
export ENV_FOR_DYNACONF=alembic
MSG=${1:-"init"}
REV=${2:-""}
if [ -n "$REV" ]; then
    alembic revision --autogenerate -m "$MSG" --rev-id "$REV"
    exit 0
fi
alembic revision --autogenerate -m "$MSG"

