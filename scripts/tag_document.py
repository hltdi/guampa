import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import model
from model import Document
from model import Tag

import constants

engine = create_engine(constants.THEDB)
Session = sessionmaker(bind=engine)

Base = model.Base
Base.metadata.create_all(engine)

def tag_docid(docid, tagname):
    """Get the document by number and the tag by name. Optionally create the tag
    if it doesn't exist yet.
    """
    session = Session()

    document = session.query(Document).filter_by(id=docid).first() 
    assert document

    tag = session.query(Tag).filter_by(text=tagname).first() 
    if not tag:
        tag = Tag(tagname)
        session.add(tag)
    document.tags.append(tag)
    print("document tags:", document.tags)
    print("tag documents:", tag.documents)
    session.commit()

def main():
    import sys
    docid = int(sys.argv[1])
    tagname = sys.argv[2]
    tag_docid(docid, tagname)

if __name__ == "__main__": main()
