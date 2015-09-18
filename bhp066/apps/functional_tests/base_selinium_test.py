from selenium import webdriver

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

from .pages.login_page import LoginPage


class BaseSeleniumTest(StaticLiveServerTestCase):

    username = 'testuser'
    password = '12345'
    email = 'testuser@123.org'

    def setUp(self):
        User.objects.create_superuser(self.username, self.email, self.password)
        super().setUp()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

    def tearDown(self):
        self.browser.quit()

    def login(self):
        self.login_page = LoginPage(self.browser)
        self.login_page.login(self.username, self.password)
