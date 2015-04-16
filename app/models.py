from flask.ext.mongoengine import MongoEngine
from datetime import datetime

db = MongoEngine()


class User(db.Document):
    name = db.StringField(required=True, max_length=64)
    password = db.StringField(max_length=256)
    email = db.StringField(max_length=64)
    description = db.StringField(max_length=1024)

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


class Post(db.Document):
    title = db.StringField(required=True, max_length=64)
    content = db.StringField(required=True)
    author = db.ReferenceField(User)
    tags = db.ListField(db.StringField(max_length=32))
    status = db.IntField(required=True, choices=post_status)
    create_time = db.DateTimeField(default=datetime.now)
    modify_time = db.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.title

    meta = {
        'ordering': ['-create_time']
    }