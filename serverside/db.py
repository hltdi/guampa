from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import constants
import model
from model import Document
from model import Sentence
from model import Tag
from model import Translation

from flask import _app_ctx_stack

def get_session():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'db_session'):
        engine = create_engine(constants.THEDB, echo=True)
        Session = sessionmaker(bind=engine)
        top.db_session = Session()
    return top.db_session

def list_documents():
    """Returns a list of all the Document objects."""
    out = []
    session = get_session()
    for instance in session.query(Document).order_by(Document.id): 
        out.append(instance)
    return out

def list_tags():
    """Returns a list of all the Tag objects."""
    session = get_session()
    return session.query(Tag).order_by(Tag.text)

def documents_for_tagname(tagname):
    """Returns a list of all the Documents that pertain to a certain tag."""
    session = get_session()
    tag = session.query(Tag).filter_by(text=tagname).first() 
    if not tag: return out
    return tag.documents

def sentences_for_document(docid):
    """Returns a list of sentences for the given docid."""
    out = []
    session = get_session()
    for instance in session.query(Sentence).\
                            filter(Sentence.docid == docid).\
                            order_by(Sentence.id): 
        out.append(instance)
    return out

def translations_for_document(docid):
    """Returns a list of translations for the given docid."""
    out = []
    session = get_session()
    for instance in session.query(Translation).\
                    filter(Translation.docid == docid).\
                    order_by(Translation.sentenceid, Translation.id.desc()): 
        out.append(instance)
    return out

def translations_for_sentence(sentid):
    """Returns a list of translations for the given sentid."""
    out = []
    session = get_session()
    for instance in session.query(Translation).\
                    filter(Translation.sentenceid == sentid).\
                    order_by(Translation.id.desc()): 
        out.append(instance)
    return out

def latest_translation_for_sentence(sentid):
    """Returns the latest translation for the given sentid."""
    out = []
    session = get_session()
    return session.query(Translation).\
                   filter(Translation.sentenceid == sentid).\
                   order_by(Translation.id.desc()).\
                   first()
