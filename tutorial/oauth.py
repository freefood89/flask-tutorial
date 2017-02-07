import flask
import flask_oauthlib.client

from tutorial import app

oauth = flask_oauthlib.client.OAuth(app)
github = oauth.remote_app(
    'github',
    consumer_key='-',
    consumer_secret='-',
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

# TODO - need own user mgmt so I dont call github APIs all the time
@app.before_request
def attach_user():
    if 'github_token' in flask.session:
        flask.g.user = github.get('user').data
    else:
        flask.g.user = None

@github.tokengetter
def get_github_oauth_token():
    return flask.session.get('github_token')

@app.route('/auth/login')
def login():
    return github.authorize(callback=flask.url_for('authorized', _external=True))

@app.route('/auth/logout')
def logout():
    flask.session.pop('github_token', None)
    return flask.redirect('/')

@app.route('/auth/login/authorized')
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

@app.route('/auth/profile')
def get_user_profile():
    if 'github_token' in flask.session:
        print(flask.session.get('github_token'))
        user_data = github.get('user').data
        return flask.jsonify(user_data)
    flask.abort(401)

