import datetime

import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

## NOTE: Please keep the database design wiki page up to date if you change
## this.
## https://github.com/hltdi/guampa/wiki/DatabaseLayout

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
       return ("<User('%s','%s', '%s')>"
                % (self.name, self.fullname, self.password))

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    user = Column(Integer, ForeignKey('users.id'))
    sl = Column(String) ## string?
    tags = relationship("Tag", secondary=lambda:documenttag_table)

    def __init__(self, title, user, sl):
        self.title = title
        self.user = user 
        self.sl = sl

    def __repr__(self):
       return ("<Document(%d, '%s', '%s', '%s')>"
                % (self.id, self.title, self.user, self.sl))

class Sentence(Base):
    __tablename__ = 'sentences'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    docid = Column(Integer, ForeignKey('documents.id'))

    def __init__(self, text, docid):
        self.text = text
        self.docid = docid

    def __repr__(self):
       return ("<Sentence(%d, '%s')>" % (self.id, self.text))

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    documents = relationship("Document", secondary=lambda:documenttag_table)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
       return ("<Tag(%d, '%s')>" % (self.id, self.text))

class Translation(Base):
    __tablename__ = 'translations'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    docid = Column(Integer, ForeignKey('documents.id'))
    sentenceid = Column(Integer, ForeignKey('sentences.id'))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, text, docid, sentenceid):
        self.text = text
        self.docid = docid
        self.sentenceid = sentenceid

    def __repr__(self):
       return ("<Translation(%d, '%s')>" % (self.id, self.text))

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    docid = Column(Integer, ForeignKey('documents.id'))
    sentenceid = Column(Integer, ForeignKey('sentences.id'))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, text, docid, sentenceid):
        self.text = text
        self.docid = docid
        self.sentenceid = sentenceid

    def __repr__(self):
       return ("<Comment(%d, '%s')>" % (self.id, self.text))

### relationships.

documenttag_table = Table('documenttag', Base.metadata,
    Column('docid', Integer, ForeignKey('documents.id')),
    Column('tagid', Integer, ForeignKey('tags.id'))
)
