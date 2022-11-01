from functools import wraps
from flask import abort, current_app
from flask_login import current_user

from helper.current_user_id import get_current_user_id

READER = 'READER'
WRITER = 'WRITER'


def writer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user_can_write():
            current_app.logger.warn(
                'User {user_id} attempted to perform a write action but does not have the WRITER role'.format(user_id=get_current_user_id()))
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def current_user_can_write():
    return current_app.config['LOGIN_DISABLED'] or current_user.can_write
