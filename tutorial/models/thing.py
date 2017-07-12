from tutorial.database import db

class Thing(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	owner = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, name, owner):
		self.name = name
		self.owner = owner

	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'owner': self.owner,
		}
