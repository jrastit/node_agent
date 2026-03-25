set -e
source venv/bin/activate

# Keep pip below 26 because current pip-tools is not compatible with pip 26 APIs.
pip install --upgrade "pip<26" "pip-tools"

pip-compile --output-file=requirements.txt pyproject.toml --resolver=backtracking
pip-compile --output-file=requirements_test.txt pyproject.toml --extra=test --resolver=backtracking
