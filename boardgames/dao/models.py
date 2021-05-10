
from .db import db


class Boardgame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    boardgame_id = db.Column(db.String(200))
    name = db.Column(db.String(200), nullable=False)
    publisher = db.Column(db.String(200), nullable=False)
    minplayer = db.Column(db.Integer)
    maxplayer = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    author = db.Column(db.String(200), nullable=False)
