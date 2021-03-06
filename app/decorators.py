from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.email_confirmed is False:
            return redirect(url_for('main.unconfirmed'))
        return func(*args, **kwargs)
    return decorated_function