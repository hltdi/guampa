import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import model
from model import Document
from model import Sentence

import constants

engine = create_engine(constants.THEDB)
Session = sessionmaker(bind=engine)

Base = model.Base
Base.metadata.create_all(engine)

def save_file(fn):
    session = Session()
    title = os.path.basename(fn)
    document = Document(title, "bob", "en")
    session.add(document)
    session.commit()

    docid = document.id

    with open(fn) as infile:
        sentences = []
        for line in infile:
            sent = Sentence(line.strip(), docid)
            sentences.append(sent)
    session.add_all(sentences)
    session.commit()
    print("added document:", document)

def main():
    import sys
    fn = sys.argv[1]
    save_file(fn)

if __name__ == "__main__": main()
