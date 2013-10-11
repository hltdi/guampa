#!/usr/bin/env python3

"""
Script to trangle over a directory full of wikipedia dumps as produced by
WikiExtractor.py and add them to the database.
"""

import glob
import os

import constants
import model
import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from model import Document
from model import Sentence
from model import Tag

engine = create_engine(constants.THEDB)
Session = sessionmaker(bind=engine)
Base = model.Base
Base.metadata.create_all(engine)

def save_document(title, session):
    """Create a new document; return it."""
    ## XXX(alexr): need to handle source languages...
    document = Document(title, "bob", "en")
    session.add(document)
    session.commit()
    print("added document:", document)
    return document

def get_tag(tagname, session):
    """Return or create a Tag object for this tag name."""
    tag = session.query(Tag).filter_by(text=tagname).first() 
    if not tag:
        tag = Tag(tagname)
        session.add(tag)
        session.commit()
    return tag

def iterate_through_file(fn):
    docid = None
    session = Session()
    with open(fn) as infile:
        for line in infile:
            line = line.strip()
            if line.startswith("###"):
                splitted = line[3:].split("|||")
                title = splitted[0]
                ## save document, get docid.
                document = save_document(title, session)
                docid = document.id
                tagnames = splitted[1:]
                ## tag that document with these tags.
                for tagname in tagnames:
                    tag = get_tag(tagname, session)
                    document.tags.append(tag)
                continue
            ## Otherwise, we have a sentence.
            assert docid, "We're not currently in a document??"
            sent = Sentence(line, docid)
            session.add(sent)
        session.commit()

def main():
    import sys
    document_dir = sys.argv[1]
    fns = sorted(glob.glob("{0}/wiki*".format(document_dir)))
    print("going through {0} files, each with many articles.".format(len(fns)))
    for fn in fns:
        iterate_through_file(fn)

if __name__ == "__main__": main()
