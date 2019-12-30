#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

black --exclude "(/migrations|/management)" flexitime main