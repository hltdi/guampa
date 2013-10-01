from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import constants
import model
from model import Document

engine = create_engine(constants.THEDB, echo=True)
Session = sessionmaker(bind=engine)

def list_documents():
    """Returns a list of document ids."""
    out = []

    session = Session()
    for instance in session.query(Document).order_by(Document.id): 
        out.append(instance.id)
    return out
