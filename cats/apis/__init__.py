from flask_restplus import Api
from .cat import api as cat_api

api = Api(version='1.0', title='Simple API',
          description='a simple flask API')


api.add_namespace(cat_api, path='/v1/cats')
