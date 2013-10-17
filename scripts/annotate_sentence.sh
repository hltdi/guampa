#!/bin/bash

export PYTHONPATH=$PYTHONPATH:serverside
python3 scripts/annotate_sentence.py "$@"
