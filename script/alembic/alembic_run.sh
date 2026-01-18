#!/bin/bash
cd "$(dirname "$(dirname "$0")")"
cd ..
export ENV_FOR_DYNACONF=alembic
alembic upgrade head
