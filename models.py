from sqlalchemy import JSON
from datetime import datetime
from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_md5 = db.Column(db.String(120), nullable=False)
    tickets = db.Column(db.String(), default="")
    is_member = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    loyalty_points = db.Column(db.Float, default=0.0)
    is_admin = db.Column(db.Boolean, default=False)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_holder_id = db.Column(db.Integer, nullable=False)
    ticket_type = db.Column(db.String(120), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    date_expires = db.Column(db.DateTime, nullable=False)
    admit = db.Column(JSON, nullable=False)
    hotel_rooms = db.Column(db.String(), default="")
    cost = db.Column(db.Float, nullable=False)


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    species_name = db.Column(db.String(120), unique=True, nullable=False)
    api_name = db.Column(db.String(120), nullable=False)
    info = db.Column(db.String(), default="")
    individual_details = db.Column(JSON, nullable=False)
    image = db.Column(db.String(120), nullable=False)


class UserFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(), nullable=False)
    answer = db.Column(db.String(), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
