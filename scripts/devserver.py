#!/usr/bin/env python3

import bottle

## Load up all the functions that return pages.
from urldispatch import *

## Start the development server with debugging help on and caching off.
bottle.debug(True)
bottle.run(host='localhost', port=8084, reloader=True)
