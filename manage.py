from flask.ext.script import Manager, Server
from app import create_app
from app.models import User, Post
from werkzeug.security import generate_password_hash

app = create_app()
manager = Manager(app)

manager.add_command("runserver",
                    Server(host='0.0.0.0',
                           port=5000,
                           use_debugger=True))


@manager.option('-u', '--name', dest='name', default='admin')
@manager.option('-p', '--password', dest='password', default='123456')
def create_admin(name, password):
    admin = User(name=name, password=generate_password_hash(password))
    admin.save()


@manager.command
def add_post():
    user = User.objects(name="admin").first()
    post = Post(title="Hello", content="Hello Wolrd", author=user, tags=['python', 'flask'])
    post.save()


if __name__ == '__main__':
    manager.run()