import flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import os

app = flask.Flask(__name__)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
stream_handler.setFormatter(formatter)
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)

app.secret_key = 'oooohhh secret'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    user = flask.g.get('user', None)
    if not user:
        return 'Welcome stranger'

    return 'Welcome ' + user['login']

@app.route('/v1/health')
def health_check():
    return 'OK'

import tutorial.oauth
import tutorial.things
import tutorial.users
