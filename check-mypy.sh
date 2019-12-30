#!/bin/bash

## Exit immediately if a command exits with a non-zero status.
set -e

source venv/bin/activate

mypy --ignore-missing-imports --allow-untyped-globals "$@" flexitime main
