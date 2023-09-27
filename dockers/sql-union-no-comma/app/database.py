from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String(), unique=False)
    email = db.Column(db.String(), unique=True)
    posts = db.relationship('Posts', back_populates="author")
        
    def __repr__(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True)
    body = db.Column(db.String(), unique=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id')) 
    author = db.relationship('Users', back_populates="posts")
    
    def __repr__(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}