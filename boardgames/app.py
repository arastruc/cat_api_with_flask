
from flask import Flask
from flask_restplus import Api
from dao.db import db
from apis.boardgame import api as boardgame_api
from apis.author import api as author_api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/postgres'
app.config['ERROR_404_HELP'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(version='1.0', title='Board Game API',
          description='a simple flask API using sqllite as BDD')
db.init_app(app)
api.init_app(app)


api.add_namespace(boardgame_api, path='/v1/boardgames')
api.add_namespace(author_api, path='/v1/authors')
