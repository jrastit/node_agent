#!/bin/bash
set -e

virtualenv -p python3.11 venv

source venv/bin/activate

pip3 install -r requirements.txt



