#!/usr/bin/env python3
import argparse
import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug import generate_password_hash

import constants
import model
import db
from model import User

engine = create_engine(constants.THEDB)
Session = sessionmaker(bind=engine)

Base = model.Base
Base.metadata.create_all(engine)

def save_user(username, fullname, password):
    session = Session()
    user = session.query(User).filter(User.username == username).first()
    if user is not None:
        print("username already exists: {0}".format(username))
        print(user)
        return
    pwhash = generate_password_hash(password)
    user = User(username, fullname, pwhash)
    session.add(user)
    session.commit()
    print("created:", user)

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='add_user')
    parser.add_argument('--username', type=str, required=True)
    parser.add_argument('--fullname', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()
    save_user(args.username, args.fullname, args.password)

if __name__ == "__main__": main()
