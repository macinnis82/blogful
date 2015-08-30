import os
import unittest
from urlparse import urlparse

from werkzeug.security import generate_password_hash

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session

class TestViews(unittest.TestCase):
  def setUp(self):
    """ Test Setup """
    self.client = app.test_client()
    
    # Set up the tables in the database
    Base.metadata.create_all(engine)
    
    # Create an example user
    self.user = models.User(
      name="Alice",
      email="alice@example.com",
      password=generate_password_hash("test")
    )
    
    session.add(self.user)
    session.commit()
    
  def tearDown(self):
    """ Test Teardown """
    session.close()
    
    # Remove the tables and their data from the database
    Base.metadata.drop_all(engine)
    
  def simulate_login(self):
    """ mimics what Flask-Login looks for when determining whether a user is logged in """
    with self.client.session_transaction() as http_session:
      http_session["user_id"] = str(self.user.id)
      http_session["_fresh"] = True
  
  def test_add_post(self):
    self.simulate_login()
    
    response = self.client.post("/post/add", data={
      "title": "Test Post",
      "content": "Test content"
    })
    
    self.assertEqual(response.status_code, 302)
    self.assertEqual(urlparse(response.location).path, "/")
    posts = session.query(models.Post).all()
    self.assertEqual(len(posts), 1)
    
    post = posts[0]
    self.assertEqual(post.title, "Test Post")
    # self.assertEqual(post.content, "<p>Test content</p>\n")
    self.assertEqual(post.content, "Test content")
    self.assertEqual(post.author, self.user)
    
  # test edit post when user logged in
  def test_edit_post(self):
    self.simulate_login()
    
    test_post = models.Post(
      title="Test Post",
      content="Test Content",
      author_id=self.user.id
    )
    session.add(test_post)
    session.commit()
    
    response = self.client.post("/post/edit/1", data={
      "title": "Edit Post",
      "content": "Edit content"
    })
    
    self.assertEqual(response.status_code, 302)
    self.assertEqual(urlparse(response.location).path, "/")
    posts = session.query(models.Post).all()
    self.assertEqual(len(posts), 1)
    
    post = posts[0]
    self.assertEqual(post.title, "Edit Post")
    # self.assertEqual(post.content, "<p>Edit content</p>\n")
    self.assertEqual(post.content, "Edit content")
    self.assertEqual(post.author, self.user)
  
  # test logged out users cannot delete things
  def test_delete_post_logout(self):
    pass
  
  # test users cannot delete posts they didn't author
  def test_delete_post_not_author(self):
    pass
  
  # test user can delete their own posts
  def test_delete_post(self):

    test_post = models.Post(
      title="Test Post",
      content="Test Content",
      author_id=self.user.id
    )
    session.add(test_post)
    session.commit()
    post_id=test_post.id
    
    self.simulate_login()
    response = self.client.post("/post/delete/{}".format(post_id))

    """ self.assertEqual(response.status_code, 302) AssertionError: 405 != 302 """
    self.assertEqual(response.status_code, 302)
    self.assertEqual(urlparse(response.location).path, "/")
    posts = session.query(models.Post).all()
    self.assertEqual(len(posts), 0)
  
if __name__ == "__main__":
  unittest.main()