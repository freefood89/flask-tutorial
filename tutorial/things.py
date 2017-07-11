import flask

bp = flask.Blueprint('things', __name__)

@bp.route('/v1/things/<int:id>', methods=['GET'])
def retrieve_thing_by_id(id):
    return flask.jsonify({
        'name': 'thing %d' % id,
    })

@bp.route('/v1/things')
def retrieve_all_things():
    things = [{'name': 'thing %d' % id} for id in range(10)]

    return flask.jsonify({
        'things': things,
    })

@bp.route('/v1/things', methods=['POST'])
def create_thing():
    return (
        flask.jsonify({'message': 'didnt really create thing'}),
        201,
    )

@bp.route('/v1/things/<int:id>', methods=['PUT'])
def update_thing(id):
    return (
        flask.jsonify({'message': 'didnt really modify thing'}),
        202,
    )

@bp.route('/v1/things/<int:id>', methods=['DELETE'])
def destroy_thing(id):
    user = flask.g.get('user', None)
    if not user:
        app.logger.info('stranger destroyed thing %d' % id)
    else:
        app.logger.info('%s destroyed thing %d' % (user['login'], id))
    return flask.jsonify({}), 204
