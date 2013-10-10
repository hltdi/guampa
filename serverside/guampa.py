#!/usr/bin/env python3

"""
This module handles all of the URL dispatching for guampa, mapping from
URLs to the functions that will be called in response.
"""
import json
import os

from flask import Flask, request, session, url_for, redirect, render_template,\
                  abort, g, flash, _app_ctx_stack, send_from_directory, jsonify
from werkzeug import check_password_hash, generate_password_hash

import db
import utils

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

@app.route('/json/documents')
@utils.json
@utils.nocache
def documents():
    docs = db.list_documents()
    out = {'documents': [{'title': doc.title, 'id':doc.id} for doc in docs]}
    print(out)
    return(json.dumps(out))

@app.route('/json/tags')
@utils.json
@utils.nocache
def tags():
    tags = db.list_tags()
    out = {'tags': [tag.text for tag in tags]}
    print(out)
    return(json.dumps(out))

@app.route('/json/documents/<tagname>')
@utils.json
@utils.nocache
def documents_for_tag(tagname):
    docs = db.documents_for_tagname(tagname)
    out = {'documents': [{'title': doc.title, 'id':doc.id} for doc in docs]}
    print(out)
    return(json.dumps(out))

# XXX: just to demo; make sure to take this out later.
@app.route('/document/<docid>')
def document(docid):
    docid = int(docid)
    sentences = db.sentences_for_document(docid)
    translations = db.translations_for_document(docid)
    out = "<html><body>"
    out += "<h1>sentences</h1>\n"
    out += "<ul>\n"
    for sent in sentences:
        out += ("<li>%d: %s</li>\n") % (sent.id, sent.text)
    out += "</ul>"
    out += "<h1>translations</h1>\n"
    out += "<ul>\n"
    for translation in translations:
        out += ("<li>%d: %s</li>\n") % (translation.id, translation.text)
    out += "</ul>"
    out += "</body></html>"
    return out

if __name__ == '__main__':
    app.run(host='0.0.0.0')
