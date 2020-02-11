#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

source venv/bin/activate

black --check \
   --exclude "(/migrations|/management)" \
   flexitime main