from functools import wraps
from flask import session, redirect

def login_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        if "token" not in session:
            return redirect("/login")

        return f(*args, **kwargs)

    return wrapper


def role_required(required_role):

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):

            if "token" not in session:
                return redirect("/login")

            if session.get("role") != required_role:
                return redirect("/")

            return f(*args, **kwargs)

        return wrapper

    return decorator