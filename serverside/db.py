from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import constants
import model
from model import Document
from model import Sentence
from model import Translation

engine = create_engine(constants.THEDB, echo=True)
Session = sessionmaker(bind=engine)

def list_documents():
    """Returns a list of document ids."""
    out = []

    session = Session()
    for instance in session.query(Document).order_by(Document.id): 
        out.append(instance.id)
    return out

def sentences_for_document(docid):
    """Returns a list of sentences for the given docid."""
    out = []
    session = Session()
    for instance in session.query(Sentence).\
                            filter(Sentence.docid == docid).\
                            order_by(Sentence.id): 
        out.append(instance)
    return out

def translations_for_document(docid):
    """Returns a list of translations for the given docid."""
    out = []
    session = Session()
    for instance in session.query(Translation).\
                    filter(Translation.docid == docid).\
                    order_by(Translation.sentenceid, Translation.id.desc()): 
        out.append(instance)
    return out
