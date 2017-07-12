import flask

from tutorial.auth import authorize
from tutorial.database import db
from tutorial.models import (
    Thing,
    User,
)

bp = flask.Blueprint('things', __name__)
bp.before_request(authorize)

@bp.route('/v1/things/<int:id>', methods=['GET'])
def retrieve_thing_by_id(id):
    user = User.query.filter_by(id=flask.g.user_id).first()
    thing = user.things.filter_by(id=id).first()

    if not thing:
        return 'Not Found', 404

    return flask.jsonify(thing.to_dict())

@bp.route('/v1/things')
def retrieve_all_things():
    user = User.query.filter_by(id=flask.g.user_id).first()
    things = [t.to_dict()
        for t
        in user.things.all()
    ]

    return flask.jsonify({
        'things': things,
    })

@bp.route('/v1/things', methods=['POST'])
def create_thing():
    payload = flask.request.get_json()
    thing = Thing(
        name=payload['name'],
        owner=flask.g.user_id,
    )
    db.session.add(thing)
    db.session.commit()

    return (
        flask.jsonify({
            'message': 'created', 
            'thing': thing.to_dict(),
        }),
        201,
    )

@bp.route('/v1/things/<int:id>', methods=['PUT'])
def update_thing(id):
    user = User.query.filter_by(id=flask.g.user_id).first()
    thing = user.things.filter_by(id=id).first()

    updates = flask.request.get_json()
    
    # TODO - there's probably a better way to do this
    if 'name' in updates:
        thing.name = updates['name']
        db.session.add(thing)
        db.session.commit()
        return (
            flask.jsonify({
                'message': 'updated thing',
                'thing': thing.to_dict(),
            }),
            202,
        )
    return 'Invalid Input', 400
