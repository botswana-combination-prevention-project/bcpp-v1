from selenium.webdriver.common.by import By


class BasePage(object):
    def __init__(self, browser):
        self.browser = browser


class BaseModelAdminPage(BasePage):
    save_button = (By.NAME, "_save")

    def click_save_button(self):
        self.browser.find_element(*BaseModelAdminPage.save_button).click()
