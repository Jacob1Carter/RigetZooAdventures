import hashlib
import re

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def hash_password(password):
    password_hash = hashlib.md5(password.encode())

    return password_hash.hexdigest()


def validate_email(email):
    pattern = re.compile(r"[^@]+@[^@]+\.+[^@]+")

    if re.match(pattern, email):
        return True
    else:
        return False
