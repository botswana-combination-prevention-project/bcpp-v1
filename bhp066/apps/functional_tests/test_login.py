import time

from .base_selinium_test import BaseSeleniumTest


class LoginSeleniumTest(BaseSeleniumTest):

    def test_success_login(self):
        self.login()
        time.sleep(1)
        self.assertIn('/home/', self.browser.current_url)
