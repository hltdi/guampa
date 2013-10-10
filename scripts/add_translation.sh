#!/bin/bash

export PYTHONPATH=$PYTHONPATH:serverside
python3 scripts/add_translation.py "$@"
