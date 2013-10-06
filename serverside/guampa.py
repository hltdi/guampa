#!/usr/bin/env python3

"""
This module handles all of the URL dispatching for guampa, mapping from
URLs to the functions that will be called in response.
"""
import os
from flask import Flask, request, session, url_for, redirect, render_template,\
                  abort, g, flash, _app_ctx_stack, send_from_directory
from werkzeug import check_password_hash, generate_password_hash

PER_PAGE = 30
DEBUG = True

app = Flask(__name__)

## this file is in serverside, but we need one directory up.
myfn = os.path.abspath(__file__)
app.root_path = os.path.dirname(os.path.dirname(myfn)) + os.path.sep
app.debug = DEBUG

@app.route('/')
def index():
    return send_from_directory(app.root_path + 'app', 'index.html')

@app.route('/partials/<fn>')
def partials(fn):
    return send_from_directory(app.root_path + 'app/partials', fn)

@app.route('/css/<fn>')
def css(fn):
    return send_from_directory(app.root_path + 'app/css', fn)

@app.route('/js/<fn>')
def js(fn):
    return send_from_directory(app.root_path + 'app/js', fn)

@app.route('/img/<fn>')
def img(fn):
    return send_from_directory(app.root_path + 'app/img', fn)

@app.route('/lib/<fn>')
def lib(fn):
    return send_from_directory(app.root_path + 'app/lib', fn)

if __name__ == '__main__':
    app.run()
