import os
import sys

CWD = os.path.dirname(__file__)
# Change working directory so relative paths (and template lookup) work again
os.chdir(CWD)

sys.path.insert(0, "venv/lib/python3.3/site-packages")
sys.path.insert(0, "serverside")
from guampa import app as application
