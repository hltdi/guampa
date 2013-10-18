#!/usr/bin/env python3
import argparse
import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import model
from model import Comment
from model import Document
from model import Sentence
from model import Translation

import constants

engine = create_engine(constants.THEDB)
Session = sessionmaker(bind=engine)

Base = model.Base
Base.metadata.create_all(engine)

def save_annotation(klass, docid, sentenceid, text):
    """Add a Translation or a Comment for the specified sentence."""
    session = Session()
    sentence = session.query(Sentence).get(sentenceid)
    assert sentence.docid == docid

    annotation = klass(text, docid, sentenceid)
    session.add(annotation)
    session.commit()

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='annotate_sentence')
    parser.add_argument('--docid', type=int, required=True)
    parser.add_argument('--sentenceid', type=int, required=True)
    parser.add_argument('--text', type=str, required=True)
    parser.add_argument('--comment',dest='isComment',action='store_true')
    parser.add_argument('--translation',dest='isComment',action='store_false')
    parser.set_defaults(isComment=False)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()

    klass = Comment if args.isComment else Translation
    save_annotation(klass, args.docid, args.sentenceid, args.text)

if __name__ == "__main__": main()
