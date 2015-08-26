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
    
    # set up the tables in the database
    Base.metadata.create_all(engine)
    
    # create an example user
    self.user = models.User(
      name="Alice",
      email="alice@example.com",
      password=generate_password_hash("test")
    )
    
    session.add(self.user)
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
    
  def test_login_correct(self):
    # self.browser.visit("http://0.0.0.0:8080/login")
    self.browser.visit("http://127.0.0.1:5000/login")
    self.browser.fill("email", "alice@example.com")
    self.browser.fill("password", "test")
    button = self.browser.find_by_css("button[type=submit]")
    button.click()
    # self.assertEqual(self.browser.url, "http://0.0.0.0:8080/")
    self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")
    
  def test_login_incorrect(self):
    # self.browser.visit("http://0.0.0.0:8080/login")
    self.browser.visit("http://127.0.0.1:5000/login")
    self.browser.fill("email", "bob@example.com")
    self.browser.fill("password", "test")
    button = self.browser.find_by_css("button[type=submit]")
    button.click()
    # self.assertEqual(self.browser.url, "http://0.0.0.0:8080/login")
    self.assertEqual(self.browser.url, "http://127.0.0.1:5000/login")
    
if __name__ == "__main__":
  unittest.main()