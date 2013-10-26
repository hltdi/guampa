#!/bin/bash

virtualenv -p /usr/local/bin/python3 venv
. venv/bin/activate
pip install Flask
pip install sqlalchemy
pip install beautifulsoup4
pip install python-social-auth

pip install https://github.com/nltk/nltk/tarball/master
## make sure we have sentence segmenter models
python3 -m nltk.downloader punkt
