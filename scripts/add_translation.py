import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import model
from model import Document
from model import Sentence
from model import Translation

import constants

engine = create_engine(constants.THEDB)
Session = sessionmaker(bind=engine)

Base = model.Base
Base.metadata.create_all(engine)

def save_translation(docid, sentenceid, text):
    session = Session()
    translation = Translation(text, docid, sentenceid)

    session.add(translation)
    session.commit()

def main():
    import sys
    docid = int(sys.argv[1])
    sentenceid = int(sys.argv[2])
    text = sys.argv[3]
    save_translation(docid, sentenceid, text)

if __name__ == "__main__": main()
