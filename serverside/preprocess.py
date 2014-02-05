#! /usr/bin/python3

import fileinput
import sys

import freeling

## Modify this line to be your FreeLing installation directory
FREELINGDIR = "/usr/local";
DATA = FREELINGDIR+"/share/freeling/";
LANG="es";
freeling.util_init_locale("default");

# create options set for maco analyzer. Default values are Ok, except for data files.
op = freeling.maco_options("es")
op.set_active_modules(0,1,1,1,1,1,1,1,1,1)
op.set_data_files("",DATA+LANG+"/locucions.dat", DATA+LANG+"/quantities.dat", 
                  DATA+LANG+"/afixos.dat", DATA+LANG+"/probabilitats.dat", 
                  DATA+LANG+"/dicc.src", DATA+LANG+"/np.dat",  
                  DATA+"common/punct.dat")

# create analyzers
tk=freeling.tokenizer(DATA+LANG+"/tokenizer.dat")
sp=freeling.splitter(DATA+LANG+"/splitter.dat")
mf=freeling.maco(op)

def preprocess(line):
    l = tk.tokenize(line)
    ls = sp.split(l,0)
    ls = mf.analyze(ls)
    return ls

def get_lemmas(line):
    """Take a string and return all the lemmas in it."""
    ls = preprocess(line)
    lemmas = []
    for s in ls:
        ws = s.get_words()
        for w in ws:
            lemmas.append(w.get_lemma())
    return lemmas
