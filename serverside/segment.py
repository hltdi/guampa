#!/usr/bin/env python3

import subprocess
import sys
import nltk

SEGMENTER = nltk.data.load("tokenizers/punkt/spanish.pickle")

path_to_tika = "/home/alex/trytika/tika-app-1.5.jar"

def read_file_with_tika(fn):
    out = subprocess.check_output(
              ["java", "-jar", path_to_tika, "-T", fn],
              universal_newlines=True)
    return out

def read_doc_segments(filename):
    """Given a filename, return a list of strings that are segmented
    sentences."""
    tika_exts = [".docx", ".doc", ".pdf"]
    if any(filename.lower().endswith(ext) for ext in tika_exts):
        text = read_file_with_tika(filename)
    else:
        with open(filename, encoding="utf-8", errors="surrogateescape") as infile:
            text = infile.read()
    return segment_string(text)
    
def segment_string(text):
    """Given a large chunk of text, segment it by sentences and return
    that list."""
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    segments = SEGMENTER.tokenize(text) 
    return segments
