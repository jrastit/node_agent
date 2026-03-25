#!/usr/bin/env bash
set -euo pipefail

# Resolve repository root from this script location.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

export ENV_FOR_DYNACONF=test

if [[ -x "${REPO_ROOT}/venv/bin/python" ]]; then
	PYTHON_BIN="${REPO_ROOT}/venv/bin/python"
else
	PYTHON_BIN="python3.12"
fi

if [[ -d "${REPO_ROOT}/venv/bin" ]]; then
	export PATH="${REPO_ROOT}/venv/bin:${PATH}"
fi

# Keep the same DB reset/migration workflow as test.sh before running pytest.
"${PYTHON_BIN}" ./reset_database.py
./script/alembic/alembic_run.sh

exec "${PYTHON_BIN}" -m pytest "$@"
