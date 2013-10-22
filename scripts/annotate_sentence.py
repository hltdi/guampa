#!/usr/bin/env python3
import argparse
import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import constants
import model
from model import Comment
from model import Document
from model import Sentence
from model import Translation
from model import User

engine = create_engine(constants.THEDB)
Session = sessionmaker(bind=engine)

Base = model.Base
Base.metadata.create_all(engine)

def save_annotation(klass, args):
    """Add a Translation or a Comment for the specified sentence."""
    session = Session()

    username = args.username
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        print("username not found: {0}".format(username))
        return

    text = args.text
    docid = args.docid
    sentenceid = args.sentenceid

    sentence = session.query(Sentence).get(sentenceid)
    assert sentence.docid == docid

    annotation = klass(user.id, text, docid, sentenceid)
    session.add(annotation)
    session.commit()

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='annotate_sentence')
    parser.add_argument('--docid', type=int, required=True)
    parser.add_argument('--sentenceid', type=int, required=True)
    parser.add_argument('--username', type=str, required=True)
    parser.add_argument('--text', type=str, required=True)
    parser.add_argument('--comment',dest='isComment',action='store_true')
    parser.add_argument('--translation',dest='isComment',action='store_false')
    parser.set_defaults(isComment=False)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()

    klass = Comment if args.isComment else Translation
    save_annotation(klass, args)

if __name__ == "__main__": main()
