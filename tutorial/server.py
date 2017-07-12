import flask
import flask_oauthlib.client
from flask_migrate import Migrate
import os

from tutorial.database import db
from tutorial.models import (
    Thing,
    User,
)

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
        user_id = flask.session.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        return user.github_token
    
    auth = flask.Blueprint('github_oauth', __name__)
    
    @auth.route('/login')
    def login():
        return github.authorize(callback=flask.url_for('github_oauth.authorized', _external=True))

    @auth.route('/logout')
    def logout():
        flask.session.pop('user_id')
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
        github_token = resp['access_token']
        github_profile = github.get('user', token=(github_token, None)).data
        user = User.query.filter_by(
            github_id=github_profile['id']
        ).first()

        if not user:
            user = User(
                username=github_profile['login'],
                github_id=github_profile['id'],
                github_token=github_token,
            )
            db.session.add(user)
            db.session.commit()

        flask.session['user_id'] = user.id
        return flask.redirect('/auth/profile')

    app.register_blueprint(auth, url_prefix='/auth')

    return app

def noauth_server():
    app = flask.Flask(__name__)
    app.secret_key = 'oooohhh secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'postgresql://postgres@localhost:5432/postgres')
    db.init_app(app)
    migrate = Migrate(app, db)

    return app