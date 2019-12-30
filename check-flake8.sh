#!/bin/bash

set -e

source venv/bin/activate

flake8 --select=F --ignore=F401,F403,F405,W503 flexitime main


# Old ignore.
# --ignore F401,F403,F405,W503
# See here for some error codes.
# flake8.pycqa.org/en/3.1.1/user/error-codes.html