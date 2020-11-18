
from flask import session, url_for, redirect, jsonify
from functools import wraps
from blueprints.user import user

# ensure_logged_in decorator
def ensure_logged_in(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            # can add flash but idk for rest api so not for now
            return jsonify(
                error = "Need to login first."
            )
        return fn(*args, **kwargs)
    return wrapper