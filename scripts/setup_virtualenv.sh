#!/bin/bash

virtualenv -p /usr/bin/python3.3 venv
. venv/bin/activate
pip install Flask
pip install sqlalchemy
