import os
from flask.ext.script import Manager

from blog import app
from blog.models import Post
from blog.database import session

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
        
if __name__ == "__main__":
  manager.run()