from tutorial.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    github_id = db.Column(db.Integer, unique=True)
    github_token = db.Column(db.String)
    things = db.relationship('Thing', backref='user', lazy='dynamic')

    def __init__(self, username, github_id, github_token):
        self.username = username
        self.github_id = github_id
        self.github_token = github_token

    def __repr__(self):
        return '<User %r>' % self.username

    def to_dict(self):
        return {
            'id': self.id, 
            'username': self.username,
            'github_id': self.github_id,
        }
