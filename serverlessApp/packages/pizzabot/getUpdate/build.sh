#!/bin/bash

set -e

python3 -m virtualenv venv
source venv/bin/activate
python3 -m pip install --no-cache-dir requests
deactivate
