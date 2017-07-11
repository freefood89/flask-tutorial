import flask
import flask_oauthlib.client
from flask_migrate import Migrate
import os

from tutorial.database import db

def oauth_server():
    app = noauth_server()
    oauth = flask_oauthlib.client.OAuth(app)
    github = oauth.remote_app(
        'github',
        consumer_key=os.environ.get('GITHUB_CLIENT'),
        consumer_secret=os.environ.get('GITHUB_SECRET'),
        request_token_params={'scope': 'user:email'},
        base_url='https://api.github.com',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize'
    )

    @github.tokengetter
    def get_github_oauth_token():
        return flask.session.get('github_token')
    
    auth = flask.Blueprint('github_oauth', __name__)
    
    @auth.route('/login')
    def login():
        return github.authorize(callback=flask.url_for('github_oauth.authorized', _external=True))

    @auth.route('/logout')
    def logout():
        flask.session.pop('github_token', None)
        return flask.redirect('/')

    @auth.route('/authorized')
    def authorized():
        resp = github.authorized_response()
        if resp is None or resp.get('access_token') is None:
            return 'Access denied: reason=%s error=%s resp=%s' % (
                flask.request.args['error'],
                flask.request.args['error_description'],
                resp
            )
        flask.session['github_token'] = (resp['access_token'], '')
        return flask.redirect('/auth/profile')

    app.register_blueprint(auth, url_prefix='/auth')

    return app

def noauth_server():
    app = flask.Flask(__name__)
    app.secret_key = 'oooohhh secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
    db.init_app(app)
    migrate = Migrate(app, db)

    return app