from selenium.webdriver.common.by import By


class BasePage(object):
    def __init__(self, browser):
        self.browser = browser
#         self.url = self.browser.get(self.live_server_url)


class BaseModelAdminPage(BasePage):
    save_button = (By.NAME, "_save")

    def click_save_button(self):
        self.browser.find_element(*BaseModelAdminPage.save_button).click()
