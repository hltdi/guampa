#!/usr/bin/env python3

from model import *
import constants

from sqlalchemy import create_engine
engine = create_engine(constants.THEDB, echo=False)
Base.metadata.create_all(engine)
