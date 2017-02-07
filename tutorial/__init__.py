import flask
import logging

app = flask.Flask(__name__)
app.secret_key = 'oooohhh secret'

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
stream_handler.setFormatter(formatter)

app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)

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
