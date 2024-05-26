set -e
source venv/bin/activate

pip-compile --output-file=requirements.txt requirements.in --resolver=backtracking
pip-compile --output-file=requirements_test.txt requirements_test.in --resolver=backtracking
