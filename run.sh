#!/bin/bash

python -m venv .venv
. .venv/Scripts/activate
python -m pip install -e '.[dev]'
aegis doctor
aegis server
pytest