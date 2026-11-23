#!/usr/bin/env bash
# Install dependencies for CI and review experiments.
set -euo pipefail

python -m pip install -U pip wheel setuptools
python -m pip install -U -r requirements-test.txt
python -m pip install -U -e .
