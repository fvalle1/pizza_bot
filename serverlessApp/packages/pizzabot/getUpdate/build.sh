#!/bin/bash

set -e

virtualenv venv
source venv/bin/activate
pip install --no-cache-dir requests
deactivate
