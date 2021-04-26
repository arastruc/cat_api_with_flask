from flask_restplus import Api
from .character import api as character_api
from .cat import api as cat_api

api = Api(version='1.0', title='Simple API',
          description='a simple flask API')


api.add_namespace(character_api, path='/v1/characters')
api.add_namespace(cat_api, path='/v1/cats')
