from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    url = "http://localhost:8000/login/"
    username = (By.ID, 'id_username')
    password = (By.ID, 'id_password')
    login_button = (By.XPATH, "//div[@class='submit-row']/input")
    login_error = (By.ID, 'login_message')

    def set_username(self, username):
        usernameElement = self.browser.find_element(*LoginPage.username)
        usernameElement.send_keys(username)

    def set_password(self, password):
        passwordElement = self.browser.find_element(*LoginPage.password)
        passwordElement.send_keys(password)

    def click_login(self):
        self.browser.find_element(*LoginPage.login_button).click()

    def authentication_failed(self):
        notifcationElement = self.browser.find_element(*LoginPage.login_error)
        return notifcationElement.is_displayed()

    def login(self, username, password):
        self.set_username(username)
        self.set_password(password)
        self.click_login()
