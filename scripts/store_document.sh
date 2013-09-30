#!/bin/bash

export PYTHONPATH=$PYTHONPATH:serverside
python3 scripts/store_document.py $*
