import flask
import sqlalchemy
from tutorial import app
from tutorial import db
from tutorial.models import User

# TODO - see if usage of sqlalchemy here follows best practices

@app.route('/v1/users/<username>', methods=['GET'])
def retrieve_users_by_id(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flask.abort(404)
    return flask.jsonify(user.serialize())

@app.route('/v1/users')
def retrieve_all_users():
    users = User.query.all()

    return flask.jsonify(
        users=[u.serialize() for u in users]
    )

@app.route('/v1/users', methods=['POST'])
def create_user():
    user = flask.request.get_json()

    try:
        db.session.add(User(
            username=user['username'],
            email=user['email']
        ))
        db.session.commit()
    except KeyError as e:
        flask.abort(400)
    except sqlalchemy.exc.IntegrityError as e:
        flask.abort(409)

    return (
        flask.jsonify({'message': 'successfully created user'}),
        201,
    )

@app.route('/v1/users/<username>', methods=['PUT'])
def update_user(username):
    updates = flask.request.get_json()
    user = User.query.filter_by(username=username).first()

    if not user:
        flask.abort(404)
    try:
        for k, v in updates.items():
            setattr(user, k, v)
        db.session.add(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        flask.abort(409)
    return (
        flask.jsonify({'message': 'successfully updated user'}),
        202,
    )
