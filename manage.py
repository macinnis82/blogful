import os

from flask.ext.script import Manager
from getpass import getpass
from werkzeug.security import generate_password_hash
from flask.ext.migrate import Migrate, MigrateCommand

from blog import app
from blog.models import Post, User
from blog.database import session, Base

manager = Manager(app)

@manager.command
def run():
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)
  
@manager.command
def seed():
  content = """Roof party literally farm-to-table, Tumblr Austin selfies letterpress forage craft beer squid cronut drinking vinegar."""
  
  for i in range(25):
    post = Post(
      title = "Test Post #{}".format(i),
      content=content
    )
    session.add(post)
    
  session.commit()
  
@manager.command
def adduser():
  name = raw_input("Name: ")
  email = raw_input("Email: ")
  if session.query(User).filter_by(email=email).first():
    print "User with that email address already exists"
    return
  
  password = ""
  password_2 = ""
  while not(password and password_2) or password != password_2:
    password = getpass("Password: ")
    password_2 = getpass("Re-enter Password: ")
  
  user = User(
    name=name, 
    email=email, 
    password=generate_password_hash(password)
  )
  session.add(user)
  session.commit()
  
class DB(object):
  def __init__(self, metadata):
    self.metadata = metadata
    
migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)
  
if __name__ == "__main__":
  manager.run()