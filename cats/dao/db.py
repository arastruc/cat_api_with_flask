from flask_mongoengine import MongoEngine

me = MongoEngine()


def initialize_db(app):
    me.init_app(app)
