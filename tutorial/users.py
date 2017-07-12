import flask
import github3

from tutorial.auth import authorize
from tutorial.database import db
from tutorial.models import User

# TODO - see if usage of sqlalchemy here follows best practices
bp = flask.Blueprint('users', __name__)

bp.before_request(authorize)

@bp.route('/v1/user', methods=['GET'])
def retrieve_self():
    user = User.query.filter_by(id=flask.g.user_id).first()
    return flask.jsonify(user.to_dict())

@bp.route('/v1/user/profile', methods=['GET'])
def retrieve_own_github_profile():
    user = User.query.filter_by(id=flask.g.user_id).first()
    gh = github3.login(token=user.github_token)

    return flask.jsonify(github_profile=gh.user().to_json())

@bp.route('/v1/users/<int:id>', methods=['GET'])
def retrieve_users_by_id(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        flask.abort(404)
    return flask.jsonify(user.serialize())

@bp.route('/v1/users')
def retrieve_all_users():
    users = User.query.all()

    return flask.jsonify(
        users=[u.to_dict() for u in users]
    )
