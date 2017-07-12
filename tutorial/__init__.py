from tutorial.database import db

from tutorial import (
    server,
    users,
    things,
)

app = server.oauth_server()

@app.route('/')
def index():
    user = flask.session.get('user_id')
    if not user:
        return 'Welcome stranger'

    return 'Welcome ' + user['login']

@app.route('/v1/health')
def health_check():
    return 'OK'

app.register_blueprint(users.bp)
app.register_blueprint(things.bp)
