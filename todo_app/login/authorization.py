from functools import wraps
from flask import abort, current_app
from flask_login import current_user

READER = 'READER'
WRITER = 'WRITER'


def writer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user_can_write():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def current_user_can_write():
    return current_app.config['LOGIN_DISABLED'] or current_user.can_write
