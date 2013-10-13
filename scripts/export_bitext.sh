#!/bin/bash

export PYTHONPATH=$PYTHONPATH:serverside
python3 scripts/export_bitext.py $*
