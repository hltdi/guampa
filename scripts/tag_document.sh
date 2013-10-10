#!/bin/bash

export PYTHONPATH=$PYTHONPATH:serverside
python3 scripts/tag_document.py "$@"
