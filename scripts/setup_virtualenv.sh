#!/bin/bash

virtualenv -p /usr/bin/python3.3 venv
. venv/bin/activate
pip install Flask
pip install sqlalchemy
pip install beautifulsoup4

pip install https://github.com/nltk/nltk/tarball/master
## make sure we have sentence segmenter models
python3 -m nltk.downloader punkt
