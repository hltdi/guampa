#!/usr/bin/env python3

import argparse
import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import constants
import model
from model import Sentence
from model import Translation

engine = create_engine(constants.THEDB)
Session = sessionmaker(bind=engine)
session = Session()

Base = model.Base
Base.metadata.create_all(engine)

def sentence_translation_pairs():
    """Generates s,t pairs for sentences that have a translation."""
    have_translation = set()
    for s,t in session.query(Sentence,Translation).\
                         filter(Sentence.id == Translation.sentenceid).\
                         order_by(Sentence.id, Translation.id.desc()):
        if s.id not in have_translation:
            have_translation.add(s.id)
            yield((s,t))

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='WikiExtractor')
    parser.add_argument('--sourcefn', type=str, required=True)
    parser.add_argument('--targetfn', type=str, required=True)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()

    with open(args.sourcefn, "w") as source, open(args.targetfn, "w") as target:
        for (s,t) in sentence_translation_pairs():
            if (not s.text) or (not t.text): continue
            assert "\n" not in s.text
            assert "\n" not in t.text
            print(s.text, file=source)
            print(t.text, file=target)

if __name__ == '__main__':
    main()
