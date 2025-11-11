set -e
source venv/bin/activate

pip install --upgrade "pip<25.3"
pip show pip-tools >/dev/null 2>&1 || pip install pip-tools

pip-compile --output-file=requirements.txt pyproject.toml --resolver=backtracking
pip-compile --output-file=requirements_test.txt pyproject.toml --extra=test --resolver=backtracking
