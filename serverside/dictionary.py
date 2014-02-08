#!/usr/bin/env python3

import functools
import os

#import preprocess

HERE = os.path.dirname(os.path.realpath(__file__))
DICTIONARYFN = HERE + "/avanee-es-gn-palabras.txt"

@functools.lru_cache(maxsize=10000)
def load_dictionary(fn=DICTIONARYFN):
    d = {}
    with open(DICTIONARYFN, encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            es, gn = line.split("|||")
            es_words = es.split(",")
            for es_word in es_words:
                es_word = es_word.strip()
                d[es_word] = gn.strip()
    return d

def lookup_sent(text):
    included = set()
    d = load_dictionary()

    ## XXX(alexr): these are not really lemmas
    lemmas = text.strip().lower().split()

    ## TODO(alexr): turn freeling back on!!
    ##lemmas = preprocess.get_lemmas(text)
    lookups = []
    for lemma in lemmas:
        if lemma in d and lemma not in included:
            lookups.append("{0} => {1}".format(lemma, d[lemma]))
            included.add(lemma)
    out = "; ".join(lookups)
    return out

def main():
    s = input("> ")
    print(lookup_sent(s))

if __name__ == "__main__": main()
