from flask import Flask
from apis import api

from dao.db import initialize_db

app = Flask(__name__)
api.init_app(app)


app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database',
    'host': 'localhost',
    'port': 27017
}

initialize_db(app)
