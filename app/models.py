from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from .database import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(256))
    email = db.Column(db.String(64))
    description = db.Column(db.Text)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    # TypeError: ObjectId('552f41e56a85f00dd043406b') is not JSON serializable
    def get_id(self):
        return str(self.id)

    def __unicode__(self):
        return self.name

post_status = ((0, 'draft'), (1, 'published'))


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=True)
    status = db.Column(db.Integer)
    create_time= db.Column(db.DateTime, default=datetime.utcnow())
    modify_time= db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __unicode__(self):
        return self.title

    meta = {
        'ordering': ['-create_time']
    }

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(64), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), index=True, nullable=False)