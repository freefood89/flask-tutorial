import flask

def authorize():
	user_id = flask.session.get('user_id')
	if not user_id:
		return 'Unauthorized'
	else:
		flask.g.user_id = user_id