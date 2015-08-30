import os
import unittest
import multiprocessing
import time
from urlparse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session

class TestViews(unittest.TestCase):
  def setUp(self):
    """ Test Setup """
    self.browser = Browser("phantomjs")
    self.browser.driver.set_window_size(1440, 900) # set browser size.
    
    # set up the tables in the database
    Base.metadata.create_all(engine)
    
    # create 2 example users
    self.user = models.User(name="Alice", email="alice@example.com", password=generate_password_hash("test"))
    session.add(self.user)
    session.commit()
    
    self.user2 = models.User(name="Ryan", email="macinnis82@gmail.com", password=generate_password_hash("test"))
    session.add(self.user2)
    session.commit()
    
    # Create some sample posts
    content = "Acceptance testing content"
    for i in range (5):
      post = models.Post(title="Acceptance test post #{}".format(i+1), content=content, author=self.user)
      session.add(post)
    session.commit()    
    
    """ gives the ability to start and run other code simultaneously with your own scripts """
    self.process = multiprocessing.Process(target=app.run)
    self.process.start()
    # pause for 1 second
    time.sleep(1)
    
  def tearDown(self):
    """ Test Teardown """
    # Remove the tables and their data from the database
    self.process.terminate()
    session.close()
    engine.dispose()
    Base.metadata.drop_all(engine)
    self.browser.quit()
    
  def login(self, email, password):
    self.browser.visit("http://127.0.0.1:5000/login")
    self.browser.fill("email", email)
    self.browser.fill("password", password)
    button = self.browser.find_by_css("button[type=submit]")
    button.click()    
    
  def test_login_correct(self):
    self.login(email="alice@example.com", password="test")
    self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")
    
  def test_login_incorrect(self):
    self.login(email="bob@example.com", password="test")
    self.assertEqual(self.browser.url, "http://127.0.0.1:5000/login")
    
  # def test_add_post(self):
  #   self.login(email="alice@example.com", password="test")
  #   self.browser.visit("http://127.0.0.1:5000/post/add")
  #   self.browser.fill("title", "new title")
  #   self.browser.fill("content", "new content")
  #   button = self.browser.find_by_css("button[type=submit]")
  #   button.click()
  #   self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")
  #   self.assertTrue(self.browser.is_text_present("new title"))
  #   self.assertTrue(self.browser.is_text_present("new content")) 
    
  # def test_edit_post_as_author(self):
  #   self.login(email="alice@example.com", password="test")
  #   self.browser.visit("http://127.0.0.1:5000/post/edit/3")
  #   self.assertEqual(self.browser.url, "http://127.0.0.1:5000/post/edit/3")
  #   self.browser.fill("title", "edited title")
  #   time.sleep(2)
  #   self.browser.fill("content", "edited content")
  #   button = self.browser.find_by_css("button[type=submit]")
  #   button.click()
  #   self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")
  #   self.assertTrue(self.browser.is_text_present("edited title"))
  #   self.assertTrue(self.browser.is_test_present("edited content"))
    
  def test_edit_post_not_as_author(self):
    self.login(email="macinnis82@gmail.com", password="test")
    self.browser.visit("http://0.0.0.0:8080/post/edit/2")
    self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")  
    
if __name__ == "__main__":
  unittest.main()