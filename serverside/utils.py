from flask import make_response
from functools import update_wrapper

def nocache(f):
    def new_func(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp
    return update_wrapper(new_func, f)

def json(f):
    def new_func(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.mimetype = 'application/json'
        return resp
    return update_wrapper(new_func, f)
