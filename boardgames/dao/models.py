
from .db import db


assoc_table = db.Table('author_boardgame',
                       db.Column('id', db.Integer,
                                 primary_key=True),
                       db.Column('author_id', db.Integer, db.ForeignKey(
                           'author.id'), primary_key=True),
                       db.Column('boardgame_id', db.Integer, db.ForeignKey(
                           'boardgame.id'), primary_key=True)
                       )


class Boardgame(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    boardgame_id = db.Column(db.String(200))
    name = db.Column(db.String(200), nullable=False)
    publisher = db.Column(db.String(200), nullable=False)
    minplayer = db.Column(db.Integer)
    maxplayer = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    authors = db.relationship('Author',
                              secondary=assoc_table,
                              lazy='subquery',
                              backref=db.backref('authors',
                                                 viewonly=True,
                                                 lazy=True,
                                                 ))


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.String(200))
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    nationality = db.Column(db.String(200), nullable=False)
    boardgames = db.relationship('Boardgame',
                                 secondary=assoc_table,
                                 viewonly=True,
                                 lazy='subquery',
                                 backref=db.backref(
                                     'boardgames',
                                      lazy=True,
                                 )
                                 )
