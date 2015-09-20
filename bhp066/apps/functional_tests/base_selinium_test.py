import unittest
from selenium import webdriver

from django.contrib.auth.models import User

from .pages.login_page import LoginPage


class BaseSeleniumTest(unittest.TestCase):

    username = 'testuser'
    password = '12345'
    email = 'testuser@123.org'

    def setUp(self):
        self.user = User.objects.create_superuser('testuser', self.email, self.password)
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.close()

    def login(self):
        self.login_page = LoginPage(self.browser)
        self.browser.get(self.login_page.url)
        self.login_page.login(self.username, self.password)
