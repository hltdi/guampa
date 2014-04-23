#!/usr/bin/env python3

"""
This module handles all of the URL dispatching for guampa, mapping from
URLs to the functions that will be called in response.
"""
import json
import os
import re
import urllib.parse

from flask import Flask, request, session, url_for, redirect, render_template,\
                  abort, g, flash, _app_ctx_stack, send_from_directory, jsonify
from flask import Response
from werkzeug import check_password_hash
from werkzeug.utils import secure_filename
import requests

import constants
import db
import dictionary
import model
import segment
import utils


DEBUG = True
SECRET_KEY = 'development key'
app = Flask(__name__)
app.config.from_object(__name__)

## this file is in serverside, but we need one directory up.
myfn = os.path.abspath(__file__)
app.root_path = os.path.dirname(os.path.dirname(myfn)) + os.path.sep
app.debug = DEBUG

app.config.update(
    PERSONA_JS='https://login.persona.org/include.js',
    PERSONA_VERIFIER='https://verifier.login.persona.org/verify',
)

@utils.nocache
@app.route('/')
def index():
    return send_from_directory(app.root_path + 'app', 'index.html')

@app.route('/upload', methods=['GET'])
def upload():
    return send_from_directory(app.root_path + 'app', 'upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file: 
        filename = secure_filename(file.filename)
        
        here = os.path.dirname(os.path.abspath(__file__))
        print(here)
        here = os.path.join(here, "..")
        print(here)
        here = os.path.abspath(here)
        print(here)
        file.save(os.path.join(here, "uploads", filename))
        ### XXX: this redirect should really happen in the js
        newurl = url_for('index') + "#/view_upload/" + filename
        return redirect(newurl)

@app.route('/json/segmented_upload/<filename>')
@utils.json
def tokenize_upload(filename):
    absfn = os.path.join(app.root_path, 'uploads', filename)
    segments = segment.read_doc_segments(absfn)
    numbered_segments = list(enumerate(segments))
    return json.dumps({"segments":numbered_segments})

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
    dictionaries = []

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
            dictionaries.append(dictionary.lookup_sent(s.text))
    out = {'docid': docid,
           'sentences':sent_texts,
           'translations':trans_texts,
           'dictionaries':dictionaries}
    return(json.dumps(out))

@app.route('/json/add_translation', methods=['post'])
@utils.json
@utils.nocache
def add_translation():
    if g.user is None:
        abort(403)
    try:
        d = request.get_json()
        text = d['text']
        sentenceid = d['sentenceid']
        documentid = d['documentid']
        db.save_translation(g.user.id, documentid, sentenceid, text)
    except Exception as inst:
        import traceback
        traceback.print_exc()
        print("it was an exception somewhere")
        abort(500)
    return "OK"

@app.route('/json/add_comment', methods=['post'])
@utils.json
@utils.nocache
def add_comment():
    if g.user is None:
        abort(403)
    try:
        d = request.get_json()
        text = d['text']
        sentenceid = d['sentenceid']
        documentid = d['documentid']
        db.save_comment(g.user.id, documentid, sentenceid, text)
    except Exception as inst:
        import traceback
        traceback.print_exc()
        print("it was an exception somewhere")
        abort(500)
    return "OK"

@app.route('/json/save_document', methods=['post'])
@utils.json
@utils.nocache
def save_document():
    if g.user is None:
        abort(403)
    try:
        d = request.get_json()
        segments = d['segments']
        title = d['title']
        tags_str = d['tags']
        tags = [tag.strip() for tag in tags_str.split(",")]

        assert title.strip(), "title should be non-empty"
        assert len(tags) > 0
        assert all(tag.strip() for tag in tags)

        db.save_document(title, tags, segments)
    except Exception as inst:
        import traceback
        traceback.print_exc()
        print("it was an exception somewhere")
        abort(500)
    return "OK"

def ts_format(timestamp):
    """Given a datetime.datetime object, format it. This could/should probably
    be localized."""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

@app.route('/json/sentencehistory/<sentenceid>')
@utils.json
@utils.nocache
def sentencehistory(sentenceid):
    """All the stuff you need to render the history of a sentence."""
    sentenceid = int(sentenceid)

    sentence = db.get_sentence(sentenceid)
    ## get all the translations and all the comments, sort them by timestamp.
    comments_users = db.things_for_sentence_with_user(sentenceid, model.Comment)
    translations_users = db.things_for_sentence_with_user(sentenceid,
                                                          model.Translation)
    items = []
    for (item, user) in comments_users:
        items.append({'text':item.text,'ts':ts_format(item.timestamp),
                      'username':user.username,'type':'comment'})
    for (item, user) in translations_users:
        items.append({'text':item.text,'ts':ts_format(item.timestamp),
                      'username':user.username, 'type':'translation'})
    out = {'docid': sentence.docid, 'text': sentence.text, 'items':items}
    return(json.dumps(out))

### Dealing with logins; demonstrates sessions and the g global.
### Need to make this work with Angular templating instead.
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = db.get_user(session['user_id'])

@app.route('/json/currentuser')
@utils.json
@utils.nocache
def currentuser():
    """Surface the currently logged in user to the client."""
    if g.user:
        out = {'username': g.user.username, 'fullname':g.user.fullname}
    else:
        out = {'username': None, 'fullname':None}
    return(json.dumps(out))

@app.route('/json/currentemail')
@utils.json
@utils.nocache
def currentemail():
    """Surface the currently logged-in Persona email address to the client."""
    out = {'email': None}
    if 'email' in session:
        out['email'] = session['email']
    return(json.dumps(out))

@app.route('/json/login', methods=['POST'])
@utils.json
@utils.nocache
def json_login():
    """Logs the user in."""
    d = request.get_json()
    username = d['username']
    password = d['password']

    user = db.lookup_username(username)
    success = check_password_hash(user.pwhash, password)
    if user is None:
        error = 'Invalid username'
        abort(403)
    elif not success:
        error = 'Invalid password'
        abort(403)
    else:
        session['user_id'] = user.id
        g.user = user
    return "OK"

@app.route('/json/logout', methods=['GET', 'POST'])
@utils.json
@utils.nocache
def json_logout():
    """Logs the user out."""
    session.clear()
    return json.dumps("OK")

@app.route('/json/create_persona_user', methods=['POST'])
@utils.json
@utils.nocache
def create_persona_user():
    """Create a new PersonaUser and User for the associated email address and
    passed username. Fail out if we can't do that."""

    ### XXX: we should only be doing this iff:
    ### - the user has currently verified their email address via Persona
    ### - but has not logged in with a Guampa account
    ### - and the email address is not yet associated with any Guampa account
    ### - and the account name is valid
    ### - and the account name is not yet in use
    if 'email' in session and g.user is None:
        d = request.get_json()
        username = d['username']
        email = session['email']
        if db.lookup_user_by_email(email):
            print("email address already in use, this should never happen")
            abort(400)
        if (db.lookup_username(username) or
            not constants.USERNAMEPATTERN.match(username)):
            abort(400)
        user = db.create_user_with_email(username, email)
        session['user_id'] = user.id
        g.user = user
        out = {'username': user.username, 'fullname':user.fullname}
        return json.dumps(out)
    abort(403)

## adapted from the flask persona demo
@app.route('/_auth/login', methods=['GET', 'POST'])
@utils.json
@utils.nocache
def login_handler():
    """This is used by the persona js to kick off the verification securely from
    the server side.
    """
    resp = None
    if request.form['assertion']:
        resp = requests.post(app.config['PERSONA_VERIFIER'], data={
            'assertion': request.form['assertion'],
            'audience': request.host_url,
        }, verify=True)
    if resp and resp.ok:
        decoded = resp.content.decode('utf-8')
        verification_data = json.loads(decoded)
        if verification_data['status'] == 'okay':
            email = verification_data['email']
            session['email'] = email
            ## See if there's an existing User with this email address.
            user = db.lookup_user_by_email(email)
            if user:
                print("FOUND USER:", user)
                session['user_id'] = user.id
                g.user = user
                out = {'username': user.username, 'fullname':user.fullname}
                return json.dumps(out)
            ## Otherwise, we're going to have to create one...
            return json.dumps('OK')
    abort(400)
##/adapted from the flask persona demo

if __name__ == '__main__':
    app.run(host='0.0.0.0')
