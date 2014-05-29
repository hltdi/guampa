import os
import sys
import glob

CWD = os.path.dirname(__file__)
# Change working directory so relative paths (and template lookup) work again
os.chdir(CWD)

site_packages = glob.glob("venv/lib/python3*/site-packages")[0]

sys.path.insert(0, site_packages)
sys.path.insert(0, "serverside")
from guampa import app as application
