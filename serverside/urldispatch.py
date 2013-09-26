#!/usr/bin/env python3

from bottle import error
from bottle import request
from bottle import response
from bottle import route
from bottle import static_file

import os
import json

"""
This module handles all of the URL dispatching for guampa, mapping from
URLs to the functions that will be called in response.
"""

@route('/')
def index():
    return static_file('index.html', root='app')

@route('/partials/<fn>')
def partials(fn):
    return static_file(fn, root='app/partials')

@route('/css/<fn>')
def css(fn):
    return static_file(fn, root='app/css')

@route('/js/<fn>')
def js(fn):
    return static_file(fn, root='app/js')

@route('/img/<fn>')
def img(fn):
    return static_file(fn, root='app/img')

@route('/lib/<fn>')
def lib(fn):
    return static_file(fn, root='app/lib')

@error(404)
def error404(error):
    return ('Nothing here, sorry: ' + str(error))
