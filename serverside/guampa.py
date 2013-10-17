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
import urllib.parse

DEBUG = True
app = Flask(__name__)

## this file is in serverside, but we need one directory up.
myfn = os.path.abspath(__file__)
app.root_path = os.path.dirname(os.path.dirname(myfn)) + os.path.sep
app.debug = DEBUG

@utils.nocache
@app.route('/')
def index():
    return send_from_directory(app.root_path + 'app', 'index.html')

@app.route('/partials/<fn>')
def partials(fn):
    return send_from_directory(app.root_path + 'app/partials', fn)

@app.route('/css/<fn>')
def css(fn):
    return send_from_directory(app.root_path + 'app/css', fn)

@utils.nocache
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
    return(json.dumps(out))

@app.route('/json/tags')
@utils.json
@utils.nocache
def tags():
    tags = db.list_tags()
    out = {'tags': [tag.text for tag in tags]}
    return(json.dumps(out))

@app.route('/json/documents/<path:tagname>')
@utils.json
@utils.nocache
def documents_for_tag(tagname):
    tagname = urllib.parse.unquote(tagname)
    docs = db.documents_for_tagname(tagname)
    out = {'documents': [{'title': doc.title, 'id':doc.id} for doc in docs]}
    return(json.dumps(out))

@app.route('/json/document/<docid>')
@utils.json
@utils.nocache
def document(docid):
    """All the stuff you need to render a document in the editing interface."""
    docid = int(docid)

    sent_texts = []
    trans_texts = []

    ## sentence ids for which we've seen a translation
    have_translation = set()
    for (s,t) in db.sentences_with_translations_for_document(docid):
        if s.id in have_translation:
            continue
        else:
            sent_texts.append(s.text)
            if t:
                have_translation.add(s.id)
            translation_text = t.text if t else None
            trans_texts.append({'text':translation_text,
                                'sentenceid':s.id,
                                'docid':docid})
    out = {'docid': docid, 'sentences':sent_texts, 'translations':trans_texts}
    return(json.dumps(out))

@app.route('/json/add_translation', methods=['post'])
@utils.json
@utils.nocache
def add_translation():
    try:
        d = request.get_json()
        text = d['text']
        sentenceid = d['sentenceid']
        documentid = d['documentid']
        db.save_translation(documentid, sentenceid, text)
    except Exception as inst:
        import traceback
        traceback.print_exc()
        print("it was an exception somewhere")
        abort(500)
    return "OK"

@app.route('/json/sentencehistory/<sentenceid>')
@utils.json
@utils.nocache
def sentencehistory(sentenceid):
    """All the stuff you need to render the history of a sentence."""
    sentenceid = int(sentenceid)

    sentence = db.get_sentence(sentenceid)
    ## get all the translations and all the comments, sort them by timestamp.
    comments = db.comments_for_sentence(sentenceid)
    translations = db.translations_for_sentence(sentenceid)
    items = []
    for item in comments:
        items.append({'text':item.text,'ts':str(item.timestamp),'type':'comment'})
    for item in translations:
        items.append({'text':item.text,'ts':str(item.timestamp),'type':'translation'})
    out = {'text': sentence.text, 'items':items}
    return(json.dumps(out))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
